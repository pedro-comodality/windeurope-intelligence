import re
import pdfplumber
import pandas as pd

from rapidfuzz import fuzz

from src.intelligence.keyword_engine import enrich_keywords


# =========================================================
# CLEANING FUNCTIONS
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_company_name(name):

    if not name:
        return ""

    # eliminar numeración tipo "1 / 199"
    name = re.sub(r"\d+\s*/\s*\d+", "", name)

    # eliminar espacios múltiples
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def clean_website(url):

    if not url:
        return ""

    # eliminar espacios internos
    url = url.replace(" ", "")

    return url.strip()


def clean_product_category(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_generation_type(text):

    if not text:
        return ""

    return text.lower().strip()


# =========================================================
# DUPLICATE DETECTION
# =========================================================

def deduplicate_companies(df):

    seen = []
    keep_rows = []

    for idx, row in df.iterrows():

        company = row["company"].lower()

        duplicate = False

        for existing in seen:

            similarity = fuzz.ratio(
                company,
                existing
            )

            if similarity > 95:
                duplicate = True
                break

        if not duplicate:

            seen.append(company)

            keep_rows.append(idx)

    return df.loc[keep_rows].reset_index(drop=True)


# =========================================================
# COMPANY EXTRACTION
# =========================================================

def extract_companies(text):

    pattern = re.compile(
        r"Company Name:\s*(.*?)\s*"
        r"Stands:\s*(.*?)\s*"
        r"Product Category:\s*(.*?)\s*"
        r"Generation Type:\s*(.*?)\s*"
        r"Website:\s*(.*?)\s*"
        r"Country:\s*(.*?)(?=Company Name:|$)",
        re.DOTALL
    )

    matches = pattern.findall(text)

    companies = []

    for match in matches:

        company = {
            "company": clean_company_name(match[0]),
            "stand": clean_text(match[1]),
            "product_category": clean_product_category(match[2]),
            "generation_type": clean_generation_type(match[3]),
            "website": clean_website(match[4]),
            "country": clean_text(match[5]),
        }

        companies.append(company)

    return companies


# =========================================================
# PDF PARSER
# =========================================================

def parse_pdf(pdf_path):

    full_text = ""

    print("\nReading PDF...\n")

    with pdfplumber.open(pdf_path) as pdf:

        total_pages = len(pdf.pages)

        print(f"Total pages: {total_pages}")

        for i, page in enumerate(pdf.pages):

            text = page.extract_text()

            if text:
                full_text += "\n" + text

            # progreso
            if i % 20 == 0:
                print(f"Processed pages: {i}/{total_pages}")

    print("\nExtracting companies...\n")

    companies = extract_companies(full_text)

    df = pd.DataFrame(companies)

    print(f"Raw companies extracted: {len(df)}")

    # eliminar duplicados
    df = deduplicate_companies(df)

    print(f"Companies after deduplication: {len(df)}")

    # =====================================================
    # INDUSTRIAL INTELLIGENCE
    # =====================================================

    print("\nApplying industrial intelligence...\n")

    df = enrich_keywords(df)

    print("Keyword intelligence completed")

    return df


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    pdf_path = "data/raw/windeurope2026.pdf"

    df = parse_pdf(pdf_path)

    print("\nPreview:\n")

    print(df.head())

    print(f"\nFinal companies extracted: {len(df)}")

    output_path = "data/processed/exhibitors_clean.xlsx"

    df.to_excel(
        output_path,
        index=False
    )

    print("\nExcel exported successfully")

    print(f"\nSaved to: {output_path}")