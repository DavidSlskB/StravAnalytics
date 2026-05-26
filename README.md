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