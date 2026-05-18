import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import streamlit as st
import sys
import os

# =====================================================
# PATH FIX
# =====================================================

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# =====================================================
# IMPORTS
# =====================================================

import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

from src.reporting.pdf_report import (
    generate_executive_pdf
)

from src.profiling.executive_summary import (
    generate_executive_summary
)

from src.profiling.relationship_engine import (
    generate_relationship_analysis
)

from src.visualization.network_graph import (
    build_network_graph
)

from src.profiling.recommendation_engine import (
    top_strategic_companies,
    top_floating_companies,
    top_epc_companies,
    top_digitalization_companies
)

from src.profiling.chat_analyst import (
    ask_ai_analyst
)

from src.sales.outreach_generator import (
    generate_outreach_email
)

from src.crm.crm_engine import (
    save_crm
)

from src.sales.meeting_prep import (
    generate_meeting_prep
)

from src.scoring.advanced_scoring import (
    calculate_advanced_scores
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="WindEurope Intelligence",
    layout="wide"
)
# =====================================================
# AUTHENTICATION
# =====================================================

with open("config.yaml") as file:

    config = yaml.load(
        file,
        Loader=SafeLoader
    )

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

authenticator.login()

if st.session_state["authentication_status"]:

    st.sidebar.success(
        f"Welcome {st.session_state['name']}"
    )

    authenticator.logout(
        "Logout",
        "sidebar"
    )

elif st.session_state["authentication_status"] is False:

    st.error("Username/password incorrect")
    st.stop()

elif st.session_state["authentication_status"] is None:

    st.warning("Please login")
    st.stop()
# =====================================================
# STYLING
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #07111f;
    color: white;
}

