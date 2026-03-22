# Document Processor — Architecture

## Workflow Diagram

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="900" height="600" font-family="system-ui, sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#64748b"/>
    </marker>
    <marker id="arrp" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#a855f7"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="900" height="600" fill="#f8f9fa" rx="12"/>
  <text x="450" y="32" text-anchor="middle" font-size="15" font-weight="bold" fill="#1e293b">Document Processor — End-to-End Pipeline</text>

  <!-- ── TAB ROW ── -->
  <rect x="10" y="48" width="880" height="52" fill="#e2e8f0" rx="8"/>
  <text x="450" y="68" text-anchor="middle" font-size="10" fill="#475569" font-weight="bold">USER SELECTS TAB</text>

  <rect x="20"  y="74" width="140" height="20" rx="4" fill="#f59e0b"/>
  <text x="90"  y="88" text-anchor="middle" font-size="9" fill="white" font-weight="bold">Invoices</text>
  <rect x="170" y="74" width="140" height="20" rx="4" fill="#3b82f6"/>
  <text x="240" y="88" text-anchor="middle" font-size="9" fill="white" font-weight="bold">Contracts</text>
  <rect x="320" y="74" width="140" height="20" rx="4" fill="#10b981"/>
  <text x="390" y="88" text-anchor="middle" font-size="9" fill="white" font-weight="bold">Referrals</text>
  <text x="620" y="88" text-anchor="middle" font-size="9" fill="#475569">Each tab has isolated Jotai state — switching tabs keeps results</text>

  <!-- ── LANE LABELS ── -->
  <rect x="10"  y="112" width="95"  height="380" fill="#e2e8f0" rx="6"/>
  <text x="57"  y="240" text-anchor="middle" font-size="10" fill="#475569" transform="rotate(-90,57,240)">Frontend (React)</text>

  <rect x="113" y="112" width="95"  height="380" fill="#fef9c3" rx="6"/>
  <text x="160" y="250" text-anchor="middle" font-size="10" fill="#854d0e" transform="rotate(-90,160,250)">Rendering</text>

  <rect x="216" y="112" width="125" height="380" fill="#dcfce7" rx="6"/>
  <text x="278" y="265" text-anchor="middle" font-size="10" fill="#166534" transform="rotate(-90,278,265)">AWS Textract</text>

  <rect x="349" y="112" width="175" height="380" fill="#ede9fe" rx="6"/>
  <text x="436" y="265" text-anchor="middle" font-size="10" fill="#5b21b6" transform="rotate(-90,436,265)">★ AI — Amazon Nova Pro</text>

  <rect x="532" y="112" width="130" height="380" fill="#fee2e2" rx="6"/>
  <text x="597" y="265" text-anchor="middle" font-size="10" fill="#991b1b" transform="rotate(-90,597,265)">Coord Mapping</text>

  <rect x="670" y="112" width="220" height="380" fill="#e0f2fe" rx="6"/>
  <text x="780" y="265" text-anchor="middle" font-size="10" fill="#075985" transform="rotate(-90,780,265)">Response / Display</text>

  <!-- ── STEP BOXES ── -->

  <!-- Upload -->
  <rect x="16"  y="130" width="83" height="44" rx="6" fill="#334155"/>
  <text x="57"  y="149" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Upload PDF</text>
  <text x="57"  y="163" text-anchor="middle" font-size="8"  fill="#cbd5e1">+ select doc_type</text>

  <!-- Render -->
  <rect x="119" y="130" width="83" height="44" rx="6" fill="#ca8a04"/>
  <text x="160" y="149" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Render Pages</text>
  <text x="160" y="163" text-anchor="middle" font-size="8"  fill="#fef9c3">PyMuPDF  2×</text>

  <!-- Textract -->
  <rect x="222" y="130" width="113" height="44" rx="6" fill="#16a34a"/>
  <text x="278" y="148" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Textract OCR</text>
  <text x="278" y="161" text-anchor="middle" font-size="8"  fill="#dcfce7">AnalyzeDocument</text>
  <text x="278" y="172" text-anchor="middle" font-size="8"  fill="#dcfce7">TABLES + FORMS</text>

  <!-- Parse Blocks -->
  <rect x="222" y="220" width="113" height="44" rx="6" fill="#15803d"/>
  <text x="278" y="238" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Parse Blocks</text>
  <text x="278" y="253" text-anchor="middle" font-size="8"  fill="#dcfce7">words · KV pairs · tables</text>

  <!-- AI -->
  <rect x="355" y="175" width="163" height="60" rx="6" fill="#7c3aed"/>
  <text x="436" y="196" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">★ Amazon Nova Pro</text>
  <text x="436" y="209" text-anchor="middle" font-size="8"  fill="#ede9fe">Prompt selected by doc_type</text>
  <text x="436" y="221" text-anchor="middle" font-size="8"  fill="#ede9fe">→ key_fields · items · flags</text>
  <text x="436" y="233" text-anchor="middle" font-size="8"  fill="#c4b5fd">returns source_words (no coords)</text>

  <!-- Map Coords -->
  <rect x="538" y="175" width="118" height="60" rx="6" fill="#b91c1c"/>
  <text x="597" y="196" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Map Coordinates</text>
  <text x="597" y="210" text-anchor="middle" font-size="8"  fill="#fee2e2">source_words lookup</text>
  <text x="597" y="223" text-anchor="middle" font-size="8"  fill="#fee2e2">→ Textract bbox</text>
  <text x="597" y="236" text-anchor="middle" font-size="8"  fill="#fca5a5">union + sanity check</text>

  <!-- Build Response -->
  <rect x="676" y="130" width="207" height="44" rx="6" fill="#0369a1"/>
  <text x="779" y="149" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Build API Response</text>
  <text x="779" y="163" text-anchor="middle" font-size="8"  fill="#e0f2fe">pages · annotations · summary</text>

  <!-- Page Viewer -->
  <rect x="676" y="220" width="207" height="44" rx="6" fill="#0284c7"/>
  <text x="779" y="239" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Page Viewer</text>
  <text x="779" y="253" text-anchor="middle" font-size="8"  fill="#e0f2fe">yellow · orange · red overlays</text>

  <!-- Summary Panel -->
  <rect x="676" y="310" width="207" height="44" rx="6" fill="#0284c7"/>
  <text x="779" y="329" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Summary Panel</text>
  <text x="779" y="343" text-anchor="middle" font-size="8"  fill="#e0f2fe">key fields · items · flags tables</text>

  <!-- Downloads -->
  <rect x="676" y="400" width="207" height="44" rx="6" fill="#075985"/>
  <text x="779" y="419" text-anchor="middle" font-size="9"  fill="white" font-weight="bold">Downloads</text>
  <text x="779" y="433" text-anchor="middle" font-size="8"  fill="#e0f2fe">Annotated PDF  ·  JSON export</text>

  <!-- ── ARROWS ── -->
  <line x1="99"  y1="152" x2="117" y2="152" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="202" y1="152" x2="220" y2="152" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="278" y1="174" x2="278" y2="218" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="335" y1="242" x2="353" y2="220" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <path d="M202 140 Q290 110 353 190" fill="none" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrp)"/>
  <line x1="518" y1="205" x2="536" y2="205" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="656" y1="192" x2="674" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="779" y1="174" x2="779" y2="218" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="779" y1="264" x2="779" y2="308" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="779" y1="354" x2="779" y2="398" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- image label -->
  <text x="240" y="108" font-size="8" fill="#a855f7">page images (multimodal)</text>

  <!-- ── LEGEND ── -->
  <rect x="10" y="504" width="880" height="84" fill="#f1f5f9" rx="8"/>
  <text x="20" y="522" font-size="10" font-weight="bold" fill="#1e293b">Legend</text>
  <rect x="20"  y="530" width="10" height="10" fill="#7c3aed" rx="2"/>
  <text x="36"  y="540" font-size="9" fill="#1e293b">★ AI step — only place where Nova Pro is called</text>
  <rect x="20"  y="548" width="10" height="10" fill="none" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="3,2" rx="2"/>
  <text x="36"  y="558" font-size="9" fill="#1e293b">Multimodal input — page images + Textract text both sent to model</text>
  <rect x="300" y="530" width="10" height="10" fill="#f59e0b" rx="2"/>
  <text x="316" y="540" font-size="9" fill="#1e293b">Invoice tab — line items · anomaly detection</text>
  <rect x="300" y="548" width="10" height="10" fill="#3b82f6" rx="2"/>
  <text x="316" y="558" font-size="9" fill="#1e293b">Contract tab — clauses · risk detection</text>
  <rect x="300" y="566" width="10" height="10" fill="#10b981" rx="2"/>
  <text x="316" y="576" font-size="9" fill="#1e293b">Referral tab — services · missing field flags</text>
  <text x="580" y="540" font-size="9" fill="#475569">All tabs share identical pipeline.</text>
  <text x="580" y="554" font-size="9" fill="#475569">Only the AI prompt changes per doc_type.</text>
  <text x="580" y="568" font-size="9" fill="#475569">Output shape is always: key_fields · items · flags</text>

