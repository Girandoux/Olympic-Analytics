# =========================================================
# OLYMPIC MEDAL PREDICTION
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
import plotly.express as px
import joblib

# =========================================================
# 2. DATA LOADING
# =========================================================

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


@st.cache_data
def load_ml_data():

    return pd.read_csv(

        BASE_DIR / "data" / "olympics_ML_cleaned.csv"
    )


@st.cache_data
def load_future_predictions():

    return pd.read_parquet(

        BASE_DIR / "data" / "future_olympic_predictions.parquet"
    )


df_ml = load_ml_data()

future_df = load_future_predictions()

df = st.session_state["filtered_df"]

# =========================================================
# 3. LOAD MODEL
# =========================================================

model = joblib.load(

    BASE_DIR / "models" / "olympic_medal_model.pkl"
)

# =========================================================
# 4. PAGE TITLE
# =========================================================

st.subheader("🤖 Olympic Medal Prediction")

st.markdown(
"""
Interactive machine learning model for estimating
Olympic medal probabilities based on athlete
characteristics and historical Olympic data.
"""
)

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 5. PREDICTION OVERVIEW
# =========================================================

st.subheader("📊 Prediction Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.metric(
        "Predictions",
        f"{len(future_df):,}"
    )

with kpi2:

    st.metric(
        "Countries",
        future_df["country_name"].nunique()
    )

with kpi3:

    st.metric(
        "Sports",
        future_df["sport_name"].nunique()
    )

with kpi4:

    st.metric(
        "Avg Probability",
        f"{future_df['medal_probability'].mean()*100:.1f}%"
    )

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 6. ATHLETE PREDICTION TOOL
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏃 Athlete Information")

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=60,
            value=24
        )

        height = st.number_input(
            "Height (cm)",
            min_value=120,
            max_value=230,
            value=180
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=35,
            max_value=220,
            value=75
        )

        gender = st.selectbox(
            "Gender",
            ["M", "F"]
        )

    with input_col2:

        year = st.selectbox(
            "Olympic Year",
            list(range(2000, 2040, 4)),
            index=4
        )

        sport = st.selectbox(
            "Sport",
            sorted(df["sport_name"].dropna().unique())
        )

        country = st.selectbox(
            "Country",
            sorted(df["country_name"].dropna().unique())
        )

        bmi = weight / ((height / 100) ** 2)

        st.metric(
            "Calculated BMI",
            round(bmi, 2)
        )

    predict_button = st.button(
        "🎯 Predict Medal Probability",
        use_container_width=True
    )

# =========================================================
# 7. PREDICTION RESULTS
# =========================================================

with col2:

    st.subheader("🎯 Prediction Results")

    if predict_button:

        new_athlete = pd.DataFrame({

            "age": [age],
            "height_cm": [height],
            "weight_kg": [weight],
            "bmi": [bmi],
            "gender": [gender],
            "sport_name": [sport],
            "country_name": [country],
            "year": [year]

        })

        probability = (
            model.predict_proba(new_athlete)[0][1]
        )

        probability_percent = round(
            probability * 100,
            2
        )

        confidence = round(
            abs(probability - 0.5) * 200,
            2
        )

        if probability_percent >= 70:
            prediction_text = "High Medal Chance"

        elif probability_percent >= 40:
            prediction_text = "Medium Medal Chance"

        else:
            prediction_text = "Low Medal Chance"

        k1, k2, k3 = st.columns(3)

        k1.metric(
            "Probability",
            f"{probability_percent}%"
        )

        k2.metric(
            "Confidence",
            f"{confidence}%"
        )

        k3.metric(
            "Prediction",
            prediction_text
        )

        fig, ax = plt.subplots(
            figsize=(8, 2.5)
        )

        ax.barh(
            ["Medal Probability"],
            [probability_percent]
        )

        ax.set_xlim(0, 100)

        ax.set_xlabel(
            "Probability (%)"
        )

        ax.grid(alpha=0.2)

        st.pyplot(fig)

    else:

        st.info(
            "Enter athlete information and generate a prediction."
        )
