import {
  AdminStats,
  Booking,
  Event,
  EventForm,
  ManagerForm,
  PasswordChange,
  TokenResponse,
  User,
  UserCredentials,
  UserProfileUpdate,
  UserRegistration,
} from "./types"

const BASE = "/api"
const PUBLIC_AUTH_PATHS = new Set(["/auth/login", "/auth/register", "/auth/refresh", "/auth/logout"])
let refreshInFlight: Promise<string | null> | null = null

export function setTokens(accessToken: string | null, refreshToken: string | null = null) {
  if (accessToken) localStorage.setItem("access_token", accessToken)
  else localStorage.removeItem("access_token")
  if (refreshToken) localStorage.setItem("refresh_token", refreshToken)
  else localStorage.removeItem("refresh_token")
}

async function refreshAccessToken(): Promise<string | null> {
  if (!refreshInFlight) {
    refreshInFlight = (async () => {
      const refreshToken = localStorage.getItem("refresh_token")
      if (!refreshToken) return null

      try {
        const response = await fetch(`${BASE}/auth/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken }),
        })
        if (!response.ok) {
          setTokens(null)
          return null
        }
        const tokens: TokenResponse = await response.json()
        setTokens(tokens.access_token, tokens.refresh_token)
        return tokens.access_token
      } catch {
        setTokens(null)
        return null
      }
    })().finally(() => {
      refreshInFlight = null
    })
  }
  return refreshInFlight
}

async function fetchWithToken(path: string, init: RequestInit, token: string | null): Promise<Response> {
  const headers = new Headers(init.headers)
  if (token) headers.set("Authorization", `Bearer ${token}`)
  else headers.delete("Authorization")
  if (init.body) headers.set("Content-Type", "application/json")
  return fetch(`${BASE}${path}`, { ...init, headers })
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const usesAccessToken = !PUBLIC_AUTH_PATHS.has(path)
  let token = usesAccessToken ? localStorage.getItem("access_token") : null
  let response = await fetchWithToken(path, init, token)

  if (response.status === 401 && usesAccessToken) {
    token = await refreshAccessToken()
    if (token) response = await fetchWithToken(path, init, token)
  }

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail ?? `Request failed (${response.status})`)
  }
  if (response.status === 204) return undefined as T
  return response.json()
}

export function register(data: UserRegistration): Promise<User> {
  return request("/auth/register", { method: "POST", body: JSON.stringify(data) })
}

export function login(data: UserCredentials): Promise<TokenResponse> {
  return request("/auth/login", { method: "POST", body: JSON.stringify(data) })
}

export function logout(refreshToken: string): Promise<void> {
  return request("/auth/logout", { method: "POST", body: JSON.stringify({ refresh_token: refreshToken }) })
}

export function getMe(): Promise<User> {
  return request("/auth/me")
}

export function updateMe(data: UserProfileUpdate): Promise<User> {
  return request("/auth/me", { method: "PATCH", body: JSON.stringify(data) })
}

export function changePassword(data: PasswordChange): Promise<void> {
  return request("/auth/change-password", { method: "POST", body: JSON.stringify(data) })
}

export function getEvents(): Promise<Event[]> {
  return request("/events")
}

export function getEvent(id: number): Promise<Event> {
  return request(`/events/${id}`)
}

export function createEvent(data: EventForm): Promise<Event> {
  return request("/events", { method: "POST", body: JSON.stringify(data) })
}

export function updateEvent(id: number, data: Partial<EventForm>): Promise<Event> {
  return request(`/events/${id}`, { method: "PUT", body: JSON.stringify(data) })
}

export function deleteEvent(id: number): Promise<void> {
  return request(`/events/${id}`, { method: "DELETE" })
}

export function createManager(data: ManagerForm): Promise<User> {
  return request("/managers", { method: "POST", body: JSON.stringify(data) })
}

export function getAdminUsers(banned?: boolean): Promise<User[]> {
  const query = banned === undefined ? "" : `?banned=${banned}`
  return request(`/admin/users${query}`)
}

export function getAdminStats(): Promise<AdminStats> {
  return request("/admin/stats")
}

export function getAdminBookings(): Promise<Booking[]> {
  return request("/admin/bookings")
}

export function deleteAdminUser(userId: number): Promise<void> {
  return request(`/admin/users/${userId}`, { method: "DELETE" })
}

export function banUser(userId: number): Promise<User> {
  return request(`/admin/users/${userId}/ban`, { method: "POST" })
}

export function unbanUser(userId: number): Promise<void> {
  return request(`/admin/users/${userId}/ban`, { method: "DELETE" })
}

export function bookEvent(eventId: number): Promise<Booking> {
  return request("/bookings", { method: "POST", body: JSON.stringify({ event_id: eventId }) })
}

export function getMyBookings(): Promise<Booking[]> {
  return request("/bookings/my")
}

export function getEventBookings(eventId: number): Promise<Booking[]> {
  return request(`/events/${eventId}/bookings`)
}

export function cancelBooking(bookingId: number): Promise<void> {
  return request(`/bookings/${bookingId}`, { method: "DELETE" })
}
