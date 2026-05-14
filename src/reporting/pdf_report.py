from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def generate_executive_pdf(row, summary):

    output_path = f"{row['company']}_report.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = "WindEurope Executive Intelligence Report"

    elements.append(
        Paragraph(title, styles['Title'])
    )

    elements.append(
        Spacer(1, 20)
    )

    company_info = f"""
    <b>Company:</b> {row['company']}<br/>
    <b>Country:</b> {row['country']}<br/>
    <b>Strategic Level:</b> {row['strategic_level']}<br/>
    <b>Lead Tier:</b> {row['lead_tier']}<br/>
    """

    elements.append(
        Paragraph(company_info, styles['BodyText'])
    )

    elements.append(
        Spacer(1, 20)
    )

    executive_summary = f"""
    <b>Executive Summary</b><br/><br/>
    {summary}
    """

    elements.append(
        Paragraph(executive_summary, styles['BodyText'])
    )

    doc.build(elements)

    return output_path