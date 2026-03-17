from __future__ import annotations

import hashlib
import secrets
from typing import Any

import streamlit as st

from lib.mongo import (
    create_user,
    find_user_by_email,
    find_user_by_session_token,
    record_login_event,
    update_user_last_login,
    update_user_session_token,
)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(full_name: str, email: str, password: str) -> tuple[bool, str]:
    full_name = full_name.strip()
    normalized_email = email.strip().lower()

    if not full_name:
        return False, "Full name is required."
    if not normalized_email or "@" not in normalized_email:
        return False, "A valid email is required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    try:
        if find_user_by_email(normalized_email):
            return False, "An account with this email already exists."
        create_user(full_name=full_name, email=normalized_email, password_hash=_hash_password(password))
        return True, "Registration successful."
    except Exception:
        return False, "Unable to register right now. Please try again."


def authenticate_user(email: str, password: str) -> dict[str, Any] | None:
    normalized_email = email.strip().lower()
    password_hash = _hash_password(password)

    try:
        user = find_user_by_email(normalized_email)
        if user and user.get("password_hash") == password_hash:
            update_user_last_login(normalized_email)
            record_login_event(normalized_email, role="user", success=True)
            return {"full_name": user.get("full_name", ""), "email": user.get("email", normalized_email)}
        record_login_event(normalized_email, role="user", success=False)
    except Exception:
        return None

    return None


def record_admin_login(identifier: str, success: bool) -> None:
    try:
        record_login_event(identifier=identifier, role="admin", success=success)
    except Exception:
        pass


def is_registered_user(email: str) -> bool:
    normalized_email = email.strip().lower()
    if not normalized_email:
        return False
    try:
        return find_user_by_email(normalized_email) is not None
    except Exception:
        return False


def login_user(user: dict[str, Any]) -> None:
    email = user.get("email", "").strip().lower()
    token = secrets.token_urlsafe(24)
    try:
        update_user_session_token(email=email, token=token)
    except Exception:
        token = ""

    st.session_state["user_logged_in"] = True
    st.session_state["current_user"] = {
        "full_name": user.get("full_name", ""),
        "email": email,
    }
    st.session_state["auth_token"] = token
    if token:
        st.query_params["auth_token"] = token


def logout_user() -> None:
    current_user = st.session_state.get("current_user") or {}
    email = current_user.get("email", "").strip().lower()
    if email:
        try:
            update_user_session_token(email=email, token=None)
        except Exception:
            pass

    st.session_state["user_logged_in"] = False
    st.session_state.pop("current_user", None)
    st.session_state.pop("auth_token", None)
    try:
        if "auth_token" in st.query_params:
            del st.query_params["auth_token"]
    except Exception:
        pass


def bootstrap_user_session() -> None:
    if st.session_state.get("user_logged_in") and st.session_state.get("current_user"):
        return

    token = st.query_params.get("auth_token", "")
    if not token:
        return

    try:
        user = find_user_by_session_token(token)
    except Exception:
        return

    if not user:
        return

    st.session_state["user_logged_in"] = True
    st.session_state["current_user"] = {
        "full_name": user.get("full_name", ""),
        "email": user.get("email", ""),
    }
    st.session_state["auth_token"] = token


def get_auth_token() -> str:
    token = st.session_state.get("auth_token", "")
    if token:
        return token
    return st.query_params.get("auth_token", "")


def get_current_user() -> dict[str, Any] | None:
    bootstrap_user_session()
    return st.session_state.get("current_user")


def require_user_login() -> None:
    bootstrap_user_session()
    if not st.session_state.get("user_logged_in"):
        st.warning("Please log in to continue.")
        st.switch_page("pages/11_Login.py")
        st.stop()


def require_login() -> None:
    if not st.session_state.get("logged_in"):
        st.stop()

