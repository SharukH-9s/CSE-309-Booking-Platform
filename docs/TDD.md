# Technical Design Document (TDD)

## Project Name: Event Booking Platform
**Course:** CSE-309 Web Engineering  
**Project Type:** Course Project  
**Stack:** FastAPI, React (TypeScript), SQLite / SQLAlchemy, Vercel  

---

## 1. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React 19 + TypeScript + Vite | Single-page application for the user interface |
| **Backend** | Python 3.10+, FastAPI, Pydantic | REST API, data validation, and business logic |
| **Database** | SQLite (`events.db`) | Local file-based SQL database, zero setup needed |
| **ORM** | SQLAlchemy | Models and database queries in Python |
| **Authentication** | JWT (`python-jose`), `passlib[bcrypt]` | Token-based login and secure password hashing |
| **Authorization** | FastAPI Dependencies | Protects endpoints based on user roles (`admin`, `manager`, `user`) |
| **Deployment** | Vercel (`vercel.json`) | Hosts both React frontend and FastAPI backend under one domain |
| **Version Control** | Git + GitHub | Tracking code changes and team collaboration |

---

## 2. System Architecture

The application is structured as a full-stack monorepo with two main folders:
- **`frontend/`:** React 19 single-page app built with Vite. It calls API endpoints at `/api/*`.
- **`backend/`:** FastAPI app that handles database models, API routes, and serves the API on port 8000 during development.
- **`vercel.json`:** Handles routing in production on Vercel: requests starting with `/api/` go to the FastAPI serverless function, and everything else serves the static React build.

### Architecture Overview:
```
User Browser
    │
    ├── /api/* ─────────► FastAPI Backend ───► SQLite (events.db)
    └── (all other routes) ──► React SPA (Vite build)
```

---

## 3. Database Schema (SQLite / SQLAlchemy)

We use SQLite for local persistence with SQLAlchemy ORM.

### 3.1 Table: `users` `[Beta]`
Stores registered accounts and their platform role.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique user ID |
| `name` | String | Not Null | User full name |
| `email` | String | Unique, Not Null | Login email |
| `hashed_password`| String | Not Null | Bcrypt hashed password |
| `role` | String | Default: 'user' | Role: `'admin'`, `'manager'`, or `'user'` |
| `created_at` | DateTime | Default: UTC now | When account was registered |

*(Note for MVP: Before full auth is implemented in Beta, a mock/guest user record is used for bookings).*

### 3.2 Table: `events` `[MVP / Beta]`
Stores all published events.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique event ID |
| `title` | String | Not Null | Event name |
| `description` | Text | Nullable | Event description/details |
| `location` | String | Not Null | Venue name or online link |
| `event_date` | String / DateTime | Not Null | Date and time of the event |
| `manager_id` | Integer | Foreign Key (`users.id`), Nullable | User ID of the assigned manager `[Beta]` |
| `created_at` | DateTime | Default: UTC now | Event creation timestamp |

### 3.3 Table: `tickets` `[MVP]`
Stores ticket tiers configured for each event.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique ticket ID |
| `event_id` | Integer | Foreign Key (`events.id`), Not Null | Event this ticket belongs to |
| `ticket_type` | String | Not Null | Tier name (e.g. "General", "VIP", "Student") |
| `price` | Float | Default: 0.0 | Ticket price |
| `date` | String | Not Null | Date this ticket is valid for |
| `total_quantity` | Integer | Not Null | Total seats available initially |
| `available_quantity`| Integer | Not Null | Seats currently remaining |

### 3.4 Table: `bookings` `[MVP / Beta]`
Records completed reservations.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique booking ID |
| `user_id` | Integer | Foreign Key (`users.id`), Nullable in MVP | User ID who booked `[Beta]` |
| `user_name` | String | Not Null | Attendee name |
| `user_email` | String | Not Null | Attendee email |
| `ticket_id` | Integer | Foreign Key (`tickets.id`), Not Null | Reference to the booked ticket tier |
| `quantity` | Integer | Not Null, Default: 1 | Number of tickets booked |
| `booking_date` | DateTime | Default: UTC now | Time booking was placed |

---

## 4. REST API Specification

