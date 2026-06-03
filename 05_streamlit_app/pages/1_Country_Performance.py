# =========================================================
# COUNTRY PERFORMANCE ANALYSIS
# Olympic Analytics Dashboard
# =========================================================

# =========================================================
# 1. LIBRARIES
# =========================================================

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# =========================================================
# 2. LOAD DATA
# =========================================================

df = st.session_state["filtered_df"]

medals = df[
    df["medal_type"] != "No Medal"
]


# =========================================================
# 3. PAGE HEADER
# =========================================================

st.subheader("🌍 Country Performance Analysis")

st.markdown(
"""
Analysis of Olympic country performance,
medal dominance and sport specialization.
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
        "Countries",
        medals["country_name"].nunique()
    )

with kpi2:

    st.metric(
        "Sports",
        medals["sport_name"].nunique()
    )

with kpi3:

    st.metric(
        "Total Medals",
        medals.shape[0]
    )

with kpi4:

    leading_country = (
        medals["country_name"]
        .value_counts()
        .idxmax()
    )

    st.metric(
        "Leading Country",
        leading_country
    )

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)


# =========================================================
# ROW 1
# COUNTRY RANKING + HEATMAP
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# COUNTRY MEDAL RANKING
# =========================================================

with col1:

    st.subheader("🏅 Country Medal Ranking")

    top_n = st.slider(
        "Top Countries",
        5,
        20,
        10
    )

    country_medals = (

        medals["country_name"]

        .value_counts()

        .head(top_n)

        .sort_values()
    )

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    ax.barh(
        country_medals.index,
        country_medals.values
    )

    ax.set_xlabel(
        "Total Medals"
    )

    ax.grid(
        axis="x",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)


# =========================================================
# COUNTRY VS SPORT HEATMAP
# =========================================================

with col2:

    st.subheader(
        "🔥 Country vs Sport Heatmap"
    )
    st.markdown("<div style='margin-top:90px;'></div>",unsafe_allow_html=True)
    top_countries = (

        medals["country_name"]

        .value_counts()

        .head(top_n)

        .index
    )

    top_sports = (

        medals["sport_name"]

        .value_counts()

        .head(10)

        .index
    )

    heatmap_data = pd.crosstab(

        medals["country_name"],

        medals["sport_name"]
    )

    heatmap_data = heatmap_data.loc[
        top_countries,
        top_sports
    ]

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.heatmap(

        heatmap_data,

        cmap="Blues",

        linewidths=0.5,

        annot=False,

        ax=ax
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.yticks(
        rotation=0
    )

    plt.tight_layout()

    st.pyplot(fig)


# =========================================================
# ROW 2
# WORLD MAP + COUNTRY INSIGHTS
# =========================================================

col3, col4 = st.columns(2)


# =========================================================
# WORLD MAP
# =========================================================

with col3:

    st.subheader(
        "🗺️ Olympic World Map"
    )

    map_df = (

        medals

        .groupby("country_name")

        .size()

        .reset_index(
            name="total_medals"
        )
    )

    fig = px.choropleth(

        map_df,

        locations="country_name",

        locationmode="country names",

        color="total_medals",

        hover_name="country_name",

        color_continuous_scale="Blues"
    )

    # -----------------------------------------------------
    # PROFESSIONELLE FARBSKALA
    # -----------------------------------------------------

    fig.update_layout(

        height=450,

        coloraxis_colorbar=dict(

            title="Total Medals",

            thickness=15,   # Breite der Skala

            len=0.70,       # Höhe der Skala

            y=0.5           # vertikal zentrieren
        ),

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# COUNTRY INSIGHTS SUMMARY
# =========================================================

with col4:

    st.subheader(
        "📝 Country Insights"
    )

    st.markdown("<div style='margin-top:110px;'></div>",unsafe_allow_html=True)

    leading_country = (

        medals["country_name"]

        .value_counts()

        .idxmax()
    )

    leading_country_medals = (

        medals["country_name"]

        .value_counts()

        .max()
    )

    top_sport = (

        medals["sport_name"]

        .value_counts()

        .idxmax()
    )

    st.info(
        f"""
        • **{leading_country}** leads the Olympic medal ranking with
        **{leading_country_medals:,} medals**.

        • **{top_sport}** is the most successful sport category.

        • Olympic medals were won by
        **{medals['country_name'].nunique()} countries**.
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
Country Performance Analysis highlights medal dominance,
country specialization, historical performance trends,
and the global distribution of Olympic success.
"""
)