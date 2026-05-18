import streamlit as st
import pandas as pd
from database import (fetch_all, add_bus, delete_record, verify_admin,
                       get_stats, get_complaints, add_complaint, update_complaint_status)

def show():
    st.markdown("""
    <div class="main-header">
        <div class="badge">⚙️ Administration</div>
        <h1>⚙️ Admin Panel</h1>
        <p>Secure administrative controls for transport management</p>
    </div>
    """, unsafe_allow_html=True)

    # Session auth
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        _login_screen()
    else:
        _admin_dashboard()

def _login_screen():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f1923,#1a2e44);border-radius:16px;
                    padding:2.5rem;border:1px solid rgba(255,140,0,0.3);text-align:center;margin-top:2rem;">
            <div style="font-size:3rem;margin-bottom:0.5rem;">🔐</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:white;margin-bottom:0.3rem;">
                Admin Login
            </div>
            <div style="color:rgba(255,200,100,0.7);font-size:0.85rem;margin-bottom:2rem;">
                Restricted access · Authorized personnel only
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if st.button("🔓 Sign In", use_container_width=True):
            user = verify_admin(username, password)
            if user:
                st.session_state.admin_logged_in = True
                st.session_state.admin_user = user
                st.success(f"Welcome, {user['username']}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Try admin / admin123")

        st.markdown("""
        <div style="text-align:center;color:#94a3b8;font-size:0.78rem;margin-top:1rem;">
            Default credentials: <code>admin</code> / <code>admin123</code>
        </div>
        """, unsafe_allow_html=True)

