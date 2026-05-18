from src.extraction.pdf_parser import parse_pdf

from src.scraping.website_scraper import (
    scrape_websites
)

from src.profiling.deep_profile_engine import (
    enrich_profiles
)

from src.enrichment.enricher import (
    enrich_dataframe
)

from src.scoring.scoring_engine import (
    calculate_score,
    classify_lead
)

from src.scoring.advanced_scoring import (
    calculate_strategic_score,
    classify_strategic_level
)

from src.sales.sales_agent import (
    enrich_sales
)

# =====================================================
# STEP 1 — PARSE PDF
# =====================================================

print("\nSTEP 1 — Parsing PDF...\n")

pdf_path = "data/raw/windeurope2026.pdf"

df = parse_pdf(pdf_path)

print("\nPDF parsing completed")


# =====================================================
# OPTIONAL TEST MODE
# =====================================================

# =====================================================
# IMPORTANTE:
# usar solo para pruebas rápidas
# comenta esta línea para procesar TODO
# =====================================================

df = df


# =====================================================
# STEP 1.5 — WEBSITE SCRAPING
# =====================================================

print("\nSTEP 1.5 — Website Scraping...\n")

df = scrape_websites(df)

print("\nWebsite scraping completed")

# =====================================================
# STEP 1.7 — DEEP AI PROFILING
# =====================================================

print("\nSTEP 1.7 — Deep AI Profiling...\n")

df = enrich_profiles(df)

print("\nDeep AI profiling completed")


# =====================================================
# STEP 2 — AI ENRICHMENT
# =====================================================

print("\nSTEP 2 — AI Enrichment...\n")

df = enrich_dataframe(df)

print("\nAI enrichment completed")


# =====================================================
# REMOVE DUPLICATED COLUMNS
# =====================================================

df = df.loc[:, ~df.columns.duplicated()]


# =====================================================
# STEP 3 — LEAD SCORING
# =====================================================

print("\nSTEP 3 — Lead Scoring...\n")

df["lead_score"] = df.apply(
    calculate_score,
    axis=1
)

df["lead_tier"] = df[
    "lead_score"
].apply(classify_lead)

print("\nLead scoring completed")

# =====================================================
# STEP 3.5 — STRATEGIC SCORING
# =====================================================

print("\nSTEP 3.5 — Strategic Scoring...\n")

df["strategic_score"] = df.apply(
    calculate_strategic_score,
    axis=1
)

df["strategic_level"] = df[
    "strategic_score"
].apply(classify_strategic_level)

print("\nStrategic scoring completed")

# =====================================================
# STEP 4 — AI SALES AGENT
# =====================================================

print("\nSTEP 4 — AI Sales Agent...\n")

df = enrich_sales(df)

print("\nAI Sales Agent completed")

# =====================================================
# STEP 4 — SORT LEADS
# =====================================================

print("\nSTEP 4 — Sorting leads...\n")

df = df.sort_values(
    by="lead_score",
    ascending=False
)

print("Lead sorting completed")


# =====================================================
# STEP 5 — EXPORT
# =====================================================

output_path = "data/exports/windeurope_ai_sales.xlsx"

df.to_excel(
    output_path,
    index=False
)

print("\nExcel exported successfully")

print(f"\nSaved to: {output_path}")


# =====================================================
# FINAL PREVIEW
# =====================================================

print("\nTOP LEADS:\n")

preview_columns = [
    "company",
    "country",
    "offshore",
    "floating_wind",
    "epc",
    "lead_score",
    "lead_tier"
]

print(
    df[
        preview_columns
    ].head(20)
)