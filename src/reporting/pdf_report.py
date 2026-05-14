from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

import os


def generate_executive_pdf(row, summary):

    output_path = f"temp_{row['company']}.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = f"""
    WindEurope Executive Intelligence Report
    """

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
    <b>Lead Score:</b> {row['lead_score']}<br/>
    <b>Strategic Score:</b> {row['strategic_score']}<br/>
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

    elements.append(
        Spacer(1, 20)
    )

    sales_strategy = f"""
    <b>AI Sales Strategy</b><br/><br/>
    {row['sales_strategy']}
    """

    elements.append(
        Paragraph(sales_strategy, styles['BodyText'])
    )

    doc.build(elements)

    return output_path