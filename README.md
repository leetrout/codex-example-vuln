# FastAPI HTMX Example

This repository contains a simple web application using:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [HTMX](https://htmx.org/)
- [Alpine.js](https://alpinejs.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/) with SQLite

## Running the app

Install dependencies and start the development server:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://localhost:8000` in your browser.

## Vulnerabilities

This application intentionally demonstrates common OWASP vulnerabilities:

- **SQL Injection**: `/search` builds SQL queries using unsanitized input.
- **Cross-Site Scripting (XSS)**: user-provided values are rendered using `|safe` in templates.
- **Plaintext Password Storage**: sample credentials are stored without hashing.

Use this project only for educational purposes.
