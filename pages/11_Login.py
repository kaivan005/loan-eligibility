import io
from pathlib import Path
import os

import streamlit as st
from PIL import Image

from lib import ui
from lib.auth import authenticate_user, bootstrap_user_session, login_user, record_admin_login


image = Image.open("assets/logo.png")
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ - Login", page_icon=byte_im, layout="centered")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

ui.hide_streamlit_chrome()
bootstrap_user_session()

if st.session_state.get("user_logged_in"):
    st.switch_page("pages/12_UserDashboard.py")

st.title("Login")
st.caption("One login form for both user and admin")

with st.form("unified_login_form"):
    identifier = st.text_input("Email or Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

if submitted:
    entered_id = identifier.strip()
    admin_user = st.secrets.get("auth", {}).get("username", os.getenv("ADMIN_USERNAME", "admin"))
    admin_pass = st.secrets.get("auth", {}).get("password", os.getenv("ADMIN_PASSWORD", "admin"))

    if entered_id == admin_user and password == admin_pass:
        st.session_state["admin_logged_in"] = True
        record_admin_login(identifier=entered_id, success=True)
        st.success("Admin login successful.")
        st.switch_page("pages/9_Admin.py")
    else:
        user = authenticate_user(entered_id, password)
        if user:
            login_user(user)
            st.success("Login successful.")
            st.switch_page("pages/12_UserDashboard.py")
        else:
            if entered_id == admin_user:
                record_admin_login(identifier=entered_id, success=False)
            st.error("Invalid credentials.")

st.info("New user? Please register first.")
st.page_link("pages/10_Register.py", label="Create Account", icon="📝")

c1, c2 = st.columns(2)
with c1:
    st.page_link("pages/10_Register.py", label="Register", icon="📝")
with c2:
    st.page_link("app.py", label="Back to Home", icon="🏠")
