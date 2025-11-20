# Alembic + SQLAlchemy example

This workspace provides a minimal setup to manage a `users` table using SQLAlchemy + Alembic.

Quick steps (PowerShell):

1. Install deps:

```powershell
python -m pip install -r requirements.txt
```

2. (Optional) Edit DB URL in `alembic.ini` under `sqlalchemy.url`. Default is `sqlite:///app.db`.

3. To auto-generate a migration after model changes:

```powershell
alembic revision --autogenerate -m "create users table"
```

4. Apply migrations:

```powershell
alembic upgrade head
```

5. To inspect the DB file (SQLite):

```powershell
sqlite3 app.db ".schema"
```
