# Product Requirements Document (PRD)

## Project Name: Event Booking Platform (TBD)
**Course:** CSE-309  
**Type:** Student Project  
**Stack:** FastAPI (Python), React + TypeScript (Vite), SQLite / SQLAlchemy, Vercel  

---

## 1. Project Overview
The Event Booking Platform is a lightweight web application that allows users to explore events and book tickets online. The system supports three user roles:
- **Admin:** Manages events, assigns event managers, and views all platform bookings.
- **Manager:** Manages ticket inventory for assigned events and monitors event-specific bookings.
- **User:** Browses events, books tickets, and tracks personal bookings.

The project is structured for a student semester with two milestone releases:
1. **MVP (Mid-Term Demo):** Working local prototype with core CRUD REST APIs and basic frontend interaction.
2. **Beta (Final Demo):** Secure role-based access control (RBAC), user accounts, personal dashboards, and production deployment on Vercel.

---

## 2. Release Roadmap

| Release | Target | Scope |
|---|---|---|
| **MVP** | Mid-Term Demo | Core REST APIs running locally, event CRUD, ticket CRUD, basic ticket booking, public booking list view. |
| **Beta** | Final Demo | User registration and login (JWT), role-based permissions (Admin, Manager, User), manager assignment to events, user profile/booking dashboard, and Vercel cloud deployment. |

---

## 3. User Roles and Capabilities

### 3.1 Visitor / Unauthenticated User
- Browse published events. `[MVP]`
- View event details and ticket availability. `[MVP]`
- Register for an account and log in. `[Beta]`

### 3.2 Regular User
- Log in and manage personal session. `[Beta]`
- Browse upcoming events and filter by date. `[MVP]`
- Book available tickets for an event. `[MVP: mock user / Beta: authenticated user]`
- View personal booking history on a dashboard. `[Beta]`

### 3.3 Event Manager
- View events assigned to them by an Admin. `[Beta]`
- Create tickets for specific dates/tiers for their assigned event. `[MVP: direct API / Beta: role-restricted]`
- Delete tickets for their assigned event. `[MVP: direct API / Beta: role-restricted]`
- View the list of all bookings made for their assigned event. `[MVP: direct API / Beta: role-restricted]`

### 3.4 Admin
- Create, edit, and delete any event. `[MVP: direct API / Beta: role-restricted]`
- Assign a registered user as the manager of a specific event. `[Beta]`
- View all bookings across all platform events. `[MVP: direct API / Beta: role-restricted]`
- Access the Admin management panel. `[Beta]`

---

## 4. Feature Specifications

### Feature 1: Event Management
- **Description:** Allows administrators to create, update, and remove events (title, description, location, date, banner image).
- **MVP Scope:** REST endpoints to create, read, update, and delete events (`GET /api/events`, `POST /api/events`, `PUT /api/events/{id}`, `DELETE /api/events/{id}`). Basic frontend form to test CRUD locally.
- **Beta Scope:** Restrict event creation, editing, and deletion exclusively to the Admin role. Admin assigns an event manager from the user list.

### Feature 2: Ticket Management by Date/Event
- **Description:** Allows event managers to configure tickets (ticket type, price, date, available quantity).
- **MVP Scope:** REST endpoints to add and delete tickets linked to an event ID (`GET /api/events/{id}/tickets`, `POST /api/events/{id}/tickets`, `DELETE /api/tickets/{id}`).
- **Beta Scope:** Manager authorization check ensuring only the assigned manager (or Admin) can add/delete tickets for that specific event.

### Feature 3: Event Browsing and Ticket Booking
- **Description:** Allows users to view upcoming events and reserve tickets.
- **MVP Scope:** Public event catalog and simple booking action that decreases ticket quantity and creates a booking record (`POST /api/bookings`).
- **Beta Scope:** Booking requires an active user session; records are tied to the authenticated `user_id`. Prevents overbooking if remaining ticket count is zero.

### Feature 4: Booking List and Oversight
- **Description:** Viewing attendee and reservation lists.
- **MVP Scope:** Endpoint to retrieve all bookings (`GET /api/bookings`) with event and ticket details.
- **Beta Scope:** 
  - Admin can view all bookings across all events.
  - Managers can only view bookings for events assigned to them.
  - Users can view their own booking history (`GET /api/bookings/my-bookings`).

### Feature 5: Authentication & User Accounts `[Beta]`
- **Description:** Secure user registration, login, and password management.
- **Endpoints:** `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`.
- **Implementation:** Password hashing, JSON Web Tokens (JWT) for session management, and role-based permissions stored in token/database.

### Feature 6: Cloud Deployment `[Beta]`
- **Description:** Live deployment on Vercel using the monorepo configuration (`vercel.json`), serving the React frontend and FastAPI backend under unified routing.

---

## 5. Non-Functional Goals
- **Simplicity:** Keep codebase clean and straightforward for easy grading and demoing.
- **Reliability:** Prevent overselling tickets with basic database validation on available seats.
- **Clean Separation:** Clear folder separation between `backend/` (FastAPI) and `frontend/` (React Vite).

---

## 6. Out of Scope
- Online payment gateway integration (mock/free bookings only).
- QR code / PDF ticket generation.
- Automated email or SMS notifications.
- Ticket refunds and cancellation dispute workflows.
