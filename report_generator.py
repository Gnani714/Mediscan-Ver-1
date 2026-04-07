"""
PDF Report Generator for MediScan AI
Generates professional medical analysis reports using ReportLab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime


# ── Color Palette ─────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor('#0A1628')
MED_BLUE    = colors.HexColor('#1565C0')
LIGHT_BLUE  = colors.HexColor('#E3F2FD')
TEAL        = colors.HexColor('#00897B')
GREEN       = colors.HexColor('#2E7D32')
GREEN_BG    = colors.HexColor('#E8F5E9')
AMBER       = colors.HexColor('#F57F17')
AMBER_BG    = colors.HexColor('#FFF8E1')
RED         = colors.HexColor('#C62828')
RED_BG      = colors.HexColor('#FFEBEE')
GREY        = colors.HexColor('#546E7A')
LIGHT_GREY  = colors.HexColor('#F5F5F5')
WHITE       = colors.white


def risk_colors(level: str):
    mapping = {
        'Normal':           (GREEN,  GREEN_BG),
        'Needs Attention':  (AMBER,  AMBER_BG),
        'Critical':         (RED,    RED_BG),
    }
    return mapping.get(level, (GREY, LIGHT_GREY))


def status_color(status: str) -> colors.Color:
    if status in ('Critical High', 'Critical Low'):
        return RED
    if status in ('High', 'Low'):
        return AMBER
    return GREEN


def generate_pdf_report(result: dict, patient_name: str, patient_age: str,
                         patient_gender: str, output_path: str, source_file: str = ''):
    """Generate a full A4 PDF medical analysis report"""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    story  = []

    # ── Custom Styles ──────────────────────────────────────────────────────
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    h1  = S('H1',  fontSize=22, textColor=WHITE,       fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
    sub = S('Sub', fontSize=11, textColor=LIGHT_BLUE,  fontName='Helvetica',      alignment=TA_CENTER)
    h2  = S('H2',  fontSize=13, textColor=MED_BLUE,    fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
    h3  = S('H3',  fontSize=11, textColor=DARK_BLUE,   fontName='Helvetica-Bold', spaceBefore=6,  spaceAfter=2)
    body= S('Body',fontSize=9,  textColor=DARK_BLUE,   fontName='Helvetica',      spaceAfter=3, leading=13)
    note= S('Note',fontSize=8,  textColor=GREY,        fontName='Helvetica-Oblique', spaceAfter=3)
    ctr = S('Ctr', fontSize=9,  textColor=GREY,        fontName='Helvetica',      alignment=TA_CENTER)

    # ── Header Banner ──────────────────────────────────────────────────────
    header_data = [[
        Paragraph('🏥 MediScan AI', h1),
        Paragraph('Intelligent Medical Report Analysis', sub)
    ]]
    header_table = Table(header_data, colWidths=[18*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING',   (0,0), (-1,-1), 20),
        ('SPAN', (0,0), (-1,-1)),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.4*cm))

    # ── Patient Info Row ───────────────────────────────────────────────────
    now = datetime.now().strftime('%d %B %Y  %H:%M')
    pi_data = [
        ['Patient Name', patient_name or 'N/A',
         'Age / Gender',  f"{patient_age} / {patient_gender}"],
        ['Report Date',  now,
         'Source File',   source_file or 'Text Input'],
        ['AI Provider',  result.get('ai_provider', 'MediScan Engine'),
         'Report ID',    f"MS-{datetime.now().strftime('%Y%m%d%H%M%S')}"]
    ]
    pi_table = Table(pi_data, colWidths=[3.5*cm, 5.5*cm, 3.5*cm, 5.5*cm])
    pi_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), LIGHT_BLUE),
        ('BACKGROUND',    (2,0), (2,-1), LIGHT_BLUE),
        ('FONTNAME',      (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',      (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
        ('TEXTCOLOR',     (0,0), (0,-1), MED_BLUE),
        ('TEXTCOLOR',     (2,0), (2,-1), MED_BLUE),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ]))
    story.append(pi_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Risk Level Banner ──────────────────────────────────────────────────
    risk_level = result.get('risk_level', 'Unknown')
    risk_score = result.get('risk_score', 0)
    fc, bc = risk_colors(risk_level)

    risk_text = f"Overall Risk: {risk_level.upper()}   |   Risk Score: {risk_score}/100"
    rS = S('Risk', fontSize=14, textColor=fc, fontName='Helvetica-Bold',
           alignment=TA_CENTER, spaceAfter=0)
    risk_table = Table([[Paragraph(risk_text, rS)]], colWidths=[18*cm])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bc),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [6]),
        ('BOX', (0,0), (-1,-1), 1.5, fc),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 0.4*cm))

    # ── Summary ───────────────────────────────────────────────────────────
    story.append(Paragraph('Executive Summary', h2))
    story.append(HRFlowable(width='100%', thickness=1, color=MED_BLUE))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(result.get('summary', 'No summary available.'), body))
    story.append(Spacer(1, 0.3*cm))

    # ── Critical Alerts ───────────────────────────────────────────────────
    alerts = result.get('critical_alerts', [])
    if alerts:
        story.append(Paragraph('⚠ Critical Alerts', h2))
        story.append(HRFlowable(width='100%', thickness=1, color=RED))
        story.append(Spacer(1, 0.2*cm))
        for alert in alerts:
            aS = S(f'Alert', fontSize=9, textColor=RED,
                   fontName='Helvetica-Bold', leftIndent=10, spaceAfter=3)
            story.append(Paragraph(f'• {alert}', aS))
        story.append(Spacer(1, 0.3*cm))

    # ── Parameters Table ──────────────────────────────────────────────────
    params = result.get('parameters', [])
    if params:
        story.append(Paragraph('Detailed Parameter Analysis', h2))
        story.append(HRFlowable(width='100%', thickness=1, color=MED_BLUE))
        story.append(Spacer(1, 0.2*cm))

        tdata = [['Parameter', 'Value', 'Normal Range', 'Status', 'Interpretation']]
        for p in params:
            sc = status_color(p.get('status', 'Normal'))
            sSt = S(f'St_{p["name"]}', fontSize=8, textColor=sc,
                    fontName='Helvetica-Bold', alignment=TA_CENTER)
            tdata.append([
                Paragraph(p.get('name', ''), body),
                Paragraph(str(p.get('value', '')), body),
                Paragraph(p.get('normal_range', ''), note),
                Paragraph(p.get('status', ''), sSt),
                Paragraph(p.get('interpretation', ''), note),
            ])

        param_table = Table(tdata, colWidths=[3.2*cm, 2.8*cm, 3.5*cm, 2.5*cm, 6*cm])
        ts = TableStyle([
            ('BACKGROUND',    (0,0), (-1,0), MED_BLUE),
            ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
            ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',      (0,0), (-1,0), 9),
            ('ALIGN',         (0,0), (-1,0), 'CENTER'),
            ('GRID',          (0,0), (-1,-1), 0.4, colors.HexColor('#B0BEC5')),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',   (0,0), (-1,-1), 5),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',         (3,1), (3,-1), 'CENTER'),
        ])
        for i in range(1, len(tdata)):
            bg = LIGHT_GREY if i % 2 == 0 else WHITE
            ts.add('BACKGROUND', (0,i), (-1,i), bg)
        param_table.setStyle(ts)
        story.append(param_table)
        story.append(Spacer(1, 0.4*cm))

    # ── Conditions Identified ─────────────────────────────────────────────
    conditions = result.get('conditions_identified', [])
    if conditions:
        story.append(Paragraph('Conditions Identified', h2))
        story.append(HRFlowable(width='100%', thickness=1, color=MED_BLUE))
        story.append(Spacer(1, 0.2*cm))
        cdata = [['Condition', 'Confidence', 'Supporting Evidence']]
        for c in conditions:
            conf = c.get('confidence', '')
            cc = RED if conf == 'High' else AMBER if conf == 'Moderate' else GREEN
            cS = S(f'Conf', fontSize=8, textColor=cc, fontName='Helvetica-Bold', alignment=TA_CENTER)
            cdata.append([
                Paragraph(c.get('condition', ''), body),
                Paragraph(conf, cS),
                Paragraph(c.get('evidence', ''), note),
            ])
        cond_table = Table(cdata, colWidths=[5*cm, 3*cm, 10*cm])
        cond_table.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0), TEAL),
            ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
            ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',      (0,0), (-1,0), 9),
            ('GRID',          (0,0), (-1,-1), 0.4, colors.HexColor('#B0BEC5')),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',   (0,0), (-1,-1), 5),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        for i in range(1, len(cdata)):
            cond_table.setStyle(TableStyle([('BACKGROUND', (0,i), (-1,i), LIGHT_GREY if i%2==0 else WHITE)]))
        story.append(cond_table)
        story.append(Spacer(1, 0.4*cm))

    # ── Recommendations ───────────────────────────────────────────────────
    recs = result.get('recommendations', [])
    if recs:
        story.append(Paragraph('Recommendations', h2))
        story.append(HRFlowable(width='100%', thickness=1, color=MED_BLUE))
        story.append(Spacer(1, 0.2*cm))
        priority_order = {'Urgent': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        recs_sorted = sorted(recs, key=lambda x: priority_order.get(x.get('priority','Low'), 4))
        for rec in recs_sorted:
            pri = rec.get('priority', 'Low')
            pc = RED if pri == 'Urgent' else AMBER if pri == 'High' else TEAL if pri == 'Medium' else GREY
            pS = S(f'Pri', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)
            rdata = [[
                Paragraph(pri, pS),
                Paragraph(rec.get('action', ''), body)
            ]]
            rt = Table(rdata, colWidths=[2*cm, 16*cm])
            rt.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (0,0), pc),
                ('TOPPADDING',    (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING',   (0,0), (-1,-1), 6),
                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
            ]))
            story.append(rt)
            story.append(Spacer(1, 0.15*cm))
        story.append(Spacer(1, 0.2*cm))

    # ── Lifestyle Advice ──────────────────────────────────────────────────
    lifestyle = result.get('lifestyle_advice', [])
    if lifestyle:
        story.append(Paragraph('Lifestyle Recommendations', h2))
        story.append(HRFlowable(width='100%', thickness=1, color=MED_BLUE))
        story.append(Spacer(1, 0.2*cm))
        for tip in lifestyle:
            story.append(Paragraph(f'✔  {tip}', body))
        story.append(Spacer(1, 0.2*cm))

    # ── Follow-up ─────────────────────────────────────────────────────────
    followup = result.get('followup', '')
    if followup:
        story.append(Paragraph('Follow-Up Plan', h2))
        story.append(HRFlowable(width='100%', thickness=1, color=MED_BLUE))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(followup, body))
        story.append(Spacer(1, 0.3*cm))

    # ── Disclaimer ────────────────────────────────────────────────────────
    disclaimer = result.get('disclaimer', '')
    disc_data = [[Paragraph(f'⚕  DISCLAIMER: {disclaimer}', note)]]
    disc_table = Table(disc_data, colWidths=[18*cm])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#FFF9C4')),
        ('BOX',           (0,0), (-1,-1), 0.8, AMBER),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ]))
    story.append(disc_table)
    story.append(Spacer(1, 0.3*cm))

    # ── Footer ────────────────────────────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=0.5, color=GREY))
    story.append(Paragraph(
        f'MediScan AI  •  Generated: {now}  •  For educational purposes only',
        ctr
    ))

    doc.build(story)
    print(f"[MediScan] PDF report generated: {output_path}")
