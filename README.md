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

uv run uvicorn app.main:app --reload --app-dir src


## Environment Variables

Create `.env` file in project root.

| Variable | Description | Default |
|----------|-------------|---------|
| DB_SCHEMA | Database driver | postgresql+asyncpg |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | postgres |
| DB_NAME | Database name | app_db |
| APP_NAME | Application name | Academic Performance API |
| APP_VERSION | Application version | 1.0.0 |

---

## Alembic Migrations

Create migration:

```bash
alembic revision --autogenerate -m "message"