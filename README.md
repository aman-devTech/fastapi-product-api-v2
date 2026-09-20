# FastAPI Product API

A Dockerized backend API for managing products with FastAPI, PostgreSQL, SQLAlchemy, Pydantic, JWT authentication, password hashing, and Redis-backed caching.

This project is built as a practical backend portfolio application. It includes user registration and login, protected product CRUD operations, product search, pagination, minimum-price filtering, input validation, PostgreSQL persistence, and Redis caching for read-heavy product endpoints.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- PostgreSQL 18
- SQLAlchemy
- Pydantic
- JWT authentication with `python-jose`
- Password hashing with Passlib and bcrypt
- Redis
- Docker
- Docker Compose

## Architecture

```text
Client
  |
  v
FastAPI application
  |
  +--> PostgreSQL
  |
  +--> Redis
```

FastAPI handles HTTP requests, authentication, validation, and routing. SQLAlchemy manages database access to PostgreSQL. Redis is used as a cache for product read endpoints, with a 60-second cache TTL and cache invalidation after product create, update, and delete operations.

## Features

- User registration
- User login with JWT access tokens
- Protected product APIs using bearer token authentication
- Product create, read, update, and delete operations
- Product search by name
- Pagination for product lists
- Minimum-price filtering
- Pydantic request validation
- Password hashing before user storage
- Redis caching for product read endpoints
- PostgreSQL persistence
- Dockerized FastAPI, PostgreSQL, and Redis services
- Persistent PostgreSQL Docker volume

## Project Structure

```text
FastAPI_phase-1/
|-- app/
|   |-- routers/
|   |   |-- auth.py
|   |   `-- product.py
|   |-- utils/
|   |   `-- security.py
|   |-- crud.py
|   |-- database.py
|   |-- database_model.py
|   |-- main.py
|   |-- models.py
|   `-- redis_client.py
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- docker-compose.yml
|-- README.md
`-- requirements.txt
```

## Prerequisites

For Docker setup:

- Docker
- Docker Compose

For local setup without Docker:

- Python 3.13 or compatible Python 3 version
- PostgreSQL
- Redis

## Environment Variables

The application reads configuration from environment variables.

| Variable | Used by | Description |
| --- | --- | --- |
| `DATABASE_URL` | FastAPI app | SQLAlchemy PostgreSQL connection URL |
| `SECRET_KEY` | FastAPI app | Secret used to sign and verify JWT access tokens |
| `REDIS_HOST` | FastAPI app | Redis hostname |
| `REDIS_PORT` | FastAPI app | Redis port |
| `REDIS_DB` | FastAPI app | Redis database number |
| `POSTGRES_PASSWORD` | Docker Compose PostgreSQL service | Password for the Docker PostgreSQL user |

Do not commit `.env` or `.env.docker` files. They are intentionally ignored by Git.

For Docker, `docker-compose.yml` expects an `.env.docker` file for the FastAPI container and a `POSTGRES_PASSWORD` value available to Docker Compose.

Example variable names only:

```env
DATABASE_URL=postgresql://postgres:<password>@postgres:5432/fastAPI_beginner
SECRET_KEY=<secure-secret-key>
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
POSTGRES_PASSWORD=<postgres-password>
```

For non-Docker local development, use local service hosts instead:

```env
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/fastAPI_beginner
SECRET_KEY=<secure-secret-key>
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Docker Setup

The repository includes a Dockerized setup with three services:

- `api`: FastAPI app served by Uvicorn on port `8000`
- `postgres`: PostgreSQL 18 exposed on host port `5433`
- `redis`: Redis exposed on host port `6379`

PostgreSQL data is stored in the named Docker volume `postgres_data`.

1. Create `.env.docker` in the project root using the variable names listed above. Do not commit this file.

2. Make sure `POSTGRES_PASSWORD` is available to Docker Compose. One option is to define it in an ignored environment file or export it in your shell before running Compose.

3. Build and start the containers:

```bash
docker compose --env-file .env.docker up --build -d
```

4. Open the API docs:

```text
http://localhost:8000/docs
```

5. Stop the containers:

```bash
docker compose down
```

To stop containers and remove the PostgreSQL volume:

```bash
docker compose down -v
```

Use `-v` only when you intentionally want to delete the persisted database volume.

## Local Setup Without Docker

1. Create and activate a virtual environment.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with local PostgreSQL and Redis connection values.

4. Make sure PostgreSQL is running and the database referenced in `DATABASE_URL` exists.

5. Make sure Redis is running.

6. Start the FastAPI app:

```bash
uvicorn app.main:app --reload
```

7. Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## API Usage

### Root

```http
GET /
```

Returns a simple welcome message.

### Register

```http
POST /register
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

### Login

```http
POST /login
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Response includes an access token:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

Use the token on protected product routes:

```http
Authorization: Bearer <jwt-token>
```

### Product Routes

All product routes require a bearer token.

```http
GET /product
POST /product
GET /product/{id}
PUT /product/{id}
DELETE /product/{id}
GET /product/search/{name}
GET /product/page/?page=1&limit=5
GET /product/price/?min_price=100
```

Product create and update request body:

```json
{
  "name": "phone",
  "description": "budget phone",
  "price": 699.99,
  "quantity": 50
}
```

Validation currently enforced by the product routes:

- `price` must be greater than zero.
- `quantity` cannot be negative.

## Database Notes

The application creates SQLAlchemy tables on startup using:

```python
database_model.Base.metadata.create_all(bind=engine)
```

The Docker setup uses a persistent PostgreSQL volume named `postgres_data`. The existing PostgreSQL database for this project has been migrated/restored into the Docker PostgreSQL database.

## Deployment

The app is container-ready through the included `Dockerfile` and `docker-compose.yml`.

For deployment, provide production environment variables through the target platform's secret/configuration system. At minimum, configure:

- `DATABASE_URL`
- `SECRET_KEY`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`

Use a strong production `SECRET_KEY`, do not commit environment files, and make sure the deployed PostgreSQL and Redis hosts match the environment values used by the FastAPI container.