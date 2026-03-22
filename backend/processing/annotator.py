import fitz  # PyMuPDF
from ..models.schemas import Annotation

CATEGORY_COLORS = {
    "key_field":  (1.0, 0.90, 0.0),   # yellow
    "line_item":  (1.0, 0.55, 0.0),   # orange
    "anomaly":    (0.86, 0.20, 0.20),  # red
}


def annotate_pdf(pdf_bytes: bytes, page_annotations: dict[int, list[Annotation]]) -> bytes:
    """
    Draw highlight rectangles on a copy of the PDF using normalized bboxes.
    Returns the annotated PDF as bytes.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for i, page in enumerate(doc):
        page_num = i + 1
        annotations = page_annotations.get(page_num, [])
        w = page.rect.width
        h = page.rect.height

        for ann in annotations:
            bn = ann.bbox_norm
            if bn.width == 0 or bn.height == 0:
                continue

            rect = fitz.Rect(
                bn.left * w,
                bn.top * h,
                (bn.left + bn.width) * w,
                (bn.top + bn.height) * h,
            )
            color = CATEGORY_COLORS.get(ann.category, (1.0, 1.0, 0.0))
            highlight = page.add_highlight_annot(rect)
            highlight.set_colors(stroke=color)
            highlight.set_opacity(0.4)
            highlight.update()

    return doc.tobytes()
