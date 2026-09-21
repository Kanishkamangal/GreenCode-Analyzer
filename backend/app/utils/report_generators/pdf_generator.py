from __future__ import annotations

from io import BytesIO
from datetime import datetime
from typing import Optional, Sequence, Any
from html import escape
import math
import os
import re

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

from app.schemas.report import ReportDTO


# =============================================================================
# GreenCode Analyzer — reference-matched premium PDF
# =============================================================================
# The page is intentionally drawn with absolute coordinates. This is deliberate:
# the supplied reference has a fixed one-page composition and the report should
# preserve its spacing/size instead of allowing Platypus flow to re-layout it.
#
# Data is always read from ReportDTO / stored Analysis results. No benchmark is
# executed while generating a PDF.
# =============================================================================

PAGE_W, PAGE_H = A4

# Reference palette
WHITE = HexColor("#FFFFFF")
NAVY = HexColor("#102A43")
DARK = HexColor("#123B32")
GREEN = HexColor("#087A42")
GREEN_DARK = HexColor("#0B5A3B")
GREEN_TEXT = HexColor("#176B45")
GREEN_SOFT = HexColor("#EAF7EE")
GREEN_CARD = HexColor("#E8F6EC")
GREEN_BORDER = HexColor("#CFE7D7")
GREEN_WASH = HexColor("#F4FBF6")
MINT = HexColor("#E3F3E8")
BLUE = HexColor("#79A9DE")
BLUE_SOFT = HexColor("#EAF2FF")
ORANGE = HexColor("#F4A44E")
YELLOW_SOFT = HexColor("#FFF6DE")
YELLOW = HexColor("#F3B92E")
TEXT = HexColor("#253B4D")
MUTED = HexColor("#627D98")
GRID = HexColor("#DDE8E2")
BORDER = HexColor("#D7E4DD")
CODE_BG = HexColor("#111D2B")
CODE_GUTTER = HexColor("#1A293A")
CODE_TEXT = HexColor("#E8EEF5")
CODE_COMMENT = HexColor("#7E93A8")
CODE_KEYWORD = HexColor("#F4D06F")
CODE_STRING = HexColor("#A7D7FF")
CODE_FUNCTION = HexColor("#7DE0AE")
CODE_NUMBER = HexColor("#F5B7D1")

_configured_asset_dir = os.getenv("GREENCODE_REPORT_ASSET_DIR")
if _configured_asset_dir:
    ASSET_DIR = os.path.abspath(_configured_asset_dir)
else:
    _production_assets = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "assets", "reports")
    )
    _local_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "reports"))
    _flat_assets = os.path.dirname(__file__)
    ASSET_DIR = next(
        (p for p in (_production_assets, _local_assets, _flat_assets) if os.path.isdir(p)),
        _production_assets,
    )


# -----------------------------------------------------------------------------
# Data helpers
# -----------------------------------------------------------------------------

def _num(value: Any, decimals: int = 2, unavailable: str = "Not available") -> str:
    if value is None or value == "":
        return unavailable
    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def _value(value: Any, unavailable: str = "Not available") -> str:
    return unavailable if value is None or value == "" else str(value)


def _metric(report: ReportDTO, name: str):
    return getattr(report.metrics, name, None)


def _language(report: ReportDTO) -> str:
    return _value(report.metadata.language)


def _best(reports: Sequence[ReportDTO], metric: str, lower: bool = True) -> Optional[ReportDTO]:
    rows = [r for r in reports if _metric(r, metric) is not None]
    if not rows:
        return None
    return min(rows, key=lambda r: float(_metric(r, metric))) if lower else max(
        rows, key=lambda r: float(_metric(r, metric))
    )


def _metadata(report: ReportDTO) -> dict:
    """Read optional benchmark metadata without assuming one exact DTO shape."""
    raw = getattr(getattr(report, "metadata", None), "benchmark_metadata", None)
    if isinstance(raw, dict):
        return raw
    raw = getattr(report, "benchmark_metadata", None)
    return raw if isinstance(raw, dict) else {}


def _metadata_value(report: ReportDTO, *keys: str, default=None):
    data = _metadata(report)
    for key in keys:
        value = data.get(key)
        if value not in (None, ""):
            return value
    return default


def _iterations(report: ReportDTO) -> str:
    return _value(_metadata_value(
        report, "iterations", "iteration_count", "runs", "repeat_count", default=None
    ))


