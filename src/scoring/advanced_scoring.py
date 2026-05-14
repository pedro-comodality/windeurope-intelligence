import pandas as pd


# =====================================================
# SAFE VALUE
# =====================================================

def safe_number(value):

    try:
        return float(value)
    except:
        return 0


# =====================================================
# STRATEGIC SCORE
# =====================================================

def calculate_strategic_score(row):

    score = 0

    # =========================================
    # OFFSHORE
    # =========================================

    score += safe_number(
        row.get("offshore_maturity")
    ) * 0.20

    # =========================================
    # FLOATING
    # =========================================

    score += safe_number(
        row.get("floating_readiness")
    ) * 0.20

    # =========================================
    # EPC
    # =========================================

    score += safe_number(
        row.get("epc_strength")
    ) * 0.15

    # =========================================
    # INNOVATION
    # =========================================

    score += safe_number(
        row.get("innovation_score")
    ) * 0.10

    # =========================================
    # DIGITALIZATION
    # =========================================

    score += safe_number(
        row.get("digitalization_score")
    ) * 0.10

    # =========================================
    # STRATEGIC FIT
    # =========================================

    score += safe_number(
        row.get("strategic_fit")
    ) * 0.15

    # =========================================
    # GROWTH
    # =========================================

    score += safe_number(
        row.get("growth_potential")
    ) * 0.05

    # =========================================
    # MARKET PRESENCE
    # =========================================

    score += safe_number(
        row.get("market_presence")
    ) * 0.05

    return round(score, 2)


# =====================================================
# CLASSIFICATION
# =====================================================

def classify_strategic_level(score):

    if score >= 8:
        return "STRATEGIC"

    elif score >= 6:
        return "HIGH VALUE"

    elif score >= 4:
        return "GROWTH TARGET"

    elif score >= 2:
        return "NICHE PLAYER"

    else:
        return "LOW PRIORITY"