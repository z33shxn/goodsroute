# GoodsRoute Backend

A FastAPI backend application for GoodsRoute with PostGIS spatial database support.

## Features

- FastAPI REST API
- PostGIS for geospatial queries
- JWT authentication
- Store management
- Product listings
- Geospatial search capabilities

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Quick Start

1. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

2. Start services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Access the API:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── dependencies.py
│   └── core/
│       ├── security.py
│       └── utils.py
├── alembic/
├── scripts/
├── tests/
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT
