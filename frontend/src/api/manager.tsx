import { request } from "./client"
import { Booking, ManagerForm, User } from "../types"

export function createManager(data: ManagerForm): Promise<User> {
  return request("/managers", { method: "POST", body: JSON.stringify(data) })
}
export function getEventBookings(eventId: number): Promise<Booking[]> {
  return request(`/events/${eventId}/bookings`)
}
