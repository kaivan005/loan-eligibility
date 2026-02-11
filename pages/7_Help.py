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

ui.navbar(cta_href="/Eligibility", cta_label="Check Eligibility", nav_links=nav_links, active_page="/Help")

ui.section_title("Help & Support Center")
st.caption("Find answers to common questions or reach out to our support team")

# Quick Start Guides - 4 cards in a row
st.subheader("Quick Start Guides")
quick_guides = [
    ("📝", "Complete Your Application", ["Click 'Application' in sidebar", "Fill out all 4 steps", "Review information", "Submit to get results"]),
    ("✅", "Check Eligibility", ["Submit loan application", "Review eligibility score", "Check evaluation factors", "Follow recommendations"]),
    ("🧮", "Calculate Your EMI", ["Open 'Calculator'", "Enter amount, rate, term", "Click 'Calculate Loan'", "Review monthly payment"]),
    ("📈", "Improve Your Credit", ["Visit 'Credit Assistance'", "Learn credit score factors", "Review improvement tips", "Monitor progress"]),
]

for i in range(0, len(quick_guides), 4):
    cols = st.columns(4)
    for idx, (icon, title, steps) in enumerate(quick_guides[i:i+4]):
        with cols[idx]:
            steps_html = "".join([f"<li>{step}</li>" for step in steps])
            st.markdown(f"""
              <div style='font-size: 32px; margin-bottom: 12px; text-align: center;'>{icon}</div>
              <h4 style='margin: 12px 0; color: #0d9488; text-align: center;'>{title}</h4>
              <ul style='text-align: left; font-size: 13px; line-height: 1.6;align-items: center; color: #4b5563; padding-left: 20px;'>
                {steps_html}
              </ul>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# FAQ - Expandable with arrows
st.subheader("Frequently Asked Questions")
faq = [
    ("How do I apply for a loan?", "Go to the Application page and complete the 4-step form. Click 'Submit Application' for instant results."),
    ("What information do I need?", "Personal info, employment details, financial data, and loan preferences."),
    ("How long does it take?", "Instant — processing under 30 seconds with detailed recommendations."),
    ("How is eligibility determined?", "Credit score (40%), income-to-debt (30%), employment stability (20%), request reasonability (10%). 60+ score indicates approval."),
    ("What if I'm not approved?", "View personalized recommendations: maximum eligible amount, improvement areas, alternatives, and a 12-month plan."),
    ("Can I reapply?", "Yes — wait 3–6 months while working on improvement areas."),
]

for q, a in faq:
    with st.expander(f"❓ {q}"):
        st.write(a)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# Contact Cards - 4 cards in a row
st.subheader("Contact Us")
contact_options = [
    ("📧", "Email Support", "contact@loaneligibility.com", "Response within 24 hours"),
    ("☎️", "Call Us", "+91-800-000-0000", "Monday - Friday, 10 AM - 5 PM"),
    ("💬", "Live Chat", "Chat with our support team", "Available 9 AM - 6 PM"),
    ("📍", "Visit Us", "Ahmedabad, India", "Offline Support Center"),
]

cols = st.columns(4)
for idx, (icon, title, desc, detail) in enumerate(contact_options):
    with cols[idx]:
        st.markdown(f"""
          <div style='font-size: 40px; margin-bottom: 12px; align-items: center; display: flex; justify-content: center;'>{icon}</div>
          <h4 style='margin: 12px 0; color: #0d9488; text-align: center;'>{title}</h4>
          <p style='font-weight: 600; color: #1f2937; margin: 8px 0; text-align: center;'>{desc}</p>
          <p style='color: #6b7280; font-size: 13px; text-align: center;'>{detail}</p>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

# Contact Form
st.subheader("Send Us a Message")
with st.form("contact_form"):
    name = st.text_input("Your Name *")    
    email = st.text_input("Email Address *")
    subject = st.selectbox("Subject *", ["General Inquiry","Technical Issue","Application Help","Calculator Question","Credit Assistance","Feedback","Other"],placeholder="Select a subject")
    message = st.text_area("Message *", height=150, placeholder="Tell us how we can help...")
    submitted = st.form_submit_button("Send Message", use_container_width=True)
    
    if submitted:
        if name and email and message:
            st.success("✅ Message submitted successfully! Our team will contact you soon.")
        else:
            st.error("❌ Please fill in all required fields.")

ui.footer()
