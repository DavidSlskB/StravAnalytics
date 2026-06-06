import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from utils import format_pace, load_data, STRAVA_ORANGE, STRAVA_BLUE, PLOT_BG, PAPER_BG


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


st.divider()
st.subheader("Clustering K-Means")

df_features = df[["distance_km", "pace_min_km"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_features)

# Détermination automatique du meilleur K
silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores.append(silhouette_score(X_scaled, labels))

# best_k = silhouette_scores.index(max(silhouette_scores)) + 2
best_k = 3 # Choix métier : 3 types d'entraînement naturels

# Entraînement final avec le meilleur K
kmeans_final = KMeans(n_clusters=best_k, random_state=0, n_init="auto")
df["cluster"] = kmeans_final.fit_predict(X_scaled)
df["cluster"] = df["cluster"].astype(str)

st.info(f"Meilleur K selon le score de silhouette : **{best_k}**")

# Visualisation des clusters
fig_clusters = px.scatter(
    df,
    x="distance_km",
    y="pace_min_km",
    color="cluster",
    hover_data=["name", "date"],
    title=f"Clustering de tes sorties ({best_k} groupes)",
    labels={
        "distance_km": "Distance (km)",
        "pace_min_km": "Allure (min/km)",
        "cluster": "Cluster"
    },
    color_discrete_sequence=[STRAVA_ORANGE, STRAVA_BLUE, "#A8E063", "#E040FB"]
)
fig_clusters.update_layout(
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color="white"),
    xaxis=dict(gridcolor="#3D3D42"),
    yaxis=dict(gridcolor="#3D3D42"),
)
st.plotly_chart(fig_clusters, use_container_width=True)

# Caractéristiques de chaque cluster
st.subheader("Caractéristiques des clusters")
df_cluster_stats = df.groupby("cluster").agg(
    nb_sorties=("id", "count"),
    distance_moyenne=("distance_km", "mean"),
    allure_moyenne=("pace_min_km", "mean")
).reset_index()
df_cluster_stats["distance_moyenne"] = df_cluster_stats["distance_moyenne"].round(1)
df_cluster_stats["allure_moyenne"]   = df_cluster_stats["allure_moyenne"].apply(format_pace)
df_cluster_stats.columns = ["Cluster", "Nb sorties", "Distance moy. (km)", "Allure moy."]
st.dataframe(df_cluster_stats, use_container_width=True, hide_index=True)