def _generated_by(report: ReportDTO, explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    return _value(_metadata_value(
        report, "generated_by", "user_name", "username", default=None
    ), "GreenCode Analyzer")


def _execution_dt(report: ReportDTO) -> str:
    dt = getattr(report.metadata, "execution_date", None)
    if not dt:
        return "Not available"
    return dt.strftime("%d %B %Y, %I:%M %p")


def _category(report: ReportDTO) -> str:
    return _value(getattr(report.metadata, "category", None))


def _task(report: ReportDTO) -> str:
    return _value(getattr(report.metadata, "benchmark_task", None), "Benchmark")


# -----------------------------------------------------------------------------
# Canvas primitives
# -----------------------------------------------------------------------------

def _round_rect(c, x, y, w, h, fill=WHITE, stroke=BORDER, radius=5, line=0.55):
    c.setLineWidth(line)
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def _text(c, x, y, text, size=8, color=TEXT, font="Helvetica", align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, str(text))
    elif align == "right":
        c.drawRightString(x, y, str(text))
    else:
        c.drawString(x, y, str(text))


def _wrap_lines(text: str, max_width: float, font="Helvetica", size=8) -> list[str]:
    words = str(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _paragraph(c, x, y_top, text, max_width, size=8, leading=10.5,
               color=TEXT, font="Helvetica", max_lines=None):
    lines = _wrap_lines(text, max_width, font, size)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while stringWidth(last + "…", font, size) > max_width and last:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    for i, line in enumerate(lines):
        _text(c, x, y_top - i * leading, line, size, color, font)
    return len(lines) * leading


def _image(c, path, x, y, w, h, preserve=True):
    if not path or not os.path.exists(path):
        return False
    try:
        c.drawImage(path, x, y, width=w, height=h, preserveAspectRatio=preserve,
                    anchor="sw", mask="auto")
        return True
    except Exception:
        return False


# -----------------------------------------------------------------------------
# Vector icons matching the reference language
# -----------------------------------------------------------------------------

def _icon(c, kind, cx, cy, size=16, color=GREEN_TEXT, circle_fill=None):
    if circle_fill is not None:
        c.setFillColor(circle_fill)
        c.setStrokeColor(circle_fill)
        c.circle(cx, cy, size * 0.62, fill=1, stroke=0)

    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(max(0.8, size * 0.075))

    if kind == "doc":
        c.roundRect(cx-size*.22, cy-size*.32, size*.44, size*.64, 1.2, fill=0, stroke=1)
        c.line(cx, cy+size*.32, cx+size*.22, cy+size*.10)
        c.line(cx-size*.12, cy+size*.02, cx+size*.12, cy+size*.02)
        c.line(cx-size*.12, cy-size*.12, cx+size*.12, cy-size*.12)
    elif kind == "calendar":
        c.roundRect(cx-size*.34, cy-size*.29, size*.68, size*.58, 1.3, fill=0, stroke=1)
        c.line(cx-size*.34, cy+size*.08, cx+size*.34, cy+size*.08)
        c.line(cx-size*.18, cy+size*.40, cx-size*.18, cy+size*.20)
        c.line(cx+size*.18, cy+size*.40, cx+size*.18, cy+size*.20)
    elif kind == "person":
        c.circle(cx, cy+size*.20, size*.16, fill=0, stroke=1)
        p = c.beginPath()
        p.moveTo(cx-size*.32, cy-size*.33)
        p.curveTo(cx-size*.28, cy-size*.03, cx+size*.28, cy-size*.03, cx+size*.32, cy-size*.33)
        c.drawPath(p, fill=0, stroke=1)
    elif kind == "gear":
        c.circle(cx, cy, size*.25, fill=0, stroke=1)
        for a in range(0, 360, 45):
            r1=size*.34; r2=size*.48
            a1=math.radians(a)
            c.line(cx+math.cos(a1)*r1, cy+math.sin(a1)*r1,
                   cx+math.cos(a1)*r2, cy+math.sin(a1)*r2)
    elif kind == "bolt":
        p=c.beginPath()
        p.moveTo(cx+size*.08, cy+size*.47)
        p.lineTo(cx-size*.28, cy+size*.02)
        p.lineTo(cx-size*.03, cy+size*.02)
        p.lineTo(cx-size*.10, cy-size*.48)
        p.lineTo(cx+size*.32, cy-size*.02)
        p.lineTo(cx+size*.04, cy-size*.02)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    elif kind == "leaf":
        p=c.beginPath()
        p.moveTo(cx-size*.38, cy-size*.02)
        p.curveTo(cx-size*.18, cy+size*.47, cx+size*.34, cy+size*.45, cx+size*.38, cy+size*.05)
        p.curveTo(cx+size*.17, cy-size*.32, cx-size*.15, cy-size*.31, cx-size*.38, cy-size*.02)
        c.drawPath(p, fill=1, stroke=0)
        c.setStrokeColor(WHITE)
        c.line(cx-size*.26, cy-size*.13, cx+size*.25, cy+size*.29)
    elif kind == "database":
        c.ellipse(cx-size*.33, cy+size*.20, cx+size*.33, cy+size*.43, fill=0, stroke=1)
        c.rect(cx-size*.33, cy-size*.25, size*.66, size*.56, fill=0, stroke=1)
        c.ellipse(cx-size*.33, cy-size*.36, cx+size*.33, cy-size*.13, fill=0, stroke=1)
    elif kind == "star":
        pts=[]
        for i in range(10):
            a=math.radians(-90+i*36)
            r=size*.47 if i%2==0 else size*.21
            pts += [cx+math.cos(a)*r, cy+math.sin(a)*r]
        c.setFillColor(color)
        c.setStrokeColor(color)
        p=c.beginPath(); p.moveTo(pts[0],pts[1])
        for i in range(2,len(pts),2): p.lineTo(pts[i],pts[i+1])
        p.close(); c.drawPath(p, fill=1, stroke=0)
    elif kind == "chart":
        c.line(cx-size*.40,cy-size*.40,cx-size*.40,cy+size*.40)
        c.line(cx-size*.40,cy-size*.40,cx+size*.45,cy-size*.40)
        for i,h in enumerate((.25,.43,.65)):
            c.rect(cx-size*.25+i*size*.25, cy-size*.38, size*.13, size*h, fill=1, stroke=0)
    elif kind == "summary":
        c.roundRect(cx-size*.34, cy-size*.44, size*.68, size*.88, 2, fill=1, stroke=0)
        c.setStrokeColor(WHITE); c.setLineWidth(.8)
        for yy in (.18,0,-.18):
            c.line(cx-size*.18, cy+size*yy, cx+size*.18, cy+size*yy)
    elif kind == "code":
        c.line(cx-size*.40,cy,cx-size*.08,cy+size*.28)
        c.line(cx-size*.08,cy+size*.28,cx-size*.40,cy-size*.28)
        c.line(cx+size*.40,cy,cx+size*.08,cy+size*.28)
        c.line(cx+size*.08,cy+size*.28,cx+size*.40,cy-size*.28)
    elif kind == "bulb":
        c.circle(cx, cy+size*.10, size*.24, fill=0, stroke=1)
        c.line(cx-size*.12,cy-size*.20,cx+size*.12,cy-size*.20)
        c.line(cx-size*.13,cy-size*.34,cx+size*.13,cy-size*.34)
    elif kind == "quote":
        _text(c,cx,cy-size*.12,"“",size*1.9,GREEN_TEXT,"Helvetica-Bold","center")


# -----------------------------------------------------------------------------
# Decorative background and footer
# -----------------------------------------------------------------------------

def _draw_leaf(c, x, y, scale=1.0, fill="#DCEFE2", stroke="#A8D2B2"):
    c.saveState()
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke)); c.setLineWidth(.45)
    p=c.beginPath()
    p.moveTo(x,y)
    p.curveTo(x+9*scale,y+24*scale,x+27*scale,y+30*scale,x+33*scale,y+41*scale)
    p.curveTo(x+16*scale,y+40*scale,x+3*scale,y+24*scale,x,y)
    c.drawPath(p,fill=1,stroke=0)
    c.line(x+3*scale,y+3*scale,x+29*scale,y+35*scale)
    c.restoreState()


