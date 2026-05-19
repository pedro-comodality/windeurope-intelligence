import streamlit as st
import plotly.express as px

def render_dashboard(df):

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