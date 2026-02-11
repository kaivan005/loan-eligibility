import streamlit as st
from pathlib import Path
from lib import ui
from lib.mongo import get_all_eligibility
from PIL import Image
import io
from datetime import datetime
import pandas as pd
import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def clean_records(records):
    rows = []

    for r in records:
        if not isinstance(r, dict):
            continue

        person = r.get("person", {})
        result = r.get("result", {})

        rows.append({
            "Name": person.get("fullName"),
            "Email": person.get("email"),
            "Gender": person.get("gender"),
            "Marital Status": person.get("married"),
            "Income": person.get("applicantIncome") + person.get("coapplicantIncome", 0),
            "Loan Amount": person.get("loanAmount"),
            "Loan Duration": person.get("loanAmountTerm"),
            "Property Area": person.get("propertyArea"),
            "Eligiblity Score": result.get("score"),
            "Status": result.get("status"),
            "Date Created": r.get("created_at"),
        })

    return pd.DataFrame(rows)

image = Image.open('assets/logo.png')
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ Admin", page_icon=byte_im, layout="wide")

css_path = Path(__file__).parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

ui.hide_streamlit_chrome(hide_sidebar=True, hide_header=True)
st.markdown("""
<style>
.block-container {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ============ LOGIN PAGE ============
if not st.session_state.get("admin_logged_in"):
    st.switch_page("pages/admin_login.py")

# ============ ADMIN DASHBOARD ============
logo_base64 = get_base64_image("assets/logo.png")
col_nav1, col_nav2 = st.columns([6, 1])

with col_nav1:
    st.markdown(
        f"""
        <div class='navbar'>
            <div class='container navbar-inner'>
                <div class='brand'>
                    <div><img src='data:image/png;base64,{logo_base64}' style='height:40px;'/></div>
                    <div>
                        <div class='brand-title'>LoanIQ</div>
                        <div class='brand-subtitle'>Smart Loan Eligibility System</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_nav2:
    if st.button("Log out", key="navbar_logout"):
        st.session_state["admin_logged_in"] = False
        st.switch_page("pages/admin_login.py")


st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)
# Fetch all records
try:
    @st.cache_data(ttl=300)
    def _get_all_records():
        return get_all_eligibility()
    
    all_records = _get_all_records()
    
    if all_records:
        # Separate approved and rejected
        approved_records = [
        r for r in all_records
        if r.get("result", {}).get("eligible") is True
        ]

        rejected_records = [
            r for r in all_records
            if r.get("result", {}).get("eligible") is False
        ]

        # Stats row
        stat_col1, stat_col2, stat_col3 = st.columns(3)

        with stat_col1:
            st.markdown(f"""
            <div class="admin-card">
                <div class="admin-sub">Total Applications</div>
                <div class="metric-number">{len(all_records)}</div>
            </div>
            """, unsafe_allow_html=True)

        with stat_col2:
            st.markdown(f"""
            <div class="admin-card">
                <div class="admin-sub">Approved</div>
                <div class="metric-number" style="color:#22c55e;">{len(approved_records)}</div>
            </div>
            """, unsafe_allow_html=True)

        with stat_col3:
            st.markdown(f"""
            <div class="admin-card">
                <div class="admin-sub">Rejected</div>
                <div class="metric-number" style="color:#ef4444;">{len(rejected_records)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        # Approved Loans
        st.markdown("#### Approved Loans")
        
        if approved_records:
            st.dataframe(clean_records(approved_records), use_container_width=True, height=400)

            st.markdown(f"**Total Approved:** {len(approved_records)}")
        else:
            st.info("No approved loans yet.")
        
        st.markdown("---")
        
        # Rejected Loans
        st.markdown("#### Rejected/Requires Review Loans")
        
        if rejected_records:
            st.dataframe(clean_records(rejected_records), use_container_width=True, height=400)
            st.markdown(f"**Total Requires Review:** {len(rejected_records)}")
        else:
            st.info("No rejections or pending reviews.")
    
    else:
        st.info("📊 No records found yet.")

except Exception as e:
    st.error(f"❌ Error loading records: {e}")
    st.code(str(e))

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #9ca3af; font-size: 12px; padding: 20px;'>
        <p style='margin: 0;'>LoanIQ Admin Dashboard © 2026</p>
        <p style='margin: 4px 0 0;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
