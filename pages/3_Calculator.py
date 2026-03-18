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
st.caption("Calculate your monthly payments and assess your debt obligations")

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

st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)

st.markdown("<h3 style='color: #1e293b; margin-bottom: 16px;'>💰 Fixed Obligation to Income Ratio (FOIR) Analysis</h3>", unsafe_allow_html=True)

col_foir1, col_foir2 = st.columns([1, 1])

with col_foir1:
    st.markdown("<p style='color: #6b7280; font-size: 14px;'><strong>Add existing EMI (Optional)</strong></p>", unsafe_allow_html=True)
    
    existing_emi = st.number_input(
        "Your Existing Monthly EMIs & Obligations (₹)",
        value=0.0,
        min_value=0.0,
        step=1000.0,
        format="%.0f",
        help="Total monthly payments for all existing loans and obligations"
    )
    
    annual_income = st.number_input(
        "Your Annual Income (₹)",
        value=500000.0,
        min_value=1.0,
        step=10000.0,
        format="%.0f",
        help="Your annual gross income"
    )
    
with col_foir2:
    st.markdown("<p style='color: #6b7280; font-size: 14px;'><strong>FOIR Threshold Settings</strong></p>", unsafe_allow_html=True)
    
    foir_threshold = st.slider(
        "Maximum acceptable FOIR (%)",
        min_value=30,
        max_value=100,
        value=75,
        step=5,
        help="Default 75% - the maximum % of income that should go towards EMI"
    )
    
    st.markdown(f"""
    <div style='background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 12px; margin-top: 20px;'>
        <p style='margin: 0; font-size: 13px; color: #166534;'>
            <strong>ℹ️ FOIR Explanation</strong><br/>
            FOIR is the percentage of your monthly income that goes towards loan payments. 
            A lower FOIR indicates better loan affordability.
        </p>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.get("loan") and st.session_state.loan.get("monthlyPayment", 0) > 0 and (existing_emi > 0 or annual_income > 0):
    loan = st.session_state.loan
    monthly_income = annual_income / 12
    loan_emi = loan["monthlyPayment"]
    total_emi = existing_emi + loan_emi
    foir_ratio = (total_emi / monthly_income) * 100 if monthly_income > 0 else 0
    
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    
    stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)
    
    with stat_c1:
        st.metric("Monthly Income", f"₹{monthly_income:,.0f}")
    
    with stat_c2:
        st.metric("Loan EMI", f"₹{loan_emi:,.0f}")
    
    with stat_c3:
        st.metric("Existing EMI", f"₹{existing_emi:,.0f}")
    
    with stat_c4:
        total_color = "#22c55e" if foir_ratio <= foir_threshold else "#ef4444"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {total_color}, {total_color}); border-radius: 12px; padding: 16px; color: white; text-align: center;'>
            <div style='font-size: 12px; opacity: 0.9;'>TOTAL MONTHLY EMI</div>
            <div style='font-size: 20px; font-weight: bold; margin-top: 6px;'>₹{total_emi:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    
    foir_color = "#10b981" if foir_ratio <= foir_threshold else "#ef4444"
    foir_status = "✅ Healthy" if foir_ratio <= foir_threshold else "⚠️ High"
    
    st.markdown(f"""
    <div style='border: 2px solid {foir_color}; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, {foir_color}15, {foir_color}08);'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;'>
            <h4 style='margin: 0; color: #1e293b;'>Fixed Obligation to Income Ratio (FOIR)</h4>
            <span style='font-size: 28px; font-weight: bold; color: {foir_color};'>{foir_ratio:.1f}%</span>
        </div>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 12px;'>
            <div>
                <small style='color: #6b7280;'>Your FOIR:</small><br/>
                <strong style='color: {foir_color}; font-size: 20px;'>{foir_ratio:.1f}%</strong>
            </div>
            <div>
                <small style='color: #6b7280;'>Threshold:</small><br/>
                <strong style='color: #3b82f6; font-size: 20px;'>{foir_threshold}%</strong>
            </div>
        </div>
        <div style='padding-top: 12px; border-top: 1px solid {foir_color}40;'>
            <small style='color: #6b7280;'>{foir_status}</small><br/>
            <small style='color: #6b7280;'>You can afford {loan_emi:,.0f}₹ per month towards this loan while maintaining {foir_threshold}% FOIR.</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if foir_ratio > foir_threshold:
        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        st.error(
            f"⚠️ **FOIR Exceeds Threshold!**\n\n"
            f"Your total monthly obligations ({foir_ratio:.1f}%) exceed your acceptable FOIR threshold ({foir_threshold}%). "
            f"This means {foir_ratio - foir_threshold:.1f}% of your income would go beyond your comfort level. "
            f"Consider reducing the loan amount or extending the loan term to lower your monthly EMI."
        )

ui.footer()
