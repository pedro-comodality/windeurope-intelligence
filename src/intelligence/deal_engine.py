import pandas as pd


# =====================================================
# TOP ACQUISITION TARGETS
# =====================================================

def top_acquisition_targets(df):

    acquisition_df = df.copy()

    acquisition_df["deal_score"] = (

        acquisition_df["growth_potential"].fillna(0) * 0.30 +

        acquisition_df["innovation_score_v2"].fillna(0) * 0.25 +

        acquisition_df["digital_score"].fillna(0) * 0.15 +

        acquisition_df["floating_score"].fillna(0) * 0.15 +

        acquisition_df["offshore_score"].fillna(0) * 0.15

    )

    acquisition_df = acquisition_df.sort_values(
        "deal_score",
        ascending=False
    )

    return acquisition_df.head(25)


# =====================================================
# TOP PARTNERSHIP TARGETS
# =====================================================

def top_partnership_targets(df):

    partnership_df = df.copy()

    partnership_df["partnership_rank"] = (

        partnership_df["partnership_score"].fillna(0) * 0.40 +

        partnership_df["ecosystem_score"].fillna(0) * 0.30 +

        partnership_df["epc_score"].fillna(0) * 0.15 +

        partnership_df["digital_score"].fillna(0) * 0.15

    )

    partnership_df = partnership_df.sort_values(
        "partnership_rank",
        ascending=False
    )

    return partnership_df.head(25)


# =====================================================
# HIDDEN CHAMPIONS
# =====================================================

def hidden_champions(df):

    hidden_df = df.copy()

    hidden_df = hidden_df[

        hidden_df["final_strategic_score"] > 60

    ]

    hidden_df = hidden_df[

        hidden_df["lead_tier"] != "HOT"

    ]

    hidden_df = hidden_df.sort_values(
        "final_strategic_score",
        ascending=False
    )

    return hidden_df.head(25)