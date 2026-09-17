import streamlit as st
import requests

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AutoPrice AI",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed" # Collapsed sidebar for a cleaner front-page focus
)

# -----------------------------------------------------------------------------
# Custom CSS for Modern UI
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main Header Styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* Developer Info Styling */
    .developer-section {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 1rem;
        background-color: #F8FAFC;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
    .developer-name {
        font-size: 1.1rem;
        color: #334155;
        margin-bottom: 0.8rem;
    }
    .developer-name strong {
        color: #0F172A;
        font-weight: 700;
    }
    .dev-links {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
    }
    .dev-link {
        text-decoration: none;
        color: #475569;
        font-weight: 600;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        transition: all 0.2s ease;
    }
    .dev-link:hover {
        background-color: #EFF6FF;
        border-color: #3B82F6;
        color: #2563EB;
        transform: translateY(-1px);
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 10px;
        padding: 0.8rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.3);
    }
    
    /* Prediction Box Styling */
    .prediction-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #86EFAC;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .prediction-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #15803D;
        margin-top: 0.5rem;
    }
    
    /* Form Input Styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #CBD5E1;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Content
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">AutoPrice AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">ML and FastAPI Powered Car Price Prediction API</div>', unsafe_allow_html=True)

# Developer Info Section (Front Page, Below Project Name)
st.markdown("""
<div class="developer-section">
    <div class="developer-name">Developed by <strong>Aniket Sharma</strong></div>
    <div class="dev-links">
        <a href="https://www.linkedin.com/in/aniket-sharma-42a700418?utm_source=share_via&utm_content=profile&utm_medium=member_android" target="_blank" class="dev-link">
            💼 LinkedIn
        </a>
        <a href="https://github.com/aniket-andyy" target="_blank" class="dev-link">
            🐙 GitHub
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "https://car-prediction-lpfl.onrender.com/predict"

# -----------------------------------------------------------------------------
# Input Form
# -----------------------------------------------------------------------------
with st.form("prediction_form", clear_on_submit=False):
    st.markdown("#### 📋 Vehicle Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        car_name = st.text_input("Car Name", value="ritz", help="e.g., swift, ritz, sx4")
        year = st.number_input("Year", min_value=1990, max_value=2026, value=2014, step=1)
        present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, value=5.59, step=0.1)
    
    with col2:
        kms_driven = st.number_input("Kms Driven", min_value=0, value=27000, step=1000)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
        seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
        
    col3, col4 = st.columns(2)
    with col3:
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    with col4:
        owner_label = st.selectbox("Owner", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"])
        owner = int(owner_label.split()[0])
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button("🔮 Predict Price")

# -----------------------------------------------------------------------------
# Prediction Logic
# -----------------------------------------------------------------------------
if submit_button:
    # NOTE: Keys exactly match the CarFeatures Pydantic model in schema.py (no trailing spaces)
    payload = {
        "Car_Name": str(car_name).strip(),
        "Year": int(year),
        "Present_Price": float(present_price),
        "Kms_Driven": int(kms_driven),
        "Fuel_Type": str(fuel_type),
        "Seller_Type": str(seller_type),
        "Transmission": str(transmission),
        "Owner": int(owner),
    }
    
    with st.spinner("🤖 Analyzing vehicle data and calculating prediction..."):
        try:
            res = requests.post(API_URL, json=payload, timeout=20)
            
            if res.status_code == 200:
                data = res.json()
                # Matches the PredictionResponse model in schema.py
                pred = data.get("prediction_price")
                
                if pred is not None:
                    st.markdown(f"""
                    <div class="prediction-box">
                        <div style="font-size: 1.1rem; color: #15803D; font-weight: 600;">✅ Predicted Selling Price</div>
                        <div class="prediction-value">₹ {pred:.2f} Lakhs</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ API responded but prediction key not found.")
                    with st.expander("🔍 View Full API Response"):
                        st.json(data)
            else:
                st.error(f"❌ API Error {res.status_code}")
                with st.expander("🔍 View Error Details"):
                    st.code(res.text)
                    
        except requests.exceptions.RequestException as e:
            st.error("❌ Could not connect to the prediction API. Please ensure the FastAPI backend is running.")
            with st.expander("🔍 View Connection Error"):
                st.code(str(e))
                
    # Payload Expander for debugging
    with st.expander("🛠️ View JSON Payload Sent to API"):
        st.json(payload)
