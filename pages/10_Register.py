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

st.title("Create User Account")
st.caption("Register to access your user dashboard and feedback module")

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    submitted = st.form_submit_button("Register", type="primary", use_container_width=True)

if submitted:
    if password != confirm_password:
        st.error("Passwords do not match.")
    else:
        ok, message = register_user(full_name, email, password)
        if ok:
            st.success("Registration successful. Please login.")
        else:
            st.error(message)

c1, c2 = st.columns(2)
with c1:
    st.page_link("pages/11_Login.py", label="Go to Login", icon="🔐")
with c2:
    st.page_link("app.py", label="Back to Home", icon="🏠")
