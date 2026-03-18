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

st.markdown("""
<div style='text-align:center; padding: 24px 0;'>
    <h1 style='font-size: 36px; color: #111827; margin: 0 0 8px;'>Login</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='max-width: 420px; margin: 0 auto;'>", unsafe_allow_html=True)

with st.form("unified_login_form"):
    identifier = st.text_input(
        "Username",
        placeholder="Username",
        help="Enter your username"
    )
    password = st.text_input("Password", type="password", placeholder="••••••••")
    st.markdown("")
    submitted = st.form_submit_button("🔓 Login", type="primary", use_container_width=True)

if submitted:
    entered_id = identifier.strip()
    admin_user = st.secrets.get("auth", {}).get("username", os.getenv("ADMIN_USERNAME", "admin"))
    admin_pass = st.secrets.get("auth", {}).get("password", os.getenv("ADMIN_PASSWORD", "admin"))

    if entered_id == admin_user and password == admin_pass:
        st.session_state["admin_logged_in"] = True
        record_admin_login(identifier=entered_id, success=True)
        st.success("✓ Admin login successful!")
        st.switch_page("pages/9_Admin.py")
    else:
        user = authenticate_user(entered_id, password)
        if user:
            login_user(user)
            st.success("✓ Login successful!")
            st.switch_page("pages/12_UserDashboard.py")
        else:
            if entered_id == admin_user:
                record_admin_login(identifier=entered_id, success=False)
            st.error("❌ Invalid email/username or password.")

st.markdown("")
st.markdown(
    """<div style='background: linear-gradient(135deg, #f0fdf4, #dcfce7); border: 2px solid #86efac; 
    border-radius: 14px; padding: 16px; text-align: center;'>
    <strong style='color: #166534;'>New user?</strong><br/>
    <span style='color: #4b5563; font-size: 14px;'>Create an account to get started with LoanIQ</span>
    </div>""",
    unsafe_allow_html=True,
)
st.markdown("")

col1, col3 = st.columns([1, 1])
with col1:
    if st.button("📝 Register", use_container_width=True, key="goto_register"):
        st.switch_page("pages/10_Register.py")
with col3:
    if st.button("🏠 Home", use_container_width=True, key="goto_home"):
        st.switch_page("app.py")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """<div style='text-align: center; margin-top: 48px; padding-top: 24px; border-top: 1px solid #e5e7eb; color: #9ca3af; font-size: 12px;'>
    <p style='margin: 0;'>© 2026 LoanIQ. All rights reserved.</p>
    </div>""",
    unsafe_allow_html=True,
)
