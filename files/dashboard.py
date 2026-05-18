import streamlit as st
import pandas as pd
from database import get_stats, fetch_all

def show():
    st.markdown("""
    <div class="main-header">
        <div class="badge">🎓 Academic Year 2025–26</div>
        <h1>🚌 Transport Management System</h1>
        <p>College of Engineering, Jodhpur · Real-time Fleet Overview</p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_stats()

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['active_buses']}/{stats['total_buses']}</div>
            <div class="metric-label">🚌 Active Buses</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['active_drivers']}/{stats['total_drivers']}</div>
            <div class="metric-label">🚗 Active Drivers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_students']}</div>
            <div class="metric-label">🎓 Enrolled Students</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_routes']}</div>
            <div class="metric-label">🛣️ Active Routes</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("🚌 Fleet Status")
        buses = fetch_all("buses")
        if buses:
            df = pd.DataFrame(buses)[["bus_number", "model", "capacity", "status", "current_route", "last_service"]]
            df.columns = ["Bus No.", "Model", "Capacity", "Status", "Route", "Last Service"]
            def color_status(series):
                return [
                    "color: #00c864; font-weight: 600;" if val == "Active"
                    else "color: #ffa500; font-weight: 600;" if val == "Maintenance"
                    else "color: #dc3232; font-weight: 600;"
                    for val in series
                ]
            st.dataframe(
                df.style.apply(color_status, subset=["Status"], axis=0),
                use_container_width=True, hide_index=True
            )

    with col_right:
        st.subheader("📊 Quick Stats")
        fee_pct = round((stats['fee_paid'] / stats['total_students']) * 100) if stats['total_students'] else 0
        st.markdown(f"""
        <div class="info-box">
            <b>💰 Fee Collection</b><br>
            {stats['fee_paid']}/{stats['total_students']} students paid ({fee_pct}%)
        </div>
        """, unsafe_allow_html=True)

        routes = fetch_all("routes")
        total_dist = sum(r.get("distance_km", 0) or 0 for r in routes)
        st.markdown(f"""
        <div class="info-box">
            <b>📏 Total Route Coverage</b><br>
            {total_dist:.1f} km across {len(routes)} routes
        </div>
        """, unsafe_allow_html=True)

        buses = fetch_all("buses")
        maint = sum(1 for b in buses if b["status"] == "Maintenance")
        if maint:
            st.markdown(f"""
            <div class="danger-box">
                ⚠️ <b>{maint} bus(es)</b> currently under maintenance
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-box">
                ✅ All buses are operational
            </div>
            """, unsafe_allow_html=True)

        st.subheader("⏰ Today's Departure Schedule")
        for r in routes:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.5rem 0.8rem;border-bottom:1px solid rgba(0,0,0,0.06);">
                <span style="font-weight:500;font-size:0.9rem;">{r['route_number']} · {r['start_point']}</span>
                <span style="color:#ffa500;font-weight:700;font-family:'Syne',sans-serif;">{r['departure_time']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Recent Student Enrollments")
    students = fetch_all("students")
    if students:
        df_s = pd.DataFrame(students[-5:][::-1])[["name", "roll_number", "department", "year", "pickup_stop", "fee_paid"]]
        df_s.columns = ["Name", "Roll No.", "Department", "Year", "Pickup Stop", "Fee Paid"]
        df_s["Fee Paid"] = df_s["Fee Paid"].map({1: "✅ Yes", 0: "❌ No"})
        st.dataframe(df_s, use_container_width=True, hide_index=True)
