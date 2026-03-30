import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
from lib.logic import calculate_emi
from lib import ui
from lib.auth import get_current_user

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

st.markdown(
    """
    <style>
      .calc-hero {
        border: 1px solid #dbeafe;
        border-radius: 16px;
        padding: 18px 20px;
        background: radial-gradient(circle at 10% 10%, #eff6ff 0%, #ecfeff 45%, #ffffff 100%);
        margin-bottom: 18px;
      }
      .calc-hero h2 {
        margin: 0;
        color: #0f172a;
        font-size: 28px;
        text-align: left;
      }
      .calc-hero p {
        margin: 8px 0 0 0;
        color: #475569;
        text-align: left;
      }
      .foir-callout {
        border: 1px solid #bfdbfe;
        background: linear-gradient(135deg, #eff6ff, #f8fafc);
        border-radius: 12px;
        padding: 12px 14px;
        color: #1e3a8a;
        font-size: 13px;
      }
      .status-pill {
        display: inline-block;
        border-radius: 999px;
        padding: 5px 10px;
        font-weight: 600;
        font-size: 12px;
      }
    </style>
    <div class='calc-hero'>
      <h2>EMI + FOIR Planner</h2>
      <p>Estimate your monthly EMI and instantly see whether your obligations stay within a healthy FOIR range.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

current_user = get_current_user() or {}

def _safe_float(value, default):
    try:
        parsed = float(str(value).replace(",", "").strip())
        return parsed if parsed > 0 else default
    except Exception:
        return default

default_income = _safe_float(current_user.get("applicant_income", 0), 500000.0)

left_col, right_col = st.columns([1.05, 0.95], gap="large")

with left_col:
    st.markdown("### Loan Inputs")
    in_c1, in_c2 = st.columns(2)

    with in_c1:
        principal = st.number_input(
            "Loan Amount (Rs)",
            value=st.session_state.get("calc_principal", 1500000.0),
            min_value=10000.0,
            step=50000.0,
            format="%.0f",
        )
        years = st.number_input(
            "Loan Term (Years)",
            value=st.session_state.get("calc_years", 10.0),
            min_value=1.0,
            step=1.0,
        )

    with in_c2:
        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            value=st.session_state.get("calc_rate", 8.75),
            min_value=0.1,
            step=0.1,
        )
        processing_fee_pct = st.number_input(
            "Processing Fee (%)",
            value=st.session_state.get("calc_fee", 0.5),
            min_value=0.0,
            step=0.1,
            help="Optional one-time processing fee estimate.",
        )

    if st.button("Calculate EMI", type="primary", use_container_width=True):
        st.session_state["calc_principal"] = principal
        st.session_state["calc_years"] = years
        st.session_state["calc_rate"] = annual_rate
        st.session_state["calc_fee"] = processing_fee_pct
        st.session_state.loan = {
            "loanAmount": principal,
            "interestRate": annual_rate,
            "loanTerm": years,
            "processingFee": principal * (processing_fee_pct / 100.0),
            **calculate_emi(principal, annual_rate, years),
        }
        st.rerun()

with right_col:
    st.markdown("### Repayment Snapshot")
    loan = st.session_state.get("loan")

    if not loan or loan.get("monthlyPayment", 0) <= 0:
        st.info("Enter loan details and click Calculate EMI to see your repayment summary.")
    else:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Monthly EMI", f"Rs {loan['monthlyPayment']:,.0f}")
        with m2:
            st.metric("Total Interest", f"Rs {loan['totalInterest']:,.0f}")
        with m3:
            st.metric("Total Payment", f"Rs {loan['totalPayment']:,.0f}")

        breakdown = go.Figure(
            data=[
                go.Pie(
                    labels=["Principal", "Interest"],
                    values=[loan["loanAmount"], loan["totalInterest"]],
                    hole=0.55,
                    marker=dict(colors=["#0ea5e9", "#f59e0b"]),
                    textinfo="label+percent",
                )
            ]
        )
        breakdown.update_layout(height=300, margin=dict(t=18, b=8, l=8, r=8), showlegend=False)
        st.plotly_chart(breakdown, use_container_width=True)

        term_months = int(loan["loanTerm"] * 12)
        st.caption(
            f"Term: {term_months} months | APR: {loan['interestRate']}% | Est. Processing Fee: Rs {loan.get('processingFee', 0):,.0f}"
        )

st.markdown("<hr style='margin: 26px 0 22px 0;'>", unsafe_allow_html=True)
st.markdown("### FOIR Affordability Studio")

foir_c1, foir_c2, foir_c3 = st.columns([1, 1, 1])

with foir_c1:
    existing_emi = st.number_input(
        "Existing Monthly Obligations (Rs)",
        value=st.session_state.get("foir_existing", 0.0),
        min_value=0.0,
        step=1000.0,
        format="%.0f",
        help="Include EMI, credit card dues, and other fixed monthly commitments.",
    )

with foir_c2:
    annual_income = st.number_input(
        "Annual Gross Income (Rs)",
        value=st.session_state.get("foir_income", default_income),
        min_value=1.0,
        step=10000.0,
        format="%.0f",
    )

with foir_c3:
    foir_threshold = st.slider(
        "FOIR Threshold (%)",
        min_value=30,
        max_value=90,
        value=int(st.session_state.get("foir_threshold", 60)),
        step=5,
    )

st.session_state["foir_existing"] = existing_emi
st.session_state["foir_income"] = annual_income
st.session_state["foir_threshold"] = foir_threshold

st.markdown(
    """
    <div class='foir-callout'>
      FOIR = (Existing EMI + New Loan EMI) / Monthly Income x 100. Lower FOIR usually means stronger repayment capacity.
    </div>
    """,
    unsafe_allow_html=True,
)

loan = st.session_state.get("loan")
if loan and loan.get("monthlyPayment", 0) > 0:
    monthly_income = annual_income / 12.0
    loan_emi = loan["monthlyPayment"]
    total_emi = existing_emi + loan_emi
    foir_ratio = (total_emi / monthly_income) * 100 if monthly_income > 0 else 0

    max_emi_allowed = (monthly_income * (foir_threshold / 100.0)) - existing_emi
    affordability_buffer = max_emi_allowed - loan_emi

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Monthly Income", f"Rs {monthly_income:,.0f}")
    with s2:
        st.metric("Loan EMI", f"Rs {loan_emi:,.0f}")
    with s3:
        st.metric("Total EMI Outflow", f"Rs {total_emi:,.0f}")
    with s4:
        st.metric("FOIR", f"{foir_ratio:.1f}%")

    st.progress(min(max(foir_ratio / 100.0, 0.0), 1.0))

    status_ok = foir_ratio <= foir_threshold
    status_text = "Healthy" if status_ok else "High Risk"
    status_bg = "#dcfce7" if status_ok else "#fee2e2"
    status_color = "#166534" if status_ok else "#991b1b"

    st.markdown(
        f"""
        <div style='margin-top: 12px; border: 1px solid #e5e7eb; border-radius: 14px; padding: 14px; background: #ffffff;'>
          <div style='display:flex; align-items:center; justify-content:space-between; gap: 10px;'>
            <strong style='color:#0f172a; font-size: 16px;'>FOIR Decision</strong>
            <span class='status-pill' style='background:{status_bg}; color:{status_color};'>{status_text}</span>
          </div>
          <p style='margin:10px 0 6px 0; text-align:left; color:#475569;'>
            Your FOIR is <strong>{foir_ratio:.1f}%</strong> against a threshold of <strong>{foir_threshold}%</strong>.
          </p>
          <p style='margin:0; text-align:left; color:#475569;'>
            Maximum new EMI you can support at this threshold: <strong>Rs {max(max_emi_allowed, 0):,.0f}</strong>.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if status_ok:
        st.success(
            f"Good affordability. You still have an EMI buffer of Rs {max(affordability_buffer, 0):,.0f} before reaching your selected FOIR threshold."
        )
    else:
        overflow = abs(min(affordability_buffer, 0))
        st.error(
            f"FOIR exceeds threshold by {foir_ratio - foir_threshold:.1f}%. Reduce EMI by about Rs {overflow:,.0f} per month, "
            "or increase loan term to improve affordability."
        )
else:
    st.info("Calculate EMI first to unlock FOIR analysis.")

ui.footer()
