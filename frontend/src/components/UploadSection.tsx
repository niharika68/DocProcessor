import { useRef, useState } from "react";
import { useSetAtom, useAtom } from "jotai";
import {
  invoiceResultAtom,
  contractResultAtom,
  referralResultAtom,
  loadingAtom,
  errorAtom,
  selectedAnnotationAtom,
} from "../store";
import type { ProcessResponse, DocType } from "../types";

interface Props {
  docType: DocType;
}

export default function UploadSection({ docType }: Props) {
  const setInvoice = useSetAtom(invoiceResultAtom);
  const setContract = useSetAtom(contractResultAtom);
  const setReferral = useSetAtom(referralResultAtom);
  const setLoading = useSetAtom(loadingAtom);
  const setError = useSetAtom(errorAtom);
  const setSelected = useSetAtom(selectedAnnotationAtom);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  function setResult(data: ProcessResponse) {
    if (docType === "invoice") setInvoice(data);
    else if (docType === "contract") setContract(data);
    else setReferral(data);
  }

  async function upload(file: File) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Please upload a PDF file.");
      return;
    }
    setError(null);
    setLoading(true);
    setSelected(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`/api/process?doc_type=${docType}`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail ?? `Server error ${res.status}`);
      }
      const data: ProcessResponse = await res.json();
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        const file = e.dataTransfer.files[0];
        if (file) upload(file);
      }}
      onClick={() => inputRef.current?.click()}
      style={{
        border: `2px dashed ${dragging ? "#4f8ef7" : "#aaa"}`,
        borderRadius: 8,
        padding: "40px 24px",
        textAlign: "center",
        cursor: "pointer",
        background: dragging ? "#f0f6ff" : "#fafafa",
        transition: "all 0.15s",
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        style={{ display: "none" }}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) upload(file);
        }}
      />
      <p style={{ margin: 0, color: "#555", fontSize: 16 }}>
        Drag & drop a PDF here, or <strong>click to browse</strong>
      </p>
    </div>
  );
}
