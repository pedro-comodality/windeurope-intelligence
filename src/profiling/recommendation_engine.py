import pandas as pd


# =====================================================
# SAFE SORT
# =====================================================

def safe_sort(df, column):

    if column not in df.columns:
        return df

    return df.sort_values(
        by=column,
        ascending=False
    )


# =====================================================
# TOP STRATEGIC
# =====================================================

def top_strategic_companies(df, top_n=10):

    strategic_df = df[
        df["strategic_level"] == "STRATEGIC"
    ]

    strategic_df = safe_sort(
        strategic_df,
        "strategic_score"
    )

    return strategic_df.head(top_n)


# =====================================================
# TOP FLOATING
# =====================================================

def top_floating_companies(df, top_n=10):

    floating_df = df[
        df["floating_wind"] == True
    ]

    floating_df = safe_sort(
        floating_df,
        "strategic_score"
    )

    return floating_df.head(top_n)


# =====================================================
# TOP EPC
# =====================================================

def top_epc_companies(df, top_n=10):

    epc_df = df[
        df["epc"] == True
    ]

    epc_df = safe_sort(
        epc_df,
        "strategic_score"
    )

    return epc_df.head(top_n)


# =====================================================
# TOP DIGITALIZATION
# =====================================================

def top_digitalization_companies(
    df,
    top_n=10
):

    digital_df = df[
        df["digitalization"] == True
    ]

    digital_df = safe_sort(
        digital_df,
        "strategic_score"
    )

    return digital_df.head(top_n)


# =====================================================
# TOP INNOVATORS
# =====================================================

def top_innovators(df, top_n=10):

    innovator_df = safe_sort(
        df,
        "innovacion"
    )

    return innovator_df.head(top_n)