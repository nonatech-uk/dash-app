"""App registry — central nav configuration for all apps."""

import logging

import psycopg2
from fastapi import APIRouter, Header, HTTPException, Response
from pydantic import BaseModel

from config.settings import settings

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/apps", tags=["registry"])

EXTERNAL = [
    {"label": "Healthchecks", "href": "https://hc.mees.st"},
    {"label": "Grafana", "href": "https://grafana.mees.st"},
    {"label": "Paperless", "href": "https://docs.mees.st"},
    {"label": "Immich", "href": "https://pix.mees.st"},
    {"label": "Plex", "href": "https://plex.mees.st"},
]

HOME_APP = {"label": "Home", "href": "https://dash.mees.st", "icon": "\u2302"}


class AppRegistration(BaseModel):
    label: str
    href: str
    icon: str
    sort_order: int = 99


def _get_conn():
    if not settings.usage_dsn:
        return None
    return psycopg2.connect(settings.usage_dsn)


@router.post("/register", status_code=204)
def register_app(
    body: AppRegistration,
    response: Response,
    authorization: str = Header(default=""),
):
    expected = settings.registry_api_key
    if not expected:
        raise HTTPException(503, "Registry not configured")

    token = authorization.removeprefix("Bearer ").strip()
    if token != expected:
        raise HTTPException(401, "Invalid API key")

    conn = _get_conn()
    if not conn:
        raise HTTPException(503, "Database not available")

    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO app_registry (label, href, icon, sort_order, registered_at)
               VALUES (%s, %s, %s, %s, now())
               ON CONFLICT (label) DO UPDATE
               SET href = EXCLUDED.href,
                   icon = EXCLUDED.icon,
                   sort_order = EXCLUDED.sort_order,
                   registered_at = now()""",
            (body.label, body.href, body.icon, body.sort_order),
        )
        conn.commit()
        log.info("Registered app: %s → %s", body.label, body.href)
    except Exception:
        log.exception("Failed to register app %s", body.label)
        conn.rollback()
        raise HTTPException(500, "Registration failed")
    finally:
        conn.close()


@router.get("")
def get_apps(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"

    apps = [HOME_APP]

    conn = _get_conn()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT label, href, icon FROM app_registry ORDER BY sort_order, label"
            )
            for label, href, icon in cur.fetchall():
                apps.append({"label": label, "href": href, "icon": icon})
        except Exception:
            log.exception("Failed to fetch app registry")
        finally:
            conn.close()

    return {"apps": apps, "external": EXTERNAL}
