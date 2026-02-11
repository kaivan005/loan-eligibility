import streamlit as st
from pathlib import Path
from lib import ui
from PIL import Image
import io


image = Image.open('assets/logo.png')
buf = io.BytesIO()
image.save(buf, format="PNG")
byte_im = buf.getvalue()
st.set_page_config(page_title="LoanIQ", page_icon=byte_im, layout="wide")

# Inject minimal CSS to approximate gradients and cards
css_path = Path(__file__).parent / "styles" / "theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>",
                unsafe_allow_html=True)
ui.hide_streamlit_chrome()

nav_links = [
    ("Home", "/"),
    ("Eligibility", "/Eligibility"),
    ("Calculator", "/Calculator"),
    ("Credit Help", "/CreditAssistance"),
    ("About", "/About"),
    ("Help", "/Help"),
]

ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility",
          nav_links=nav_links, active_page="/")

ui.hero(
    title_lines=("Check Your Eligibility", "In Seconds"),
    subtitle="Our AI-powered system will instantly assess your loan eligibility. If approved, proceed to submit your application. If not approved, we'll guide you through our document verification and executive review process.",
    primary=("Check Eligibility →", "./pages/2_Eligibility.py"),
    secondary=("Learn More", "./pages/8_About.py"),
)
st.write("")
st.write("")


# Stats Section - Centered
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style='text-align: center;'>
      <div style='font-size: 48px; margin-bottom: 12px;'>🏆</div>
      <div style='font-size: 20px; color: #111827; font-weight: 600; margin-bottom: 8px;'>95% Accuracy</div>
      <p style='color: #6b7280; font-size: 14px; margin: 0;'>AI Prediction Rate</p>
    </div>
    """, unsafe_allow_html=True)
 
with col2:
    st.markdown("""
  <div style='text-align: center;'>
    <div style='font-size: 48px; margin-bottom: 12px;'>⚡</div>
    <div style='font-size: 20px; color: #111827; font-weight: 600; margin-bottom: 8px;'>&lt; 30 Seconds</div>
    <p style='color: #6b7280; font-size: 14px; margin: 0;'>Average Processing Time</p>
  </div>
  """, unsafe_allow_html=True)

with col3:
    st.markdown("""
  <div style='text-align: center;'>
    <div style='font-size: 48px; margin-bottom: 12px;'>🔒</div>
    <div style='font-size: 20px; color: #111827; font-weight: 600; margin-bottom: 8px;'>100% Secure</div>
    <p style='color: #6b7280; font-size: 14px; margin: 0;'>Data Protection</p>
  </div>
  """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)

# Features Section - Centered
st.markdown("""
<div style='text-align: center; margin-bottom: 40px;'>
  <h2 style='font-size: 32px; color: #111827; margin: 0 0 16px;'>Why Choose Our System?</h2>
  <p style='font-size: 18px; color: #4b5563; margin: 0;'>Comprehensive features designed to simplify your loan journey</p>
</div>
""", unsafe_allow_html=True)

features = [
    ("📝", "Easy Application",
     "Simple and intuitive loan application process with step-by-step guidance"),
    ("🧠", "AI-Powered Analysis",
     "Advanced algorithms evaluate your eligibility with high accuracy"),
    ("✅", "Instant Decisions", "Get your loan eligibility results in seconds, not days"),
    ("🧮", "EMI Calculator", "Calculate your monthly payments and plan your finances"),
    ("📈", "Smart Recommendations",
     "Receive personalized loan amount suggestions based on your profile"),
    ("🔐", "Secure & Private",
     "Your data is protected with industry-standard security measures"),
]

for i in range(0, len(features), 3):
    cols = st.columns(3)
    for idx, (emoji, title, desc) in enumerate(features[i:i+3]):
        with cols[idx]:
            st.markdown(f"""
            <div class='card1' style='padding: 32px; text-align: center;'>
              <div style='font-size: 36px; margin-bottom: 16px;'>{emoji}</div>
              <h3 style='color: #0d9488; margin: 12px 0; font-size: 18px;'>{title}</h3>
              <p style='color: #4b5563; font-size: 14px; line-height: 1.6; margin: 0;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)

