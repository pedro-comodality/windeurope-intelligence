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
# SAFE BOOL
# =====================================================

def safe_bool(value):

    if pd.isna(value):
        return False

    return str(value).lower() in [
        "1",
        "true",
        "yes",
        "si"
    ]


# =====================================================
# ACQUISITION TARGETS
# =====================================================

def top_acquisition_targets(df):

    acquisition_df = df.copy()

    required_columns = [

        "growth_potential",
        "innovation_score_v2",
        "final_strategic_score"

    ]

    for col in required_columns:

        if col not in acquisition_df.columns:

            acquisition_df[col] = 0

    acquisition_df["growth_potential"] = safe_numeric(
        acquisition_df["growth_potential"]
    )

    acquisition_df["innovation_score_v2"] = safe_numeric(
        acquisition_df["innovation_score_v2"]
    )

    acquisition_df["final_strategic_score"] = safe_numeric(
        acquisition_df["final_strategic_score"]
    )

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


# =====================================================
# LOGISTICS TARGETS
# =====================================================

def top_logistics_targets(df):

    logistics_df = df.copy()

    # =================================================
    # REQUIRED COLUMNS
    # =================================================

    required_columns = [

        "final_strategic_score",
        "growth_potential",
        "market_presence"

    ]

    for col in required_columns:

        if col not in logistics_df.columns:

            logistics_df[col] = 0

    # =================================================
    # SAFE NUMERIC
    # =================================================

    logistics_df["final_strategic_score"] = safe_numeric(
        logistics_df["final_strategic_score"]
    )

    logistics_df["growth_potential"] = safe_numeric(
        logistics_df["growth_potential"]
    )

    logistics_df["market_presence"] = safe_numeric(
        logistics_df["market_presence"]
    )

    # =================================================
    # LOGISTICS SCORE
    # =================================================

    scores = []

    for _, row in logistics_df.iterrows():

        score = 0

        # =============================================
        # OFFSHORE
        # =============================================

        if safe_bool(row.get("offshore")):
            score += 25

        # =============================================
        # FLOATING
        # =============================================

        if safe_bool(row.get("floating_wind")):
            score += 30

        # =============================================
        # EPC
        # =============================================

        if safe_bool(row.get("epc")):
            score += 25

        # =============================================
        # MARITIME
        # =============================================

        if safe_bool(row.get("maritime_logistics")):
            score += 15

        # =============================================
        # STRATEGIC SCORE
        # =============================================

        score += (
            row.get(
                "final_strategic_score",
                0
            ) * 0.20
        )

        # =============================================
        # GROWTH
        # =============================================

        score += (
            row.get(
                "growth_potential",
                0
            ) * 5
        )

        # =============================================
        # MARKET PRESENCE
        # =============================================

        score += (
            row.get(
                "market_presence",
                0
            ) * 4
        )

        scores.append(round(score, 2))

    logistics_df["logistics_opportunity_score"] = scores

    # =================================================
    # PRIORITY CATEGORY
    # =================================================

    def classify(score):

        if score >= 85:
            return "MEGA TARGET"

        elif score >= 65:
            return "HIGH PRIORITY"

        elif score >= 45:
            return "STRATEGIC"

        else:
            return "MONITOR"

    logistics_df["logistics_priority"] = (

        logistics_df[
            "logistics_opportunity_score"
        ].apply(classify)
    )

    # =================================================
    # SORT
    # =================================================

    return logistics_df.sort_values(

        by="logistics_opportunity_score",

        ascending=False

    ).head(30)
# =====================================================
# LOGISTICS TARGETS
# =====================================================

def top_logistics_targets(df):

    logistics_df = df.copy()

    required_columns = [

        "offshore_score",
        "floating_score",
        "epc_score",
        "final_strategic_score"

    ]

    for col in required_columns:

        if col not in logistics_df.columns:

            logistics_df[col] = 0

    logistics_df["offshore_score"] = safe_numeric(
        logistics_df["offshore_score"]
    )

    logistics_df["floating_score"] = safe_numeric(
        logistics_df["floating_score"]
    )

    logistics_df["epc_score"] = safe_numeric(
        logistics_df["epc_score"]
    )

    logistics_df["final_strategic_score"] = safe_numeric(
        logistics_df["final_strategic_score"]
    )

    # =================================================
    # LOGISTICS OPPORTUNITY SCORE
    # =================================================

    logistics_df["logistics_opportunity_score"] = (

        logistics_df["offshore_score"] * 0.35 +

        logistics_df["floating_score"] * 0.30 +

        logistics_df["epc_score"] * 0.20 +

        logistics_df["final_strategic_score"] * 0.15

    ).round(2)

    # =================================================
    # PRIORITY
    # =================================================

    def classify(score):

        if score >= 80:
            return "MEGA TARGET"

        elif score >= 65:
            return "HIGH PRIORITY"

        elif score >= 50:
            return "GOOD TARGET"

        else:
            return "LOW PRIORITY"

    logistics_df["logistics_priority"] = (

        logistics_df[
            "logistics_opportunity_score"
        ].apply(classify)

    )

    return logistics_df.sort_values(

        by="logistics_opportunity_score",

        ascending=False

    ).head(50)