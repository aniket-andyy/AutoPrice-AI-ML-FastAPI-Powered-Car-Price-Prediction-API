import streamlit as st
import requests
import time
import json

# --- CONFIGURATION ---
API_BASE_URL = "http://127.0.0.1:8000"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

# --- CSS STYLES ---
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Reset & Background */
    * {
        box-sizing: border-box;
    }
    body, .stApp, .glass-card, .sys-card, .meta-item, .dev-card {
        overflow-wrap: normal;
        word-break: normal;
        white-space: normal;
    }
    
    .stApp {
        background: #05050A;
        background-image: radial-gradient(circle at 50% 0%, rgba(0, 242, 254, 0.08) 0%, transparent 50%),
                          radial-gradient(circle at 100% 100%, rgba(176, 102, 254, 0.05) 0%, transparent 50%);
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        overflow-x: hidden;
    }

    /* Hide Streamlit defaults */
    header[data-testid="stHeader"], 
    footer, 
    #MainMenu, 
    .stDeployButton, 
    div[data-testid="stSidebarNav"],
    div[data-testid="collapsedControl"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Glass Card */
    .glass-card {
        background: rgba(20, 25, 40, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: clamp(16px, 4vw, 32px);
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        width: 100%;
        max-width: 100%;
    }

    /* Top Nav */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px clamp(16px, 4vw, 40px);
        background: rgba(15, 20, 35, 0.6);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 24px;
        flex-wrap: wrap;
        gap: 12px;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .nav-logo {
        font-size: clamp(1.2rem, 4vw, 1.5rem);
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .pulse {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-anim 2s infinite;
    }
    @keyframes pulse-anim {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: clamp(40px, 10vw, 100px) clamp(16px, 4vw, 40px);
        max-width: 900px;
        margin: 0 auto;
    }
    .hero h1 {
        font-size: clamp(2.5rem, 8vw, 5rem);
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #00f2fe 50%, #b066fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .hero p {
        font-size: clamp(1rem, 2.5vw, 1.25rem);
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto 24px auto;
        line-height: 1.6;
    }
    .badge-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 12px;
    }
    .badge {
        background: rgba(0, 242, 254, 0.1);
        border: 1px solid rgba(0, 242, 254, 0.3);
        color: #00f2fe;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* Section Headings */
    .section-title {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .section-subtitle {
        color: #94a3b8;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        margin-bottom: 24px;
        line-height: 1.5;
    }
    .content-wrapper {
        max-width: 1100px;
        margin: 0 auto;
        padding: 0 clamp(16px, 4vw, 40px);
    }

    /* Prediction Form Tweaks */
    div[data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    div[data-testid="stForm"] button {
        background: linear-gradient(90deg, #00f2fe, #4facfe) !important;
        color: #05050A !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.3) !important;
        min-height: 54px !important;
        margin-top: 16px !important;
    }
    div[data-testid="stForm"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0, 242, 254, 0.5) !important;
    }
    
    /* Streamlit Input Overrides */
    div[data-baseweb="input"] input, 
    div[data-baseweb="select"] div, 
    .stNumberInput input,
    div[data-baseweb="select"] input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        min-height: 44px !important;
    }
    div[data-baseweb="input"] input:focus, 
    div[data-baseweb="select"] div:focus-within,
    .stNumberInput input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.2) !important;
    }
    label, .st-emotion-cache-16idsys p, div[data-testid="stWidgetLabel"] {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }

    /* Responsive Columns Fix */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0 !important;
        }
        .top-nav {
            justify-content: center;
            text-align: center;
        }
    }

    /* Result Card */
    .result-price {
        font-size: clamp(2.5rem, 10vw, 4.5rem);
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #b066fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 16px 0;
        line-height: 1;
    }
    .result-meta {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 16px;
        margin-top: 24px;
    }
    .meta-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        min-width: 140px;
        flex: 1 1 140px;
        max-width: 250px;
    }
    .meta-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .meta-value {
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    /* System Grid */
    .system-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-top: 24px;
    }
    .sys-card {
        background: rgba(20, 25, 40, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .sys-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.3);
    }
    .sys-icon {
        font-size: 2rem;
        margin-bottom: 12px;
    }
    .sys-title {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .sys-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Code Block */
    .code-container {
        background: #0B0F19;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        overflow-x: auto;
        margin-top: 16px;
    }
    .code-container pre {
        margin: 0;
        color: #00f2fe;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Developer Section */
    .dev-card {
        text-align: center;
        padding: clamp(24px, 5vw, 48px);
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.05), rgba(176, 102, 254, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        margin-bottom: 40px;
    }
    .dev-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00f2fe, #b066fe);
        margin: 0 auto 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: #05050A;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.4);
    }
    .dev-links {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 16px;
        margin-top: 24px;
    }
    .dev-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: #00f2fe;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        min-width: 140px;
        justify-content: center;
    }
    .dev-btn:hover {
        background: rgba(0, 242, 254, 0.1);
        border-color: #00f2fe;
        transform: translateY(-2px);
    }

    /* Footer */
    .glass-footer {
        text-align: center;
        padding: 40px 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 40px;
    }
    .footer-links {
        margin-top: 16px;
    }
    .footer-links a {
        color: #00f2fe;
        text-decoration: none;
        margin: 0 10px;
    }

    /* Error Card */
    .error-card {
        background: rgba(255, 68, 68, 0.05);
        border: 1px solid rgba(255, 68, 68, 0.3);
        text-align: center;
        padding: 24px;
        border-radius: 20px;
        margin-top: 24px;
    }
    .error-card h3 { color: #ff4444; margin-bottom: 12px; }
    .error-card code {
        background: rgba(0,0,0,0.4);
        color: #ff9999;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API HELPERS ---
def check_api_health():
    try:
        res = requests.get(f"{API_BASE_URL}/", timeout=3)
        return res.status_code in [200, 404, 307, 405]
    except Exception:
        return False

def predict_car_price(data):
    start_time = time.time()
    try:
        res = requests.post(PREDICT_ENDPOINT, json=data, timeout=10)
        elapsed = int((time.time() - start_time) * 1000)
        if res.status_code == 200:
            return {"success": True, "data": res.json(), "time": elapsed}
        else:
            return {"success": False, "error": f"HTTP {res.status_code}", "details": res.text, "time": elapsed}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Error", "details": "Cannot reach API. Ensure FastAPI is running.", "time": 0}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout", "details": "The server took too long to respond.", "time": 0}
    except Exception as e:
        return {"success": False, "error": str(e), "details": "An unexpected error occurred.", "time": 0}

# --- RENDER FUNCTIONS ---
def render_header(is_online):
    status_color = "#00ff88" if is_online else "#ff4444"
    status_text = "Online" if is_online else "Offline"
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-logo">AutoPrice AI</div>
        <div class="status-badge" style="background: {status_color}15; border: 1px solid {status_color}40; color: {status_color};">
            <span class="pulse" style="background: {status_color};"></span>
            API {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("""
    <div class="hero">
        <h1>AutoPrice AI</h1>
        <p>ML & FastAPI-Powered Car Price Prediction API. Predict vehicle market prices using a machine learning model exposed through a FastAPI backend.</p>
        <div class="badge-container">
            <span class="badge">● Machine Learning</span>
            <span class="badge">● FastAPI</span>
            <span class="badge">● Prediction API</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_prediction_form():
    st.markdown("""
    <div class="content-wrapper">
        <h2 class="section-title">Predict Your Car's Market Price</h2>
        <p class="section-subtitle">Enter your vehicle details and get an ML-powered price prediction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
        with st.form("prediction_form"):
            c1, c2 = st.columns(2)
            with c1:
                brand = st.text_input("Brand / Make", value="Maruti")
                model = st.text_input("Model", value="Swift")
                year = st.number_input("Year", min_value=1990, max_value=2026, value=2018)
                kms = st.number_input("Kilometers Driven", min_value=0, value=45000, step=1000)
                fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
            with c2:
                trans = st.selectbox("Transmission", ["Manual", "Automatic"])
                engine = st.text_input("Engine / CC", value="1197 CC")
                mileage = st.text_input("Mileage", value="16.0 km/l")
                owner_label = st.selectbox("Number of Owners", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"])
                location = st.text_input("Location", value="Delhi")
                
            st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 24px 0;'>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;'>Additional Market Details (Required by ML Model)</p>", unsafe_allow_html=True)
            
            c3, c4 = st.columns(2)
            with c3:
                present_price = st.number_input("Current Ex-Showroom Price (Lakhs)", min_value=0.0, value=6.5, step=0.1)
            with c4:
                seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
                
            submitted = st.form_submit_button("⚡ Predict Car Price", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    return submitted, brand, model, year, kms, fuel, trans, owner_label, present_price, seller_type

def render_prediction_result(result):
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    if result["success"]:
        pred_price = result["data"].get("prediction_price", result["data"].get("prediction", 0))
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; margin-top: 24px;">
            <h3 style="color: #94a3b8; letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 0; text-transform: uppercase;">Estimated Market Price</h3>
            <div class="result-price">₹ {pred_price:,.2f} Lakhs</div>
            <div class="result-meta">
                <div class="meta-item">
                    <div class="meta-label">Model Used</div>
                    <div class="meta-value">Connected ML Model</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Prediction Status</div>
                    <div class="meta-value" style="color: #00ff88;">Successful</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Response Time</div>
                    <div class="meta-value">{result['time']} ms</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="error-card">
            <h3>⚠️ Unable to connect to AutoPrice API</h3>
            <p style="color: #cbd5e1; margin-bottom: 12px;"><strong>Error:</strong> {result['error']}</p>
            <p style="color: #94a3b8; margin-bottom: 12px;"><strong>API URL:</strong> <code>{PREDICT_ENDPOINT}</code></p>
            <p style="color: #94a3b8;"><strong>Suggested Action:</strong> Make sure FastAPI is running on <code>{API_BASE_URL}</code></p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_overview():
    st.markdown("""
    <div class="content-wrapper" style="margin-top: 60px;">
        <h2 class="section-title">System Overview</h2>
        <div class="system-grid">
            <div class="sys-card">
                <div class="sys-icon">🟢</div>
                <div class="sys-title">API Status</div>
                <div class="sys-value">Online</div>
            </div>
            <div class="sys-card">
                <div class="sys-icon">🧠</div>
                <div class="sys-title">ML Model</div>
                <div class="sys-value">Active</div>
            </div>
            <div class="sys-card">
                <div class="sys-icon">⚡</div>
                <div class="sys-title">Prediction Endpoint</div>
                <div class="sys-value">POST /predict</div>
            </div>
            <div class="sys-card">
                <div class="sys-icon">🚀</div>
                <div class="sys-title">Backend</div>
                <div class="sys-value">FastAPI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_ml_section():
    st.markdown("""
    <div class="content-wrapper" style="margin-top: 60px;">
        <h2 class="section-title">Machine Learning</h2>
        <p class="section-subtitle">AutoPrice AI uses a trained ML model to estimate vehicle prices based on vehicle features.</p>
        <div class="system-grid">
            <div class="sys-card">
                <div class="sys-title">Model</div>
                <div class="sys-value">Connected ML Model</div>
            </div>
            <div class="sys-card">
                <div class="sys-title">Features</div>
                <div class="sys-value">Vehicle Specs</div>
            </div>
            <div class="sys-card">
                <div class="sys-title">Inference</div>
                <div class="sys-value">Real-time</div>
            </div>
            <div class="sys-card">
                <div class="sys-title">API</div>
                <div class="sys-value">REST / JSON</div>
            </div>
            <div class="sys-card">
                <div class="sys-title">Prediction Type</div>
                <div class="sys-value">Regression</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_api_section():
    req_json = {
        "Car_Name": "Maruti Swift",
        "Year": 2018,
        "Present_Price": 6.5,
        "Kms_Driven": 45000,
        "Fuel_Type": "Petrol",
        "Seller_Type": "Dealer",
        "Transmission": "Manual",
        "Owner": 0
    }
    json_str = json.dumps(req_json, indent=4)
    
    st.markdown(f"""
    <div class="content-wrapper" style="margin-top: 60px;">
        <h2 class="section-title">FastAPI Prediction API</h2>
        <p class="section-subtitle">Interact with the prediction endpoint using JSON payloads.</p>
        <div class="glass-card">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;">
                <span style="background: rgba(0, 255, 136, 0.1); color: #00ff88; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-family: monospace;">POST</span>
                <span style="font-family: monospace; font-size: 1.1rem; color: #e2e8f0;">/predict</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;"><strong>API Base URL:</strong> <code style="background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; color: #00f2fe;">{API_BASE_URL}</code></p>
            <div class="code-container">
                <pre>{json_str}</pre>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_developer():
    st.markdown("""
    <div class="content-wrapper" style="margin-top: 60px;">
        <h2 class="section-title" style="text-align: center;">Built by Aniket Sharma</h2>
        <p class="section-subtitle" style="text-align: center;">AI/ML Developer</p>
        <div class="dev-card">
            <div class="dev-avatar">👨‍💻</div>
            <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 500px; margin: 0 auto; line-height: 1.6;">
                Building Machine Learning, Generative AI, Agentic AI, and API-powered applications.
            </p>
            <div class="dev-links">
                <a href="https://www.linkedin.com/in/aniket-sharma-42a700418" target="_blank" class="dev-btn">LinkedIn ↗</a>
                <a href="https://github.com/aniket-andyy" target="_blank" class="dev-btn">GitHub ↗</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="glass-footer">
        <p style="font-size: 1.1rem; color: #e2e8f0; margin-bottom: 8px;"><strong>AutoPrice AI</strong></p>
        <p style="margin-bottom: 16px;">ML & FastAPI-Powered Car Price Prediction API</p>
        <p style="margin-bottom: 16px;">Built with Python • Machine Learning • FastAPI • Streamlit</p>
        <p>Developed by Aniket Sharma</p>
        <div class="footer-links">
            <a href="https://www.linkedin.com/in/aniket-sharma-42a700418" target="_blank">LinkedIn</a> | 
            <a href="https://github.com/aniket-andyy" target="_blank">GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN EXECUTION ---
def main():
    st.set_page_config(
        page_title="AutoPrice AI",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    inject_css()
    
    is_online = check_api_health()
    render_header(is_online)
    render_hero()
    
    submitted, brand, model, year, kms, fuel, trans, owner_label, present_price, seller_type = render_prediction_form()
    
    if submitted:
        owner_val = int(owner_label.split()[0])
        payload = {
            "Car_Name": f"{brand} {model}".strip(),
            "Year": int(year),
            "Present_Price": float(present_price),
            "Kms_Driven": int(kms),
            "Fuel_Type": fuel,
            "Seller_Type": seller_type,
            "Transmission": trans,
            "Owner": owner_val
        }
        with st.spinner("Analyzing vehicle data..."):
            result = predict_car_price(payload)
        render_prediction_result(result)
        
    render_system_overview()
    render_ml_section()
    render_api_section()
    render_developer()
    render_footer()

if __name__ == "__main__":
    main()
