from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_executive_pdf(row, summary):

    company_name = row["company"]

    output_path = f"/tmp/{company_name}_report.pdf"

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        f"<b>Executive Intelligence Report</b><br/>{company_name}",
        styles["Title"]
    )

    story.append(title)

    story.append(Spacer(1, 20))

    content = f"""
    <b>Country:</b> {row['country']}<br/><br/>

    <b>Lead Tier:</b> {row['lead_tier']}<br/><br/>

    <b>Strategic Level:</b> {row['strategic_level']}<br/><br/>

    <b>Strategic Score:</b> {row['strategic_score']}<br/><br/>

    <b>Executive Summary:</b><br/>{summary}
    """

    paragraph = Paragraph(
        content,
        styles["BodyText"]
    )

    story.append(paragraph)

    doc.build(story)

    return output_path