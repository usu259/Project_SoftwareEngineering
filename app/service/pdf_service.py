from fpdf import FPDF
from app.domain.invoice import Invoice
from app.domain.customer import Customer
from app.domain.position import PersonnelPosition
from config import TAX_RATE


class _InvoicePDF(FPDF):
    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6, f"Page {self.page_no()}", align="C")


def generate_invoice_pdf(invoice: Invoice, customer: Customer) -> bytes:
    pdf = _InvoicePDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    PAGE_W = pdf.w - 40  # usable width (170 mm)
    BLUE = (37, 99, 235)
    DARK = (17, 24, 39)
    GRAY = (107, 114, 128)
    MID  = (55, 65, 81)
    LIGHT_BG = (249, 250, 251)
    ROW_BG   = (243, 244, 246)

    # ── Logo / INVOICE header ──────────────────────────────────────
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*BLUE)
    pdf.cell(PAGE_W / 2, 10, "Billing App", ln=False)

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*DARK)
    pdf.cell(PAGE_W / 2, 10, "INVOICE", align="R", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(PAGE_W / 2, 6, "", ln=False)
    pdf.cell(PAGE_W / 2, 6, f"# {invoice.id:04d}", align="R", ln=True)

    pdf.ln(3)
    pdf.set_draw_color(229, 231, 235)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(5)

    # ── Bill To (left) / Invoice details (right) ──────────────────
    COL_W = PAGE_W / 2 - 6
    RIGHT_X = 20 + COL_W + 12

    start_y = pdf.get_y()

    # — Left: Bill To —
    pdf.set_xy(20, start_y)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(COL_W, 5, "BILL TO", ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(COL_W, 6, customer.full_name, ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*MID)
    for line in [
        customer.email,
        customer.phone,
        customer.address.street,
        f"{customer.address.zip_code} {customer.address.city}",
        customer.address.country,
    ]:
        pdf.cell(COL_W, 5, line, ln=True)

    left_end_y = pdf.get_y()

    # — Right: Invoice details —
    ry = start_y

    def _right_row(label: str, value: str, h: int = 6) -> None:
        nonlocal ry
        pdf.set_xy(RIGHT_X, ry)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(28, h, label, ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK)
        pdf.cell(COL_W - 28, h, value, align="R", ln=False)
        ry += h

    _right_row("DATE",   str(invoice.creation_date))
    _right_row("STATUS", invoice.status.name)
    _right_row("TITLE",  invoice.title)

    pdf.set_y(max(left_end_y, ry) + 8)

    pdf.set_draw_color(229, 231, 235)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)

    # ── Items table ────────────────────────────────────────────────
    #   Description | Type | Qty/Hrs | Rate | Amount
    CW = [PAGE_W - 96, 22, 24, 26, 24]

    # Header row
    pdf.set_fill_color(*LIGHT_BG)
    pdf.set_text_color(*GRAY)
    pdf.set_font("Helvetica", "B", 8)
    headers = ["DESCRIPTION", "TYPE", "QTY / HRS", "RATE", "AMOUNT"]
    aligns  = ["L", "L", "R", "R", "R"]
    for w, h, a in zip(CW, headers, aligns):
        pdf.cell(w, 7, h, border="B", align=a, fill=True)
    pdf.ln()

    pdf.set_text_color(*MID)

    for wr in invoice.work_reports:
        # Work-report title row
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK)
        pdf.set_fill_color(*ROW_BG)
        label = f"  {wr.title}   -   {wr.execution_date}"
        pdf.cell(PAGE_W, 6, label, border="B", fill=True, ln=True)
        pdf.set_text_color(*MID)

        for pos in wr.positions:
            pdf.set_font("Helvetica", "", 9)
            desc = f"  {pos.description}" if pos.description else "  —"

            if isinstance(pos, PersonnelPosition):
                type_lbl = "Labour"
                qty  = f"{pos.hours}h"
                rate = f"{pos.hourly_rate:.2f}"
            else:
                type_lbl = "Material"
                qty  = str(pos.quantity)
                rate = f"{pos.unit_price:.2f}"

            pdf.cell(CW[0], 6, desc,            border="B", align="L")
            pdf.cell(CW[1], 6, type_lbl,        border="B", align="L")
            pdf.cell(CW[2], 6, qty,             border="B", align="R")
            pdf.cell(CW[3], 6, rate,            border="B", align="R")
            pdf.cell(CW[4], 6, f"{pos.subtotal:.2f}", border="B", align="R")
            pdf.ln()

    pdf.ln(6)

    # ── Totals ─────────────────────────────────────────────────────
    subtotal   = invoice.total_cost
    tax_amount = invoice.total_cost_with_tax - subtotal
    total      = invoice.total_cost_with_tax

    lbl_w = PAGE_W - 50
    val_w = 50

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(lbl_w, 6, "Subtotal", align="R")
    pdf.cell(val_w, 6, f"{subtotal:.2f}", align="R", ln=True)

    pdf.cell(lbl_w, 6, "Tax (8.1%)", align="R")
    pdf.cell(val_w, 6, f"{tax_amount:.2f}", align="R", ln=True)

    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(20 + lbl_w - 20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*DARK)
    pdf.cell(lbl_w, 8, "TOTAL", align="R")
    pdf.cell(val_w, 8, f"{total:.2f}", align="R", ln=True)

    # ── Notes ──────────────────────────────────────────────────────
    if invoice.notes:
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(0, 5, "NOTES", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*MID)
        pdf.multi_cell(0, 5, invoice.notes)

    return bytes(pdf.output())
