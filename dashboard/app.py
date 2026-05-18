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
# STYLING
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #07111f;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="metric-container"] {
    background-color: #111c2d;
    border: 1px solid #1e2d45;
    padding: 15px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #111c2d;
    border-radius: 10px;
    padding: 10px 20px;
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

st.success("Dataset loaded successfully")
st.write("TOTAL COMPANIES:", len(df))

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🎯 Filters")

# SEARCH

search = st.sidebar.text_input(
    "Search company"
)

if search:

    df = df[
        df["company"].astype(str).str.contains(
            search,
            case=False,
            na=False
        )
    ]

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
# CHECKBOXES
# =====================================================

offshore_filter = st.sidebar.checkbox(
    "Offshore only"
)

if offshore_filter and "offshore" in df.columns:

    df = df[
        df["offshore"] == True
    ]

floating_filter = st.sidebar.checkbox(
    "Floating Wind only"
)

if floating_filter and "floating_wind" in df.columns:

    df = df[
        df["floating_wind"] == True
    ]

epc_filter = st.sidebar.checkbox(
    "EPC only"
)

if epc_filter and "epc" in df.columns:

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

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Companies",
        len(df)
    )

    hot_count = 0

    if "lead_tier" in df.columns:

        hot_count = len(
            df[df["lead_tier"] == "HOT"]
        )

    col2.metric(
        "HOT Leads",
        hot_count
    )

    strategic_count = 0

    if "strategic_level" in df.columns:

        strategic_count = len(
            df[df["strategic_level"] == "STRATEGIC"]
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

    offshore_count = 0

    if "offshore" in df.columns:

        offshore_count = len(
            df[df["offshore"] == True]
        )

    col4.metric(
        "Offshore",
        offshore_count
    )

    floating_count = 0

    if "floating_wind" in df.columns:

        floating_count = len(
            df[df["floating_wind"] == True]
        )

    col5.metric(
        "Floating",
        floating_count
    )

    # COUNTRY DISTRIBUTION

    if "country" in df.columns:

        st.subheader("🌍 Country Distribution")

        country_chart = px.histogram(
            df,
            x="country"
        )

        st.plotly_chart(
            country_chart,
            use_container_width=True
        )

    # LEAD SCORE

    if "lead_score" in df.columns:

        st.subheader("📈 Lead Score Distribution")

        score_chart = px.histogram(
            df,
            x="lead_score"
        )

        st.plotly_chart(
            score_chart,
            use_container_width=True
        )

    # STRATEGIC SCORE

    if "strategic_score" in df.columns:

        st.subheader("🧠 Strategic Score Distribution")

        strategic_chart = px.histogram(
            df,
            x="strategic_score"
        )

        st.plotly_chart(
            strategic_chart,
            use_container_width=True
        )

    # EXPORT CSV

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="windeurope_filtered.csv",
        mime="text/csv"
    )

# =====================================================
# TAB 2 — INTELLIGENCE
# =====================================================