def _background(c):
    c.setFillColor(WHITE); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)

    # Top-right soft botanical wash.
    c.setFillColor(HexColor("#F0FAF3"))
    c.circle(PAGE_W-20*mm,PAGE_H-18*mm,39*mm,fill=1,stroke=0)
    _draw_leaf(c,PAGE_W-56*mm,PAGE_H-47*mm,1.25)
    _draw_leaf(c,PAGE_W-41*mm,PAGE_H-33*mm,.82)
    _draw_leaf(c,PAGE_W-73*mm,PAGE_H-55*mm,.88)

    # Bottom wave.
    c.setFillColor(HexColor("#E6F5EA"))
    p=c.beginPath(); p.moveTo(0,0)
    p.curveTo(38*mm,14*mm,72*mm,-2*mm,112*mm,6*mm)
    p.curveTo(148*mm,14*mm,178*mm,-2*mm,PAGE_W,9*mm)
    p.lineTo(PAGE_W,0); p.close(); c.drawPath(p,fill=1,stroke=0)
    c.setFillColor(HexColor("#D4EEDD"))
    p=c.beginPath(); p.moveTo(0,0)
    p.curveTo(42*mm,8*mm,77*mm,1*mm,115*mm,4*mm)
    p.curveTo(154*mm,7*mm,185*mm,2*mm,PAGE_W,6*mm)
    p.lineTo(PAGE_W,0); p.close(); c.drawPath(p,fill=1,stroke=0)


