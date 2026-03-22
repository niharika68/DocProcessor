import os
import boto3
from typing import Any

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

_textract_client = None


def get_textract_client():
    global _textract_client
    if _textract_client is None:
        _textract_client = boto3.client("textract", region_name=AWS_REGION)
    return _textract_client


def analyze_page(png_bytes: bytes) -> list[dict]:
    """Call Textract AnalyzeDocument on a single page PNG. Returns raw blocks."""
    client = get_textract_client()
    response = client.analyze_document(
        Document={"Bytes": png_bytes},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return response["Blocks"]


def parse_blocks(blocks: list[dict]) -> dict:
    """
    Parse raw Textract blocks into structured output:
    - words: {block_id: {text, bbox_norm}}
    - lines: [text]
    - key_value_pairs: [{key, value}]
    - tables: [[[cell_text]]]  — list of tables, each is list of rows, each row is list of cell strings
    """
    block_map: dict[str, dict] = {b["Id"]: b for b in blocks}

    words: dict[str, dict] = {}
    lines: list[str] = []
    key_value_pairs: list[dict] = []
    tables: list[list[list[str]]] = []

    for block in blocks:
        btype = block.get("BlockType")
        bbox = block.get("Geometry", {}).get("BoundingBox", {})

        if btype == "WORD":
            words[block["Id"]] = {
                "text": block.get("Text", ""),
                "bbox_norm": {
                    "Left": bbox.get("Left", 0),
                    "Top": bbox.get("Top", 0),
                    "Width": bbox.get("Width", 0),
                    "Height": bbox.get("Height", 0),
                },
            }

        elif btype == "LINE":
            lines.append(block.get("Text", ""))

        elif btype == "KEY_VALUE_SET" and block.get("EntityTypes", []) == ["KEY"]:
            key_text = _get_text_from_relationships(block, block_map, "CHILD")
            value_block_id = _get_related_id(block, "VALUE")
            value_text = ""
            if value_block_id and value_block_id in block_map:
                value_text = _get_text_from_relationships(
                    block_map[value_block_id], block_map, "CHILD"
                )
            if key_text:
                key_value_pairs.append({"key": key_text, "value": value_text})

        elif btype == "TABLE":
            table = _parse_table(block, block_map)
            if table:
                tables.append(table)

    return {
        "words": words,
        "lines": lines,
        "key_value_pairs": key_value_pairs,
        "tables": tables,
    }


def _get_text_from_relationships(
    block: dict, block_map: dict, rel_type: str
) -> str:
    texts = []
    for rel in block.get("Relationships", []):
        if rel["Type"] == rel_type:
            for child_id in rel["Ids"]:
                child = block_map.get(child_id, {})
                if child.get("BlockType") == "WORD":
                    texts.append(child.get("Text", ""))
    return " ".join(texts)


def _get_related_id(block: dict, rel_type: str) -> str | None:
    for rel in block.get("Relationships", []):
        if rel["Type"] == rel_type and rel["Ids"]:
            return rel["Ids"][0]
    return None


def _parse_table(
    table_block: dict, block_map: dict
) -> list[list[str]]:
    cells: dict[tuple[int, int], str] = {}
    max_row = 0
    max_col = 0

    for rel in table_block.get("Relationships", []):
        if rel["Type"] == "CHILD":
            for cell_id in rel["Ids"]:
                cell = block_map.get(cell_id, {})
                if cell.get("BlockType") == "CELL":
                    r = cell.get("RowIndex", 1)
                    c = cell.get("ColumnIndex", 1)
                    text = _get_text_from_relationships(cell, block_map, "CHILD")
                    cells[(r, c)] = text
                    max_row = max(max_row, r)
                    max_col = max(max_col, c)

    if not cells:
        return []

    table = []
    for r in range(1, max_row + 1):
        row = [cells.get((r, c), "") for c in range(1, max_col + 1)]
        table.append(row)
    return table


def tables_to_markdown(tables: list[list[list[str]]]) -> str:
    """Convert parsed tables to markdown for the prompt."""
    parts = []
    for i, table in enumerate(tables):
        parts.append(f"**Table {i + 1}:**")
        if not table:
            continue
        header = "| " + " | ".join(table[0]) + " |"
        separator = "| " + " | ".join(["---"] * len(table[0])) + " |"
        rows = [header, separator]
        for row in table[1:]:
            rows.append("| " + " | ".join(row) + " |")
        parts.append("\n".join(rows))
    return "\n\n".join(parts)


def norm_to_px(bbox_norm: dict, image_width_px: int, image_height_px: int) -> dict:
    """Convert normalized Textract bbox to pixel coordinates."""
    return {
        "x0": round(bbox_norm["Left"] * image_width_px),
        "y0": round(bbox_norm["Top"] * image_height_px),
        "x1": round((bbox_norm["Left"] + bbox_norm["Width"]) * image_width_px),
        "y1": round((bbox_norm["Top"] + bbox_norm["Height"]) * image_height_px),
    }


def words_union_bbox(word_texts: list[str], words: dict[str, dict]) -> dict | None:
    """
    Find all WORD blocks matching any of the given texts and return
    the union bounding box (normalized).
    """
    matched = [
        w["bbox_norm"]
        for w in words.values()
        if w["text"] in word_texts
    ]
    if not matched:
        return None

    left = min(b["Left"] for b in matched)
    top = min(b["Top"] for b in matched)
    right = max(b["Left"] + b["Width"] for b in matched)
    bottom = max(b["Top"] + b["Height"] for b in matched)

    return {
        "Left": left,
        "Top": top,
        "Width": right - left,
        "Height": bottom - top,
    }
