import { useAtom } from "jotai";
import {
  activeTabAtom,
  invoiceResultAtom,
  contractResultAtom,
  referralResultAtom,
  loadingAtom,
  errorAtom,
} from "./store";
import UploadSection from "./components/UploadSection";
import PageViewer from "./components/PageViewer";
import SummaryPanel from "./components/SummaryPanel";
import type { DocType } from "./types";
import { DOC_CONFIGS } from "./types";

const TABS: DocType[] = ["invoice", "contract", "referral"];

export default function App() {
  const [activeTab, setActiveTab] = useAtom(activeTabAtom);
  const [invoiceResult] = useAtom(invoiceResultAtom);
  const [contractResult] = useAtom(contractResultAtom);
  const [referralResult] = useAtom(referralResultAtom);
  const [loading] = useAtom(loadingAtom);
  const [error] = useAtom(errorAtom);

  const resultMap = {
    invoice: invoiceResult,
    contract: contractResult,
    referral: referralResult,
  };
  const result = resultMap[activeTab];

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 1400, margin: "0 auto", padding: "24px 16px" }}>
      <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700 }}>Document Processor</h1>
      <p style={{ margin: "0 0 20px", color: "#666", fontSize: 14 }}>
        Upload a PDF to extract and highlight key fields, items, and flags.
      </p>

      {/* Tab Bar */}
      <div style={{ display: "flex", gap: 0, borderBottom: "2px solid #e5e7eb", marginBottom: 24 }}>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: "10px 24px",
              border: "none",
              borderBottom: activeTab === tab ? "2px solid #2563eb" : "2px solid transparent",
              marginBottom: -2,
              background: "none",
              cursor: "pointer",
              fontWeight: activeTab === tab ? 700 : 400,
              color: activeTab === tab ? "#2563eb" : "#6b7280",
              fontSize: 14,
              transition: "all 0.15s",
            }}
          >
            {DOC_CONFIGS[tab].label}
          </button>
        ))}
      </div>

      <UploadSection docType={activeTab} />

      {error && (
        <div style={{ marginTop: 16, padding: "10px 14px", background: "#fff0f0", border: "1px solid #f5c6c6", borderRadius: 6, color: "#c0392b" }}>
          {error}
        </div>
      )}

      {loading && (
        <div style={{ marginTop: 32, textAlign: "center", color: "#666" }}>
          <div style={{ fontSize: 28, marginBottom: 8 }}>⏳</div>
          Processing document — running OCR and AI analysis…
        </div>
      )}

      {result && (
        <div style={{ marginTop: 32, display: "grid", gridTemplateColumns: "1fr 380px", gap: 32, alignItems: "start" }}>
          <PageViewer pages={result.pages} />
          <div style={{ position: "sticky", top: 16 }}>
            <SummaryPanel result={result} docType={activeTab} />
          </div>
        </div>
      )}
    </div>
  );
}
