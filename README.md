# Tasnif Service

A FastAPI-based REST API service for managing products and groups, backed by PostgreSQL.

## Overview

This service provides REST endpoints to query product and group data sourced from JSON files. It uses SQLAlchemy ORM for database operations and supports multilingual product names (Uzbek, Russian, Latin).

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- PostgreSQL (or Docker)

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd tasnif-service
   ```

2. **Start PostgreSQL (using Docker):**
   ```bash
   docker-compose up -d
   ```

3. **Activate virtual environment and install dependencies:**
   ```bash
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

4. **Configure environment:**
   
   Copy `.env` and adjust if needed:
   ```bash
   # Default: DATABASE_URL=postgresql://postgres:postgres@localhost/postgres
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Seed the database:**
   ```bash
   poe seed
   ```

7. **Start the development server:**
   ```bash
   poe dev
   ```

The API will be available at `http://localhost:8000`.

## Available Commands

This project uses [poe](https://poethepoet.natn.io/) (similar to npm scripts) for task management:

```bash
poe dev      # Start dev server with auto-reload
poe test     # Run tests
poe lint     # Lint code with ruff
poe seed     # Seed database with JSON data from data/ directory
```

## API Endpoints

### Products

**List all products**
```http
GET /products?skip=0&limit=20
```

Query parameters:
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 20) - Maximum number of records to return

**Get product by mxik**
```http
GET /products/{mxik}
```

Example: `GET /products/12345`

### Groups

**List all groups**
```http
GET /groups?skip=0&limit=20
```

Query parameters:
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 20) - Maximum number of records to return

## Data Models

### Product

| Field | Type | Description |
|-------|------|-------------|
| `mxik` | String (PK) | Unique product identifier |
| `mxik_name_uz` | String | Product name in Uzbek |
| `mxik_name_ru` | String | Product name in Russian |
| `mxik_name_lat` | String | Product name in Latin script |
| `label_for_check` | Integer | Check label flag |
| `international_code` | String | International product code |
| `use_package` | Integer | Package usage flag |
| `created_at` | BigInteger | Creation timestamp |
| `update_at` | BigInteger | Last update timestamp |
| `label` | Integer | Label flag |
| `cash_sale` | Integer | Cash sale flag |
| `packages` | Relationship | Related packages |

### Package

| Field | Type | Description |
|-------|------|-------------|
| `code` | Integer (PK) | Package code |
| `mxik_code` | String (FK) | Reference to product mxik |
| `name_uz` | String | Package name in Uzbek |
| `name_ru` | String | Package name in Russian |
| `name_lat` | String | Package name in Latin script |
| `package_type` | String | Type of package |

### Group

| Field | Type | Description |
|-------|------|-------------|
| `group_code` | Integer (PK) | Group identifier |
| `name_uz` | String | Group name in Uzbek |
| `name_ru` | String | Group name in Russian |
| `name_lat` | String | Group name in Latin script |

## Data Sources

The service seeds its database from JSON files in the `data/` directory:

- `data/products.json` - Product and package data
- `data/groups.json` - Group data

Run `poe seed` to reload data from these files.

**Note:** These files can be very large and may lack newlines. Use `jq` for reading/querying:
```bash
jq '.[0]' data/products.json  # First product
jq 'length' data/products.json  # Total count
```

## Development

### Running Tests
```bash
poe test
```

### Linting
```bash
poe lint
```

### Database Migrations

This project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## JS/Node Developer Notes

| JS/Node | Python Equivalent | Purpose |
|---------|------------------|---------|
| `package.json` | `pyproject.toml` | Project metadata & config |
| `npm install` | `uv pip install -r requirements.txt` | Install dependencies |
| `node_modules/` | `.venv/` | Installed packages |
| `npx` | `uv run` | Run commands in project context |
| `nodemon` | `uvicorn --reload` | Dev server with hot reload |
| `jest` | `pytest` | Testing |
| `eslint` | `ruff` | Linting |

## Project Structure

```
tasnif-service/
├── data/                  # JSON data files for seeding
│   ├── products.json
│   └── groups.json
├── migrations/            # Alembic database migrations
├── main.py                # FastAPI application entry point
├── models.py              # SQLAlchemy ORM models
├── database.py            # Database connection setup
├── seed.py                # Database seeding script
├── pyproject.toml         # Project configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── alembic.ini            # Alembic configuration
└── docker-compose.yml     # PostgreSQL service
```

## Configuration

Environment variables (via `.env`):

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |

Example:
```
DATABASE_URL=postgresql://postgres:postgres@localhost/postgres
```
