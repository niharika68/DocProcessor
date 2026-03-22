import { useAtom } from "jotai";
import { selectedAnnotationAtom } from "../store";
import type { Annotation, PageResult, ProcessResponse, DocType } from "../types";
import { DOC_CONFIGS } from "../types";

interface Props {
  result: ProcessResponse;
  docType: DocType;
}

export default function SummaryPanel({ result, docType }: Props) {
  const [selected, setSelected] = useAtom(selectedAnnotationAtom);
  const config = DOC_CONFIGS[docType];

  const allAnnotations: (Annotation & { page_number: number })[] =
    result.pages.flatMap((p: PageResult) =>
      p.annotations.map((a) => ({ ...a, page_number: p.page_number }))
    );

  const keyFields = allAnnotations.filter((a) => a.category === "key_field");
  const items = allAnnotations.filter((a) => a.category === "line_item");
  const flags = allAnnotations.filter((a) => a.category === "anomaly");

  function rowStyle(ann: Annotation): React.CSSProperties {
    return {
      cursor: "pointer",
      background: selected === ann ? "#fffbea" : "transparent",
      borderBottom: "1px solid #eee",
    };
  }

  function handleRowClick(ann: Annotation) {
    setSelected(selected === ann ? null : ann);
  }

  return (
    <div style={{ fontSize: 13 }}>
      <Section title="Key Fields" color="#f5c400">
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f9f9f9" }}>
              <Th>Field</Th><Th>Value</Th><Th>Page</Th>
            </tr>
          </thead>
          <tbody>
            {keyFields.map((ann, i) => (
              <tr key={i} style={rowStyle(ann)} onClick={() => handleRowClick(ann)}>
                <Td>{ann.label}</Td>
                <Td>{ann.value}</Td>
                <Td>{ann.page_number}</Td>
              </tr>
            ))}
            {keyFields.length === 0 && <EmptyRow cols={3} />}
          </tbody>
        </table>
      </Section>

      <Section title={config.itemsLabel} color="#f57c00">
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f9f9f9" }}>
              {config.itemsColumns.map((col) => <Th key={col}>{col}</Th>)}
              <Th>Page</Th>
            </tr>
          </thead>
          <tbody>
            {items.map((ann, i) => (
              <tr key={i} style={rowStyle(ann)} onClick={() => handleRowClick(ann)}>
                <Td>{ann.label}</Td>
                <Td style={{ color: "#666" }}>{ann.value}</Td>
                {config.itemsColumns.length > 2 && <Td />}
                <Td>{ann.page_number}</Td>
              </tr>
            ))}
            {items.length === 0 && <EmptyRow cols={config.itemsColumns.length + 1} />}
          </tbody>
        </table>
      </Section>

      <Section title={config.flagsLabel} color="#dc3232">
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f9f9f9" }}>
              <Th>Type</Th><Th>Description</Th><Th>Page</Th>
            </tr>
          </thead>
          <tbody>
            {flags.map((ann, i) => (
              <tr key={i} style={rowStyle(ann)} onClick={() => handleRowClick(ann)}>
                <Td>{ann.label}</Td>
                <Td style={{ color: "#555" }}>{ann.value}</Td>
                <Td>{ann.page_number}</Td>
              </tr>
            ))}
            {flags.length === 0 && (
              <tr>
                <td colSpan={3} style={{ padding: "8px 6px", color: "#aaa", fontStyle: "italic" }}>
                  None detected
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </Section>

      <div style={{ marginTop: 20, display: "flex", gap: 10, justifyContent: "center" }}>
        <button
          onClick={() => window.open(`/api/download/${result.session_id}`, "_blank")}
          style={btnStyle("#2563eb")}
        >
          Download Annotated PDF
        </button>
        <button
          onClick={() => window.open(`/api/export/${result.session_id}`, "_blank")}
          style={btnStyle("#16a34a")}
        >
          Download JSON
        </button>
      </div>
    </div>
  );
}

function btnStyle(bg: string): React.CSSProperties {
  return {
    padding: "10px 22px",
    background: bg,
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
    fontWeight: 600,
    fontSize: 14,
  };
}

function Section({ title, color, children }: { title: string; color: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ margin: "0 0 8px", fontSize: 14, borderLeft: `4px solid ${color}`, paddingLeft: 8 }}>
        {title}
      </h3>
      {children}
    </div>
  );
}

function Th({ children }: { children: React.ReactNode }) {
  return (
    <th style={{ textAlign: "left", padding: "6px", fontWeight: 600, borderBottom: "2px solid #ddd" }}>
      {children}
    </th>
  );
}

function Td({ children, style }: { children?: React.ReactNode; style?: React.CSSProperties }) {
  return <td style={{ padding: "6px", ...style }}>{children}</td>;
}

function EmptyRow({ cols }: { cols: number }) {
  return (
    <tr>
      <td colSpan={cols} style={{ padding: "8px 6px", color: "#aaa", fontStyle: "italic" }}>
        None found
      </td>
    </tr>
  );
}
