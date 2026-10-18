# Software Requirements Specification (SRS)

## Project Name: Event Booking Platform
**Course:** CSE-309 Web Engineering  
**Project Type:** Course Project  
**Target Milestones:** MVP (Mid-Term Demo) & Beta (Final Demo)  

---

## 1. Introduction

### 1.1 Purpose
This document outlines the software requirements for the Event Booking Platform. The app allows users to browse campus events, book tickets, and manage reservations, while providing organizers and administrators with tools to manage event details and seat inventory.

### 1.2 Scope
The system is built as a single-page React frontend connected to a FastAPI backend with SQLite storage. The project deliverables are split into two phases:
- **MVP (Mid-Term):** Core CRUD endpoints for events and tickets, basic seat booking with quantity checks, and unauthenticated frontend testing.
- **Beta (Final):** User registration and login (JWT), role-based permissions (Admin, Manager, User), manager assignment to events, personal booking dashboards, and deployment on Vercel.

---

## 2. Technology Stack

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic
- **Frontend:** React 19, TypeScript, Vite, CSS
- **Authentication (Beta):** JWT (JSON Web Tokens) with passlib / bcrypt password hashing
- **Deployment (Beta):** Vercel (monorepo setup using `vercel.json`)

---

## 3. User Classes and Characteristics

| Role | Description |
|---|---|
| **Visitor** | Anyone visiting the website without an account. Can browse published events and check ticket availability. |
| **User** | Registered student or attendee. Can log in, book tickets for events, and view their past bookings. |
| **Manager** | An event organizer assigned to specific events. Can create ticket tiers, set quantities, and see who booked tickets. |
| **Admin** | System administrator. Can create and edit any event, assign managers to events, and view all bookings across the platform. |

---

## 4. Functional Requirements

### 4.1 Event Management
- **FR-1.1: Event Creation `[MVP]`**  
  Admins can create new events by providing title, description, location/venue, and event date.
- **FR-1.2: Event Editing `[MVP]`**  
  Admins can update information (title, description, location, date) for any existing event.
- **FR-1.3: Event Deletion `[MVP]`**  
  Admins can delete an event, which also removes any associated ticket tiers and booking records.
- **FR-1.4: View Events `[MVP]`**  
  Public endpoints allow any user to list all published events and view the details of an individual event.
- **FR-1.5: Assign Event Manager `[Beta]`**  
  Admins can assign a registered user as the manager for a specific event by saving their `user_id` as the event's `manager_id`.
- **FR-1.6: Restrict Event Editing to Admins `[Beta]`**  
  Event creation, updates, and deletion require an authenticated user with the `Admin` role.

### 4.2 Ticket Management
- **FR-2.1: Add Tickets to Events `[MVP]`**  
  Managers can configure ticket tiers for an event, including ticket type (e.g., General, Student, VIP), price, date, and total seat quantity.
- **FR-2.2: Delete Tickets `[MVP]`**  
  Managers can remove a ticket tier from an event.
- **FR-2.3: Seat Inventory Tracking `[MVP]`**  
  The system tracks both `total_quantity` and `available_quantity` for every ticket tier.
- **FR-2.4: Manager Permission Check `[Beta]`**  
  Only the manager assigned to an event (or an Admin) can add or remove tickets for that event.

### 4.3 Ticket Booking
- **FR-3.1: Create Booking `[MVP]`**  
  Users can select a ticket tier, specify the number of tickets, and complete a reservation.
- **FR-3.2: Check Available Seats `[MVP]`**  
  The backend checks remaining seats before confirming a booking. If requested seats exceed `available_quantity`, the request is rejected with HTTP 400.
- **FR-3.3: Automatic Seat Decrement `[MVP]`**  
  When a booking succeeds, `available_quantity` is immediately reduced by the booked count.
- **FR-3.4: Link Bookings to User `[Beta]`**  
  Bookings must be saved with the authenticated user's `user_id`.
- **FR-3.5: User Booking History `[Beta]`**  
  Logged-in users can view their own past bookings via a dedicated endpoint.

