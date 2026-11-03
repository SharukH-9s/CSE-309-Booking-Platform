import { Event, EventForm } from "./types"

const BASE = "/api"

export async function getEvents(): Promise<Event[]> {
  const res = await fetch(`${BASE}/events`)
  if (!res.ok) throw new Error("Failed to fetch events")
  return res.json()
}

export async function getEvent(id: number): Promise<Event> {
  const res = await fetch(`${BASE}/events/${id}`)
  if (!res.ok) throw new Error("Event not found")
  return res.json()
}

export async function createEvent(data: EventForm): Promise<Event> {
  const res = await fetch(`${BASE}/events`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error("Failed to create event")
  return res.json()
}

export async function updateEvent(id: number, data: Partial<EventForm>): Promise<Event> {
  const res = await fetch(`${BASE}/events/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error("Failed to update event")
  return res.json()
}

export async function deleteEvent(id: number): Promise<void> {
  const res = await fetch(`${BASE}/events/${id}`, { method: "DELETE" })
  if (!res.ok) throw new Error("Failed to delete event")
}

