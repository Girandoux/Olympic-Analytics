# =========================================================
# PROJECT INSIGHTS & CONCLUSIONS
# Olympic Analytics Dashboard
# =========================================================


# =========================================================
# 1. BIBLIOTHEKEN
# =========================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd


# =========================================================
# 2. DATEN LADEN
# =========================================================

df = st.session_state["filtered_df"]

medals = df[df["medal_type"] != "No Medal"]


# =========================================================
# 3. TITEL
# =========================================================

st.subheader("📖 Project Insights & Conclusions")

st.markdown(
"""
Final summary of key findings, business insights,
project outcomes and future development opportunities.
"""
)

st.markdown(
    "<hr style='margin:4px 0;'>",
    unsafe_allow_html=True
)


# =========================================================
# 4. KPI SECTION
# =========================================================

total_athletes = len(df)

total_medals = len(medals)

countries = df["country_name"].nunique()

sports = df["sport_name"].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Athletes",
        f"{total_athletes}"
    )

with kpi2:
    st.metric(
        "Medals",
        f"{total_medals}"
    )

with kpi3:
    st.metric(
        "Countries",
        countries
    )

with kpi4:
    st.metric(
        "Sports",
        sports
    )


# =========================================================
# SPACE
# =========================================================

st.markdown(
    "<div style='height:15px;'></div>",
    unsafe_allow_html=True
)


# =========================================================
# KEY FINDINGS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏅 Key Findings")

    st.info(
        """
        • Olympic participation increased significantly over time.

        • Medal competition became more global and competitive.

        • A small number of countries consistently dominated medal rankings.

        • Athlete performance patterns vary across sports.

        • Historical trends reveal strong long-term growth in participation.
        """
    )


with col2:

    st.subheader("👥 Diversity Findings")

    st.info(
        """
        • Female participation has grown steadily.

        • Gender representation became more balanced.

        • More sports now show similar participation levels.

        • Medal distribution between genders is increasingly equal.

        • Modern Olympic Games demonstrate stronger inclusivity.
        """
    )


# =========================================================
# SPACE
# =========================================================

st.markdown(
    "<div style='height:15px;'></div>",
    unsafe_allow_html=True
)


# =========================================================
# PROJECT ACHIEVEMENTS
# =========================================================

col3, col4 = st.columns(2)

with col3:

    st.subheader("🚀 Project Achievements")

    st.success(
        """
        ✔ Data Cleaning & Preparation

        ✔ Exploratory Data Analysis

        ✔ Olympic Historical Trend Analysis

        ✔ Country Performance Evaluation

        ✔ Athlete Performance Analysis

        ✔ Gender & Diversity Analysis

        ✔ Machine Learning Medal Prediction

        ✔ Interactive Streamlit Dashboard
        """
    )


with col4:

    st.subheader("🛠 Technologies Used")

    st.success(
        """
        • Python

        • Pandas

        • NumPy

        • Matplotlib

        • Seaborn

        • Scikit-Learn

        • Streamlit

        • SQL

        • Git & GitHub
        """
    )


# =========================================================
# SPACE
# =========================================================

st.markdown(
    "<div style='height:15px;'></div>",
    unsafe_allow_html=True
)


# =========================================================
# BUSINESS VALUE + FUTURE IMPROVEMENTS
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# BUSINESS VALUE
# =========================================================

with col1:

    st.subheader("💡 Business Value")

    st.info(
        """
        This project demonstrates how data analytics and machine learning
        can transform large historical datasets into actionable insights.

        The platform enables users to:

        • Explore Olympic performance trends

        • Identify successful countries and sports

        • Analyze athlete characteristics

        • Evaluate gender diversity developments

        • Generate medal probability predictions

        • Support data-driven decision making
        """
    )

# =========================================================
# FUTURE IMPROVEMENTS
# =========================================================

with col2:

    st.subheader("🔮 Future Improvements")

    st.info(
        """
        • Advanced Machine Learning algorithms

        • Country-level medal forecasting

        • Real-time Olympic data integration

        • Enhanced athlete performance analytics

        • Interactive geographical dashboards

        • Cloud deployment and automated updates
        """
    )


# =========================================================
# FINAL CONCLUSION
# =========================================================

st.subheader("📌 Final Conclusion")

st.success(
    """
    Olympic Analytics combines Data Engineering,
    SQL Analytics, Power BI, Machine Learning,
    and Streamlit into a complete end-to-end analytics solution.

    The project demonstrates how historical Olympic data
    can be transformed into meaningful insights, interactive dashboards,
    and predictive models, showcasing practical Data Analytics,
    Business Intelligence, and Machine Learning capabilities.
    """
)