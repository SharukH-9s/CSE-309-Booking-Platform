# Software Requirements Specification (SRS)

## Project Name: Event Booking Platform (TBD)
**Course:** CSE-309  
**Type:** Student Project  
**Target Releases:** MVP (Mid-Term Demo) & Beta (Final Demo)  

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for the Event Booking Platform. The system is designed to provide basic event publishing, ticket configuration, and seat booking capabilities for students and administrators.

### 1.2 Scope
The application consists of a single-page React frontend and a FastAPI backend using SQLite for persistence. Requirements are categorized into:
- **MVP (Mid-Term):** Core REST APIs, local database CRUD, and unauthenticated feature testing.
- **Beta (Final):** User authentication, role-based access control (RBAC), user profile dashboard, security scopes, and cloud deployment on Vercel.

---

## 2. Technology Stack

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic.
- **Frontend:** React 19, TypeScript, Vite, Vanilla CSS.
- **Authentication (Beta):** JWT (JSON Web Tokens) with passlib/bcrypt password hashing.
- **Deployment (Beta):** Vercel (monorepo hosting via `vercel.json`).

---

## 3. User Classes and Characteristics

| Role | Description |
|---|---|
| **Visitor** | Public user who can view event listings and details. |
| **User** | Registered student/attendee who can reserve tickets and view booking history. |
| **Manager** | Event organizer assigned to specific events; manages ticket stock and dates. |
| **Admin** | System owner who creates events, assigns managers, and monitors all bookings. |

---

## 4. Functional Requirements

### 4.1 Event Management
- **FR-1.1: Create Event `[MVP]`**  
  The system shall allow creating an event with title, description, location, and date.
- **FR-1.2: Edit Event `[MVP]`**  
  The system shall allow updating event information (title, description, location, date).
- **FR-1.3: Delete Event `[MVP]`**  
  The system shall allow deleting an event and cascading deletion of associated tickets/bookings.
- **FR-1.4: List and Retrieve Events `[MVP]`**  
  The system shall provide public endpoints to list all events and get single event details.
- **FR-1.5: Assign Event Manager `[Beta]`**  
  The system shall allow an Admin to link a specific registered user (`manager_id`) to an event.
- **FR-1.6: Admin-Only Event Mutability `[Beta]`**  
  The system shall restrict event creation, editing, and deletion to users with the `Admin` role.

### 4.2 Ticket Management
- **FR-2.1: Create Tickets by Date/Event `[MVP]`**  
  The system shall allow creating tickets for an event with ticket type (e.g., General, VIP), price, date, and total quantity.
- **FR-2.2: Delete Tickets `[MVP]`**  
  The system shall allow deleting an existing ticket type from an event.
- **FR-2.3: Track Available Quantity `[MVP]`**  
  The system shall maintain `total_quantity` and `available_quantity` for every ticket record.
- **FR-2.4: Manager Ownership Validation `[Beta]`**  
  The system shall only permit the assigned event manager (or Admin) to create or delete tickets for that particular event.

### 4.3 Booking Management
- **FR-3.1: Create Booking `[MVP]`**  
  The system shall allow creating a booking for a selected ticket type and quantity.
- **FR-3.2: Enforce Stock Limits `[MVP]`**  
  The system shall reject any booking request if requested quantity exceeds `available_quantity`.
- **FR-3.3: Automatic Stock Decrement `[MVP]`**  
  The system shall decrement `available_quantity` immediately upon successful booking creation.
- **FR-3.4: User Booking Binding `[Beta]`**  
  The system shall bind bookings to the logged-in user's identity (`user_id`).
- **FR-3.5: User Booking History `[Beta]`**  
  The system shall provide an endpoint for authenticated users to view only their own bookings.

### 4.4 Booking Lists & Reporting
- **FR-4.1: View All Bookings (Admin) `[MVP: open / Beta: restricted]`**  
  The system shall allow the Admin to view all bookings across the platform with user, event, and ticket information.
- **FR-4.2: View Event Bookings (Manager) `[Beta]`**  
  The system shall allow an assigned manager to view attendee booking lists only for events they manage.

### 4.5 User Accounts & Authentication `[Beta]`
- **FR-5.1: User Registration `[Beta]`**  
  The system shall allow new users to register with name, email, and password. Default role assigned is `User`.
- **FR-5.2: User Login & JWT Issuance `[Beta]`**  
  The system shall authenticate users via email and password, returning a JWT bearer token.
- **FR-5.3: Role-Based Authorization Scopes `[Beta]`**  
  The backend shall enforce role checks (`Admin`, `Manager`, `User`) on protected API endpoints.
- **FR-5.4: User Profile Dashboard `[Beta]`**  
  The frontend shall provide a dashboard displaying the user's profile info and booked tickets.

### 4.6 Deployment & System Integration `[Beta]`
- **FR-6.1: Monorepo Deployment `[Beta]`**  
  The system shall build the React frontend and deploy FastAPI serverless functions onto Vercel using `vercel.json`.

---

## 5. Non-Functional Requirements

### 5.1 Usability
- Straightforward UI forms for event creation, ticket setup, and checkout.
- Clear error messages (e.g., "Sold Out", "Invalid Credentials", "Unauthorized").

### 5.2 Performance & Concurrency
- SQLite database transactions for booking creation to prevent race conditions during seat reduction.
- Fast API response times (< 200ms locally).

### 5.3 Security `[Beta]`
- Passwords must be hashed using bcrypt before database storage.
- Protected API routes require standard `Authorization: Bearer <token>` headers.
- Route-level role enforcement to block unauthorized access to manager/admin controls.

---

## 6. Milestone Deliverables & Demo Criteria

### 6.1 Mid-Term Demo (MVP Checklist)
- [ ] FastAPI backend running locally on port 8000.
- [ ] Working REST API endpoints documented in Swagger UI (`/docs`).
- [ ] CRUD operations for Events (Create, Read, Update, Delete).
- [ ] Add and Delete tickets for an event.
- [ ] Book a ticket with automatic inventory deduction and stock validation.
- [ ] View list of all current bookings.
- [ ] Basic React interface running on Vite (`localhost:5173`) connecting to the backend.

### 6.2 Final Demo (Beta Checklist)
- [ ] Complete User Registration and Login flow.
- [ ] JWT authentication and role-based route protection (Admin, Manager, User).
- [ ] Admin panel to assign users as event managers.
- [ ] Manager view restricted only to their assigned events.
- [ ] User profile dashboard showing booked tickets.
- [ ] Public live deployment running on Vercel.
