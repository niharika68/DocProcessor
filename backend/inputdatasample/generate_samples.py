"""
Run from project root:
  poetry run python backend/inputdatasample/generate_samples.py
Outputs:
  backend/inputdatasample/sample_contract.pdf
  backend/inputdatasample/sample_referral.pdf
"""
import fitz
from pathlib import Path

OUT_DIR = Path(__file__).parent
PAGE_W, PAGE_H = 595, 842  # A4


def text(page, x, y, content, size=10, bold=False, color=(0, 0, 0)):
    page.insert_text((x, y), content, fontname="hebo" if bold else "helv", fontsize=size, color=color)


def hline(page, x0, x1, y, width=0.5):
    page.draw_line((x0, y), (x1, y), width=width, color=(0.6, 0.6, 0.6))


# ── CONTRACT ──────────────────────────────────────────────────────────────────

def make_contract():
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Header
    text(page, 50, 60, "PHARMACEUTICAL SUPPLY AGREEMENT", size=16, bold=True, color=(0.1, 0.1, 0.4))
    text(page, 50, 80, "Contract No: PSA-2024-0092", size=10)
    text(page, 50, 94, "Effective Date: January 1, 2024", size=10)
    text(page, 50, 108, "Expiration Date: December 31, 2025", size=10)
    hline(page, 50, 545, 120, width=1.5)

    # Parties
    text(page, 50, 140, "PARTIES", size=11, bold=True)
    text(page, 50, 158, "Party A (Vendor / Supplier):", size=10, bold=True)
    text(page, 50, 172, "Vantage MedSupply Distribution Co.", size=10)
    text(page, 50, 185, "3300 Industrial Parkway, Columbus, OH 43219", size=10)
    text(page, 50, 198, "Represented by: Douglas Carmichael, VP of Sales", size=10)

    text(page, 50, 220, "Party B (Hospital Pharmacy):", size=10, bold=True)
    text(page, 50, 234, "Stonebridge Regional Medical Center — Pharmacy Services", size=10)
    text(page, 50, 247, "800 Stonebridge Blvd, Hartford, CT 06103", size=10)
    text(page, 50, 260, "Represented by: Dr. Renata Kowalski, PharmD, Director of Pharmacy", size=10)

    hline(page, 50, 545, 275)

    # Contract Value
    text(page, 50, 292, "CONTRACT VALUE & PAYMENT TERMS", size=11, bold=True)
    text(page, 50, 308, "Estimated Annual Contract Value:  $1,850,000.00  (USD)", size=10)
    text(page, 50, 322, "Payment Terms:  Net 45 days from verified delivery", size=10)
    text(page, 50, 336, "Minimum Order Commitment:  $75,000.00 per quarter", size=10)
    text(page, 50, 350, "Late Payment Penalty:  2.0% per month on outstanding balance", size=10)

    hline(page, 50, 545, 364)

    # Clauses
    text(page, 50, 380, "KEY CLAUSES", size=11, bold=True)

    clauses = [
        ("1. Scope of Supply",
         "Vendor shall supply pharmaceuticals, IV solutions, and medical consumables\n"
         "as listed in the formulary schedule attached as Exhibit A."),
        ("2. Delivery & Cold Chain Compliance",
         "All temperature-sensitive products must be shipped per USP <1> guidelines.\n"
         "Vendor bears full liability for cold-chain failures during transit."),
        ("3. Auto-Renewal",                                      # intentional risk
         "This Agreement shall automatically renew for successive one-year terms unless\n"
         "either party provides written notice of non-renewal at least 120 days prior to expiry."),
        ("4. Product Recall & Shortage",
         "Vendor shall notify Hospital Pharmacy within 24 hours of any FDA recall or\n"
         "anticipated shortage affecting contracted products."),
        ("5. Limitation of Liability",
         "Vendor liability for defective products is limited to replacement cost only.\n"
         "Hospital waives right to consequential or patient-harm damages."),   # intentional risk
        ("6. Governing Law",
         "This Agreement is governed by the laws of the State of Connecticut.\n"
         "Disputes shall be resolved via binding arbitration in Hartford, CT."),
    ]

    y = 398
    for title, body in clauses:
        text(page, 50, y, title, size=10, bold=True, color=(0.1, 0.1, 0.4))
        y += 14
        for line in body.split("\n"):
            text(page, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
            y += 13
        y += 5

    # Signatures
    hline(page, 50, 545, y + 4, width=1.0)
    y += 18
    text(page, 50,  y, "Douglas Carmichael", size=10, bold=True)
    text(page, 320, y, "Dr. Renata Kowalski, PharmD", size=10, bold=True)
    y += 14
    text(page, 50,  y, "Vantage MedSupply Distribution Co.", size=9, color=(0.4, 0.4, 0.4))
    text(page, 320, y, "Stonebridge Regional Medical Center", size=9, color=(0.4, 0.4, 0.4))
    y += 12
    text(page, 50,  y, "Date: _______________", size=9)
    text(page, 320, y, "Date: _______________", size=9)

    out = OUT_DIR / "sample_contract.pdf"
    doc.save(str(out))
    print(f"Contract saved to: {out}")
    print("Intentional risks for testing:")
    print("  - Auto-renewal clause (120-day notice window)")
    print("  - Vendor liability limited to replacement cost only (waives patient-harm damages)")


# ── REFERRAL ──────────────────────────────────────────────────────────────────

def make_referral():
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Header
    text(page, 50, 55, "PATIENT REFERRAL FORM", size=18, bold=True, color=(0.1, 0.3, 0.1))
    text(page, 50, 75, "FAKE HOSPITAL Medical Group", size=12, bold=True)
    text(page, 50, 89, "123 Fake Hospital Blvd, Faketown, FK 00001  |  Tel: (000) 555-0000", size=9, color=(0.4, 0.4, 0.4))
    hline(page, 50, 545, 100, width=1.5)

    # Patient Info
    text(page, 50, 118, "PATIENT INFORMATION", size=11, bold=True)
    fields_left = [
        ("Patient Name:", "FAKE PATIENT"),
        ("Date of Birth:", "01/01/1980"),
        ("Patient ID:", "FAKE-000001"),
        ("Insurance Provider:", "FAKE INSURANCE CO."),
    ]
    fields_right = [
        ("Insurance ID:", "FAKE-INS-0001"),
        ("Authorization No:", ""),          # intentional missing field
        ("Phone:", "(000) 555-1234"),
        ("Primary Language:", "English"),
    ]
    y = 134
    for (lbl, val), (lbl2, val2) in zip(fields_left, fields_right):
        text(page, 50,  y, lbl, size=9, bold=True)
        text(page, 160, y, val, size=9)
        text(page, 310, y, lbl2, size=9, bold=True)
        text(page, 420, y, val2, size=9)
        y += 16

    hline(page, 50, 545, y + 2)
    y += 16

    # Referring / Referred-To
    text(page, 50, y, "PROVIDER INFORMATION", size=11, bold=True)
    y += 16
    text(page, 50,  y, "Referring Provider:", size=9, bold=True)
    text(page, 160, y, "Dr. FAKE DOCTOR, MD", size=9)
    text(page, 310, y, "NPI:", size=9, bold=True)
    text(page, 340, y, "0000000000", size=9)
    y += 14
    text(page, 50,  y, "Referred To:", size=9, bold=True)
    text(page, 160, y, "Dr. FAKE SPECIALIST, MD — Fake Specialty", size=9)
    text(page, 310, y, "Practice:", size=9, bold=True)
    text(page, 355, y, "FAKE CLINIC Associates", size=9)
    y += 14
    text(page, 50,  y, "Referral Date:", size=9, bold=True)
    text(page, 160, y, "January 1, 2024", size=9)
    text(page, 310, y, "Appt. Needed By:", size=9, bold=True)
    text(page, 420, y, "January 14, 2024", size=9)  # tight window — flag

    hline(page, 50, 545, y + 14)
    y += 28

    # Diagnosis
    text(page, 50, y, "DIAGNOSIS & REASON FOR REFERRAL", size=11, bold=True)
    y += 16
    text(page, 50, y, "Primary Diagnosis:", size=9, bold=True)
    text(page, 160, y, "FAKE-001 — Fake Primary Condition, unspecified", size=9)
    y += 14
    text(page, 50, y, "Secondary Diagnosis:", size=9, bold=True)
    text(page, 160, y, "FAKE-002 — Fake Secondary Condition, mild", size=9)
    y += 14
    text(page, 50, y, "Reason for Referral:", size=9, bold=True)
    y += 13
    text(page, 60, y,
         "FAKE PATIENT presents with fake symptoms requiring specialist evaluation.", size=9)
    y += 13
    text(page, 60, y,
         "Recommend urgent assessment and initiation of FAKE MEDICINE as appropriate.", size=9)

    hline(page, 50, 545, y + 14)
    y += 28

    # Services Requested
    text(page, 50, y, "SERVICES REQUESTED", size=11, bold=True)
    y += 14

    services = [
        ("FAKE SPECIALIST Consultation", "URGENT",  "Full workup including FAKE SCAN"),
        ("FAKE PROCEDURE A",             "URGENT",  "Rule out FAKE CONDITION"),
        ("FAKE LAB TEST",                "Routine", "FAKE MEDICINE levels panel"),
        ("FAKE IMAGING",                 "Routine", "If FAKE PROCEDURE inconclusive"),
    ]

    # Table header
    text(page, 50,  y, "Service", size=9, bold=True)
    text(page, 230, y, "Priority", size=9, bold=True)
    text(page, 310, y, "Notes", size=9, bold=True)
    hline(page, 50, 545, y + 6, width=0.8)
    y += 18

    for svc, priority, notes in services:
        text(page, 50,  y, svc, size=9)
        text(page, 230, y, priority, size=9,
             color=(0.8, 0.1, 0.1) if priority == "URGENT" else (0, 0, 0))
        text(page, 310, y, notes, size=9, color=(0.3, 0.3, 0.3))
        hline(page, 50, 545, y + 8, width=0.3)
        y += 20

    # Footer / Signature
    hline(page, 50, 545, y + 4, width=1.0)
    y += 16
    text(page, 50, y, "Referring Physician Signature:", size=9, bold=True)
    text(page, 50, y + 18, "Dr. FAKE DOCTOR, MD", size=10, bold=True)
    text(page, 50, y + 32, "Date: January 1, 2024", size=9)

    out = OUT_DIR / "sample_referral.pdf"
    doc.save(str(out))
    print(f"Referral saved to: {out}")
    print("Intentional flags for testing:")
    print("  - Authorization No. is missing")
    print("  - Appointment needed within 14 days (urgent timeline)")
    print("  - Two URGENT priority services")


if __name__ == "__main__":
    make_contract()
    make_referral()