### 4.1 Authentication Endpoints `[Beta]`
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/auth/register` | Public | Register a new account with email and password |
| `POST` | `/api/auth/login` | Public | Check credentials and return JWT bearer token |
| `GET` | `/api/auth/me` | Authenticated | Get current logged-in user profile |

### 4.2 Event Endpoints
| Method | Endpoint | Release | Access | Description |
|---|---|---|---|---|
| `GET` | `/api/events` | MVP | Public | Get list of all upcoming events |
| `GET` | `/api/events/{id}` | MVP | Public | Get single event details and its ticket tiers |
| `POST` | `/api/events` | MVP (open) / Beta | Admin | Create a new event |
| `PUT` | `/api/events/{id}` | MVP (open) / Beta | Admin | Update event details |
| `DELETE` | `/api/events/{id}` | MVP (open) / Beta | Admin | Delete an event and its tickets |
| `PUT` | `/api/events/{id}/assign-manager` | Beta | Admin | Set `manager_id` for an event |

### 4.3 Ticket Endpoints
| Method | Endpoint | Release | Access | Description |
|---|---|---|---|---|
| `GET` | `/api/events/{id}/tickets` | MVP | Public | List tickets available for an event |
| `POST` | `/api/events/{id}/tickets` | MVP (open) / Beta | Manager / Admin | Add a ticket tier with total seats |
| `DELETE` | `/api/tickets/{ticket_id}` | MVP (open) / Beta | Manager / Admin | Remove a ticket tier |

### 4.4 Booking Endpoints
| Method | Endpoint | Release | Access | Description |
|---|---|---|---|---|
| `POST` | `/api/bookings` | MVP | Public (MVP) / User (Beta) | Book tickets and decrement remaining seats |
| `GET` | `/api/bookings` | MVP (all) / Beta | Admin & Manager | View booking list (filtered by role in Beta) |
| `GET` | `/api/bookings/my-bookings` | Beta | User | View personal booking history |

---

## 5. Business Logic & Security Workflow

### 5.1 Booking Logic and Stock Control
To prevent overselling tickets, the booking endpoint uses a database transaction:
1. Client sends `POST /api/bookings` with `{ ticket_id, quantity, user_name, user_email }`.
2. Backend queries the ticket record from SQLite inside a transaction.
3. If `ticket.available_quantity < quantity`, return HTTP 400 (`"Not enough tickets available"`).
4. Otherwise, subtract: `ticket.available_quantity -= quantity`.
5. Insert a new row into the `bookings` table.
6. Commit the transaction and return the booking confirmation.

### 5.2 Role-Based Access Control (RBAC) `[Beta]`
We use FastAPI's dependency injection (`Depends`) to protect routes:
- `get_current_user`: Reads the `Authorization: Bearer <token>` header, decodes the JWT, and looks up the user in the database.
- `require_role(["admin"])`: Ensures `current_user.role == 'admin'`, returning 403 Forbidden otherwise.
- For manager routes, the endpoint checks if `current_user.id == event.manager_id` or `current_user.role == 'admin'`.

---

## 6. Frontend Architecture

The frontend is a single-page React application using client-side views:
- **Event Catalog (`/`):** Homepage showing cards for all published events with date, venue, and a "View Event" button. `[MVP]`
- **Event Detail Page (`/events/:id`):** Shows full description, available ticket tiers, remaining seats, and a booking form. `[MVP]`
- **Admin Panel (`/admin`):** Forms to create/edit/delete events and assign managers to events. `[Beta]`
- **Manager Dashboard (`/manager`):** Allows an event manager to add/delete tickets for their event and see attendee lists. `[Beta]`
- **Login / Register Page (`/login`, `/register`):** User signup and login forms; stores JWT token in `localStorage`. `[Beta]`
- **My Bookings (`/profile`):** Shows the logged-in user's account details and their booked tickets. `[Beta]`

---

## 7. Project Structure

The repository is organized as a monorepo containing both backend and frontend:

```
IUB/
├── vercel.json                 # Vercel deployment routing config
├── README.md                   # Setup guide and instructions
├── docs/                       # Project documentation
│   ├── PRD.md
│   ├── SRS.md
│   └── TDD.md
├── backend/                    # FastAPI backend
│   ├── main.py                 # FastAPI app entry point & route definitions
│   ├── requirements.txt        # Python packages (fastapi, uvicorn, sqlalchemy, etc.)
│   ├── database.py             # SQLite engine and session maker
│   ├── models.py               # SQLAlchemy models (User, Event, Ticket, Booking)
│   ├── schemas.py              # Pydantic schemas for request/response validation
│   ├── auth.py                 # JWT token generation and bcrypt password hashing
│   └── dependencies.py         # Auth dependencies (get_current_user, role checks)
└── frontend/                   # React + TypeScript frontend
    ├── index.html              # HTML shell
    ├── package.json            # Node dependencies and scripts
    ├── vite.config.ts          # Vite build config with /api proxy to backend
    ├── tsconfig.json           # TypeScript configuration
    └── src/
        ├── main.tsx            # React root mount
        ├── App.tsx             # Main component and view switching
        ├── index.css           # Styling
        ├── components/         # Reusable UI parts (Navbar, EventCard, BookingModal)
        └── types/              # TypeScript types for events, tickets, bookings
