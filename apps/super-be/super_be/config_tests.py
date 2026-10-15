from super_be.config import DEFAULT_DATABASE_URL, build_settings


def test_database_url_defaults_to_local_compose_database() -> None:
    settings = build_settings({})

    assert settings.database_url == DEFAULT_DATABASE_URL


def test_database_url_comes_from_env() -> None:
    settings = build_settings(
        {"DATABASE_URL": "postgresql+psycopg://u:p@db:5432/other"}
    )

    assert settings.database_url == "postgresql+psycopg://u:p@db:5432/other"
