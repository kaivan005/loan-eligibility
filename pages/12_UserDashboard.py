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

st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 32px 24px; border-radius: 16px; margin-bottom: 32px;'>
    <div style='color: white;'>
        <h1 style='font-size: 32px; margin: 0 0 4px;'>Welcome back, {name}</h1>
        <p style='font-size: 14px; opacity: 0.9; margin: 0;'>Manage your loan applications and track your progress</p>
    </div>
</div>
""".format(name=name), unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #60a5fa, #3b82f6); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
            <div style='font-size: 24px; font-weight: bold;'>📋</div>
            <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>PROFILE</div>
            <div style='font-size: 14px; font-weight: bold; margin-top: 12px;'>{name}</div>
            <div style='font-size: 11px; opacity: 0.8; margin-top: 4px; word-break: break-all;'>{email}</div>
        </div>
    """.format(name=name, email=email), unsafe_allow_html=True)

with col2:
    eligibility_items = get_eligibility_for_user(email)
    checked_count = len(eligibility_items)
    approved_count = sum(1 for e in eligibility_items if e.get("result", {}).get("eligible"))
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
            <div style='font-size: 24px; font-weight: bold;'>✅</div>
            <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>APPLICATIONS</div>
            <div style='font-size: 24px; font-weight: bold; margin-top: 8px;'>{checked_count}</div>
            <div style='font-size: 11px; opacity: 0.8; margin-top: 4px;'>{approved_count} Approved</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if checked_count > 0:
        approval_rate = (approved_count / checked_count) * 100
    else:
        approval_rate = 0
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
            <div style='font-size: 24px; font-weight: bold;'>📊</div>
            <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>APPROVAL RATE</div>
            <div style='font-size: 24px; font-weight: bold; margin-top: 8px;'>{approval_rate:.0f}%</div>
            <div style='font-size: 11px; opacity: 0.8; margin-top: 4px;'>Success Rate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style='border-radius: 12px; background: #f8fafc; padding: 16px; border: 1px solid #e2e8f0;'>
        <h3 style='margin-top: 0; color: #1e293b;'>⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Check Eligibility", use_container_width=True, key="btn_eligibility"):
        st.switch_page("pages/2_Eligibility.py")
    if st.button("🧮 Loan Calculator", use_container_width=True, key="btn_calculator"):
        st.switch_page("pages/3_Calculator.py")
    if st.button("💬 Send Feedback", use_container_width=True, key="btn_feedback"):
        st.switch_page("pages/13_Feedback.py")

with col2:
    st.markdown("""
    <div style='border-radius: 12px; background: #f8fafc; padding: 16px; border: 1px solid #e2e8f0;'>
        <h3 style='margin-top: 0; color: #1e293b;'>🔐 Account</h3>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        logout_user()
        st.switch_page("pages/11_Login.py")

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #1e293b; margin-bottom: 16px;'>📈 Your Eligibility History</h2>", unsafe_allow_html=True)

eligibility_items = get_eligibility_for_user(email)
if not eligibility_items:
    st.info("📭 No eligibility checks yet. Start by checking your eligibility!")
else:
    for i, item in enumerate(eligibility_items[:10]):
        person = item.get("person", {})
        result = item.get("result", {})
        status = result.get("status", "-")
        score = result.get("score", "-")
        loan_amount = person.get("loanAmount", 0) or 0
        rejection_reasons = result.get("rejection_reasons", [])
        created_at = item.get("created_at", "")
        is_eligible = result.get("eligible", False)
        
        status_badge = "✅ APPROVED" if is_eligible else "❌ REJECTED"
        status_bg = "#dcfce7" if is_eligible else "#fee2e2"
        border_color = "#22c55e" if is_eligible else "#ef4444"
        
        reasons_html = ""
        if rejection_reasons:
            reasons_list = " • ".join(rejection_reasons[:3])
            if len(rejection_reasons) > 3:
                reasons_list += f" • +{len(rejection_reasons)-3} more"
            reasons_html = f"""<br/><span style='color: #dc2626; font-size: 12px;'>⚠️ {reasons_list}</span>"""
        
        st.markdown(f"""
        <div style='border-left: 4px solid {border_color}; background: {status_bg}; 
             padding: 16px; margin-bottom: 12px; border-radius: 8px;'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <div>
                    <span style='background: {border_color}; color: white; padding: 4px 12px; border-radius: 4px; 
                          font-size: 12px; font-weight: bold;'>{status_badge}</span>
                    <div style='margin-top: 12px; color: #374151;'>
                        <strong>Loan Amount:</strong> ₹{loan_amount:,.0f} &nbsp;&nbsp; 
                        <strong>Score:</strong> {score}/100{reasons_html}
                    </div>
                    <div style='margin-top: 8px; font-size: 12px; color: #6b7280;'>📅 {created_at}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #1e293b; margin-bottom: 16px;'>💬 Your Recent Feedback</h2>", unsafe_allow_html=True)

feedback_items = get_feedback_for_user(email)
if not feedback_items:
    st.info("📭 No feedback submitted yet. Share your experience!")
else:
    for item in feedback_items[:5]:
        rating = item.get('rating', 0)
        message = item.get('message', '')
        submitted_at = item.get('created_at', '')
        stars = "⭐" * int(rating) if isinstance(rating, (int, float)) else ""
        
        st.markdown(f"""
        <div style='border-radius: 8px; background: #fef3c7; border: 1px solid #fcd34d; 
             padding: 14px; margin-bottom: 10px;'>
            <div style='font-size: 14px; margin-bottom: 6px;'>{stars} {rating}/5 stars</div>
            <div style='color: #374151; margin-bottom: 8px;'>{message}</div>
            <div style='font-size: 12px; color: #6b7280;'>📅 {submitted_at}</div>
        </div>
        """, unsafe_allow_html=True)

ui.footer()
