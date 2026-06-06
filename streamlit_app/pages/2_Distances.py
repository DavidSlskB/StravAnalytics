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

# ── Allure par tranche de distance ──
st.subheader("Allure pondérée par tranche de distance")

bins   = [0, 4, 6, 9, 13, 50]
labels = ["0-4km", "4-6km", "6-9km", "9-13km", "13km+"]
df["tranche"] = pd.cut(df["distance_km"], bins=bins, labels=labels)

df_tranches = df.groupby("tranche", observed=True).agg(
    total_distance=("distance_km", "sum"),
    total_time=("moving_time_seconds", "sum"),
    nb_sorties=("id", "count")
).reset_index()

df_tranches["pace_ponderee"] = df_tranches["total_time"] / 60 / df_tranches["total_distance"]

fig_bar = px.bar(
    df_tranches,
    x="tranche",
    y="pace_ponderee",
    text="nb_sorties",
    title="Allure pondérée par tranche de distance",
    labels={
        "tranche": "Tranche de distance",
        "pace_ponderee": "Allure (min/km)",
    },
    color_discrete_sequence=[STRAVA_ORANGE]
)
fig_bar.update_traces(texttemplate="%{text} sorties", textposition="outside")
fig_bar.update_layout(
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color="white"),
    xaxis=dict(gridcolor="#3D3D42"),
    yaxis=dict(gridcolor="#3D3D42"),
)
st.plotly_chart(fig_bar, use_container_width=True)


# ── K ──
st.subheader("K-means")

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Extraire les features distance_km et pace_min_km
# Appliquer StandardScaler
# Boucler sur K de 1 à 10, entraîner un KMeans à chaque fois et récupérer son inertie (kmeans.inertia_)
# Tracer la courbe inertie vs K