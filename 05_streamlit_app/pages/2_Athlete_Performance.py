# =========================================================
# ATHLETE PERFORMANCE ANALYSIS
# Olympic Analytics Dashboard
# =========================================================

# =========================================================
# 1. LIBRARIES
# =========================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
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

st.subheader("🏃 Athlete Performance Analysis")

st.markdown(
"""
Analysis of athlete profiles, body characteristics,
and performance factors associated with Olympic success.
"""
)

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 4. KPI SECTION
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Average Age",
        round(medals["age"].mean(), 1)
    )

with kpi2:
    st.metric(
        "Average Height",
        f"{round(medals['height_cm'].mean(),1)} cm"
    )

with kpi3:
    st.metric(
        "Average Weight",
        f"{round(medals['weight_kg'].mean(),1)} kg"
    )

with kpi4:
    st.metric(
        "Average BMI",
        round(medals["bmi"].mean(), 1)
    )

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 5. HEIGHT VS WEIGHT + BMI DISTRIBUTION
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# HEIGHT VS WEIGHT ANALYSIS
# =========================================================

with col1:

    st.subheader("📊 Height vs Weight Analysis")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=medals,
        x="height_cm",
        y="weight_kg",
        hue="gender",
        alpha=0.60,
        s=40,
        ax=ax
    )

    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Weight (kg)")

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# BMI DISTRIBUTION
# =========================================================

with col2:

    st.subheader("⚖️ BMI Distribution")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(
        medals["bmi"],
        bins=30,
        kde=True,
        ax=ax
    )

    ax.set_xlabel("BMI")
    ax.set_ylabel("Frequency")

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# SPACING
# =========================================================

st.markdown(
    "<div style='height:10px;'></div>",
    unsafe_allow_html=True
)

# =========================================================
# 6. GENDER COMPARISON + ATHLETE SUMMARY
# =========================================================

col3, col4 = st.columns(2)

# =========================================================
# GENDER COMPARISON
# =========================================================

with col3:

    st.subheader("👥 Gender Comparison")

    gender_profile = (

        medals.groupby("gender")[

            ["height_cm", "weight_kg"]

        ]

        .mean()

        .round(1)
    )

    fig, ax = plt.subplots(figsize=(8, 4.8))

    gender_profile.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Gender")
    ax.set_ylabel("Average Value")

    ax.grid(
        axis="y",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# ATHLETE PERFORMANCE SUMMARY
# =========================================================

with col4:

    st.subheader("📋 Athlete Performance Summary")

    st.markdown(
        "<div style='height:45px;'></div>",
        unsafe_allow_html=True
    )

    st.info(
        """
        • Olympic medalists maintain a relatively stable BMI profile despite differences in height and weight.

        • Male athletes generally show higher average height and weight values than female athletes.

        • Most successful athletes fall within a healthy BMI range.

        • Physical characteristics differ across sports, reflecting specific performance requirements.
        """
    )