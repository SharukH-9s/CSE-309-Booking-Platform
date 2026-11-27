import { request } from "./client"
import { AdminStats, Booking, User } from "../types"

export function getAdminUsers(banned?: boolean): Promise<User[]> {
  const query = banned === undefined ? "" : `?banned=${banned}`
  return request(`/admin/users${query}`)
}
export function getAdminStats(): Promise<AdminStats> { return request("/admin/stats") }
export function getAdminBookings(): Promise<Booking[]> { return request("/admin/bookings") }
export function deleteAdminUser(userId: number): Promise<void> {
  return request(`/admin/users/${userId}`, { method: "DELETE" })
}
export function banUser(userId: number): Promise<User> {
  return request(`/admin/users/${userId}/ban`, { method: "POST" })
}
export function unbanUser(userId: number): Promise<void> {
  return request(`/admin/users/${userId}/ban`, { method: "DELETE" })
}
