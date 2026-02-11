import os
import streamlit as st


def require_login() -> None:
    """Require authentication before showing page content"""
    if not st.session_state.get("logged_in"):
        st.stop()

