#!/usr/bin/python3

from fpdf import FPDF
from datetime import date

TITLE_H = 8      # title bar height
PAD = 2          # padding inside the box
LINE_H = 6       # height of each text line

def measure_box(pdf, w, lines):
    """Return the total height this box needs for its content."""
    pdf.set_font("Helvetica", size=10)
    body_h = pdf.multi_cell(w=w - 2 * PAD, h=LINE_H, text="\n".join(lines),
                            dry_run=True, output="HEIGHT")
    return TITLE_H + PAD + body_h + PAD

def draw_box(pdf, x, y, w, h, title, lines):
    pdf.rect(x, y, w, h)

    pdf.set_xy(x, y)
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(w=w, h=TITLE_H, text=title, border=1, align="C", fill=True)

    pdf.set_xy(x + PAD, y + TITLE_H + PAD)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(w=w - 2 * PAD, h=LINE_H, text="\n".join(lines))

def divider(pdf, space=3):
    pdf.ln(space)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(space)

def generate_newsletter():
    pdf = FPDF()
    pdf.add_page()

    # Date
    pdf.set_font("Helvetica", size=10)
    pdf.cell(w=0, h=6, text=date.today().strftime("%A, %B %d, %Y"),
            new_x="LMARGIN", new_y="NEXT", align="R")

    # Masthead
    pdf.set_font("Helvetica", style="B", size=24)
    pdf.cell(w=0, h=15, text="The Aldous Herald", new_x="LMARGIN", new_y="NEXT", align="C")

    divider(pdf)

    # Intro text
    pdf.set_font("Helvetica", size=12)
    pdf.cell(w=0, h=10, text="This PDF file was created quickly using the fpdf2 library.",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

     # Box content
    weather = [
        "Today: Sunny",
        "High: 75 F",
        "Low: 52 F",
        "Wind: 5 mph",
    ]
    schedule = [
        "9:00 AM   Class",
        "12:00 PM  Lunch",
        "12:30 PM  Back to the Grind",
        "3:00 PM   Study group",
        "6:00 PM   Project work",
    ]

    top = pdf.get_y()
    margin = pdf.l_margin

    # Measure both boxes, then use the taller height for each
    h = max(measure_box(pdf, 120, weather), measure_box(pdf, 60, schedule))

    draw_box(pdf, margin, top, 120, h, "Weather", weather)
    draw_box(pdf, margin + 125, top, 60, h, "Schedule", schedule)

    # Move the cursor below the boxes before drawing the divider
    pdf.set_y(top + h)
    divider(pdf)

    pdf.output("simple_document.pdf")

generate_newsletter()
print("Saved simple_document.pdf")