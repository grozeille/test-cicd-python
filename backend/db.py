"""Database utilities for the Flask app."""
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

def get_database_url() -> str:
    url = os.getenv('DATABASE_URL')
    if url:
        return url
    user = os.getenv('PGUSER', 'postgres')
    password = os.getenv('PGPASSWORD', '')
    host = os.getenv('PGHOST', 'localhost')
    port = os.getenv('PGPORT', '5432')
    database = os.getenv('PGDATABASE', 'postgres')
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'


DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    """Yield a SQLAlchemy session (use in `with` or manually close)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
