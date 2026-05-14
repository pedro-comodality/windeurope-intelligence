
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)



import pandas as pd
import streamlit as st
import plotly.express as px

from src.profiling.executive_summary import (
    generate_executive_summary
)

from src.profiling.relationship_engine import (
    generate_relationship_analysis
)

import streamlit.components.v1 as components

from src.visualization.network_graph import (
    build_network_graph
)

from src.profiling.recommendation_engine import (
    top_strategic_companies,
    top_floating_companies,
    top_epc_companies,
    top_digitalization_companies,
    top_innovators
)

from src.profiling.chat_analyst import (
    ask_ai_analyst
)


from src.sales.outreach_generator import (
    generate_outreach_email
)


from src.crm.crm_engine import (
    load_crm,
    save_crm
)

from src.sales.meeting_prep import (
    generate_meeting_prep
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="WindEurope Intelligence",
    layout="wide"
)

st.title("🌊 WindEurope 2026 Intelligence Platform")


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
        df["company"].str.contains(
            search,
            case=False,
            na=False
        )
    ]


# =====================================================
# LEAD TIER
# =====================================================

tier_filter = st.sidebar.multiselect(
    "Lead Tier",
    options=df["lead_tier"].unique(),
    default=df["lead_tier"].unique()
)

df = df[
    df["lead_tier"].isin(tier_filter)
]


# =====================================================
# STRATEGIC LEVEL
# =====================================================

strategic_filter = st.sidebar.multiselect(
    "Strategic Level",
    options=df["strategic_level"].unique(),
    default=df["strategic_level"].unique()
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

if offshore_filter:
    df = df[df["offshore"] == True]


floating_filter = st.sidebar.checkbox(
    "Floating Wind only"
)

if floating_filter:
    df = df[df["floating_wind"] == True]


epc_filter = st.sidebar.checkbox(
    "EPC only"
)

if epc_filter:
    df = df[df["epc"] == True]


# =====================================================
# KPIs
# =====================================================

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
    "Strategic",
    len(df[df["strategic_level"] == "STRATEGIC"])
)

col4.metric(
    "Offshore",
    len(df[df["offshore"] == True])
)

col5.metric(
    "Floating",
    len(df[df["floating_wind"] == True])
)

# =====================================================
# AI TARGET RECOMMENDATIONS
# =====================================================

st.subheader("🎯 AI Target Recommendations")


# TOP STRATEGIC

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


# TOP FLOATING

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


# TOP EPC

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


# TOP DIGITALIZATION

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

# =====================================================
# TOP STRATEGIC COMPANIES
# =====================================================

st.subheader("🏆 Top Strategic Companies")

top_df = df.sort_values(
    by="strategic_score",
    ascending=False
)

st.dataframe(
    top_df[
        [
            "company",
            "country",
            "lead_score",
            "lead_tier",
            "strategic_score",
            "strategic_level",
            "offshore",
            "floating_wind",
            "epc"
        ]
    ],
    use_container_width=True
)


# =====================================================
# COUNTRY DISTRIBUTION
# =====================================================

st.subheader("🌍 Country Distribution")

country_chart = px.histogram(
    df,
    x="country"
)

st.plotly_chart(
    country_chart,
    use_container_width=True
)


# =====================================================
# LEAD SCORE DISTRIBUTION
# =====================================================

st.subheader("📈 Lead Score Distribution")

score_chart = px.histogram(
    df,
    x="lead_score"
)

st.plotly_chart(
    score_chart,
    use_container_width=True
)


# =====================================================
# STRATEGIC SCORE DISTRIBUTION
# =====================================================

st.subheader("🧠 Strategic Score Distribution")

strategic_chart = px.histogram(
    df,
    x="strategic_score"
)

st.plotly_chart(
    strategic_chart,
    use_container_width=True
)


# =====================================================
# AI SALES STRATEGY VIEWER
# =====================================================

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

    # =====================================================
    # COMPANY PROFILE
    # =====================================================

    st.subheader("🧠 Company Intelligence Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Company")

        st.write(row["company"])

        st.markdown("### Country")

        st.write(row["country"])

        st.markdown("### Segment")

        st.write(row.get("segmento", ""))

        st.markdown("### Company Type")

        st.write(row.get("tipo_empresa", ""))

        st.markdown("### Strategic Level")

        st.write(row["strategic_level"])

        st.markdown("### Lead Tier")

        st.write(row["lead_tier"])

    with col2:

        st.markdown("### Scores")

        st.metric(
            "Lead Score",
            row["lead_score"]
        )

        st.metric(
            "Strategic Score",
            row["strategic_score"]
        )

        st.markdown("### Offshore")

        st.write(row["offshore"])

        st.markdown("### Floating Wind")

        st.write(row["floating_wind"])

        st.markdown("### EPC")

        st.write(row["epc"])

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    st.subheader("📋 Executive Summary")

    summary = generate_executive_summary(row)

    st.write(summary)

    # =====================================================
    # WEBSITE INTELLIGENCE
    # =====================================================

    st.subheader("🌐 Website Intelligence")

    st.write(
        row.get("website_text", "")
    )

    # =====================================================
    # AI SALES STRATEGY
    # =====================================================

    st.subheader("🤖 AI Sales Strategy")

    st.write(
        row["sales_strategy"]
    )

    # =====================================================
    # RELATIONSHIP INTELLIGENCE
    # =====================================================

    st.subheader("🔗 Relationship Intelligence")

    relationship_analysis = generate_relationship_analysis(
        row["company"],
        df
    )

    st.write(
        relationship_analysis
    )


# =====================================================
# AI CHAT ANALYST
# =====================================================

st.subheader("🧠 AI Market Intelligence Analyst")

question = st.text_input(
    "Ask the AI analyst"
)

if question:

    with st.spinner("Analyzing market intelligence..."):

        answer = ask_ai_analyst(
            question,
            df
        )

        st.write(answer)


# =====================================================
# AI OUTREACH GENERATOR
# =====================================================

st.subheader("📧 AI Outreach Generator")

if st.button("Generate Outreach Email"):

    with st.spinner("Generating outreach strategy..."):

        outreach_email = generate_outreach_email(
            row
        )

        st.write(outreach_email)


# =====================================================
# CRM PANEL
# =====================================================

st.subheader("📌 CRM Management")

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

    st.success("CRM updated")


# =====================================================
# AI MEETING PREP
# =====================================================

st.subheader("🧠 AI Meeting Preparation")

if st.button("Generate Meeting Briefing"):

    with st.spinner("Preparing strategic briefing..."):

        meeting_prep = generate_meeting_prep(
            row
        )

        st.write(meeting_prep)


# =====================================================
# EXPORT CSV
# =====================================================

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="windeurope_filtered.csv",
    mime="text/csv"
)

# =====================================================
# NETWORK GRAPH
# =====================================================

st.subheader("🌐 Offshore Ecosystem Network")

if st.button("Generate Network Graph"):

    with st.spinner("Building ecosystem graph..."):

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