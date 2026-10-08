# Technical Design Document (TDD)

## Project Name: Event Booking Platform (TBD)
**Course:** CSE-309  
**Type:** Student Project  
**Stack:** FastAPI, React (TypeScript), SQLite / SQLAlchemy, Vercel  

---

## 1. System Architecture

The project is structured as a full-stack monorepo:
- **Frontend (`frontend/`):** React 19 + TypeScript + Vite. Communicates with backend endpoints at `/api/*`.
- **Backend (`backend/`):** FastAPI application with SQLAlchemy ORM and SQLite database (`events.db`).
- **Deployment (`vercel.json`):** Unified hosting where requests to `/api/(.*)` route to `backend/main.py` and all other paths serve the React build.

- **Architecture Flow:** Client Browser -> Vercel Router -> `/api/*` routes to FastAPI Backend (with SQLite `events.db`), while all frontend routes serve the React SPA build.

---

## 2. Database Schema (SQLite / SQLAlchemy)

### 2.1 Table: `users` `[Beta]`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `name` | String | Not Null | User full name |
| `email` | String | Unique, Not Null | Login email |
| `hashed_password`| String | Not Null | Bcrypt hashed password |
| `role` | String | Default: 'user' | `'admin'`, `'manager'`, or `'user'` |
| `created_at` | DateTime | Default: UTC now | Account creation timestamp |

*(Note for MVP: A default mock user record can be used for booking associations prior to Beta auth).*

### 2.2 Table: `events` `[MVP / Beta]`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique event identifier |
| `title` | String | Not Null | Event title |
| `description` | Text | Nullable | Detailed event description |
| `location` | String | Not Null | Venue or online link |
| `event_date` | String / DateTime | Not Null | Date and time of the event |
| `manager_id` | Integer | Foreign Key (`users.id`), Nullable | Assigned event manager `[Beta]` |
| `created_at` | DateTime | Default: UTC now | Event creation timestamp |

### 2.3 Table: `tickets` `[MVP]`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique ticket identifier |
| `event_id` | Integer | Foreign Key (`events.id`), Not Null | Associated event |
| `ticket_type` | String | Not Null | E.g., "General Admission", "VIP" |
| `price` | Float | Default: 0.0 | Ticket price |
| `date` | String | Not Null | Date of validity |
| `total_quantity` | Integer | Not Null | Maximum capacity |
| `available_quantity`| Integer | Not Null | Remaining available seats |

### 2.4 Table: `bookings` `[MVP / Beta]`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique booking identifier |
| `user_id` | Integer | Foreign Key (`users.id`), Nullable in MVP | Attendee user ID `[Beta]` |
| `user_name` | String | Not Null | Attendee name (manual in MVP, profile in Beta) |
| `user_email` | String | Not Null | Attendee email |
| `ticket_id` | Integer | Foreign Key (`tickets.id`), Not Null | Reserved ticket reference |
| `quantity` | Integer | Not Null, Default: 1 | Number of tickets booked |
| `booking_date` | DateTime | Default: UTC now | Timestamp of reservation |

---

## 3. REST API Specification

