import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def navbar(cta_href: str, cta_label: str, nav_links: list[tuple[str, str]] | None = None, active_page: str = ""):
    links_markup = ""
    nav_links = nav_links or []
    for label, href in nav_links:
        active_class = " nav-active" if href == active_page else ""
        links_markup += f"<a class='nav-link{active_class}' href='{href}' target='_self'>{label}</a>"
    logo_base64 = get_base64_image("assets/logo.png")

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
            <div class='nav-links'>{links_markup}</div>
            <div>
              <a href='admin_login' class='gradient-button'>Admin Login</a>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hide_streamlit_chrome(hide_sidebar: bool = True, hide_header: bool = True):
    css = "<style>"
    if hide_header:
        css += "header[data-testid='stHeader']{display:none;}"
    if hide_sidebar:
        css += "[data-testid='stSidebar']{display:none;} [data-testid='collapsedControl']{display:none;}"
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)


def hero(title_lines: tuple[str, str], subtitle: str, primary: tuple[str, str], secondary: tuple[str, str]):
    title_1, title_2 = title_lines
    prim_label, prim_href = primary
    sec_label, sec_href = secondary
    st.markdown(
        f"""
        <div class='hero'>
          <div class='badge badge-teal'>⚡ AI-Powered Loan Eligibility System</div>
          <h1 class='section-title'>{title_1}<br/><span style='background:linear-gradient(90deg,#0d9488,#2563eb);-webkit-background-clip:text;background-clip:text;color:transparent;'>{title_2}</span></h1>
          <p class='subtitle'>{subtitle}</p>
          <div class='hero-actions'>
            <a href='{prim_href}' class='gradient-button'>{prim_label}</a>
            <a href='{sec_href}' class='button-outline'>{sec_label}</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(f"<h3 class='section-title'>{text}</h3>", unsafe_allow_html=True)


def cta(title: str, message: str, primary: tuple[str, str], secondary: tuple[str, str]):
    prim_label, prim_href = primary
    sec_label, sec_href = secondary
    st.markdown(
        f"""
        <div class='card' style='text-align:center;background:linear-gradient(90deg,#0d9488,#2563eb);color:white;'>
          <h3 style='margin:0 0 8px;'>{title}</h3>
          <p style='opacity:0.9;'>{message}</p>
          <div style='display:flex;gap:12px;justify-content:center;margin-top:12px;flex-wrap:wrap;'>
            <a href='{prim_href}' class='gradient-button' style='background:white;color:#0d9488;'>{prim_label}</a>
            <a href='{sec_href}' class='gradient-button' style='border:2px solid white;background:transparent;color:white;'>{sec_label}</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        """
        <div class='footer'>
          <div class='container footer-inner'>
            <div class='footer-col'>
              <h4>LoanIQ</h4>
              <p style='margin:4px 0; opacity:0.85;'>Smart, fast, and transparent loan eligibility with personalized guidance.</p>
            </div>
            <div class='footer-col'>
              <h4>Quick Links</h4>
              <a class='footer-link' href='/'>Home</a>
              <a class='footer-link' href='/Application'>Application</a>
              <a class='footer-link' href='/Eligibility'>Eligibility</a>
              <a class='footer-link' href='/Calculator'>Calculator</a>
            </div>
            <div class='footer-col'>
              <h4>Resources</h4>
              <a class='footer-link' href='/CreditAssistance'>Credit Assistance</a>
              <a class='footer-link' href='/Help'>Help Center</a>
              <a class='footer-link' href='/About'>About</a>
            </div>
            <div class='footer-col'>
              <h4>Contact</h4>
              <div class='footer-link'>support@ailoanpro.com</div>
              <div class='footer-link'>+1 (800) 555-0142</div>
              <div class='footer-link'>Mon–Fri, 9am–6pm</div>
            </div>
          </div>
        </div>
        <style>
          .footer { margin-top: 48px; padding: 32px 24px; background: #374151; color: #f3f4f6; }
          .footer-inner { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 24px; align-items: flex-start; }
          .footer-col h4 { margin: 0 0 12px; font-size: 16px; font-weight: 700; color: #ffffff; }
          .footer-link { display: block; color: #d1d5db; text-decoration: none; margin: 6px 0; font-size: 14px; }
          .footer-link:hover { color: #ffffff; text-decoration: underline; }
        </style>
        """,
        unsafe_allow_html=True,
    )
