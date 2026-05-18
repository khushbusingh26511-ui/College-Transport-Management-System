import streamlit as st
import pandas as pd
from database import fetch_all, add_student, add_route, delete_record

def show():
    st.markdown("""
    <div class="main-header">
        <div class="badge">🛣️ Routes & Students</div>
        <h1>🛣️ Student Routes</h1>
        <p>Manage bus routes and student transport enrollments</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Routes", "🎓 Students", "➕ Add Route", "➕ Add Student"])

    # ── Tab 1: Routes ──────────────────────────────────────────────
    with tab1:
        routes = fetch_all("routes")
        buses = fetch_all("buses")
        bus_map = {b["id"]: b["bus_number"] for b in buses}

        if routes:
            for r in routes:
                stops_list = r.get("stops", "").split(",") if r.get("stops") else []
                status_color = "#00c864" if r["status"] == "Active" else "#ffa500"
                with st.expander(f"🚌 {r['route_number']} — {r['route_name']}  |  Departs: {r['departure_time']}"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"""
                        <div class="info-box">
                            <b>📍 From:</b> {r['start_point']}<br>
                            <b>🏁 To:</b> {r['end_point']}<br>
                            <b>📏 Distance:</b> {r['distance_km']} km<br>
                            <b>⏱️ Duration:</b> {r['duration_min']} min
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                        <div class="info-box">
                            <b>🚌 Bus:</b> {bus_map.get(r['bus_id'], 'Not Assigned')}<br>
                            <b>🕐 Departure:</b> {r['departure_time']}<br>
                            <b>📊 Status:</b> <span style="color:{status_color};font-weight:700;">{r['status']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"**🗺️ Stops ({len(stops_list)}):**")
                        for i, stop in enumerate(stops_list):
                            prefix = "🔵" if i == 0 else ("🔴" if i == len(stops_list)-1 else "⚪")
                            st.markdown(f"{prefix} {stop.strip()}")

                    col_del = st.columns([4, 1])
                    with col_del[1]:
                        if st.button("🗑️ Delete", key=f"del_route_{r['id']}", type="secondary"):
                            delete_record("routes", r["id"])
                            st.success("Route deleted.")
                            st.rerun()
        else:
            st.info("No routes found.")

    # ── Tab 2: Students ────────────────────────────────────────────
    with tab2:
        students = fetch_all("students")
        routes = fetch_all("routes")
        route_map = {r["id"]: r["route_name"] for r in routes}

        if students:
            search = st.text_input("🔍 Search by name or roll number", placeholder="e.g. Aarav or 2024CS001")
            dept_filter = st.selectbox("Filter by Department", ["All"] + sorted(set(s["department"] for s in students)))

            filtered = students
            if search:
                filtered = [s for s in filtered if search.lower() in s["name"].lower() or search.lower() in s["roll_number"].lower()]
            if dept_filter != "All":
                filtered = [s for s in filtered if s["department"] == dept_filter]

            st.markdown(f"**Showing {len(filtered)} students**")

            df = pd.DataFrame(filtered)
            df["route"] = df["route_id"].map(route_map)
            df["fee_paid"] = df["fee_paid"].map({1: "✅ Paid", 0: "❌ Unpaid"})
            display_cols = ["name", "roll_number", "department", "year", "pickup_stop", "route", "bus_pass_expiry", "fee_paid"]
            display_df = df[display_cols].copy()
            display_df.columns = ["Name", "Roll No.", "Dept.", "Year", "Pickup Stop", "Route", "Pass Expiry", "Fee"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Fee summary
            paid = sum(1 for s in students if s["fee_paid"] == 1)
            unpaid = len(students) - paid
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="success-box">✅ <b>{paid}</b> students have paid transport fee</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="danger-box">❌ <b>{unpaid}</b> students have unpaid transport fee</div>', unsafe_allow_html=True)

            # Delete student
            st.markdown("---")
            del_roll = st.text_input("Enter Roll No. to remove student from transport")
            if st.button("🗑️ Remove Student", type="secondary"):
                match = next((s for s in students if s["roll_number"] == del_roll), None)
                if match:
                    delete_record("students", match["id"])
                    st.success(f"Removed {match['name']} from transport.")
                    st.rerun()
                else:
                    st.error("Roll number not found.")

    # ── Tab 3: Add Route ───────────────────────────────────────────
    with tab3:
        st.subheader("➕ Add New Route")
        buses = fetch_all("buses")

        with st.form("add_route_form"):
            c1, c2 = st.columns(2)
            with c1:
                route_name = st.text_input("Route Name*", placeholder="e.g. Pal Link Road – College")
                route_number = st.text_input("Route Number*", placeholder="e.g. R-06")
                start_point = st.text_input("Start Point*")
                end_point = st.text_input("End Point*", value="Engineering College")
                departure_time = st.text_input("Departure Time*", placeholder="07:30")
            with c2:
                stops = st.text_area("Stops (comma-separated)*", placeholder="Stop 1, Stop 2, College")
                distance_km = st.number_input("Distance (km)", min_value=0.0, step=0.5)
                duration_min = st.number_input("Duration (minutes)", min_value=0, step=5)
                bus_id = st.selectbox("Assign Bus", options=[b["id"] for b in buses],
                                      format_func=lambda x: next(b["bus_number"] for b in buses if b["id"] == x))
                status = st.selectbox("Status", ["Active", "Inactive"])

            submitted = st.form_submit_button("➕ Add Route", use_container_width=True)
            if submitted:
                if not all([route_name, route_number, start_point]):
                    st.error("Please fill all required (*) fields.")
                else:
                    try:
                        add_route({
                            "route_name": route_name, "route_number": route_number,
                            "start_point": start_point, "end_point": end_point,
                            "stops": stops, "distance_km": distance_km,
                            "duration_min": duration_min, "departure_time": departure_time,
                            "bus_id": bus_id, "status": status
                        })
                        st.success(f"✅ Route '{route_name}' added successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ── Tab 4: Add Student ─────────────────────────────────────────
    with tab4:
        st.subheader("➕ Enroll New Student")
        routes = fetch_all("routes")

        with st.form("add_student_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name*")
                roll_number = st.text_input("Roll Number*", placeholder="e.g. 2024CS011")
                department = st.selectbox("Department*", ["Computer Science", "Electronics", "Mechanical", "Civil", "IT", "Electrical", "Chemical"])
                year = st.selectbox("Year", [1, 2, 3, 4])
                phone = st.text_input("Student Phone")
                parent_phone = st.text_input("Parent Phone")
            with c2:
                route_id = st.selectbox("Route*", options=[r["id"] for r in routes],
                                         format_func=lambda x: next(r["route_name"] for r in routes if r["id"] == x))
                pickup_stop = st.text_input("Pickup Stop*")
                drop_stop = st.text_input("Drop Stop", value="College")
                bus_pass_expiry = st.date_input("Bus Pass Expiry")
                fee_paid = st.checkbox("Fee Paid")

            submitted = st.form_submit_button("✅ Enroll Student", use_container_width=True)
            if submitted:
                if not all([name, roll_number, pickup_stop]):
                    st.error("Please fill all required (*) fields.")
                else:
                    try:
                        add_student({
                            "name": name, "roll_number": roll_number,
                            "department": department, "year": year,
                            "phone": phone, "parent_phone": parent_phone,
                            "pickup_stop": pickup_stop, "drop_stop": drop_stop,
                            "route_id": route_id,
                            "bus_pass_expiry": str(bus_pass_expiry),
                            "fee_paid": int(fee_paid)
                        })
                        st.success(f"✅ {name} enrolled successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
