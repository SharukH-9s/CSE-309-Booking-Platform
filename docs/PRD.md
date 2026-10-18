# Product Requirements Document (PRD)

## Project Name: Event Booking Platform
**Course:** CSE-309 Web Engineering  
**Project Type:** Course Project  
**Tech Stack:** FastAPI (Python), React + TypeScript (Vite), SQLite / SQLAlchemy, Vercel  

---

## 1. Project Overview

The Event Booking Platform is a web app for managing and booking events on campus or locally. It allows students and visitors to discover upcoming events, check ticket availability, and reserve seats. 

The application has four user roles:
- **Visitor:** Anyone visiting the site who wants to browse events and check ticket prices without logging in.
- **User:** A registered student or attendee who logs in, books tickets, and can see their booking history.
- **Event Manager:** An organizer assigned to a particular event to set up ticket types, dates, prices, and view the attendee list.
- **Admin:** System administrator who can create and manage all events, assign managers to events, and view platform-wide bookings.

The project is planned in two milestone stages for the semester:
1. **MVP (Mid-Term):** Core REST APIs running locally, event and ticket CRUD, basic seat booking with quantity checks, and initial frontend integration.
2. **Beta (Final):** User accounts with JWT authentication, role-based access control (Admin, Manager, User), manager assignment, user dashboards, and deployment on Vercel.

---

## 2. Release Roadmap

| Milestone | Target | What's Included |
|---|---|---|
| **MVP** | Mid-Term Demo | Local FastAPI backend + React frontend. Create, read, update, delete events. Add and delete tickets per event. Book tickets with inventory decrement. Public list of bookings for testing. |
| **Beta** | Final Demo | User registration and login using JWT. Role permissions (Admin, Manager, User). Admins assign managers to specific events. Managers manage only their own events. User dashboard showing "My Bookings". Deployed live on Vercel. |

---

## 3. Target Users

The platform is designed for four primary target user roles:

### 3.1 Visitor (Unauthenticated)
- View list of published events on the homepage. `[MVP]`
- Open an event to see date, venue, description, and available ticket types. `[MVP]`
- Register for a new account. `[Beta]`

### 3.2 Regular User (Student / Attendee)
- Log in and log out of their account. `[Beta]`
- Browse upcoming events and filter by date. `[MVP]`
- Book available tickets for an event. `[MVP: guest booking / Beta: authenticated]`
- View past and upcoming ticket reservations in their profile dashboard. `[Beta]`

### 3.3 Event Manager
- View the specific events assigned to them by an admin. `[Beta]`
- Add ticket tiers (e.g. Early Bird, Regular, VIP) with prices, dates, and seat quantities. `[MVP: open API / Beta: restricted to assigned event]`
- Delete ticket tiers for their event. `[MVP: open API / Beta: restricted]`
- View the list of people who booked tickets for their event. `[MVP: open API / Beta: restricted]`

### 3.4 Admin
- Create new events, edit event details, or delete events. `[MVP: open API / Beta: admin only]`
- Assign registered users as managers for specific events. `[Beta]`
- View all bookings across every event on the platform. `[MVP: open API / Beta: admin only]`
- Access the admin panel to manage events and user roles. `[Beta]`

---

## 4. User Stories

### 4.1 Visitor
- **US-01:** As a visitor, I want to see a list of upcoming events on the homepage so I know what events are taking place.
- **US-02:** As a visitor, I want to view an event's details (date, venue, description, ticket prices) so I can decide if I want to go.
- **US-03:** As a visitor, I want to sign up with my email and password so that I can have an account for booking tickets. `[Beta]`

### 4.2 Regular User
- **US-04:** As a registered user, I want to log in securely so that my bookings are saved to my account. `[Beta]`
- **US-05:** As a user, I want to filter events by date so I can quickly find something happening on a specific day.
- **US-06:** As a user, I want to select ticket type and quantity to book my seat before tickets run out.
- **US-07:** As a user, I want a "My Bookings" page so I can look up tickets I previously reserved. `[Beta]`

### 4.3 Event Manager
- **US-08:** As an event manager, I want to see only the events assigned to me so I can focus on managing my own events. `[Beta]`
- **US-09:** As an event manager, I want to add ticket tiers with specific quantities and prices so attendees can buy them.
- **US-10:** As an event manager, I want to delete ticket tiers if plans change or if an option is no longer offered.
- **US-11:** As an event manager, I want to see who has booked tickets for my event so I can track attendance.