### 4.4 Booking Lists & Reporting
- **FR-4.1: View All Bookings (Admin) `[MVP / Beta]`**  
  Admins can view all bookings across the platform, including attendee names, event details, and ticket tiers.
- **FR-4.2: View Event Bookings (Manager) `[Beta]`**  
  Event managers can only view attendee booking lists for the events they manage.

### 4.5 User Accounts & Authentication `[Beta]`
- **FR-5.1: User Registration `[Beta]`**  
  Visitors can sign up with their name, email, and password. New accounts are assigned the `user` role by default.
- **FR-5.2: User Login & JWT `[Beta]`**  
  Users log in with their email and password. Upon successful validation, the backend returns a signed JWT access token.
- **FR-5.3: Role Authorization `[Beta]`**  
  Protected endpoints verify user roles (`Admin`, `Manager`, `User`) and reject unauthorized access with HTTP 403.
- **FR-5.4: User Profile Dashboard `[Beta]`**  
  The frontend includes a profile page showing the user's account info and their reserved tickets.

### 4.6 Deployment & System Integration `[Beta]`
- **FR-6.1: Vercel Monorepo Deployment `[Beta]`**  
  The frontend build and FastAPI serverless backend are deployed together on Vercel using `vercel.json`.

---

## 5. Use Cases

### UC-01: Browse Events (Visitor)
- **Actor:** Visitor
- **Precondition:** The website is running. No account needed.
- **Main Flow:**
  1. Visitor opens the homepage.
  2. The system loads and displays a list of upcoming events.
  3. Visitor clicks on an event card.
  4. The system opens the event details page, showing the description, venue, date, and available ticket options.
- **Postcondition:** The visitor can review all event info and decide whether to book.

### UC-02: Book a Ticket (User)
- **Actor:** Registered User (MVP: guest user; Beta: authenticated user)
- **Precondition:** The event has at least one ticket tier with `available_quantity > 0`.
- **Main Flow:**
  1. User goes to the event details page.
  2. User selects a ticket tier and enters the desired quantity.
  3. User enters attendee name and email (in Beta, auto-filled from login session) and clicks "Book".
  4. Backend verifies that requested tickets <= `available_quantity`.
  5. Backend reduces `available_quantity` and saves the booking record.
  6. Frontend displays a confirmation message with booking details.
- **Alternative Flow:** If requested quantity > `available_quantity`, backend returns HTTP 400 with "Not enough tickets available" and the frontend displays the error.
- **Postcondition:** Booking is saved in the database and remaining seats are reduced.

### UC-03: Create an Event (Admin)
- **Actor:** Admin
- **Precondition (Beta):** Logged in with the `Admin` role.
- **Main Flow:**
  1. Admin opens the Admin Panel.
  2. Admin fills in event title, description, location, and date.
  3. Admin clicks "Create Event".
  4. Backend validates the input and saves the event to the database.
  5. Frontend updates to show the new event in the list.
- **Postcondition:** The new event is visible on the public event list.

### UC-04: Assign an Event Manager (Admin) `[Beta]`
- **Actor:** Admin
- **Precondition:** Admin is logged in. The event and the target user already exist.
- **Main Flow:**
  1. Admin navigates to the event management section.
  2. Admin selects an event and picks a registered user from the user list.
  3. Admin submits the assignment.
  4. Backend updates the event record with `manager_id = user.id`.
- **Postcondition:** The assigned user now has permission to manage tickets and view attendees for that event.

### UC-05: Add Tickets to an Event (Manager)
- **Actor:** Event Manager
- **Precondition (Beta):** Manager is logged in and assigned to the selected event.
- **Main Flow:**
  1. Manager opens the Manager Dashboard and selects their assigned event.
  2. Manager fills out the ticket form (ticket type, price, date, total seats).
  3. Manager clicks "Add Ticket".
  4. Backend verifies the manager is assigned to this event (Beta) and saves the ticket tier.
  5. The new ticket tier appears in the event's ticket list.
