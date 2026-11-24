# Event Booking Platform

A web application for discovering campus events, booking attendance, and managing event organizers and users. The frontend is built with React and TypeScript; the API uses FastAPI and PostgreSQL. The project is configured for deployment to Vercel.

## Live application

- **Frontend:** [cse-309-booking-platform.vercel.app](https://cse-309-booking-platform.vercel.app/)
- **API:** [cse-309-booking-platform.vercel.app/api](https://cse-309-booking-platform.vercel.app/api)
- **API documentation:** [Swagger UI](https://cse-309-booking-platform.vercel.app/api/docs)
- **GitHub:** [SharukH-9s/CSE-309-Booking-Platform](https://github.com/SharukH-9s/CSE-309-Booking-Platform)
- **Final project report:** [FINAL_REPORT.md](./FINAL_REPORT.md)

## Features

- Public event browsing and event details.
- Account registration, login, logout, profile editing, and password changes.
- Booking and cancellation for signed-in users.
- Three roles: `user`, `manager`, and `admin`. Managers can manage assigned events and their attendee bookings; admins can manage all events and bookings.
- Admin dashboard with platform counts, event and account lists, active/banned account filters, ban/unban controls, eligible account deletion, and platform-wide booking cancellation.
- Banned users see an account notice and cannot book events.

Groups and group permissions are not implemented. Access and refresh tokens are returned in JSON and stored in browser `localStorage`; the application does not use `httpOnly` cookies.

## Technology

- **Frontend:** React, TypeScript, Vite
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** PostgreSQL with Psycopg
- **Authentication:** JWT access tokens, rotating refresh tokens, bcrypt password hashes
- **Deployment:** Vercel

## Requirements

- Python 3.10 or newer
- Node.js 22 or newer with npm
- PostgreSQL database

## Run locally

### 1. Configure the backend

From the repository root, copy the example environment file:

```powershell
Copy-Item backend/.env.example backend/.env
```

Edit `backend/.env` and set the PostgreSQL URL, a strong development JWT secret, and the initial admin account values. The example values are placeholders and should be replaced.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL, for example `postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE` |
| `SECRET_KEY` | Secret used to sign JWTs |
| `ALGORITHM` | JWT algorithm; defaults to `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime; defaults to 60 minutes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime; defaults to 7 days |
| `ADMIN_NAME` | Name for the initial admin account |
| `ADMIN_EMAIL` | Email for the initial admin account |
| `ADMIN_PHONE` | Phone for the initial admin account |
| `ADMIN_PASSWORD` | Password for the initial admin account |

Start the API in the first terminal:

```powershell
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
fastapi dev main.py
```

On startup, the API creates missing tables and seeds the configured admin if that email is not already registered.

### 2. Start the frontend

In a second terminal, from the repository root:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Vite forwards `/api` requests to the backend at `http://localhost:8000`.

- API documentation: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- Health check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

## Build check

Run the frontend TypeScript and production build check from `frontend/`:

```powershell
npm run build
```

The repository does not currently include an automated backend test suite or a separate frontend test runner.

## Deployment

The Vercel configuration at the repository root routes `/api/*` to the FastAPI service and other paths to the Vite frontend. Import the repository into Vercel with the project root set to `./`, then configure the environment variables listed above. Use a managed PostgreSQL database and store its URL and secrets in Vercel's environment settings. Do not commit real credentials or `.env` files.
