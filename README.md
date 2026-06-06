# StravAnalytics
Personal running data analysis dashboard using Strava API.

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
5. Run `streamlit run streamlit_app/app.py` to launch the dashboard

## Project structure
```bash
StravAnalytics/
├── src/
│   ├── auth.py          # Strava OAuth authentication
│   └── fetch.py         # Fetch and save activities
├── notebooks/
│   └── 01_exploration.ipynb  # Data cleaning and EDA
├── streamlit_app/
│   ├── app.py           # Main dashboard page
│   └── pages/
│       ├── 2_Distances.py
│       └── 3_Map.py
└── data/                # Local only, not versioned
```

## Roadmap
- [ ] Internationalisation (FR/EN)
- [ ] Données de flux par activité (splits, PR sur sous-distances)
- [ ] Modèle ML de prédiction du suffer score
- [ ] Déploiement Streamlit Cloud
- [ ] Enrichissement météo via API Open-Meteo (température, conditions) pour affiner le clustering
