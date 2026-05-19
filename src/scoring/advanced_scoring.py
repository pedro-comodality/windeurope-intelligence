import pandas as pd


# =====================================================
# SAFE COLUMN
# =====================================================

def safe_col(df, col, default=0):

    if col in df.columns:

        return pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(default)

    return pd.Series(
        [default] * len(df),
        dtype="float"
    )


# =====================================================
# ADVANCED SCORING
# =====================================================

def calculate_advanced_scores(df):

    # =================================================
    # SAFE REQUIRED COLUMNS
    # =================================================

    required_columns = [

        "potencial_offshore",
        "potencial_floating",
        "potencial_epc",
        "innovacion",
        "digitalizacion",
        "crecimiento",
        "market_presence"

    ]

    for col in required_columns:

        if col not in df.columns:

            df[col] = 0

    # =================================================
    # SCORE CALCULATIONS
    # =================================================

    offshore_score = (
        safe_col(df, "potencial_offshore") * 20
    )

    floating_score = (
        safe_col(df, "potencial_floating") * 20
    )

    epc_score = (
        safe_col(df, "potencial_epc") * 20
    )

    innovation_score = (
        safe_col(df, "innovacion") * 20
    )

    digital_score = (
        safe_col(df, "digitalizacion") * 20
    )

    growth_score = (
        safe_col(df, "crecimiento") * 20
    )

    influence_score = (
        safe_col(df, "market_presence", 3) * 20
    )

    # =================================================
    # ASSIGN COLUMNS
    # =================================================

    df["offshore_score"] = offshore_score
    df["floating_score"] = floating_score
    df["epc_score"] = epc_score
    df["innovation_score_v2"] = innovation_score
    df["digital_score"] = digital_score
    df["influence_score"] = influence_score

    # =================================================
    # ECOSYSTEM
    # =================================================

    ecosystem_score = (

        offshore_score

        + floating_score

        + epc_score

    ) / 3

    df["ecosystem_score"] = ecosystem_score

    # =================================================
    # PARTNERSHIP
    # =================================================

    partnership_score = (

        innovation_score

        + digital_score

        + ecosystem_score

    ) / 3

    df["partnership_score"] = partnership_score

    # =================================================
    # ACQUISITION
    # =================================================

    acquisition_score = (

        growth_score

        + innovation_score

    ) / 2

    df["acquisition_score"] = acquisition_score

    # =================================================
    # FINAL SCORE
    # =================================================

    final_score = (

        offshore_score * 0.20 +

        floating_score * 0.15 +

        epc_score * 0.15 +

        innovation_score * 0.15 +

        digital_score * 0.10 +

        partnership_score * 0.15 +

        influence_score * 0.10

    )

    df["final_strategic_score"] = (

        final_score

        .fillna(0)

        .round(0)

        .astype(int)

    )

    # =================================================
    # CATEGORY
    # =================================================

    def categorize(score):

        if score >= 85:
            return "ELITE"

        elif score >= 70:
            return "STRATEGIC"

        elif score >= 55:
            return "HIGH VALUE"

        elif score >= 40:
            return "GROWTH TARGET"

        else:
            return "LOW PRIORITY"

    df["strategic_category_v2"] = (
        df["final_strategic_score"]
        .apply(categorize)
    )

    return df