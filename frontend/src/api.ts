import {
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

export function setToken(token: string | null) {
  if (token) localStorage.setItem("access_token", token)
  else localStorage.removeItem("access_token")
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  const token = localStorage.getItem("access_token")
  if (token) headers.set("Authorization", `Bearer ${token}`)
  if (init.body) headers.set("Content-Type", "application/json")

  const response = await fetch(`${BASE}${path}`, { ...init, headers })
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