def _admin_dashboard():
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                background:#f0fdf4;border:1px solid #86efac;border-radius:10px;
                padding:0.8rem 1.2rem;margin-bottom:1.5rem;">
        <span>✅ Signed in as <b>{st.session_state.admin_user['username']}</b> ({st.session_state.admin_user['role']})</span>
    </div>
    """, unsafe_allow_html=True)

    col_logout = st.columns([5, 1])
    with col_logout[1]:
        if st.button("🚪 Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["🚌 Bus Management", "📊 Reports", "📣 Complaints", "🛠️ System"])

    # ── Tab 1: Bus Management ─────────────────────────────────────
    with tab1:
        buses = fetch_all("buses")
        st.subheader("🚌 Fleet Management")

        df = pd.DataFrame(buses)[["bus_number", "model", "capacity", "status", "last_service", "current_route"]]
        df.columns = ["Bus No.", "Model", "Capacity", "Status", "Last Service", "Route"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("➕ Add New Bus")
        with st.form("add_bus_form"):
            c1, c2 = st.columns(2)
            with c1:
                bus_number = st.text_input("Bus Number*", placeholder="BUS-006")
                model = st.text_input("Model*", placeholder="Tata Starbus")
                capacity = st.number_input("Seating Capacity*", min_value=10, max_value=80, value=45)
            with c2:
                status = st.selectbox("Status", ["Active", "Maintenance", "Inactive"])
                last_service = st.date_input("Last Service Date")

            submitted = st.form_submit_button("✅ Register Bus", use_container_width=True)
            if submitted:
                if not all([bus_number, model]):
                    st.error("Fill all required fields.")
                else:
                    try:
                        add_bus({
                            "bus_number": bus_number, "model": model,
                            "capacity": capacity, "status": status,
                            "last_service": str(last_service)
                        })
                        st.success(f"✅ Bus {bus_number} registered!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        st.markdown("---")
        st.subheader("🗑️ Remove Bus")
        bus_to_del = st.selectbox("Select Bus to Remove",
            options=[b["id"] for b in buses],
            format_func=lambda x: next(b["bus_number"] + " – " + b["model"] for b in buses if b["id"] == x))
        if st.button("🗑️ Remove Bus", type="secondary"):
            delete_record("buses", bus_to_del)
            st.success("Bus removed from fleet.")
            st.rerun()

    # ── Tab 2: Reports ────────────────────────────────────────────
    with tab2:
        stats = get_stats()
        st.subheader("📊 System Reports")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["total_buses"]}</div><div class="metric-label">Total Buses</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["total_students"]}</div><div class="metric-label">Total Students</div></div>', unsafe_allow_html=True)
        with c3:
            fee_pct = round(stats["fee_paid"]/stats["total_students"]*100) if stats["total_students"] else 0
            st.markdown(f'<div class="metric-card"><div class="metric-value">{fee_pct}%</div><div class="metric-label">Fee Collection</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("🛣️ Route Utilization")
            routes = fetch_all("routes")
            students = fetch_all("students")
            route_counts = {}
            for s in students:
                rid = s.get("route_id")
                route_counts[rid] = route_counts.get(rid, 0) + 1
            route_data = []
            for r in routes:
                bus_cap = next((b["capacity"] for b in fetch_all("buses") if b["id"] == r.get("bus_id")), 45)
                count = route_counts.get(r["id"], 0)
                route_data.append({
                    "Route": r["route_number"],
                    "Name": r["route_name"],
                    "Students": count,
                    "Capacity": bus_cap,
                    "Utilization": f"{round(count/bus_cap*100)}%" if bus_cap else "N/A"
                })
            st.dataframe(pd.DataFrame(route_data), use_container_width=True, hide_index=True)

        with col_b:
            st.subheader("💰 Fee Collection by Dept.")
            students = fetch_all("students")
            dept_data = {}
            for s in students:
                dept = s["department"]
                if dept not in dept_data:
                    dept_data[dept] = {"total": 0, "paid": 0}
                dept_data[dept]["total"] += 1
                if s["fee_paid"]:
                    dept_data[dept]["paid"] += 1
            fee_df = pd.DataFrame([
                {"Department": k, "Total": v["total"], "Paid": v["paid"],
                 "Pending": v["total"] - v["paid"],
                 "Rate": f"{round(v['paid']/v['total']*100)}%"}
                for k, v in dept_data.items()
            ])
            st.dataframe(fee_df, use_container_width=True, hide_index=True)

        st.subheader("🚗 Driver Summary")
        drivers = fetch_all("drivers")
        drv_df = pd.DataFrame(drivers)[["name", "employee_id", "experience_years", "status", "license_expiry"]]
        drv_df.columns = ["Driver", "ID", "Experience (yrs)", "Status", "License Expiry"]
        st.dataframe(drv_df, use_container_width=True, hide_index=True)

    # ── Tab 3: Complaints ─────────────────────────────────────────
    with tab3:
        st.subheader("📣 Complaint Management")

        complaints = get_complaints()
        students = fetch_all("students")

        col_new, col_list = st.columns([1, 2])
        with col_new:
            st.markdown("**Submit a Complaint**")
            with st.form("complaint_form"):
                stu_id = st.selectbox("Student",
                    options=[s["id"] for s in students],
                    format_func=lambda x: next(s["name"] + " (" + s["roll_number"] + ")" for s in students if s["id"] == x))
                subject = st.text_input("Subject")
                description = st.text_area("Description", height=100)
                sub = st.form_submit_button("📤 Submit")
                if sub:
                    add_complaint({"student_id": stu_id, "subject": subject, "description": description})
                    st.success("Complaint submitted!")
                    st.rerun()

        with col_list:
            st.markdown("**All Complaints**")
            if complaints:
                for c in complaints:
                    s_color = {"Pending": "#ffa500", "Resolved": "#00c864", "In Progress": "#3b82f6"}.get(c["status"], "#94a3b8")
                    new_status = st.selectbox(
                        f"Status – {c['subject'] or 'No subject'} ({c.get('student_name','?')})",
                        ["Pending", "In Progress", "Resolved"],
                        index=["Pending", "In Progress", "Resolved"].index(c["status"]) if c["status"] in ["Pending","In Progress","Resolved"] else 0,
                        key=f"status_{c['id']}"
                    )
                    if new_status != c["status"]:
                        update_complaint_status(c["id"], new_status)
                        st.rerun()
                    st.markdown(f"""
                    <div style="background:#f8fafc;border-radius:8px;padding:0.8rem 1rem;
                                margin-bottom:0.6rem;border-left:3px solid {s_color};font-size:0.85rem;">
                        <b>{c.get('student_name','Unknown')}</b> ({c.get('roll_number','?')})<br>
                        {c.get('description','')}<br>
                        <span style="color:#94a3b8;font-size:0.75rem;">{c['created_at']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No complaints registered.")

    # ── Tab 4: System ─────────────────────────────────────────────
    with tab4:
        st.subheader("🛠️ System Settings")
        st.markdown("""
        <div class="info-box">
            <b>ℹ️ System Information</b><br>
            <b>App:</b> College Transport Management System v1.0<br>
            <b>Database:</b> SQLite (ctms.db)<br>
            <b>Framework:</b> Streamlit + Python<br>
            <b>Map:</b> Folium + OpenStreetMap<br>
            <b>College:</b> Engineering College, Jodhpur, Rajasthan
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🔑 Change Admin Password")
        import hashlib, sqlite3
        with st.form("change_pw_form"):
            old_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")
            change = st.form_submit_button("🔐 Update Password")
            if change:
                if new_pw != confirm_pw:
                    st.error("Passwords don't match.")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    from database import verify_admin, get_connection
                    user = verify_admin(st.session_state.admin_user["username"], old_pw)
                    if user:
                        new_hash = hashlib.sha256(new_pw.encode()).hexdigest()
                        conn = get_connection()
                        conn.execute("UPDATE admin_users SET password_hash=? WHERE username=?",
                                     (new_hash, st.session_state.admin_user["username"]))
                        conn.commit()
                        conn.close()
                        st.success("✅ Password updated successfully!")
                    else:
                        st.error("Current password is incorrect.")

        st.markdown("---")
        st.subheader("🗄️ Database Statistics")
        stats = get_stats()
        for k, v in stats.items():
            st.markdown(f"- **{k.replace('_', ' ').title()}:** {v}")
