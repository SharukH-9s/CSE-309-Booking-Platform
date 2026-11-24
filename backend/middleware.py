import re
from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from database import SessionLocal
from models import User
from repositories.ban_repository import is_user_banned
from repositories.user_repository import get_user_by_id
from security import decode_access_token

EVENT_ITEM_PATH = re.compile(r"^/api/events/\d+$")
EVENT_BOOKINGS_PATH = re.compile(r"^/api/events/\d+/bookings$")
BOOKING_ITEM_PATH = re.compile(r"^/api/bookings/\d+$")
BOOKING_EVENT_PATH = re.compile(r"^/api/bookings/event/\d+$")
ADMIN_USER_ITEM_PATH = re.compile(r"^/api/admin/users/\d+$")
ADMIN_USER_BAN_PATH = re.compile(r"^/api/admin/users/\d+/ban$")


class RBACMiddleware(BaseHTTPMiddleware):
    """Authenticate bearer tokens and enforce route-level role policies."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        policy = self._policy_for(request.method, request.url.path)
        user, auth_error = self._load_user(request)
        if auth_error is not None:
            return auth_error

        # Expose the database-backed user and ban status to handlers and services.
        request.state.current_user = user
        request.state.is_banned = bool(user and getattr(user, "is_banned", False))

        if policy is not None:
            allowed_roles, authentication_required = policy
            if authentication_required and user is None:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Authentication required"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if user is not None and allowed_roles is not None and user.role not in allowed_roles:
                return JSONResponse(status_code=403, content={"detail": "You do not have permission"})

        if (
            user is not None
            and request.state.is_banned
            and request.method == "POST"
            and request.url.path == "/api/bookings"
        ):
            return JSONResponse(status_code=403, content={"detail": "Your account is banned from booking events"})

        return await call_next(request)

    @staticmethod
    def _policy_for(method: str, path: str) -> tuple[set[str] | None, bool] | None:
        if method == "GET" and path == "/api/auth/me":
            return None, True
        if method == "PATCH" and path == "/api/auth/me":
            return None, True
        if method == "POST" and path == "/api/auth/change-password":
            return None, True
        if method == "POST" and path == "/api/events":
            return {"admin"}, True
        if method in {"PUT", "DELETE"} and EVENT_ITEM_PATH.fullmatch(path):
            return {"admin", "manager"}, True
        if method == "POST" and path == "/api/bookings":
            return {"admin", "manager", "user"}, True
        if method == "GET" and path == "/api/bookings/my":
            return {"admin", "manager", "user"}, True
        if method == "GET" and (BOOKING_EVENT_PATH.fullmatch(path) or EVENT_BOOKINGS_PATH.fullmatch(path)):
            return {"admin", "manager"}, True
        if method == "DELETE" and BOOKING_ITEM_PATH.fullmatch(path):
            return {"admin", "manager", "user"}, True
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

    @staticmethod
    def _load_user(request: Request) -> tuple[User | None, JSONResponse | None]:
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None, None

        scheme, separator, token = authorization.partition(" ")
        if not separator or scheme.lower() != "bearer" or not token.strip():
            return None, JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = decode_access_token(token.strip())
        if user_id is None:
            return None, JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        with SessionLocal() as db:
            user = get_user_by_id(db, user_id)
            if user is None:
                return None, JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired token"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user.is_banned = is_user_banned(db, user.id)
            # Copy scalar values before closing the database session.
            db.expunge(user)
            return user, None