with tab2:

    st.subheader("🎯 AI Target Recommendations")

    if "strategic_score" in df.columns:

        st.markdown("## 🏆 Top Strategic Companies")

        strategic_df = top_strategic_companies(df)

        st.dataframe(
            strategic_df[
                [
                    "company",
                    "country",
                    "strategic_score",
                    "strategic_level"
                ]
            ],
            use_container_width=True
        )

    if "floating_wind" in df.columns:

        st.markdown("## 🌊 Top Floating Wind Companies")

        floating_df = top_floating_companies(df)

        st.dataframe(
            floating_df[
                [
                    "company",
                    "country",
                    "floating_wind",
                    "strategic_score"
                ]
            ],
            use_container_width=True
        )

    if "epc" in df.columns:

        st.markdown("## 🏗️ Top EPC Companies")

        epc_df = top_epc_companies(df)

        st.dataframe(
            epc_df[
                [
                    "company",
                    "country",
                    "epc",
                    "strategic_score"
                ]
            ],
            use_container_width=True
        )

    if "digitalization" in df.columns:

        st.markdown("## 🤖 Top Digitalization Targets")

        digital_df = top_digitalization_companies(df)

        st.dataframe(
            digital_df[
                [
                    "company",
                    "country",
                    "digitalization",
                    "strategic_score"
                ]
            ],
            use_container_width=True
        )

    # COMPANY SELECTOR

    st.subheader("🤖 AI Sales Strategy Viewer")

    company_selected = st.selectbox(
        "Select company",
        df["company"]
    )

    selected_df = df[
        df["company"] == company_selected
    ]

    if len(selected_df) > 0:

        row = selected_df.iloc[0]

        # PROFILE

        st.subheader("🧠 Company Intelligence Profile")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Company")
            st.write(row.get("company", ""))

            st.markdown("### Country")
            st.write(row.get("country", ""))

            st.markdown("### Segment")
            st.write(row.get("segmento", ""))

            st.markdown("### Strategic Level")
            st.write(row.get("strategic_level", ""))

            st.markdown("### Lead Tier")

            lead_tier = row.get("lead_tier", "")

            if lead_tier == "HOT":

                st.error("🔥 HOT LEAD")

            elif lead_tier == "WARM":

                st.warning("🟠 WARM LEAD")

            else:

                st.success("🟢 LOW / COLD LEAD")

        with col2:

            st.metric(
                "Lead Score",
                row.get("lead_score", 0)
            )

            st.metric(
                "Strategic Score",
                row.get("strategic_score", 0)
            )

            st.write(
                f"🌊 Offshore: {row.get('offshore', False)}"
            )

            st.write(
                f"⚓ Floating Wind: {row.get('floating_wind', False)}"
            )

            st.write(
                f"🏗 EPC: {row.get('epc', False)}"
            )

        # EXECUTIVE SUMMARY

        st.subheader("📋 Executive Summary")

        try:

            summary = generate_executive_summary(row)

            st.write(summary)

        except Exception as e:

            summary = "Executive summary not available"

            st.warning(str(e))

        # PDF REPORT

        st.subheader("📄 Executive Report")

        if st.button("📄 Generate Executive PDF"):

            with st.spinner("Generating executive report..."):

                pdf_path = generate_executive_pdf(
                    row,
                    summary
                )

                with open(pdf_path, "rb") as pdf_file:

                    st.download_button(
                        label="⬇ Download Executive PDF",
                        data=pdf_file,
                        file_name=f"{row['company']}_executive_report.pdf",
                        mime="application/pdf"
                    )

        # WEBSITE

        st.subheader("🌐 Website Intelligence")

        website_text = row.get(
            "website_text",
            ""
        )

        if pd.notna(website_text) and website_text != "":

            st.write(website_text)

        else:

            st.info(
                "No website intelligence available"
            )

        # SALES STRATEGY

        st.subheader("🤖 AI Sales Strategy")

        sales_strategy = row.get(
            "sales_strategy",
            ""
        )

        if pd.notna(sales_strategy) and sales_strategy != "":

            st.write(sales_strategy)

        else:

            st.info(
                "AI sales strategy not generated yet"
            )

        # RELATIONSHIP ANALYSIS

        st.subheader("🔗 Relationship Intelligence")

        try:

            relationship_analysis = (
                generate_relationship_analysis(
                    row["company"],
                    df
                )
            )

            st.write(
                relationship_analysis
            )

        except Exception as e:

            st.warning(
                f"Relationship analysis error: {e}"
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
            "Analyzing market intelligence..."
        ):

            try:

                answer = ask_ai_analyst(
                    question,
                    df
                )

                st.write(answer)

            except Exception as e:

                st.error(str(e))

    # OUTREACH

    st.subheader("📧 AI Outreach Generator")

    if "row" in locals():

        if st.button(
            "Generate Outreach Email"
        ):

            with st.spinner(
                "Generating outreach strategy..."
            ):

                try:

                    outreach_email = (
                        generate_outreach_email(
                            row
                        )
                    )

                    st.write(outreach_email)

                except Exception as e:

                    st.error(str(e))

    # MEETING PREP

    st.subheader(
        "🧠 AI Meeting Preparation"
    )

    if "row" in locals():

        if st.button(
            "Generate Meeting Briefing"
        ):

            with st.spinner(
                "Preparing strategic briefing..."
            ):

                try:

                    meeting_prep = (
                        generate_meeting_prep(
                            row
                        )
                    )

                    st.write(meeting_prep)

                except Exception as e:

                    st.error(str(e))

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

            try:

                save_crm(
                    row["company"],
                    crm_status,
                    crm_notes
                )

                st.success(
                    "CRM updated"
                )

            except Exception as e:

                st.error(str(e))

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
            "Building ecosystem graph..."
        ):

            try:

                graph_path = (
                    build_network_graph(df)
                )

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

            except Exception as e:

                st.error(str(e))