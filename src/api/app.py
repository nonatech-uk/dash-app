"""Dashboard API — FastAPI application."""

import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from src.api.aggregator import fetch_dashboard
from src.api.deps import CurrentUser, get_current_user

STATIC_DIR = Path(_project_root) / "static"

app = FastAPI(
    title="Dashboard API",
    version="0.1.0",
    description="Service aggregation dashboard",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/auth/me")
def auth_me(user: CurrentUser = Depends(get_current_user)):
    return {"email": user.email, "display_name": user.display_name}


@app.get("/api/v1/dashboard")
async def dashboard(request: Request, _user: CurrentUser = Depends(get_current_user)):
    headers = dict(request.headers)
    return await fetch_dashboard(headers)


# Serve React SPA
if STATIC_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        file_path = STATIC_DIR / full_path
        if full_path and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
