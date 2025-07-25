from __future__ import annotations

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.models import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "smartport")
    host = os.getenv("PGHOST", "localhost")
    db = os.getenv("PGDATABASE", "postgres")
    return f"postgresql+psycopg://{user}:{password}@{host}/{db}"


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()}, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
