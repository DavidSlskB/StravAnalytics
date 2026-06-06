import streamlit as st
import pandas as pd
import folium
import polyline
from streamlit_folium import st_folium
from utils import load_data, STRAVA_ORANGE

df_map = load_data("data/activities_map.csv")

st.title("🗺️ Carte de mes sorties")

m = folium.Map(location=[49.4, 2.8], zoom_start=13)

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