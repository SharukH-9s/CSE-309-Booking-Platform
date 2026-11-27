import { request } from "./client"
import { Event, EventForm } from "../types"

export function getEvents(): Promise<Event[]> { return request("/events") }
export function getEvent(id: number): Promise<Event> { return request(`/events/${id}`) }
export function createEvent(data: EventForm): Promise<Event> {
  return request("/events", { method: "POST", body: JSON.stringify(data) })
}
export function updateEvent(id: number, data: Partial<EventForm>): Promise<Event> {
  return request(`/events/${id}`, { method: "PUT", body: JSON.stringify(data) })
}
export function deleteEvent(id: number): Promise<void> {
  return request(`/events/${id}`, { method: "DELETE" })
}
