import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Constantes couleurs Strava ──
STRAVA_ORANGE = "#FC4C02"
STRAVA_BLUE = "#4FC3F7"
PLOT_BG = "#2D2D32"
PAPER_BG = "#242428"

@st.cache_data
def load_data():
    df = pd.read_csv("data/activities_clean.csv")
    df["month"] = df["month"].astype("period[M]")
    return df

df = load_data()

st.title("📏 Analyse par distance")

# ── Distribution des distances ──
st.subheader("Distribution des distances")

fig_hist = px.histogram(
    df,
    x="distance_km",
    nbins=30,
    title="Répartition de mes sorties par distance",
    labels={"distance_km": "Distance (km)", "count": "Nombre de sorties"},
    color_discrete_sequence=[STRAVA_ORANGE]
)
fig_hist.update_layout(
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color="white"),
    xaxis=dict(gridcolor="#3D3D42", title="Distance (km)"),
    yaxis=dict(gridcolor="#3D3D42", title="Nombre de sorties"),
    bargap=0.1
)
st.plotly_chart(fig_hist, use_container_width=True)