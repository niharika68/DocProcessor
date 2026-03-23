import os
import json

import boto3

from .renderer import render_pages, PageRender
from .textract import (
    analyze_page,
    parse_blocks,
    tables_to_markdown,
    norm_to_px,
    words_union_bbox,
)
from .prompts import DOC_CONFIGS
from ..models.schemas import Annotation, BboxNorm, BboxPx

CATEGORY_MAP = {
    "key_fields": "key_field",
    "items": "line_item",
    "flags": "anomaly",
}

BATCH_SIZE = 5  # Max pages sent to the AI in a single call


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))


def _merge_ai_results(batches: list[dict]) -> dict:
    """Merge results from multiple AI batch calls into one unified result."""
    merged_key_fields: dict[str, dict] = {}
    merged_items: list[dict] = []
    merged_flags: list[dict] = []

    for batch in batches:
        for kf in batch.get("key_fields", []):
            field = kf.get("field", "")
            if field and field not in merged_key_fields:
                merged_key_fields[field] = kf
        merged_items.extend(batch.get("items", []))
        merged_flags.extend(batch.get("flags", []))

    return {
        "key_fields": list(merged_key_fields.values()),
        "items": merged_items,
        "flags": merged_flags,
    }


def run_pipeline(pdf_bytes: bytes, doc_type: str = "invoice") -> dict:
    """
    Full document processing pipeline:
    1. Render PDF pages to PNG
    2. Run Textract on each page
    3. Send images + structured text to Nova Pro for semantic analysis
       (batched in groups of BATCH_SIZE for large documents)
    4. Map source_words back to Textract bboxes
    Returns dict with pages (image + annotations) and summary.
    """
    config = DOC_CONFIGS[doc_type]

    # Step 1: Render
    pages = render_pages(pdf_bytes, scale=2.0)

    # Step 2: Textract
    all_structured = []
    for page in pages:
        blocks = analyze_page(page.png_bytes)
        structured = parse_blocks(blocks)
        all_structured.append(structured)

    # Step 3: AI analysis (batched if needed)
    if len(pages) <= BATCH_SIZE:
        ai_result = _call_ai(pages, all_structured, config["system_prompt"], doc_type)
    else:
        batch_results = []
        for batch_start in range(0, len(pages), BATCH_SIZE):
            batch_pages = pages[batch_start: batch_start + BATCH_SIZE]
            batch_structured = all_structured[batch_start: batch_start + BATCH_SIZE]

            # Carry last page of previous batch as context (if not the first batch)
            if batch_start > 0:
                context_page = pages[batch_start - 1]
                context_structured = all_structured[batch_start - 1]
            else:
                context_page = None
                context_structured = None

            result = _call_ai(
                batch_pages,
                batch_structured,
                config["system_prompt"],
                doc_type,
                context_page=context_page,
                context_structured=context_structured,
            )
            batch_results.append(result)

        ai_result = _merge_ai_results(batch_results)

    # Step 4: Map coordinates + build annotations per page
    page_annotations: dict[int, list[Annotation]] = {p.page_number: [] for p in pages}

    for category_key, category_label in CATEGORY_MAP.items():
        for item in ai_result.get(category_key, []):
            page_num = item.get("page", 1)
            page_idx = min(page_num - 1, len(pages) - 1)
            page = pages[page_idx]
            words = all_structured[page_idx]["words"]

            source_words = item.get("source_words", [])
            bbox_n = words_union_bbox(source_words, words)
            # Discard bboxes that are unreasonably large (words scattered across page)
            if bbox_n is None or bbox_n["Width"] > 0.8 or bbox_n["Height"] > 0.15:
                bbox_n = {"Left": 0.0, "Top": 0.0, "Width": 0.0, "Height": 0.0}

            bbox_px = norm_to_px(bbox_n, page.width_px, page.height_px)

            if category_key == "key_fields":
                label = item.get("field", "")
                value = item.get("value", "")
            elif category_key == "items":
                label = _item_label(item, config)
                value = _item_value(item, config)
            else:
                label = item.get("type", "")
                value = item.get("description", "")

            page_annotations[page.page_number].append(Annotation(
                category=category_label,
                label=label,
                value=value,
                bbox_norm=BboxNorm(
                    left=bbox_n["Left"],
                    top=bbox_n["Top"],
                    width=bbox_n["Width"],
                    height=bbox_n["Height"],
                ),
                bbox_px=BboxPx(
                    x0=bbox_px["x0"],
                    y0=bbox_px["y0"],
                    x1=bbox_px["x1"],
                    y1=bbox_px["y1"],
                ),
            ))

    summary = {
        "key_fields": {
            item["field"]: item["value"]
            for item in ai_result.get("key_fields", [])
        },
        "items": ai_result.get("items", []),
        "flags": ai_result.get("flags", []),
    }

    return {
        "pages": pages,
        "page_annotations": page_annotations,
        "summary": summary,
    }


def _item_label(item: dict, config: dict) -> str:
    keys = config["items_keys"]
    return item.get(keys[0], "") if keys else ""


def _item_value(item: dict, config: dict) -> str:
    keys = config["items_keys"][1:]
    cols = config["items_columns"][1:]
    parts = [f"{col}={item.get(key, '')}" for col, key in zip(cols, keys) if item.get(key)]
    return "  ".join(parts)


def _call_ai(
    pages: list[PageRender],
    all_structured: list[dict],
    system_prompt: str,
    doc_type: str,
    context_page: "PageRender | None" = None,
    context_structured: "dict | None" = None,
) -> dict:
    client = get_bedrock_client()
    model_id = os.getenv("MODEL_ARN") or os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0")

    content = []

    # If a context page from the previous batch is provided, prepend it as read-only context
    if context_page is not None and context_structured is not None:
        content.append({
            "image": {
                "format": "png",
                "source": {"bytes": context_page.png_bytes},
            }
        })
        kv_text = "\n".join(
            f"  {p['key']}: {p['value']}"
            for p in context_structured["key_value_pairs"]
        )
        tables_md = tables_to_markdown(context_structured["tables"])
        content.append({
            "text": (
                f"--- Context: Previous Batch Last Page (page {context_page.page_number}) ---\n"
                f"Key-Value Pairs:\n{kv_text or '  (none)'}\n\n"
                f"Tables:\n{tables_md or '  (none)'}\n"
                "NOTE: Do NOT extract items from this context page — it is included for continuity only.\n"
            )
        })

    for page, structured in zip(pages, all_structured):
        content.append({
            "image": {
                "format": "png",
                "source": {"bytes": page.png_bytes},
            }
        })

        kv_text = "\n".join(
            f"  {p['key']}: {p['value']}"
            for p in structured["key_value_pairs"]
        )
        tables_md = tables_to_markdown(structured["tables"])
        lines_text = "\n".join(f"  {line}" for line in structured["lines"][:50])

        content.append({
            "text": (
                f"--- Page {page.page_number} Textract Output ---\n"
                f"Key-Value Pairs:\n{kv_text or '  (none)'}\n\n"
                f"Tables:\n{tables_md or '  (none)'}\n\n"
                f"Text Lines (first 50):\n{lines_text}"
            )
        })

    content.append({"text": f"Now analyze this {doc_type} document and return the JSON as specified."})

    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": content}],
    )

    raw = response["output"]["message"]["content"][0]["text"]
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]

    return json.loads(raw)
