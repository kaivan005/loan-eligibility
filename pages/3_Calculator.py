import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
from lib.logic import calculate_emi
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


ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/Calculator")

ui.section_title("Loan EMI Calculator")
st.caption("Calculate your monthly payments and visualize the breakdown")

c1, c2 = st.columns([1,1])

with c1:
    ui.section_title("Loan Details")
    principal = st.number_input("Loan Amount (₹)", value=500000.0, min_value=0.0, step=10000.0, format="%.0f")
    annual_rate = st.number_input("Annual Interest Rate (%)", value=7.5, min_value=0.1, step=0.1)
    years = st.number_input("Loan Term (Years)", value=5.0, min_value=1.0, step=1.0)

    if st.button("Calculate Loan", type="primary", use_container_width=True):
        st.session_state.loan = {
            "loanAmount": principal,
            "interestRate": annual_rate,
            "loanTerm": years,
            **calculate_emi(principal, annual_rate, years)
        }
        st.rerun()

with c2:
    ui.section_title("Loan Summary")
    loan = st.session_state.get("loan")
    if not loan or loan["monthlyPayment"] == 0:
        st.info("Enter loan details and click Calculate to see results")
    else:
        st.metric("Monthly Payment", f"₹{loan['monthlyPayment']:,.0f}")
        st.metric("Total Payment", f"₹{loan['totalPayment']:,.0f}")
        st.metric("Total Interest", f"₹{loan['totalInterest']:,.0f}")

        # Pie chart
        fig = go.Figure(data=[go.Pie(labels=["Principal","Interest"], values=[loan["loanAmount"], loan["totalInterest"]], hole=0)])
        fig.update_traces(textinfo='label+percent')
        fig.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")
        cA, cB = st.columns(2)
        with cA:
            st.write("Total Payments")
            st.write(f"{int(years*12)} months")
        with cB:
            st.write("Interest Rate")
            st.write(f"{annual_rate}% APR")

ui.footer()
