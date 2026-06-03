# =========================================================
# GENDER & DIVERSITY ANALYSIS
# Olympic Analytics Dashboard
# =========================================================

# =========================================================
# 1. LIBRARIES
# =========================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# 2. DATA LOADING
# =========================================================

df = st.session_state["filtered_df"]

# Medal Winners Only
medals = df[df["medal_type"] != "No Medal"]

# =========================================================
# 3. PAGE TITLE
# =========================================================

st.subheader("👥 Gender & Diversity Analysis")

st.markdown(
"""
Comparison of male and female athlete performance,
participation trends and gender diversity across Olympic sports.
"""
)

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 4. KPI SECTION
# =========================================================

male_athletes = df[df["gender"] == "M"].shape[0]

female_athletes = df[df["gender"] == "F"].shape[0]

male_medals = medals[medals["gender"] == "M"].shape[0]

female_medals = medals[medals["gender"] == "F"].shape[0]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Male Athletes",
        male_athletes
    )

with kpi2:
    st.metric(
        "Female Athletes",
        female_athletes
    )

with kpi3:
    st.metric(
        "Male Medals",
        male_medals
    )

with kpi4:
    st.metric(
        "Female Medals",
        female_medals
    )

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 5. MEDAL RATIO + AGE DISTRIBUTION
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# MEDAL RATIO BY GENDER
# =========================================================

with col1:

    st.subheader("🥇 Medal Ratio by Gender")

    gender_counts = (
        medals["gender"]
        .value_counts()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.40)
    )

    ax.axis("equal")

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# AGE DISTRIBUTION BY MEDAL TYPE
# =========================================================

with col2:

    st.subheader("👤 Age Distribution by Medal Type")

    medal_order = [
        "Gold",
        "Silver",
        "Bronze"
    ]

    medal_data = medals[
        medals["medal_type"].isin(
            medal_order
        )
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=medal_data,
        x="medal_type",
        y="age",
        order=medal_order,
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("Age")

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# 6. PARTICIPATION ANALYSIS
# =========================================================

col3, col4 = st.columns(2)

# =========================================================
# PARTICIPATION BY GENDER
# =========================================================

with col3:

    st.subheader("📈 Participation by Gender")

    gender_year = (

        df.groupby(
            ["year", "gender"]
        )

        .size()

        .unstack()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    gender_year.plot(
        ax=ax,
        linewidth=2.5,
        marker="o"
    )

    ax.set_xlabel("Olympic Year")

    ax.set_ylabel(
        "Participations"
    )

    ax.grid(alpha=0.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# SPORT PARTICIPATION BY GENDER
# =========================================================

with col4:

    st.subheader("🏅 Sport Participation by Gender")

    top_sports = (

        df["sport_name"]

        .value_counts()

        .head(10)

        .index
    )

    sport_gender = pd.crosstab(

        df[
            df["sport_name"]
            .isin(top_sports)
        ]["sport_name"],

        df["gender"]
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sport_gender.plot(
        kind="bar",
        stacked=True,
        ax=ax
    )

    ax.set_xlabel("")

    ax.set_ylabel(
        "Participations"
    )

    plt.xticks(rotation=35)

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# 7. AVERAGE AGE + DIVERSITY INSIGHTS
# =========================================================

col5, col6 = st.columns(2)

# =========================================================
# AVERAGE AGE BY GENDER
# =========================================================

with col5:

    st.subheader("📊 Average Age by Gender")

    avg_age_gender = (

        medals.groupby("gender")["age"]

        .mean()

        .round(1)

        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))

    sns.barplot(
        data=avg_age_gender,
        x="gender",
        y="age",
        ax=ax
    )

    ax.set_xlabel("Gender")

    ax.set_ylabel(
        "Average Age"
    )

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# DIVERSITY INSIGHTS
# =========================================================

with col6:

    st.subheader("✨ Diversity Insights")

    st.markdown(
        "<div style='height:40px;'></div>",
        unsafe_allow_html=True
    )

    st.info(
        """
        • Female participation has increased significantly across Olympic history.

        • Gender representation has become more balanced in many sports.

        • Participation growth reflects increasing diversity and inclusiveness.

        • Modern Olympic Games demonstrate stronger global commitment to equal opportunities.
        """
    )