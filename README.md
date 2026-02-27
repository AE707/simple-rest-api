# Simple REST API

> A production-ready REST API built with **FastAPI**, **SQLite**, **JWT authentication**, and full **CRUD** support. Includes Docker support and auto-generated Swagger UI.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Docker](https://img.shields.io/badge/Docker-supported-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **User Registration** — Create accounts with bcrypt-hashed passwords
- **JWT Login** — `POST /token` returns a signed Bearer token
- **Protected Endpoints** — All item routes require `Authorization: Bearer <token>`
- **Full CRUD** — Create, Read, Update, Delete for both Users and Items
- **Auto Docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
- **Docker Ready** — Multi-stage `Dockerfile` + `docker-compose.yml`
- **Config via `.env`** — All secrets and settings are environment-driven

---

## Project Structure

```
simple-rest-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app factory, CORS, routers
│   ├── config.py        # Settings via pydantic-settings (.env)
│   ├── db.py            # SQLAlchemy engine, session, init_db
│   ├── models.py        # ORM models: User, Item
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT creation/decode, bcrypt, dependencies
│   └── routers/
│       ├── __init__.py
│       ├── users.py     # POST /users, POST /token, GET/PUT/DELETE /users
│       └── items.py     # Full CRUD: POST/GET/PUT/DELETE /items
├── .env.example         # Environment variable template
├── .gitignore
├── Dockerfile           # Multi-stage build (builder + runtime)
├── docker-compose.yml
├── requirements.txt
└── LICENSE
```

---

## Quick Start (Local)

### 1. Clone the repo

```bash
git clone https://github.com/AE707/simple-rest-api.git
cd simple-rest-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY:
# python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API is now live at **http://localhost:8000**
Swagger UI: **http://localhost:8000/docs**

---

## Quick Start (Docker)

```bash
# Build and start
docker compose up --build

# Start in background
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f api
```

---

## API Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/users` | No | Register a new user |
| `POST` | `/token` | No | Login — returns JWT token |

### Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/users` | No | List all users (paginated) |
| `GET` | `/users/me` | Yes | Get current user |
| `GET` | `/users/{id}` | No | Get user by ID |
| `PUT` | `/users/me` | Yes | Update current user |
| `DELETE` | `/users/me` | Yes | Delete current user |

### Items (all protected)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/items` | Yes | Create a new item |
| `GET` | `/items` | Yes | List your items (paginated) |
| `GET` | `/items/{id}` | Yes | Get item by ID |
| `PUT` | `/items/{id}` | Yes | Update an item |
| `DELETE` | `/items/{id}` | Yes | Delete an item |

### Health

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | No | Health check |

---

## Usage Examples (curl)

### Register a user

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alaa", "email": "alaa@example.com", "password": "secret123"}'
```

### Login and get token

```bash
curl -X POST http://localhost:8000/token \
  -d "username=alaa&password=secret123"
```

### Use token to create an item

```bash
curl -X POST http://localhost:8000/items \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My first item", "description": "Hello world"}'
```

### Get all your items

```bash
curl http://localhost:8000/items \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Simple REST API` | Application name |
| `APP_VERSION` | `1.0.0` | Application version |
| `DATABASE_URL` | `sqlite:///./app.db` | SQLAlchemy DB URL |
| `SECRET_KEY` | *(change this!)* | JWT signing secret |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime in minutes |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI 0.110 |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (default) / MySQL (optional) |
| Validation | Pydantic v2 |
| Auth | JWT (`python-jose`) |
| Hashing | bcrypt (`passlib`) |
| Config | `pydantic-settings` |
| Container | Docker (multi-stage) |

---

## License

MIT License — see [LICENSE](LICENSE) for details.
