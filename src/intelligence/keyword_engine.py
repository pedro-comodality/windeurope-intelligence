import pandas as pd


# =========================================================
# INDUSTRIAL KEYWORDS
# =========================================================

KEYWORDS = {

    "floating_wind": [
        "floating",
        "mooring",
        "dynamic cable",
        "floating foundation"
    ],

    "offshore": [
        "offshore",
        "subsea",
        "marine",
        "vessel",
        "shipyard"
    ],

    "cable_systems": [
        "cable",
        "subsea cable",
        "hv cable",
        "inter-array"
    ],

    "foundations": [
        "foundation",
        "monopile",
        "jacket",
        "anchor"
    ],

    "robotics": [
        "robot",
        "robotics",
        "inspection systems",
        "drone"
    ],

    "predictive_maintenance": [
        "condition monitoring",
        "predictive",
        "scada",
        "asset management"
    ],

    "digitalization": [
        "iot",
        "software",
        "analytics",
        "data analysis",
        "digital"
    ],

    "ai": [
        "artificial intelligence",
        "machine learning",
        "ai"
    ],

    "maritime_logistics": [
        "port",
        "transportation",
        "vessel",
        "marine",
        "logistics"
    ],

    "epc": [
        "construction",
        "engineering",
        "installation",
        "infrastructure"
    ]
}


# =========================================================
# DETECT KEYWORDS
# =========================================================

def detect_keywords(text):

    text = str(text).lower()

    results = {}

    for category, keywords in KEYWORDS.items():

        found = False

        for keyword in keywords:

            if keyword in text:
                found = True
                break

        results[category] = found

    return results


# =========================================================
# APPLY INTELLIGENCE
# =========================================================

def enrich_keywords(df):

    all_results = []

    for _, row in df.iterrows():

        combined_text = " ".join([
            str(row["company"]),
            str(row["product_category"]),
            str(row["generation_type"])
        ])

        keyword_results = detect_keywords(
            combined_text
        )

        all_results.append(keyword_results)

    keywords_df = pd.DataFrame(all_results)

    df = pd.concat(
        [df, keywords_df],
        axis=1
    )

    return df