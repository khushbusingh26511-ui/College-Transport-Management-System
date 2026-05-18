import streamlit as st
import folium
from streamlit_folium import st_folium
from database import fetch_all, update_bus_location
import random

def show():
    st.markdown("""
    <div class="main-header">
        <div class="badge">📡 Live Tracking</div>
        <h1>🗺️ Bus Tracking</h1>
        <p>Real-time location monitoring of all college buses</p>
    </div>
    """, unsafe_allow_html=True)

    buses = fetch_all("buses")
    routes = fetch_all("routes")
    route_map = {r["id"]: r for r in routes}

    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("🚌 Bus Status")
        selected_bus = st.selectbox(
            "Select Bus to Track",
            options=[b["bus_number"] for b in buses],
            index=0
        )
        sel = next((b for b in buses if b["bus_number"] == selected_bus), None)
        if sel:
            status_color = "#00c864" if sel["status"] == "Active" else "#ffa500"
            st.markdown(f"""
            <div style="background:#f8fafc;border-radius:12px;padding:1.2rem;border:1px solid #e2e8f0;">
                <div style="font-size:1.8rem;text-align:center;margin-bottom:0.5rem;">🚌</div>
                <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;text-align:center;">{sel['bus_number']}</div>
                <div style="text-align:center;color:#64748b;font-size:0.85rem;margin-bottom:1rem;">{sel['model']}</div>
                <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                    <span style="color:#64748b;font-size:0.8rem;">Status</span>
                    <span style="color:{status_color};font-weight:600;font-size:0.8rem;">{sel['status']}</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                    <span style="color:#64748b;font-size:0.8rem;">Capacity</span>
                    <span style="font-weight:600;font-size:0.8rem;">{sel['capacity']} seats</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                    <span style="color:#64748b;font-size:0.8rem;">Route</span>
                    <span style="font-weight:600;font-size:0.8rem;">{sel['current_route'] or 'N/A'}</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#64748b;font-size:0.8rem;">Coordinates</span>
                    <span style="font-weight:600;font-size:0.75rem;">{sel['latitude']:.4f}, {sel['longitude']:.4f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔄 Simulate Location")
        if st.button("📡 Update Bus Locations", use_container_width=True):
            # Simulate random small GPS drift
            jodhpur_center = (26.2389, 73.0243)
            for b in buses:
                if b["status"] == "Active":
                    new_lat = jodhpur_center[0] + random.uniform(-0.05, 0.05)
                    new_lng = jodhpur_center[1] + random.uniform(-0.05, 0.05)
                    update_bus_location(b["id"], round(new_lat, 4), round(new_lng, 4))
            st.success("✅ Locations updated!")
            st.rerun()

        st.markdown("---")
        st.subheader("📋 All Buses")
        for b in buses:
            icon = "🟢" if b["status"] == "Active" else "🟡" if b["status"] == "Maintenance" else "🔴"
            st.markdown(f"""
            <div style="padding:0.4rem 0;border-bottom:1px solid #f0f0f0;font-size:0.85rem;">
                {icon} <b>{b['bus_number']}</b> · {b['model']}<br>
                <span style="color:#94a3b8;font-size:0.75rem;padding-left:1.2rem;">{b['current_route'] or 'No route'}</span>
            </div>
            """, unsafe_allow_html=True)

    with col1:
        # Build Folium map centered on Jodhpur
        m = folium.Map(
            location=[26.2389, 73.0243],
            zoom_start=12,
            tiles="CartoDB positron"
        )

        # Route stop coordinates (approximate for Jodhpur)
        route_coords = {
            1: [(26.2948, 73.0149), (26.2800, 73.0180), (26.2650, 73.0200), (26.2512, 73.0200), (26.2389, 73.0243)],
            2: [(26.2511, 73.0232), (26.2560, 73.0290), (26.2480, 73.0310), (26.2389, 73.0243)],
            3: [(26.2700, 73.0350), (26.2600, 73.0280), (26.2500, 73.0260), (26.2389, 73.0243)],
            4: [(26.2712, 73.0087), (26.2600, 73.0150), (26.2500, 73.0180), (26.2389, 73.0243)],
            5: [(26.3200, 73.0500), (26.2950, 73.0420), (26.2700, 73.0350), (26.2389, 73.0243)],
        }

        route_colors = ["#FF6B35", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

        for i, (rid, coords) in enumerate(route_coords.items()):
            if i < len(routes):
                r = routes[i]
                folium.PolyLine(
                    locations=coords,
                    color=route_colors[i % len(route_colors)],
                    weight=3,
                    opacity=0.7,
                    tooltip=f"Route {r['route_number']}: {r['route_name']}"
                ).add_to(m)

                # Add stop markers
                stops = r.get("stops", "").split(",") if r.get("stops") else []
                for j, (lat, lng) in enumerate(coords[:-1]):
                    stop_name = stops[j].strip() if j < len(stops) else f"Stop {j+1}"
                    folium.CircleMarker(
                        location=[lat, lng],
                        radius=5,
                        color=route_colors[i % len(route_colors)],
                        fill=True,
                        fill_color=route_colors[i % len(route_colors)],
                        fill_opacity=0.8,
                        tooltip=stop_name
                    ).add_to(m)

        # College marker
        folium.Marker(
            location=[26.2389, 73.0243],
            popup="<b>Engineering College</b>",
            tooltip="🎓 College",
            icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa")
        ).add_to(m)

        # Bus markers
        for bus in buses:
            lat, lng = bus.get("latitude", 26.2389), bus.get("longitude", 73.0243)
            if lat and lng:
                color = "green" if bus["status"] == "Active" else "orange"
                popup_html = f"""
                <div style="font-family:sans-serif;min-width:150px;">
                    <b style="font-size:1rem;">🚌 {bus['bus_number']}</b><br>
                    <span style="color:#666;">{bus['model']}</span><br><br>
                    <b>Status:</b> {bus['status']}<br>
                    <b>Capacity:</b> {bus['capacity']} seats<br>
                    <b>Route:</b> {bus['current_route'] or 'N/A'}
                </div>
                """
                folium.Marker(
                    location=[lat, lng],
                    popup=folium.Popup(popup_html, max_width=200),
                    tooltip=f"🚌 {bus['bus_number']} ({bus['status']})",
                    icon=folium.Icon(color=color, icon="bus", prefix="fa")
                ).add_to(m)

        # Legend
        legend_html = """
        <div style="position:fixed;bottom:30px;left:30px;background:white;padding:12px 16px;
                    border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.2);z-index:1000;font-size:12px;">
            <b>Map Legend</b><br>
            🟢 Active Bus &nbsp;&nbsp; 🟡 Maintenance<br>
            🎓 College Campus &nbsp;&nbsp; ● Route Stop
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m, width=None, height=550, returned_objects=[])
