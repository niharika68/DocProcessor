from pydantic import BaseModel


class BboxNorm(BaseModel):
    left: float
    top: float
    width: float
    height: float


class BboxPx(BaseModel):
    x0: int
    y0: int
    x1: int
    y1: int


class Annotation(BaseModel):
    category: str  # "key_field" | "line_item" | "anomaly"
    label: str
    value: str
    bbox_norm: BboxNorm
    bbox_px: BboxPx


class PageResult(BaseModel):
    page_number: int
    image_b64: str
    image_width_px: int
    image_height_px: int
    annotations: list[Annotation]


class Summary(BaseModel):
    key_fields: dict
    items: list[dict]    # line_items / clauses / services
    flags: list[dict]    # anomalies / risks / flags


class ProcessResponse(BaseModel):
    session_id: str
    doc_type: str
    pages: list[PageResult]
    summary: Summary
