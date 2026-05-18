import streamlit as st
import pandas as pd
from datetime import date, datetime
from database import fetch_all, add_driver, update_driver, delete_record

def show():
    st.markdown("""
    <div class="main-header">
        <div class="badge">🚗 Driver Management</div>
        <h1>🚗 Driver Details</h1>
        <p>Manage driver profiles, assignments and license records</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["👥 Driver Directory", "➕ Add Driver", "✏️ Edit / Remove"])

    drivers = fetch_all("drivers")
    buses = fetch_all("buses")
    routes = fetch_all("routes")
    bus_map = {b["id"]: b["bus_number"] for b in buses}
    route_map = {r["id"]: r["route_name"] for r in routes}

    # ── Tab 1 ─────────────────────────────────────────────────────
    with tab1:
        # Summary cards
        active = sum(1 for d in drivers if d["status"] == "Active")
        on_leave = sum(1 for d in drivers if d["status"] == "On Leave")
        today = date.today()
        expiring_soon = sum(1 for d in drivers if d.get("license_expiry") and
                            (datetime.strptime(d["license_expiry"], "%Y-%m-%d").date() - today).days <= 180)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{active}</div><div class="metric-label">Active Drivers</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{on_leave}</div><div class="metric-label">On Leave</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{expiring_soon}</div><div class="metric-label">License Expiring Soon</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if expiring_soon:
            st.markdown(f'<div class="danger-box">⚠️ <b>{expiring_soon} driver(s)</b> have licenses expiring within 6 months. Please renew promptly.</div>', unsafe_allow_html=True)

        # Driver cards
        cols = st.columns(2)
        for i, d in enumerate(drivers):
            with cols[i % 2]:
                status_color = {"Active": "#00c864", "On Leave": "#ffa500", "Inactive": "#dc3232"}.get(d["status"], "#94a3b8")
                bus = bus_map.get(d["assigned_bus"], "Unassigned")
                route = route_map.get(d["assigned_route"], "Unassigned")

                exp_days = None
                if d.get("license_expiry"):
                    try:
                        exp_date = datetime.strptime(d["license_expiry"], "%Y-%m-%d").date()
                        exp_days = (exp_date - today).days
                    except:
                        pass

                license_warning = ""
                if exp_days is not None and exp_days <= 180:
                    license_warning = f'<br><span style="color:#ffa500;font-size:0.75rem;">⚠️ License expires in {exp_days} days</span>'

                st.markdown(f"""
                <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;
                            padding:1.2rem 1.4rem;margin-bottom:1rem;
                            border-left:4px solid {status_color};">
                    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.8rem;">
                        <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#0f1923,#1a2e44);
                                    display:flex;align-items:center;justify-content:center;
                                    font-size:1.5rem;flex-shrink:0;">👨‍✈️</div>
                        <div>
                            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;">{d['name']}</div>
                            <div style="color:#64748b;font-size:0.8rem;">{d['employee_id']}</div>
                        </div>
                        <div style="margin-left:auto;">
                            <span style="background:{status_color}22;color:{status_color};border:1px solid {status_color}44;
                                         padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;">
                                {d['status']}
                            </span>
                        </div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;font-size:0.82rem;">
                        <div><span style="color:#94a3b8;">📱 Phone</span><br><b>{d['phone']}</b></div>
                        <div><span style="color:#94a3b8;">🎓 Experience</span><br><b>{d['experience_years']} years</b></div>
                        <div><span style="color:#94a3b8;">🚌 Bus</span><br><b>{bus}</b></div>
                        <div><span style="color:#94a3b8;">🛣️ Route</span><br><b>{route}</b></div>
                        <div><span style="color:#94a3b8;">🪪 License</span><br><b style="font-size:0.75rem;">{d['license_number']}</b></div>
                        <div><span style="color:#94a3b8;">📅 Expiry</span><br><b>{d['license_expiry'] or 'N/A'}</b>{license_warning}</div>
                    </div>
                    <div style="margin-top:0.6rem;font-size:0.8rem;color:#64748b;">
                        📍 {d['address'] or 'N/A'} &nbsp;·&nbsp; Joined: {d['joining_date'] or 'N/A'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: Add Driver ─────────────────────────────────────────
    with tab2:
        st.subheader("➕ Register New Driver")
        with st.form("add_driver_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name*")
                employee_id = st.text_input("Employee ID*", placeholder="DRV-006")
                phone = st.text_input("Phone Number*")
                license_number = st.text_input("License Number*")
                license_expiry = st.date_input("License Expiry Date*")
                experience_years = st.number_input("Experience (years)", min_value=0, max_value=50)
            with c2:
                status = st.selectbox("Status", ["Active", "On Leave", "Inactive"])
                assigned_bus = st.selectbox("Assign Bus",
                    options=[0] + [b["id"] for b in buses],
                    format_func=lambda x: "Not Assigned" if x == 0 else bus_map.get(x, ""))
                assigned_route = st.selectbox("Assign Route",
                    options=[0] + [r["id"] for r in routes],
                    format_func=lambda x: "Not Assigned" if x == 0 else route_map.get(x, ""))
                address = st.text_input("Home Address")
                joining_date = st.date_input("Joining Date")

            submitted = st.form_submit_button("✅ Add Driver", use_container_width=True)
            if submitted:
                if not all([name, employee_id, phone, license_number]):
                    st.error("Please fill all required (*) fields.")
                else:
                    try:
                        add_driver({
                            "name": name, "employee_id": employee_id,
                            "phone": phone, "license_number": license_number,
                            "license_expiry": str(license_expiry),
                            "experience_years": experience_years,
                            "assigned_bus": assigned_bus or None,
                            "assigned_route": assigned_route or None,
                            "status": status, "address": address,
                            "joining_date": str(joining_date)
                        })
                        st.success(f"✅ Driver '{name}' registered successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ── Tab 3: Edit/Remove ────────────────────────────────────────
    with tab3:
        st.subheader("✏️ Edit Driver")
        if not drivers:
            st.info("No drivers available.")
        else:
            sel_driver = st.selectbox("Select Driver to Edit",
                options=[d["id"] for d in drivers],
                format_func=lambda x: next(d["name"] + " (" + d["employee_id"] + ")" for d in drivers if d["id"] == x))
            d = next((x for x in drivers if x["id"] == sel_driver), None)

            if d:
                with st.form("edit_driver_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        name = st.text_input("Full Name", value=d["name"])
                        phone = st.text_input("Phone", value=d["phone"] or "")
                        exp_years = st.number_input("Experience (years)", value=d["experience_years"] or 0)
                        lic_exp = st.date_input("License Expiry",
                            value=datetime.strptime(d["license_expiry"], "%Y-%m-%d").date() if d.get("license_expiry") else date.today())
                    with c2:
                        status = st.selectbox("Status", ["Active", "On Leave", "Inactive"],
                            index=["Active", "On Leave", "Inactive"].index(d["status"]) if d["status"] in ["Active", "On Leave", "Inactive"] else 0)
                        assigned_bus = st.selectbox("Assign Bus",
                            options=[0] + [b["id"] for b in buses],
                            index=([0] + [b["id"] for b in buses]).index(d["assigned_bus"] or 0) if (d["assigned_bus"] or 0) in ([0] + [b["id"] for b in buses]) else 0,
                            format_func=lambda x: "Not Assigned" if x == 0 else bus_map.get(x, ""))
                        assigned_route = st.selectbox("Assign Route",
                            options=[0] + [r["id"] for r in routes],
                            index=([0] + [r["id"] for r in routes]).index(d["assigned_route"] or 0) if (d["assigned_route"] or 0) in ([0] + [r["id"] for r in routes]) else 0,
                            format_func=lambda x: "Not Assigned" if x == 0 else route_map.get(x, ""))

                    c_upd, c_del = st.columns(2)
                    with c_upd:
                        update = st.form_submit_button("💾 Update Driver", use_container_width=True)
                    with c_del:
                        delete = st.form_submit_button("🗑️ Delete Driver", use_container_width=True)

                    if update:
                        update_driver(sel_driver, {
                            "name": name, "phone": phone,
                            "license_expiry": str(lic_exp),
                            "experience_years": exp_years,
                            "assigned_bus": assigned_bus or None,
                            "assigned_route": assigned_route or None,
                            "status": status
                        })
                        st.success("✅ Driver updated!")
                        st.rerun()

                    if delete:
                        delete_record("drivers", sel_driver)
                        st.success("Driver removed.")
                        st.rerun()
