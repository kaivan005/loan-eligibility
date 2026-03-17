import streamlit as st
from pathlib import Path
from lib import ui
from lib.mongo import get_all_eligibility, get_all_users, get_all_feedback
from PIL import Image
import io
from datetime import datetime
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

_, logout_col = st.columns([10, 1])
with logout_col:
    if st.button("Logout", key="admin_logout"):
        st.session_state["admin_logged_in"] = False
        st.switch_page("pages/11_Login.py")

st.markdown("<br>", unsafe_allow_html=True)
st.title("Admin Dashboard")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

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
    @st.cache_data(ttl=120)
    def _load():
        return get_all_eligibility(), get_all_users(), get_all_feedback()

    all_eligibility, all_users, all_feedbacks = _load()
    approved = [r for r in all_eligibility if r.get("result", {}).get("eligible") is True]
    rejected = [r for r in all_eligibility if r.get("result", {}).get("eligible") is False]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="admin-card"><div class="admin-sub">Total Checks</div>
            <div class="metric-number">{len(all_eligibility)}</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="admin-card"><div class="admin-sub">Approved</div>
            <div class="metric-number" style="color:#22c55e;">{len(approved)}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="admin-card"><div class="admin-sub">Rejected</div>
            <div class="metric-number" style="color:#ef4444;">{len(rejected)}</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="admin-card"><div class="admin-sub">Registered Users</div>
            <div class="metric-number" style="color:#3b82f6;">{len(all_users)}</div></div>""", unsafe_allow_html=True)

    st.divider()

    tab_elig, tab_users, tab_feedback = st.tabs(["📋 Eligibility Checks", "👥 Users", "💬 Feedbacks"])

    with tab_elig:
        st.markdown("#### ✅ Approved Loans")
        if approved:
            st.dataframe(_clean_eligibility(approved), use_container_width=True, height=380)
            st.caption(f"Total approved: {len(approved)}")
        else:
            st.info("No approved loans yet.")
        st.divider()
        st.markdown("#### ❌ Rejected / Requires Review")
        if rejected:
            st.dataframe(_clean_eligibility(rejected), use_container_width=True, height=380)
            st.caption(f"Total rejected: {len(rejected)}")
        else:
            st.info("No rejections yet.")

    with tab_users:
        st.markdown(f"#### Registered Users ({len(all_users)} total)")
        if all_users:
            st.dataframe(_clean_users(all_users), use_container_width=True, height=500)
        else:
            st.info("No registered users yet.")

    with tab_feedback:
        st.markdown(f"#### All User Feedbacks ({len(all_feedbacks)} total)")
        if all_feedbacks:
            st.dataframe(_clean_feedback(all_feedbacks), use_container_width=True, height=500)
            avg = sum(f.get("rating", 0) for f in all_feedbacks) / len(all_feedbacks)
            st.caption(f"Average rating: {avg:.1f} / 5")
        else:
            st.info("No feedbacks submitted yet.")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.code(str(e))

ui.footer()

