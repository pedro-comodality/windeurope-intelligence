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
    # REQUIRED COLUMNS
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
    # NUMERIC CLEANING
    # =================================================

    for col in df.columns:

        try:

            df[col] = pd.to_numeric(
                df[col],
                errors="ignore"
            )

        except Exception:

            pass

    # =================================================
    # OFFSHORE
    # =================================================

    df["offshore_score"] = (
        safe_col(df, "potencial_offshore") * 20
    )

    # =================================================
    # FLOATING
    # =================================================

    df["floating_score"] = (
        safe_col(df, "potencial_floating") * 20
    )

    # =================================================
    # EPC
    # =================================================

    df["epc_score"] = (
        safe_col(df, "potencial_epc") * 20
    )

    # =================================================
    # INNOVATION
    # =================================================

    df["innovation_score_v2"] = (
        safe_col(df, "innovacion") * 20
    )

    # =================================================
    # DIGITALIZATION
    # =================================================

    df["digital_score"] = (
        safe_col(df, "digitalizacion") * 20
    )

    # =================================================
    # ECOSYSTEM
    # =================================================

    df["ecosystem_score"] = (

        safe_col(df, "offshore_score")

        + safe_col(df, "floating_score")

        + safe_col(df, "epc_score")

    ) / 3

    # =================================================
    # PARTNERSHIP
    # =================================================

    df["partnership_score"] = (

        safe_col(df, "innovation_score_v2")

        + safe_col(df, "digital_score")

        + safe_col(df, "ecosystem_score")

    ) / 3

    # =================================================
    # ACQUISITION
    # =================================================

    df["acquisition_score"] = (

        (
            safe_col(df, "crecimiento") * 20
        )

        + safe_col(df, "innovation_score_v2")

    ) / 2

    # =================================================
    # INFLUENCE
    # =================================================

    df["influence_score"] = (
        safe_col(df, "market_presence", 3) * 20
    )

    # =================================================
    # FINAL SCORE
    # =================================================

    df["final_strategic_score"] = (

        safe_col(df, "offshore_score") * 0.20 +

        safe_col(df, "floating_score") * 0.15 +

        safe_col(df, "epc_score") * 0.15 +

        safe_col(df, "innovation_score_v2") * 0.15 +

        safe_col(df, "digital_score") * 0.10 +

        safe_col(df, "partnership_score") * 0.15 +

        safe_col(df, "influence_score") * 0.10

    )

    df["final_strategic_score"] = (

        df["final_strategic_score"]

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