import os
from collections.abc import Mapping
from dataclasses import dataclass

# Matches the defaults in the root compose.yaml, so db:up works without setup.
DEFAULT_DATABASE_URL = "postgresql+psycopg://super_be:super_be@localhost:5432/super_be"


@dataclass(frozen=True)
class Settings:
    database_url: str


def build_settings(env: Mapping[str, str]) -> Settings:
    return Settings(database_url=env.get("DATABASE_URL", DEFAULT_DATABASE_URL))


# Built once at import time, so the rest of the app reads a single object.
settings = build_settings(os.environ)
