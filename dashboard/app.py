```python
import streamlit as st
import sys
import os
import yaml
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

from yaml.loader import SafeLoader

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

from src.crm.watchlist_engine import (
    load_watchlist,
    add_to_watchlist
)

from src.intelligence.deal_engine import (
    top_acquisition_targets,
    top_partnership_targets,
    hidden_champions,
    top_logistics_targets
)

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
# CLEAN + NORMALIZE
# =====================================================

df = df.fillna("")

# remove duplicated columns
df = df.loc[
    :,
    ~df.columns.duplicated()
]

# convert ALL object/bool columns to string
for col in df.columns:

    try:

        if (
            df[col].dtype == "object"
            or
            df[col].dtype == "bool"
        ):

            df[col] = (
                df[col]
                .astype(str)
            )

    except:

        df[col] = (
            df[col]
            .astype(str)
        )

# =====================================================
# CLEAN COUNTRY
# =====================================================

if "country" in df.columns:

    df["country"] = (

        df["country"]

        .astype(str)

        .str.replace(
            r"Powered by TCPDF.*",
            "",
            regex=True
        )

        .str.replace(
            r"\d+\s*/\s*\d+",
            "",
            regex=True
        )

        .str.replace(
            r"\d+",
            "",
            regex=True
        )

        .str.replace(
            r"[/()-]",
            "",
            regex=True
        )

        .str.replace(
            r"\s+",
            " ",
            regex=True
        )

        .str.strip()
    )

    df = df[
        df["country"] != ""
    ]

# =====================================================
# ADVANCED SCORING
# =====================================================

df = calculate_advanced_scores(df)

# =====================================================
# FINAL SAFE CONVERSION
# =====================================================

for col in df.columns:

    try:

        df[col] = (
            df[col]
            .astype(str)
        )

    except:

        pass

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

        default=country_values[:5]
    )

    if selected_countries:

        df = df[
            df["country"]
            .isin(selected_countries)
        ]

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([

    "📊 Dashboard",

    "🧠 Intelligence",

    "🤖 AI Analyst",

    "📌 CRM",

    "🌐 Network",

    "🧠 Deal Intelligence",

    "⭐ Watchlist",

    "🚢 Logistics Intelligence"
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
        width="stretch"
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "🎯 Strategic Intelligence"
    )

    strategic_df = (
        top_strategic_companies(df)
        .astype(str)
    )

    st.dataframe(
        strategic_df.head(25),
        width="stretch"
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

        st.json(
            row.astype(str).to_dict()
        )

        summary = generate_executive_summary(
            row
        )

        st.subheader(
            "📋 Executive Summary"
        )

        st.write(summary)

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
# TAB 5 — NETWORK
# =====================================================

with tab5:

    st.subheader(
        "🌐 Ecosystem Network"
    )

    st.write(
        f"ROWS: {len(df)}"
    )

    if st.button(
        "Generate Network"
    ):

        try:

            html_data = build_network_graph(df)

            components.html(
                html_data,
                height=1000,
                scrolling=True
            )

        except Exception as e:

            st.error(
                f"NETWORK ERROR: {e}"
            )

# =====================================================
# TAB 6 — DEAL INTELLIGENCE
# =====================================================

with tab6:

    st.subheader(
        "🧠 AI Deal Intelligence Engine"
    )

    st.markdown(
        "## 🏢 Top Acquisition Targets"
    )

    acquisition_df = (
        top_acquisition_targets(df)
        .astype(str)
    )

    st.dataframe(

        acquisition_df[
            [
                "company",
                "country",
                "deal_score",
                "final_strategic_score"
            ]
        ],

        width="stretch"
    )

    st.markdown(
        "## 🤝 Strategic Partnership Targets"
    )

    partnership_df = (
        top_partnership_targets(df)
        .astype(str)
    )

    st.dataframe(

        partnership_df[
            [
                "company",
                "country",
                "partnership_rank",
                "partnership_score"
            ]
        ],

        width="stretch"
    )

    st.markdown(
        "## 🚀 Hidden Champions"
    )

    hidden_df = (
        hidden_champions(df)
        .astype(str)
    )

    st.dataframe(

        hidden_df[
            [
                "company",
                "country",
                "final_strategic_score",
                "strategic_category_v2"
            ]
        ],

        width="stretch"
    )

# =====================================================
# TAB 7 — WATCHLIST
# =====================================================

with tab7:

    st.subheader(
        "⭐ Strategic Watchlist"
    )

    if "row" in locals():

        watchlist_status = st.selectbox(
            "Watchlist Status",
            [
                "Target",
                "Partner",
                "Supplier",
                "Monitor",
                "Competitor"
            ]
        )

        watchlist_notes = st.text_area(
            "Watchlist Notes"
        )

        if st.button(
            "➕ Add To Watchlist"
        ):

            add_to_watchlist(
                row["company"],
                row["country"],
                watchlist_status,
                watchlist_notes
            )

            st.success(
                "Added to watchlist"
            )

    st.markdown(
        "## 📋 Current Watchlist"
    )

    watchlist_df = (
        load_watchlist()
        .astype(str)
    )

    st.dataframe(
        watchlist_df,
        width="stretch"
    )

# =====================================================
# TAB 8 — LOGISTICS INTELLIGENCE
# =====================================================

with tab8:

    st.subheader(
        "🚢 Logistics Intelligence Engine"
    )

    st.markdown(
        """
        AI-powered logistics opportunity
        detection across offshore wind ecosystem.
        """
    )

    logistics_df = (
        top_logistics_targets(df)
        .astype(str)
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Targets",
        len(logistics_df)
    )

    col2.metric(
        "Mega Targets",
        len(
            logistics_df[
                logistics_df[
                    "logistics_priority"
                ] == "MEGA TARGET"
            ]
        )
    )

    col3.metric(
        "High Priority",
        len(
            logistics_df[
                logistics_df[
                    "logistics_priority"
                ] == "HIGH PRIORITY"
            ]
        )
    )

    st.markdown(
        "## 🎯 Top Logistics Targets"
    )

    st.dataframe(

        logistics_df[
            [
                "company",
                "country",
                "segmento",
                "logistics_opportunity_score",
                "logistics_priority",
                "final_strategic_score"
            ]
        ],

        width="stretch"
    )

    st.markdown(
        "## 🏆 Best Opportunity"
    )

    if len(logistics_df) > 0:

        top_target = logistics_df.iloc[0]

        st.success(
            f"""
            TOP TARGET:
            {top_target['company']}

            Logistics Score:
            {top_target['logistics_opportunity_score']}
            """
        )

        st.json(
            top_target.to_dict()
        )
```
