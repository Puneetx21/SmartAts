from io import BytesIO
from datetime import datetime
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def _safe_list(values):
    if not values:
        return ["None"]
    return [str(value) for value in values]


def _clean_text(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    text = re.sub(r"^[^A-Za-z0-9(]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _truncate_list(values, limit: int):
    cleaned = [_clean_text(v) for v in _safe_list(values)]
    cleaned = [v for v in cleaned if v]
    if not cleaned:
        return ["None"]

    if len(cleaned) <= limit:
        return cleaned

    remaining = len(cleaned) - limit
    return cleaned[:limit] + [f"... and {remaining} more"]


class _ReportCanvas(canvas.Canvas):
    def __init__(self, *args, generated_label: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self._generated_label = generated_label

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for idx, page_state in enumerate(self._saved_page_states, start=1):
            self.__dict__.update(page_state)
            self._draw_footer(page_number=idx, total_pages=total_pages)
            super().showPage()
        super().save()

    def _draw_footer(self, page_number: int, total_pages: int) -> None:
        self.saveState()
        footer_y = 0.45 * inch

        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4b5563"))
        if self._generated_label:
            self.drawString(0.75 * inch, footer_y, self._generated_label)
        self.drawRightString(A4[0] - 0.75 * inch, footer_y, f"Page {page_number}")

        self.restoreState()


def _add_section_header(content, styles, title: str):
    content.append(Spacer(1, 18))
    content.append(Paragraph(f"<u><b>{title}</b></u>", styles["SectionHeader"]))
    content.append(Spacer(1, 10))


def _add_bullet_list(content, styles, items):
    for item in _safe_list(items):
        content.append(Paragraph(_clean_text(item), styles["BulletLine"], bulletText="•"))


def _add_colored_bullet_list(content, styles, items, text_color: str):
    bullet_style = ParagraphStyle(
        "BulletLineColor",
        parent=styles["BulletLine"],
        textColor=colors.HexColor(text_color),
    )
    for item in _safe_list(items):
        content.append(Paragraph(_clean_text(item), bullet_style, bulletText="•"))


def _add_keyword_text_list(content, styles, items, usable_width: float, text_color: str):
    values = [_clean_text(v) for v in _safe_list(items)]
    values = [v for v in values if v]
    if not values:
        values = ["None"]

    # Use 2 columns only for richer lists to save vertical space.
    if len(values) >= 3:
        two_col_style = ParagraphStyle(
            "TwoColKeywordLine",
            parent=styles["BulletLine"],
            textColor=colors.HexColor(text_color),
        )
        two_col_style.tabStops = [usable_width / 2]
        for index in range(0, len(values), 2):
            left = values[index]
            right = values[index + 1] if index + 1 < len(values) else ""
            row_text = f"• {left}"
            if right:
                row_text += f"\t• {right}"
            content.append(Paragraph(row_text, two_col_style))
    else:
        _add_colored_bullet_list(content, styles, values, text_color)


def generate_report_pdf(report_data: dict) -> bytes:
    buffer = BytesIO()
    page_margin = 0.75 * inch
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=page_margin,
        leftMargin=page_margin,
        topMargin=page_margin,
        bottomMargin=page_margin,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="MetaLine",
            parent=styles["Normal"],
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#6b7280"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyLine",
            parent=styles["Normal"],
            fontSize=11,
            leading=15,
            fontName="Helvetica",
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletLine",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            leftIndent=18,
            bulletIndent=7,
            firstLineIndent=0,
            fontName="Helvetica",
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading3"],
            fontSize=13,
            leading=15,
            spaceBefore=3,
            spaceAfter=2,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1f2937"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeader",
            parent=styles["Heading2"],
            fontSize=15,
            leading=17,
            spaceBefore=0,
            spaceAfter=1,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1e3a8a"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="TitleLine",
            parent=styles["Heading1"],
            fontSize=18,
            leading=20,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1e3a8a"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="EndingLine",
            parent=styles["Normal"],
            fontSize=11,
            leading=13,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#6b7280"),
        )
    )

    content = []

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    ats_score = report_data.get("ats_score", 0)
    keyword_coverage = round(report_data.get("keyword_match", {}).get("coverage", 0), 1)
    candidate_name = report_data.get("name") or "Not detected"
    role_name = report_data.get("role", "-")
    usable_width = A4[0] - document.leftMargin - document.rightMargin

    content.append(Paragraph("<u><b>SmartATS Resume Analysis Report</b></u>", styles["TitleLine"]))
    content.append(Spacer(1, 4))

    score_card = Table(
        [[f"Overall ATS Score: {ats_score}/100", f"Keyword Coverage: {keyword_coverage}%"]],
        colWidths=[usable_width / 2, usable_width / 2],
    )
    score_card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 13),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#bfdbfe")),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#bfdbfe")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    content.append(score_card)

    _add_section_header(content, styles, "Summary")
    summary_rows = [
        ["Candidate Name", candidate_name],
        ["Target Role", role_name],
        ["Overall ATS Score", f"{ats_score}/100"],
        ["Experience Level", report_data.get("experience_level", {}).get("level", "-")],
        ["Keyword Coverage", f"{keyword_coverage}%"],
    ]

    summary_table = Table(summary_rows, colWidths=[usable_width * 0.35, usable_width * 0.65])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#fafafa")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1f2937")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    content.append(summary_table)

    _add_section_header(content, styles, "Score Explanation")
    content.append(Paragraph(_clean_text(report_data.get("score_explanation", "Analysis complete.")), styles["BodyLine"]))

    section_info = report_data.get("section_info", {})
    metrics_rows = [
        ["Length Score", f"{report_data.get('length_score', 0)}/100", "#0f766e"],
        ["Formatting Score", f"{report_data.get('formatting_score', 0)}/100", "#1d4ed8"],
        ["Action Verb Score", f"{report_data.get('action_verb_score', 0)}/100", "#b45309"],
        ["Technical Depth Score", f"{report_data.get('technical_depth_score', 0)}/100", "#7c3aed"],
        ["Consistency Score", f"{report_data.get('consistency_score', 0)}/100", "#065f46"],
        ["Sections Present", f"{len(section_info.get('present', []))}/4", "#0f172a"],
    ]

    _add_section_header(content, styles, "Detailed Metrics")
    metrics_data = [[name, value] for name, value, _ in metrics_rows]
    metric_styles = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#fafafa")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for row_idx, (_, _, color_code) in enumerate(metrics_rows):
        metric_styles.append(("TEXTCOLOR", (1, row_idx), (1, row_idx), colors.HexColor(color_code)))

    metrics_table = Table(metrics_data, colWidths=[usable_width * 0.65, usable_width * 0.35])
    metrics_table.setStyle(TableStyle(metric_styles))
    content.append(metrics_table)

    keyword_match = report_data.get("keyword_match", {})
    _add_section_header(content, styles, "Keyword Analysis")

    content.append(Paragraph("<b><font color='#065f46'>Required Skills Present</font></b>", styles["SubTitle"]))
    _add_keyword_text_list(content, styles, keyword_match.get("required_present", []), usable_width, "#065f46")

    content.append(Paragraph("<b><font color='#991b1b'>Missing Required Skills</font></b>", styles["SubTitle"]))
    _add_keyword_text_list(content, styles, keyword_match.get("required_missing", []), usable_width, "#991b1b")

    content.append(Paragraph("<b><font color='#92400e'>Nice-to-Have Skills Present</font></b>", styles["SubTitle"]))
    _add_keyword_text_list(content, styles, keyword_match.get("nice_present", []), usable_width, "#92400e")

    _add_section_header(content, styles, "Feedback Summary")

    content.append(Paragraph("<b><font color='#166534'>Strong Areas</font></b>", styles["SubTitle"]))
    _add_colored_bullet_list(content, styles, report_data.get("strong_areas", []), "#166534")

    content.append(Paragraph("<b><font color='#991b1b'>Areas for Improvement</font></b>", styles["SubTitle"]))
    _add_colored_bullet_list(content, styles, _truncate_list(report_data.get("weak_points", []), 5), "#991b1b")

    content.append(Paragraph("<b><font color='#1e3a8a'>Prioritized Suggestions</font></b>", styles["SubTitle"]))
    _add_colored_bullet_list(content, styles, report_data.get("improvement_suggestions", []), "#1e3a8a")

    _add_section_header(content, styles, "Resume Format Best Practices")
    _add_colored_bullet_list(content, styles, report_data.get("template_feedback", []), "#92400e")

    content.append(Spacer(1, 12))
    content.append(Paragraph("**************************************************", styles["EndingLine"]))

    generated_label = f"Report generated By SmartAts on {report_time}"
    document.build(
        content,
        canvasmaker=lambda *args, **kwargs: _ReportCanvas(*args, generated_label=generated_label, **kwargs),
    )
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content