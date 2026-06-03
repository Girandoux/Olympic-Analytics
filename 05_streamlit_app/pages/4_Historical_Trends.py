# =========================================================
# HISTORICAL TRENDS ANALYSIS
# Olympic Analytics Dashboard
# =========================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# DATA LOADING
# =========================================================

df = st.session_state["filtered_df"]

medals = df[df["medal_type"] != "No Medal"].copy()

# =========================================================
# PAGE TITLE
# =========================================================

st.subheader("📈 Historical Trends Analysis")

st.markdown(
"""
Analysis of long-term Olympic developments,
including athlete evolution, medal growth,
country dominance and participation trends.
"""
)

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# KPI SECTION
# =========================================================

first_year = int(df["year"].min())
latest_year = int(df["year"].max())

years_covered = latest_year - first_year

total_medals = medals.shape[0]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "First Olympic Year",
        first_year
    )

with kpi2:
    st.metric(
        "Latest Olympic Year",
        latest_year
    )

with kpi3:
    st.metric(
        "Years Covered",
        years_covered
    )

with kpi4:
    st.metric(
        "Total Medals",
        f"{total_medals}"
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
# ATHLETE AGE EVOLUTION
# =========================================================

with col1:

    st.subheader("👤 Athlete Age Evolution")

    age_evolution = (
        df.groupby("year")["age"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        age_evolution["year"],
        age_evolution["age"],
        linewidth=3
    )

    ax.set_xlabel("Olympic Year")
    ax.set_ylabel("Average Age")

    ax.grid(alpha=0.3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# MEDAL GROWTH OVER DECADES
# =========================================================

with col2:

    st.subheader("🏅 Medal Growth Over Decades")

    medals["decade"] = (
        medals["year"] // 10
    ) * 10

    decade_growth = (
        medals.groupby("decade")
        .size()
        .reset_index(name="medals")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.fill_between(
        decade_growth["decade"],
        decade_growth["medals"],
        alpha=0.4
    )

    ax.plot(
        decade_growth["decade"],
        decade_growth["medals"],
        linewidth=3
    )

    ax.set_xlabel("Decade")
    ax.set_ylabel("Total Medals")

    ax.grid(alpha=0.3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# ROW 2
# =========================================================

col3, col4 = st.columns(2)

# =========================================================
# COUNTRY DOMINANCE TIMELINE
# =========================================================

with col3:

    st.subheader("🌍 Country Dominance Timeline")

    top_countries = (
        medals["country_name"]
        .value_counts()
        .head(5)
        .index
    )

    timeline = (
        medals[
            medals["country_name"].isin(top_countries)
        ]
        .groupby(
            ["year", "country_name"]
        )
        .size()
        .unstack(fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    timeline.plot(
        ax=ax,
        linewidth=2.5
    )

    ax.set_xlabel("Olympic Year")
    ax.set_ylabel("Medals Won")

    ax.grid(alpha=0.3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# PARTICIPATION GROWTH
# =========================================================

with col4:

    st.subheader("📊 Olympic Participation Growth")

    participation = (
        df.groupby("year")
        .size()
        .reset_index(name="participants")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.fill_between(
        participation["year"],
        participation["participants"],
        alpha=0.4
    )

    ax.plot(
        participation["year"],
        participation["participants"],
        linewidth=3
    )

    ax.set_xlabel("Olympic Year")
    ax.set_ylabel("Participants")

    ax.grid(alpha=0.3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# HISTORICAL TRENDS SUMMARY
# =========================================================

st.markdown(
    "<div style='height:10px;'></div>",
    unsafe_allow_html=True
)

st.subheader("📋 Historical Trends Summary")

st.info(
    f"""
    • Olympic records span from **{first_year}** to **{latest_year}**.

    • Participation has increased significantly throughout Olympic history.

    • Medal competition expanded as more nations entered the Games.

    • Leading countries maintained strong performance across multiple Olympic eras.

    • Historical trends reveal the continuous evolution of global sports, athlete development and international competitiveness.
    """
)