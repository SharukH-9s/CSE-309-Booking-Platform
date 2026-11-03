from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers.events import router as events_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Booking Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