def _footer(c, generated_date: Optional[datetime] = None):
    logo = os.path.join(ASSET_DIR,"greencode_logo.png")
    if not _image(c,logo,14*mm,4.5*mm,39*mm,12.7*mm):
        _text(c,14*mm,10*mm,"GreenCode",8.8,GREEN_DARK,"Helvetica-Bold")
        _text(c,14*mm,6.5*mm,"A N A L Y Z E R",4.2,MUTED,"Helvetica")

    c.setStrokeColor(HexColor("#9FC8AC")); c.setLineWidth(.7)
    c.line(73*mm,8.2*mm,91*mm,8.2*mm)
    c.line(127*mm,8.2*mm,145*mm,8.2*mm)
    _text(c,PAGE_W/2,6.2*mm,"Small optimizations. A bigger tomorrow.",7.2,GREEN_TEXT,"Helvetica-Oblique","center")
    _text(c,PAGE_W-14*mm,9.2*mm,"Page 1 of 1",6.8,GREEN_DARK,"Helvetica-Bold","right")
    dt=generated_date or datetime.now()
    _text(c,PAGE_W-14*mm,5.6*mm,f"Generated on {dt.strftime('%d %B %Y')}",5.1,MUTED,"Helvetica","right")


# -----------------------------------------------------------------------------
# Header / hero
# -----------------------------------------------------------------------------

def _header(c, report: ReportDTO, generated_by: Optional[str], comparison: bool):
    logo = os.path.join(ASSET_DIR,"greencode_logo.png")
    brand = os.path.join(ASSET_DIR,"brand_right.png")
    _image(c,logo,14*mm,PAGE_H-27*mm,53*mm,17.4*mm)
    _image(c,brand,PAGE_W-72*mm,PAGE_H-27*mm,72*mm,21.5*mm)

    left_x=8*mm
    top=PAGE_H-30*mm
    _text(c,left_x,top,"BENCHMARK REPORT",7.3,GREEN_TEXT,"Helvetica-Bold")

    title=f"{_task(report)} — Performance Analysis"
    title_size=20.2
    if stringWidth(title,"Helvetica-Bold",title_size) > 120*mm:
        title_size=18.5
    _text(c,left_x,top-10.0*mm,title,title_size,NAVY,"Helvetica-Bold")

    if comparison:
        desc=(f"A comparative analysis of {_task(report)} implemented in different programming languages, "
              "evaluating execution performance and energy efficiency.")
    else:
        desc=(f"A performance and sustainability analysis of {_task(report)} implemented in {_language(report)}.")
    _paragraph(c,left_x,top-17.0*mm,desc,124*mm,8.1,10.8,TEXT,"Helvetica",max_lines=3)

    # Metadata card exactly in the upper-right hero area.
    x=PAGE_W-65*mm; y=PAGE_H-63*mm; w=59*mm; h=39*mm
    _round_rect(c,x,y,w,h,WHITE,GREEN_BORDER,4.2,.55)
    rows=[
        ("calendar","Report Generated",_execution_dt(report)),
        ("person","Generated By",_generated_by(report,generated_by)),
    ]
    yy=y+h-10*mm
    for kind,label,val in rows:
        _icon(c,kind,x+7*mm,yy+1*mm,14,GREEN_DARK)
        _text(c,x+14*mm,yy+3*mm,label,6.3,MUTED,"Helvetica")
        _text(c,x+14*mm,yy-1.1*mm,val,7.2,NAVY,"Helvetica-Bold")
        yy-=13*mm
    _icon(c,"gear",x+7*mm,yy+1*mm,14,GREEN_DARK)
    _text(c,x+14*mm,yy+3*mm,"Benchmark Configuration",6.3,MUTED,"Helvetica")
    _text(c,x+14*mm,yy-1.0*mm,
          f"Input Size: {_value(report.metadata.input_size)}  |  Iterations: {_iterations(report)}",
          6.8,NAVY,"Helvetica-Bold")
    _text(c,x+14*mm,yy-5.0*mm,f"Benchmark Type: {_category(report)}",6.8,NAVY,"Helvetica-Bold")


# -----------------------------------------------------------------------------
# Executive summary
# -----------------------------------------------------------------------------

