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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Reset & Background */
    .stApp {
        background: linear-gradient(135deg, #05050A 0%, #0B0F19 50%, #111522 100%);
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 20% 20%, rgba(0, 242, 254, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 80% 80%, rgba(176, 102, 254, 0.05) 0%, transparent 40%);
        z-index: -1;
        animation: bg-pan 20s linear infinite;
    }

    @keyframes bg-pan {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Hide default Streamlit chrome */
    header[data-testid="stHeader"] { display: none; }
    #MainMenu { display: none; }
    footer { display: none; }
    .stDeployButton { display: none; }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(20, 25, 40, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.1);
        border: 1px solid rgba(0, 242, 254, 0.2);
    }

    /* Header */
    .glass-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 20, 35, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .gradient-text {
        background: linear-gradient(90deg, #00f2fe, #4facfe, #b066fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }
    .subtitle {
        color: #94a3b8;
        margin: 0;
        font-size: 1rem;
        font-weight: 400;
    }
    .status-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
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

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 20, 35, 0.8);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {
        flex-direction: column;
        gap: 10px;
    }
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        width: 100%;
        transition: all 0.3s ease;
    }
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
        background: rgba(0, 242, 254, 0.1);
        border-color: rgba(0, 242, 254, 0.3);
    }
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label > div:first-child {
        display: none;
    }
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label p {
        color: #e2e8f0 !important;
        font-weight: 500;
        margin: 0;
    }

    /* Inputs */
    div[data-baseweb="input"] input, 
    div[data-baseweb="select"] div, 
    div[data-baseweb="select"] input,
    .stNumberInput input,
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"] input:focus, 
    div[data-baseweb="select"] div:focus-within,
    .stNumberInput input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.2) !important;
    }
    label, .st-emotion-cache-16idsys p {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        color: #05050A !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.5);
    }

    /* Result & Error Cards */
    .result-card {
        text-align: center;
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(176, 102, 254, 0.1));
        border: 1px solid rgba(0, 242, 254, 0.3);
    }
    .price-value {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    .result-meta {
        display: flex;
        justify-content: center;
        gap: 30px;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    .error-card {
        background: rgba(255, 68, 68, 0.05);
        border: 1px solid rgba(255, 68, 68, 0.3);
    }
    .error-card h3 {
        color: #ff4444;
    }
    .error-card code {
        background: rgba(0,0,0,0.3);
        color: #ff9999;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Profile Links */
    .profile-links {
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }
    .glass-btn {
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #00f2fe;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .glass-btn:hover {
        background: rgba(0, 242, 254, 0.1);
        border-color: #00f2fe;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }

    /* Footer */
    .glass-footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748b;
        font-size: 0.85rem;
    }
    .footer-links a {
        color: #00f2fe;
        text-decoration: none;
        margin: 0 10px;
    }
    
    /* Metric Cards Dashboard */
    .metric-card {
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-icon { font-size: 2rem; margin-bottom: 10px; }
    .metric-title { color: #94a3b8; font-size: 0.9rem; margin-bottom: 5px; }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #fff; }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API HELPERS ---
def check_api_health():
    try:
        requests.get(f"{API_BASE_URL}/", timeout=3)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return True

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
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px; padding-top: 20px;">
            <div class="gradient-text" style="font-size: 1.8rem;">AutoPrice AI</div>
            <p style="color: #64748b; font-size: 0.8rem; margin-top: 5px;">v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "🚗 Predict Price", "⚡ API Explorer", "🤖 ML Model", "👨‍💻 Developer"],
            label_visibility="collapsed"
        )
        
        if "Dashboard" in page: st.session_state["page"] = "Dashboard"
        elif "Predict" in page: st.session_state["page"] = "Predict Price"
        elif "API" in page: st.session_state["page"] = "API"
        elif "ML" in page: st.session_state["page"] = "ML Model"
        elif "Developer" in page: st.session_state["page"] = "Developer"
        
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 40px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem;">
            Developed by<br>
            <strong style="color: #e2e8f0; font-size: 1rem;">Aniket Sharma</strong>
        </div>
        """, unsafe_allow_html=True)

def render_header(is_online):
    status_color = "#00ff88" if is_online else "#ff4444"
    status_text = "Online" if is_online else "Offline"
    pulse_color = "rgba(0, 255, 136, 0.7)" if is_online else "rgba(255, 68, 68, 0.7)"
    
    st.markdown(f"""
    <div class="glass-header">
        <div>
            <h1 class="gradient-text">AutoPrice AI</h1>
            <p class="subtitle">ML & FastAPI-Powered Car Price Prediction API</p>
        </div>
        <div class="status-badge" style="background: {status_color}20; border: 1px solid {status_color}50; color: {status_color};">
            <span class="pulse" style="background: {status_color}; box-shadow: 0 0 0 0 {pulse_color};"></span>
            API {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    st.markdown("<h2 style='margin-bottom: 20px;'>System Overview</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("API Status", "Online", "🟢"),
        ("ML Model", "Active", "🧠"),
        ("Prediction API", "POST /predict", "⚡"),
        ("Backend", "FastAPI", "🚀")
    ]
    for col, (title, value, icon) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""
            <div class="glass-card metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

def render_prediction():
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 24px;">
        <h2 style="margin-top:0;">Predict Your Car's Market Price</h2>
        <p style="color: #94a3b8; margin-bottom: 0;">Enter vehicle specifications and let the machine learning model estimate its market value.</p>
    </div>
    """, unsafe_allow_html=True)
    
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
            owner = st.selectbox("Number of Owners", [0, 1, 3])
            location = st.text_input("Location", value="Delhi")
            
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Additional Market Details (Required by ML Model):</p>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            present_price = st.number_input("Current Ex-Showroom Price (Lakhs)", min_value=0.0, value=6.5, step=0.1)
        with c4:
            seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
            
        submitted = st.form_submit_button("⚡ Predict Price", use_container_width=True)
        
    if submitted:
        with st.spinner("Analyzing vehicle data..."):
            car_name = f"{brand} {model}".strip()
            payload = {
                "Car_Name": car_name,
                "Year": int(year),
                "Present_Price": float(present_price),
                "Kms_Driven": int(kms),
                "Fuel_Type": fuel,
                "Seller_Type": seller_type,
                "Transmission": trans,
                "Owner": int(owner)
            }
            result = predict_car_price(payload)
            
        if result["success"]:
            pred_price = result["data"].get("prediction_price", result["data"].get("prediction", 0))
            st.markdown(f"""
            <div class="glass-card result-card">
                <h3 style="color: #94a3b8; letter-spacing: 1px;">ESTIMATED MARKET PRICE</h3>
                <div class="price-value">₹ {pred_price:,.2f} Lakhs</div>
                <div class="result-meta">
                    <span>Model: Random Forest</span>
                    <span>Response Time: {result['time']} ms</span>
                    <span>Status: Prediction Successful</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="glass-card error-card">
                <h3>⚠️ Unable to connect to AutoPrice API</h3>
                <p><strong>Error:</strong> {result['error']}</p>
                <p><strong>API URL:</strong> <code>{PREDICT_ENDPOINT}</code></p>
                <p><strong>Suggested Action:</strong> Make sure FastAPI is running on <code>{API_BASE_URL}</code></p>
            </div>
            """, unsafe_allow_html=True)

def render_api_page():
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top:0;">FastAPI Prediction Endpoint</h2>
        <p style="color: #00f2fe; font-family: monospace; font-size: 1.1rem;">POST /predict</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### API Base URL")
        st.code(API_BASE_URL, language="text")
    with c2:
        st.markdown("### Content Type")
        st.code("application/json", language="text")
    
    st.markdown("### Example Request Payload")
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
    st.code(json.dumps(req_json, indent=4), language="json")
    
    st.markdown("### Example Response")
    res_json = {
        "prediction_price": 4.85
    }
    st.code(json.dumps(res_json, indent=4), language="json")

def render_model_page():
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top:0;">Machine Learning Architecture</h2>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #00f2fe;">Model Type</h4>
            <p>Random Forest Regressor</p>
            <hr style="border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="color: #00f2fe;">Prediction Type</h4>
            <p>Supervised Regression</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #00f2fe;">Backend Framework</h4>
            <p>FastAPI (Python)</p>
            <hr style="border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="color: #00f2fe;">Inference API</h4>
            <p>RESTful JSON Endpoint</p>
        </div>
        """, unsafe_allow_html=True)

def render_developer_page():
    st.markdown("""
    <div class="glass-card profile-card" style="text-align: center; max-width: 600px; margin: 0 auto;">
        <div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #00f2fe, #b066fe); margin: 0 auto 20px auto; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;">
            👨‍💻
        </div>
        <h2 style="margin-top:0;">Aniket Sharma</h2>
        <h4 style="color: #94a3b8; font-weight: 500;">AI/ML Developer</h4>
        <p style="color: #cbd5e1; margin-top: 20px;">Building Machine Learning, Generative AI, Agentic AI, and API-powered applications.</p>
        <div class="profile-links" style="justify-content: center;">
            <a href="https://www.linkedin.com/in/aniket-sharma-42a700418" target="_blank" class="glass-btn">LinkedIn ↗</a>
            <a href="https://github.com/aniket-andyy" target="_blank" class="glass-btn">GitHub ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="glass-footer">
        <p><strong style="color: #e2e8f0;">AutoPrice AI</strong> • ML & FastAPI-Powered Car Price Prediction API</p>
        <p>Built with Python • Machine Learning • FastAPI • Streamlit</p>
        <p>Developed by Aniket Sharma</p>
        <div class="footer-links" style="margin-top: 15px;">
            <a href="https://www.linkedin.com/in/aniket-sharma-42a700418" target="_blank">LinkedIn</a> | 
            <a href="https://github.com/aniket-andyy" target="_blank">GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN EXECUTION ---
def main():
    st.set_page_config(page_title="AutoPrice AI", layout="wide", page_icon="🚗")
    inject_css()
    
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
        
    render_sidebar()
    
    is_online = check_api_health()
    render_header(is_online)
    
    page = st.session_state.page
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Predict Price":
        render_prediction()
    elif page == "API":
        render_api_page()
    elif page == "ML Model":
        render_model_page()
    elif page == "Developer":
        render_developer_page()
        
    render_footer()

if __name__ == "__main__":
    main()