</svg>
```

---

## Where AI Is Used

There is exactly **one AI step** in the entire pipeline. Everything else (rendering, OCR, coordinate mapping) is deterministic.

### ★ Amazon Nova Pro (AWS Bedrock) — `_call_ai()` in `pipeline.py`

**Input:**
- Page images from PyMuPDF (the model sees the document visually — multimodal)
- Pre-structured Textract output: key-value pairs, tables as markdown, raw text lines

**Output (same shape for all doc types):**
```json
{
  "key_fields": [{ "field": "...", "value": "...", "page": 1, "source_words": ["word1"] }],
  "items":      [{ ... , "page": 1, "source_words": ["word1"] }],
  "flags":      [{ "type": "...", "description": "...", "page": 1, "source_words": ["word1"] }]
}
```

> The model returns `source_words` — exact word strings from the document. It is **never asked for coordinates**. Coordinates are resolved separately by looking up those words in Textract's WORD blocks.

---

## Prompts by Document Type

### Invoice (`doc_type=invoice`)

```
You are an expert invoice analyst.

key_fields to extract:
  invoice_number, invoice_date, due_date, vendor_name, vendor_address,
  bill_to, po_number, subtotal, tax, total

items → each billable line item:
  description, quantity, unit_price, total

flags (anomalies) to detect:
  - qty × unit_price ≠ line total
  - sum of line totals ≠ invoice subtotal
  - duplicate line items
  - missing required fields
  - date inconsistencies
