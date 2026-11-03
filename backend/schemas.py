from datetime import datetime
from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    location: str
    event_date: str


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    event_date: str | None = None


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None
    location: str
    event_date: str
    created_at: datetime

    model_config = {"from_attributes": True}

