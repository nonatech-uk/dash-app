from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Internal service URLs (container hostnames on podman-frontend)
    journal_url: str = "http://journal:8000"
    finance_url: str = "http://host.docker.internal:8000"
    wine_url: str = "http://wine:8200"
    pipeline_url: str = "http://pipeline:8080"
    music_url: str = "http://scrobble-receiver:42010"
    locations_url: str = "http://host.docker.internal:8100"

    # Usage tracking
    usage_dsn: str = ""

    # Auth
    auth_enabled: bool = True
    dev_user_email: str = "stu@mees.st"
    cors_origins: list[str] = [
        "https://dash.mees.st",
        "http://localhost:5173",
    ]

    model_config = {
        "env_file": str(Path(__file__).resolve().parent / ".env"),
        "env_file_encoding": "utf-8",
    }


settings = Settings()
