# 🚌 College Transport Management System (CTMS)

A full-featured **College Transport Management System** built with Python and Streamlit.  
Manage buses, routes, drivers, and students — all in one place.

[Features](#-features)
• [Screenshots](#-screenshots) 
• [Installation](#-installation) 
• [Usage](#-usage) 
• [Database](#-database-schema) 
• [Contributing](#-contributing)

 📌 About The Project

The **College Transport Management System (CTMS)** is a web-based application designed to streamline and digitize the transport operations of colleges and universities. It provides real-time bus tracking on an interactive map, complete student route management, driver profile management, and a secure admin panel — all accessible through a clean and modern UI.

Built for **Engineering College, Jodhpur, Rajasthan** as a final year project.

✨ Features

🏠 Dashboard
- Live KPI cards — total buses, drivers, students, routes
- Fleet status overview table
- Today's departure schedule
- Recent student enrollments

🗺️ Bus Tracking
- Interactive **Folium map** centered on Jodhpur
- Real-time bus location markers (color-coded by status)
- Route polylines with stop markers
- Bus location simulation (GPS drift)
- Clickable popups with full bus info

🛣️ Student Routes
- Full route directory with stop-by-stop breakdown
- Distance, duration, departure time per route
- Student enrollment table with search & department filter
- Fee payment status tracking
- Add new routes and enroll new students

🚗 Driver Details
- Driver profile cards with photo avatar
- License expiry alerts (warns 6 months in advance)
- Bus and route assignment management
- Add / Edit / Delete drivers
- Experience and status tracking

⚙️ Admin Panel *(Login Protected)*
- Secure login with hashed passwords (SHA-256)
- Bus fleet management — add/remove buses
- Route utilization report (students vs capacity)
- Fee collection report by department
- Complaint management system with status tracking
- Admin password change
- Full system statistics

🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **Streamlit** | Web application framework |
| **SQLite** | Lightweight relational database |
| **Folium** | Interactive map rendering |
| **streamlit-folium** | Folium integration with Streamlit |
| **Pandas** | Data manipulation and display |

📁 Project Structure

```
college_transport/
│
├── app.py                  # Main entry point, routing, global CSS
├── database.py             # DB schema, seed data, all CRUD functions
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── ctms.db                 # SQLite database (auto-created on first run)
│
└── pages/
    ├── __init__.py         # Package init
    ├── dashboard.py        # Dashboard page
    ├── bus_tracking.py     # Live map tracking page
    ├── student_routes.py   # Routes & student management page
    ├── driver_details.py   # Driver profiles page
    └── admin_panel.py      # Admin panel page
```

---

⚙️ Installation

Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/college-transport-management.git
cd college-transport-management
```

Step 2 — Create Virtual Environment

```bash
python -m venv venv
```

Step 3 — Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

Step 5 — Run the Application

```bash
streamlit run app.py
```

Step 6 — Open in Browser

```
http://localhost:8501
```

The database (`ctms.db`) is **automatically created and seeded** with sample data on the first run.

---

🔐 Default Admin Credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ Change the password after first login via **Admin Panel → System → Change Password**

---

🗃️ Database Schema

```
buses          → id, bus_number, capacity, model, status, last_service, latitude, longitude, current_route
routes         → id, route_name, route_number, start_point, end_point, stops, distance_km, duration_min, departure_time, bus_id, status
drivers        → id, name, employee_id, phone, license_number, license_expiry, experience_years, assigned_bus, assigned_route, status, address, joining_date
students       → id, name, roll_number, department, year, phone, parent_phone, pickup_stop, drop_stop, route_id, bus_pass_expiry, fee_paid
admin_users    → id, username, password_hash, role
complaints     → id, student_id, subject, description, status, created_at
attendance     → id, driver_id, date, status
```

---

📦 Sample Data (Pre-loaded)

The system comes pre-loaded with realistic Jodhpur data:

- **5 Buses** — Tata Starbus, Ashok Leyland, Volvo 9400, Force Traveller
- **5 Routes** — Paota, Ratanada, Sardarpura, Shyam Nagar, Mandore → College
- **5 Drivers** — With license details and assignments
- **10 Students** — Across CS, EC, ME, Civil, IT departments
- **1 Admin User** — admin / admin123

---

🚀 Deployment

Deploy on Streamlit Cloud (Free)

1. Push your code to **GitHub**
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **New App**
4. Select your repository and set **Main file:** `app.py`
5. Click **Deploy** ✅

Deploy on Replit

1. Go to [https://replit.com](https://replit.com)
2. Create new **Python** repl
3. Upload all project files
4. In Shell run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

🌍 Real-Life Industry Usage

- 🎓 **Colleges & Universities** — Daily student transport management
- 🏫 **Schools** — School bus tracking and parent communication
- 🏛️ **Transport Departments** — Fleet, driver, and route administration
- 🏢 **Corporate Shuttles** — Employee transport management

---

⚠️ Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` |
| `venv\Scripts\activate` fails | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell as Admin |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
| `python not recognized` | Reinstall Python and check **"Add to PATH"** during install |
| Database locked error | Close any other running instance of the app |


Acknowledgements

- [Streamlit](https://streamlit.io) — Amazing Python web framework
- [Folium](https://python-visualization.github.io/folium/) — Beautiful map rendering
- [OpenStreetMap](https://www.openstreetmap.org) — Free map tiles
- [SQLite](https://www.sqlite.org) — Lightweight embedded database