def _summary_text(reports: Sequence[ReportDTO]) -> str:
    task=_task(reports[0])
    if len(reports) == 1:
        return (f"This report presents the measured performance, resource utilization, and energy "
                f"consumption of {task} implemented in {_language(reports[0])}. The results provide a "
                "concise view of execution speed, memory usage, and sustainability metrics for the run.")

    fastest=_best(reports,"execution_time",True)
    energy=_best(reports,"energy_consumption",True)
    memory=_best(reports,"memory_usage",True)
    if fastest and energy:
        lead=(f"This report compares the performance, resource utilization, and energy consumption of "
              f"{task} implemented in multiple programming languages. {_language(fastest)} recorded the "
              f"lowest measured execution time, while {_language(energy)} recorded the lowest measured energy consumption.")
    elif fastest:
        lead=(f"This report compares the performance, resource utilization, and energy consumption of "
              f"{task} implemented in multiple programming languages. {_language(fastest)} recorded the "
              f"lowest measured execution time.")
    else:
        lead=(f"This report compares measured performance and resource utilization for {task} across "
              "multiple programming language implementations.")
    tail=" The results highlight the trade-offs between execution speed, memory usage, and energy efficiency across languages."
    return lead + tail


def _executive_summary(c, reports: Sequence[ReportDTO], y_top: float) -> float:
    x=6*mm; w=PAGE_W-12*mm; h=29*mm; y=y_top-h
    _round_rect(c,x,y,w,h,GREEN_SOFT,GREEN_BORDER,5,.55)
    _icon(c,"summary",11*mm,y+h-9*mm,17,WHITE,GREEN)
    _text(c,18*mm,y+h-10*mm,"Executive Summary",11.4,DARK,"Helvetica-Bold")

    # Quote area is a pale circular-ish card on the right.
    qx=x+w-45*mm; qy=y+3.5*mm; qw=41*mm; qh=h-7*mm
    _round_rect(c,qx,qy,qw,qh,HexColor("#DDF1E4"),HexColor("#DDF1E4"),14,.1)
    _text(c,qx+8*mm,qy+qh-10*mm,"“",22,GREEN_TEXT,"Helvetica-Bold")
    _text(c,qx+qw/2,qy+qh-17*mm,"Efficient code",7.9,GREEN_DARK,"Helvetica-Oblique","center")
    _text(c,qx+qw/2,qy+qh-22*mm,"today, a greener",7.9,GREEN_DARK,"Helvetica-Oblique","center")
    _text(c,qx+qw/2,qy+qh-27*mm,"tomorrow.",7.9,GREEN_DARK,"Helvetica-Oblique","center")

    _paragraph(c,18*mm,y+h-16*mm,_summary_text(reports),w-58*mm,7.35,9.8,TEXT,"Helvetica",max_lines=5)
    # Decorative leaf in quote corner.
    _draw_leaf(c,qx+qw-11*mm,qy+4*mm,.34,"#BDE1C8","#8EC29C")
    return y


# -----------------------------------------------------------------------------
# KPI cards
# -----------------------------------------------------------------------------

def _kpi_card(c,x,y,w,h,label,kind,result,metric,unit,bg,icon_bg,icon_color,lower=True):
    _round_rect(c,x,y,w,h,bg,GREEN_BORDER,4.5,.5)
    _icon(c,kind,x+9*mm,y+h/2,22,icon_color,icon_bg)
    _text(c,x+18*mm,y+h-7.2*mm,label,6.0,GREEN_TEXT if bg!=BLUE_SOFT else HexColor("#315E93"),"Helvetica")
    lang=_language(result) if result else "Not available"
    _text(c,x+18*mm,y+h-13.8*mm,lang,12.2,NAVY,"Helvetica-Bold")
    val=_num(_metric(result,metric),2) if result else "Not available"
    _text(c,x+18*mm,y+3.8*mm,f"{val} {unit}",8.4,GREEN_TEXT,"Helvetica-Bold")


def _kpis(c,reports: Sequence[ReportDTO], y_top: float) -> float:
    x=6*mm; w=PAGE_W-12*mm; h=37*mm; y=y_top-h
    _round_rect(c,x,y,w,h,WHITE,BORDER,5,.55)
    _icon(c,"chart",11*mm,y+h-10*mm,18,GREEN_TEXT)
    _text(c,18*mm,y+h-10.5*mm,"Key Metrics",11.5,DARK,"Helvetica-Bold")
    _text(c,52*mm,y+h-10.5*mm,"(Best Performing Language)",8.2,GREEN_TEXT,"Helvetica-Bold")

    cards_y=y+4.2*mm; card_h=21*mm; gap=4.5*mm; inner_x=x+6*mm
    card_w=(w-12*mm-3*gap)/4
    specs=[
        ("Fastest Execution","bolt","execution_time","ms",GREEN_WASH,GREEN_CARD,GREEN_TEXT,True),
        ("Lowest Energy Usage","leaf","energy_consumption","J",GREEN_WASH,GREEN_CARD,GREEN_TEXT,True),
        ("Lowest Memory Usage","database","memory_usage","MB",BLUE_SOFT,HexColor("#DCEAFF"),HexColor("#2D6FB8"),True),
        ("Highest Green Score","star","green_score","/ 100",YELLOW_SOFT,HexColor("#FFF0C8"),HexColor("#B47A05"),False),
    ]
    for i,(label,kind,metric,unit,bg,ibg,ic,lower) in enumerate(specs):
        r=_best(reports,metric,lower)
        _kpi_card(c,inner_x+i*(card_w+gap),cards_y,card_w,card_h,label,kind,r,metric,unit,bg,ibg,ic,lower)
    return y


