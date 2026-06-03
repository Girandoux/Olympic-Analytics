# =========================================================
# EXECUTIVE OVERVIEW
# Olympic Analytics Platform
# =========================================================

import streamlit as st
import matplotlib.pyplot as plt

# =========================================================
# DATA LOADING
# =========================================================

df = st.session_state["filtered_df"]

medals = df[df["medal_type"] != "No Medal"]

# =========================================================
# PAGE TITLE
# =========================================================

st.subheader("📊 Executive Overview")

st.markdown(
"""
Overview of key Olympic trends,
medal performance and global competitiveness.
"""
)

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# KPI SECTION
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Athletes",
        df["athlete_id"].nunique()
    )

with kpi2:
    st.metric(
        "Total Medals",
        medals.shape[0]
    )

with kpi3:
    st.metric(
        "Countries",
        df["country_name"].nunique()
    )

with kpi4:
    st.metric(
        "Sports",
        df["sport_name"].nunique()
    )

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# ROW 1
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# MEDALS OVER TIME
# =========================================================

with col1:

    st.subheader("🏅 Medals Over Time")

    medals_year = (
        medals
        .groupby("year")
        .size()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        medals_year.index,
        medals_year.values,
        linewidth=3
    )

    ax.set_xlabel("Olympic Year")
    ax.set_ylabel("Total Medals")

    ax.grid(alpha=0.3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# TOP COUNTRIES
# =========================================================

with col2:

    st.subheader("🌍 Top 10 Countries")

    top_countries = (
        medals["country_name"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        top_countries.index,
        top_countries.values
    )

    ax.set_xlabel("Total Medals")

    ax.grid(
        axis="x",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# ROW 2
# =========================================================

col3, col4 = st.columns(2)

# =========================================================
# MEDAL TYPE DISTRIBUTION
# =========================================================

with col3:

    st.subheader("🏅 Medal Type Distribution")

    medal_distribution = (
        medals["medal_type"]
        .value_counts()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.pie(
        medal_distribution.values,
        labels=medal_distribution.index,
        autopct="%1.1f%%",
        startangle=90
    )

    centre_circle = plt.Circle(
        (0, 0),
        0.55,
        fc="white"
    )

    fig.gca().add_artist(
        centre_circle
    )

    ax.axis("equal")

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

with col4:

    st.subheader("📝 Executive Summary")

    st.markdown(
        "<div style='height:45px;'></div>",
        unsafe_allow_html=True
    )

    top_country = (
        medals["country_name"]
        .value_counts()
        .idxmax()
    )

    top_country_medals = (
        medals["country_name"]
        .value_counts()
        .max()
    )

    first_year = int(df["year"].min())

    last_year = int(df["year"].max())

    st.info(
        f"""
        • Olympic data covers the period from
        **{first_year} to {last_year}**.

        • A total of **{medals.shape[0]} medals**
        are included in the dataset.

        • **{top_country}** leads the ranking with
        **{top_country_medals:,} medals**.

        • Gold, Silver and Bronze medals show a
        balanced distribution across Olympic history.
        """
    )

# =========================================================
# FOOTER SUMMARY
# =========================================================

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

st.caption(
"""
Executive Overview provides a high-level summary of Olympic
performance, medal trends, leading countries and medal
distribution across the Olympic Games.
"""
)