# How It Works Section
st.markdown(f"""
<div style='background: linear-gradient(135deg, #f3f4f6, #dbeafe, #f0fdfa); border-radius: 24px; padding: 40px;'>
  <div style='text-align: center; margin-bottom: 40px;'>
    <h2 style='font-size: 32px; color: #111827; margin: 0 0 16px;'>How It Works</h2>
    <p style='font-size: 18px; color: #4b5563; margin: 0;'>Simple 4-step process to get your loan eligibility</p>
  </div>
    <div style='display: flex;align-items: center; justify-content: space-between; flex-wrap: wrap;'>
    <div style='text-align: center;'>
      <div style='width: 80px; height: 80px; margin: 0 auto 24px; background: linear-gradient(to bottom right, #14b8a6, #2563eb); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: 700; box-shadow: 0 8px 24px rgba(20, 184, 166, 0.3);'>01</div>
      <h3 style='color: #111827; margin: 0 0 12px; font-size: 18px;'>Fill Application</h3>
      <p style='color: #6b7280; font-size: 14px; margin: 0;'>Provide your personal and financial details</p>
    </div>
    <div style='text-align: center;'>
      <div style='width: 80px; height: 80px; margin: 0 auto 24px; background: linear-gradient(to bottom right, #14b8a6, #2563eb); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: 700; box-shadow: 0 8px 24px rgba(20, 184, 166, 0.3);'>02</div>
      <h3 style='color: #111827; margin: 0 0 12px; font-size: 18px;'>AI Evaluation</h3>
      <p style='color: #6b7280; font-size: 14px; margin: 0;'>Our system analyzes your eligibility</p>
    </div>
    <div style='text-align: center;'>
      <div style='width: 80px; height: 80px; margin: 0 auto 24px; background: linear-gradient(to bottom right, #14b8a6, #2563eb); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: 700; box-shadow: 0 8px 24px rgba(20, 184, 166, 0.3);'>03</div>
      <h3 style='color: #111827; margin: 0 0 12px; font-size: 18px;'>Get Results</h3>
      <p style='color: #6b7280; font-size: 14px; margin: 0;'>Receive instant approval decision</p>
    </div>
    <div style='text-align: center;'>
      <div style='width: 80px; height: 80px; margin: 0 auto 24px; background: linear-gradient(to bottom right, #14b8a6, #2563eb); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: 700; box-shadow: 0 8px 24px rgba(20, 184, 166, 0.3);'>04</div>
      <h3 style='color: #111827; margin: 0 0 12px; font-size: 18px;'>Plan Repayment</h3>
      <p style='color: #6b7280; font-size: 14px; margin: 0;'>Use EMI calculator to plan payments</p>
    </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)

# Quick Navigation Cards - No columns outside cards
st.markdown(f"""
<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin-bottom: 32px;'>
  <div class='card' style='padding: 40px; background: linear-gradient(135deg, #f0fdf4, #dcfce7); border: 2px solid #86efac; text-align: left;'>
    <div style='font-size: 40px; margin-bottom: 10px;'>✅</div>
    <h3 style='color: #111827; margin: 0 0 6px; font-size: 20px;'>Check Eligibility</h3>
    <p style='color: #4b5563; margin: 0 0 12px; font-size: 14px; line-height: 1.6;'>Find out if you qualify for a loan based on your financial profile</p>
    <a href='{"pages/2_Eligibility.py"}' class='button-outline'>Start Eligibility Check</a>
  </div>

          
  <div class='card' style='padding: 40px; background: linear-gradient(135deg, #eff6ff, #dbeafe); border: 2px solid #93c5fd; text-align: left;'>
    <div style='font-size: 40px; margin-bottom: 10px;'>📈</div>
    <h3 style='color: #111827; margin: 0 0 6px; font-size: 20px;'>Credit Assistance</h3>
    <p style='color: #4b5563; margin: 0 0 12px; font-size: 14px; line-height: 1.6;'>Learn how to improve your credit score and increase approval chances</p>
    <a href='{"pages/5_CreditAssistance.py"}' class='button-outline'>Get Credit Help</a>
  </div>
</div>
""", unsafe_allow_html=True)


# Final CTA
st.markdown(f"""
<div style='background: linear-gradient(to right, #14b8a6, #2563eb, #7c3aed); border-radius: 24px; padding: 60px 40px; text-align: center; color: white;'>
  <h2 style='font-size: 32px; color: white; margin: 0 0 16px;'>Ready to Get Started?</h2>
  <p style='font-size: 18px; color: rgba(255, 255, 255, 0.9); margin: 0 0 32px; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;'>
    Take the first step towards your financial goals. Our AI-powered system is here to help you make informed loan decisions.
  </p>
  <div>
    <a href='{"pages/1_Application.py"}' class='button-outline'>Apply Now</a>
    <a href='{"pages/8_About.py"}' class='button-outline'>Learn More</a>
    </div>
</div>
""", unsafe_allow_html=True)

ui.footer()