# -----------------------------------------------------------------------------
# Charts
# -----------------------------------------------------------------------------

def _nice_max(v: float) -> float:
    if v <= 0: return 1.0
    raw=v*1.12
    mag=10**math.floor(math.log10(raw))
    for step in (1,2,2.5,5,10):
        candidate=step*mag
        if candidate>=raw:
            return candidate
    return 10*mag


def _chart_panel(c,x,y,w,h,title,metric,ylabel,reports):
    _round_rect(c,x,y,w,h,WHITE,BORDER,5,.55)
    kind="leaf" if metric=="energy_consumption" else "clock"
    _icon(c,kind,x+10*mm,y+h-10*mm,17,GREEN_TEXT)
    _text(c,x+18*mm,y+h-10.4*mm,title,10.1,DARK,"Helvetica-Bold")

    vals=[]; labels=[]
    for r in reports:
        v=_metric(r,metric)
        if v is not None:
            vals.append(float(v)); labels.append(_language(r))
    if not vals:
        _text(c,x+w/2,y+h/2,"No measured data available",7.5,MUTED,"Helvetica","center")
        return

    px=x+14*mm; py=y+8*mm; pw=w-20*mm; ph=h-21*mm
    ymax=_nice_max(max(vals))
    grid_count=5
    c.setLineWidth(.35)
    for i in range(grid_count+1):
        yy=py+(ph*i/grid_count)
        c.setStrokeColor(HexColor("#E1EAE5")); c.line(px,yy,px+pw,yy)
        val=ymax*i/grid_count
        decimals=1 if ymax>=10 else 2
        _text(c,px-2.5*mm,yy-1.3*mm,_num(val,decimals),5.2,MUTED,"Helvetica","right")

    c.setStrokeColor(HexColor("#718292")); c.setLineWidth(.6)
    c.line(px,py,px,py+ph); c.line(px,py,px+pw,py)

    bar_colors=[GREEN,BLUE,ORANGE]
    slot=pw/max(len(vals),1)
    bw=min(17*mm,slot*.43)
    for i,(v,label) in enumerate(zip(vals,labels)):
        bx=px+slot*(i+.5)-bw/2
        bh=ph*(v/ymax)
        c.setFillColor(bar_colors[i%3]); c.setStrokeColor(bar_colors[i%3])
        c.roundRect(bx,py,bw,max(1,bh),1.2,fill=1,stroke=0)
        _text(c,bx+bw/2,py+bh+2.0*mm,_num(v,1 if metric=="execution_time" else 2),6.6,NAVY,"Helvetica-Bold","center")
        _text(c,bx+bw/2,py-4.3*mm,label,6.4,TEXT,"Helvetica","center")

    # Vertical axis label.
    c.saveState(); c.translate(x+4*mm,y+h/2-1*mm); c.rotate(90)
    _text(c,0,0,ylabel,5.4,MUTED,"Helvetica","center")
    c.restoreState()


def _charts(c,reports: Sequence[ReportDTO], y_top: float) -> float:
    x=8*mm; gap=4*mm; w=(PAGE_W-16*mm-gap)/2; h=55*mm; y=y_top-h
    _chart_panel(c,x,y,w,h,"Execution Time Comparison","execution_time","Execution Time (ms)",reports)
    _chart_panel(c,x+w+gap,y,w,h,"Energy Consumption Comparison","energy_consumption","Energy (Joules)",reports)
    return y


# -----------------------------------------------------------------------------
# Detailed results
# -----------------------------------------------------------------------------

