from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def _safe_list(values):
    if not values:
        return ["None"]
    return [str(value) for value in values]


def _add_section_header(content, styles, title: str):
    header_table = Table([[title]], colWidths=[6.8 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef2ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -1), 0.8, colors.HexColor("#c7d2fe")),
            ]
        )
    )
    content.append(Spacer(1, 10))
    content.append(header_table)
    content.append(Spacer(1, 6))


def _add_bullet_list(content, styles, items):
    for item in _safe_list(items):
        content.append(Paragraph(f"• {item}", styles["BulletLine"]))


def generate_report_pdf(report_data: dict) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="MetaLine",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#6b7280"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyLine",
            parent=styles["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletLine",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            leftIndent=10,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading3"],
            fontSize=10,
            leading=13,
            spaceBefore=5,
            spaceAfter=4,
            textColor=colors.HexColor("#1f2937"),
        )
    )

    content = []

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    ats_score = report_data.get("ats_score", 0)
    keyword_coverage = round(report_data.get("keyword_match", {}).get("coverage", 0), 1)
    candidate_name = report_data.get("name") or "Not detected"
    role_name = report_data.get("role", "-")

    title_table = Table([["SmartATS Resume Analysis Report"]], colWidths=[6.8 * inch])
    title_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 14),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    content.append(title_table)
    content.append(Spacer(1, 8))
    content.append(Paragraph(f"Generated on {report_time}", styles["MetaLine"]))
    content.append(Spacer(1, 6))

    score_card = Table(
        [[f"Overall ATS Score: {ats_score}/100", f"Keyword Coverage: {keyword_coverage}%"]],
        colWidths=[3.4 * inch, 3.4 * inch],
    )
    score_card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
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

    summary_table = Table(summary_rows, colWidths=[2.2 * inch, 4.6 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f9fafb")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#374151")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    content.append(summary_table)

    _add_section_header(content, styles, "Score Explanation")
    content.append(Paragraph(report_data.get("score_explanation", "Analysis complete."), styles["BodyLine"]))

    section_info = report_data.get("section_info", {})
    metrics_rows = [
        ["Length Score", f"{report_data.get('length_score', 0)}/100"],
        ["Formatting Score", f"{report_data.get('formatting_score', 0)}/100"],
        ["Action Verb Score", f"{report_data.get('action_verb_score', 0)}/100"],
        ["Technical Depth Score", f"{report_data.get('technical_depth_score', 0)}/100"],
        ["Consistency Score", f"{report_data.get('consistency_score', 0)}/100"],
        ["Sections Present", f"{len(section_info.get('present', []))}/4"],
    ]

    _add_section_header(content, styles, "Detailed Metrics")
    metrics_table = Table(metrics_rows, colWidths=[4.6 * inch, 2.2 * inch])
    metrics_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f9fafb")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    content.append(metrics_table)

    keyword_match = report_data.get("keyword_match", {})
    _add_section_header(content, styles, "Keyword Analysis")
    content.append(Paragraph("Required Skills Present", styles["SubTitle"]))
    _add_bullet_list(content, styles, keyword_match.get("required_present", []))

    content.append(Paragraph("Missing Required Skills", styles["SubTitle"]))
    _add_bullet_list(content, styles, keyword_match.get("required_missing", []))

    content.append(Paragraph("Nice-to-Have Skills Present", styles["SubTitle"]))
    _add_bullet_list(content, styles, keyword_match.get("nice_present", []))

    _add_section_header(content, styles, "Feedback Summary")
    content.append(Paragraph("Strong Areas", styles["SubTitle"]))
    _add_bullet_list(content, styles, report_data.get("strong_areas", []))

    content.append(Paragraph("Areas for Improvement", styles["SubTitle"]))
    _add_bullet_list(content, styles, report_data.get("weak_points", []))

    content.append(Paragraph("Prioritized Suggestions", styles["SubTitle"]))
    _add_bullet_list(content, styles, report_data.get("improvement_suggestions", []))

    _add_section_header(content, styles, "Resume Format Best Practices")
    _add_bullet_list(content, styles, report_data.get("template_feedback", []))

    content.append(Spacer(1, 12))
    content.append(Paragraph("This report is generated by SmartATS (logic-based analysis).", styles["MetaLine"]))

    document.build(content)
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content