####
# =========================================================
# FUTURE OLYMPIC PREDICTIONS
# =========================================================

st.markdown(
    "<hr style='margin:5px 0;'>",
    unsafe_allow_html=True
)

st.subheader("🔮 Future Olympic Predictions")

# =========================================================
# TOP COUNTRIES
# =========================================================

st.subheader("📊 Top 10 Future Olympic Countries")

top_countries = (

    future_df

    .groupby("country_name")["medal_probability"]

    .mean()

    .sort_values(ascending=False)

    .head(10)

    .reset_index()
)

fig = px.bar(

    top_countries,

    x="medal_probability",

    y="country_name",

    orientation="h",

    color="medal_probability",

    color_continuous_scale="Blues"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# FUTURE FORECAST & PROBABILITY DISTRIBUTION
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# FUTURE MEDAL FORECAST
# =========================================================

with col1:

    st.subheader("📈 Future Medal Forecast")

    forecast = (

        future_df

        .groupby("year")["medal_probability"]

        .mean()

        .reset_index()
    )

    fig = px.line(

        forecast,

        x="year",

        y="medal_probability",

        markers=True,

        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(

        xaxis_title="Olympic Year",

        yaxis_title="Average Medal Probability",

        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# MEDAL PROBABILITY DISTRIBUTION
# =========================================================

with col2:

    st.subheader("🎯 Medal Probability Distribution")

    fig = px.histogram(

        future_df,

        x="medal_probability",

        nbins=30,

        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(

        xaxis_title="Medal Probability",

        yaxis_title="Number of Predictions",

        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# COUNTRY SPORT DOMINANCE
# =========================================================

st.subheader("🔥 Country-Sport Dominance")

top15 = (

    future_df

    .groupby("country_name")

    ["medal_probability"]

    .mean()

    .sort_values(ascending=False)

    .head(15)

    .index
)

heatmap_df = (

    future_df[
        future_df["country_name"].isin(top15)
    ]
)

pivot = (

    heatmap_df

    .groupby(
        ["country_name", "sport_name"]
    )["medal_probability"]

    .mean()

    .reset_index()

    .pivot(
        index="country_name",
        columns="sport_name",
        values="medal_probability"
    )
)

fig = px.imshow(

    pivot,

    aspect="auto",

    color_continuous_scale="Blues"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)
################################
# =========================================================
# INSIGHTS SECTION
# =========================================================

col1, col2, col3 = st.columns([1.2, 1, 1])

# =========================================================
# MACHINE LEARNING INSIGHTS
# =========================================================

with col1:

    st.subheader("🧠 Machine Learning Insights")

    st.info(
        """
        Random Forest was used to predict Olympic medal probabilities.

        Main prediction factors:

        • Age

        • Height

        • Weight

        • BMI

        • Gender

        • Sport

        • Country

        • Olympic Year

        Predictions represent probabilities rather than guaranteed outcomes.
        """
    )

# =========================================================
# BUSINESS VALUE
# =========================================================

with col2:

    st.subheader("💡 Business Value")

    st.info(
        """
        • Identify high-potential Olympic countries

        • Detect strong sports disciplines

        • Support strategic investment decisions

        • Demonstrate predictive analytics capabilities

        • Forecast future Olympic performance trends
        """
    )

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

with col3:

    st.subheader("📌 Executive Summary")

    top_country = (

        future_df

        .groupby("country_name")

        ["medal_probability"]

        .mean()

        .idxmax()
    )

    avg_prob = (
        future_df["medal_probability"].mean() * 100
    )

    st.success(
        f"""
        Highest predicted country:

        • {top_country}

        Average medal probability:

        • {avg_prob:.1f}%

        Forecast horizon:

        • 2028–2036

        Demonstrates practical machine learning
        and predictive analytics capabilities.
        """
    )