def _details(c,reports: Sequence[ReportDTO], y_top: float) -> float:
    x=6*mm; w=PAGE_W-12*mm; h=43*mm; y=y_top-h
    _round_rect(c,x,y,w,h,WHITE,BORDER,5,.55)
    _icon(c,"summary",11*mm,y+h-10*mm,17,WHITE,GREEN)
    _text(c,18*mm,y+h-10.3*mm,"Detailed Results",11.2,DARK,"Helvetica-Bold")

    # Configuration pill.
    pill_w=49*mm; pill_h=8*mm; px=x+w-pill_w-5*mm; py=y+h-14*mm
    _round_rect(c,px,py,pill_w,pill_h,GREEN_WASH,GREEN_WASH,6,.1)
    _text(c,px+pill_w/2,py+2.6*mm,
          f"Input Size: {_value(reports[0].metadata.input_size)}  |  Iterations: {_iterations(reports[0])}",
          6.4,TEXT,"Helvetica","center")

    table_x=x+4*mm; table_y=y+4*mm; table_w=w-8*mm; header_h=7.7*mm; row_h=6.8*mm
    cols=[0.15,0.18,0.16,0.18,0.20,0.13]
    headers=["Language","Execution Time (ms)","CPU Usage (%)","Memory Usage (MB)","Energy Consumption (J)","Green Score"]
    cx=table_x
    for i,pct in enumerate(cols):
        cw=table_w*pct
        c.setFillColor(GREEN_SOFT); c.setStrokeColor(GREEN_BORDER); c.rect(cx,table_y+len(reports)*row_h,cw,header_h,fill=1,stroke=1)
        _text(c,cx+2.5*mm,table_y+len(reports)*row_h+3.0*mm,headers[i],6.0,NAVY,"Helvetica-Bold")
        cx+=cw

    for row_i,r in enumerate(reports):
        yy=table_y+(len(reports)-1-row_i)*row_h
        fill=HexColor("#EFFAF2") if row_i==0 else WHITE
        cx=table_x
        values=[
            _language(r),_num(_metric(r,"execution_time")),_num(_metric(r,"cpu_usage")),
            _num(_metric(r,"memory_usage")),_num(_metric(r,"energy_consumption"),2),
            _num(_metric(r,"green_score")),
        ]
        for col_i,pct in enumerate(cols):
            cw=table_w*pct
            c.setFillColor(fill); c.setStrokeColor(GREEN_BORDER); c.rect(cx,yy,cw,row_h,fill=1,stroke=1)
            _text(c,cx+2.5*mm,yy+2.45*mm,values[col_i],6.4,NAVY if col_i==0 else TEXT,
                  "Helvetica-Bold" if col_i==0 else "Helvetica")
            cx+=cw
    return y


# -----------------------------------------------------------------------------
# Code editor and insights
# -----------------------------------------------------------------------------

def _tokenize_code(line: str):
    """Conservative syntax tokenizer for the visible source excerpt."""
    pattern=r'(//.*|#.*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\b\d+(?:\.\d+)?\b|\b(?:if|else|for|while|return|int|void|class|public|private|protected|static|const|auto|new|def|import|from|return|in|True|False|None|try|except|finally|async|await|function|let|var|const)\b|\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()|.)'
    return re.findall(pattern,line)


def _token_color(tok: str):
    if tok.startswith("//") or tok.startswith("#"):
        return CODE_COMMENT
    if tok.startswith('"') or tok.startswith("'"):
        return CODE_STRING
    if re.fullmatch(r"\d+(?:\.\d+)?",tok):
        return CODE_NUMBER
    if tok in {"if","else","for","while","return","int","void","class","public","private","protected","static","const","auto","new","def","import","from","in","True","False","None","try","except","finally","async","await","function","let","var"}:
        return CODE_KEYWORD
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",tok):
        return CODE_FUNCTION if tok and tok[0].islower() and tok not in {"arr","l","r","m","i","j","n","x","y"} else CODE_TEXT
    return CODE_TEXT


def _code_panel(c,x,y,w,h,code,language):
    _round_rect(c,x,y,w,h,WHITE,BORDER,5,.55)
    _icon(c,"code",x+10*mm,y+h-10*mm,17,GREEN_TEXT)
    _text(c,x+17*mm,y+h-10.3*mm,f"Code Snippet ({_value(language)})",10.5,DARK,"Helvetica-Bold")

    pill_w=17*mm; pill_h=7*mm
    _round_rect(c,x+w-pill_w-5*mm,y+h-12*mm,pill_w,pill_h,GREEN_CARD,GREEN_CARD,5,.1)
    _text(c,x+w-pill_w/2-5*mm,y+h-9.7*mm,_value(language),6.2,GREEN_TEXT,"Helvetica-Bold","center")

    bx=x+5*mm; by=y+4*mm; bw=w-10*mm; bh=h-18*mm
    _round_rect(c,bx,by,bw,bh,CODE_BG,CODE_BG,2.5,.1)

    if not code:
        code="// Source code was not stored with this analysis."
    lines=str(code).splitlines()
    max_lines=8
    truncated=len(lines)>max_lines
    lines=lines[:max_lines]
    if truncated and lines:
        lines[-1]=lines[-1].rstrip()+"  …"

    gutter=8*mm
    c.setFillColor(CODE_GUTTER); c.rect(bx,by,gutter,bh,fill=1,stroke=0)
    start_y=by+bh-7*mm
    font="Courier"; size=5.9; leading=6.9
    for i,line in enumerate(lines,1):
        yy=start_y-(i-1)*leading
        _text(c,bx+gutter/2,yy,str(i),size,CODE_COMMENT,font,"center")
        xx=bx+gutter+3*mm
        for tok in _tokenize_code(line):
            _text(c,xx,yy,tok,size,_token_color(tok),font)
            xx += stringWidth(tok,font,size)
            if xx>bx+bw-3*mm:
                break


