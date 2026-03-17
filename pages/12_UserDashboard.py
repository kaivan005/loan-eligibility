import io
from pathlib import Path

import streamlit as st
from PIL import Image

from lib import ui
from lib.auth import get_current_user, logout_user, require_user_login
from lib.feedback import get_feedback_for_user
from lib.mongo import get_eligibility_for_user


image = Image.open("assets/logo.png")
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ - User Dashboard", page_icon=byte_im, layout="wide")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

ui.hide_streamlit_chrome()
require_user_login()

nav_links = [
    ("Home", "/"),
    ("Eligibility", "/Eligibility"),
    ("Calculator", "/Calculator"),
    ("Credit Help", "/CreditAssistance"),
    ("About", "/About"),
    ("Help", "/Help"),
]

ui.navbar(
    cta_href="/Eligibility",
    cta_label="Check Eligibility",
    nav_links=nav_links,
    active_page="/UserDashboard",
)

user = get_current_user() or {}
name = user.get("full_name", "User")
email = user.get("email", "")

st.title("User Dashboard")
st.caption(f"Welcome, {name}")

if st.button("Logout", type="secondary"):
    logout_user()
    st.switch_page("pages/11_Login.py")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Profile")
    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")

with col2:
    st.subheader("Quick Actions")
    st.page_link("pages/1_Application.py", label="Open Loan Application", icon="🧾")
    st.page_link("pages/13_Feedback.py", label="Give Feedback", icon="💬")

st.divider()
st.subheader("Your Eligibility Predictions")
eligibility_items = get_eligibility_for_user(email)
if not eligibility_items:
    st.info("No eligibility predictions found yet.")
else:
    for item in eligibility_items[:10]:
        person = item.get("person", {})
        result = item.get("result", {})
        status = result.get("status", "-")
        score = result.get("score", "-")
        loan_amount = person.get("loanAmount", 0) or 0
        rejection_reasons = result.get("rejection_reasons", [])
        created_at = item.get("created_at", "")
        status_color = "#dcfce7" if result.get("eligible") else "#fef2f2"
        border_color = "#22c55e" if result.get("eligible") else "#ef4444"
        reasons_html = ""
        if rejection_reasons:
            reasons_html = "<br/><strong>Reasons:</strong> " + " · ".join(rejection_reasons)
        st.markdown(
            f"""
            <div style='border-left:4px solid {border_color};background:{status_color};
                 padding:12px 16px;margin-bottom:10px;border-radius:8px;'>
              <strong>Status:</strong> {status} &nbsp;|&nbsp; <strong>Score:</strong> {score}/100<br/>
              <strong>Loan Requested:</strong> ₹{loan_amount:,.0f}{reasons_html}<br/>
              <small style='color:#6b7280;'>Checked: {created_at}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()
st.subheader("Your Recent Feedback")
feedback_items = get_feedback_for_user(email)
if not feedback_items:
    st.info("No feedback submitted yet.")
else:
    for item in feedback_items[:5]:
        st.markdown(
            f"""
            <div class='card1' style='padding: 14px; margin-bottom: 10px;'>
              <strong>Rating:</strong> {item.get('rating', '-')}/5<br/>
              <strong>Message:</strong> {item.get('message', '')}<br/>
              <small style='color:#6b7280;'>Submitted: {item.get('created_at', '')}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

ui.footer()
