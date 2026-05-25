import os
import webbrowser
from dotenv import load_dotenv
from stravalib import Client

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

client = Client()

url = client.authorization_url(
    client_id=CLIENT_ID,
    redirect_uri="http://localhost",
    scope=["read", "activity:read_all"]
)

print("Opening Strava authorization page...")
print(f"URL: {url}")
webbrowser.open(url)

code = input("\nPaste the 'code' from the redirect URL here: ")

token_response = client.exchange_code_for_token(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    code=code
)

print("\nSuccess! Your tokens:")
print(f"Access token:  {token_response['access_token']}")
print(f"Refresh token: {token_response['refresh_token']}")
print(f"Expires at:    {token_response['expires_at']}")