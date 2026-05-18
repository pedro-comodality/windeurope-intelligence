import streamlit as st
import sys
import os
import yaml
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

from yaml.loader import SafeLoader
from src.intelligence.deal_engine import (
    top_acquisition_targets,
    top_partnership_targets,
    hidden_champions
)
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

from src.reporting.pdf_report import (
    generate_executive_pdf
)

from src.profiling.executive_summary import (
    generate_executive_summary
)

from src.visualization.network_graph import (
    build_network_graph
)

from src.profiling.recommendation_engine import (
    top_strategic_companies
)

from src.profiling.chat_analyst import (
    ask_ai_analyst
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
# SEARCH
# =====================================================

search = st.sidebar.text_input(
    "Search company"
)

if search:

    df = df[
        df["company"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

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

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard",
    "🧠 Intelligence",
    "🤖 AI Analyst",
    "📌 CRM",
    "🌐 Network"
    "🧠 Deal Intelligence"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("📊 Executive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Companies",
        len(df)
    )

    col2.metric(
        "Countries",
        df["country"].nunique()
    )

    col3.metric(
        "Elite",
        len(
            df[
                df["strategic_category_v2"]
                == "ELITE"
            ]
        )
    )

    col4.metric(
        "Strategic",
        len(
            df[
                df["strategic_category_v2"]
                == "STRATEGIC"
            ]
        )
    )

    st.subheader(
        "🌍 Country Distribution"
    )

    country_chart = px.histogram(
        df,
        x="country"
    )

    st.plotly_chart(
        country_chart,
        use_container_width=True
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "🎯 Strategic Intelligence"
    )

    strategic_df = top_strategic_companies(df)

    st.dataframe(
        strategic_df.head(25),
        use_container_width=True
    )

    company_selected = st.selectbox(
        "Select company",
        df["company"]
    )

    selected_df = df[
        df["company"] == company_selected
    ]

    if len(selected_df) > 0:

        row = selected_df.iloc[0]

        st.subheader(
            "🧠 Company Intelligence"
        )

        st.write(row)

        summary = generate_executive_summary(
            row
        )

        st.subheader(
            "📋 Executive Summary"
        )

        st.write(summary)

        if st.button(
            "📄 Generate Executive PDF"
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
                    label="⬇ Download PDF",
                    data=pdf_file,
                    file_name=f"{row['company']}.pdf",
                    mime="application/pdf"
                )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "🤖 AI Market Analyst"
    )

    question = st.text_input(
        "Ask AI"
    )

    if question:

        answer = ask_ai_analyst(
            question,
            df
        )

        st.write(answer)

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader("📌 CRM")

    if "row" in locals():

        crm_status = st.selectbox(
            "Status",
            [
                "Prospect",
                "Contacted",
                "Meeting",
                "Proposal",
                "Partner"
            ]
        )

        crm_notes = st.text_area(
            "Notes"
        )

        if st.button(
            "Save CRM"
        ):

            save_crm(
                row["company"],
                crm_status,
                crm_notes
            )

            st.success(
                "CRM Updated"
            )

# =====================================================
# TAB 5
# =====================================================

with tab5:

    st.subheader(
        "🌐 Ecosystem Network"
    )

    if st.button(
        "Generate Network"
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
        ```python id="y1odqr"

# =====================================================

# TAB 6 — DEAL INTELLIGENCE

# =====================================================

with tab6:

st.subheader(
    "🧠 AI Deal Intelligence Engine"
)

# =================================================
# ACQUISITION TARGETS
# =================================================

st.markdown(
    "## 🏢 Top Acquisition Targets"
)

acquisition_df = top_acquisition_targets(df)

st.dataframe(

    acquisition_df[
        [
            "company",
            "country",
            "deal_score",
            "final_strategic_score"
        ]
    ],

    use_container_width=True
)

# =================================================
# PARTNERSHIP TARGETS
# =================================================

st.markdown(
    "## 🤝 Strategic Partnership Targets"
)

partnership_df = top_partnership_targets(df)

st.dataframe(

    partnership_df[
        [
            "company",
            "country",
            "partnership_rank",
            "partnership_score"
        ]
    ],

    use_container_width=True
)

# =================================================
# HIDDEN CHAMPIONS
# =================================================

st.markdown(
    "## 🚀 Hidden Champions"
)

hidden_df = hidden_champions(df)

st.dataframe(

    hidden_df[
        [
            "company",
            "country",
            "final_strategic_score",
            "strategic_category_v2"
        ]
    ],

    use_container_width=True
)