from __future__ import with_statement

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from dotenv import load_dotenv

# Ensure project package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load environment variables from a `.env` file in the project root (if present)
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Build the SQLAlchemy DB URL. Priority:
# 1. `DATABASE_URL` env var
# 2. individual PG* env vars (PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDATABASE)
db_url = os.getenv('DATABASE_URL')
if not db_url:
    user = os.getenv('PGUSER', 'postgres')
    password = os.getenv('PGPASSWORD', '')
    host = os.getenv('PGHOST', 'localhost')
    port = os.getenv('PGPORT', '5432')
    database = os.getenv('PGDATABASE', 'postgres')
    db_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# Set the sqlalchemy.url in the Alembic config so rest of env.py can use it
config.set_main_option('sqlalchemy.url', db_url)

# Import the metadata from the app's models
from app.models import Base  # noqa: E402

target_metadata = Base.metadata


def get_url() -> str:
    return config.get_main_option('sqlalchemy.url')


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
