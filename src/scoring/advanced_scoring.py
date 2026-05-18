import pandas as pd


# =====================================================
# ADVANCED STRATEGIC SCORING ENGINE
# =====================================================

def calculate_advanced_scores(df):

    # =================================================
    # OFFSHORE SCORE
    # =================================================

    df["offshore_score"] = (
        df["potencial_offshore"].fillna(0) * 20
    )

    # =================================================
    # FLOATING SCORE
    # =================================================

    df["floating_score"] = (
        df["potencial_floating"].fillna(0) * 20
    )

    # =================================================
    # EPC SCORE
    # =================================================

    df["epc_score"] = (
        df["potencial_epc"].fillna(0) * 20
    )

    # =================================================
    # INNOVATION SCORE
    # =================================================

    df["innovation_score_v2"] = (
        df["innovacion"].fillna(0) * 20
    )

    # =================================================
    # DIGITALIZATION SCORE
    # =================================================

    df["digital_score"] = (
        df["digitalizacion"].fillna(0) * 20
    )

    # =================================================
    # ECOSYSTEM SCORE
    # =================================================

    ecosystem_base = (
        df["offshore_score"]
        + df["floating_score"]
        + df["epc_score"]
    ) / 3

    df["ecosystem_score"] = ecosystem_base

    # =================================================
    # PARTNERSHIP SCORE
    # =================================================

    df["partnership_score"] = (
        (
            df["innovation_score_v2"]
            + df["digital_score"]
            + df["ecosystem_score"]
        ) / 3
    )

    # =================================================
    # ACQUISITION SCORE
    # =================================================

    df["acquisition_score"] = (
        (
            df["growth"].fillna(0) * 20
            + df["innovation_score_v2"]
        ) / 2
    )

    # =================================================
    # INFLUENCE SCORE
    # =================================================

    df["influence_score"] = (
        (
            df["market_presence"].fillna(3) * 20
        )
    )

    # =================================================
    # FINAL STRATEGIC SCORE
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
        .round(0)
        .astype(int)
    )

    # =================================================
    # STRATEGIC CATEGORY
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