```

---

## 8. Deployment / Configuration

### 8.1 Running Locally

**Backend Setup:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1      # On Windows (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
fastapi dev main.py
```
- API runs at `http://localhost:8000`
- Interactive Swagger docs at `http://localhost:8000/docs`

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```
- React app runs at `http://localhost:5173`
- In development, Vite proxies requests from `/api/*` to `http://localhost:8000`.

### 8.2 Vercel Deployment (Beta)

The project uses `vercel.json` at the root of the repository so both the React build and FastAPI serverless functions deploy together:

```json
{
  "builds": [
    { "src": "backend/main.py", "use": "@vercel/python" },
    { "src": "frontend/package.json", "use": "@vercel/static-build", "config": { "distDir": "dist" } }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "backend/main.py" },
    { "src": "/(.*)", "dest": "frontend/dist/$1" }
  ]
}
```

### 8.3 Environment Variables

| Variable | Where Used | Description | Required For |
|---|---|---|---|
| `SECRET_KEY` | Backend | Secret string used for signing JWT tokens | Beta |
| `ALGORITHM` | Backend | JWT hashing algorithm (`HS256`) | Beta |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Backend | Token validity period (e.g. 60) | Beta |
| `DATABASE_URL` | Backend | Path to SQLite database file (default: `sqlite:///./events.db`) | MVP + Beta |

For local testing, environment variables can be set in a `.env` file in `backend/`. On Vercel, they are entered under Project Settings -> Environment Variables.

---

## 9. Implementation Milestones

### Milestone 1: MVP (Mid-Term Demo)
1. **Database Setup:** SQLite connection and SQLAlchemy models for `Event`, `Ticket`, and `Booking`.
2. **Core Endpoints:** Endpoints for event CRUD, adding/deleting tickets, and submitting bookings with seat checks.
3. **Swagger UI Testing:** Test all endpoints directly at `/docs`.
4. **Basic UI:** React pages to display events, open an event, and book tickets through a simple form.

### Milestone 2: Beta (Final Demo)
1. **User Authentication:** Add `User` model, bcrypt password hashing, and JWT login endpoints.
2. **Role Protection:** Protect admin routes and manager routes with role checks.
3. **Manager Assignment:** Allow admin to link a user to an event as its manager.
4. **User Dashboard:** "My Bookings" page showing reservations for the logged-in user.
5. **Vercel Deployment:** Deploy the repository to Vercel and test the live URL.

---

## 10. Testing Strategy

### 10.1 Automated Tests (pytest)
- **Overbooking Check:** Try to book more tickets than `available_quantity` and assert that the API returns HTTP 400.
- **Stock Decrement:** Book 1 ticket and verify that `available_quantity` drops by 1 in the database.
- **Cascade Deletion:** Delete an event and ensure its tickets are also deleted.
- **Auth Guard Test `[Beta]`:** Confirm that non-admin users get HTTP 403 when trying to delete events.

### 10.2 Manual Test Checklist
1. Open the homepage -> Verify published events appear.
2. Click an event -> Check that date, venue, and tickets are displayed.
3. Book 2 tickets when 5 are available -> Confirm remaining count updates to 3.
4. Try booking 10 tickets when only 3 are left -> Confirm the app shows an error.
5. In Beta: Register a new account -> Log in -> Verify token is returned -> Book tickets -> Check "My Bookings" page.
