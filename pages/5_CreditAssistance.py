import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
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


ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/CreditAssistance")

ui.section_title("Credit Score Assistance")
st.caption("Understand, monitor, and improve your credit score with expert guidance")

credit_factors = [
    {"name": "Payment History", "value": 35, "color": "#10b981"},
    {"name": "Credit Utilization", "value": 30, "color": "#3b82f6"},
    {"name": "Credit Age", "value": 15, "color": "#8b5cf6"},
    {"name": "Credit Mix", "value": 10, "color": "#f59e0b"},
    {"name": "New Credit", "value": 10, "color": "#ef4444"},
]

# Initialize session state for custom tabs
if "credit_tab" not in st.session_state:
    st.session_state.credit_tab = 0

# Style the tabs to match navbar
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {
  background: white;
  padding: 4px;
  gap: 4px;
  width: 100%;
  display: flex;
  border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 25px !important;
  padding: 10px 16px !important;
  font-weight: 600;
  font-size: 14px;
  flex: 1;
  border-bottom: none !important;
}


</style>
""", unsafe_allow_html=True)

# Use native Streamlit tabs
tab1, tab2, tab3 = st.tabs(["Understanding Credit", "Improvement Tips", "Score Monitoring"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What is a Credit Score?", anchor=False)
        st.write(
            "In India, your credit score (typically 300-900 from CIBIL/Experian/Equifax/CRIF High Mark) represents how reliably you repay debt. Banks and NBFCs use it to price loans, decide approval, and set credit limits."
        )

    with col2:
        st.subheader("CIBIL Composition (Indicative)", anchor=False)
        fig = go.Figure(data=[go.Pie(labels=[f["name"] for f in credit_factors], values=[f["value"] for f in credit_factors])])
        fig.update_traces(textinfo='label+percent', marker=dict(colors=[f["color"] for f in credit_factors]))
        fig.update_layout(height=320, margin=dict(t=16,b=16,l=16,r=16))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Credit Score Ranges (India)", anchor=False)
    ranges = [
        ("300-549", "Poor", "High risk; approvals unlikely except secured products"),
        ("550-649", "Fair", "Below average; approvals possible with higher rates"),
        ("650-699", "Average", "May get loans/cards but pricing is higher"),
        ("700-749", "Good", "Generally acceptable; competitive offers start here"),
        ("750-799", "Very Good", "Better odds and rates from most banks/NBFCs"),
        ("800-900", "Excellent", "Best rates/limits; strongest eligibility"),
    ]
    for r, rating, desc in ranges:
        st.write(f"- **{r}** — {rating}: {desc}")

with tab2:
    st.subheader("Improvement Tips")
    tips = [
        ("Always pay on time", "Set auto-pay/standing instructions; even 1 DPD (day past due) can hurt CIBIL.", "High Impact"),
        ("Keep utilization under 30%", "Stay well below your card limit (ideally <10%) to avoid score dips.", "High Impact"),
        ("Avoid minimum-due-only", "Pay full statement to prevent revolving interest and risk flags.", "Medium Impact"),
        ("Limit hard inquiries", "Batch applications; too many loan/card pulls in a short span lowers odds.", "Medium Impact"),
        ("Keep oldest accounts", "Age of credit matters—keep long-tenure cards active with small spends.", "Medium Impact"),
        ("Clean up errors & settlements", "Dispute inaccuracies with bureaus; close written-off/settled accounts properly.", "High Impact"),
        ("Diversify sensibly", "A mix of secured (home/auto) and unsecured (card/PL) helps, but avoid over-leverage.", "Low/Medium"),
        ("Monitor jointly held loans", "Co-signed or add-on card delays also impact your score.", "Medium Impact"),
    ]
    for title, desc, impact in tips:
        st.write(f"- **{title}** — {desc} ({impact})")

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Why Monitor Your Score?", anchor=False)
        st.write(
            "Regular monitoring helps you catch errors, track progress, and act before your score drops. In India, "
            "you can check your CIBIL score free once annually via CIBIL's website; paid reports from bureaus are ₹99–₹199."
        )
        st.markdown("**Key monitoring tips:**")
        tips_monitor = [
            "Check score every 30–60 days for early warning signs",
            "Watch for unexpected enquiries or hard pulls",
            "Monitor payment due dates to avoid DPDs",
            "Track credit utilization trends month-on-month",
            "Raise disputes within 30 days of spotting errors",
            "Set calendar reminders for statement reviews",
        ]
        for tip in tips_monitor:
            st.write(f"✓ {tip}")
        
        st.markdown("**Action Plan:**")
        st.write(
            "If your score dips 20+ points, review recent activity. If you find errors, file disputes with the bureau "
            "(CIBIL toll-free: 1800-22-6011). If no errors, focus on on-time payments and reducing utilization over the next 30–60 days."
        )
    
    with col2:
        st.subheader("Projected Score Growth", anchor=False)
        bar = px.bar(
            {"month": ["Month 1","Month 3","Month 6","Month 9","Month 12"], "score": [650,670,695,720,745]}, 
            x="month", 
            y="score"
        )
        bar.update_layout(height=400, yaxis=dict(range=[600,800]), title="Score Improvement Journey")
        st.plotly_chart(bar, use_container_width=True)
        
        st.markdown("**What This Shows:**")
        st.write(
            "By consistently paying on time, keeping utilization low, and avoiding new enquiries, your score can climb "
            "50–100 points in 6–12 months, unlocking better approvals and rates."
        )

ui.footer()
