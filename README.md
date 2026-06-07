# StravAnalytics
Personal running data analysis dashboard using Strava API.

## Live demo
👉 [stravanalytics.streamlit.app](https://stravanalytics.streamlit.app)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

## Usage
1. Create a Strava API app at https://www.strava.com/settings/api
2. Copy `.env.example` to `.env` and fill in your credentials
3. Run `python src/auth.py` to authenticate
4. Run `python src/fetch.py` to fetch your activities
5. Open `notebooks/01_exploration.ipynb` and run all cells to generate cleaned datasets
6. Run `streamlit run streamlit_app/app.py` to launch the dashboard

## Project structure
```bash
StravAnalytics/
├── src/
│   ├── auth.py               # Strava OAuth authentication
│   └── fetch.py              # Fetch and save activities
├── notebooks/
│   └── 01_exploration.ipynb  # Data cleaning and feature engineering
├── streamlit_app/
│   ├── app.py                # Main dashboard page
│   ├── utils.py              # Shared functions and constants
│   └── pages/
        ├── 1_Vue_générale.py # Overview, metrics, charts
        ├── 2_Distances.py    # Distance analysis and K-Means clustering
        ├── 3_Carte.py        # Interactive GPS map
        ├── 4_Activités.py    # Activities list with filters
        └── 5_Détail.py       # Single activity detail
└── data/                     # Local only, not versioned
```

## Roadmap

### ✅ V1.0.0 — Terminé
- [x] Pipeline de collecte via API Strava (OAuth2, fetch, refresh token)
- [x] Nettoyage et feature engineering (notebook)
- [x] Dashboard Streamlit - Vue générale (métriques, évolution, scatter)
- [x] Dashboard Streamlit - Analyse par distance (histogramme, clustering K-Means)
- [x] Dashboard Streamlit - Carte GPS interactive (zones auto-détectées, géocodage)
- [x] Dashboard Streamlit - Liste des activités (filtres, navigation)
- [x] Dashboard Streamlit - Page détail par sortie (tracé GPS, stats)
- [x] Déploiement Streamlit Cloud

### Court terme
- [ ] Automatisation du fetch et push des données (scheduler)
- [ ] Enrichissement météo via API Open-Meteo
- [ ] Visualisations temporelles : répartition par heure, jour, saison
- [ ] Amélioration clustering : ajout features météo, temporelles

### Moyen terme
- [ ] Données de flux par activité (splits, PR sur sous-distances)
- [ ] Amélioration page détail (description, splits via get_activity())
- [ ] Modèle ML de prédiction du suffer score
- [ ] Courbes de progression avec projection future
- [ ] Score de forme sur les 4 dernières semaines basé sur le volume et l'allure

### Long terme
- [ ] Commentaire IA sur la situation actuelle (LLM)
- [ ] Internationalisation (FR/EN)
- [ ] Multi-utilisateurs (authentification, token personnalisé)
- [ ] Suggestions de sorties types pour la prochaine course