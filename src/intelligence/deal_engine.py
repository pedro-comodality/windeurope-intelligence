import pandas as pd


# =====================================================
# SAFE NUMERIC
# =====================================================

def safe_numeric(series):

    return pd.to_numeric(
        series,
        errors="coerce"
    ).fillna(0)


# =====================================================
# ACQUISITION TARGETS
# =====================================================

def top_acquisition_targets(df):

    acquisition_df = df.copy()

    # safe columns
    required_columns = [

        "growth_potential",
        "innovation_score_v2",
        "final_strategic_score"

    ]

    for col in required_columns:

        if col not in acquisition_df.columns:

            acquisition_df[col] = 0

    # numeric conversion
    acquisition_df["growth_potential"] = safe_numeric(
        acquisition_df["growth_potential"]
    )

    acquisition_df["innovation_score_v2"] = safe_numeric(
        acquisition_df["innovation_score_v2"]
    )

    acquisition_df["final_strategic_score"] = safe_numeric(
        acquisition_df["final_strategic_score"]
    )

    # final score
    acquisition_df["deal_score"] = (

        acquisition_df["growth_potential"] * 0.30 +

        acquisition_df["innovation_score_v2"] * 0.25 +

        acquisition_df["final_strategic_score"] * 0.45

    ).round(2)

    return acquisition_df.sort_values(
        by="deal_score",
        ascending=False
    ).head(25)


# =====================================================
# PARTNERSHIP TARGETS
# =====================================================

def top_partnership_targets(df):

    partnership_df = df.copy()

    if "partnership_score" not in partnership_df.columns:

        partnership_df["partnership_score"] = 0

    partnership_df["partnership_score"] = safe_numeric(
        partnership_df["partnership_score"]
    )

    partnership_df = partnership_df.sort_values(
        by="partnership_score",
        ascending=False
    ).head(25)

    partnership_df["partnership_rank"] = range(
        1,
        len(partnership_df) + 1
    )

    return partnership_df


# =====================================================
# HIDDEN CHAMPIONS
# =====================================================

def hidden_champions(df):

    hidden_df = df.copy()

    if "final_strategic_score" not in hidden_df.columns:

        hidden_df["final_strategic_score"] = 0

    hidden_df["final_strategic_score"] = safe_numeric(
        hidden_df["final_strategic_score"]
    )

    hidden_df = hidden_df[
        hidden_df["final_strategic_score"] >= 60
    ]

    return hidden_df.sort_values(
        by="final_strategic_score",
        ascending=False
    ).head(25)