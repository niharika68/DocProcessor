import base64
import json
import logging
import os
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .processing.pipeline import run_pipeline
from .processing.annotator import annotate_pdf
from .processing.prompts import SUPPORTED_DOC_TYPES
from .models.schemas import ProcessResponse, PageResult, Summary

log = logging.getLogger(__name__)

app = FastAPI(title="Invoice Processor")

# ── Security constants ────────────────────────────────────────────────────────
MAX_FILE_SIZE = 50 * 1024 * 1024   # 50 MB
SESSION_TTL   = 60 * 60            # 1 hour in seconds

# In-memory session store: session_id -> {pdf_bytes, summary, doc_type, created_at}
_sessions: dict[str, dict] = {}


def _purge_expired_sessions() -> None:
    """Remove sessions older than SESSION_TTL."""
    cutoff = time.time() - SESSION_TTL
    expired = [sid for sid, s in _sessions.items() if s["created_at"] < cutoff]
    for sid in expired:
        del _sessions[sid]


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/auth/check")
async def auth_check():
    """Returns whether a password is required to use the app."""
    return {"required": bool(os.getenv("VITE_APP_PASSWORD"))}


class AuthRequest(BaseModel):
    password: str


@app.post("/api/auth/login")
async def auth_login(body: AuthRequest):
    """Validates the submitted password against the VITE_APP_PASSWORD env var."""
    expected = os.getenv("VITE_APP_PASSWORD")
    if not expected or body.password == expected:
        return {"ok": True}
    raise HTTPException(status_code=401, detail="Incorrect password.")


@app.post("/api/process", response_model=ProcessResponse)
async def process_invoice(
    file: UploadFile = File(...),
    doc_type: str = Query(default="invoice"),
):
    if doc_type not in SUPPORTED_DOC_TYPES:
        raise HTTPException(status_code=400, detail=f"doc_type must be one of {SUPPORTED_DOC_TYPES}")
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    pdf_bytes = await file.read()

    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 50 MB.")
    if not pdf_bytes.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="File does not appear to be a valid PDF.")

    try:
        result = run_pipeline(pdf_bytes, doc_type=doc_type)
    except Exception:
        log.exception("Pipeline error")
        raise HTTPException(status_code=500, detail="An error occurred while processing your document.")

    pages_out: list[PageResult] = []
    for page in result["pages"]:
        b64 = base64.b64encode(page.png_bytes).decode()
        annotations = result["page_annotations"].get(page.page_number, [])
        pages_out.append(PageResult(
            page_number=page.page_number,
            image_b64=b64,
            image_width_px=page.width_px,
            image_height_px=page.height_px,
            annotations=annotations,
        ))

    summary_data = result["summary"]
    summary = Summary(
        key_fields=summary_data["key_fields"],
        items=summary_data["items"],
        flags=summary_data["flags"],
    )

    # Purge stale sessions before adding a new one
    _purge_expired_sessions()

    session_id = str(uuid.uuid4())
    _sessions[session_id] = {
        "pdf_bytes": pdf_bytes,
        "summary": summary_data,
        "doc_type": doc_type,
        "created_at": time.time(),
    }

    return ProcessResponse(
        session_id=session_id,
        doc_type=doc_type,
        pages=pages_out,
        summary=summary,
    )


@app.get("/api/export/{session_id}")
async def export_json(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    return JSONResponse(
        content=session["summary"],
        headers={"Content-Disposition": f"attachment; filename={session['doc_type']}_{session_id[:8]}.json"},
    )


@app.get("/api/download/{session_id}")
async def download_annotated(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        pdf_bytes = session["pdf_bytes"]
        result = run_pipeline(pdf_bytes, doc_type=session["doc_type"])
        annotated = annotate_pdf(pdf_bytes, result["page_annotations"])
    except Exception:
        log.exception("Annotation error")
        raise HTTPException(status_code=500, detail="An error occurred while generating the annotated PDF.")

    return Response(
        content=annotated,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=annotated_{session_id[:8]}.pdf"},
    )


# Serve React frontend (built to frontend/dist)
_dist = Path(__file__).parent.parent / "frontend" / "dist"
if _dist.exists():
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="static")
