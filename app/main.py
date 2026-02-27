from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import init_db
from app.routers import items, users


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "A simple REST API built with **FastAPI** + **SQLite**.\n\n"
            "## Features\n"
            "- User registration & login with **JWT Bearer** tokens\n"
            "- Password hashing with **bcrypt**\n"
            "- Full **CRUD** for items (protected endpoints)\n"
            "- Auto-generated **Swagger UI** at `/docs`\n"
            "- **ReDoc** at `/redoc`"
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(users.router)
    app.include_router(items.router)

    # Create tables on startup
    @app.on_event("startup")
    def on_startup():
        init_db()

    @app.get("/", tags=["health"])
    def health_check():
        """Root health-check endpoint."""
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
        }

    return app


app = create_app()
