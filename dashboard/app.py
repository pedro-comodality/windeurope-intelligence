import os
import sys
import yaml
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

from yaml.loader import SafeLoader

# =========================================================
# PATH FIX
# =========================================================

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# =========================================================
# IMPORTS
# =========================================================

from src.visualization.network_graph import (
    build_network_graph
)

from src.crm.watchlist_engine import (
    add_to_watchlist
)

from src.intelligence.deal_engine import (
    top_acquisition_targets,
    top_partnership_targets,
    hidden_champions,
    top_logistics_targets
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="WindEurope Intelligence",
    layout="wide"
)

# =========================================================
# LOAD AUTH CONFIG
# =========================================================

with open("config.yaml") as file:

    config = yaml.load(
        file,
        Loader=SafeLoader
    )

# =========================================================
# AUTHENTICATION
# =========================================================

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

authenticator.login()

# =========================================================
# LOGIN STATUS
# =========================================================

if st.session_state["authentication_status"] is False:

    st.error("Username/password incorrect")

elif st.session_state["authentication_status"] is None:

    st.warning("Please enter username and password")

elif st.session_state["authentication_status"]:

    # =====================================================
    # LOGOUT
    # =====================================================

    st.sidebar.success(
        f"Welcome {st.session_state['name']}"
    )

    authenticator.logout(
        "Logout",
        "sidebar"
    )

    # =====================================================
    # LOAD DATA
    # =====================================================

    DATA_PATH = (
        "data/exports/windeurope_ai_v3.xlsx"
    )

    df = pd.read_excel(DATA_PATH)

    # =====================================================
    # SAFE DATAFRAME
    # =====================================================

    df.columns = df.columns.astype(str)

    for col in df.columns:

        try:
            df[col] = df[col].astype(str)

        except:
            pass

    # =====================================================
    # SIDEBAR FILTERS
    # =====================================================

    st.sidebar.markdown("## 🎯 Filters")

    search_company = st.sidebar.text_input(
        "Search company"
    )

    countries = sorted(

        df["country"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()

    )

    selected_countries = st.sidebar.multiselect(
        "🌍 Countries",
        countries
    )

    # =====================================================
    # TOP FILTER
    # =====================================================

    top_n = st.sidebar.selectbox(
        "🏆 Top Companies",
        [25, 50, 100, "All"],
        index=1
    )

    # =====================================================
    # FILTER DATA
    # =====================================================

    filtered_df = df.copy()

    # COUNTRY FILTER

    if selected_countries:

        filtered_df = filtered_df[
            filtered_df["country"].isin(
                selected_countries
            )
        ]

    # SEARCH FILTER

    if search_company:

        filtered_df = filtered_df[

            filtered_df["company"]
            .astype(str)
            .str.contains(
                search_company,
                case=False,
                na=False
            )
        ]

    # TOP FILTER

    if top_n != "All":

        if (
            "final_strategic_score"
            in filtered_df.columns
        ):

            filtered_df[
                "final_strategic_score"
            ] = pd.to_numeric(

                filtered_df[
                    "final_strategic_score"
                ],

                errors="coerce"

            ).fillna(0)

            filtered_df = filtered_df.sort_values(

                by="final_strategic_score",

                ascending=False

            ).head(int(top_n))

    # =====================================================
    # HEADER
    # =====================================================

    st.title(
        "🌊 WindEurope 2026 Intelligence Platform"
    )

    st.caption(
        "AI-powered offshore wind ecosystem intelligence platform"
    )

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([

        "📊 Dashboard",

        "🧠 Intelligence",

        "🤖 AI Analyst",

        "📌 CRM",

        "🌐 Network",

        "🧠 Deal Intelligence",

        "⭐ Watchlist"

    ])

    # =====================================================
    # TAB 1 — DASHBOARD
    # =====================================================

    with tab1:

        st.subheader(
            "📊 Executive Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Companies",
            len(filtered_df)
        )

        col2.metric(
            "Countries",
            filtered_df["country"].nunique()
        )

        if "offshore" in filtered_df.columns:

            offshore_count = (

                filtered_df["offshore"]
                .astype(str)
                .str.lower()
                .isin(["true", "1", "yes"])

            ).sum()

        else:
            offshore_count = 0

        col3.metric(
            "Offshore Players",
            offshore_count
        )

        if (
            "final_strategic_score"
            in filtered_df.columns
        ):

            filtered_df[
                "final_strategic_score"
            ] = pd.to_numeric(

                filtered_df[
                    "final_strategic_score"
                ],

                errors="coerce"

            ).fillna(0)

            avg_score = round(

                filtered_df[
                    "final_strategic_score"
                ].mean(),

                1
            )

        else:
            avg_score = 0

        col4.metric(
            "Avg Strategic Score",
            avg_score
        )

        # COUNTRY CHART

        country_chart = (

            filtered_df["country"]
            .value_counts()
            .head(15)
            .reset_index()

        )

        country_chart.columns = [
            "Country",
            "Companies"
        ]

        fig = px.bar(
            country_chart,
            x="Country",
            y="Companies",
            title="Top Countries"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # TAB 2 — INTELLIGENCE
    # =====================================================

    with tab2:

        st.subheader(
            "🧠 Strategic Intelligence"
        )

        st.dataframe(
            filtered_df.head(100),
            use_container_width=True
        )

    # =====================================================
    # TAB 3 — AI ANALYST
    # =====================================================

    with tab3:

        st.subheader(
            "🤖 AI Analyst"
        )

        st.info(
            "AI analysis engine ready."
        )

    # =====================================================
    # TAB 4 — CRM
    # =====================================================

    with tab4:

        st.subheader(
            "📌 CRM Watchlist"
        )

        selected_company = st.selectbox(
            "Select company",
            filtered_df["company"]
            .astype(str)
            .unique()
        )

        if st.button(
            "Add to Watchlist"
        ):

            add_to_watchlist(
                selected_company
            )

            st.success(
                f"{selected_company} added"
            )

    # =====================================================
    # TAB 5 — NETWORK
    # =====================================================

    with tab5:

        st.subheader(
            "🌐 Ecosystem Network"
        )

        st.write(
            f"ROWS: {len(filtered_df)}"
        )

        if st.button(
            "Generate Network"
        ):

            html_data = build_network_graph(
                filtered_df
            )

            components.html(
                html_data,
                height=1000,
                scrolling=True
            )

    # =====================================================
    # TAB 6 — DEAL INTELLIGENCE
    # =====================================================

    with tab6:

        st.subheader(
            "🧠 AI Deal Intelligence Engine"
        )

        # ACQUISITIONS

        st.markdown(
            "### 🏢 Top Acquisition Targets"
        )

        acquisition_df = (
            top_acquisition_targets(
                filtered_df
            )
        )

        st.dataframe(
            acquisition_df,
            use_container_width=True
        )

        # PARTNERSHIPS

        st.markdown(
            "### 🤝 Top Partnership Targets"
        )

        partnership_df = (
            top_partnership_targets(
                filtered_df
            )
        )

        st.dataframe(
            partnership_df,
            use_container_width=True
        )

        # HIDDEN CHAMPIONS

        st.markdown(
            "### ⭐ Hidden Champions"
        )

        hidden_df = hidden_champions(
            filtered_df
        )

        st.dataframe(
            hidden_df,
            use_container_width=True
        )

        # LOGISTICS TARGETS

        st.markdown(
            "### 🚢 Logistics Targets"
        )

        logistics_df = (
            top_logistics_targets(
                filtered_df
            )
        )

        st.dataframe(
            logistics_df,
            use_container_width=True
        )

    # =====================================================
    # TAB 7 — WATCHLIST
    # =====================================================

    with tab7:

        st.subheader(
            "⭐ Strategic Watchlist"
        )

        st.info(
            "Watchlist module connected."
        )