[data-testid="metric-container"] {
    background-color: #111c2d;
    border: 1px solid #1e2d45;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("🌊 WindEurope 2026 Intelligence Platform")

st.caption(
    "AI-powered offshore wind ecosystem intelligence platform"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    return pd.read_excel(
        "data/exports/windeurope_ai_sales.xlsx"
    )

df = load_data()

# =====================================================
# ADVANCED SCORING
# =====================================================

df = calculate_advanced_scores(df)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🎯 Filters")

# =====================================================
# COUNTRY FILTER
# =====================================================

if "country" in df.columns:

    country_values = sorted(
        df["country"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_countries = st.sidebar.multiselect(
        "🌍 Countries",
        options=country_values,
        default=country_values
    )

    df = df[
        df["country"]
        .isin(selected_countries)
    ]



search = st.sidebar.text_input(
    "Search company"
)

# =====================================================
# LEAD TIER
# =====================================================

if "lead_tier" in df.columns:

    tier_values = (
        df["lead_tier"]
        .dropna()
        .unique()
    )

    tier_filter = st.sidebar.multiselect(
        "Lead Tier",
        options=tier_values,
        default=tier_values
    )

    df = df[
        df["lead_tier"].isin(tier_filter)
    ]

# =====================================================
# STRATEGIC LEVEL
# =====================================================

if "strategic_level" in df.columns:

    strategic_values = (
        df["strategic_level"]
        .dropna()
        .unique()
    )

    strategic_filter = st.sidebar.multiselect(
        "Strategic Level",
        options=strategic_values,
        default=strategic_values
    )

    df = df[
        df["strategic_level"].isin(
            strategic_filter
        )
    ]

# =====================================================
# FILTERS
# =====================================================

offshore_filter = st.sidebar.checkbox(
    "Offshore only"
)

if offshore_filter:

    df = df[
        df["offshore"] == True
    ]

floating_filter = st.sidebar.checkbox(
    "Floating Wind only"
)

if floating_filter:

    df = df[
        df["floating_wind"] == True
    ]

epc_filter = st.sidebar.checkbox(
    "EPC only"
)

if epc_filter:

    df = df[
        df["epc"] == True
    ]

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🧠 Intelligence",
    "🤖 AI Analyst",
    "📌 CRM",
    "🌐 Network"
])

# =====================================================
# TAB 1 — DASHBOARD
# =====================================================

with tab1:

    st.subheader("📊 Executive Dashboard")

    # =================================================
    # COUNTRY OVERVIEW
    # =================================================

    selected_country_count = len(selected_countries)

    st.info(
        f"🌍 Active Countries: {selected_country_count}"
    )

    # =================================================
    # KPI METRICS
    # =================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Companies",
        len(df)
    )

    col2.metric(
        "HOT Leads",
        len(df[df["lead_tier"] == "HOT"])
    )

    col3.metric(
        "Elite + Strategic",
        len(
            df[
                df["strategic_category_v2"]
                .isin(["ELITE", "STRATEGIC"])
            ]
        )
    )

    col4.metric(
        "Offshore",
        len(df[df["offshore"] == True])
    )

    col5.metric(
        "Floating",
        len(df[df["floating_wind"] == True])
    )

    # =================================================
    # TOP COUNTRIES
    # =================================================

    st.subheader("🏆 Top Countries by Strategic Score")

    country_scores = (

        df.groupby("country")[
            "final_strategic_score"
        ]

        .mean()

        .reset_index()

        .sort_values(
            "final_strategic_score",
            ascending=False
        )

    )

    country_score_chart = px.bar(
        country_scores,
        x="country",
        y="final_strategic_score"
    )

    st.plotly_chart(
        country_score_chart,
        use_container_width=True
    )

    # =================================================
    # COUNTRY DISTRIBUTION
    # =================================================

    st.subheader("🌍 Country Distribution")

    country_chart = px.histogram(
        df,
        x="country"
    )

    st.plotly_chart(
        country_chart,
        use_container_width=True
    )

    # =================================================
    # ADVANCED STRATEGIC SCORE
    # =================================================

    st.subheader("🚀 Advanced Strategic Score")

    advanced_chart = px.histogram(
        df,
        x="final_strategic_score",
        nbins=20
    )

    st.plotly_chart(
        advanced_chart,
        use_container_width=True
    )

    # =================================================
    # STRATEGIC CATEGORY
    # =================================================

    st.subheader("🏆 Strategic Category Distribution")

    category_chart = px.histogram(
        df,
        x="strategic_category_v2",
        color="strategic_category_v2"
    )

    st.plotly_chart(
        category_chart,
        use_container_width=True
    )

    # =================================================
    # ELITE COMPANIES
    # =================================================

    st.subheader("🚀 Elite Strategic Companies")

    elite_df = df.sort_values(
        "final_strategic_score",
        ascending=False
    ).head(25)

    st.dataframe(
        elite_df[
            [
                "company",
                "country",
                "final_strategic_score",
                "strategic_category_v2",
                "offshore_score",
                "floating_score",
                "epc_score"
            ]
        ],
        use_container_width=True
    )

    # =================================================
    # COUNTRY LEADERS
    # =================================================

    st.subheader("🌍 Country Strategic Leaders")

    country_leaders = (

        df.sort_values(
            "final_strategic_score",
            ascending=False
        )

        .groupby("country")

        .head(3)

    )

    st.dataframe(

        country_leaders[
            [
                "country",
                "company",
                "final_strategic_score",
                "strategic_category_v2"
            ]
        ],

        use_container_width=True
    )


# =====================================================
# TAB 2 — INTELLIGENCE
# =====================================================

with tab2:

    st.subheader("🎯 AI Target Recommendations")

    strategic_df = top_strategic_companies(df)

    st.dataframe(
        strategic_df.head(25),
        use_container_width=True
    )

    # COMPANY SELECTOR

    company_selected = st.selectbox(
        "Select company",
        df["company"]
    )

    selected_df = df[
        df["company"] == company_selected
    ]

    if len(selected_df) > 0:

        row = selected_df.iloc[0]

        st.subheader("🧠 Company Intelligence")

        st.write(row)

        # EXECUTIVE SUMMARY

        st.subheader("📋 Executive Summary")

        summary = generate_executive_summary(
            row
        )

        st.write(summary)

        # PDF

        st.subheader("📄 Executive Report")

        if st.button("📄 Generate Executive PDF"):

            with st.spinner(
                "Generating executive report..."
            ):

                pdf_path = generate_executive_pdf(
                    row,
                    summary
                )

                with open(
                    pdf_path,
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        label="⬇ Download Executive PDF",
                        data=pdf_file,
                        file_name=f"{row['company']}_executive_report.pdf",
                        mime="application/pdf"
                    )

# =====================================================
# TAB 3 — AI ANALYST
# =====================================================

with tab3:

    st.subheader(
        "🧠 AI Market Intelligence Analyst"
    )

    question = st.text_input(
        "Ask the AI analyst"
    )

    if question:

        with st.spinner(
            "Analyzing..."
        ):

            answer = ask_ai_analyst(
                question,
                df
            )

            st.write(answer)

# =====================================================
# TAB 4 — CRM
# =====================================================

with tab4:

    st.subheader("📌 CRM Management")

    if "row" in locals():

        crm_status = st.selectbox(
            "Lead Status",
            [
                "Prospect",
                "Contacted",
                "Meeting",
                "Proposal",
                "Partner",
                "Rejected"
            ]
        )

        crm_notes = st.text_area(
            "Commercial Notes"
        )

        if st.button("Save CRM"):

            save_crm(
                row["company"],
                crm_status,
                crm_notes
            )

            st.success(
                "CRM updated"
            )

# =====================================================
# TAB 5 — NETWORK
# =====================================================

with tab5:

    st.subheader(
        "🌐 Offshore Ecosystem Network"
    )

    if st.button(
        "Generate Network Graph"
    ):

        with st.spinner(
            "Building graph..."
        ):

            graph_path = build_network_graph(df)

            with open(
                graph_path,
                "r",
                encoding="utf-8"
            ) as f:

                html_data = f.read()

            components.html(
                html_data,
                height=900,
                scrolling=True
            )