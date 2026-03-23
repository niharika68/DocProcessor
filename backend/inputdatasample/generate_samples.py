"""
Run from project root:
  poetry run python backend/inputdatasample/generate_samples.py
Outputs:
  backend/inputdatasample/sample_contract.pdf   (10 pages)
  backend/inputdatasample/sample_referral.pdf   (3 pages)
"""
import fitz
from pathlib import Path

OUT_DIR = Path(__file__).parent
PAGE_W, PAGE_H = 595, 842  # A4


def text(page, x, y, content, size=10, bold=False, color=(0, 0, 0)):
    page.insert_text((x, y), content, fontname="hebo" if bold else "helv", fontsize=size, color=color)


def hline(page, x0, x1, y, width=0.5):
    page.draw_line((x0, y), (x1, y), width=width, color=(0.6, 0.6, 0.6))


def section(page, y, title):
    text(page, 50, y, title, size=11, bold=True, color=(0.1, 0.1, 0.4))
    return y + 18


def page_header(page, title, contract_no):
    text(page, 50, 40, title, size=9, color=(0.5, 0.5, 0.5))
    text(page, 400, 40, f"Contract No: {contract_no}", size=9, color=(0.5, 0.5, 0.5))
    hline(page, 50, 545, 50, width=0.5)


def page_footer(page, page_num, total):
    hline(page, 50, 545, PAGE_H - 30, width=0.3)
    text(page, 50, PAGE_H - 18, "CONFIDENTIAL — PHARMACEUTICAL SUPPLY AGREEMENT", size=7, color=(0.6, 0.6, 0.6))
    text(page, 490, PAGE_H - 18, f"Page {page_num} of {total}", size=7, color=(0.6, 0.6, 0.6))


# ── CONTRACT (10 pages) ───────────────────────────────────────────────────────

