import { useAtom } from "jotai";
import { selectedAnnotationAtom } from "../store";
import type { PageResult, Annotation, AnnotationCategory } from "../types";

const OVERLAY_COLORS: Record<AnnotationCategory, string> = {
  key_field: "rgba(255, 230, 0, 0.35)",
  line_item: "rgba(255, 140, 0, 0.30)",
  anomaly: "rgba(220, 50, 50, 0.35)",
};

const SELECTED_COLORS: Record<AnnotationCategory, string> = {
  key_field: "rgba(255, 220, 0, 0.75)",
  line_item: "rgba(255, 120, 0, 0.65)",
  anomaly: "rgba(200, 30, 30, 0.70)",
};

interface Props {
  pages: PageResult[];
}

export default function PageViewer({ pages }: Props) {
  const [selected, setSelected] = useAtom(selectedAnnotationAtom);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      {pages.map((page) => (
        <div key={page.page_number}>
          <p style={{ margin: "0 0 6px", fontWeight: 600, color: "#444" }}>
            Page {page.page_number}
          </p>
          <div style={{ position: "relative", display: "inline-block" }}>
            <img
              src={`data:image/png;base64,${page.image_b64}`}
              alt={`Page ${page.page_number}`}
              style={{ display: "block", width: "100%", maxWidth: page.image_width_px }}
            />
            {page.annotations.map((ann, i) => (
              <OverlayBox
                key={i}
                ann={ann}
                pageWidthPx={page.image_width_px}
                pageHeightPx={page.image_height_px}
                isSelected={selected === ann}
                onClick={() => setSelected(selected === ann ? null : ann)}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function OverlayBox({
  ann,
  pageWidthPx,
  pageHeightPx,
  isSelected,
  onClick,
}: {
  ann: Annotation;
  pageWidthPx: number;
  pageHeightPx: number;
  isSelected: boolean;
  onClick: () => void;
}) {
  const { left, top, width, height } = ann.bbox_norm;
  if (width === 0 || height === 0) return null;

  return (
    <div
      onClick={onClick}
      title={`${ann.label}: ${ann.value}`}
      style={{
        position: "absolute",
        left: `${left * 100}%`,
        top: `${top * 100}%`,
        width: `${width * 100}%`,
        height: `${height * 100}%`,
        background: isSelected
          ? SELECTED_COLORS[ann.category]
          : OVERLAY_COLORS[ann.category],
        border: isSelected ? "2px solid #333" : "1px solid transparent",
        borderRadius: 2,
        cursor: "pointer",
        boxSizing: "border-box",
        transition: "background 0.1s",
      }}
    />
  );
}
