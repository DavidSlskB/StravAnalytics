import streamlit as st
import pandas as pd
import numpy as np
import folium
import polyline
from streamlit_folium import st_folium
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from geopy.geocoders import Nominatim
from utils import load_data, parse_latlng, STRAVA_ORANGE

@st.cache_data
def get_city_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="stravanalytics")
        location = geolocator.reverse((lat, lon), language="fr")
        addr = location.raw["address"]
        return (
            addr.get("city") or
            addr.get("town") or
            addr.get("village") or
            "Zone inconnue"
        )
    except:
        return "Zone inconnue"

def get_best_center(cluster_idx, cluster_labels, X_scaled, centers_scaled, coords_clean):
    mask = cluster_labels == cluster_idx
    cluster_points = X_scaled[mask]
    centroid = centers_scaled[cluster_idx]
    distances = np.linalg.norm(cluster_points - centroid, axis=1)
    closest_idx = np.argmin(distances)
    return coords_clean.values[mask][closest_idx]

df_map = load_data("data/activities_map.csv")
df_map["coords"] = df_map["start_latlng"].apply(parse_latlng)

coords_clean = df_map["coords"].dropna()
X = np.array(coords_clean.tolist())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

silhouette_scores = []
for k in range(2, min(11, len(X))):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores.append(silhouette_score(X_scaled, labels))

best_k = silhouette_scores.index(max(silhouette_scores)) + 2

kmeans_final = KMeans(n_clusters=best_k, random_state=0, n_init="auto")
cluster_labels = kmeans_final.fit_predict(X_scaled)

centers = scaler.inverse_transform(kmeans_final.cluster_centers_)

seuil = max(10, len(df_map) * 0.15)
cluster_counts = pd.Series(cluster_labels).value_counts()
main_zones = cluster_counts[cluster_counts >= seuil].index.tolist()

st.title("🗺️ Carte de mes sorties")
st.info(f"{len(main_zones)} zone(s) principale(s) détectée(s) sur {best_k} clusters")

zone_options = {}
for i, z in enumerate(main_zones):
    best_center = get_best_center(
        z, cluster_labels, X_scaled,
        kmeans_final.cluster_centers_, coords_clean
    )
    city = get_city_name(float(best_center[0]), float(best_center[1]))
    zone_options[f"{city} ({cluster_counts[z]} sorties)"] = best_center

selected_zone = st.selectbox("Centrer sur :", list(zone_options.keys()))
center = zone_options[selected_zone]

# m = folium.Map(location=[49.4, 2.8], zoom_start=13) # Compiègne
m = folium.Map(location=center, zoom_start=13)

for _, row in df_map.iterrows():
    if pd.isna(row["summary_polyline"]):
        continue
    coordinates = polyline.decode(row["summary_polyline"])
    folium.PolyLine(
        locations=coordinates,
        color=STRAVA_ORANGE,
        weight=2,
        opacity=0.7
    ).add_to(m)

st_folium(m, use_container_width=True, height=600)