def make_contract():
    doc = fitz.open()
    CONTRACT_NO = "PSA-2024-0092"
    TOTAL_PAGES = 10

    # ── Page 1: Cover / Parties ──────────────────────────────────────────────
    p1 = doc.new_page(width=PAGE_W, height=PAGE_H)
    text(p1, 50, 80, "PHARMACEUTICAL SUPPLY AGREEMENT", size=20, bold=True, color=(0.1, 0.1, 0.4))
    text(p1, 50, 106, f"Contract No: {CONTRACT_NO}", size=11)
    text(p1, 50, 122, "Effective Date:   January 1, 2024", size=10)
    text(p1, 50, 136, "Expiration Date:  December 31, 2025", size=10)
    text(p1, 50, 150, "Contract Term:    24 months", size=10)
    hline(p1, 50, 545, 165, width=1.5)

    y = section(p1, 182, "PARTY A — VENDOR / SUPPLIER")
    text(p1, 50, y,       "Company Name:   Vantage MedSupply Distribution Co.", size=10)
    text(p1, 50, y + 14,  "Address:        3300 Industrial Parkway, Columbus, OH 43219", size=10)
    text(p1, 50, y + 28,  "Phone:          (614) 555-0100", size=10)
    text(p1, 50, y + 42,  "DEA License:    RV1234567", size=10)
    text(p1, 50, y + 56,  "Authorized Rep: Douglas Carmichael, VP of Sales", size=10)
    hline(p1, 50, 545, y + 72)

    y2 = section(p1, y + 88, "PARTY B — HOSPITAL PHARMACY")
    text(p1, 50, y2,       "Institution:    Stonebridge Regional Medical Center — Pharmacy Services", size=10)
    text(p1, 50, y2 + 14,  "Address:        800 Stonebridge Blvd, Hartford, CT 06103", size=10)
    text(p1, 50, y2 + 28,  "Phone:          (860) 555-0200", size=10)
    text(p1, 50, y2 + 42,  "DEA License:    FS9876543", size=10)
    text(p1, 50, y2 + 56,  "Authorized Rep: Dr. Renata Kowalski, PharmD, Director of Pharmacy", size=10)
    hline(p1, 50, 545, y2 + 72)

    y3 = section(p1, y2 + 88, "RECITALS")
    recitals = [
        "WHEREAS, Vendor is a licensed pharmaceutical distributor authorized to supply Schedule II–V",
        "controlled substances, specialty biologics, and general pharmaceutical products;",
        "WHEREAS, Hospital Pharmacy requires a reliable supply chain for formulary medications",
        "to support inpatient, outpatient, and emergency care services;",
        "NOW, THEREFORE, in consideration of the mutual covenants herein, the parties agree as follows.",
    ]
    for line in recitals:
        text(p1, 60, y3, line, size=9, color=(0.2, 0.2, 0.2))
        y3 += 13
    page_footer(p1, 1, TOTAL_PAGES)

    # ── Page 2: Contract Value & Payment Terms ───────────────────────────────
    p2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p2, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p2, 75, "ARTICLE 1 — CONTRACT VALUE & PAYMENT TERMS")
    rows = [
        ("Estimated Annual Contract Value",  "$1,850,000.00 USD"),
        ("Total 24-Month Commitment",        "$3,700,000.00 USD"),
        ("Payment Terms",                    "Net 45 days from verified delivery"),
        ("Minimum Order — Per Quarter",      "$75,000.00 USD"),
        ("Early Payment Discount",           "1.5% if paid within 10 days of invoice"),
        ("Late Payment Penalty",             "2.0% per month on outstanding balance"),
        ("Invoice Submission Deadline",      "Within 5 business days of delivery"),
        ("Preferred Payment Method",         "ACH bank transfer (wire fees borne by payer)"),
        ("Currency",                         "United States Dollars (USD)"),
    ]
    for label, val in rows:
        text(p2, 50, y, label + ":", size=9, bold=True)
        text(p2, 270, y, val, size=9)
        y += 16
    hline(p2, 50, 545, y)

    y = section(p2, y + 14, "ARTICLE 2 — PRICE ADJUSTMENT")
    adj_lines = [
        "2.1  Unit prices in Exhibit B are fixed for the first 12 months of this Agreement.",
        "2.2  Beginning month 13, Vendor may request a price increase not to exceed 4% annually,",
        "     provided 60 days written notice is given and supported by published CPI data.",
        "2.3  Hospital Pharmacy may reject proposed price increases within 30 days of notice.",
        "     Rejection triggers a 30-day renegotiation window; failure to agree allows either",
        "     party to terminate this Agreement with 60 days notice.",
        "2.4  Emergency drug shortages declared by the FDA may trigger temporary surcharges",
        "     not to exceed 12% of contracted unit price, subject to written mutual agreement.",
    ]
    for line in adj_lines:
        text(p2, 50, y, line, size=9, color=(0.2, 0.2, 0.2))
        y += 13
    hline(p2, 50, 545, y)

    y = section(p2, y + 14, "ARTICLE 3 — ORDERING PROCEDURE")
    order_lines = [
        "3.1  Hospital Pharmacy shall submit purchase orders via the Vendor's secure EDI portal.",
        "3.2  Standard orders require 48-hour lead time; emergency orders require 6-hour response.",
        "3.3  Order acknowledgment by Vendor within 2 hours of submission is mandatory.",
        "3.4  Partial deliveries must be noted on the delivery manifest; unannounced partial",
        "     deliveries will be treated as shortfalls under Article 5.",
    ]
    for line in order_lines:
        text(p2, 50, y, line, size=9, color=(0.2, 0.2, 0.2))
        y += 13
    page_footer(p2, 2, TOTAL_PAGES)

    # ── Page 3: Formulary Pricing Schedule (Exhibit A sample) ───────────────
    p3 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p3, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p3, 75, "EXHIBIT A — FORMULARY PRICING SCHEDULE (Selected Items)")
    text(p3, 50, y, "Prices are per unit (vial, tablet, bag) as specified. All prices in USD.", size=9, color=(0.4, 0.4, 0.4))
    y += 18

    # Table header
    cols = [50, 120, 230, 310, 390, 470]
    headers = ["NDC", "Drug Name", "Form / Strength", "Unit", "Contract $", "List $"]
    for c, h in zip(cols, headers):
        text(p3, c, y, h, size=9, bold=True)
    hline(p3, 50, 545, y + 8, width=0.8)
    y += 18

    formulary = [
        ("0069-4190-30", "Amoxicillin",          "Cap 500 mg",        "Each",  "$0.18",  "$0.42"),
        ("0006-0951-58", "Lisinopril",            "Tab 10 mg",         "Each",  "$0.09",  "$0.21"),
        ("0093-7244-98", "Atorvastatin",          "Tab 40 mg",         "Each",  "$0.22",  "$0.58"),
        ("0002-8215-01", "Insulin Lispro",        "Vial 100U/mL 10mL", "Vial",  "$28.40", "$68.00"),
        ("0338-0049-03", "0.9% NaCl IV",          "Bag 1000 mL",       "Bag",   "$1.95",  "$4.50"),
        ("0143-9682-10", "Vancomycin HCl",        "Vial 1g",           "Vial",  "$5.80",  "$14.20"),
        ("0517-0730-25", "Morphine Sulfate",      "Vial 10mg/mL 30mL", "Vial",  "$9.10",  "$22.00"),
        ("63323-0173-10","Ondansetron HCl",       "Vial 2mg/mL 20mL",  "Vial",  "$3.40",  "$8.75"),
        ("0069-3070-83", "Piperacillin/Tazobactam","Vial 3.375g",      "Vial",  "$12.60", "$30.00"),
        ("0641-6018-25", "Heparin Sodium",        "Vial 5000U/mL",     "Vial",  "$4.20",  "$9.80"),
        ("0074-3805-02", "Dexamethasone Na Phos", "Vial 4mg/mL 1mL",   "Vial",  "$1.85",  "$4.40"),
        ("0069-3150-20", "Metronidazole",         "Bag 500mg/100mL",   "Bag",   "$3.10",  "$7.20"),
        ("0049-0610-83", "Azithromycin",          "Tab 250 mg",        "Each",  "$0.55",  "$1.30"),
        ("0002-7140-01", "Enoxaparin Na",         "Syringe 40mg/0.4mL","Each",  "$8.90",  "$21.50"),
        ("0013-2013-94", "Norepinephrine",        "Amp 4mg/4mL",       "Amp",   "$6.75",  "$15.80"),
        ("0517-4601-25", "Labetalol HCl",         "Vial 5mg/mL 20mL",  "Vial",  "$4.60",  "$11.00"),
        ("0006-3598-54", "Finasteride",           "Tab 5 mg",          "Each",  "$0.38",  "$0.95"),
        ("0121-4285-16", "Cefazolin Na",          "Vial 1g",           "Vial",  "$3.20",  "$7.50"),
    ]
    for row in formulary:
        for c, val in zip(cols, row):
            text(p3, c, y, val, size=8)
        hline(p3, 50, 545, y + 8, width=0.2)
        y += 16

    text(p3, 50, y + 8, "* Full formulary of 480 line items available in Exhibit A-Full (attached digitally).", size=8, color=(0.5, 0.5, 0.5))
    page_footer(p3, 3, TOTAL_PAGES)

    # ── Page 4: Delivery & Logistics ────────────────────────────────────────
    p4 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p4, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p4, 75, "ARTICLE 4 — DELIVERY, LOGISTICS & COLD-CHAIN COMPLIANCE")
    delivery_clauses = [
        ("4.1 Delivery Schedule",
         "Standard deliveries shall occur Monday through Friday between 07:00 and 15:00 local\n"
         "time at the Hospital Pharmacy loading dock. Holiday schedules require 5 business days\n"
         "advance coordination."),
        ("4.2 Cold-Chain Requirements",
         "Refrigerated products (2°C–8°C) must be shipped in validated cold-chain containers\n"
         "with continuous temperature loggers. Logs must be provided with each delivery.\n"
         "Frozen biologics must maintain ≤ -20°C throughout transit."),
        ("4.3 Temperature Excursion Liability",
         "Any product delivered outside specified temperature range shall be rejected by Hospital\n"
         "Pharmacy and returned at Vendor's expense within 24 hours. Vendor bears full liability\n"
         "for cold-chain failures during transit including replacement cost and expedited freight."),
        ("4.4 Controlled Substances",
         "Schedule II–V controlled substances must be delivered with DEA Form 222 or equivalent\n"
         "CSOS electronic record. Chain of custody documentation is mandatory. Discrepancies\n"
         "exceeding $500 in value must be reported to the DEA within 1 business day."),
        ("4.5 Short-Dated Products",
         "Vendor shall not ship products with fewer than 6 months remaining shelf life unless\n"
         "Hospital Pharmacy provides prior written consent. Products received short-dated without\n"
         "consent are subject to full credit."),
        ("4.6 Delivery Confirmation",
         "Hospital Pharmacy shall provide signed delivery receipt within 4 hours of delivery.\n"
         "Receipt does not waive right to reject products upon pharmacist inspection within 48 hours."),
    ]
    for title, body in delivery_clauses:
        text(p4, 50, y, title, size=10, bold=True, color=(0.1, 0.1, 0.4))
        y += 14
        for line in body.split("\n"):
            text(p4, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
            y += 13
        y += 6
    page_footer(p4, 4, TOTAL_PAGES)

    # ── Page 5: Quality & Regulatory Compliance ──────────────────────────────
    p5 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p5, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p5, 75, "ARTICLE 5 — QUALITY, COMPLIANCE & PRODUCT RECALLS")
    quality_clauses = [
        ("5.1 FDA Registration",
         "Vendor represents and warrants that it holds current FDA Drug Distributor registration\n"
         "and all state wholesale distributor licenses in states of operation. Lapse of any\n"
         "license must be disclosed within 24 hours of Vendor becoming aware of such lapse."),
        ("5.2 Product Authenticity",
         "All products must be sourced directly from FDA-registered manufacturers or authorized\n"
         "tier-1 distributors. Vendor shall maintain chain-of-custody records (pedigree documents)\n"
         "for each product line for a minimum of 3 years and provide records upon request within\n"
         "5 business days."),
        ("5.3 Recall Notification",
         "Upon receiving any FDA recall notice (Class I, II, or III) affecting contracted products,\n"
         "Vendor shall notify Hospital Pharmacy within 4 hours by phone and within 24 hours in\n"
         "writing. Vendor shall arrange pick-up of recalled products within 2 business days."),
        ("5.4 Drug Shortage Reporting",
         "Vendor shall notify Hospital Pharmacy no less than 14 days before any anticipated\n"
         "shortage affecting products with >$10,000 annual contract value. Notice must include\n"
         "expected duration, substitute product options, and interim pricing."),
        ("5.5 Audits",
         "Hospital Pharmacy reserves the right to audit Vendor's warehouse and distribution\n"
         "operations once annually with 30 days written notice. Vendor must remediate any\n"
         "USP, FDA, or state board findings within 60 days of audit report."),
        ("5.6 Product Non-Conformance",
         "Hospital Pharmacy may reject any lot with documented non-conformance within 48 hours\n"
         "of delivery. Vendor shall issue full credit within 5 business days of rejected return."),
    ]
    for title, body in quality_clauses:
        text(p5, 50, y, title, size=10, bold=True, color=(0.1, 0.1, 0.4))
        y += 14
        for line in body.split("\n"):
            text(p5, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
            y += 13
        y += 6
    page_footer(p5, 5, TOTAL_PAGES)

    # ── Page 6: Term, Auto-Renewal & Termination ────────────────────────────
    p6 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p6, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p6, 75, "ARTICLE 6 — TERM, AUTO-RENEWAL & TERMINATION")
    term_clauses = [
        ("6.1 Initial Term",
         "This Agreement commences January 1, 2024 and expires December 31, 2025."),
        ("6.2 Automatic Renewal",                    # INTENTIONAL RISK
         "This Agreement shall automatically renew for successive one-year terms unless either\n"
         "party provides written notice of non-renewal at least 120 days prior to the expiration\n"
         "date. Failure to provide timely notice shall constitute binding renewal. Notice sent\n"
         "by email is not accepted — written notice must be sent by certified mail only."),
        ("6.3 Termination for Cause",
         "Either party may terminate immediately upon written notice if the other party:\n"
         "(a) materially breaches this Agreement and fails to cure within 30 days of notice;\n"
         "(b) becomes insolvent, assigns for benefit of creditors, or enters bankruptcy;\n"
         "(c) loses any license, permit, or accreditation required for performance."),
        ("6.4 Termination for Convenience",          # INTENTIONAL RISK
         "Hospital Pharmacy may terminate this Agreement for convenience with 180 days written\n"
         "notice. Vendor may terminate for convenience with 180 days notice. In either case,\n"
         "a termination fee equal to 15% of the remaining contract value shall be payable\n"
         "by the terminating party."),
        ("6.5 Wind-Down Obligations",
         "Upon expiration or termination: (a) Vendor shall fulfill all open purchase orders\n"
         "submitted before the termination notice date; (b) Hospital Pharmacy shall pay all\n"
         "undisputed invoices within 60 days; (c) parties shall cooperate for 90 days on\n"
         "transition to a replacement supplier."),
        ("6.6 Survival",
         "Articles 7, 8, 10, and 11 survive expiration or termination of this Agreement."),
    ]
    for title, body in term_clauses:
        text(p6, 50, y, title, size=10, bold=True, color=(0.1, 0.1, 0.4))
        y += 14
        for line in body.split("\n"):
            text(p6, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
            y += 13
        y += 6
    page_footer(p6, 6, TOTAL_PAGES)

    # ── Page 7: Liability & Indemnification ─────────────────────────────────
    p7 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p7, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p7, 75, "ARTICLE 7 — LIABILITY, INDEMNIFICATION & INSURANCE")
    liab_clauses = [
        ("7.1 Limitation of Vendor Liability",       # INTENTIONAL RISK
         "VENDOR'S TOTAL LIABILITY FOR ANY CLAIM ARISING UNDER THIS AGREEMENT, INCLUDING\n"
         "PRODUCT DEFECTS, RECALLS, OR DELIVERY FAILURES, SHALL NOT EXCEED THE VALUE OF\n"
         "THE SPECIFIC PURCHASE ORDER GIVING RISE TO THE CLAIM. VENDOR SHALL NOT BE LIABLE\n"
         "FOR CONSEQUENTIAL, INCIDENTAL, INDIRECT, OR PUNITIVE DAMAGES, INCLUDING PATIENT\n"
         "HARM OR LOSS OF LIFE, EVEN IF ADVISED OF SUCH POSSIBILITY."),
        ("7.2 Hospital Pharmacy Indemnification",
         "Hospital Pharmacy shall indemnify and hold harmless Vendor from any third-party\n"
         "claims arising from Hospital Pharmacy's storage, handling, dispensing, or\n"
         "administration of products after delivery, provided products were delivered in\n"
         "conformance with this Agreement."),
        ("7.3 Vendor Indemnification",
         "Vendor shall indemnify Hospital Pharmacy from third-party claims arising from\n"
         "product defects, adulteration, mislabeling, or cold-chain failures attributable\n"
         "to Vendor's acts or omissions prior to delivery."),
        ("7.4 Insurance Requirements",
         "Vendor shall maintain at its own expense:\n"
         "  (a) Commercial General Liability — min. $5,000,000 per occurrence\n"
         "  (b) Product Liability — min. $10,000,000 per occurrence\n"
         "  (c) Errors & Omissions — min. $2,000,000\n"
         "  (d) Workers' Compensation — statutory limits\n"
         "Certificates of insurance naming Hospital Pharmacy as additional insured are due\n"
         "within 10 days of execution and annually upon renewal."),
        ("7.5 Mutual Waiver of Consequential Damages",   # INTENTIONAL RISK
         "BOTH PARTIES WAIVE ANY CLAIM FOR LOST PROFITS, LOST REVENUE, OR BUSINESS\n"
         "INTERRUPTION, REGARDLESS OF THE FORM OF ACTION OR LEGAL THEORY ASSERTED."),
    ]
    for title, body in liab_clauses:
        text(p7, 50, y, title, size=10, bold=True, color=(0.1, 0.1, 0.4))
        y += 14
        for line in body.split("\n"):
            text(p7, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
            y += 13
        y += 6
    page_footer(p7, 7, TOTAL_PAGES)

    # ── Page 8: Confidentiality & Data Protection ────────────────────────────
    p8 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p8, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p8, 75, "ARTICLE 8 — CONFIDENTIALITY & DATA PROTECTION")
    conf_clauses = [
        ("8.1 Definition of Confidential Information",
         "Confidential Information means all non-public pricing, formulary data, patient\n"
         "utilization statistics, operational processes, and financial terms disclosed by\n"
         "either party in connection with this Agreement."),
        ("8.2 Non-Disclosure Obligations",
         "Each party shall: (a) hold Confidential Information in strict confidence;\n"
         "(b) use Confidential Information solely for purposes of performing this Agreement;\n"
         "(c) not disclose to any third party without prior written consent;\n"
         "(d) limit internal disclosure to employees with a need to know."),
        ("8.3 HIPAA Compliance",
         "To the extent Vendor handles Protected Health Information (PHI) as defined under\n"
         "HIPAA, Vendor agrees to execute a Business Associate Agreement (BAA) concurrent\n"
         "with this Agreement and comply with all applicable HIPAA/HITECH requirements."),
        ("8.4 Data Breach Notification",
         "In the event of a data breach involving either party's Confidential Information or\n"
         "PHI, the breached party shall notify the other within 48 hours of discovery. Notice\n"
         "shall include nature of breach, data categories affected, and remediation plan."),
        ("8.5 Duration of Confidentiality Obligations",
         "Confidentiality obligations survive expiration or termination of this Agreement for\n"
         "a period of 5 years. Trade secrets receive perpetual protection under applicable law."),
        ("8.6 Return of Information",
         "Upon termination, each party shall promptly return or destroy the other's Confidential\n"
         "Information and certify in writing that destruction is complete within 30 days."),
    ]
    for title, body in conf_clauses:
        text(p8, 50, y, title, size=10, bold=True, color=(0.1, 0.1, 0.4))
        y += 14
        for line in body.split("\n"):
            text(p8, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
            y += 13
        y += 6
    page_footer(p8, 8, TOTAL_PAGES)

    # ── Page 9: Force Majeure, Dispute Resolution, Governing Law ────────────
    p9 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p9, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p9, 75, "ARTICLE 9 — FORCE MAJEURE")
    fm_lines = [
        "9.1  Neither party shall be in default if performance is prevented by events beyond its",
        "     reasonable control including natural disasters, pandemics, government orders, acts",
        "     of war, or FDA-mandated plant shutdowns (collectively, 'Force Majeure Events').",
        "9.2  The affected party shall notify the other within 48 hours of a Force Majeure Event,",
        "     including expected duration and a mitigation plan.",
        "9.3  If a Force Majeure Event prevents performance for more than 60 consecutive days,",
        "     either party may terminate this Agreement without penalty on 10 days written notice.",
        "9.4  Supply shortage due to Vendor's own operational failures does NOT constitute Force",
        "     Majeure and remains subject to breach and shortfall remedies under Article 5.",
    ]
    for line in fm_lines:
        text(p9, 50, y, line, size=9, color=(0.2, 0.2, 0.2))
        y += 13
    hline(p9, 50, 545, y)

    y = section(p9, y + 14, "ARTICLE 10 — DISPUTE RESOLUTION")
    dr_lines = [
        "10.1  The parties shall attempt to resolve any dispute through good-faith negotiation",
        "      between senior representatives within 15 business days of written notice of dispute.",
        "10.2  If unresolved after 15 business days, disputes shall be submitted to non-binding",
        "      mediation under the AAA Commercial Mediation Rules in Hartford, CT.",
        "10.3  If mediation fails within 45 days, disputes shall proceed to binding arbitration",
        "      before a single arbitrator under AAA Commercial Arbitration Rules.",
        "10.4  Notwithstanding the above, either party may seek injunctive relief in a court of",
        "      competent jurisdiction to prevent irreparable harm pending arbitration.",
    ]
    for line in dr_lines:
        text(p9, 50, y, line, size=9, color=(0.2, 0.2, 0.2))
        y += 13
    hline(p9, 50, 545, y)

    y = section(p9, y + 14, "ARTICLE 11 — GENERAL PROVISIONS")
    gen_lines = [
        "11.1  Governing Law: This Agreement is governed by the laws of the State of Connecticut.",
        "11.2  Entire Agreement: This Agreement, including all Exhibits, constitutes the entire",
        "      agreement and supersedes all prior negotiations, representations, and agreements.",
        "11.3  Amendments: This Agreement may only be amended by a written instrument signed by",
        "      authorized representatives of both parties.",
        "11.4  Severability: If any provision is found unenforceable, the remaining provisions",
        "      remain in full force and effect.",
        "11.5  Waiver: Failure to enforce any right is not a waiver of future enforcement.",
        "11.6  Assignment: Neither party may assign this Agreement without prior written consent,",
        "      except in connection with a merger or acquisition of all or substantially all assets.",
        "11.7  Notices: All notices must be in writing and delivered by certified mail or overnight",
        "      courier to the addresses on Page 1. Email notices are not valid for legal purposes.",
        "11.8  Counterparts: This Agreement may be executed in counterparts, each of which is an",
        "      original, and together constitute one Agreement.",
    ]
    for line in gen_lines:
        text(p9, 50, y, line, size=9, color=(0.2, 0.2, 0.2))
        y += 13
    page_footer(p9, 9, TOTAL_PAGES)

    # ── Page 10: Execution / Signatures ─────────────────────────────────────
    p10 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p10, "PHARMACEUTICAL SUPPLY AGREEMENT", CONTRACT_NO)
    y = section(p10, 75, "SIGNATURE PAGE — EXECUTION")
    text(p10, 50, y, "IN WITNESS WHEREOF, the authorized representatives of each party have executed this", size=10)
    y += 14
    text(p10, 50, y, "Pharmaceutical Supply Agreement as of the Effective Date first written above.", size=10)
    hline(p10, 50, 545, y + 18, width=1.0)
    y += 36

    # Two-column signature blocks
    text(p10, 50, y, "PARTY A — VENDOR", size=11, bold=True, color=(0.1, 0.1, 0.4))
    text(p10, 320, y, "PARTY B — HOSPITAL PHARMACY", size=11, bold=True, color=(0.1, 0.1, 0.4))
    y += 20

    text(p10, 50, y, "Signature: ___________________________", size=10)
    text(p10, 320, y, "Signature: ___________________________", size=10)
    y += 20
    text(p10, 50, y, "Printed Name: Douglas Carmichael", size=10)
    text(p10, 320, y, "Printed Name: Dr. Renata Kowalski, PharmD", size=10)
    y += 14
    text(p10, 50, y, "Title: VP of Sales", size=10)
    text(p10, 320, y, "Title: Director of Pharmacy", size=10)
    y += 14
    text(p10, 50, y, "Company: Vantage MedSupply Distribution Co.", size=10)
    text(p10, 320, y, "Institution: Stonebridge Regional Medical Center", size=10)
    y += 14
    text(p10, 50, y, "Date: _______________", size=10)
    text(p10, 320, y, "Date: _______________", size=10)
    hline(p10, 50, 545, y + 20, width=0.5)
    y += 40

    # Exhibits list
    y = section(p10, y, "EXHIBITS INCORPORATED BY REFERENCE")
    exhibits = [
        ("Exhibit A",      "Full Formulary List (480 line items, digital attachment)"),
        ("Exhibit A-1",    "Controlled Substances Sub-Schedule"),
        ("Exhibit B",      "Unit Price Schedule — Year 1 (Jan 2024 – Dec 2024)"),
        ("Exhibit B-1",    "Unit Price Schedule — Year 2 (Jan 2025 – Dec 2025)"),
        ("Exhibit C",      "Cold-Chain Compliance Standards and Logger Specifications"),
        ("Exhibit D",      "Business Associate Agreement (HIPAA BAA)"),
        ("Exhibit E",      "DEA License Copies — Vendor and Hospital Pharmacy"),
        ("Exhibit F",      "Insurance Certificates — Vendor"),
        ("Exhibit G",      "EDI Portal Access Instructions and SLA"),
    ]
    for ex, desc in exhibits:
        text(p10, 50, y, ex + ":", size=9, bold=True)
        text(p10, 130, y, desc, size=9)
        y += 15

    text(p10, 50, y + 10, "Contract intentionally includes the following risks for testing:", size=8, color=(0.5, 0.5, 0.5))
    text(p10, 50, y + 22, "  • 120-day auto-renewal window, certified mail only (§6.2)", size=8, color=(0.5, 0.5, 0.5))
    text(p10, 50, y + 34, "  • 15% termination-for-convenience fee (§6.4)", size=8, color=(0.5, 0.5, 0.5))
    text(p10, 50, y + 46, "  • Vendor liability capped at single PO value; no patient-harm damages (§7.1)", size=8, color=(0.5, 0.5, 0.5))
    page_footer(p10, 10, TOTAL_PAGES)

    out = OUT_DIR / "sample_contract.pdf"
    doc.save(str(out))
    print(f"Contract saved to: {out}  ({TOTAL_PAGES} pages)")
    print("Intentional risks for testing:")
    print("  - Auto-renewal: 120-day window, certified mail only (§6.2)")
    print("  - Termination for convenience fee: 15% of remaining contract value (§6.4)")
    print("  - Vendor liability capped to single PO value; no patient-harm damages (§7.1)")


