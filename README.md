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

Run the Flask backend (development)
----------------------------------

1. Create a `.env` at the repo root or set `DATABASE_URL`/PG* env vars.
2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Start the Flask app:

```powershell
python -m backend.app
```

4. Open http://localhost:5000 in your browser to see the "Hello World" page and the users table.

API Documentation (Swagger UI)
-----------------------------

flask-restx automatically generates docs and a Swagger UI. After starting the Flask server, open:

```
http://localhost:5000/docs-restx
```

The OpenAPI JSON is available at:

```
http://localhost:5000/swagger.json
```

Notes:
- The page fetches `/api/users` to list users from the database using the existing SQLAlchemy model in `app/models.py`.
- For production, use a WSGI server (gunicorn, waitress) and proper configuration.
```