### 3.1 Authentication Endpoints `[Beta]`
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/register` | Create a new user account | Public |
| `POST` | `/api/auth/login` | Validate credentials and return JWT | Public |
| `GET` | `/api/auth/me` | Return currently logged-in user details | Authenticated |

### 3.2 Event Endpoints
| Method | Endpoint | Release | Access | Description |
|---|---|---|---|---|
| `GET` | `/api/events` | **MVP** | Public | List all upcoming events |
| `GET` | `/api/events/{id}` | **MVP** | Public | Get single event details with tickets |
| `POST` | `/api/events` | **MVP** (open) / **Beta** | Admin | Create a new event |
| `PUT` | `/api/events/{id}` | **MVP** (open) / **Beta** | Admin | Update event details |
| `DELETE` | `/api/events/{id}` | **MVP** (open) / **Beta** | Admin | Delete an event |
| `PUT` | `/api/events/{id}/assign-manager` | **Beta** | Admin | Assign a manager user to an event |

### 3.3 Ticket Endpoints
| Method | Endpoint | Release | Access | Description |
|---|---|---|---|---|
| `GET` | `/api/events/{id}/tickets` | **MVP** | Public | List all tickets for an event |
| `POST` | `/api/events/{id}/tickets` | **MVP** (open) / **Beta** | Manager / Admin | Add ticket tier & stock for a date |
| `DELETE` | `/api/tickets/{ticket_id}` | **MVP** (open) / **Beta** | Manager / Admin | Remove ticket tier |

### 3.4 Booking Endpoints
| Method | Endpoint | Release | Access | Description |
|---|---|---|---|---|
| `POST` | `/api/bookings` | **MVP** | Public (MVP) / User (Beta) | Book ticket(s) and decrement stock |
| `GET` | `/api/bookings` | **MVP** (all) / **Beta** | Admin & Manager | View booking list (filtered by role) |
| `GET` | `/api/bookings/my-bookings` | **Beta** | User | View personal booking history |

---

## 4. Business Logic & Security Workflow

### 4.1 Ticket Booking Flow (Inventory Protection)
1. Client sends `POST /api/bookings` with `{ ticket_id, quantity, user_name, user_email }`.
2. Backend queries the ticket record with a database transaction.
3. If `available_quantity < quantity`, return HTTP `400 Bad Request` ("Not enough tickets available").
4. Decrement `available_quantity = available_quantity - quantity`.
5. Insert new row in `bookings`.
6. Commit transaction and return booking confirmation.

### 4.2 Role-Based Access Control (RBAC) `[Beta]`
FastAPI dependency injection checks user permissions on protected endpoints:
- A dependency validates the JWT bearer token and extracts the user record.
- The user's role is checked against permitted roles for the action, returning HTTP 403 Forbidden if not authorized.
- **Admin:** Has full access to `/api/events` mutations and manager assignment.
- **Manager:** Authorized if `event.manager_id == current_user.id` or `current_user.role == 'admin'`.
- **User:** Can book tickets and access `/api/bookings/my-bookings`.

---

## 5. Frontend Architecture

### 5.1 Page Breakdown
- **Event Catalog (`/`):** Public browsing view of all active events. `[MVP]`
- **Event Detail Page (`/events/:id`):** Shows event info, available dates/tickets, and booking modal/form. `[MVP]`
- **Admin Panel (`/admin`):** Forms to create/edit/delete events and assign managers. `[MVP basic UI / Beta RBAC]`
- **Manager Panel (`/manager`):** Interface for managers to view their assigned events, add/delete tickets, and inspect attendees. `[MVP basic UI / Beta RBAC]`
- **Login / Register Modal (`/login`, `/register`):** User onboarding and session token storage in `localStorage`. `[Beta]`
- **User Profile Dashboard (`/profile`):** Displays user details and their active bookings. `[Beta]`

---

## 6. Implementation Milestones

### Milestone 1: MVP (Mid-Term Demo)
1. **Backend Database:** Setup SQLite engine and SQLAlchemy models for `Event`, `Ticket`, and `Booking`.
2. **Backend Routes:** Implement CRUD for events, ticket creation/deletion, and booking creation with stock validation.
3. **Swagger Verification:** Verify all endpoints work via `/docs`.
4. **Basic Frontend UI:** Simple React pages to list events, create events, add tickets, and execute bookings.

### Milestone 2: Beta (Final Demo)
1. **User Model & Passwords:** Add `User` model, bcrypt hashing, and JWT creation/decoding utilities.
2. **RBAC Guarding:** Protect Admin and Manager routes with FastAPI dependency scopes.
3. **Manager Assignment:** Add UI and endpoint for Admin to assign a manager to an event.
4. **User Profile Dashboard:** Show booked tickets for the logged-in user.
5. **Deployment:** Finalize monorepo deployment on Vercel and verify production URLs.

---

## 7. Testing Strategy

### 7.1 Automated Backend Tests (pytest + FastAPI TestClient)
- **Ticket Stock Test:** Attempt to book more tickets than available and assert HTTP 400.
- **Cascade Delete Test:** Delete an event and ensure related tickets are cleaned up.
- **RBAC Test `[Beta]`:** Confirm a standard user cannot create events or delete tickets.

### 7.2 Manual Verification Checklist
1. Create an event -> Confirm it displays on the home catalog.
2. Add a ticket tier with 5 seats -> Verify count displays as 5.
3. Book 2 tickets -> Verify remaining count becomes 3.
4. Check Admin/Manager booking list -> Verify booking appears with correct contact details.
