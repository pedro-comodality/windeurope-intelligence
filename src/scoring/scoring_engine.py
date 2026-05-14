import pandas as pd


# =====================================================
# SAFE VALUE EXTRACTION
# =====================================================

def get_single_value(value):

    # si viene una serie duplicada
    if isinstance(value, pd.Series):

        if len(value) > 0:
            value = value.iloc[0]
        else:
            return False

    return value


# =====================================================
# SAFE BOOLEAN CHECK
# =====================================================

def is_true(value):

    value = get_single_value(value)

    if pd.isna(value):
        return False

    if isinstance(value, bool):
        return value

    value = str(value).lower()

    return value in [
        "true",
        "verdadero",
        "1",
        "yes"
    ]


# =====================================================
# SCORE CALCULATION
# =====================================================

def calculate_score(row):

    score = 0

    # =================================================
    # OFFSHORE
    # =================================================

    if is_true(row.get("offshore")):
        score += 20

    # =================================================
    # FLOATING WIND
    # =================================================

    if is_true(row.get("floating_wind")):
        score += 15

    # =================================================
    # EPC
    # =================================================

    if is_true(row.get("epc")):
        score += 10

    # =================================================
    # DIGITALIZATION
    # =================================================

    if is_true(row.get("digitalization")):
        score += 10

    # =================================================
    # AI
    # =================================================

    if is_true(row.get("ai")):
        score += 10

    # =================================================
    # ROBOTICS
    # =================================================

    if is_true(row.get("robotics")):
        score += 10

    # =================================================
    # PREDICTIVE MAINTENANCE
    # =================================================

    if is_true(row.get("predictive_maintenance")):
        score += 10

    # =================================================
    # CABLE SYSTEMS
    # =================================================

    if is_true(row.get("cable_systems")):
        score += 5

    # =================================================
    # FOUNDATIONS
    # =================================================

    if is_true(row.get("foundations")):
        score += 5

    # =================================================
    # MARITIME LOGISTICS
    # =================================================

    if is_true(row.get("maritime_logistics")):
        score += 5

    # =================================================
    # LIMIT
    # =================================================

    if score > 100:
        score = 100

    return score


# =====================================================
# LEAD CLASSIFICATION
# =====================================================

def classify_lead(score):

    if score >= 80:
        return "HOT"

    elif score >= 50:
        return "WARM"

    return "LOW"