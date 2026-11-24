import { FormEvent, useEffect, useState } from "react"
import {
  changePassword,
  createEvent,
  createManager,
  deleteAdminUser,
  deleteEvent,
  getEvent,
  getAdminUsers,
  getEvents,
  getMe,
  login,
  logout as logoutApi,
  register,
  setTokens,
  updateMe,
  updateEvent,
} from "./api"
import { Event, EventForm, User } from "./types"

type View = "list" | "detail" | "create" | "edit" | "login" | "register" | "manager" | "profile" | "admin"

const emptyEventForm: EventForm = { title: "", description: "", location: "", event_date: "" }

export default function App() {
  const [view, setView] = useState<View>("list")
  const [events, setEvents] = useState<Event[]>([])
  const [adminEvents, setAdminEvents] = useState<Event[]>([])
  const [adminUsers, setAdminUsers] = useState<User[]>([])
  const [selected, setSelected] = useState<Event | null>(null)
  const [eventForm, setEventForm] = useState<EventForm>(emptyEventForm)
  const [user, setUser] = useState<User | null>(null)
  const [error, setError] = useState("")
  const [notice, setNotice] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    if (token) {
      getMe().then(setUser).catch(() => {
        setTokens(null)
        setUser(null)
      })
    }
    void loadEvents()
  }, [])

  async function loadEvents() {
    setLoading(true)
    try {
      setEvents(await getEvents())
      setError("")
    } catch (err) {
      setError(errorMessage(err, "Could not load events."))
    } finally {
      setLoading(false)
    }
  }

  async function openDetail(id: number) {
    setError("")
    try {
      setSelected(await getEvent(id))
      setView("detail")
    } catch (err) {
      setError(errorMessage(err, "Could not load event."))
    }
  }

  function openCreate() {
    setEventForm(emptyEventForm)
    setError("")
    setView("create")
  }

  function openEdit() {
    if (!selected) return
    setEventForm({
      title: selected.title,
      description: selected.description ?? "",
      location: selected.location,
      event_date: selected.event_date,
    })
    setError("")
    setView("edit")
  }

  async function handleEventSubmit(event: FormEvent) {
    event.preventDefault()
    setError("")
    try {
      if (view === "create") await createEvent(eventForm)
      else if (selected) await updateEvent(selected.id, eventForm)
      setView("list")
      await loadEvents()
    } catch (err) {
      setError(errorMessage(err, "Could not save event."))
    }
  }

  async function handleDelete() {
    if (!selected || !confirm("Delete this event?")) return
    setError("")
    try {
      await deleteEvent(selected.id)
      setSelected(null)
      setView("list")
      await loadEvents()
    } catch (err) {
      setError(errorMessage(err, "Could not delete event."))
    }
  }

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const values = new FormData(event.currentTarget)
    try {
      const result = await login({
        email: String(values.get("email")),
        password: String(values.get("password")),
      })
      setTokens(result.access_token, result.refresh_token)
      setUser(result.user)
      setError("")
      setView("list")
      await loadEvents()
    } catch (err) {
      setError(errorMessage(err, "Could not log in."))
    }
  }

  async function handleRegister(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const values = new FormData(event.currentTarget)
    const account = {
      name: String(values.get("name")),
      email: String(values.get("email")),
      phone: String(values.get("phone")),
      password: String(values.get("password")),
    }
    try {
      await register(account)
      const result = await login({ email: account.email, password: account.password })
      setTokens(result.access_token, result.refresh_token)
      setUser(result.user)
      setError("")
      setView("list")
      await loadEvents()
    } catch (err) {
      setError(errorMessage(err, "Could not create account."))
    }
  }

  async function handleManagerCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selected) return
    const values = new FormData(event.currentTarget)
    try {
      await createManager({
        name: String(values.get("name")),
        email: String(values.get("email")),
        phone: String(values.get("phone")) || undefined,
        password: String(values.get("password")),
        event_id: selected.id,
      })
      setSelected(await getEvent(selected.id))
      setView("detail")
      setError("")
    } catch (err) {
      setError(errorMessage(err, "Could not create manager."))
    }
  }

  async function handleProfileUpdate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const values = new FormData(event.currentTarget)
    try {
      const updated = await updateMe({
        name: String(values.get("name")),
        email: String(values.get("email")),
        phone: String(values.get("phone")) || null,
      })
      setUser(updated)
      setError("")
      setNotice("Profile updated.")
    } catch (err) {
      setError(errorMessage(err, "Could not update profile."))
      setNotice("")
    }
  }

  async function handlePasswordChange(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const values = new FormData(event.currentTarget)
    try {
      await changePassword({
        current_password: String(values.get("current_password")),
        new_password: String(values.get("new_password")),
      })
      setTokens(null)
      setUser(null)
      setError("")
      setNotice("Password changed. Please log in again.")
      setView("login")
    } catch (err) {
      setError(errorMessage(err, "Could not change password."))
      setNotice("")
    }
  }

  async function logout() {
    const refreshToken = localStorage.getItem("refresh_token")
    if (refreshToken) {
      try {
        await logoutApi(refreshToken)
      } catch {
        // Clear the local session even when the server is unreachable.
      }
    }
    setTokens(null)
    setUser(null)
    setView("list")
    void loadEvents()
  }

  async function openAdminDashboard() {
    setError("")
    setView("admin")
    try {
      setAdminEvents(await getEvents())
    } catch (err) {
      setError(errorMessage(err, "Could not load events."))
    }
    try {
      setAdminUsers(await getAdminUsers())
    } catch (err) {
      setAdminUsers([])
      setError(errorMessage(err, "Could not load accounts."))
    }
  }

  async function handleAdminDeleteUser(userToDelete: User) {
    if (userToDelete.id === user?.id) return
    if (!confirm(`Delete ${userToDelete.name}'s account?`)) return
    try {
      await deleteAdminUser(userToDelete.id)
      const [users, allEvents] = await Promise.all([getAdminUsers(), getEvents()])
      setAdminUsers(users)
      setAdminEvents(allEvents)
      setError("")
    } catch (err) {
      setError(errorMessage(err, "Could not delete account."))
    }
  }

  function handleEventField(field: keyof EventForm, value: string) {
    setEventForm((current) => ({ ...current, [field]: value }))
  }

  if (view === "login" || view === "register") {
    const isRegister = view === "register"
    return (
      <div className="container">
        <button onClick={() => { setError(""); setView("list") }}>← Back to events</button>
        <h1>{isRegister ? "Create account" : "Log in"}</h1>
        {error && <p className="error">{error}</p>}
        {notice && <p>{notice}</p>}
        <form onSubmit={isRegister ? handleRegister : handleLogin}>
          {isRegister && <div className="field"><label>Name</label><input name="name" required /></div>}
          <div className="field"><label>Email</label><input name="email" type="email" required /></div>
          {isRegister && <div className="field"><label>Phone (optional)</label><input name="phone" /></div>}
          <div className="field"><label>Password</label><input name="password" type="password" minLength={8} required /></div>
          <button type="submit">{isRegister ? "Register" : "Log in"}</button>
        </form>
        <p>
          {isRegister ? "Already have an account? " : "Need an account? "}
          <button className="link-button" onClick={() => { setError(""); setView(isRegister ? "login" : "register") }}>
            {isRegister ? "Log in" : "Register"}
          </button>
        </p>
      </div>
    )
  }

  if (view === "manager" && selected) {
    return (
      <div className="container">
        <button onClick={() => setView("detail")}>← Back to event</button>
        <h2>Create manager for {selected.title}</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleManagerCreate}>
          <div className="field"><label>Name</label><input name="name" required /></div>
          <div className="field"><label>Email</label><input name="email" type="email" required /></div>
          <div className="field"><label>Phone (optional)</label><input name="phone" /></div>
          <div className="field"><label>Initial password</label><input name="password" type="password" minLength={8} required /></div>
          <button type="submit">Create and assign manager</button>
        </form>
      </div>
    )
  }

  if (view === "profile" && user) {
    return (
      <div className="container">
        <button onClick={() => { setError(""); setNotice(""); setView("list") }}>← Back to events</button>
        <h1>Profile</h1>
        {error && <p className="error">{error}</p>}
        {notice && <p>{notice}</p>}
        <h2>Account details</h2>
        <form onSubmit={(event) => void handleProfileUpdate(event)}>
          <div className="field"><label>Name</label><input name="name" defaultValue={user.name} required /></div>
          <div className="field"><label>Email</label><input name="email" type="email" defaultValue={user.email} required /></div>
          <div className="field"><label>Phone</label><input name="phone" defaultValue={user.phone ?? ""} /></div>
          <button type="submit">Save profile</button>
        </form>
        <h2>Change password</h2>
        <form onSubmit={(event) => void handlePasswordChange(event)}>
          <div className="field"><label>Current password</label><input name="current_password" type="password" required /></div>
          <div className="field"><label>New password</label><input name="new_password" type="password" minLength={8} required /></div>
          <button type="submit">Change password</button>
        </form>
      </div>
    )
  }

  if (view === "admin") {
    return (
      <div className="container">
        <button onClick={() => setView("list")}>← Back to events</button>
        <h1>Admin dashboard</h1>
        {error && <p className="error">{error}</p>}
        <h2>Events ({adminEvents.length})</h2>
        {adminEvents.length === 0 ? <p>No events yet.</p> : (
          <table>
            <thead><tr><th>Title</th><th>Location</th><th>Date</th><th>Manager</th></tr></thead>
            <tbody>{adminEvents.map((event) => {
              const manager = adminUsers.find((account) => account.id === event.manager_id)
              return <tr key={event.id}>
                <td>{event.title}</td><td>{event.location}</td><td>{event.event_date}</td>
                <td>{manager ? `${manager.name} (${manager.email})` : "Unassigned"}</td>
              </tr>
            })}</tbody>
          </table>
        )}
        <h2>Accounts ({adminUsers.length})</h2>
        {adminUsers.length === 0 ? <p>No accounts found.</p> : (
          <table>
            <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Role</th><th>Assigned event</th><th></th></tr></thead>
            <tbody>{adminUsers.map((account) => {
              const assignedEvent = account.role === "manager"
                ? adminEvents.find((event) => event.manager_id === account.id)
                : undefined
              return <tr key={account.id}>
                <td>{account.name}</td><td>{account.email}</td><td>{account.phone ?? "—"}</td>
                <td>{account.role}</td><td>{assignedEvent?.title ?? (account.role === "manager" ? "Unassigned" : "—")}</td>
                <td><button
                  className="danger"
                  disabled={account.id === user.id}
                  onClick={() => void handleAdminDeleteUser(account)}
                >Delete</button></td>
              </tr>
            })}</tbody>
          </table>
        )}
      </div>
    )
  }

  if (view === "list") {
    return (
      <div className="container">
        <h1>Event Booking Platform</h1>
        <div className="actions">
          {user ? <><span>{user.name} ({user.role})</span><button onClick={() => { setError(""); setNotice(""); setView("profile") }}>Profile</button><button onClick={() => void openAdminDashboard()}>Admin dashboard</button><button onClick={() => void logout()}>Log out</button></> : <>
            <button onClick={() => { setError(""); setView("login") }}>Log in</button>
            <button onClick={() => { setError(""); setView("register") }}>Register</button>
          </>}
          <button onClick={openCreate}>+ Add Event</button>
        </div>
        {error && <p className="error">{error}</p>}
        {loading && <p>Loading...</p>}
        {!loading && events.length === 0 && <p>No events yet.</p>}
        {events.length > 0 && (
          <table>
            <thead><tr><th>Title</th><th>Location</th><th>Date</th><th></th></tr></thead>
            <tbody>{events.map((event) => (
              <tr key={event.id}>
                <td>{event.title}</td><td>{event.location}</td><td>{event.event_date}</td>
                <td><button onClick={() => void openDetail(event.id)}>View</button></td>
              </tr>
            ))}</tbody>
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
        {error && <p className="error">{error}</p>}
        <div className="actions">
          <button onClick={openEdit}>Edit</button>
          <button className="danger" onClick={() => void handleDelete()}>Delete</button>
        </div>
        {selected.manager_id === null && (
          <button onClick={() => { setError(""); setView("manager") }}>Assign manager</button>
        )}
      </div>
    )
  }

  if (view === "create" || view === "edit") {
    return (
      <div className="container">
        <button onClick={() => setView(view === "edit" ? "detail" : "list")}>← Back</button>
        <h2>{view === "create" ? "Add Event" : "Edit Event"}</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={(event) => void handleEventSubmit(event)}>
          <div className="field"><label>Title</label><input value={eventForm.title} onChange={(e) => handleEventField("title", e.target.value)} required /></div>
          <div className="field"><label>Location</label><input value={eventForm.location} onChange={(e) => handleEventField("location", e.target.value)} required /></div>
          <div className="field"><label>Date</label><input type="date" value={eventForm.event_date} onChange={(e) => handleEventField("event_date", e.target.value)} required /></div>
          <div className="field"><label>Description</label><textarea value={eventForm.description} onChange={(e) => handleEventField("description", e.target.value)} rows={3} /></div>
          <button type="submit">{view === "create" ? "Create Event" : "Save Changes"}</button>
        </form>
      </div>
    )
  }

  return <div className="container"><p>You do not have access to this action.</p><button onClick={() => setView("list")}>Back to events</button></div>
}

function errorMessage(error: unknown, fallback: string): string {
  return error instanceof Error ? error.message : fallback
}
