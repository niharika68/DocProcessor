import fitz  # PyMuPDF
from dataclasses import dataclass


@dataclass
class PageRender:
    page_number: int  # 1-indexed
    png_bytes: bytes
    width_px: int
    height_px: int
    width_pt: float
    height_pt: float


def render_pages(pdf_bytes: bytes, scale: float = 2.0) -> list[PageRender]:
    """Render each PDF page to a PNG at the given scale factor."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    results: list[PageRender] = []

    for i, page in enumerate(doc):
        rect = page.rect  # dimensions in PDF points
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        results.append(PageRender(
            page_number=i + 1,
            png_bytes=pix.tobytes("png"),
            width_px=pix.width,
            height_px=pix.height,
            width_pt=rect.width,
            height_pt=rect.height,
        ))

    doc.close()
    return results
