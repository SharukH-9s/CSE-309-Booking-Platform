import { request, setTokens } from "./client"
import { Booking, PasswordChange, TokenResponse, User, UserCredentials, UserProfileUpdate, UserRegistration } from "../types"

export { setTokens }

export function register(data: UserRegistration): Promise<User> {
  return request("/auth/register", { method: "POST", body: JSON.stringify(data) })
}
export function login(data: UserCredentials): Promise<TokenResponse> {
  return request("/auth/login", { method: "POST", body: JSON.stringify(data) })
}
export function logout(refreshToken: string): Promise<void> {
  return request("/auth/logout", { method: "POST", body: JSON.stringify({ refresh_token: refreshToken }) })
}
export function getMe(): Promise<User> { return request("/auth/me") }
export function updateMe(data: UserProfileUpdate): Promise<User> {
  return request("/auth/me", { method: "PATCH", body: JSON.stringify(data) })
}
export function changePassword(data: PasswordChange): Promise<void> {
  return request("/auth/change-password", { method: "POST", body: JSON.stringify(data) })
}
export function bookEvent(eventId: number): Promise<Booking> {
  return request("/bookings", { method: "POST", body: JSON.stringify({ event_id: eventId }) })
}
export function getMyBookings(): Promise<Booking[]> { return request("/bookings/my") }
export function cancelBooking(bookingId: number): Promise<void> {
  return request(`/bookings/${bookingId}`, { method: "DELETE" })
}
