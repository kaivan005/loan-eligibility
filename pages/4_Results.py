import streamlit as st
from lib.logic import EligibilityResult
from lib import ui

from PIL import Image
import io

image = Image.open('assets/logo.png')
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ", page_icon=byte_im, layout="wide")

ui.section_title("Loan Application Result")
st.caption("Your application has been processed and evaluated")

res: EligibilityResult | None = st.session_state.get("eligibility")

if not res:
    st.warning("No Application Found — please submit an application first")
    st.page_link("pages/1_Application.py", label="Go to Application", icon="📝")
else:
    # Main Result Card
    if res.eligible:
        st.success(f"🎉 Congratulations, {res.applicantName}! Your loan application has been APPROVED")
        colA, colB = st.columns(2)
        with colA:
            st.metric("Approved Loan Amount", f"${res.maxLoanAmount:,.0f}")
        with colB:
            st.metric("Interest Rate", f"{res.recommendedRate:.2f}% APR")
    else:
        st.error("❗ Application Not Approved — We have recommendations to help you qualify")

    st.write("AI Confidence Score")
    st.progress(res.score / 100)

    # Application Details
    ui.section_title("Application Details")
    d1, d2, d3, d4 = st.columns(4)
    d1.write(f"Applicant Name: **{res.applicantName}**")
    d2.write(f"Requested Amount: **${res.requestedAmount:,.0f}**")
    d3.write(f"Loan Purpose: **{res.loanPurpose}**")
    d4.write("Application Status: **Approved**" if res.eligible else "Application Status: **Not Approved**")

    # Evaluation Factors
    ui.section_title("Evaluation Factors")
    for f in res.factors:
        if f.status == "positive":
            st.success(f"{f.name} — {f.impact}")
        elif f.status == "negative":
            st.error(f"{f.name} — {f.impact}")
        else:
            st.warning(f"{f.name} — {f.impact}")

    # Next Steps
    ui.section_title("Next Steps")
    if res.eligible:
        st.page_link("pages/3_Calculator.py", label="Calculate EMI", icon="🧮")
        st.page_link("app.py", label="Back to Home", icon="🏠")
    else:
        st.page_link("pages/6_Recommendation.py", label="View Recommendations", icon="🎯")
        st.page_link("pages/5_CreditAssistance.py", label="Credit Assistance", icon="📈")
