import base64
import json
import logging
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

log.info("AWS_REGION        = %s", os.getenv("AWS_REGION", "NOT SET"))
log.info("BEDROCK_MODEL_ID  = %s", os.getenv("BEDROCK_MODEL_ID", "NOT SET"))
log.info("AWS_ACCESS_KEY_ID = %s", "SET" if os.getenv("AWS_ACCESS_KEY_ID") else "NOT SET")
log.info("AWS_SECRET_ACCESS_KEY = %s", "SET" if os.getenv("AWS_SECRET_ACCESS_KEY") else "NOT SET")

from .processing.pipeline import run_pipeline
from .processing.annotator import annotate_pdf
from .processing.prompts import SUPPORTED_DOC_TYPES
from .models.schemas import ProcessResponse, PageResult, Summary

app = FastAPI(title="Invoice Processor")

# In-memory session store: session_id -> {pdf_bytes, summary, doc_type}
_sessions: dict[str, dict] = {}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


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

    try:
        result = run_pipeline(pdf_bytes, doc_type=doc_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

    session_id = str(uuid.uuid4())
    _sessions[session_id] = {
        "pdf_bytes": pdf_bytes,
        "summary": summary_data,
        "doc_type": doc_type,
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Response(
        content=annotated,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=annotated_{session_id[:8]}.pdf"},
    )


# Serve React frontend (built to frontend/dist)
_dist = Path(__file__).parent.parent / "frontend" / "dist"
if _dist.exists():
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="static")
