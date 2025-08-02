import os
from dotenv import load_dotenv

load_dotenv()

# Use the current working directory as base (the root of the project)
base_dir = os.getcwd()

# Load .env from the root of the project
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

# Now resolve credentials path correctly
relative_cred_path = os.getenv("GOOGLE_CREDENTIALS_FILE")
GOOGLE_CREDENTIALS_FILE = os.path.join(base_dir, relative_cred_path)
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

# Print to verify
print("Using Google Credentials File:", GOOGLE_CREDENTIALS_FILE)


OAUTH_CONFIGS = {
    "google": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "scopes": ["openid", "email", "profile"],
        "redirect_uri": "http://localhost:8000/auth/google/callback",
        "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
    },
    "facebook": {
        "client_id": os.getenv("FACEBOOK_CLIENT_ID"),
        "client_secret": os.getenv("FACEBOOK_CLIENT_SECRET"),
        "auth_url": "https://www.facebook.com/v18.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
        "userinfo_url": "https://graph.facebook.com/v18.0/me",
        "scopes": ["email", "public_profile"],
        "redirect_uri": "http://localhost:8000/auth/facebook/callback",
        "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN"),
    },
    "github": {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
        "scopes": ["user:email", "read:user"],
        "redirect_uri": "http://localhost:8000/auth/github/callback",
        "access_token": os.getenv("GITHUB_ACCESS_TOKEN"),
    },
    "csv_file": os.getenv("CSV_FILE", "benchmark_results.csv"),
}


def get_oauth_config(provider: str):
    if provider not in OAUTH_CONFIGS:
        raise ValueError(f"Unsupported provider: {provider}")
    return OAUTH_CONFIGS[provider]
