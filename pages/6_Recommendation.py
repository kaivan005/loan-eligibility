import streamlit as st
from lib import ui
from pathlib import Path

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


ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/Recommendation")

st.title("Personalized Loan Recommendations")
st.caption("Tailored suggestions to help you qualify for your desired loan amount")

res = st.session_state.get("eligibility")
if not res:
    st.info("No result found. Submit an application or run the eligibility checker.")
    st.stop()

recommended_amount = int(res.requestedAmount * 0.6) if not res.eligible else int(res.maxLoanAmount)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Current Status")
    st.write(f"Eligibility Score: **{res.score}/100**")
    st.write(f"Requested Amount: **${res.requestedAmount:,.0f}**")
    st.error("Status: Not Approved" if not res.eligible else "Status: Approved")
with c2:
    st.subheader("Recommended Goal")
    st.write("Target Score: **70+/100**")
    st.write(f"Achievable Amount: **${recommended_amount:,.0f}**")
    st.write("Timeline: **6-12 months**")

st.subheader("Maximum Eligible Loan Amount")
st.info(f"Based on your current profile, aim for ${recommended_amount:,.0f}. Work towards ${res.requestedAmount:,.0f} by following our recommendations.")

st.subheader("Key Areas for Improvement")
improvement_areas = [
    ("Improve Credit Score", "Fair (580-669)", "Good (670-739)", 45, "6-12 months", [
        "Pay all bills on time for the next 6 months",
        "Reduce credit card utilization to below 30%",
        "Dispute any errors on credit reports",
        "Avoid opening new credit accounts",
    ], "High"),
    ("Increase Income", "Current income level", "+20% income increase", 60, "3-6 months", [
        "Negotiate salary raise with current employer",
        "Take on additional part-time work",
        "Develop skills for higher-paying position",
        "Consider side business or freelancing",
    ], "High"),
    ("Stabilize Employment", "Less than 2 years", "2+ years continuous", 75, "6-12 months", [
        "Maintain current employment position",
        "Build strong work performance record",
        "Obtain employment verification letter",
        "Avoid job changes during this period",
    ], "Medium"),
    ("Reduce Debt-to-Income Ratio", "45% DTI", "Below 36% DTI", 50, "3-6 months", [
        "Pay down existing loan balances",
        "Consolidate high-interest debts",
        "Reduce monthly expenses by 15-20%",
        "Create and stick to monthly budget",
    ], "High"),
]

for title, current, target, progress, timeline, actions, impact in improvement_areas:
    st.markdown(f"#### {title}")
    st.write(f"{current} → {target}")
    st.progress(progress / 100)
    st.caption(f"Timeline: {timeline} — Impact: {impact}")
    for a in actions:
        st.write(f"- {a}")
    st.write("")

st.subheader("Alternative Loan Options")
options = [
    ("Secured Loan", "$15,000 - $30,000", "4.5% - 7.5%", "Use collateral like property or vehicle to secure loan"),
    ("Co-signed Loan", "$20,000 - $50,000", "5.0% - 9.0%", "Add a co-signer with strong credit to your application"),
    ("Smaller Personal Loan", f"Up to ${recommended_amount:,.0f}", "8.0% - 12.0%", "Start with a smaller amount you can qualify for now"),
]
for t, amt, rate, desc in options:
    st.write(f"**{t}** — Amount: {amt} — Rate: {rate}")
    st.write(desc)

st.subheader("Next Steps")
st.page_link("pages/5_CreditAssistance.py", label="Credit Assistance", icon="📈")
st.page_link("pages/3_Calculator.py", label="Calculate Target EMI", icon="🧮")
st.page_link("pages/1_Application.py", label="New Application", icon="📝")

ui.footer()