- **Postcondition:** Attendees can now see and book this ticket tier.

### UC-06: Register and Log In (User) `[Beta]`
- **Actor:** Visitor
- **Precondition:** User does not already have an account.
- **Main Flow:**
  1. Visitor opens the registration form and enters their name, email, and password.
  2. Backend hashes the password using bcrypt and creates a user record with role `user`.
  3. User goes to the login form and enters email and password.
  4. Backend verifies credentials and returns a JWT token.
  5. Frontend stores the token in `localStorage` for future API calls.
- **Postcondition:** User is logged in and can access authenticated features.

### UC-07: View Booking History (User) `[Beta]`
- **Actor:** Registered User
- **Precondition:** User is logged in.
- **Main Flow:**
  1. User navigates to the "My Bookings" page.
  2. Frontend sends a request to `/api/bookings/my-bookings` with the user's JWT token.
  3. Backend finds all bookings matching the user's `user_id`.
  4. Frontend displays a list of the user's booked tickets and event details.
- **Postcondition:** User can review all tickets they have reserved.

---

## 6. Non-Functional Requirements

### 6.1 Usability
- Clean, responsive layout for browsing events and booking tickets on both desktop and mobile screens.
- User-friendly error messages when actions fail (e.g., "Sold Out", "Invalid email or password", "You do not have permission").

### 6.2 Reliability & Concurrency
- SQLite database transactions during booking creation so two users cannot book the last seat at the exact same moment.
- Keep API endpoints fast (< 200ms response time on local machine).

### 6.3 Security `[Beta]`
- Passwords must be hashed using bcrypt before being saved to SQLite. Plaintext passwords must never be stored.
- Protected API routes require a valid `Authorization: Bearer <token>` header.
- Endpoint-level role checks prevent regular users from accessing manager or admin functions.

---

## 7. Acceptance Criteria

### 7.1 MVP Acceptance Criteria (Mid-Term)
For the mid-term demo, the following items must be working:

| ID | Criterion | How to Verify |
|---|---|---|
| AC-01 | FastAPI backend runs locally on port 8000 without errors | Start with `fastapi dev main.py` or uvicorn |
| AC-02 | Interactive API documentation is accessible at `/docs` | Open `http://localhost:8000/docs` in browser |
| AC-03 | Admin can create, read, update, and delete events via API | Test via Swagger UI or frontend form |
| AC-04 | Ticket tiers can be added to and deleted from an event | Test via Swagger UI or frontend |
| AC-05 | Booking a ticket successfully reduces `available_quantity` in the database | Inspect SQLite database or API response |
| AC-06 | Booking fails with HTTP 400 if requested seats exceed remaining seats | Submit booking with excessive quantity in `/docs` |
| AC-07 | Booking list is viewable at `GET /api/bookings` | Fetch from `/api/bookings` |
| AC-08 | React frontend (port 5173) connects to backend and completes event browsing and booking | Test in browser from `http://localhost:5173` |

### 7.2 Beta Acceptance Criteria (Final Demo)
For the final submission, in addition to the MVP items, the following must be complete:

| ID | Criterion | How to Verify |
|---|---|---|
| AC-09 | New users can sign up; passwords are saved as bcrypt hashes in SQLite | Check database records |
| AC-10 | Registered users can log in and receive a valid JWT token | Test login via Swagger or UI |
| AC-11 | Protected endpoints reject requests without a valid token with HTTP 401 | Send request without Authorization header |
| AC-12 | Admin can assign a registered user as manager for an event | Check `manager_id` in database / UI |
| AC-13 | Managers can only manage tickets and view attendees for their own events (HTTP 403 otherwise) | Test with different manager accounts |
| AC-14 | Regular users can only see their own bookings via `/api/bookings/my-bookings` | Log in as regular user and check response |
| AC-15 | User profile page shows the user's info and active reservations | View profile page in frontend |
| AC-16 | Project builds and runs on Vercel under a single deployment | Verify live URL on Vercel |
