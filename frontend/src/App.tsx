import { useState, useEffect, FormEvent } from "react"
import { Event, EventForm } from "./types"
import { getEvents, getEvent, createEvent, updateEvent, deleteEvent } from "./api"

type View = "list" | "detail" | "create" | "edit"

const emptyForm: EventForm = { title: "", description: "", location: "", event_date: "" }

export default function App() {
  const [view, setView] = useState<View>("list")
  const [events, setEvents] = useState<Event[]>([])
  const [selected, setSelected] = useState<Event | null>(null)
  const [form, setForm] = useState<EventForm>(emptyForm)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (view === "list") loadEvents()
  }, [view])

  async function loadEvents() {
    setLoading(true)
    try {
      const data = await getEvents()
      setEvents(data)
    } catch {
      setError("Could not load events.")
    }
    setLoading(false)
  }

  async function openDetail(id: number) {
    setError("")
    try {
      const event = await getEvent(id)
      setSelected(event)
      setView("detail")
    } catch {
      setError("Could not load event.")
    }
  }

  function openCreate() {
    setForm(emptyForm)
    setError("")
    setView("create")
  }

  function openEdit() {
    if (!selected) return
    setForm({
      title: selected.title,
      description: selected.description ?? "",
      location: selected.location,
      event_date: selected.event_date,
    })
    setError("")
    setView("edit")
  }

  async function handleCreate(e: FormEvent) {
    e.preventDefault()
    setError("")
    try {
      await createEvent(form)
      setView("list")
    } catch {
      setError("Failed to create event.")
    }
  }

  async function handleUpdate(e: FormEvent) {
    e.preventDefault()
    if (!selected) return
    setError("")
    try {
      await updateEvent(selected.id, form)
      setView("list")
    } catch {
      setError("Failed to update event.")
    }
  }

  async function handleDelete() {
    if (!selected) return
    if (!confirm("Delete this event?")) return
    setError("")
    try {
      await deleteEvent(selected.id)
      setSelected(null)
      setView("list")
    } catch {
      setError("Failed to delete event.")
    }
  }

  function handleField(field: keyof EventForm, value: string) {
    setForm({ ...form, [field]: value })
  }

  if (view === "list") {
    return (
      <div className="container">
        <h1>Event Booking Platform</h1>
        <button onClick={openCreate}>+ Add Event</button>
        {error && <p className="error">{error}</p>}
        {loading && <p>Loading...</p>}
        {!loading && events.length === 0 && <p>No events yet.</p>}
        {events.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Location</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {events.map((ev) => (
                <tr key={ev.id}>
                  <td>{ev.title}</td>
                  <td>{ev.location}</td>
                  <td>{ev.event_date}</td>
                  <td>
                    <button onClick={() => openDetail(ev.id)}>View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    )
  }

  if (view === "detail" && selected) {
    return (
      <div className="container">
        <button onClick={() => setView("list")}>← Back</button>
        <h2>{selected.title}</h2>
        <p><strong>Location:</strong> {selected.location}</p>
        <p><strong>Date:</strong> {selected.event_date}</p>
        {selected.description && <p><strong>Description:</strong> {selected.description}</p>}
        <p><strong>Created:</strong> {new Date(selected.created_at).toLocaleDateString()}</p>
        {error && <p className="error">{error}</p>}
        <div className="actions">
          <button onClick={openEdit}>Edit</button>
          <button className="danger" onClick={handleDelete}>Delete</button>
        </div>
      </div>
    )
  }

  if (view === "create" || view === "edit") {
    return (
      <div className="container">
        <button onClick={() => setView(view === "edit" ? "detail" : "list")}>← Back</button>
        <h2>{view === "create" ? "Add Event" : "Edit Event"}</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={view === "create" ? handleCreate : handleUpdate}>
          <div className="field">
            <label>Title</label>
            <input
              value={form.title}
              onChange={(e) => handleField("title", e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Location</label>
            <input
              value={form.location}
              onChange={(e) => handleField("location", e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Date</label>
            <input
              type="date"
              value={form.event_date}
              onChange={(e) => handleField("event_date", e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Description</label>
            <textarea
              value={form.description}
              onChange={(e) => handleField("description", e.target.value)}
              rows={3}
            />
          </div>
          <button type="submit">{view === "create" ? "Create Event" : "Save Changes"}</button>
        </form>
      </div>
    )
  }

  return null
}
