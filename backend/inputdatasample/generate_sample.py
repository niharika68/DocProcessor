"""
Run from project root:
  poetry run python backend/inputdatasample/generate_sample.py
Outputs: backend/inputdatasample/sample_invoice.pdf
"""
import fitz  # PyMuPDF
from pathlib import Path

OUT = Path(__file__).parent / "sample_invoice.pdf"
PAGE_W, PAGE_H = 595, 842  # A4 points


def add_text(page, x, y, text, size=10, bold=False, color=(0, 0, 0)):
    font = "helv" if not bold else "hebo"
    page.insert_text((x, y), text, fontname=font, fontsize=size, color=color)


def hline(page, x0, x1, y, width=0.5):
    page.draw_line((x0, y), (x1, y), width=width, color=(0.6, 0.6, 0.6))


doc = fitz.open()
page = doc.new_page(width=PAGE_W, height=PAGE_H)

# ── Header ────────────────────────────────────────────────────────────────
add_text(page, 50, 60, "ACME SUPPLIES INC.", size=18, bold=True, color=(0.1, 0.1, 0.5))
add_text(page, 50, 78, "123 Commerce Street, Austin, TX 78701", size=9, color=(0.4, 0.4, 0.4))
add_text(page, 50, 90, "Phone: (512) 555-0199  |  billing@acmesupplies.com", size=9, color=(0.4, 0.4, 0.4))

add_text(page, 380, 60, "INVOICE", size=22, bold=True, color=(0.1, 0.1, 0.5))
add_text(page, 380, 85, "Invoice #:   INV-2024-0047", size=10)
add_text(page, 380, 100, "Invoice Date: March 10, 2024", size=10)
add_text(page, 380, 115, "Due Date:     April 9, 2024", size=10)
add_text(page, 380, 130, "PO Number:   PO-8821", size=10)

hline(page, 50, 545, 145, width=1.5)

# ── Bill To ───────────────────────────────────────────────────────────────
add_text(page, 50, 165, "BILL TO", size=9, bold=True, color=(0.4, 0.4, 0.4))
add_text(page, 50, 180, "Citation Technologies LLC", size=11, bold=True)
add_text(page, 50, 195, "456 Innovation Drive, Suite 200", size=10)
add_text(page, 50, 208, "San Francisco, CA 94105", size=10)
add_text(page, 50, 221, "Attn: Accounts Payable", size=10)

# ── Line Items Table ──────────────────────────────────────────────────────
TABLE_Y = 260
add_text(page, 50,  TABLE_Y, "DESCRIPTION",  size=9, bold=True)
add_text(page, 270, TABLE_Y, "QTY",          size=9, bold=True)
add_text(page, 320, TABLE_Y, "UNIT PRICE",   size=9, bold=True)
add_text(page, 420, TABLE_Y, "TOTAL",        size=9, bold=True)
hline(page, 50, 545, TABLE_Y + 6, width=1.0)

rows = [
    # description,                       qty, unit_price, total (last one is wrong for anomaly test)
    ("Cloud Storage Subscription (1 yr)", "2",  "$1,200.00", "$2,400.00"),
    ("Professional Services - Setup",     "10", "$150.00",   "$1,500.00"),
    ("API Access License",                "5",  "$299.00",   "$1,495.00"),
    ("Support & Maintenance Package",     "1",  "$850.00",   "$850.00"),
    # Deliberate anomaly: 3 × $75.00 should be $225.00, not $275.00
    ("Data Export Module",                "3",  "$75.00",    "$275.00"),
]

y = TABLE_Y + 20
for desc, qty, price, total in rows:
    add_text(page, 50,  y, desc,  size=10)
    add_text(page, 270, y, qty,   size=10)
    add_text(page, 320, y, price, size=10)
    add_text(page, 420, y, total, size=10)
    hline(page, 50, 545, y + 8, width=0.3)
    y += 22

# ── Totals ────────────────────────────────────────────────────────────────
hline(page, 330, 545, y + 4, width=0.8)
y += 18
add_text(page, 330, y, "Subtotal:", size=10)
add_text(page, 420, y, "$6,520.00", size=10)   # correct sum would be $6,470.00 (another anomaly)

y += 18
add_text(page, 330, y, "Tax (8.25%):", size=10)
add_text(page, 420, y, "$537.90", size=10)

y += 18
hline(page, 330, 545, y - 4, width=0.8)
add_text(page, 330, y, "TOTAL DUE:", size=11, bold=True)
add_text(page, 420, y, "$7,057.90", size=11, bold=True, color=(0.1, 0.1, 0.5))

# ── Payment Terms ─────────────────────────────────────────────────────────
y += 50
hline(page, 50, 545, y - 10, width=0.5)
add_text(page, 50, y, "Payment Terms", size=9, bold=True, color=(0.4, 0.4, 0.4))
add_text(page, 50, y + 15, "Please remit payment within 30 days. Late payments subject to 1.5% monthly interest.", size=9)
add_text(page, 50, y + 28, "Wire Transfer: First National Bank  |  Routing: 021000089  |  Account: 4471009922", size=9)

# ── Footer ────────────────────────────────────────────────────────────────
add_text(page, 50, PAGE_H - 40, "Thank you for your business!", size=9, color=(0.4, 0.4, 0.4))
add_text(page, 50, PAGE_H - 28, "Questions? Contact billing@acmesupplies.com", size=9, color=(0.4, 0.4, 0.4))

doc.save(str(OUT))
print(f"Sample invoice saved to: {OUT}")
print("Intentional anomalies for testing:")
print("  - Data Export Module: 3 × $75.00 = $225.00, but listed as $275.00")
print("  - Subtotal $6,520.00 does not match sum of line items ($6,470.00 corrected)")
