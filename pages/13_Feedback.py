import io
from pathlib import Path

import streamlit as st
from PIL import Image

from lib import ui
from lib.auth import get_current_user, require_user_login
from lib.feedback import add_feedback, get_feedback_for_user


image = Image.open("assets/logo.png")
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ - Feedback", page_icon=byte_im, layout="centered")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

ui.hide_streamlit_chrome()
require_user_login()

user = get_current_user() or {}
user_name = user.get("full_name", "User")
user_email = user.get("email", "")

st.title("Feedback")
st.caption("Share your experience with LoanIQ")

with st.form("feedback_form"):
    rating = st.slider("Rating", min_value=1, max_value=5, value=5)
    message = st.text_area("Your Feedback", placeholder="Tell us what worked well and what can be improved")
    submitted = st.form_submit_button("Submit Feedback", type="primary", use_container_width=True)

if submitted:
    if not message.strip():
        st.error("Please enter feedback before submitting.")
    else:
        add_feedback(user_email=user_email, user_name=user_name, rating=rating, message=message)
        st.success("Feedback submitted successfully.")

st.page_link("pages/12_UserDashboard.py", label="Back to Dashboard", icon="⬅️")

st.divider()
st.subheader("Your Feedback History")
items = get_feedback_for_user(user_email)
if not items:
    st.info("No feedback history found.")
else:
    for item in items:
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
