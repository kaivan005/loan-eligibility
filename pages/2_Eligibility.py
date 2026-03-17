import streamlit as st
from pathlib import Path
from urllib.parse import quote
from lib import ui
from lib.mongo import save_eligibility
from lib.auth import bootstrap_user_session, get_current_user, is_registered_user
from lib.feedback import add_feedback

from PIL import Image
import io

image = Image.open('assets/logo.png')
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ", page_icon=byte_im, layout="wide")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
ui.hide_streamlit_chrome()
bootstrap_user_session()

nav_links = [
  ("Home", "/"),
  ("Eligibility", "/Eligibility"),
  ("Calculator", "/Calculator"),
  ("Credit Help", "/CreditAssistance"),
  ("About", "/About"),
  ("Help", "/Help"),
]


ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/Eligibility")

ui.section_title("AI-Powered Eligibility Check")
st.markdown(
    "<p style='text-align:center; margin: 0 auto 12px auto; color: var(--gray-700); font-size: 14px;'>Get instant loan eligibility assessment using simple inputs</p>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Applicant Information", anchor=False)
    current_user = get_current_user() or {}
    is_user_logged_in = bool(st.session_state.get("user_logged_in") and current_user.get("email"))

    if not is_user_logged_in:
        st.info("You can browse the website, but eligibility check requires registration and login.")
    
    # Basic Information
    fullName = st.text_input("Full Name", "", placeholder="Enter applicant name")
    email = st.text_input(
        "Email",
        value=current_user.get("email", "") if is_user_logged_in else "",
        placeholder="Enter your email address",
        disabled=is_user_logged_in,
    )

    gender = st.selectbox(
        "Gender",
        ["Select Gender", "Male", "Female", "Other"],
        index=0,
        accept_new_options=False,
    )

    married = st.selectbox(
        "Marital Status",
        ["Select Marital Status", "Yes", "No"],
        index=0,
    )

    dependents_raw = st.text_input("Number of Dependents", "", placeholder="e.g., 0, 1, 2")
    
    # Education & Employment
    education = st.selectbox(
        "Education Level",
        ["Select Education Level", "Below Graduate", "Graduate", "Post Graduate"],
        index=0,
    )
    self_employed = st.selectbox(
        "Self Employed",
        ["Select Employment Type", "Yes", "No"],
        index=0,
    )
    
    # Income Information (no default values shown)
    applicant_income_raw = st.text_input("Applicant Income (Annual - ₹)", "", placeholder="e.g., 750000")
    coapplicant_income_raw = st.text_input("Co-applicant Income (Annual - ₹)", "", placeholder="e.g., 250000")
    
    # Loan Details
    loan_amount_raw = st.text_input("Loan Amount (₹)", "", placeholder="e.g., 1500000 (will be scaled to thousands for the model)")
    loan_amount_term_raw = st.text_input("Loan Amount Term (in months)", "", placeholder="e.g., 240")
    
    # Credit & Property
    credit_history = st.selectbox(
        "Credit History Available",
        ["Select Credit History", "Yes", "No"],
        index=0,
        help="Does applicant have credit history (1) or not (0)",
    )
    property_area = st.selectbox(
        "Property Area",
        ["Select Property Area", "Urban", "Rural", "Semiurban"],
        index=0,accept_new_options=False
    )

    if st.button("Check Eligibility", type="primary", use_container_width=True):
        errors = []

        if not is_user_logged_in:
            errors.append("Please login/register to check eligibility")
        elif not is_registered_user(email):
            errors.append("Only registered users can check eligibility")

        def parse_int(raw: str, field: str) -> int:
            if not raw.strip():
                errors.append(f"{field} is required")
                return 0
            try:
                return int(raw.replace(",", "").strip())
            except ValueError:
                errors.append(f"{field} must be a whole number")
                return 0

        def parse_float(raw: str, field: str) -> float:
            if not raw.strip():
                errors.append(f"{field} is required")
                return 0.0
            try:
                return float(raw.replace(",", "").strip())
            except ValueError:
                errors.append(f"{field} must be a number")
                return 0.0

        if not email.strip():
            errors.append("Email is required")
        elif "@" not in email:
            errors.append("Email looks invalid")
        elif is_user_logged_in and email.strip().lower() != current_user.get("email", "").strip().lower():
            errors.append("Eligibility can only be checked with your logged-in email")

        # Validate selects
        if gender.startswith("Select"):
            errors.append("Please select Gender")
        if married.startswith("Select"):
            errors.append("Please select Marital Status")
        if education.startswith("Select"):
            errors.append("Please select Education Level")
        if self_employed.startswith("Select"):
            errors.append("Please select Employment Type")
        if credit_history.startswith("Select"):
            errors.append("Please select Credit History")
        if property_area.startswith("Select"):
            errors.append("Please select Property Area")

        dependents = parse_int(dependents_raw, "Number of Dependents")
        applicant_income = parse_float(applicant_income_raw, "Applicant Income")
        coapplicant_income = parse_float(coapplicant_income_raw, "Co-applicant Income")
        loan_amount = parse_float(loan_amount_raw, "Loan Amount")
        loan_amount_term = parse_int(loan_amount_term_raw, "Loan Amount Term")

        if errors:
            st.error("Please correct the following: " + "; ".join(errors))
        else:
            # Store the form data in session state
            st.session_state.form_data = {
                "fullName": fullName,
                "gender": gender,
                "married": married,
                "dependents": dependents,
                "education": education,
                "self_employed": self_employed,
                "email": email,
                "applicantIncome": applicant_income,
                "coapplicantIncome": coapplicant_income,
                "loanAmount": loan_amount,
                "loanAmountTerm": loan_amount_term,
                "creditHistory": credit_history,
                "propertyArea": property_area,
            }
            
            # Mark that we need to process with ML model
            st.session_state.processing = True
            st.session_state.eligibility_saved = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("Results", anchor=False)
    
    # Check if form was submitted and we're waiting for ML model
    if st.session_state.get("processing", False):
        st.markdown(
            """
            <div style='border: 2px solid #3b82f6; border-radius: 12px; padding: 48px 24px; background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%); text-align: center; margin-top: 16px;'>
                <div style='animation: spin 1s linear infinite; display: inline-block; margin-bottom: 20px;'>
                    <div style='font-size: 48px;'>⚙️</div>
                </div>
                <h3 style='color: #1e40af; margin: 16px 0;'>ML Model Processing</h3>
                <p style='color: #1e3a8a; margin: 12px 0; font-size: 16px;'>Our machine learning model is analyzing your application...</p>
                <p style='color: #3b82f6; margin: 12px 0; font-size: 14px;'>Please wait while we evaluate your eligibility</p>
            </div>
            <style>
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Call the ML model
        from lib.ml_integration import call_ml_model
        
        with st.spinner("Running ML model prediction..."):
            result = call_ml_model(st.session_state.form_data)
            st.session_state.eligibility = result
            st.session_state.processing = False
            st.session_state.eligibility_feedback_done = False
            st.rerun()
    
    # Show results if available
    elif st.session_state.get("eligibility"):
        from lib.ml_integration import get_rejection_reasons

        res = st.session_state.eligibility
        email = st.session_state.form_data.get("email", "") if st.session_state.get("form_data") else ""

        # Build mailto link with applicant details
        details_lines = [
            f"Name: {st.session_state.form_data.get('fullName','')}",
            f"Email: {email}",
            f"Gender: {st.session_state.form_data.get('gender','')}",
            f"Married: {st.session_state.form_data.get('married','')}",
            f"Dependents: {st.session_state.form_data.get('dependents','')}",
            f"Education: {st.session_state.form_data.get('education','')}",
            f"Self Employed: {st.session_state.form_data.get('self_employed','')}",
            f"Applicant Income: ₹{st.session_state.form_data.get('applicantIncome',0):,.0f}",
            f"Coapplicant Income: ₹{st.session_state.form_data.get('coapplicantIncome',0):,.0f}",
            f"Loan Amount: ₹{st.session_state.form_data.get('loanAmount',0):,.0f}",
            f"Loan Term (months): {st.session_state.form_data.get('loanAmountTerm','')}",
            f"Credit History: {st.session_state.form_data.get('creditHistory','')}",
            f"Property Area: {st.session_state.form_data.get('propertyArea','')}",
        ]
        body = quote("\n".join(details_lines))
        mailto = f"mailto:support@ailoanpro.com?subject=Loan%20Eligibility%20Details&body={body}"

        if res.eligible:
            st.success("You are Eligible for Loan! 🎉")
        else:
            st.error("❌ Not Eligible — Requires Review")
            st.markdown("Our team will contact you soon.")
            st.markdown("**Reasons for rejection:**")
            for reason in get_rejection_reasons(st.session_state.form_data):
                st.markdown(
                    f"<div style='background:#fef2f2;border-left:4px solid #ef4444;"
                    f"padding:10px 14px;margin:6px 0;border-radius:6px;color:#991b1b;"
                    f"font-size:14px;'>⚠️ {reason}</div>",
                    unsafe_allow_html=True,
                )

        st.markdown(f"**Confidence Score:** {res.score}/100")

        if not st.session_state.get("eligibility_saved"):
            rejection_reasons = (
                get_rejection_reasons(st.session_state.form_data)
                if not res.eligible
                else []
            )
            payload = {
                "person": st.session_state.form_data,
                "result": {
                    "eligible": bool(res.eligible),
                    "score": res.score,
                    "status": "Eligible" if res.eligible else "Requires review",
                    "rejection_reasons": rejection_reasons,
                },
                "source": "eligibility_page",
                "user_email": current_user.get("email", ""),
            }
            try:
                save_eligibility(payload)
                st.session_state.eligibility_saved = True
            except Exception as exc:
                st.error(f"❌ Failed to save to database: {exc}")

        # ── Inline feedback form after each eligibility check ──────────────
        if is_user_logged_in and not st.session_state.get("eligibility_feedback_done"):
            st.divider()
            st.markdown("**How was your experience? Leave quick feedback:**")
            with st.form("post_eligibility_feedback"):
                fb_rating = st.slider("Rating", 1, 5, 5, key="elig_fb_rating")
                fb_message = st.text_area(
                    "Your feedback (optional)",
                    placeholder="Tell us what you think…",
                    key="elig_fb_msg",
                )
                fb_submit = st.form_submit_button("Submit Feedback", type="primary")
            if fb_submit:
                add_feedback(
                    user_email=current_user.get("email", ""),
                    user_name=current_user.get("full_name", ""),
                    rating=fb_rating,
                    message=fb_message or "No message provided.",
                )
                st.session_state.eligibility_feedback_done = True
                st.success("Thank you for your feedback!")
                st.rerun()
        elif is_user_logged_in and st.session_state.get("eligibility_feedback_done"):
            st.info("Feedback submitted. Thank you!")

    
    else:
        st.info("Fill in the form and check your eligibility. Results will appear here.")

ui.footer() 
