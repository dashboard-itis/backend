# Dashboard ITIS

## Description
Dashboard ITIS — это веб-приложение с интуитивно понятным интерфейсом для анализа учебной успеваемости студентов.

Основные функции:
- расчет среднего балла по группе
- визуализация распределения оценок
- рейтинг студентов
- фильтрация по дисциплинам и учебным периодам

Продукт предназначен для **старост и кураторов учебных групп**, которым необходимо регулярно отслеживать учебную динамику студентов.

---

## Team

### Backend
- [@Arsenyprogram](https://github.com/Arsenyprogram)
- [@Adel16055](https://github.com/Adel16055)

### Frontend
- [@arinasidr](https://github.com/arinasidr)
- [@dishxqz](https://github.com/dishxqz)
- [@damir-yo](https://github.com/damir-yo)

---

## Tech Stack

- **FastAPI**
- **WebSocket**
- **uv** — package manager
- **ruff** — linter & formatter


---

## How to Run

Backend part project

to start on root project:

PYTHONPATH=src uv run uvicorn app.main:app --reload

Production-like start:

PYTHONPATH=src uv run gunicorn app.main:app -c gunicorn_config.py

Initialize RBAC data:

uv run init.py


## Environment Variables

Create `.env` file in project root.

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| DB__DRIVERNAME | string | Database driver | postgresql+asyncpg |
| DB__HOST | string | Database host | localhost |
| DB__PORT | int | Database port | 5432 |
| DB__USER | string | Database user | postgres |
| DB__PASSWORD | string | Database password | postgres |
| DB__NAME | string | Database name | app_db |
| APP__NAME | string | Application name | Dashboard ITIS |
| APP__VERSION | string | Application version | 1.0.0 |
| AUTH__SECRET_KEY | string | Secret key for signing JWT tokens. Generate with `openssl rand -hex 32` |  |
| AUTH__ALGORITHM | string | JWT signing algorithm | HS256 |
| AUTH__ACCESS_TOKEN_LIFETIME_SECONDS | int | Access token lifetime in seconds | 900 |
| AUTH__REFRESH_TOKEN_LIFETIME_SECONDS | int | Refresh token lifetime in seconds | 2592000 |
| ADMIN__EMAIL | string | Default admin email | admin@example.com |
| ADMIN__PASSWORD | string | Default admin password | admin12345 |
| ADMIN__FIRST_NAME | string | Default admin first name | Admin |
| ADMIN__LAST_NAME | string | Default admin last name | User |
| RBAC__ADMIN_ROLE | string | Admin role name | admin |
| RBAC__PUBLIC_ROLE | string | Public role name for new users | public |
| RBAC__STUDENT_ROLE | string | Student role name | student |
| RBAC__CURATOR_ROLE | string | Curator role name | curator |

---

## Alembic Migrations

Create migration:

```bash
PYTHONPATH=src uv run alembic revision --autogenerate -m "message"
```
