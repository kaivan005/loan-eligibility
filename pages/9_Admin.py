import streamlit as st
from pathlib import Path
from lib import ui
from lib.mongo import (
    get_all_eligibility,
    get_eligibility_by_date_range,
    get_all_users,
    get_users_by_date_range,
    get_all_feedback,
    get_feedback_by_date_range,
)
from PIL import Image
import io
from datetime import datetime, time, timedelta
import pandas as pd

image = Image.open("assets/logo.png")
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ Admin", page_icon=byte_im, layout="wide")

css_path = Path(__file__).parent.parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

ui.hide_streamlit_chrome(hide_sidebar=True, hide_header=True)
st.markdown("""
<style>
.block-container { max-width: 100% !important; padding-left: 2rem !important; padding-right: 2rem !important; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("admin_logged_in"):
    st.switch_page("pages/11_Login.py")

nav_links = [
    ("Home", "/"), ("Eligibility", "/Eligibility"), ("Calculator", "/Calculator"),
    ("Credit Help", "/CreditAssistance"), ("About", "/About"), ("Help", "/Help"),
]
ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/Admin")

col_spacer, col_logout = st.columns([10, 1])
with col_logout:
    if st.button("🚪 Logout", key="admin_logout", type="secondary"):
        st.session_state["admin_logged_in"] = False
        st.switch_page("pages/11_Login.py")

st.markdown("""
<div style='background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%); padding: 32px 24px; border-radius: 16px; margin: 24px 0;'>
    <div style='color: white;'>
        <h1 style='font-size: 32px; margin: 0 0 4px;'>⚙️ Admin Dashboard</h1>
        <p style='font-size: 14px; opacity: 0.9; margin: 0;'>System overview and management interface</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

def _clean_eligibility(records):
    rows = []
    for r in records:
        if not isinstance(r, dict):
            continue
        person = r.get("person", {})
        result = r.get("result", {})
        reasons = result.get("rejection_reasons", [])
        rows.append({
            "Name": person.get("fullName", ""),
            "Email": r.get("user_email", person.get("email", "")),
            "Gender": person.get("gender", ""),
            "Marital Status": person.get("married", ""),
            "Income (₹)": (person.get("applicantIncome") or 0) + (person.get("coapplicantIncome") or 0),
            "Loan Amount (₹)": person.get("loanAmount", ""),
            "Loan Term (mo)": person.get("loanAmountTerm", ""),
            "Property Area": person.get("propertyArea", ""),
            "Score": result.get("score", ""),
            "Status": result.get("status", ""),
            "Rejection Reasons": " | ".join(reasons) if reasons else "-",
            "Date": r.get("created_at", ""),
        })
    return pd.DataFrame(rows)

def _clean_users(records):
    rows = []
    for u in records:
        if not isinstance(u, dict): continue
        rows.append({"Full Name": u.get("full_name",""), "Email": u.get("email",""),
                     "Registered At": u.get("created_at",""), "Last Login": u.get("last_login_at","")})
    return pd.DataFrame(rows)

def _clean_feedback(records):
    rows = []
    for f in records:
        if not isinstance(f, dict): continue
        rows.append({"User Name": f.get("user_name",""), "Email": f.get("user_email",""),
                     "Rating": f.get("rating",""), "Message": f.get("message",""),
                     "Submitted At": f.get("created_at","")})
    return pd.DataFrame(rows)

try:
    today = datetime.today().date()
    default_start = today.replace(day=1)

    @st.cache_data(ttl=120)
    def _load_eligibility_reports(start_at: datetime, end_at: datetime, is_all_time: bool):
        if is_all_time:
            return get_all_eligibility()
        return get_eligibility_by_date_range(start_at, end_at)

    @st.cache_data(ttl=120)
    def _load_users_reports(start_at: datetime, end_at: datetime, is_all_time: bool):
        if is_all_time:
            return get_all_users()
        return get_users_by_date_range(start_at, end_at)

    @st.cache_data(ttl=120)
    def _load_feedback_reports(start_at: datetime, end_at: datetime, is_all_time: bool):
        if is_all_time:
            return get_all_feedback()
        return get_feedback_by_date_range(start_at, end_at)

    quick_range = st.session_state.get("admin_quick_range", "This Month")
    from_date = st.session_state.get("admin_from_date", default_start)
    to_date = st.session_state.get("admin_to_date", today)

    if quick_range == "Today":
        from_date = today
        to_date = today
    elif quick_range == "Last 7 Days":
        from_date = today - timedelta(days=6)
        to_date = today
    elif quick_range == "This Month":
        from_date = default_start
        to_date = today

    if from_date > to_date:
        from_date, to_date = to_date, from_date

    start_dt = datetime.combine(from_date, time.min)
    end_dt = datetime.combine(to_date, time.max)

    all_eligibility = _load_eligibility_reports(start_dt, end_dt, quick_range == "All Time")
    all_users = _load_users_reports(start_dt, end_dt, quick_range == "All Time")
    all_feedbacks = _load_feedback_reports(start_dt, end_dt, quick_range == "All Time")

    approved = [r for r in all_eligibility if r.get("result", {}).get("eligible") is True]
    rejected = [r for r in all_eligibility if r.get("result", {}).get("eligible") is False]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #3b82f6, #1e40af); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>📋</div>
                <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>TOTAL CHECKS</div>
                <div style='font-size: 28px; font-weight: bold; margin-top: 8px;'>{len(all_eligibility)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>✅</div>
                <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>APPROVED</div>
                <div style='font-size: 28px; font-weight: bold; margin-top: 8px;'>{len(approved)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>❌</div>
                <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>REJECTED</div>
                <div style='font-size: 28px; font-weight: bold; margin-top: 8px;'>{len(rejected)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>👥</div>
                <div style='font-size: 12px; opacity: 0.9; margin-top: 8px;'>USERS</div>
                <div style='font-size: 28px; font-weight: bold; margin-top: 8px;'>{len(all_users)}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 10px;'>Filter all tables by time range</p>", unsafe_allow_html=True)

    filter_c1, filter_c2, filter_c3 = st.columns([1, 1, 1])
    with filter_c1:
        from_date = st.date_input("From Date", value=from_date, key="admin_from_date")
    with filter_c2:
        to_date = st.date_input("To Date", value=to_date, key="admin_to_date")
    with filter_c3:
        quick_range = st.selectbox(
            "Quick Range",
            ["Custom", "Today", "Last 7 Days", "This Month", "All Time"],
            index=["Custom", "Today", "Last 7 Days", "This Month", "All Time"].index(quick_range),
            key="admin_quick_range",
        )

    if quick_range == "Today":
        from_date = today
        to_date = today
    elif quick_range == "Last 7 Days":
        from_date = today - timedelta(days=6)
        to_date = today
    elif quick_range == "This Month":
        from_date = default_start
        to_date = today

    if from_date > to_date:
        st.warning("From Date cannot be later than To Date. Swapping automatically.")
        from_date, to_date = to_date, from_date

    start_dt = datetime.combine(from_date, time.min)
    end_dt = datetime.combine(to_date, time.max)
    all_eligibility = _load_eligibility_reports(start_dt, end_dt, quick_range == "All Time")
    all_users = _load_users_reports(start_dt, end_dt, quick_range == "All Time")
    all_feedbacks = _load_feedback_reports(start_dt, end_dt, quick_range == "All Time")
    approved = [r for r in all_eligibility if r.get("result", {}).get("eligible") is True]
    rejected = [r for r in all_eligibility if r.get("result", {}).get("eligible") is False]

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #1e293b; margin-top: 0;'>📊 System Data</h2>", unsafe_allow_html=True)

    tab_elig, tab_users, tab_feedback = st.tabs(["📋 Eligibility Checks", "👥 Registered Users", "💬 User Feedback"])

    with tab_elig:
        st.markdown("<p style='color: #6b7280; margin-bottom: 16px;'>All eligibility checks with applicant details, scores, and decisions</p>", unsafe_allow_html=True)
        
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            status_filter = st.selectbox("Filter by status", ["All", "Approved", "Rejected"], key="elig_status")
        with col_filter2:
            st.markdown("")
        
        if status_filter == "Approved":
            display_elig = approved
        elif status_filter == "Rejected":
            display_elig = rejected
        else:
            display_elig = all_eligibility
        
        if display_elig:
            df_elig = _clean_eligibility(display_elig)
            st.dataframe(df_elig, use_container_width=True, height=500)
            period_label = (
                "All Time"
                if quick_range == "All Time"
                else f"{from_date.strftime('%d %b %Y')} to {to_date.strftime('%d %b %Y')}"
            )
            st.caption(
                f"📊 Range: {period_label} | Showing {len(display_elig)} of {len(all_eligibility)} records | "
                f"✅ {len(approved)} approved | ❌ {len(rejected)} rejected"
            )
        else:
            st.info("No eligibility checks found for the selected filter.")

    with tab_users:
        st.markdown(f"<p style='color: #6b7280; margin-bottom: 16px;'>All registered users and their account information</p>", unsafe_allow_html=True)
        
        if all_users:
            df_users = _clean_users(all_users)
            st.dataframe(df_users, use_container_width=True, height=500)
            st.caption(f"📊 Total registered users: {len(all_users)}")
        else:
            st.info("No registered users yet.")

    with tab_feedback:
        st.markdown(f"<p style='color: #6b7280; margin-bottom: 16px;'>All user feedback and ratings</p>", unsafe_allow_html=True)
        
        if all_feedbacks:
            df_feedback = _clean_feedback(all_feedbacks)
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Total Feedback", len(all_feedbacks))
            with col_stat2:
                avg_rating = sum(f.get("rating", 0) for f in all_feedbacks) / len(all_feedbacks)
                st.metric("Average Rating", f"{avg_rating:.1f}/5")
            with col_stat3:
                five_star = sum(1 for f in all_feedbacks if f.get("rating") == 5)
                st.metric("5-Star Ratings", five_star)
            
            st.dataframe(df_feedback, use_container_width=True, height=400)
        else:
            st.info("No feedbacks submitted yet.")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.code(str(e))

ui.footer()

