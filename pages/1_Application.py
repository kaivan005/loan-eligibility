import streamlit as st
from pathlib import Path
from lib.logic import evaluate_eligibility
from lib import ui

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


nav_links = [
  ("Home", "/"),
  ("Eligibility", "/Eligibility"),
  ("Calculator", "/Calculator"),
  ("Credit Help", "/CreditAssistance"),
  ("About", "/About"),
  ("Help", "/Help"),
]

ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/Application")

if "application" not in st.session_state:
    st.session_state.application = {
        "fullName": "",
        "email": "",
        "phone": "",
        "dateOfBirth": "",
        "address": "",
        "city": "",
        "state": "",
        "zipCode": "",
        "employmentStatus": "employed",
        "employer": "",
        "occupation": "",
        "employmentYears": "",
        "monthlyIncome": "",
        "creditScore": "",
        "existingLoans": "",
        "monthlyExpenses": "",
        "bankAccount": "yes",
        "loanAmount": "",
        "loanPurpose": "home",
        "loanTerm": "30",
    }

ui.section_title("Loan Application Form")
st.caption("Complete all sections to submit your loan application")

if "step" not in st.session_state:
    st.session_state.step = 1

step = st.session_state.step
cols = st.columns(2)
with cols[0]:
    st.write(f"Step {step} of 4")
with cols[1]:
    st.progress(step / 4)

st.divider()

app = st.session_state.application

if step == 1:
    ui.section_title("Personal Information")
    c1, c2 = st.columns(2)
    with c1:
        app["fullName"] = st.text_input("Full Name *", app["fullName"])
        app["phone"] = st.text_input("Phone *", app["phone"])
        app["address"] = st.text_input("Street Address *", app["address"])
        app["city"] = st.text_input("City *", app["city"])
    with c2:
        app["email"] = st.text_input("Email *", app["email"])
        app["dateOfBirth"] = st.date_input("Date of Birth *")
        app["state"] = st.text_input("State *", app["state"])
        app["zipCode"] = st.text_input("ZIP Code *", app["zipCode"])

elif step == 2:
    ui.section_title("Employment Information")
    app["employmentStatus"] = st.selectbox("Employment Status *", ["employed","self-employed","business","retired","unemployed"], index=["employed","self-employed","business","retired","unemployed"].index(app["employmentStatus"]))
    c1, c2 = st.columns(2)
    with c1:
        app["employer"] = st.text_input("Employer / Company *", app["employer"])
        app["employmentYears"] = st.number_input("Years of Employment *", value=float(app["employmentYears"] or 0), min_value=0.0, step=1.0)
    with c2:
        app["occupation"] = st.text_input("Occupation / Job Title *", app["occupation"])
        app["monthlyIncome"] = st.number_input("Monthly Income ($) *", value=float(app["monthlyIncome"] or 0), min_value=0.0, step=100.0)

elif step == 3:
    ui.section_title("Financial Information")
    c1, c2 = st.columns(2)
    with c1:
        app["creditScore"] = st.number_input("Credit Score (300-850) *", value=float(app["creditScore"] or 650), min_value=300.0, max_value=850.0, step=1.0)
        app["monthlyExpenses"] = st.number_input("Monthly Expenses ($) *", value=float(app["monthlyExpenses"] or 0), min_value=0.0, step=50.0)
    with c2:
        app["existingLoans"] = st.number_input("Existing Monthly Loan Payments ($) *", value=float(app["existingLoans"] or 0), min_value=0.0, step=50.0)
        app["bankAccount"] = st.selectbox("Do you have a bank account?", ["yes","no"], index=["yes","no"].index(app["bankAccount"]))

elif step == 4:
    ui.section_title("Loan Details")
    c1, c2 = st.columns(2)
    with c1:
        app["loanAmount"] = st.number_input("Requested Loan Amount ($) *", value=float(app["loanAmount"] or 0), min_value=0.0, step=1000.0)
        app["loanTerm"] = st.number_input("Loan Term (years) *", value=float(app["loanTerm"] or 30), min_value=1.0, step=1.0)
    with c2:
        app["loanPurpose"] = st.selectbox("Loan Purpose", ["home","auto","business","education","personal"], index=["home","auto","business","education","personal"].index(app["loanPurpose"]))

st.divider()

c_prev, c_next = st.columns([1,1])
with c_prev:
    if st.button("← Previous", use_container_width=True, disabled=step == 1):
        st.session_state.step = max(1, step - 1)
        st.rerun()
with c_next:
    if step < 4:
        if st.button("Next →", use_container_width=True):
            st.session_state.step = min(4, step + 1)
            st.rerun()
    else:
        if st.button("Submit Application", type="primary", use_container_width=True):
            result = evaluate_eligibility(app)
            st.session_state.eligibility = result
            st.success("Application processed.")

# Inline result summary (no separate Results page)
res = st.session_state.get("eligibility")
if res:
    st.divider()
    ui.section_title("Your Result")
    if res.eligible:
        st.success(f"🎉 Approved — Score {res.score}/100")
    else:
        st.error(f"Not Approved — Score {res.score}/100")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Max Loan Amount", f"${res.maxLoanAmount:,.0f}")
    with cols[1]:
        st.metric("Rate", f"{res.recommendedRate:.2f}% APR")
    with cols[2]:
        st.metric("Requested", f"${res.requestedAmount:,.0f}")
    st.write("Assessment Factors")
    for f in res.factors:
        if f.status == "positive":
            st.success(f"{f.name} — {f.impact}")
        elif f.status == "negative":
            st.error(f"{f.name} — {f.impact}")
        else:
            st.warning(f"{f.name} — {f.impact}")

ui.footer()
