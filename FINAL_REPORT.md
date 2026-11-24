
<div align="center">

# Independent University, Bangladesh

## CSE309 Web Application & Internet

### Final Project Submission Report

**Submitted by**<br>
Name: Md. Mohaiminul Hassan Sharukh<br>
Student ID: 2030293<br>
Section: 05<br>
Team Number:<br>

**Project Title:**<br>
Event Booking Platform

**Vercel URL:** [https://cse-309-booking-platform.vercel.app/](https://cse-309-booking-platform.vercel.app/)<br>
**GitHub Repository:** [SharukH-9s/CSE-309-Booking-Platform](https://github.com/SharukH-9s/CSE-309-Booking-Platform)

**Submitted To**<br>
Sayef Reyadh<br>
Adjunct Lecturer<br>
Department of Computer Science & Engineering<br>
Independent University, Bangladesh

**Semester:** Autumn 2026<br>
**Date of Submission:** 25-11-26

</div>

<div style="page-break-after: always;"></div>

# Executive Summary

## 1.1 Project overview

**Project name:** Event Booking Platform

The Event Booking Platform helps students and campus visitors discover events, while organizers manage event information and administrators oversee users and platform activity. It provides account authentication, role-based access, event browsing and management, and administration tools for the people responsible for the platform.

**Stack:** React with TypeScript, FastAPI, PostgreSQL, and Vercel.

## 1.2 What was built since the mid assessment

- **JWT authentication with refresh and logout:** Users can sign in with JWT-based access, refresh their session, and log out.
- **Role based access control:** The backend checks user roles and manager ownership of events; group permissions are not implemented.
- **Event booking and cancellation:** Users can book events and cancel their own bookings; event managers and admins can view attendees and cancel bookings.
- **User ban system and booking restriction:** Admins can ban and unban regular user accounts; banned users see a persistent banned banner after signing in and are blocked (`403 Forbidden`) from booking events.
- **Admin dashboard:** Admins can view platform summary metrics (`Total Bookings`, `Total Events`, `Total Users`, `Banned Users`), review event and account lists with `All / Active / Banned` ban-status filtering, see manager assignments and account ban status (`Active` / `Banned`), ban or unban regular users, delete eligible accounts, and review or cancel any platform booking.
- **Deployment and remaining security work:** The platform is deployed on Vercel. Audit logging, brute-force protection, a security view, and exports are not implemented.

## 1.3 Live links

| Resource | Link |
|---|---|
| GitHub repository | [SharukH-9s/CSE-309-Booking-Platform](https://github.com/SharukH-9s/CSE-309-Booking-Platform) |
| Vercel frontend | [Event Booking Platform](https://cse-309-booking-platform.vercel.app/) |
| API | [Event Booking Platform API](https://cse-309-booking-platform.vercel.app/api) |
| API docs | [Swagger UI](https://cse-309-booking-platform.vercel.app/api/docs#/) |
| Video demo | [https://drive.google.com/file/d/1nD4DwmDDG9_D6RwWKST1bavX9i4HxisO/view?usp=sharing] |

# Part A. Product Requirements (PRD)

## A1. Problem statement

Students and other campus visitors need a simple way to find event information, including when and where an event takes place. Today, details may be shared across separate posts or messages, making it difficult to find the latest information. Organizers also need a clear way to keep event details current.

The project team currently manages event information and organizer assignments through the application and its admin account. Without clear role limits, a manager could change an event they do not own, or an attendee could be given access to administrative actions. These problems can cause confusion and put event information at risk.

## A2. Users and roles

| Role | Who they are | Main tasks | What they must never be able to do |
|---|---|---|---|
| Visitor | Someone using the site without signing in | Browse and view events; register an account | Create or change events, view the user list, or use a protected account function |
| User | A registered attendee | Sign in; view events; book events (unless banned); view and cancel own bookings; update their own profile and password | Change another user's profile, book events while banned, or use manager/admin functions |
| Group member | Not used in this project; the app has no groups | None | Access group functions or another user's data |
| Group owner | Not used in this project; event managers are assigned to individual events instead | None | Access group functions or claim ownership of an unassigned event |
| Admin | A system administrator | Create events; assign a manager when creating a manager account; list, ban/unban regular users, and delete eligible accounts; view and cancel any booking | Delete their own account, delete the last remaining admin account, or ban themselves, managers, or admins |
| Event manager | A registered organizer assigned to an event | View and edit assigned events; view attendee bookings and cancel bookings for assigned events | Edit or delete another manager's event, or create events |

## A3. Goals and success measures

| ID | Goal | Measure |
|---|---|---|
| G-01 | Let visitors find event details | Event list and detail requests return event data without signing in |
| G-02 | Protect accounts with password hashing | Every registered password is stored as a bcrypt hash; plaintext is not stored |
| G-03 | Limit event changes by role and ownership | A manager can update or delete an assigned event; a different manager receives HTTP 403 |
| G-04 | Support short-lived access and renewable sessions | Access token lifetime is 60 minutes by default; refresh token lifetime is 7 days by default and rotation invalidates the previous token |
| G-05 | Protect admin accounts | An admin cannot delete their own account or the last admin account |
| G-06 | Keep account and event data after service restart | User, refresh-token and event records remain in PostgreSQL after the API restarts |

## A4. Scope and non-goals

**In scope**

- Account registration, login, logout, access and refresh tokens, profile update, and password change.
- Three implemented roles: `user`, `manager`, and `admin`.
- Public event listing and event detail views.
- Event booking by registered users, attendee booking lists for managers and admins, and booking cancellation.
- Admin event creation and manager account creation with assignment to one event.
- Manager access to their assigned event, with ownership checks on event detail, update, and delete.
- Admin user listing (with optional `?banned=true|false` API filtering and `All / Active / Banned` UI controls), ban/unban of regular user accounts, and account deletion with safeguards.
- Admin dashboard summary metrics (`total_bookings`, `total_events`, `total_users`, `banned_users`) and platform-wide bookings overview with cancellation.
- Per-request ban verification, a banned banner for banned users in the UI, and booking restriction (`403 Forbidden`) for banned accounts.
- PostgreSQL storage and deployment configuration for Vercel.

**Out of scope**

- Ticket tiers, ticket purchases, seat inventory quotas, and paid transactions. These are not part of the current implementation.
- Groups and group permissions. Event assignment is the only ownership feature.
- Role changes, bulk admin actions, content moderation, activity or audit logs, security dashboard, CSV export, and session-list/revoke screens. These endpoints and screens are not implemented.
- Email or SMS, payments, ticket refunds, and downloadable tickets. These are beyond the course project's current scope.

**Assumptions and constraints**

- The app is used in a current desktop or mobile browser with JavaScript enabled.
- The API uses a PostgreSQL database configured through environment variables; production hosting follows the repository's Vercel setup.
- The course project has limited development time and uses a small role set and event-focused domain.
- Access-token lifetime defaults to 60 minutes and refresh-token lifetime defaults to 7 days; deployment can configure these values.

## A5. User stories

| ID | Story |
|---|---|
| US-01 | Visitors can browse the event list to find events. |
| US-02 | Visitors can open an event's details to check its date and location. |
| US-03 | Visitors can register with a name, email, and password to create an account. |
| US-04 | Users can sign in and refresh a session to continue using protected features. |
| US-05 | Users can update their profile and password to keep account details current. |
| US-06 | Users can log out to revoke the refresh token. |
| US-07 | Managers can see only assigned events in the event list. |
| US-08 | Managers can edit assigned events to correct event details. |
| US-09 | Managers cannot edit another manager's event, preserving event ownership. |
| US-10 | Admins can create events for publication. |
| US-11 | Admins can create a manager account for an event so an organizer can maintain it. |
| US-12 | Admins can list registered accounts to review account records. |
| US-13 | Admins can delete eligible accounts to remove obsolete records safely. |
| US-14 | Users can book an event to reserve attendance. |
| US-15 | Users can view and cancel their own bookings. |
| US-16 | Managers can view attendee bookings for their assigned events. |
| US-17 | Managers and admins can cancel bookings to maintain attendee lists. |
| US-18 | Admins can ban and unban regular user accounts (with safeguards against banning themselves, managers, or admins) to restrict event bookings. |
| US-19 | Banned users see a banned banner after signing in and are prevented from booking events. |
| US-20 | Admins can view platform summary metrics (`total_bookings`, `total_events`, `total_users`, `banned_users`) in the admin dashboard. |
| US-21 | Admins can filter accounts by ban status (`All`, `Active`, `Banned`) and view or cancel any booking in the platform bookings overview. |

# Part B. Software Requirements (SRS)

## B1. Introduction

This document states the testable requirements for the Event Booking Platform. It is for the project team, course instructor, testers, and reviewers. It describes the current React and TypeScript frontend, FastAPI backend, and PostgreSQL data store.

| Term | Meaning |
|---|---|
| JWT | A signed token format used to carry identity information; this project uses JWT for access tokens. |
| Access token | A short-lived signed token sent with requests to identify a signed-in account. |
| Refresh token | A longer-lived random token used to request a new access token; it is stored on the server as a hash and rotated when used. |
| RBAC | Role-based access control: deciding which actions are allowed based on a user's role. |
| Role | An account category in the app: `user`, `manager`, or `admin`. |
| Permission | Authorization to perform a particular action, based on role and, for managers, event assignment. |
| Audit log | A record of who performed an action and when; the current app does not provide one. |

**References:** RFC 7519, *JSON Web Token (JWT)*; OWASP, *Application Security Verification Standard (ASVS)*; FastAPI documentation, *Security* and *Middleware*; project source and README.

## B2. Functional requirements

Requirements below describe implemented behavior. The API returns HTTP 422 for invalid request fields unless another response is specified.

### Table 5. Authentication requirements (FR-AUTH)

| ID | Requirement |
|---|---|
| FR-AUTH-01 | The system shall allow a visitor to register with a name, unique email, password of 8–128 characters, and optional phone number, and shall assign the `user` role. |
| FR-AUTH-02 | The system shall hash passwords with bcrypt before storing them and shall never store a plaintext password. |
| FR-AUTH-03 | The system shall accept a valid email and password at login and return a signed access token, a refresh token, token type, expiry duration, and user profile. |
| FR-AUTH-04 | The system shall include the account ID as the access token subject and an expiry claim; the default access-token lifetime shall be 60 minutes. |
| FR-AUTH-05 | The system shall issue refresh tokens with a default lifetime of 7 days and store only their SHA-256 hashes. |
| FR-AUTH-06 | The system shall rotate a valid refresh token when used and reject a revoked, expired, or unknown refresh token with HTTP 401. |
| FR-AUTH-07 | The system shall revoke the submitted refresh token on logout and return HTTP 204. |
| FR-AUTH-08 | The system shall return the signed-in user's profile from `GET /api/auth/me` and allow that user to update their own name, email, and phone. |
| FR-AUTH-09 | The system shall change a password only when the current password is correct and the new password differs from it, then revoke that user's refresh tokens. |
| FR-AUTH-10 | The system shall reject a missing or invalid bearer token on protected endpoints with HTTP 401. |
| FR-AUTH-11 | The system shall return HTTP 401 with the message `Invalid email or password` for an unknown email or incorrect password. |
| FR-AUTH-12 | The system shall not provide a session list or a per-session revoke endpoint in the current release. |

### Table 6. Role and event requirements (FR-RBAC / FR-DOMAIN)

| ID | Requirement |
|---|---|
| FR-RBAC-01 | The system shall recognize the roles `user`, `manager`, and `admin`; public registration shall not allow the registrant to select a role. |
| FR-RBAC-02 | The system shall enforce protected route role checks in backend middleware, regardless of frontend visibility. |
| FR-RBAC-03 | The system shall allow only admins to create events and create manager accounts. |
| FR-RBAC-04 | The system shall allow an admin to create a manager account and assign that account to one existing event that has no manager. |
| FR-RBAC-05 | The system shall allow a manager to view, update, and delete only events assigned to that manager; requests to another manager's event shall return HTTP 403. |
| FR-RBAC-06 | The system shall allow an admin to view, update, and delete any event. |
| FR-RBAC-07 | The system shall reject deletion of the current admin account and deletion of the last admin account with HTTP 400. |
| FR-RBAC-08 | The system shall not provide groups, group permissions, role-change actions, or an audit log in the current release. |
| FR-DOMAIN-01 | The system shall allow a visitor to list events and retrieve an event by ID without signing in. |
| FR-DOMAIN-02 | The system shall return only events assigned to that manager when a manager lists events. |
| FR-DOMAIN-03 | The system shall allow an admin to create an event with a title, location, date, and optional description. |
| FR-DOMAIN-04 | The system shall allow an admin or assigned manager to update event title, location, date, or description. |
| FR-DOMAIN-05 | The system shall allow an admin or assigned manager to delete an event; a successful deletion shall return HTTP 204. |
| FR-DOMAIN-06 | The system shall return HTTP 404 when a requested event or account does not exist. |

### Table 6.1. Booking requirements (FR-BOOK)

| ID | Requirement |
|---|---|
| FR-BOOK-01 | The system shall allow a signed-in user to book an event at `POST /api/bookings`; duplicate bookings by the same user for the same event shall return HTTP 409. |
| FR-BOOK-02 | The system shall allow a signed-in user to list their bookings at `GET /api/bookings/my` and cancel their own booking at `DELETE /api/bookings/{booking_id}`. |
| FR-BOOK-03 | The system shall allow an event manager to view attendee bookings for their assigned event at `GET /api/events/{event_id}/bookings`; requests for an unassigned event shall return HTTP 403. |
| FR-BOOK-04 | The system shall allow an event manager to cancel a booking for their assigned event; cancellation of a booking on an unassigned event shall return HTTP 403. |
| FR-BOOK-05 | The system shall allow an admin to view bookings for any event and cancel any booking. |

### Table 7. Admin requirements (FR-ADM)

| ID | Requirement |
|---|---|
| FR-ADM-01 | The system shall allow an admin to list registered users at `GET /api/admin/users`, with optional `?banned=true` or `?banned=false` query filtering. |
| FR-ADM-02 | The system shall allow an admin to delete another account, remove its manager assignment from any event, and return HTTP 204. |
| FR-ADM-03 | The system shall prevent an admin from deleting their own account or the last remaining admin account. |
| FR-ADM-04 | The system shall allow an admin to ban and unban regular (`user`) accounts at `POST /api/admin/users/{user_id}/ban` and `DELETE /api/admin/users/{user_id}/ban`, rejecting self-bans and manager/admin bans with HTTP 400 and duplicate bans with HTTP 409. |
| FR-ADM-05 | The system shall verify ban status on authenticated requests, expose `is_banned` on user responses, display a banned banner in the UI for banned users, and reject `POST /api/bookings` from banned users with HTTP 403. |
| FR-ADM-06 | The system shall provide admin summary metrics (`total_bookings`, `total_events`, `total_users`, `banned_users`) at `GET /api/admin/stats` and a platform-wide bookings list at `GET /api/admin/bookings`. |
| FR-ADM-07 | The system shall not provide text search, pagination, user detail views, role changes, session revocation, bulk actions, content moderation, activity logs, security view, or CSV export in the current release. |

## B3. Non-functional requirements

### Table 9. Non-functional requirements

| ID | Area | Requirement |
|---|---|---|
| NFR-SEC-01 | Security | The system shall read the database URL, JWT secret, and initial admin credentials from environment variables in deployment. |
| NFR-SEC-02 | Security | The system shall use bcrypt password hashes and shall not store plaintext passwords or raw refresh tokens in the database. |
| NFR-SEC-03 | Security | The system shall use the same generic HTTP 401 login message for an unknown email and an incorrect password. |
| NFR-SEC-04 | Security | The system shall return HTTP 401 for invalid or expired access tokens and HTTP 403 for authenticated users without the required role or ownership. |
| NFR-PERF-01 | Performance | For a course-demo database with up to 100 users and 1,000 events, event and user list requests should complete within 1 second on the local project setup. |
| NFR-PERF-02 | Performance | Event and user list endpoints shall return all matching records; pagination is not implemented in the current release. |
| NFR-USE-01 | Usability | The frontend shall support viewport widths from 360 px to 1440 px without horizontal page scrolling on its main screens. |
| NFR-USE-02 | Usability | The frontend shall display a loading or error message when an API request is pending or fails. |
| NFR-REL-01 | Reliability | The system shall persist accounts, events, and refresh-token records in PostgreSQL across an API restart. |
| NFR-MNT-01 | Maintainability | The system shall keep route role policies in the backend RBAC middleware. |
| NFR-MNT-02 | Maintainability | The project shall provide automated tests for authentication, role checks, and event ownership before a release is considered complete. |

## B4. Roles and permission matrix

`Yes` means allowed, `No` means not allowed, and `Own` means allowed only for the signed-in user's profile or assigned event. These rules describe backend behavior. Admin is allowed to retrieve any event, but event listing does not have a separate admin-only endpoint.

### Table 10. Endpoint groups by role

| Endpoint group | Visitor | User | Group member | Group owner | Event manager | Admin |
|---|---:|---:|---:|---:|---:|---:|
| List events | Yes | Yes | No | No | Own events | Yes |
| Read event detail | Yes | Yes | No | No | Own event | Yes |
| Create event | No | No | No | No | No | Yes |
| Update or delete event | No | No | No | No | Own event | Yes |
| Register account | Yes | Yes | No | No | No | Yes |
| Login, refresh, logout | Yes | Yes | No | No | Yes | Yes |
| Read or update own profile; change own password | No | Own | No | No | Own | Own |
| List users | No | No | No | No | No | Yes (optional `banned` filter) |
| View admin summary metrics and all platform bookings | No | No | No | No | No | Yes |
| Delete another account | No | No | No | No | No | Yes, with safeguards |
| Ban or unban regular user account | No | No | No | No | No | Yes, with safeguards |
| Create manager and assign to an event | No | No | No | No | No | Yes |
| Book event | No | Yes (unless banned) | No | No | Yes | Yes |
| View own bookings | No | Yes | No | No | Yes | Yes |
| View event attendee bookings | No | No | No | No | Own event | Yes |
| Cancel booking | No | Own booking | No | No | Assigned event | Yes |
| Group endpoints | No | No | No | No | No | No |

### Table 11. Group permissions

| Permission | Meaning in this project |
|---|---|
| Create | Not applicable; groups are not implemented. |
| Update | Not applicable; groups are not implemented. |
| Assign | Not applicable; groups are not implemented. An admin can assign a manager to an event. |
| Owner-only actions | Not applicable to groups. An event manager may update or delete only their assigned event. |

### Table 12. Admin rules

| Rule | Current behavior |
|---|---|
| Admin deleting their own account | Denied with HTTP 400. |
| Admin deleting the last admin | Denied with HTTP 400. |
| Admin deleting another admin | Allowed unless that account is the last admin. |
| Admin changing their own role | No role-change endpoint is implemented. |
| Admin banning another admin | Denied with HTTP 400; only regular (`user`) accounts can be banned, and admins cannot ban themselves or managers. |
| System admin rights inside a group | None; the app has no groups. |
| Admin event ownership | Admin can access any event; managers remain limited to their assignments. |

## B5. Use cases

### Table 13. Use case descriptions

#### UC-01: Log in and refresh a session

- **Actor:** Registered user, manager, or admin.
- **Preconditions:** The account exists and is not deleted.
- **Main flow:**
  1. The actor submits email and password to `POST /api/auth/login`.
  2. The system verifies the password and returns an access token and refresh token.
  3. When the access token expires, the actor submits the refresh token to `POST /api/auth/refresh`.
  4. The system revokes the old refresh token and returns a new token pair.
- **Alternative/error flows:** Unknown email or wrong password returns 401; malformed input returns 422; invalid, expired, or reused refresh token returns 401.
- **Postconditions:** On refresh, the old token is revoked and the new token pair can be used.

#### UC-02: Create an event

- **Actor:** Admin.
- **Preconditions:** The actor is signed in as an admin.
- **Main flow:**
  1. The admin submits event title, location, date, and optional description to `POST /api/events`.
  2. The system validates the fields and stores the event.
  3. The system returns the created event with HTTP 201.
- **Alternative/error flows:** Missing authentication returns 401; a non-admin receives 403; invalid fields return 422.
- **Postconditions:** The event is available through the public event list and detail endpoints.

#### UC-03: Change a member's permissions (event assignment)

- **Actor:** Admin.
- **Preconditions:** The actor is signed in as an admin; the target event exists and has no manager.
- **Main flow:**
  1. The admin submits a manager's name, email, password, optional phone, and event ID to `POST /api/managers`.
  2. The system creates an account with the `manager` role and assigns it to the event.
  3. The system returns the manager profile with HTTP 201.
- **Alternative/error flows:** A missing event returns 404; an already assigned event or duplicate email returns 409; a non-admin receives 403; invalid fields return 422.
- **Postconditions:** The manager can manage that event only. The system has no separate permissions editor or groups.

#### UC-04: Denied event change

- **Actor:** Manager.
- **Preconditions:** The manager is signed in and attempts to change an event assigned to a different manager.
- **Main flow:**
  1. The manager submits an update or delete request for the event.
  2. The system loads the event and checks its manager assignment.
  3. The system rejects the request with HTTP 403.
- **Alternative/error flows:** An invalid or expired token returns 401; an unknown event returns 404; invalid update fields return 422.
- **Postconditions:** The event is unchanged.

#### UC-05: Delete a user account

- **Actor:** Admin.
- **Preconditions:** The admin is signed in and the target account exists.
- **Main flow:**
  1. The admin sends `DELETE /api/admin/users/{id}` for another account.
  2. The system checks self-deletion and last-admin safeguards.
  3. The system removes the account and clears its event manager assignments.
  4. The system returns HTTP 204.
- **Alternative/error flows:** Missing authentication returns 401; a non-admin receives 403; an unknown account returns 404; self-deletion or deleting the last admin returns 400.
- **Postconditions:** The deleted account cannot sign in and no event remains assigned to it.

#### UC-06: Read the audit log

- **Actor:** Admin.
- **Preconditions:** None; the audit-log feature is not implemented.
- **Main flow:**
  1. The admin looks for the activity log in the admin area.
  2. The system has no audit-log endpoint or screen to return.
- **Alternative/error flows:** No log data is available; audit-log filters and export are also not available.
- **Postconditions:** No audit-log record is created or returned by this feature in the current release.

### Figure 1. Use case diagram

```mermaid
flowchart LR
  Visitor[Visitor]
  User[Signed-in user]
  Manager[Event manager]
  Admin[Admin]
  Browse((Browse events))
  Register((Register))
  Auth((Log in and refresh))
  Profile((Update own profile))
  CreateEvent((Create event))
  Assign((Assign event manager))
  OwnEvent((Manage assigned event))
  DeleteUser((Delete eligible account))
  Denied((Attempt another manager's event))
  Audit((Read audit log - unavailable))
  Visitor --> Browse
  Visitor --> Register
  User --> Browse
  User --> Auth
  User --> Profile
  Manager --> Auth
  Manager --> OwnEvent
  Manager --> Denied
  Admin --> Auth
  Admin --> CreateEvent
  Admin --> Assign
  Admin --> DeleteUser
  Admin --> Browse
  Admin --> Audit
```

## B6. Acceptance criteria

### Table 14. Acceptance criteria

| ID | Given | When | Then |
|---|---|---|---|
| AC-01 | A protected endpoint requires a valid access token | The client sends an expired access token | The system returns HTTP 401. |
| AC-02 | A client sends a JWT that has been changed after signing | The client calls a protected endpoint | The system rejects the token and returns HTTP 401. |
| AC-03 | A manager is assigned to Event A, not Event B | The manager requests to update or delete Event B | The system returns HTTP 403 and Event B remains unchanged. |
| AC-04 | A visitor is not signed in | The visitor sends a request to create an event | The system returns HTTP 401. |
| AC-05 | An authenticated regular user calls an admin-only endpoint | The user requests the admin user list | The system returns HTTP 403. |
| AC-06 | A visitor submits valid registration details | The registration request succeeds | The new account has role `user`, and its stored password is a bcrypt hash. |
| AC-07 | A user has a valid refresh token | The user refreshes once, then submits the same token again | The first request returns a new token pair; the reused token is rejected with HTTP 401. |
| AC-08 | An admin is signed in | The admin requests deletion of their own account | The system returns HTTP 400 and keeps the account. |
| AC-09 | Only one admin account remains | That admin requests deletion of another account with admin role | The system returns HTTP 400 and keeps the last admin. |
| AC-10 | A visitor requests the event list | The request completes | The system returns the current event records without requiring authentication. |
| AC-11 | A user submits an incorrect password for an existing account or an unknown email | The user attempts to log in | In either case, the system returns HTTP 401 with `Invalid email or password`. |
| AC-12 | An account has been deleted by an admin | The former account attempts to sign in | The system rejects the login with HTTP 401. |
| AC-13 | A regular user account is banned by an admin | The user signs in and attempts to book an event | Login returns `is_banned: true`, the UI displays a banned banner, and `POST /api/bookings` returns HTTP 403. |
| AC-14 | An admin is signed in | The admin attempts to ban their own account, a manager, or another admin | The system rejects the request with HTTP 400. |
| AC-15 | A regular user account is currently banned | An admin unbans the account via `DELETE /api/admin/users/{user_id}/ban` | The system returns HTTP 204, `is_banned` becomes `false`, and the user can book events again. |
| AC-16 | An admin opens the admin dashboard or calls `GET /api/admin/stats` and `GET /api/admin/bookings` | The requests complete | The system returns platform counts (`total_bookings`, `total_events`, `total_users`, `banned_users`) and all bookings; non-admins receive HTTP 403. |
| AC-17 | Accounts include both active and banned users | An admin calls `GET /api/admin/users?banned=true` (or `?banned=false`) or selects `Active` / `Banned` in the UI | The system returns or displays only accounts matching the selected ban status. |

# Part C. Technical Design (TDD)

This section describes the current implementation. It does not describe planned groups, audit logging, or other features that are not in the repository.

## C1. Technology stack

### Table 16. Technology stack

| Component | Technology and version | Reason |
|---|---|---|
| Frontend | React 19, TypeScript 7, Vite 8 (versions declared in `frontend/package.json`) | Build a single-page browser app with typed UI code and a quick development server. |
| UI library | No additional component library; project CSS | Keep the course project small and easy to explain. |
| Backend | Python 3.10+, FastAPI (declared minimum 0.141.1) | Provide typed HTTP routes and automatic API documentation. |
| Database | PostgreSQL | Persist account, event, and refresh-token records. |
| ORM / database driver | SQLAlchemy 2+ and Psycopg 3.2+ | Define tables as Python models and connect to PostgreSQL. |
| Password hashing | Passlib 1.7.4+ with bcrypt; bcrypt constrained below 4.1 | Store password hashes rather than plaintext passwords. |
| JWT library | python-jose with cryptography, version 3.3+ | Sign and validate access tokens. |
| Testing | No automated test framework or test files are currently included. | Test tooling has not yet been added to this project. |
| Hosting | Vercel configuration in `vercel.json`; PostgreSQL URL supplied by environment | Host the frontend and API using the repository's Vercel setup and an external PostgreSQL service. |

Versions above are the dependency ranges in the repository, not exact locked runtime versions.

## C2. System architecture

The frontend and API are configured as Vercel services. The API connects to PostgreSQL. The current system has no audit-log store or audit-log endpoint, so no audit-log component appears in the architecture.

### Figure 2. System architecture

```mermaid
flowchart LR
  Browser[Browser: React app]
  Frontend[Vercel frontend service: Vite build]
  API[Vercel backend service: FastAPI]
  DB[(PostgreSQL database)]
  Browser -->|HTTPS page and static asset requests| Frontend
  Browser -->|HTTPS /api requests; Authorization: Bearer access token| API
  API -->|SQL via SQLAlchemy and Psycopg| DB
  API -->|JSON responses and token pair in response body| Browser
  Browser -.->|Refresh token sent in JSON body; no cookie used| API
```

**Browser to frontend:** The browser requests the application page and static frontend assets over HTTPS. Vercel routes non-API paths to the frontend service.

**Browser to API:** The frontend sends API calls to `/api/...`; protected calls include `Authorization: Bearer <access_token>`. Login, register, refresh, and logout send their data as JSON.

**API to database:** FastAPI services use SQLAlchemy sessions and Psycopg to read or change PostgreSQL records. Database credentials are read from `DATABASE_URL`.

**API to browser:** The API returns JSON responses; login and refresh include access and refresh tokens in the response body. The frontend stores both tokens in `localStorage`.

**Refresh request:** On a protected request's first HTTP 401, the frontend sends the stored refresh token in a JSON body to `/api/auth/refresh`. The refresh token is not an HTTP-only cookie.

## C3. Backend and frontend structure

### Folder tree of the backend

```text
backend/
├── main.py
├── database.py
├── middleware.py
├── security.py
├── models.py
├── schemas.py
├── routers/
│   ├── auth.py
│   ├── bookings.py
│   ├── events.py
│   ├── managers.py
│   └── admin.py
├── services/
│   ├── auth_service.py
│   ├── booking_service.py
│   ├── event_service.py
│   ├── manager_service.py
│   └── admin_service.py
└── repositories/
    ├── ban_repository.py
    ├── booking_repository.py
    ├── user_repository.py
    ├── refresh_token_repository.py
    └── event_repository.py
```

Routes in `routers/` receive HTTP requests and connect them to services. `services/` contains account, booking, event, manager, and admin operations. `repositories/` contains database queries, including `ban_repository.py` for `banned_users`. `models.py` defines database tables, and `schemas.py` defines request and response data. `security.py` hashes passwords and creates or checks tokens. `middleware.py` authenticates bearer tokens, runs the per-request ban check (`is_user_banned`), and applies role and booking-restriction rules; this is the RBAC module. Admin logic is in `services/admin_service.py` and `routers/admin.py`. `main.py` configures FastAPI and registers routes; `database.py` configures PostgreSQL.

### Folder tree of the frontend

```text
frontend/
├── index.html
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── api.ts
    ├── types.ts
    └── index.css
```

`App.tsx` contains the app views, forms, and conditional access controls. These views include event list/detail, create/edit event, login/register, manager creation, profile, and admin dashboard. `api.ts` contains the API client and token storage/refresh behavior. `types.ts` defines frontend data types, and `index.css` contains project styling. There is no separate authentication context, route-guard module, or component directory; authentication state and view selection are handled in `App.tsx`.

## C4. Data model

### Figure 3. Entity relationship diagram

```mermaid
erDiagram
  USERS ||--o{ REFRESH_TOKENS : owns
  USERS o|--o{ EVENTS : manages
  USERS ||--o| BANNED_USERS : banned_in
  USERS ||--o{ BOOKINGS : books
  EVENTS ||--o{ BOOKINGS : receives
  USERS {
    int id PK
    string name
    string email UK
    string phone
    string hashed_password
    string role
    datetime created_at
  }
  BANNED_USERS {
    int id PK
    int user_id FK
    datetime created_at
  }
  REFRESH_TOKENS {
    int id PK
    int user_id FK
    string token_hash UK
    datetime expires_at
    datetime revoked_at
    datetime created_at
  }
  EVENTS {
    int id PK
    string title
    text description
    string location
    string event_date
    int manager_id FK
    datetime created_at
  }
  BOOKINGS {
    int id PK
    int event_id FK
    int user_id FK
    datetime created_at
  }
```

### Table 17. Users

| Column | Type | Key / constraint / index |
|---|---|---|
| `id` | Integer | Primary key; indexed. |
| `name` | String(120) | Required. |
| `email` | String(255) | Required, unique, indexed. |
| `phone` | String(40) | Optional. |
| `hashed_password` | String(255) | Required; bcrypt hash. |
| `role` | String(20) | Required; application values are `user`, `manager`, `admin`. |
| `created_at` | DateTime with timezone | Required; defaults to current UTC time. |

### Table 18. Refresh tokens

| Column | Type | Key / constraint / index |
|---|---|---|
| `id` | Integer | Primary key; indexed. |
| `user_id` | Integer | Required foreign key to `users.id`; indexed; account deletion cascades. |
| `token_hash` | String(64) | Required SHA-256 hash; unique and indexed. |
| `expires_at` | DateTime with timezone | Required expiration time. |
| `revoked_at` | DateTime with timezone | Optional; set when token is revoked or rotated. |
| `created_at` | DateTime with timezone | Required; defaults to current UTC time. |

### Table 19. Events

| Column | Type | Key / constraint / index |
|---|---|---|
| `id` | Integer | Primary key; indexed. |
| `title` | String(200) | Required. |
| `description` | Text | Optional. |
| `location` | String(255) | Required. |
| `event_date` | String(40) | Required; stored as text. |
| `manager_id` | Integer | Optional foreign key to `users.id`; indexed; set to null if manager is deleted. |
| `created_at` | DateTime with timezone | Required; defaults to current UTC time. |

### Table 19.1. Bookings

| Column | Type | Key / constraint / index |
|---|---|---|
| `id` | Integer | Primary key; indexed. |
| `event_id` | Integer | Foreign key to `events.id` with cascade delete; indexed. |
| `user_id` | Integer | Foreign key to `users.id` with cascade delete; indexed. |
| `created_at` | DateTime with timezone | Required; defaults to current UTC time. |

### Table 19.2. Banned users

| Column | Type | Key / constraint / index |
|---|---|---|
| `id` | Integer | Primary key; indexed. |
| `user_id` | Integer | Required, unique foreign key to `users.id` with cascade delete; indexed. |
| `created_at` | DateTime with timezone | Required; defaults to current UTC time. |

Roles are stored as strings in `users.role` and checked by backend middleware. The event manager relation is stored in `events.manager_id`. Refresh sessions are stored as hashed, expiring, revocable records in `refresh_tokens`. Bookings are stored with foreign keys to events and users in `bookings`. Banned accounts are recorded in `banned_users` with a unique foreign key to `users.id`, allowing ban status to be tracked without altering the `users` table schema. The current schema has no group or group-membership table, permission table, or activity-log table.

## C5. API design

The API prefix is `/api`; there is no separate version segment. JSON errors use FastAPI's `{"detail": "..."}` format. Validation errors use FastAPI's standard 422 response with a `detail` list. Token errors use 401, role or ownership denials use 403, and missing records use 404. CORS is configured in `main.py` to allow all origins, methods, and headers.

### Table 20. Implemented endpoint list

| Method and path | Authentication / role | Request body | Success | Error statuses |
|---|---|---|---|---|
| `GET /api/health` | Public | None | 200 | — |
| `POST /api/auth/register` | Public | `name`, `email`, `password`, optional `phone` | 201 user profile | 409 duplicate email; 422 invalid fields |
| `POST /api/auth/login` | Public | `email`, `password` | 200 token pair and user | 401 invalid credentials; 422 invalid body |
| `POST /api/auth/refresh` | Public; valid refresh token required | `refresh_token` | 200 rotated token pair | 401 invalid, expired, revoked, or reused token; 422 invalid body |
| `POST /api/auth/logout` | Public; refresh token supplied | `refresh_token` | 204 | 422 invalid body |
| `GET /api/auth/me` | Signed-in user, manager, or admin | None | 200 current user's profile | 401 missing or invalid access token |
| `PATCH /api/auth/me` | Signed-in user, manager, or admin | Optional `name`, `email`, `phone` | 200 updated profile | 401; 409 email in use; 404 user not found; 422 invalid fields |
| `POST /api/auth/change-password` | Signed-in user, manager, or admin | `current_password`, `new_password` | 204 | 401; 400 incorrect current password or same password; 422 invalid fields |
| `GET /api/events` | Public; manager receives assigned events only | None | 200 event list | 401 if malformed/invalid Authorization header is supplied |
| `GET /api/events/{event_id}` | Public; manager limited to assigned event | None | 200 event | 401 invalid token; 403 manager ownership denial; 404 event missing |
| `POST /api/events` | Admin | `title`, `location`, `event_date`, optional `description` | 201 event | 401; 403; 422 invalid fields |
| `PUT /api/events/{event_id}` | Admin or assigned manager | Optional event fields | 200 updated event | 401; 403 manager ownership denial; 404 event missing; 422 invalid fields |
| `DELETE /api/events/{event_id}` | Admin or assigned manager | None | 204 | 401; 403 manager ownership denial; 404 event missing |
| `POST /api/managers` | Admin | `name`, `email`, `password`, optional `phone`, `event_id` | 201 manager profile | 401; 403; 404 event missing; 409 duplicate email or assigned event; 422 invalid fields |
| `GET /api/admin/stats` | Admin | None | 200 summary metrics (`total_bookings`, `total_events`, `total_users`, `banned_users`) | 401; 403 |
| `GET /api/admin/bookings` | Admin | None | 200 list of all platform bookings | 401; 403 |
| `GET /api/admin/users` | Admin | Optional `?banned=true\|false` query parameter | 200 user list (with `is_banned`) | 401; 403 |
| `POST /api/admin/users/{user_id}/ban` | Admin | None | 200 user profile (`is_banned: true`) | 401; 403; 400 self-ban or non-`user` role; 404 user missing; 409 already banned |
| `DELETE /api/admin/users/{user_id}/ban` | Admin | None | 204 | 401; 403; 404 user or ban record missing |
| `DELETE /api/admin/users/{user_id}` | Admin | None | 204 | 401; 403; 400 self or last-admin deletion; 404 user missing |
| `POST /api/bookings` | Signed-in user (not banned), manager, or admin | `event_id` | 201 booking record | 401; 403 banned user; 404 event missing; 409 duplicate booking; 422 invalid fields |
| `GET /api/bookings/my` | Signed-in user, manager, or admin | None | 200 list of user bookings | 401 |
| `GET /api/events/{event_id}/bookings` | Admin or assigned manager | None | 200 list of event bookings | 401; 403 manager ownership denial; 404 event missing |
| `DELETE /api/bookings/{booking_id}` | Admin, assigned manager, or booking owner | None | 204 | 401; 403; 404 booking missing |
| `GET /api/docs` | Public API documentation | None | 200 documentation page | — |

## C6. JWT authentication design

### Figure 4. Login, request, refresh, and logout

```mermaid
sequenceDiagram
  participant B as Browser frontend
  participant A as FastAPI API
  participant D as PostgreSQL
  B->>A: POST /api/auth/login
  A->>D: Look up account and verify bcrypt hash
  A->>D: Save refresh-token hash and expiry
  A-->>B: Return access JWT and refresh token as JSON
  B->>B: Store both tokens in localStorage
  B->>A: Send protected request with bearer access token
  A->>A: Verify JWT signature and expiry, then load current user
  A-->>B: Return protected response or 401 for expired token
  B->>A: POST /api/auth/refresh with refresh token
  A->>D: Lock token record, revoke old token, and save new hash
  A-->>B: Return new access JWT and refresh token
  B->>A: Retry protected request once with new access token
  B->>A: POST /api/auth/logout with refresh token
  A->>D: Revoke refresh token
  A-->>B: Return 204 No Content
  B->>B: Remove tokens from localStorage
  Note over B,A: Reuse of a rotated refresh token is rejected and all of that user's refresh tokens are revoked
```

Access JWT claims set by the application are `sub` (account ID as a string) and `exp` (expiry). The application does not set `iat` or a role claim. The middleware reads the current account from PostgreSQL on each request and uses its current role. The signing algorithm defaults to HS256 and is configured by `ALGORITHM`; the key comes from `SECRET_KEY`.

The access token defaults to 60 minutes and the refresh token to 7 days, configurable with environment variables. This gives API requests a shorter-lived credential while allowing a session to continue by rotating the refresh token. The app stores both tokens in `localStorage`. This is simple for a course project, but JavaScript running through an XSS flaw could read them. The app does not use an HTTP-only cookie, so cookie-based CSRF protections do not apply; there is no explicit CSRF token. The frontend sends one refresh request after an API 401, retries the original request once, and clears stored tokens if refresh fails. Logout revokes the refresh token and clears local storage. A revoked access token can remain valid until its expiry because access tokens are not checked against a revocation list.

On each bearer-authenticated API request, middleware checks token format, signature, and expiry, checks that the account still exists, and queries `is_user_banned(db, user.id)` against `banned_users` to attach `request.state.is_banned` and `user.is_banned`. Banned users can still sign in, read `/api/auth/me`, and browse events so the frontend can display their banned banner, while `POST /api/bookings` is blocked with HTTP 403. Protected route rules then check role; event service checks manager ownership.

### Table 21. Token claims

| Claim / setting | Value | Purpose |
|---|---|---|
| `sub` | User ID as text | Identifies the account. |
| `iat` | Not set by the application | No issued-at claim is currently added. |
| `exp` | Expiration time | Rejects the token after its lifetime. |
| Role claim | Not included | Middleware reads role from the database. |
| Algorithm | `HS256` by default | HMAC signing and verification. |
| Secret | `SECRET_KEY` environment variable | Signs and verifies JWTs. |
| Access lifetime | 60 minutes by default | Limits the lifetime of each access token. |
| Refresh lifetime | 7 days by default | Limits the session renewal token. |

## C7. RBAC design

For a protected route, `RBACMiddleware` reads the bearer token, verifies it, looks up the current account, applies the route's required role, and then calls the route handler. Event services apply the manager-to-event ownership check before returning, updating, or deleting a specific event. The event list query filters manager results with `events.manager_id == manager_id`, so a manager receives only assigned events.

Roles are `user`, `manager`, and `admin`. The route policy module uses role strings (`admin`, `manager`, `user`) rather than a separate permission-constant catalog. There are no group permissions or generic permission dependency in the current code.

### Code excerpt: reusable role policy

```python
if method == "POST" and path == "/api/events":
    return {"admin"}, True
if method in {"PUT", "DELETE"} and EVENT_ITEM_PATH.fullmatch(path):
    return {"admin", "manager"}, True
if method == "POST" and path == "/api/managers":
    return {"admin"}, True
if method == "GET" and path == "/api/admin/stats":
    return {"admin"}, True
if method == "GET" and path == "/api/admin/bookings":
    return {"admin"}, True
if method == "GET" and path == "/api/admin/users":
    return {"admin"}, True
if method in {"POST", "DELETE"} and ADMIN_USER_BAN_PATH.fullmatch(path):
    return {"admin"}, True
if method == "DELETE" and ADMIN_USER_ITEM_PATH.fullmatch(path):
    return {"admin"}, True
return None
```

The shared middleware applies each returned role set before invoking a handler, and rejects `POST /api/bookings` with HTTP 403 when `request.state.is_banned` is true (backed by a second `is_user_banned` check in `booking_service.create_booking`). For event item routes, the service then checks whether the manager owns the event. To add a role, add its value to the user-role validation and define the route policies and service ownership behavior that role needs. There are no independent permission constants to extend. Admin account deletion has additional checks that prevent self-deletion and deletion of the last admin, and admin ban endpoints prevent self-banning and banning non-`user` accounts.

### Figure 5. Authorization flow

```mermaid
flowchart TD
  Request[API request] --> IsProtected{Protected route?}
  IsProtected -->|No| Handler[Route handler]
  IsProtected -->|Yes| Token[Check bearer token signature and expiry]
  Token -->|Invalid| E401[Return 401]
  Token -->|Valid| User[Load account and ban status from database]
  User -->|Missing| E401
  User --> Policy[Check required role]
  Policy -->|Denied| E403[Return 403]
  Policy -->|Allowed| BanCheck{Banned user booking event?}
  BanCheck -->|Yes| E403
  BanCheck -->|No| Own{Manager event ownership needed?}
  Own -->|No| Handler
  Own -->|Yes, assigned| Handler
  Own -->|No, not assigned| E403
```

## C8. Admin dashboard design

The frontend has one admin dashboard view. It loads platform summary metrics (`Total Bookings`, `Total Events`, `Total Users`, `Banned Users`), all events, all users, and all platform bookings. It displays metric cards at the top, an Events table with manager assignments, an Accounts table with `All / Active / Banned` filter buttons and Ban/Unban/Delete controls, and a Bookings table where admins can cancel any booking. There are no text search controls, pagination, bulk actions, CSV export, security view, or audit-log events in the current implementation.

### Figure 6. Admin page and endpoint calls

```mermaid
flowchart LR
  Admin[Admin] --> Dashboard[Admin dashboard in App.tsx]
  Dashboard -->|GET admin stats| Stats[Summary metric cards]
  Dashboard -->|GET events| Events[Event list with manager assignment]
  Dashboard -->|GET admin users| Users[Account list with All / Active / Banned filter]
  Dashboard -->|GET admin bookings| Bookings[Platform bookings list]
  Dashboard -->|POST or DELETE ban| Ban[Ban or unban regular user]
  Dashboard -->|DELETE user by ID| Delete[Delete eligible account]
  Dashboard -->|DELETE booking by ID| CancelBooking[Cancel any booking]
  Dashboard -->|POST managers| Assign[Create manager from event detail view]
```

### Table 22. Admin page and actions

| Page / view | Endpoints | Filters and pagination | Actions | Audit events |
|---|---|---|---|---|
| Admin dashboard | `GET /api/admin/stats`; `GET /api/events`; `GET /api/admin/users`; `GET /api/admin/bookings` | `All / Active / Banned` ban-status filter on Accounts (`?banned=true\|false` also supported on `GET /api/admin/users`); no text search or pagination | View summary metrics; review events, accounts, roles, ban status, manager assignments, and platform bookings; ban/unban regular users; delete eligible accounts; cancel any booking | None; audit log is not implemented. |
| Event detail (admin action) | `POST /api/managers` | Selects the currently viewed event; manager list is not a separate picker | Create a manager account assigned to that event | None. |
| User ban / unban | `POST /api/admin/users/{user_id}/ban`; `DELETE /api/admin/users/{user_id}/ban` | No bulk selection | Ban or unban one regular user account (disabled for self, managers, and admins) | None. |
| Account deletion | `DELETE /api/admin/users/{user_id}` | No bulk selection | Delete one eligible account; server clears any event assignment | None. |

## C9. Security design and threats

### Table 23. Threats and current defenses

| Threat | Current defense / limitation | File or module |
|---|---|---|
| Password database leak | Passwords are stored as bcrypt hashes. A pepper is not implemented. | `backend/security.py` |
| Stolen access token | Token expires after 60 minutes by default; token is sent in the Authorization header. A stolen token can be used until expiry. | `backend/security.py`, `frontend/src/api.ts` |
| Stolen refresh token | Only its hash is stored; rotation revokes prior token; reuse triggers revocation of the user's refresh tokens. Browser storage remains exposed to JavaScript. | `backend/services/auth_service.py`, `backend/models.py` |
| Brute-force login | No rate limit or lockout is implemented. | `backend/routers/auth.py` |
| Privilege escalation | Public registration sets role to `user`; admin-only routes use backend middleware; role is loaded from the database. | `backend/services/auth_service.py`, `backend/middleware.py` |
| Access to another user's record | Profile routes use the current authenticated user's ID. Manager event list queries filter by manager ID and item operations check assignment. | `backend/routers/auth.py`, `backend/repositories/event_repository.py`, `backend/services/event_service.py` |
| Cross-site scripting (XSS) | No specific Content Security Policy or XSS defense is configured in the reviewed code; localStorage tokens could be exposed by script injection. | `frontend/src/api.ts`, `backend/main.py` |
| Cross-site request forgery (CSRF) | Tokens are sent in Authorization headers; refresh/logout use JSON bodies rather than cookies. No CSRF token is implemented. | `frontend/src/api.ts` |
| CORS misuse | Current configuration allows all origins, methods, and headers; production origin restrictions are not implemented in the code. | `backend/main.py` |
| Secrets in repository | Secret and database settings are environment variables; `.env` files are not intended for committing. A development fallback JWT secret exists and must not be used in production. | `backend/security.py`, `backend/database.py`, `.gitignore` |
| SQL injection | SQLAlchemy ORM query expressions are used for database access. | `backend/repositories/` |
| Over-posting fields | Pydantic request schemas define accepted fields; public registration explicitly sets role to `user`. | `backend/schemas.py`, `backend/services/auth_service.py` |

## C10. Deployment on Vercel

The repository's `vercel.json` declares a backend service rooted at `backend` with entry point `main:app` and a frontend service rooted at `frontend` using Vite. Requests under `/api/:path*` are routed to the backend; other paths are routed to the frontend. The frontend API client uses the relative prefix `/api`, so local Vite proxy configuration and Vercel rewrites send requests to the API. PostgreSQL is external to Vercel and is reached through `DATABASE_URL`.

For a new deployment, connect the repository in Vercel, keep the project root at the repository root, set the environment variables in the Vercel project settings, and deploy. To redeploy after a code change, push to the connected deployment branch or start a deployment from the Vercel project. No database values or secret values belong in this report.

### Figure 7. Deployment layout

```mermaid
flowchart LR
  Git[Repository] --> V[Vercel deployment]
  V --> F[Frontend service: Vite build]
  V --> B[Backend service: FastAPI main:app]
  Client[Browser] -->|/ and static assets| F
  Client -->|/api/*| B
  B -->|DATABASE_URL connection| DB[(Hosted PostgreSQL)]
```

### Table 24. Environment variable names

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL used by SQLAlchemy and Psycopg. |
| `SECRET_KEY` | JWT signing and verification secret. |
| `ALGORITHM` | JWT signing algorithm; defaults to HS256. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime in minutes; defaults to 60. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh-token lifetime in days; defaults to 7. |
| `ADMIN_NAME` | Name for the initial admin account. |
| `ADMIN_EMAIL` | Email for the initial admin account. |
| `ADMIN_PHONE` | Phone for the initial admin account. |
| `ADMIN_PASSWORD` | Password for the initial admin account; hashed on creation. |

## C11. Testing

No automated API test suite or frontend test command is currently included in the repository. The frontend package provides `npm run build`, which runs TypeScript compilation and the Vite production build; this checks compilation but does not verify endpoint behavior. API routes can be inspected manually through FastAPI's `/api/docs`, but no test results are claimed here.

### Table 25. Current test status

| Test name | Requirement checked | Result |
|---|---|---|
| Automated API tests | Authentication, ownership, role rules, and admin safeguards | Not implemented; no automated test files are present. |
| Token expiry and tampering tests | JWT expiry and signature validation | Not implemented as automated tests. |
| Group permission matrix and lockout tests | Group permissions and login lockout | Not applicable; groups and lockout are not implemented. |
| Frontend production build | Frontend TypeScript and Vite build | Available with `cd frontend` then `npm run build`; this report does not claim a run result. |
| Manual API checks | API behavior through `/api/docs` | Can be performed manually; no results recorded in this report. |

# Part D. Evidence: Screenshots of the Running Application

Screenshot evidence captions are retained below; the visual files are omitted from this report copy. Token values have been masked in the S8 evidence description.

## D1. User Side

### S1. Login validation


### S2. Logged-in user page


### S3. Profile and password form


### S5. Group permissions


### S6. RBAC denial


### S22. Banned user notice


### S23. Booking confirmation


### S24. Profile and bookings


## D2. Security Behaviour

### S7. Authorization header and expired token


### S8. Refresh request


## D3. Admin Dashboard


### S21. Dashboard account list


### S25. Banned account management


### S26. Manager booking cancellation


## D4. Deployment

### S18. Vercel production deployment and domain


### S19. Vercel environment variable names


### S20. Live API documentation


## D5. Tests



# Part E. Project Management and Conclusion

## E1. How to Run and Test

### Prerequisites

- Git
- Python 3.10 or newer
- Node.js 22 or newer, with npm
- A running PostgreSQL database and a database created for this project

### Get the project and configure the backend

1. Clone the repository and enter its folder:

   ```powershell
   git clone https://github.com/SharukH-9s/CSE-309-Booking-Platform.git
   Set-Location CSE-309-Booking-Platform
   ```

2. From the repository root, copy the example environment file:

   ```powershell
   Copy-Item backend/.env.example backend/.env
   ```

3. Edit `backend/.env` with values for the local database and admin account. These are examples only; replace the database username, password, host, database name, and local admin password with values for the local setup.

   | Variable | Example value |
   |---|---|
   | `DATABASE_URL` | `postgresql+psycopg://postgres:local-password@localhost:5432/booking_platform` |
   | `SECRET_KEY` | `local-development-only-change-this-to-a-long-random-value` |
   | `ALGORITHM` | `HS256` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
   | `REFRESH_TOKEN_EXPIRE_DAYS` | `7` |
   | `ADMIN_NAME` | `Project Admin` |
   | `ADMIN_EMAIL` | `admin@example.com` |
   | `ADMIN_PHONE` | `+8801000000000` |
   | `ADMIN_PASSWORD` | `LocalAdmin-ChangeMe-123!` |

4. In a terminal at the repository root, create and activate the Python environment, install the backend packages, and start FastAPI:

   ```powershell
   Set-Location backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   fastapi dev main.py
   ```

   FastAPI starts at `http://localhost:8000`. The app creates missing database tables and seeds the admin configured by `ADMIN_*` when it starts.

### Start the frontend

5. Open a second terminal at the repository root and run:

   ```powershell
   Set-Location frontend
   npm install
   npm run dev
   ```

6. Open `http://localhost:5173`. The Vite development server forwards `/api` requests to the backend on port 8000. The API documentation is at `http://localhost:8000/api/docs`.

### Available checks

7. In a third terminal, run the frontend production build check:

   ```powershell
   Set-Location frontend
   npm run build
   ```

   This runs TypeScript compilation and the Vite build. The repository does not currently include automated backend tests or a separate frontend test runner, so there is no `pytest`, Jest, or Vitest command to run.

8. With the backend running, check its health endpoint in PowerShell:

   ```powershell
   Invoke-RestMethod http://localhost:8000/api/health
   ```

   A healthy response is `status: ok`. Authentication, refresh, logout, role checks, and event operations can also be checked manually in the API docs and in the app; no automated test results are claimed here.

### Test account sign-in

Use the **admin** and **user** test accounts listed in the PDF report Appendix. Their user IDs and passwords are intentionally kept out of this Markdown file. The admin account is seeded from the local `ADMIN_*` values; the user account must already exist in the configured database.

## E2. GitHub Work

The table lists the repository's completed issues and pull requests, plus direct commits for later work that did not go through a pull request. Commit authorship below follows the names shown in Git history.

| Issue | Pull request or commit | What it delivered |
|---|---|---|
| [#1 Add project documentation (PRD, SRS, TDD)](https://github.com/SharukH-9s/CSE-309-Booking-Platform/issues/1) | [PR #2: docs: add PRD, SRS, and TDD files](https://github.com/SharukH-9s/CSE-309-Booking-Platform/pull/2) | Added the initial project requirements and technical design documents. |
| [#3 Update project documentation (PRD, SRS, TDD)](https://github.com/SharukH-9s/CSE-309-Booking-Platform/issues/3) | [PR #4: docs: add missing sections to PRD, SRS, and TDD](https://github.com/SharukH-9s/CSE-309-Booking-Platform/pull/4) | Expanded the project documentation with missing sections. |
| [#5 feat: Event Management CRUD](https://github.com/SharukH-9s/CSE-309-Booking-Platform/issues/5) | [PR #6: feat: implement event management CRUD](https://github.com/SharukH-9s/CSE-309-Booking-Platform/pull/6) | Implemented event create, read, update, and delete workflows. |
| No linked issue recorded | [Commit a0c523b](https://github.com/SharukH-9s/CSE-309-Booking-Platform/commit/a0c523b): feat: add PostgreSQL auth and role-based event management | Added PostgreSQL-backed authentication and role-based event management. |
| No linked issue recorded | [Commit 266b79d](https://github.com/SharukH-9s/CSE-309-Booking-Platform/commit/266b79d): feat: add refresh tokens and admin dashboard | Added refresh tokens and the admin dashboard. |
| No linked issue recorded | [Commit b0c139d](https://github.com/SharukH-9s/CSE-309-Booking-Platform/commit/b0c139d): feat: expose protected actions for RBAC feedback | Exposed protected actions in the app so denied requests can provide authorization feedback. |
| No linked issue recorded | [Commit 87d669f](https://github.com/SharukH-9s/CSE-309-Booking-Platform/commit/87d669f): fix: guard nullable user in admin dashboard | Added a guard for a nullable user in the admin dashboard. |
| No linked issue recorded | [Commit f78ba4b](https://github.com/SharukH-9s/CSE-309-Booking-Platform/commit/f78ba4b): fix: serve api docs at /api/docs for vercel | Configured API documentation routing for the Vercel deployment. |
| [#7 feat: User event booking and cancellation system](https://github.com/SharukH-9s/CSE-309-Booking-Platform/issues/7) | [PR #8: feat: implement event booking and cancellation system](https://github.com/SharukH-9s/CSE-309-Booking-Platform/pull/8) | Implemented event bookings, attendee lists for managers and admins, and booking cancellation. |
| [#9 feat: Admin user ban system and booking restriction](https://github.com/SharukH-9s/CSE-309-Booking-Platform/issues/9) | [PR #10: feat: add user ban table, verification check, and booking restriction](https://github.com/SharukH-9s/CSE-309-Booking-Platform/pull/10) | Added the `banned_users` table, per-request ban verification in middleware, admin ban/unban endpoints with safeguards, a persistent banned UI banner, and booking restrictions for banned users. |
| [#11 feat: Admin dashboard metrics, bookings overview, and banned user filter](https://github.com/SharukH-9s/CSE-309-Booking-Platform/issues/11) | [PR #12: feat: add booking metrics, platform bookings view, and banned user filtering to admin dashboard](https://github.com/SharukH-9s/CSE-309-Booking-Platform/pull/12) | Added `GET /api/admin/stats` summary metrics, `GET /api/admin/bookings` platform bookings overview with cancellation, and `?banned=true\|false` / `All / Active / Banned` user filtering in the admin dashboard. |

### Work timeline and attribution

- **October 2026:** Initial project documentation was added, then expanded through the documentation issues and pull requests. Git history attributes the implementation commits to `SharukH-9s`; the merge commits use the account's full display name.
- **November 3, 2026:** Event CRUD was merged through PR #6. The repository also received the Vercel API-docs routing change.
- **November 24, 2026:** PostgreSQL authentication, role-based event management, refresh tokens, and the admin dashboard were committed directly to `main` by `SharukH-9s`. Issue #7 and PR #8 added event booking, attendee lists for managers and admins, and booking cancellation. Issue #9 and PR #10 added the `banned_users` table, per-request ban verification, admin ban/unban endpoints, and booking restrictions. Issue #11 and PR #12 added admin summary metrics, the platform-wide bookings table, and banned-status user filtering.

The repository records changes over time but does not document how work was divided among individual team members, so this report does not assign unrecorded tasks to people.

## E3. Limitations

- Groups and group-level permissions are not implemented; managers are assigned to individual events.
- The admin dashboard supports summary metrics, event/account/booking lists, `All / Active / Banned` user filtering, ban/unban, booking cancellation, and eligible account deletion, but has no activity log, security view, text search, pagination, bulk actions, or CSV export.
- Audit logging, brute-force rate limiting or lockout, role changes, and session listing or per-session revocation are not implemented.
- Access and refresh tokens are stored in browser `localStorage`. A successful script injection could read them; access tokens are not checked against a revocation list.
- The API does not use `httpOnly` cookies or a CSRF token. CORS currently allows all origins, methods, and headers, and no specific Content Security Policy is configured.
- There is no automated API test suite or dedicated frontend test runner. The frontend build checks compilation but does not test API behavior.
- Part D's supplied S5 image shows the admin dashboard rather than group permissions; S6 shows HTTP 401 rather than an RBAC 403; S7 does not demonstrate an expired-token 401; and S8 does not show an `httpOnly` cookie. These evidence gaps are noted beside the screenshots.
- No other unresolved software bugs are documented in the repository at the time of writing.

## E4. Future Work

1. Add automated API and frontend tests for authentication, token refresh and reuse, role checks, ownership, and admin safeguards, so regressions can be caught consistently.
2. Move browser credentials to secure `httpOnly` cookies and add the CSRF protections required for cookie-based authentication, reducing exposure to script injection.
3. Add login rate limiting and account lockout controls, then restrict production CORS origins to the deployed frontend.
4. Add an audit trail and security activity view so administrators can review sensitive account and content changes.
5. Implement group membership and permissions only if the product scope requires shared ownership beyond one manager per event.
6. Add export and dashboard search/filter controls if administrators need to manage larger account or event lists.

## E5. Sources, Libraries and Tools

The library rows list the direct dependencies declared in project manifests. The checked-in lockfile pins frontend resolutions; Python requirements specify ranges rather than a complete lockfile. The table also includes project tools and the security references named in this report.

| Name | Version or link | Use |
|---|---|---|
| React | [`^19.3.0`](https://react.dev/) | Frontend UI. |
| React DOM | [`^19.3.0`](https://react.dev/) | Renders the React UI in the browser. |
| TypeScript | [`^7.0.2`](https://www.typescriptlang.org/) | Frontend type checking and compilation. |
| Vite | [`^8.3.2`](https://vite.dev/) | Frontend development server and production build. |
| `@vitejs/plugin-react` | [`^6.1.1`](https://github.com/vitejs/vite-plugin-react) | React integration for Vite. |
| `@types/react`, `@types/react-dom` | [`^19.3.0`](https://www.npmjs.com/) | Type declarations for React and React DOM. |
| FastAPI (standard extras) | [`>=0.141.1`](https://fastapi.tiangolo.com/) | API routes, validation, development server, and generated OpenAPI documentation. |
| SQLAlchemy | [`>=2.0.0`](https://www.sqlalchemy.org/) | Database ORM and PostgreSQL access. |
| Psycopg binary | [`>=3.2.0`](https://www.psycopg.org/psycopg3/) | PostgreSQL driver. |
| `python-jose[cryptography]` | [`>=3.3.0`](https://github.com/mpdavis/python-jose) | JWT encoding and verification. |
| Passlib with bcrypt | [`passlib[bcrypt] >=1.7.4`](https://passlib.readthedocs.io/) | Password hashing and verification. |
| bcrypt | [`<4.1`](https://pypi.org/project/bcrypt/) | Password-hashing backend version constraint. |
| python-dotenv | [`>=1.0.0`](https://pypi.org/project/python-dotenv/) | Loads backend settings from `backend/.env`. |
| PostgreSQL | [Official documentation](https://www.postgresql.org/docs/) | Persistent relational database. The deployment's server version is not pinned in the repository. |
| Python and Node.js | [Python](https://www.python.org/), [Node.js](https://nodejs.org/) | Runtime environments for the backend and frontend. The README specifies Python 3.10+ and Node.js 22+. |
| Vercel | [Documentation](https://vercel.com/docs) | Hosts the frontend and FastAPI backend using `vercel.json`. |
| Git and GitHub | [Git](https://git-scm.com/doc), [repository](https://github.com/SharukH-9s/CSE-309-Booking-Platform) | Version control, issue tracking, and pull requests. |
| Swagger UI / OpenAPI | [FastAPI docs](https://fastapi.tiangolo.com/features/#automatic-docs) | API documentation generated by FastAPI at `/api/docs`. |
| Mermaid | [Documentation](https://mermaid.js.org/) | Architecture, authorization, and request-flow diagrams in this report. |
| RFC 7519: JSON Web Token (JWT) | [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) | Reference for JWT claims and token format. |
| OWASP Application Security Verification Standard | [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Security requirements reference. |
| FastAPI Security and Middleware documentation | [Security](https://fastapi.tiangolo.com/tutorial/security/), [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) | Framework reference for API security and middleware concepts. |




## Appendix. Video Demo


video link - https://drive.google.com/file/d/1nD4DwmDDG9_D6RwWKST1bavX9i4HxisO/view?usp=sharing
