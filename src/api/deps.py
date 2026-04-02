"""Auth dependency — reads Authelia headers."""

from dataclasses import dataclass

from fastapi import HTTPException, Request

from config.settings import settings


@dataclass
class CurrentUser:
    email: str
    display_name: str


def get_current_user(request: Request) -> CurrentUser:
    if not settings.auth_enabled:
        return CurrentUser(email=settings.dev_user_email, display_name="Dev User")

    email = request.headers.get("Remote-Email")
    if not email:
        raise HTTPException(401, "Not authenticated")

    display_name = request.headers.get("Remote-Name", email)
    return CurrentUser(email=email, display_name=display_name)
