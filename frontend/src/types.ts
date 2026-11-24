export type Role = "admin" | "manager" | "user"

export interface User {
  id: number
  name: string
  email: string
  phone: string | null
  role: Role
  is_banned: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  expires_in: number
  token_type: "bearer"
  user: User
}

export interface UserCredentials {
  email: string
  password: string
}

export interface UserRegistration extends UserCredentials {
  name: string
  phone?: string
}

export interface UserProfileUpdate {
  name?: string
  email?: string
  phone?: string | null
}

export interface PasswordChange {
  current_password: string
  new_password: string
}

export interface ManagerForm extends UserRegistration {
  event_id: number
}

export interface Event {
  id: number
  title: string
  description: string | null
  location: string
  event_date: string
  manager_id: number | null
  created_at: string
}

export interface EventForm {
  title: string
  description: string
  location: string
  event_date: string
}

export interface Booking {
  id: number
  event_id: number
  user_id: number
  created_at: string
  user_name?: string | null
  user_email?: string | null
  event_title?: string | null
  event_date?: string | null
  event_location?: string | null
}
