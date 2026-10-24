#!/usr/bin/python3

from fpdf import FPDF
import json
import os
from datetime import datetime, date
from weather import weather_report

TITLE_H = 8      # title bar height
PAD = 2          # padding inside the box
LINE_H = 6       # height of each text line
ICON_DIR = "weather_images"      # folder holding sunny.png, rain.png, etc.
ICON_SIZE = 10          # icon width/height in mm
ROW_H = 7               # height of the hour and temp rows

with open("weather_codes.json") as f:
    WEATHER_CODES = json.load(f)

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

def hourly_box_height():
    return TITLE_H + PAD + ROW_H + ICON_SIZE + 2 + ROW_H + PAD

def draw_hourly_box(pdf, x, y, w, title, hours):
    """hours is a list of (time_str, temp, code) tuples."""
    h = hourly_box_height()
    pdf.rect(x, y, w, h)

    # Title bar
    pdf.set_xy(x, y)
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(w=w, h=TITLE_H, text=title, border=1, align="C", fill=True)

    col_w = (w - 2 * PAD) / len(hours)
    row1_y = y + TITLE_H + PAD            # hour
    row2_y = row1_y + ROW_H               # icon
    row3_y = row2_y + ICON_SIZE + 2       # temp

    for i, (time_str, temp, code) in enumerate(hours):
        col_x = x + PAD + i * col_w

        # Row 1: hour label, e.g. "2 PM"
        hour_label = datetime.fromisoformat(time_str).strftime("%I %p").lstrip("0")
        pdf.set_font("Helvetica", style="B", size=9)
        pdf.set_xy(col_x, row1_y)
        pdf.cell(w=col_w, h=ROW_H, text=hour_label, align="C")

        # Row 2: icon (falls back to text if the image is missing)
        info = WEATHER_CODES.get(str(code), {})
        icon_path = os.path.join(ICON_DIR, info.get("image", ""))
        if info and os.path.isfile(icon_path):
            pdf.image(icon_path,
                      x=col_x + (col_w - ICON_SIZE) / 2,
                      y=row2_y, w=ICON_SIZE, h=ICON_SIZE)
        else:
            pdf.set_font("Helvetica", size=7)
            pdf.set_xy(col_x, row2_y)
            pdf.cell(w=col_w, h=ICON_SIZE, text=f"Code {code}", align="C")

        # Row 3: temperature
        pdf.set_font("Helvetica", size=10)
        pdf.set_xy(col_x, row3_y)
        pdf.cell(w=col_w, h=ROW_H, text=f"{temp:.0f}°", align="C")


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

    forecast = weather_report()

    schedule = [
        "9:00 AM   Class",
        "12:00 PM  Lunch",
        "12:30 PM  Back to the Grind",
        "3:00 PM   Study group",
        "6:00 PM   Project work",
    ]

    margin = pdf.l_margin
    full_w = pdf.w - pdf.l_margin - pdf.r_margin

    # Weather box (full width)
    top = pdf.get_y()
    if forecast:
        draw_hourly_box(pdf, margin, top, full_w, "Weather", forecast[8:20])
        weather_h = hourly_box_height()
    else:
        unavailable = ["Weather forecast unavailable"]
        weather_h = measure_box(pdf, full_w, unavailable)
        draw_box(pdf, margin, top, full_w, weather_h, "Weather", unavailable)

    # Schedule box below it
    top += weather_h + 5
    sched_h = measure_box(pdf, full_w, schedule)
    draw_box(pdf, margin, top, full_w, sched_h, "Schedule", schedule)

    pdf.set_y(top + sched_h)
    divider(pdf)

    pdf.output("simple_document.pdf")

generate_newsletter()
print("Saved simple_document.pdf")