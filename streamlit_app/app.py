import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("data/activities_clean.csv")
    df["month"] = df["month"].astype("period[M]")
    return df


def format_pace(pace_decimal):
    if pd.isna(pace_decimal):
        return "N/A"
    negative = pace_decimal < 0
    pace_decimal = abs(pace_decimal)
    minutes = int(pace_decimal)
    seconds = round((pace_decimal - minutes) * 60)
    return f"-{minutes}:{seconds:02d}" if negative else f"{minutes}:{seconds:02d}"

df = load_data()

st.title("StravAnalytics 🏃")
st.header("Analyse de mes activités Strava")

current_month = pd.Period(pd.Timestamp.now(), "M")
last_month = current_month - 1

runs_this_month = len(df[df["month"] == current_month])
runs_last_month = len(df[df["month"] == last_month])
distance_this_month = df[df["month"] == current_month]["distance_km"].sum()
distance_last_month = df[df["month"] == last_month]["distance_km"].sum()
pace_this_month = df[df["month"] == current_month]["pace_min_km"].mean()
pace_last_month = df[df["month"] == last_month]["pace_min_km"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Courses ce mois",
    value=runs_this_month,
    delta=f"{runs_this_month - runs_last_month:+d} vs mois dernier"
)
col2.metric(
    label="Distance ce mois (km)",
    value=f"{distance_this_month:.1f}",
    delta=f"{distance_this_month - distance_last_month:+.1f} vs mois dernier"
)
col3.metric(
    label="Allure ce mois (min/km)",
    value=format_pace(pace_this_month),
    delta=format_pace(pace_this_month - pace_last_month) + " vs mois dernier",
    delta_color="inverse"
)

st.divider()
st.subheader("Statistiques all time")

col1, col2, col3 = st.columns(3)
col1.metric("Nombre de courses", len(df))
col2.metric("Distance totale (km)", df["distance_km"].sum().round(2))
col3.metric("Allure moyenne globale (min/km)", format_pace(df["pace_min_km"].mean()))

st.divider()
st.subheader("Évolution")

df_evolution = df.groupby("month")["pace_min_km"].mean().reset_index()
df_evolution["month"] = df_evolution["month"].astype(str)  # ← correction clé

fig = px.line(
    data_frame=df_evolution,
    x="month",
    y="pace_min_km",
    title="Évolution de l'allure moyenne par mois",
    labels={"month": "Mois", "pace_min_km": "Allure (min/km)"},
    markers=True
)
fig.update_yaxes(autorange="reversed")  # allure plus basse = meilleure = en haut
st.plotly_chart(fig, use_container_width=True)