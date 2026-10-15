from super_be.config import Settings
from super_be.db import create_db_engine


def test_engine_uses_database_url_from_settings() -> None:
    engine = create_db_engine(
        Settings(database_url="postgresql+psycopg://u:p@h:5432/d")
    )

    assert engine.url.drivername == "postgresql+psycopg"
    assert engine.url.database == "d"
    engine.dispose()
