import streamlit as st
import pandas as pd
import folium
import polyline
from streamlit_folium import st_folium
from utils import load_data, parse_latlng, format_pace, STRAVA_ORANGE, STRAVA_BLUE, PLOT_BG, PAPER_BG

# ── Chargement des données ──
df     = load_data()
df_map = load_data("data/activities_map.csv")

activity_id = st.session_state.get("selected_activity_id")

if activity_id is None:
    st.warning("Aucune sortie sélectionnée — retourne à la liste.")
    if st.button("← Retour à la liste"):
        st.switch_page("pages/4_Activities.py")
    st.stop()

activity     = df[df["id"] == activity_id].iloc[0]
activity_map = df_map[df_map["id"] == activity_id].iloc[0] if activity_id in df_map["id"].values else None

# ── En-tête ──
col_back, col_title = st.columns([1, 8])
with col_back:
    if st.button("←"):
        st.switch_page("pages/4_Activities.py")
with col_title:
    st.title(activity["name"])
    st.caption(f"{activity['day_of_week']} {activity['date_fr']} à {activity['hour_fr']}")

# Badges flagged / manuel
badges = []
if activity["flagged"]:
    badges.append("⚠️ Flagged par Strava")
if activity["manual"]:
    badges.append("✍️ Saisie manuelle")
if badges:
    st.warning("  |  ".join(badges))

st.divider()

# ── Métriques principales ──
st.subheader("📊 Statistiques")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Distance", f"{activity['distance_km']:.2f} km")
col2.metric("Allure moyenne", format_pace(activity["pace_min_km"]))
col3.metric("Durée", f"{int(activity['moving_time_seconds'] // 60)}min {int(activity['moving_time_seconds'] % 60):02d}s")
col4.metric("Suffer score", f"{int(activity['suffer_score'])}" if pd.notna(activity["suffer_score"]) else "N/A")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Dénivelé total", f"{activity['total_elevation_gain_m']:.0f} m")
col6.metric("Point haut", f"{activity['elev_high_m']:.0f} m" if pd.notna(activity["elev_high_m"]) else "N/A")
col7.metric("Point bas", f"{activity['elev_low_m']:.0f} m" if pd.notna(activity["elev_low_m"]) else "N/A")
col8.metric("Allure max", format_pace(1 / activity["max_speed_m_s"] / 60 * 1000) if pd.notna(activity["max_speed_m_s"]) else "N/A")

col9, col10, col11, col12 = st.columns(4)
col9.metric("PR obtenus", f"{int(activity['pr_count'])}")
col10.metric("Pause", f"{int(activity['pause_seconds'])}s" if activity["pause_seconds"] > 0 else "Aucune")
col11.metric("FC moyenne", f"{int(activity['average_heartrate'])} bpm" if pd.notna(activity["average_heartrate"]) else "N/A")
col12.metric("FC max", f"{int(activity['max_heartrate'])} bpm" if pd.notna(activity["max_heartrate"]) else "N/A")

st.divider()

# ── Carte GPS ──
if activity_map is not None and pd.notna(activity_map["summary_polyline"]):
    st.subheader("🗺️ Tracé GPS")
    coordinates = polyline.decode(activity_map["summary_polyline"])
    center      = coordinates[len(coordinates) // 2]

    m = folium.Map(location=center, zoom_start=14)

    # Tracé principal
    folium.PolyLine(
        locations=coordinates,
        color=STRAVA_ORANGE,
        weight=4,
        opacity=0.9
    ).add_to(m)

    # Marqueur départ
    folium.Marker(
        location=coordinates[0],
        popup="Départ",
        icon=folium.Icon(color="green", icon="play", prefix="fa")
    ).add_to(m)

    # Marqueur arrivée
    folium.Marker(
        location=coordinates[-1],
        popup="Arrivée",
        icon=folium.Icon(color="red", icon="stop", prefix="fa")
    ).add_to(m)

    st_folium(m, use_container_width=True, height=400)
else:
    st.info("Pas de tracé GPS disponible pour cette sortie.")

st.divider()

# ── Lien Strava ──
st.markdown(
    f'<a href="https://www.strava.com/activities/{activity_id}" target="_blank">'
    f'<button style="background-color:{STRAVA_ORANGE};color:white;border:none;'
    f'padding:8px 16px;border-radius:4px;cursor:pointer;font-size:14px;">'
    f'Voir sur Strava →</button></a>',
    unsafe_allow_html=True
)