export interface BboxNorm {
  left: number;
  top: number;
  width: number;
  height: number;
}

export interface BboxPx {
  x0: number;
  y0: number;
  x1: number;
  y1: number;
}

export type AnnotationCategory = "key_field" | "line_item" | "anomaly";
export type DocType = "invoice" | "contract" | "referral";

export interface Annotation {
  category: AnnotationCategory;
  label: string;
  value: string;
  bbox_norm: BboxNorm;
  bbox_px: BboxPx;
}

export interface PageResult {
  page_number: number;
  image_b64: string;
  image_width_px: number;
  image_height_px: number;
  annotations: Annotation[];
}

export interface Summary {
  key_fields: Record<string, string>;
  items: Record<string, string>[];
  flags: { type: string; description: string; page: number }[];
}

export interface ProcessResponse {
  session_id: string;
  doc_type: DocType;
  pages: PageResult[];
  summary: Summary;
}

export interface DocConfig {
  label: string;
  itemsLabel: string;
  itemsColumns: string[];
  itemsKeys: string[];
  flagsLabel: string;
}

export const DOC_CONFIGS: Record<DocType, DocConfig> = {
  invoice: {
    label: "Invoices",
    itemsLabel: "Line Items",
    itemsColumns: ["Description", "Qty", "Unit Price", "Total"],
    itemsKeys: ["description", "quantity", "unit_price", "total"],
    flagsLabel: "Anomalies",
  },
  contract: {
    label: "Contracts",
    itemsLabel: "Clauses",
    itemsColumns: ["Title", "Summary"],
    itemsKeys: ["title", "summary"],
    flagsLabel: "Risks",
  },
  referral: {
    label: "Referrals",
    itemsLabel: "Services",
    itemsColumns: ["Service", "Priority", "Notes"],
    itemsKeys: ["service", "priority", "notes"],
    flagsLabel: "Flags",
  },
};