```

**Summary panel labels:** Key Fields · Line Items · Anomalies

---

### Contract (`doc_type=contract`)

```
You are an expert contract analyst.

key_fields to extract:
  party_a, party_b, effective_date, expiration_date, contract_value,
  governing_law, jurisdiction, contract_number, notice_period, payment_terms

items → significant clauses:
  title (e.g. "Limitation of Liability"), one-sentence summary

flags (risks) to detect:
  - auto-renewal clauses
  - uncapped liability
  - unilateral termination rights
  - missing signatures
  - conflicting dates
  - unusual indemnification terms
```

**Summary panel labels:** Key Fields · Clauses · Risks

---

### Referral (`doc_type=referral`)

```
You are an expert medical document analyst.

key_fields to extract:
  patient_name, date_of_birth, patient_id, referring_provider, referred_to,
  referral_date, diagnosis_code, reason_for_referral, insurance_id, authorization_number

items → each requested service:
  service name, priority (urgent/routine/stat), notes

flags to detect:
  - missing required fields (e.g. blank authorization number)
  - urgency indicators
  - incomplete diagnosis codes
  - missing insurance info
  - expired authorizations
  - inconsistent dates
```

**Summary panel labels:** Key Fields · Services · Flags

---

## Overlay Colors

| Color | Meaning |
|---|---|
| Yellow `rgba(255, 230, 0, 0.35)` | Key fields |
| Orange `rgba(255, 140, 0, 0.30)` | Items (line items / clauses / services) |
| Red `rgba(220, 50, 50, 0.35)` | Flags (anomalies / risks / missing fields) |

Clicking an overlay highlights the matching row in the summary panel, and vice versa.
