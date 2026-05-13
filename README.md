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

Backend part project. Run commands from the `src` directory:

```bash
cd src
```

Development start:

uv run uvicorn app.main:app --reload

Production-like start:

uv run gunicorn app.main:app -c gunicorn_config.py

Initialize RBAC data:

uv run init.py

Docker image build:

```bash
docker build -t adel16055/dashboard-itis-backend:latest .
docker push adel16055/dashboard-itis-backend:latest
```

Docker Compose start for frontend developers:

```bash
cd src
cp .env.example .env
docker compose up
```

Before starting, fill required values in `src/.env`, especially
`AUTH__SECRET_KEY`, `DB__USER`, `DB__PASSWORD`, `DB__NAME` and email settings.

Compose uses only images from DockerHub and does not build services locally:
- backend image is taken from `BACKEND_IMAGE`
- frontend image for deployment is declared as `FRONTEND_IMAGE`
- database image is `postgres:18`
- reverse proxy image is `nginx:stable-alpine`

Only port `80` is exposed outside the compose network. Database, migrations,
RBAC initialization and API stay inside the internal Docker network.

Available local URLs:
- frontend/static entrypoint: `http://localhost`
- API proxy prefix: `http://localhost/api/v1`

The API container listens on `0.0.0.0:8000`; nginx proxies `/api/*` requests to
the API service and serves `nginx/html/index.html` for other paths.


## Environment Variables

Create `.env` file in the `src` directory.

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
| EMAIL__MAIL_USERNAME | string | SMTP username |  |
| EMAIL__MAIL_PASSWORD | string | SMTP app password |  |
| EMAIL__MAIL_FROM | string | Sender email address |  |
| EMAIL__MAIL_SERVER | string | SMTP server host | smtp.gmail.com |
| EMAIL__MAIL_PORT | int | SMTP server port | 587 |
| EMAIL__MAIL_FROM_NAME | string | Sender display name | Dashboard ITIS |
| EMAIL__MAIL_STARTTLS | bool | Use STARTTLS | true |
| EMAIL__MAIL_SSL_TLS | bool | Use SSL/TLS | false |
| EMAIL__USE_CREDENTIALS | bool | Use SMTP auth credentials | true |
| EMAIL__VALIDATE_CERTS | bool | Validate SMTP certificates | true |
| EMAIL__TEMPLATE_FOLDER | string | Email templates path | app/templates/email |
| EMAIL__APP_HOST | string | Backend host for confirmation links | http://localhost:8000 |
| EMAIL__CONFIRMATION_CODE_LIFETIME_MINUTES | int | Email confirmation code lifetime | 30 |

---

## Alembic Migrations

Create migration:

```bash
uv run alembic revision --autogenerate -m "message"
```
