from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# SQLite database setup using SQLAlchemy
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Initialize a table with insecure defaults
with engine.begin() as conn:
    conn.execute(
        text(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
        )
    )
    # Plaintext password storage is insecure
    conn.execute(
        text(
            "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'secret')"
        )
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/datetime", response_class=HTMLResponse)
async def datetime_partial(request: Request) -> HTMLResponse:
    """Return a fragment with the current UTC time.

    This route is intended to be loaded via HTMX.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return templates.TemplateResponse("datetime.html", {"request": request, "now": now})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, username: str = "") -> HTMLResponse:
    """Search for a user by name with a vulnerable SQL query."""

    # SQL injection vulnerability: user input is concatenated directly into the query
    query = f"SELECT username FROM users WHERE username = '{username}'"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        users = [row[0] for row in result]

    # Cross-site scripting: user input rendered without escaping
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "username": username, "users": users, "query": query},
    )
