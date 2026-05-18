import pandas as pd


# =====================================================
# SAFE COLUMN
# =====================================================

def safe_col(df, col, default=0):

    if col in df.columns:
        return df[col].fillna(default)

    return pd.Series(
        [default] * len(df)
    )


# =====================================================
# ADVANCED SCORING
# =====================================================

def calculate_advanced_scores(df):

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

        df["offshore_score"]

        + df["floating_score"]

        + df["epc_score"]

    ) / 3

    # =================================================
    # PARTNERSHIP
    # =================================================

    df["partnership_score"] = (

        df["innovation_score_v2"]

        + df["digital_score"]

        + df["ecosystem_score"]

    ) / 3

    # =================================================
    # ACQUISITION
    # =================================================

    df["acquisition_score"] = (

        (
            safe_col(df, "crecimiento") * 20
        )

        + df["innovation_score_v2"]

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

        df["offshore_score"] * 0.20 +

        df["floating_score"] * 0.15 +

        df["epc_score"] * 0.15 +

        df["innovation_score_v2"] * 0.15 +

        df["digital_score"] * 0.10 +

        df["partnership_score"] * 0.15 +

        df["influence_score"] * 0.10

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