import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, base
from pathlib import Path


# Load .env from root directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get title and version from environment
APP_TITLE = os.getenv("APP_TITLE", "OAuth Benchmark API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


app = FastAPI(title=APP_TITLE, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("ALLOWED_ORIGINS_1", "http://localhost:8000"),
        os.getenv("ALLOWED_ORIGINS_1", "http://localhost:3000"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(base.router)
