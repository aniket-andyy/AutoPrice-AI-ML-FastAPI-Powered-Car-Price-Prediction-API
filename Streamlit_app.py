import streamlit as st
import requests
import time
import json

# =====================================================================
# CONFIGURATION
# =====================================================================
API_BASE_URL = "http://127.0.0.1:8000"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

DEVELOPER_NAME = "Aniket Sharma"
LINKEDIN_URL = "https://www.linkedin.com/in/aniket-sharma-42a700418?utm_source=share_via&utm_content=profile&utm_medium=member_android"
GITHUB_URL = "https://github.com/aniket-andyy"


# =====================================================================
# CSS  (Dark Glassmorphism · Mobile-First · No broken widgets)
# =====================================================================
def inject_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* ---------- Global ---------- */
    *, *::before, *::after { box-sizing: border-box; }
    html, body { overflow-x: hidden; max-width: 100%; }
    body, p, h1, h2, h3, h4, span, div, label, li, code, pre {
        overflow-wrap: normal;
        word-break: normal;
        white-space: normal;
    }
    .stApp {
        background: #05060B;
        background-image:
            radial-gradient(circle at 50% -10%, rgba(0, 194, 255, 0.10) 0%, transparent 55%),
            radial-gradient(circle at 100% 100%, rgba(124, 92, 255, 0.07) 0%, transparent 50%);
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        overflow-x: hidden;
    }

    /* ---------- Hide Streamlit chrome ---------- */
    header[data-testid="stHeader"], footer, #MainMenu, .stDeployButton { display: none !important; }
    section[data-testid="stSidebar"], div[data-testid="collapsedControl"] { display: none !important; }

    /* Main container: real padding so NOTHING touches screen edges */
    .block-container {
        padding-top: 0.75rem !important;
        padding-left: clamp(14px, 4vw, 32px) !important;
        padding-right: clamp(14px, 4vw, 32px) !important;
        padding-bottom: 2rem !important;
        max-width: 1160px !important;
    }

    /* ---------- Glass primitives ---------- */
    .glass-card {
        background: rgba(18, 22, 36, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: clamp(16px, 4vw, 28px);
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        width: 100%;
        max-width: 100%;
    }

    /* ---------- Top navigation ---------- */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        padding: 12px clamp(14px, 3vw, 22px);
        background: rgba(13, 17, 30, 0.72);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        margin-bottom: clamp(20px, 5vw, 40px);
        position: sticky;
        top: 8px;
        z-index: 999;
    }
    .nav-left { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
    .nav-logo {
        font-size: clamp(1.05rem, 4vw, 1.35rem);
        font-weight: 800;
        letter-spacing: -0.3px;
        background: linear-gradient(90deg, #00c2ff, #6ea8ff);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap;
    }
    .nav-dev { font-size: 0.72rem; color: #7C8BA1; white-space: nowrap; }
    .nav-dev a { color: #9FB6D4; text-decoration: none; font-weight: 600; }
    .nav-dev a:hover { color: #00c2ff; }
    .nav-right { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .nav-chip {
        display: inline-flex; align-items: center; justify-content: center;
        width: 30px; height: 30px; border-radius: 9px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #9FB6D4; text-decoration: none;
        font-size: 0.72rem; font-weight: 700;
        transition: all 0.25s ease;
    }
    .nav-chip:hover { background: rgba(0, 194, 255, 0.15); color: #00c2ff; border-color: rgba(0,194,255,0.4); }
    .status-badge {
        display: inline-flex; align-items: center; gap: 7px;
        padding: 6px 12px; border-radius: 50px;
        font-size: 0.78rem; font-weight: 700; white-space: nowrap;
    }
    .pulse { width: 7px; height: 7px; border-radius: 50%; display: inline-block; animation: pulse-anim 2s infinite; }
    @keyframes pulse-anim {
        0%   { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.55); }
        70%  { box-shadow: 0 0 0 8px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }

    /* ---------- Hero ---------- */
    .hero { text-align: center; padding: clamp(28px, 7vw, 80px) 0 clamp(24px, 5vw, 56px); }
    .hero h1 {
        font-size: clamp(2.1rem, 7vw, 4.2rem);
        font-weight: 900; line-height: 1.08; letter-spacing: -1.5px;
        margin: 0 0 14px 0;
        background: linear-gradient(135deg, #ffffff 0%, #7dd6ff 55%, #8f7bff 100%);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        font-size: clamp(0.95rem, 2.4vw, 1.15rem);
        color: #94A3B8; line-height: 1.65;
        max-width: 640px; margin: 0 auto 22px auto;
    }
    .badge-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }
    .badge {
        background: rgba(0, 194, 255, 0.08);
        border: 1px solid rgba(0, 194, 255, 0.28);
        color: #6FD6FF; padding: 6px 14px; border-radius: 50px;
        font-size: 0.78rem; font-weight: 600; white-space: nowrap;
    }

    /* ---------- Section headings ---------- */
    .section-title {
        font-size: clamp(1.4rem, 4.5vw, 2.1rem);
        font-weight: 800; color: #fff; letter-spacing: -0.5px;
        margin: 0 0 6px 0;
    }
    .section-subtitle {
        color: #94A3B8; font-size: clamp(0.88rem, 2.2vw, 1rem);
        line-height: 1.55; margin: 0 0 20px 0;
    }
    .section-gap { margin-top: clamp(36px, 7vw, 72px); }

    /* ---------- FORM = the glass card (real padding, never edge-to-edge) ---------- */
    div[data-testid="stForm"] {
        background: rgba(18, 22, 36, 0.55) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: clamp(16px, 4vw, 28px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    /* ---------- Widget skin: text & number inputs ---------- */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.045) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #F1F5F9 !important;
        min-height: 46px;
        padding: 10px 14px !important;
        font-size: 0.95rem;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: rgba(0, 194, 255, 0.65) !important;
        box-shadow: 0 0 0 3px rgba(0, 194, 255, 0.15) !important;
    }

    /* ---------- Widget skin: selectbox control ---------- */
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.045) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        min-height: 46px;
    }
    div[data-baseweb="select"] > div:hover { border-color: rgba(0, 194, 255, 0.45) !important; }
    div[data-baseweb="select"] div, div[data-baseweb="select"] span { color: #F1F5F9 !important; font-size: 0.95rem; }
    div[data-baseweb="select"] svg { fill: #7C8BA1 !important; }
    ul[role="listbox"] {
        background: #0D1220 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
    }
    ul[role="listbox"] li { color: #E2E8F0 !important; }
    ul[role="listbox"] li:hover { background: rgba(0, 194, 255, 0.12) !important; }

    /* ---------- Neutral dark style for INTERNAL widget buttons
       (number steppers, select toggles) — never gradient ---------- */
    div[data-testid="stNumberInput"] button,
    div[data-baseweb="select"] button,
    div[data-testid="stSelectbox"] button {
        background: rgba(255, 255, 255, 0.07) !important;
        color: #CBD5E1 !important;
        border: none !important;
        box-shadow: none !important;
        width: auto !important;
        min-height: 0 !important;
        padding: 5px 9px !important;
        border-radius: 9px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stNumberInput"] button:hover,
    div[data-baseweb="select"] button:hover { background: rgba(255, 255, 255, 0.14) !important; }

    /* ---------- Labels ---------- */
    .stTextInput label, .stNumberInput label, div[data-testid="stWidgetLabel"] p,
    .stSelectbox label, label { color: #C3CEDD !important; font-weight: 600 !important; font-size: 0.86rem !important; }

    /* ---------- THE CTA (form submit only) ---------- */
    div[data-testid="stFormSubmitContainer"] { margin-top: 8px; }
    div[data-testid="stFormSubmitContainer"] button,
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"],
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #00c2ff 0%, #4f8cff 55%, #7c5cff 100%) !important;
        color: #04101C !important;
        border: none !important;
        border-radius: 14px !important;
        min-height: 52px !important;
        width: 100% !important;
        font-weight: 800 !important;
        font-size: 1.02rem !important;
        letter-spacing: 0.2px;
        box-shadow: 0 8px 24px rgba(0, 194, 255, 0.22) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
    }
    div[data-testid="stFormSubmitContainer"] button p,
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"] p { color: #04101C !important; font-weight: 800 !important; }
    div[data-testid="stFormSubmitContainer"] button:hover {
        transform: translateY(-1px);
        filter: brightness(1.06);
        box-shadow: 0 12px 32px rgba(0, 194, 255, 0.32) !important;
    }

    /* ---------- Responsive: stack Streamlit columns ---------- */
    @media (max-width: 980px) {
        div[data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 0.5rem !important; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"] > .stColumn {
            flex: 1 1 100% !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            padding: 0 !important;
        }
    }
    @media (max-width: 480px) {
        .nav-chip { display: none; }
        .top-nav { padding: 10px 14px; }
        div[data-testid="stForm"] { padding: 16px 14px !important; }
    }

    /* ---------- Result card ---------- */
    .result-card { text-align: center; border-color: rgba(0, 194, 255, 0.28); }
    .result-eyebrow {
        color: #8CA3BF; letter-spacing: 2.5px; font-size: 0.78rem;
        font-weight: 700; text-transform: uppercase; margin: 0 0 6px 0;
    }
    .result-price {
        font-size: clamp(2.4rem, 9vw, 4rem);
        font-weight: 900; line-height: 1.05; margin: 6px 0 2px 0;
        background: linear-gradient(90deg, #00c2ff, #8f7bff);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .result-sub { color: #94A3B8; font-size: clamp(0.9rem, 2.4vw, 1.05rem); font-weight: 600; margin: 0 0 18px 0; }
    .result-meta { display: flex; justify-content: center; flex-wrap: wrap; gap: 12px; }
    .meta-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px; padding: 12px 18px;
        flex: 1 1 150px; max-width: 260px; min-width: 140px;
    }
    .meta-label { font-size: 0.68rem; color: #7C8BA1; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 4px; }
    .meta-value { font-size: 0.95rem; font-weight: 700; color: #E8EEF6; }

    /* ---------- Error card ---------- */
    .error-card {
        background: rgba(255, 82, 82, 0.06);
        border: 1px solid rgba(255, 82, 82, 0.32);
        border-radius: 20px; padding: clamp(18px, 4vw, 28px);
        margin-top: 20px;
    }
    .error-card h3 { color: #FF7B7B; margin: 0 0 10px 0; font-size: clamp(1.05rem, 3vw, 1.3rem); }
    .error-card p { color: #C9D4E3; font-size: 0.92rem; line-height: 1.6; margin: 6px 0; }
    .error-card code {
        background: rgba(0, 0, 0, 0.45); color: #FFB3B3;
        padding: 3px 8px; border-radius: 6px; font-size: 0.82rem;
        word-break: break-all;
    }

    /* ---------- Info grids (system / ml) ---------- */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 14px;
    }
    .info-card {
        background: rgba(18, 22, 36, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 18px;
        transition: transform 0.25s ease, border-color 0.25s ease;
        min-width: 0;
    }
    .info-card:hover { transform: translateY(-3px); border-color: rgba(0, 194, 255, 0.30); }
    .info-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-bottom: 12px; }
    .info-title { font-size: 0.72rem; color: #7C8BA1; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin-bottom: 6px; }
    .info-value { font-size: 1.05rem; font-weight: 700; color: #F1F5F9; }

    /* ---------- API code block ---------- */
    .code-shell {
        background: #0A0E1A;
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px;
        padding: 16px;
        overflow-x: auto;              /* code may scroll, page may not */
        max-width: 100%;
    }
    .code-shell pre {
        margin: 0; color: #9FE4FF;
        font-family: 'SFMono-Regular', Consolas, 'Courier New', monospace;
        font-size: 0.85rem; line-height: 1.6; white-space: pre;
    }
    .method-pill {
        display: inline-block; background: rgba(0, 255, 136, 0.12);
        color: #4ADE80; border: 1px solid rgba(0, 255, 136, 0.30);
        padding: 5px 12px; border-radius: 8px;
        font-weight: 800; font-family: monospace; font-size: 0.85rem;
    }
    .endpoint-path { font-family: monospace; font-size: 1rem; color: #E8EEF6; font-weight: 600; }

    /* ---------- Developer ---------- */
    .dev-card {
        text-align: center;
        background: linear-gradient(135deg, rgba(0, 194, 255, 0.06), rgba(124, 92, 255, 0.06));
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 24px;
        padding: clamp(24px, 5vw, 44px) clamp(16px, 4vw, 32px);
    }
    .dev-avatar {
        width: 76px; height: 76px; border-radius: 50%;
        background: linear-gradient(135deg, #00c2ff, #7c5cff);
        margin: 0 auto 16px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem; font-weight: 900; color: #04101C;
        box-shadow: 0 0 34px rgba(0, 194, 255, 0.35);
    }
    .dev-links { display: flex; justify-content: center; flex-wrap: wrap; gap: 12px; margin-top: 22px; }
    .dev-btn {
        display: inline-flex; align-items: center; justify-content: center; gap: 8px;
        padding: 12px 26px; min-height: 46px; min-width: 150px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 12px; color: #6FD6FF;
        text-decoration: none; font-weight: 700; font-size: 0.92rem;
        transition: all 0.25s ease;
    }
    .dev-btn:hover { background: rgba(0, 194, 255, 0.12); border-color: rgba(0,194,255,0.5); transform: translateY(-2px); }

    /* ---------- Footer ---------- */
    .glass-footer {
        text-align: center; padding: 34px 16px 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: clamp(40px, 7vw, 70px);
        color: #64748B; font-size: 0.82rem; line-height: 1.8;
    }
    .glass-footer strong { color: #E2E8F0; }
    .glass-footer a { color: #6FD6FF; text-decoration: none; }
    .glass-footer a:hover { text-decoration: underline; }
    </style>
    """,
        unsafe_allow_html=True,
    )


# =====================================================================
# API HELPERS
# =====================================================================
@st.cache_data(ttl=30, show_spinner=False)
def check_api_health() -> bool:
    """Ping the FastAPI backend. Never raises."""
    try:
        res = requests.get(f"{API_BASE_URL}/", timeout=4)
        return res.status_code < 500
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    except Exception:
        return False


def predict_car_price(payload: dict) -> dict:
    """POST to /predict with full error handling. Never raises."""
    start = time.time()
    try:
        res = requests.post(PREDICT_ENDPOINT, json=payload, timeout=15)
        elapsed = int((time.time() - start) * 1000)

        if res.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {res.status_code}",
                "details": res.text[:300],
                "time": elapsed,
            }
        try:
            data = res.json()
        except ValueError:
            return {
                "success": False,
                "error": "Invalid JSON",
                "details": "The API responded with non-JSON content.",
                "time": elapsed,
            }
        if not isinstance(data, dict):
            return {
                "success": False,
                "error": "Unexpected response shape",
                "details": str(data)[:200],
                "time": elapsed,
            }
        return {"success": True, "data": data, "time": elapsed}

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "ConnectionError",
            "details": "The server refused the connection.",
            "time": 0,
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Timeout",
            "details": "The server took too long to respond.",
            "time": 0,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "success": False,
            "error": type(exc).__name__,
            "details": str(exc)[:200],
            "time": 0,
        }


def handle_api_error(result: dict) -> None:
    """Render a clean glassmorphic error card instead of crashing."""
    st.markdown(
        f"""
        <div class="error-card">
            <h3>⚠️ Unable to connect to AutoPrice API</h3>
            <p><strong>Error:</strong> {result.get('error', 'Unknown error')}</p>
            <p><strong>Detail:</strong> {result.get('details', '-')}</p>
            <p><strong>API URL:</strong> <code>{PREDICT_ENDPOINT}</code></p>
            <p><strong>Suggested action:</strong> Make sure FastAPI is running on
               <code>{API_BASE_URL}</code> (e.g. <code>uvicorn main:app --reload</code>).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_inr(num: float) -> str:
    """Indian numbering format: 845000 -> 8,45,000"""
    num = int(round(num))
    s = str(num)
    if len(s) <= 3:
        return s
    tail, head = s[-3:], s[:-3]
    parts = []
    while len(head) > 2:
        parts.append(head[-2:])
        head = head[:-2]
    parts.append(head)
    return ",".join(reversed(parts)) + "," + tail


# =====================================================================
# PAGE SECTIONS
# =====================================================================
def render_header(is_online: bool) -> None:
    color = "#4ADE80" if is_online else "#FF7B7B"
    bg = "rgba(74, 222, 128, 0.10)" if is_online else "rgba(255, 123, 123, 0.10)"
    border = "rgba(74, 222, 128, 0.35)" if is_online else "rgba(255, 123, 123, 0.35)"
    label = "API Online" if is_online else "API Offline"
    st.markdown(
        f"""
        <nav class="top-nav">
            <div class="nav-left">
                <div class="nav-logo">AutoPrice AI</div>
                <div class="nav-dev">by <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">{DEVELOPER_NAME}</a></div>
            </div>
            <div class="nav-right">
                <a class="nav-chip" href="{LINKEDIN_URL}" target="_blank" rel="noopener" title="LinkedIn">in</a>
                <a class="nav-chip" href="{GITHUB_URL}" target="_blank" rel="noopener" title="GitHub">GH</a>
                <span class="status-badge" style="background:{bg}; border:1px solid {border}; color:{color};">
                    <span class="pulse" style="background:{color};"></span>{label}
                </span>
            </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <h1>AutoPrice AI</h1>
            <p>ML &amp; FastAPI-Powered Car Price Prediction API. Predict vehicle market
               prices using a machine learning model exposed through a FastAPI backend.</p>
            <div class="badge-container">
                <span class="badge">● Machine Learning</span>
                <span class="badge">● FastAPI</span>
                <span class="badge">● Prediction API</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_form() -> dict:
    st.markdown(
        """
        <h2 class="section-title">Predict Your Car's Market Price</h2>
        <p class="section-subtitle">Enter your vehicle details and get an ML-powered price prediction.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("prediction_form"):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            brand = st.text_input("Brand / Make", value="Maruti")
            model = st.text_input("Model", value="Swift")
            year = st.number_input("Year", min_value=1990, max_value=2026, value=2018, step=1)
            kms = st.number_input("Kilometers Driven", min_value=0, value=45000, step=1000)
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
        with c2:
            trans = st.selectbox("Transmission", ["Manual", "Automatic"])
            engine = st.text_input("Engine / CC", value="1197 CC")
            mileage = st.text_input("Mileage", value="16.0 km/l")
            owner_label = st.selectbox(
                "Number of Owners",
                ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"],
            )
            location = st.text_input("Location", value="Delhi")

        st.markdown(
            "<p style='color:#7C8BA1; font-size:0.82rem; font-weight:600; "
            "margin:18px 0 10px 0;'>ADDITIONAL MARKET DETAILS (REQUIRED BY ML MODEL)</p>",
            unsafe_allow_html=True,
        )
        c3, c4 = st.columns(2, gap="large")
        with c3:
            present_price = st.number_input(
                "Current Ex-Showroom Price (Lakhs)", min_value=0.0, value=6.5, step=0.1
            )
        with c4:
            seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])

        submitted = st.form_submit_button("⚡ Predict Car Price", use_container_width=True)

    return {
        "submitted": submitted,
        "brand": brand,
        "model": model,
        "year": int(year),
        "kms": int(kms),
        "fuel": fuel,
        "trans": trans,
        "engine": engine,
        "mileage": mileage,
        "owner": int(owner_label.split()[0]),
        "location": location,
        "present_price": float(present_price),
        "seller_type": seller_type,
    }


def render_prediction_result(result: dict) -> None:
    if not result["success"]:
        handle_api_error(result)
        return

    data = result.get("data", {})
    price = data.get("prediction_price", data.get("prediction", data.get("predicted_price")))
    if price is None:
        st.markdown(
            """
            <div class="error-card">
                <h3>⚠️ Missing prediction field in API response</h3>
                <p>The API responded, but no <code>prediction_price</code> key was found.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Raw API response"):
            st.json(data)
        return

    price = float(price)
    st.markdown(
        f"""
        <div class="glass-card result-card">
            <p class="result-eyebrow">Estimated Market Price</p>
            <div class="result-price">₹ {price:,.2f} Lakh</div>
            <p class="result-sub">≈ ₹ {format_inr(price * 100000)}</p>
            <div class="result-meta">
                <div class="meta-item">
                    <div class="meta-label">Model Used</div>
                    <div class="meta-value">Connected ML Model</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Prediction Status</div>
                    <div class="meta-value" style="color:#4ADE80;">Successful</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Response Time</div>
                    <div class="meta-value">{result['time']} ms</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_system_overview(is_online: bool) -> None:
    api_state = "Online" if is_online else "Offline"
    api_color = "#4ADE80" if is_online else "#FF7B7B"
    st.markdown(
        f"""
        <div class="section-gap">
            <h2 class="section-title">System Overview</h2>
            <div class="info-grid">
                <div class="info-card">
                    <span class="info-dot" style="background:{api_color}; box-shadow:0 0 10px {api_color};"></span>
                    <div class="info-title">API Status</div>
                    <div class="info-value">{api_state}</div>
                </div>
                <div class="info-card">
                    <span class="info-dot" style="background:#6EA8FF; box-shadow:0 0 10px #6EA8FF;"></span>
                    <div class="info-title">ML Model</div>
                    <div class="info-value">Active</div>
                </div>
                <div class="info-card">
                    <span class="info-dot" style="background:#FFD166; box-shadow:0 0 10px #FFD166;"></span>
                    <div class="info-title">Prediction Endpoint</div>
                    <div class="info-value">POST /predict</div>
                </div>
                <div class="info-card">
                    <span class="info-dot" style="background:#8F7BFF; box-shadow:0 0 10px #8F7BFF;"></span>
                    <div class="info-title">Backend</div>
                    <div class="info-value">FastAPI</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ml_section() -> None:
    st.markdown(
        """
        <div class="section-gap">
            <h2 class="section-title">Machine Learning</h2>
            <p class="section-subtitle">AutoPrice AI uses a trained ML model to estimate vehicle
               prices based on vehicle features sent to the FastAPI inference endpoint.</p>
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-title">Model</div>
                    <div class="info-value">Connected ML Model</div>
                </div>
                <div class="info-card">
                    <div class="info-title">Features</div>
                    <div class="info-value">8 Vehicle Features</div>
                </div>
                <div class="info-card">
                    <div class="info-title">Inference</div>
                    <div class="info-value">Real-time</div>
                </div>
                <div class="info-card">
                    <div class="info-title">API</div>
                    <div class="info-value">REST · JSON</div>
                </div>
                <div class="info-card">
                    <div class="info-title">Prediction Type</div>
                    <div class="info-value">Price Regression</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_api_section() -> None:
    request_example = json.dumps(
        {
            "Car_Name": "swift",
            "Year": 2018,
            "Present_Price": 6.5,
            "Kms_Driven": 45000,
            "Fuel_Type": "Petrol",
            "Seller_Type": "Dealer",
            "Transmission": "Manual",
            "Owner": 0,
        },
        indent=4,
    )
    response_example = json.dumps({"prediction_price": 4.85}, indent=4)
    st.markdown(
        f"""
        <div class="section-gap">
            <h2 class="section-title">FastAPI Prediction API</h2>
            <p class="section-subtitle">The form above sends this exact JSON structure to the backend.</p>
            <div class="glass-card">
                <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:14px;">
                    <span class="method-pill">POST</span>
                    <span class="endpoint-path">/predict</span>
                </div>
                <p style="color:#94A3B8; font-size:0.88rem; margin:0 0 6px 0;">
                    <strong style="color:#C3CEDD;">API Base URL:
