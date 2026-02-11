import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
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

ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/About")

ui.section_title("AI-Based Loan Eligibility & Credit Assistance System")

# Purpose Card
st.markdown("""
<div class='card' style='background: linear-gradient(135deg, #f0fdfa, #eff6ff); border: 2px solid #0d9488; margin-bottom: 32px;'>
  <h2 style='margin-top: 0; color: #0d9488;'>Project Purpose</h2>
  <p style='font-size: 16px; line-height: 1.6; color: #1f2937;'>
  This project aims to demonstrate how artificial intelligence can transform traditional lending processes by providing <strong>instant, data-driven loan eligibility decisions</strong>. By automating the assessment process, we make financial services more accessible, transparent, and efficient for everyone.
  </p>
  <p style='font-size: 16px; line-height: 1.6; color: #1f2937;'>
  The system not only evaluates loan applications but also educates users about credit management and provides actionable recommendations for financial improvement.
  </p>
</div>
""", unsafe_allow_html=True)

# Objectives with checkmarks
st.subheader("Project Objectives")
objectives = [
    "Automate loan eligibility assessment using AI algorithms",
    "Reduce processing time from days to seconds",
    "Provide transparent, data-driven lending decisions",
    "Help applicants understand and improve their eligibility",
    "Demonstrate machine learning in financial services",
    "Create accessible financial tools for everyone",
]

for obj in objectives:
    st.markdown(f"""
    <div class='objective-card'>
      <span class='objective-check'>✓</span>
      <p>{obj}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# Key Features with logos
st.subheader("Key Features")
features = [
    ("⚙️", "AI-Powered Predictions", "Advanced algorithms analyze financial factors to predict eligibility"),
    ("⚡", "Instant Results", "Assessments in under 30 seconds"),
    ("🔐", "Secure & Private", "Data processed securely with best practices"),
    ("💡", "Personalized Recommendations", "Tailored suggestions to improve eligibility"),
    ("📊", "Visual Analytics", "Charts and graphs to understand your profile"),
    ("🎯", "Goal-Oriented Guidance", "Action plans to reach financial goals"),
]

for i in range(0, len(features), 3):
    cols = st.columns(3)
    for idx, (logo, title, desc) in enumerate(features[i:i+3]):
        with cols[idx]:
            st.markdown(f"""
            <div class='feature-card'>
              <div class='feature-icon'>{logo}</div>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# Technology Stack
st.subheader("Technology Stack")
tech_stack = {
    "Backend Framework": ["Streamlit", "Python 3.9+"],
    "Machine Learning": ["Scikit-learn", "Pandas", "NumPy"],
    "Data Processing": ["Feature Engineering", "Data Normalization", "Model Training"],
    "Algorithms": ["Decision Trees", "Random Forest", "Logistic Regression"],
    "Visualization": ["Plotly", "Matplotlib"],
    "Frontend": ["Streamlit Components"],
}

tech_items = list(tech_stack.items())
for i in range(0, len(tech_items), 2):
    cols = st.columns(2)
    for idx, (cat, items) in enumerate(tech_items[i:i+2]):
        with cols[idx]:
            items_html = "".join([f"<li>{item}</li>" for item in items])
            st.markdown(f"""
            <div class='tech-card'>
              <h4>{cat}</h4>
              <ul>
                {items_html}
              </ul>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# AI Methodology - All in One Card
st.subheader("AI Methodology")
methodology = [
    ("1", "Data Collection", "Gather applicant information including personal, employment, and financial details"),
    ("2", "Feature Engineering", "Transform raw data into meaningful features"),
    ("3", "Model Prediction", "Evaluate eligibility based on trained historical data"),
    ("4", "Risk Assessment", "Calculate risk score and determine terms"),
    ("5", "Result Generation", "Provide detailed results and recommendations"),
]

items = []
for num, title, desc in methodology:
    items.append(
        f"""
        <div class='methodology-item'>
          <div class='methodology-badge'>{num}</div>
          <div class='methodology-content'>
            <h4>{title}</h4>
            <p>{desc}</p>
          </div>
        </div>
        """
    )

methodology_block = f"""
<style>
  .methodology-card {{ background: #ffffff; border: 1px solid #e5e7eb; border-left: 4px solid #0d9488; border-radius: 14px; padding: 20px; box-shadow: 0 6px 20px rgba(17,24,39,0.08);font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"; }}
  .methodology-item {{ display: flex; gap: 16px; margin-bottom: 16px; align-items: flex-start; }}
  .methodology-badge {{ background: linear-gradient(90deg, #0d9488, #2563eb); color: white; border-radius: 999px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }}
  .methodology-content h4 {{ margin: 0 0 4px 0; color: #111827; }}
  .methodology-content p {{ margin: 0; color: #4b5563; font-size: 14px; line-height: 1.6; }}
</style>
<div class='methodology-card'>
  {''.join(items)}
</div>
"""

components.html(methodology_block, height=420, scrolling=False)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# Disclaimer - Full Width
st.markdown("""
<div class='card' style='background: linear-gradient(135deg, #fef2f2, #fef3c7); border: 2px solid #dc2626; margin-bottom: 24px;'>
  <div style='display: flex; gap: 16px; align-items: flex-start;'>
    <span style='font-size: 32px;'>⚠️</span>
    <div>
      <h3 style='margin: 0 0 8px 0; color: #991b1b;'>Educational Disclaimer</h3>
      <p style='margin: 0; color: #7c2d12; font-size: 16px; line-height: 1.6;'>
        This is a college project for educational purposes only. Do not use this system for actual financial decisions or loan approvals. The algorithms and recommendations are demonstrations and should not be relied upon for real financial transactions.
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Project Information
st.markdown("""
<div class='card' style='background: linear-gradient(135deg, #f0fdfa, #eff6ff);'>
  <h3 style='margin-top: 0;'>Project Information</h3>
  <p style='margin: 8px 0;'><strong>Category:</strong> AI/ML Project</p>
  <p style='margin: 8px 0;'><strong>Domain:</strong> Financial Technology</p>
  <p style='margin: 8px 0;'><strong>Year:</strong> 2026</p>
  <p style='margin: 12px 0 0 0; font-size: 14px; color: #4b5563; line-height: 1.6;'>Developed as part of academic coursework to demonstrate the application of artificial intelligence and machine learning in solving real-world financial challenges and improving accessibility to financial services.</p>
</div>
""", unsafe_allow_html=True)

ui.footer()
