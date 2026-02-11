import streamlit as st
from pathlib import Path
from PIL import Image
import io
import os

image = Image.open('assets/logo.png')
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ Admin Login", page_icon=byte_im, layout="centered")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Hide streamlit chrome
st.markdown(
    """
    <style>
        header[data-testid='stHeader']{display:none;}
        [data-testid='stSidebar']{display:none;}
        [data-testid='collapsedControl']{display:none;}
        .stForm{
            border: 0px solid #e5e7eb;
            }
    </style>
    """,
    unsafe_allow_html=True,
)

# Redirect if already logged in
if st.session_state.get("admin_logged_in"):
    st.switch_page("admin.py")
from PIL import Image
import io

image = Image.open('assets/logo1.png')
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()

# Center the login form
col1 = st.columns(1)[0]

with col1:
    
    st.image(image, width=200)
    with st.form("admin_login_form"):
        username = st.text_input(
            "Username",
            placeholder="Enter username",
            key="login_username"
        )
        password = st.text_input(
            "Password",
            placeholder="Enter password",
            type="password",
            key="login_password"
        )
        
        submit = st.form_submit_button("Login", use_container_width=True, type="primary")
        
        if submit:
            # Get credentials from secrets or env vars
            admin_user = st.secrets.get("auth", {}).get("username", os.getenv("ADMIN_USERNAME", "admin"))
            admin_pass = st.secrets.get("auth", {}).get("password", os.getenv("ADMIN_PASSWORD", "admin"))
            
            if username == admin_user and password == admin_pass:
                st.session_state["admin_logged_in"] = True
                st.success("✓ Login successful!")
                st.switch_page("pages/9_Admin.py")
            else:
                st.error("❌ Invalid username or password")
    
    st.markdown(
        """
        <div style='text-align: center; margin-top: 40px; color: #9ca3af; font-size: 12px;'>
            <p style='margin-top: 20px;'>© 2026 LoanIQ Admin Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
