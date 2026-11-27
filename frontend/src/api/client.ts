import { TokenResponse } from "../types"

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

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
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