### 4.4 Admin
- **US-12:** As an admin, I want to create, edit, and delete events so the event list stays up to date.
- **US-13:** As an admin, I want to assign a user as the manager of an event so they can handle ticket setup.
- **US-14:** As an admin, I want to view all bookings across all events to keep track of overall platform activity.
- **US-15:** As an admin, I want an admin panel in the UI so I can handle event management without manually calling APIs. `[Beta]`

---

## 5. Feature Specifications

### Feature 1: Event Management
- **Description:** Basic CRUD operations for events (title, description, location, date).
- **MVP:** Endpoints to create, view, edit, and delete events (`GET /api/events`, `POST /api/events`, `PUT /api/events/{id}`, `DELETE /api/events/{id}`). Simple React view to test creating and displaying events.
- **Beta:** Lock down event creation, editing, and deletion to Admin users only. Admin can select a registered user and assign them as the event's manager.

### Feature 2: Ticket Management
- **Description:** Adding and removing ticket tiers for an event with price and seat quotas.
- **MVP:** Endpoints to add and remove tickets linked to an event (`GET /api/events/{id}/tickets`, `POST /api/events/{id}/tickets`, `DELETE /api/tickets/{id}`). Tracks `total_quantity` and `available_quantity`.
- **Beta:** Permission check ensuring only the assigned event manager (or an admin) can add or delete tickets for that event.

### Feature 3: Ticket Booking
- **Description:** Reserving tickets for an event and keeping inventory accurate.
- **MVP:** Public booking endpoint (`POST /api/bookings`). When a booking is submitted, the backend verifies enough seats remain, decrements `available_quantity`, and creates a booking record. If seats run out, it returns an error.
- **Beta:** Bookings require user login and are tied to the authenticated `user_id`. Prevents booking when `available_quantity` is 0.

### Feature 4: Booking Lists and Attendee Tracking
- **Description:** Viewing reservation records.
- **MVP:** Public endpoint (`GET /api/bookings`) to view all current bookings with ticket and event info.
- **Beta:** 
  - Admins can view all platform bookings.
  - Managers can only view bookings for events they are assigned to.
  - Normal users can view their own booking history (`GET /api/bookings/my-bookings`).

### Feature 5: User Authentication `[Beta]`
- **Description:** User signup, login, and token generation.
- **Endpoints:** `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`.
- **Details:** Passwords hashed with bcrypt. Returns a JWT token stored on the client side (`localStorage`) to authenticate subsequent requests. Roles are `admin`, `manager`, and `user`.

### Feature 6: Vercel Deployment `[Beta]`
- **Description:** Deploy the full-stack app on Vercel using `vercel.json`, routing `/api/*` to the FastAPI backend and all other routes to the React build.

---

## 6. Non-Functional Goals
- **Code Simplicity:** Keep the project clean and easy to follow so our team can easily explain every part during the demo.
- **Data Integrity:** Prevent overselling by validating ticket quantity inside a database transaction before confirming a booking.
- **Clean Structure:** Keep backend (`backend/`) and frontend (`frontend/`) code cleanly separated in the repository.

---

## 7. Success Metrics

| Goal | Success Criteria | Target Milestone |
|---|---|---|
| Working Event CRUD | Events can be created, viewed, edited, and deleted via API and frontend | MVP |
| Ticket Setup | Ticket tiers can be added to an event with date, price, and total seats | MVP |
| Accurate Inventory | Booking reduces `available_quantity` by the requested amount | MVP |
| Prevent Overselling | Requests for more tickets than available are rejected with HTTP 400 | MVP |
| View Bookings | Bookings can be listed showing attendee name, event, and ticket tier | MVP |
| Frontend-Backend Connection | React frontend fetches data from FastAPI and completes a booking flow | MVP |
| User Signup & Login | Users can register and log in; system returns a valid JWT token | Beta |
| Password Security | Passwords are saved as bcrypt hashes in SQLite, never plaintext | Beta |
| Role Permissions | Admins, Managers, and Users can only access their allowed endpoints | Beta |
| Manager Scoping | Managers only have access to modify tickets and see attendees for their assigned events | Beta |
| My Bookings View | Logged-in users can view their personal booking history | Beta |
| Live Deployment | Whole project builds and runs successfully on Vercel | Beta |

---

## 8. Out of Scope
- Real payment gateway integration (Stripe, bKash, etc.) — all bookings are treated as free/mock checkouts.
- Generating downloadable PDF tickets or QR codes.
- Sending email/SMS confirmation messages.
- Handling ticket refunds or cancellations.
