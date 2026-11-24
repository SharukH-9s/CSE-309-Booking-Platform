export type Role = "admin" | "manager" | "user"

export interface User {
  id: number
  name: string
  email: string
  phone: string | null
  role: Role
  created_at: string
}

export interface TokenResponse {
  access_token: string
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
