# =========================================================
# OLYMPIC ANALYTICS
# STREAMLIT MAIN APPLICATION
# =========================================================

# Projekt:
# Interaktive Data Science Plattform
# für Olympische Spiele Analytics
#
# Technologien:
# - Streamlit
# - Machine Learning
# - Python
# - Matplotlib
# - Seaborn
#
# Ziel:
# Analyse historischer Olympischer Daten,
# interaktive Dashboards und Machine Learning
# zur Unterstützung datengetriebener Erkenntnisse.
#
# =========================================================

# =========================================================
# 1. BIBLIOTHEKEN IMPORTIEREN
# =========================================================

import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# 2. STREAMLIT KONFIGURATION
# =========================================================

st.set_page_config(

    page_title="Olympic Analytics",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 3. DATEN LADEN
# =========================================================

@st.cache_data
def load_data():

    current_dir = Path(__file__).parent

    csv_path = current_dir / "data" / "olympics_BI_cleaned.csv"

    return pd.read_csv(csv_path)

df = load_data()

# =========================================================
# 4. TITELBEREICH
# =========================================================

st.header("🏅 Olympic Analytics Platform")

st.markdown(
"""
#### Data Science • Machine Learning • Olympic Performance Analytics

Analyse historischer Olympischer Daten mit Python, SQL,
Power BI, Streamlit und Machine Learning.
"""
)

st.markdown(
    "<hr style='margin:3px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 5. SIDEBAR
# =========================================================

st.sidebar.subheader("🏅 Olympic Data Platform")

st.sidebar.caption(
    "Interactive Olympic Analytics Dashboard"
)

st.sidebar.markdown(
    "<hr style='margin:3px 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# 6. FILTER
# =========================================================

st.sidebar.subheader("🎛️ Global Filters")

# =========================================================
# YEAR FILTER
# =========================================================

year_range = st.sidebar.slider(

    "Olympic Year",

    int(df["year"].min()),

    int(df["year"].max()),

    (
        int(df["year"].min()),
        int(df["year"].max())
    )
)

# =========================================================
# GENDER FILTER
# =========================================================

gender_options = (
    ["All"]
    +
    sorted(
        df["gender"]
        .dropna()
        .unique()
        .tolist()
    )
)

gender_selected = st.sidebar.multiselect(

    "Gender",

    gender_options,

    default=["All"]
)

if "All" in gender_selected:

    gender_filter = df["gender"].unique()

else:

    gender_filter = gender_selected

# =========================================================
# SPORT FILTER
# =========================================================

options = (
    ["All"]
    +
    sorted(
        df["sport_name"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected = st.sidebar.multiselect(

    "Sport",

    options,

    default=["All"]
)

if "All" in selected:

    sport_filter = df["sport_name"].unique()

else:

    sport_filter = selected

# =========================================================
# COUNTRY FILTER
# =========================================================

options = (
    ["All"]
    +
    sorted(
        df["country_name"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected = st.sidebar.multiselect(

    "Country",

    options,

    default=["All"]
)

if "All" in selected:

    country_filter = df["country_name"].unique()

else:

    country_filter = selected

# =========================================================
# 7. DATEN FILTERN
# =========================================================

filtered_df = df[

    (df["year"].between(
        year_range[0],
        year_range[1]
    ))
    &
    (df["gender"].isin(gender_filter))
    &
    (df["sport_name"].isin(sport_filter))
    &
    (df["country_name"].isin(country_filter))
]

# =========================================================
# 8. SESSION STATE
# =========================================================

st.session_state["filtered_df"] = filtered_df

# =========================================================
# 9. SIDEBAR AUTHOR
# =========================================================

st.sidebar.markdown(
    "<hr style='margin:3px 0;'>",
    unsafe_allow_html=True
)

st.sidebar.subheader("👨‍💻 Author")

st.sidebar.markdown(
"""
<div style="font-size:12px">

<b>Girandoux Fandio</b><br>
Data Scientist | Data Analyst
<br>

<a href="https://www.linkedin.com/in/girandoux-fandio-08628bb9/" target="_blank">
LinkedIn
</a>
|

<a href="https://github.com/Girandoux" target="_blank">
GitHub
</a>

</div>
""",
unsafe_allow_html=True
)

# =========================================================
# 10. DATA COVERAGE
# =========================================================

st.sidebar.markdown(
    "<hr style='margin:3px 0;'>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    f"""
<div style="font-size:12px;color:steelblue">

<b>Data Coverage</b><br>

{int(df['year'].min())} - {int(df['year'].max())}

</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# 11. SEITEN DEFINIEREN
# =========================================================

overview = st.Page(
    "pages/0_Executive_Overview.py",
    title="Executive Overview",
    icon="📊"
)

country = st.Page(
    "pages/1_Country_Performance.py",
    title="Country Performance",
    icon="🌍"
)

athlete = st.Page(
    "pages/2_Athlete_Performance.py",
    title="Athlete Performance",
    icon="🏃"
)

gender = st.Page(
    "pages/3_Gender_Analysis.py",
    title="Gender Analysis",
    icon="👥"
)

history = st.Page(
    "pages/4_Historical_Trends.py",
    title="Historical Trends",
    icon="📈"
)

prediction = st.Page(
    "pages/5_Medal_Prediction.py",
    title="Medal Prediction",
    icon="🤖"
)

insights = st.Page(
    "pages/6_Project_Insights.py",
    title="Project Insights",
    icon="📖"
)

# =========================================================
# 12. NAVIGATION
# =========================================================

pg = st.navigation(

    [

        overview,
        country,
        athlete,
        gender,
        history,
        prediction,
        insights

    ],

    position="top"
)

pg.run()