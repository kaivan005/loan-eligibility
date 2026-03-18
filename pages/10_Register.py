import io
from pathlib import Path

import streamlit as st
from PIL import Image

from lib import ui
from lib.auth import register_user


image = Image.open("assets/logo.png")
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ - Register", page_icon=byte_im, layout="centered")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

ui.hide_streamlit_chrome()

st.markdown("""
<div style='text-align:center; padding: 24px 0;'>
    <h1 style='font-size: 36px; color: #111827; margin: 0 0 8px;'>Register</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='max-width: 420px; margin: 0 auto;'>", unsafe_allow_html=True)

with st.form("register_form"):
    full_name = st.text_input("Full Name", placeholder="Your full name")
    email = st.text_input("Email Address", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="Minimum 6 characters", help="At least 6 characters")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    st.markdown("")
    submitted = st.form_submit_button("📝 Create Account", type="primary", use_container_width=True)

if submitted:
    if password != confirm_password:
        st.error("❌ Passwords do not match.")
    else:
        ok, message = register_user(full_name, email, password)
        if ok:
            st.success("✓ Registration successful! You can now login.")
            st.info("Redirecting to login page...")
        else:
            st.error(f"❌ {message}")

st.markdown("")
st.markdown(
    """<div style='background: linear-gradient(135deg, #eff6ff, #dbeafe); border: 2px solid #93c5fd; 
    border-radius: 14px; padding: 16px; text-align: center;'>
    <strong style='color: #1e40af;'>Already have an account?</strong><br/>
    <span style='color: #4b5563; font-size: 14px;'>Sign in to access your loan applications</span>
    </div>""",
    unsafe_allow_html=True,
)
st.markdown("")

col1, col3 = st.columns([1, 1])
with col1:
    if st.button("🔐 Login", use_container_width=True, key="goto_login"):
        st.switch_page("pages/11_Login.py")
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
