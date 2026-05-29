import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

df_evolution = df.groupby("month").agg(
    total_distance=("distance_km", "sum"),
    mean_distance=("distance_km", "mean"),
    total_time=("moving_time_seconds", "sum")
).reset_index()

df_evolution["pace_ponderee"] = df_evolution["total_time"] / 60 / df_evolution["total_distance"]
df_evolution["month"] = df_evolution["month"].astype(str)

fig = go.Figure()

STRAVA_ORANGE = "#FC4C02"
STRAVA_BLUE = "#4FC3F7"
PLOT_BG = "#2D2D32"
PAPER_BG = "#242428"

fig.update_layout(
    title="Évolution de l'allure et de la distance moyenne par mois",
    xaxis=dict(title="Mois", gridcolor="#3D3D42"),
    yaxis=dict(title="Allure (min/km)", gridcolor="#3D3D42"),
    yaxis2=dict(title="Distance moyenne (km)", overlaying="y", side="right"),
    legend=dict(x=0, y=1.1, orientation="h"),
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color="white")
)

fig.update_traces(
    selector=dict(name="Allure (min/km)"),
    line=dict(color=STRAVA_ORANGE),
    marker=dict(color=STRAVA_ORANGE)
)
fig.update_traces(
    selector=dict(name="Distance moyenne (km)"),
    line=dict(color=STRAVA_BLUE),
    marker=dict(color=STRAVA_BLUE)
)

fig.add_trace(go.Scatter(
    x=df_evolution["month"],
    y=df_evolution["pace_ponderee"],
    name="Allure (min/km)",
    mode="lines+markers",
    yaxis="y1"
))

fig.add_trace(go.Scatter(
    x=df_evolution["month"],
    y=df_evolution["mean_distance"],
    name="Distance moyenne (km)",
    mode="lines+markers",
    yaxis="y2"
))

fig.update_layout(
    title="Évolution de l'allure et de la distance moyenne par mois",
    xaxis=dict(title="Mois"),
    yaxis=dict(title="Allure (min/km)"), # autorange="reversed"
    yaxis2=dict(title="Distance moyenne (km)", overlaying="y", side="right"),
    legend=dict(x=0, y=1.1, orientation="h")
)

st.plotly_chart(fig, use_container_width=True)