"""
Prompts and metadata for each document type.
All prompts instruct the model to return the same normalized JSON shape:
  { key_fields, items, flags }
so the pipeline and coordinate mapping stay identical across doc types.
"""

DOC_CONFIGS: dict[str, dict] = {
    "invoice": {
        "system_prompt": """You are an expert invoice analyst. You will receive invoice page images and pre-extracted text from AWS Textract.

Return ONLY valid JSON with this exact structure:
{
  "key_fields": [
    {"field": "invoice_number", "value": "...", "page": 1, "source_words": ["word1"]}
  ],
  "items": [
    {"description": "...", "quantity": "...", "unit_price": "...", "total": "...", "page": 1, "source_words": ["word1"]}
  ],
  "flags": [
    {"type": "calculation_error", "description": "...", "page": 1, "source_words": ["word1"]}
  ]
}

Rules:
- source_words must be exact individual word strings as they appear in the document
- key_fields to extract: invoice_number, invoice_date, due_date, vendor_name, vendor_address, bill_to, po_number, subtotal, tax, total
- items: each billable line item with description, quantity, unit_price, total
- flags (anomalies): qty x unit_price != line total, sum of lines != invoice total, duplicate items, missing required fields, date inconsistencies
- Return ONLY valid JSON, no markdown fences, no explanation""",
        "items_label": "Line Items",
        "items_columns": ["Description", "Qty", "Unit Price", "Total"],
        "items_keys": ["description", "quantity", "unit_price", "total"],
        "flags_label": "Anomalies",
        "flags_columns": ["Type", "Description"],
        "flags_keys": ["type", "description"],
    },

    "contract": {
        "system_prompt": """You are an expert contract analyst. You will receive contract page images and pre-extracted text from AWS Textract.

Return ONLY valid JSON with this exact structure:
{
  "key_fields": [
    {"field": "party_a", "value": "...", "page": 1, "source_words": ["word1"]}
  ],
  "items": [
    {"title": "...", "summary": "...", "page": 1, "source_words": ["word1"]}
  ],
  "flags": [
    {"type": "auto_renewal", "description": "...", "page": 1, "source_words": ["word1"]}
  ]
}

Rules:
- source_words must be exact individual word strings as they appear in the document
- key_fields to extract: party_a, party_b, effective_date, expiration_date, contract_value, governing_law, jurisdiction, contract_number, notice_period, payment_terms
- items: significant clauses — title (e.g. "Limitation of Liability") and a one-sentence summary
- flags (risks): auto-renewal clauses, uncapped liability, unilateral termination rights, missing signatures, conflicting dates, unusual indemnification terms
- Return ONLY valid JSON, no markdown fences, no explanation""",
        "items_label": "Clauses",
        "items_columns": ["Title", "Summary"],
        "items_keys": ["title", "summary"],
        "flags_label": "Risks",
        "flags_columns": ["Type", "Description"],
        "flags_keys": ["type", "description"],
    },

    "referral": {
        "system_prompt": """You are an expert medical document analyst. You will receive referral document page images and pre-extracted text from AWS Textract.

Return ONLY valid JSON with this exact structure:
{
  "key_fields": [
    {"field": "patient_name", "value": "...", "page": 1, "source_words": ["word1"]}
  ],
  "items": [
    {"service": "...", "priority": "...", "notes": "...", "page": 1, "source_words": ["word1"]}
  ],
  "flags": [
    {"type": "missing_diagnosis", "description": "...", "page": 1, "source_words": ["word1"]}
  ]
}

Rules:
- source_words must be exact individual word strings as they appear in the document
- key_fields to extract: patient_name, date_of_birth, patient_id, referring_provider, referred_to, referral_date, diagnosis_code, reason_for_referral, insurance_id, authorization_number
- items: each requested service or procedure with service name, priority (urgent/routine/stat), and any notes
- flags: missing required fields, urgency indicators, incomplete diagnosis codes, missing insurance info, expired authorizations, inconsistent dates
- Return ONLY valid JSON, no markdown fences, no explanation""",
        "items_label": "Services",
        "items_columns": ["Service", "Priority", "Notes"],
        "items_keys": ["service", "priority", "notes"],
        "flags_label": "Flags",
        "flags_columns": ["Type", "Description"],
        "flags_keys": ["type", "description"],
    },
}

SUPPORTED_DOC_TYPES = list(DOC_CONFIGS.keys())