def _insights(c,x,y,w,h,reports):
    _round_rect(c,x,y,w,h,WHITE,BORDER,5,.55)
    _icon(c,"bulb",x+10*mm,y+h-10*mm,17,GREEN_TEXT)
    _text(c,x+17*mm,y+h-10.3*mm,"Insights",10.5,DARK,"Helvetica-Bold")

    fastest=_best(reports,"execution_time",True)
    energy=_best(reports,"energy_consumption",True)
    memory=_best(reports,"memory_usage",True)
    score=_best(reports,"green_score",False)
    items=[]
    if fastest:
        items.append(("chart",HexColor("#DDF3E4"),f"{_language(fastest)} is the fastest",
                      f"Lowest measured execution time at {_num(_metric(fastest,'execution_time'))} ms."))
    if energy:
        items.append(("leaf",HexColor("#DDF3E4"),f"{_language(energy)} uses the least energy",
                      f"Lowest measured energy consumption at {_num(_metric(energy,'energy_consumption'),2)} J."))
    if memory:
        items.append(("database",HexColor("#E5F0FF"),f"{_language(memory)} uses the least memory",
                      f"Peak measured memory usage of {_num(_metric(memory,'memory_usage'))} MB."))
    if score and not fastest and not energy and not memory:
        items.append(("star",YELLOW_SOFT,f"{_language(score)} has the highest Green Score",
                      f"Measured Green Score: {_num(_metric(score,'green_score'))}/100."))

    if not items:
        _text(c,x+7*mm,y+h/2,"Insufficient measured data to produce comparative insights.",6.6,MUTED,"Helvetica")
        return

    iy=y+h-19*mm
    for kind,bg,title,body in items[:3]:
        _icon(c,kind,x+10*mm,iy,17,GREEN_TEXT,bg)
        _text(c,x+18*mm,iy+2.2*mm,title,7.0,DARK,"Helvetica-Bold")
        _text(c,x+18*mm,iy-2.1*mm,body,6.0,TEXT,"Helvetica")
        iy-=10.2*mm


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

def generate_pdf(
    report: ReportDTO,
    comparison_reports: Optional[Sequence[ReportDTO]] = None,
    code_snippet: Optional[str] = None,
    code_language: Optional[str] = None,
    generated_by: Optional[str] = None,
) -> bytes:
    """Generate the one-page reference-style GreenCode benchmark report.

    `report` and `comparison_reports` must contain already stored analysis values.
    `code_snippet` is the actual source used for the selected analysis. It is
    never executed here.
    """
    reports=[report]
    if comparison_reports:
        reports.extend(r for r in comparison_reports if r.analysis_id != report.analysis_id)

    buf=BytesIO()
    c=canvas.Canvas(buf,pagesize=A4)
    c.setTitle(report.report_title or f"{_task(report)} — Performance Analysis")
    c.setAuthor("GreenCode Analyzer")

    _background(c)
    _header(c,report,generated_by,len(reports)>1)

    y=PAGE_H-61*mm
    y=_executive_summary(c,reports,y)-5*mm
    y=_kpis(c,reports,y)-5*mm
    y=_charts(c,reports,y)-5*mm
    y=_details(c,reports,y)-4*mm

    bottom_y=10*mm
    panel_y=bottom_y+5*mm
    panel_h=45*mm
    left_x=6*mm; gap=5*mm; panel_w=(PAGE_W-16*mm-gap)/2
    _code_panel(c,left_x,panel_y,panel_w,panel_h,code_snippet,code_language or _language(report))
    _insights(c,left_x+panel_w+gap,panel_y,panel_w,panel_h,reports)

    _footer(c,getattr(report.metadata,"execution_date",None))
    c.showPage(); c.save()
    buf.seek(0)
    return buf.getvalue()


def generate_comparison_pdf(
    reports: Sequence[ReportDTO],
    code_snippet: Optional[str] = None,
    code_language: Optional[str] = None,
    generated_by: Optional[str] = None,
) -> bytes:
    if not reports:
        raise ValueError("At least one report is required.")
    return generate_pdf(
        reports[0],
        comparison_reports=reports[1:],
        code_snippet=code_snippet,
        code_language=code_language,
        generated_by=generated_by,
    )
