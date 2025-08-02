import csv
import logging
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.auth.sessions import generate_state, store_session, get_session
from app.database.database import get_db
from app.utils.save_to_gsheet import save_to_google_sheet
from app.utils.timing import measure_api_call
from app.config import OAUTH_CONFIGS, get_oauth_config
import time, datetime, httpx
from urllib.parse import urlencode
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()
CSV_FILE = OAUTH_CONFIGS["csv_file"]

logger = logging.getLogger(__name__)


@router.get("/auth/{provider}")
async def initiate_oauth(provider: str):
    """Initiate OAuth flow for a specific provider"""

    config = get_oauth_config(provider)
    state = generate_state()
    store_session(state, provider, time.time())

    params = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "scope": " ".join(config["scopes"]),
        "state": state,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }

    auth_url = f"{config['auth_url']}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@router.get("/auth/{provider}/callback")
async def oauth_callback(
    provider: str, code: str, state: str):

    callback_start_time = time.time()

    session = get_session(state)
    if not session:
        logger.warning(f"Invalid state: {state} for provider: {provider}")
        raise HTTPException(status_code=400, detail="Invalid state")

    config = get_oauth_config(provider)
    token_data = {
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code": code,
        "redirect_uri": config["redirect_uri"],
        "grant_type": "authorization_code",
    }

    headers = {"Accept": "application/json"}
    if provider == "github":
        headers["Accept"] = "application/vnd.github+json"

    async with httpx.AsyncClient() as client:
        response, token_time, error = await measure_api_call(
            client.post, config["token_url"], data=token_data, headers=headers
        )
        if not response or response.status_code != 200:
            logger.error(
                f"{provider} token exchange failed: {response.text if response else 'No response'}"
            )
            return JSONResponse(
                status_code=502, content={"error": error or "Failed token exchange"}
            )

        token_response = response.json()
        access_token = token_response.get("access_token")

        user_headers = {"Authorization": f"Bearer {access_token}"}

        user_response, user_time, user_error = await measure_api_call(
            client.get, config["userinfo_url"], headers=user_headers)

        callback_end_time = time.time()
        server_latency = callback_end_time - callback_start_time
        scopes = token_response.get("scope", "").split()
        timestamp = datetime.datetime.now()


        # Extract granted scopes
        if provider == "github":
            scopes = user_response.headers.get("X-OAuth-Scopes", "").split(", ")
        elif provider == "google":
            scopes = token_response.get("scope", "").split()
        elif provider == "facebook":
            scopes = config.get("scopes", [])
        else:
            scopes = []    

        # Flatten benchmark data
        csv_row = {
            "provider": provider,
            "token_response_time": round(token_time, 4),
            "user_info_response_time": round(user_time, 4),
            "latency": round(server_latency, 4),
            "token_received": True,
            "token_expires_in": token_response.get("expires_in"),
            "scopes_granted": ",".join(scopes),
            "timestamp": timestamp.isoformat(),
            "error": user_error,
            "start_time": session.start_time if session else None,
        }

        # Save to Google Sheet
        save_to_google_sheet(csv_row)

    return {"success": True, "benchmark": csv_row, "token_response": token_response}

        # Write to CSV
        # file_exists = os.path.isfile(CSV_FILE)
        # with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=csv_row.keys())
        #     if not file_exists:
        #         writer.writeheader()
        #     writer.writerow(csv_row)

        # with suppress(Exception):
        #     clear_session(state)
        
