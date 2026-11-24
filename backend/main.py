from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # Register all SQLAlchemy models before creating tables.
from database import Base, SessionLocal, engine, migrate_event_manager_column
from middleware import RBACMiddleware
from routers.auth import router as auth_router
from routers.admin import router as admin_router
from routers.bookings import router as bookings_router
from routers.events import router as events_router
from routers.managers import router as managers_router
from services.auth_service import seed_admin


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Create missing tables for a new PostgreSQL database.
    Base.metadata.create_all(bind=engine)
    migrate_event_manager_column()
    with SessionLocal() as db:
        seed_admin(db)
    yield


app = FastAPI(
    title="Event Booking Platform",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RBACMiddleware)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(events_router)
app.include_router(bookings_router)
app.include_router(managers_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