# ── REFERRAL (3 pages, real diagnoses, fake names) ────────────────────────────

def make_referral():
    doc = fitz.open()
    TOTAL_PAGES = 3

    # ── Page 1: Patient Info, Providers, Primary Diagnosis ──────────────────
    p1 = doc.new_page(width=PAGE_W, height=PAGE_H)
    text(p1, 50, 50, "PATIENT REFERRAL FORM", size=18, bold=True, color=(0.05, 0.25, 0.45))
    text(p1, 50, 72, "FAKE HOSPITAL MEDICAL GROUP — Cardiology Referral", size=11, bold=True)
    text(p1, 50, 86, "123 Fake Hospital Blvd, Faketown, FK 00001  |  Tel: (000) 555-0000  |  Fax: (000) 555-0001", size=8, color=(0.4, 0.4, 0.4))
    hline(p1, 50, 545, 98, width=1.5)

    y = section(p1, 112, "SECTION 1 — PATIENT INFORMATION")
    fields = [
        ("Patient Name:",       "FAKE PATIENT",         "Date of Birth:",    "03/14/1962"),
        ("Patient ID:",         "MRN-2024-004821",      "Gender:",           "Male"),
        ("Insurance Provider:", "FAKE INSURANCE CO.",   "Member ID:",        "FAKE-INS-88421"),
        ("Group No:",           "FAKE-GRP-001",         "Authorization No:", ""),
        ("Phone:",              "(000) 555-1234",       "Preferred Language:","English"),
        ("Address:",            "456 Fake St, Faketown, FK 00002", "Email:", ""),
    ]
    for lbl, val, lbl2, val2 in fields:
        text(p1, 50, y, lbl, size=9, bold=True)
        text(p1, 160, y, val, size=9)
        text(p1, 310, y, lbl2, size=9, bold=True)
        text(p1, 420, y, val2, size=9)
        y += 15
    hline(p1, 50, 545, y + 2)

    y = section(p1, y + 14, "SECTION 2 — PROVIDER INFORMATION")
    text(p1, 50, y, "Referring Provider:", size=9, bold=True)
    text(p1, 160, y, "Dr. FAKE DOCTOR, MD — Internal Medicine", size=9)
    text(p1, 400, y, "NPI: 1234567890", size=9)
    y += 14
    text(p1, 50, y, "Practice:", size=9, bold=True)
    text(p1, 160, y, "FAKE PRIMARY CARE ASSOCIATES", size=9)
    text(p1, 400, y, "UPIN: B12345", size=9)
    y += 14
    text(p1, 50, y, "Phone / Fax:", size=9, bold=True)
    text(p1, 160, y, "(000) 555-2000 / (000) 555-2001", size=9)
    y += 14
    text(p1, 50, y, "Referred To:", size=9, bold=True)
    text(p1, 160, y, "Dr. FAKE SPECIALIST, MD, FACC — Interventional Cardiology", size=9)
    text(p1, 400, y, "NPI: 0987654321", size=9)
    y += 14
    text(p1, 50, y, "Facility:", size=9, bold=True)
    text(p1, 160, y, "FAKE HEART & VASCULAR INSTITUTE", size=9)
    y += 14
    text(p1, 50, y, "Referral Date:", size=9, bold=True)
    text(p1, 160, y, "March 10, 2024", size=9)
    text(p1, 310, y, "Appt. Needed By:", size=9, bold=True)
    text(p1, 420, y, "March 24, 2024", size=9, color=(0.7, 0.1, 0.1))
    y += 14
    text(p1, 50, y, "Referral Priority:", size=9, bold=True)
    text(p1, 160, y, "URGENT", size=9, bold=True, color=(0.8, 0.1, 0.1))
    hline(p1, 50, 545, y + 14)

    y = section(p1, y + 28, "SECTION 3 — DIAGNOSIS")
    diag_rows = [
        ("Primary Diagnosis:",   "I25.110", "Atherosclerotic heart disease of native coronary artery with unstable angina pectoris"),
        ("Secondary Dx 1:",      "E11.65",  "Type 2 diabetes mellitus with hyperglycemia"),
        ("Secondary Dx 2:",      "I10",     "Essential (primary) hypertension"),
        ("Secondary Dx 3:",      "E78.5",   "Hyperlipidemia, unspecified"),
        ("Secondary Dx 4:",      "Z87.891", "Personal history of nicotine dependence"),
    ]
    for label, code, desc in diag_rows:
        text(p1, 50, y, label, size=9, bold=True)
        text(p1, 155, y, code, size=9, bold=True, color=(0.1, 0.3, 0.6))
        text(p1, 215, y, desc, size=9)
        y += 14
    hline(p1, 50, 545, y)

    y = section(p1, y + 14, "SECTION 4 — REASON FOR REFERRAL")
    reason_lines = [
        "FAKE PATIENT is a 62-year-old male with a 15-year history of Type 2 diabetes and",
        "poorly controlled hypertension (avg BP 158/96 mmHg over past 3 clinic visits) who",
        "presents with new-onset exertional chest pain and dyspnea on exertion (NYHA Class II).",
        "Resting ECG shows ST-segment depression in leads V4–V6. Troponin I mildly elevated at",
        "0.06 ng/mL (ref <0.04 ng/mL). Stress echocardiogram was non-diagnostic due to poor",
        "acoustic window. Referring for urgent cardiology evaluation and consideration of cardiac",
        "catheterization to evaluate for obstructive coronary artery disease.",
    ]
    for line in reason_lines:
        text(p1, 60, y, line, size=9, color=(0.2, 0.2, 0.2))
        y += 13
    page_footer(p1, 1, TOTAL_PAGES)

    # ── Page 2: Clinical History, Medications, Labs & Vitals ────────────────
    p2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p2, "PATIENT REFERRAL — FAKE PATIENT  MRN-2024-004821", "Cardiology")
    y = section(p2, 75, "SECTION 5 — RELEVANT CLINICAL HISTORY")
    hx_lines = [
        "Cardiac History:",
        "  • No prior myocardial infarction documented. No prior cardiac catheterization.",
        "  • Echocardiogram (Feb 2024): EF 52%, mild LV diastolic dysfunction (Grade I),",
        "    no significant valvular abnormality.",
        "  • Holter monitor (Jan 2024): Occasional PVCs, no sustained arrhythmia.",
        "",
        "Relevant Surgical / Procedural History:",
        "  • Appendectomy (1994)",
        "  • Right knee arthroscopy (2018)",
        "  • No prior cardiac procedures.",
        "",
        "Family History:",
        "  • Father: MI at age 58, CABG at age 61 (deceased age 72 — CHF)",
        "  • Mother: Type 2 diabetes, hypertension (living, age 84)",
        "  • Brother (age 55): Coronary artery stenting 2021",
        "",
        "Social History:",
        "  • Former smoker — quit 2011 (20 pack-year history)",
        "  • Alcohol: Rare, < 1 drink/week",
        "  • Sedentary lifestyle; BMI 31.4",
        "  • Retired school administrator",
        "",
        "Allergies:",
        "  • Penicillin — rash (moderate)",
        "  • Sulfonamides — urticaria (moderate)",
        "  • No known contrast media allergy (no prior exposure)",
    ]
    for line in hx_lines:
        text(p2, 50 if not line.startswith("  ") else 60, y, line, size=9, color=(0.15, 0.15, 0.15) if line.endswith(":") else (0.2, 0.2, 0.2))
        y += 13
    hline(p2, 50, 545, y)

    y = section(p2, y + 12, "SECTION 6 — CURRENT MEDICATIONS")
    text(p2, 50, y, "Medication", size=9, bold=True)
    text(p2, 200, y, "Dose / Route / Frequency", size=9, bold=True)
    text(p2, 380, y, "Indication", size=9, bold=True)
    hline(p2, 50, 545, y + 8, width=0.6)
    y += 18
    meds = [
        ("Metformin HCl",           "1000 mg PO BID",            "Type 2 Diabetes"),
        ("Lisinopril",              "20 mg PO daily",            "Hypertension / CKD protection"),
        ("Amlodipine",              "10 mg PO daily",            "Hypertension"),
        ("Atorvastatin",            "80 mg PO nightly",          "Hyperlipidemia / CAD risk"),
        ("Aspirin",                 "81 mg PO daily",            "Antiplatelet / CV prophylaxis"),
        ("Metoprolol Succinate XL", "50 mg PO daily",            "Rate control / Angina"),
        ("Isosorbide Mononitrate",  "30 mg PO daily (ER)",       "Angina symptom control"),
        ("Nitroglycerin SL",        "0.4 mg PRN chest pain",     "Acute angina"),
        ("Empagliflozin",           "10 mg PO daily",            "T2DM / CV risk reduction"),
        ("Pantoprazole",            "40 mg PO daily",            "GI prophylaxis with ASA"),
    ]
    for med, dose, indication in meds:
        text(p2, 50, y, med, size=9)
        text(p2, 200, y, dose, size=9)
        text(p2, 380, y, indication, size=9, color=(0.3, 0.3, 0.3))
        hline(p2, 50, 545, y + 9, width=0.2)
        y += 17
    hline(p2, 50, 545, y, width=0.5)

    y = section(p2, y + 12, "SECTION 7 — RECENT LABS (March 8, 2024)")
    text(p2, 50, y, "Test", size=9, bold=True)
    text(p2, 220, y, "Result", size=9, bold=True)
    text(p2, 300, y, "Reference Range", size=9, bold=True)
    text(p2, 420, y, "Status", size=9, bold=True)
    hline(p2, 50, 545, y + 8, width=0.6)
    y += 18
    labs = [
        ("HbA1c",                 "8.2%",          "< 7.0%",            "HIGH", True),
        ("Fasting Glucose",       "178 mg/dL",      "70–99 mg/dL",       "HIGH", True),
        ("Creatinine",            "1.28 mg/dL",     "0.74–1.35 mg/dL",   "Normal", False),
        ("eGFR",                  "62 mL/min/1.73m²","≥ 60",             "Normal", False),
        ("LDL Cholesterol",       "118 mg/dL",      "< 70 mg/dL (high risk)","HIGH", True),
        ("HDL Cholesterol",       "38 mg/dL",       "> 40 mg/dL",        "LOW", True),
        ("Triglycerides",         "214 mg/dL",      "< 150 mg/dL",       "HIGH", True),
        ("hsCRP",                 "4.8 mg/L",       "< 1.0 mg/L",        "HIGH", True),
        ("Troponin I",            "0.06 ng/mL",     "< 0.04 ng/mL",      "HIGH", True),
        ("BNP",                   "88 pg/mL",       "< 100 pg/mL",       "Borderline", True),
        ("Hemoglobin",            "13.4 g/dL",      "13.5–17.5 g/dL",    "LOW", True),
        ("Potassium",             "4.1 mEq/L",      "3.5–5.0 mEq/L",     "Normal", False),
    ]
    for test, result, ref, status, abnormal in labs:
        text(p2, 50, y, test, size=9)
        text(p2, 220, y, result, size=9, color=(0.7, 0.1, 0.1) if abnormal else (0.1, 0.5, 0.1))
        text(p2, 300, y, ref, size=8, color=(0.4, 0.4, 0.4))
        text(p2, 420, y, status, size=9, bold=abnormal, color=(0.7, 0.1, 0.1) if abnormal and status in ("HIGH", "LOW") else (0.2, 0.5, 0.2))
        hline(p2, 50, 545, y + 9, width=0.2)
        y += 16
    page_footer(p2, 2, TOTAL_PAGES)

    # ── Page 3: Vitals, Services Requested, Clinical Notes, Signature ───────
    p3 = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_header(p3, "PATIENT REFERRAL — FAKE PATIENT  MRN-2024-004821", "Cardiology")
    y = section(p3, 75, "SECTION 8 — RECENT VITALS (March 10, 2024 — Clinic Visit)")
    vitals = [
        ("Blood Pressure",       "162 / 98 mmHg",   "Elevated — Stage 2 Hypertension"),
        ("Heart Rate",           "84 bpm",           "Regular rhythm"),
        ("Respiratory Rate",     "18 breaths/min",   "Normal"),
        ("Temperature",          "37.1 °C (98.8 °F)","Afebrile"),
        ("SpO2",                 "96% (room air)",   "Slightly reduced"),
        ("Weight",               "97.2 kg (214 lb)", "BMI 31.4 — Obese Class I"),
        ("Height",               "175 cm (5'9\")",   ""),
    ]
    for label, val, note in vitals:
        text(p3, 50, y, label + ":", size=9, bold=True)
        text(p3, 175, y, val, size=9)
        text(p3, 310, y, note, size=9, color=(0.4, 0.4, 0.4))
        y += 14
    hline(p3, 50, 545, y)

    y = section(p3, y + 12, "SECTION 9 — SERVICES REQUESTED")
    text(p3, 50, y, "Service", size=9, bold=True)
    text(p3, 240, y, "Priority", size=9, bold=True)
    text(p3, 320, y, "Clinical Notes", size=9, bold=True)
    hline(p3, 50, 545, y + 8, width=0.8)
    y += 18
    services = [
        ("Cardiology Consultation",                "URGENT",  "Full CV risk stratification; eval for ACS"),
        ("Coronary Angiography / Cath",            "URGENT",  "Rule out obstructive CAD — ST changes + Trop elevation"),
        ("Stress Myocardial Perfusion Imaging",    "Urgent",  "If cath deferred; SPECT or PET preferred"),
        ("Repeat Echocardiogram",                  "Routine", "Reassess EF and wall motion; compare Feb 2024"),
        ("Cardiac Rehabilitation Assessment",      "Routine", "If PCI/CABG performed or CAD confirmed"),
        ("Diabetes / Endocrinology Co-management", "Routine", "HbA1c 8.2% — optimize glycemic control pre-procedure"),
    ]
    for svc, priority, notes in services:
        color = (0.8, 0.1, 0.1) if priority == "URGENT" else ((0.7, 0.4, 0.0) if priority == "Urgent" else (0, 0, 0))
        text(p3, 50, y, svc, size=9)
        text(p3, 240, y, priority, size=9, bold=True, color=color)
        text(p3, 320, y, notes, size=8, color=(0.3, 0.3, 0.3))
        hline(p3, 50, 545, y + 10, width=0.25)
        y += 20
    hline(p3, 50, 545, y, width=0.5)

    y = section(p3, y + 12, "SECTION 10 — ADDITIONAL CLINICAL NOTES")
    notes_lines = [
        "Imaging Summary:",
        "  • Chest X-ray (Mar 10, 2024): Mild cardiomegaly; no acute pulmonary edema; no effusion.",
        "  • Resting 12-lead ECG (Mar 10, 2024): Normal sinus rhythm at 84 bpm; ST-depression",
        "    0.5–1.0 mm in V4–V6; no acute STEMI pattern; QTc 448 ms.",
        "",
        "Clinical Assessment & Plan:",
        "  • High-probability unstable angina versus NSTEMI (TIMI risk score 4 — intermediate).",
        "  • Patient counseled on symptoms of acute MI and instructed to call 911 for chest pain",
        "    lasting > 5 minutes or unresponsive to 2 SL nitroglycerin doses.",
        "  • Dual antiplatelet therapy (DAPT) deferred pending cardiology evaluation.",
        "  • Statin intensification: Atorvastatin 80 mg already in place; addition of ezetimibe",
        "    10 mg PO daily initiated March 10 pending specialist input.",
        "  • BP management: Lisinopril dose increased to 40 mg; amlodipine continued at 10 mg.",
        "",
        "Flags / Concerns:",
        "  • Authorization No. for referral not yet received — INSURANCE AUTHORIZATION PENDING.",
        "  • Patient expresses financial concerns regarding procedure costs; social work referral placed.",
        "  • No known contrast allergy but no prior contrast exposure; pre-procedure allergy protocol",
        "    recommended given sulfonamide allergy history.",
    ]
    for line in notes_lines:
        indent = 60 if line.startswith("  ") else 50
        bold = line.endswith(":") and not line.startswith("  ")
        text(p3, indent, y, line.strip(), size=9, bold=bold, color=(0.2, 0.2, 0.2))
        y += 13

    # Signature block
    hline(p3, 50, 545, y + 4, width=1.0)
    y += 18
    text(p3, 50, y, "Referring Physician Signature:", size=9, bold=True)
    text(p3, 50, y + 20, "Dr. FAKE DOCTOR, MD", size=11, bold=True)
    text(p3, 50, y + 34, "FAKE PRIMARY CARE ASSOCIATES", size=9, color=(0.4, 0.4, 0.4))
    text(p3, 50, y + 48, "Date: March 10, 2024", size=9)

    text(p3, 320, y, "Received by Specialist Office:", size=9, bold=True)
    text(p3, 320, y + 20, "Signature: ___________________________", size=9)
    text(p3, 320, y + 34, "Date: _______________", size=9)
    text(p3, 320, y + 48, "Appt Scheduled: _______________", size=9)
    page_footer(p3, 3, TOTAL_PAGES)

    out = OUT_DIR / "sample_referral.pdf"
    doc.save(str(out))
    print(f"Referral saved to: {out}  ({TOTAL_PAGES} pages)")
    print("Intentional flags for testing:")
    print("  - Authorization No. missing (insurance pending)")
    print("  - Appointment window 14 days (urgent)")
    print("  - Multiple abnormal labs: HbA1c 8.2%, Troponin elevated, LDL uncontrolled")
    print("  - Two URGENT priority services requested")


if __name__ == "__main__":
    make_contract()
    make_referral()
