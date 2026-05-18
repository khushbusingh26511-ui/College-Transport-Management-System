import streamlit as st
from database import init_db

st.set_page_config(
    page_title="College Transport Management System",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize DB
init_db()

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .stMetric label { font-family: 'Syne', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f1923 0%, #1a2e44 100%);
    border-right: 1px solid rgba(255,165,0,0.2);
}
[data-testid="stSidebar"] * { color: #e8eaf0 !important; }
[data-testid="stSidebar"] .stRadio label { color: #e8eaf0 !important; }

.main-header {
    background: linear-gradient(135deg, #0f1923 0%, #1a2e44 60%, #0d2137 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,140,0,0.3);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,140,0,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.main-header h1 {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: rgba(255,200,100,0.8);
    margin: 0.3rem 0 0 0;
    font-size: 0.95rem;
}
.badge {
    display: inline-block;
    background: rgba(255,140,0,0.2);
    color: #ffa500;
    border: 1px solid rgba(255,140,0,0.4);
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.metric-card {
    background: linear-gradient(135deg, #0f1923, #1a2e44);
    border: 1px solid rgba(255,140,0,0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(255,140,0,0.5);
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffa500;
    line-height: 1;
}
.metric-label {
    color: rgba(200,210,220,0.7);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

.stButton>button {
    background: linear-gradient(135deg, #ff8c00, #ffa500);
    color: #0f1923;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.3px;
    transition: all 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #ffa500, #ffbe00);
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(255,140,0,0.4);
}

.stDataFrame { border-radius: 10px; overflow: hidden; }

.info-box {
    background: rgba(255,140,0,0.08);
    border: 1px solid rgba(255,140,0,0.25);
    border-left: 4px solid #ffa500;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    color: #e8eaf0;
}
.success-box {
    background: rgba(0,200,100,0.08);
    border: 1px solid rgba(0,200,100,0.25);
    border-left: 4px solid #00c864;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #e8eaf0;
}
.danger-box {
    background: rgba(220,50,50,0.08);
    border: 1px solid rgba(220,50,50,0.25);
    border-left: 4px solid #dc3232;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #e8eaf0;
}

.sidebar-logo {
    text-align: center;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(255,140,0,0.2);
    margin-bottom: 1rem;
}
.sidebar-logo span {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #ffa500 !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stDateInput"] label {
    font-weight: 500;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2.5rem;">🚌</div>
        <span>CTMS</span><br>
        <small style="color:rgba(200,200,200,0.6) !important; font-size:0.7rem;">College Transport Management</small>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🗺️ Bus Tracking", "🛣️ Student Routes", "🚗 Driver Details", "⚙️ Admin Panel"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("<small style='color:rgba(180,180,180,0.5) !important;'>v1.0.0 · Academic Year 2025-26</small>", unsafe_allow_html=True)

# Page routing
if page == "🏠 Dashboard":
    from dashboard import show
    show()
elif page == "🗺️ Bus Tracking":
    from bus_tracking import show
    show()
elif page == "🛣️ Student Routes":
    from student_routes import show
    show()
elif page == "🚗 Driver Details":
    from driver_details import show
    show()
elif page == "⚙️ Admin Panel":
    from admin_panel import show
    show()
