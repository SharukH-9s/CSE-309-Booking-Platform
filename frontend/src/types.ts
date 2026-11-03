export interface Event {
  id: number
  title: string
  description: string | null
  location: string
  event_date: string
  created_at: string
}

export interface EventForm {
  title: string
  description: string
  location: string
  event_date: string
}

