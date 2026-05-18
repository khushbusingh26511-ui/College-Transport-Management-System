# 🚌 College Transport Management System (CTMS)

A full-featured transport management web application built with **Python**, **Streamlit**, **SQLite**, and **Folium**.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py
```

### 3. Open Browser
The app will auto-open at: **http://localhost:8501**

---

## 🔐 Admin Login
- **Username:** `admin`  
- **Password:** `admin123`

---

## 📁 Project Structure
```
college_transport/
├── app.py              # Main entry point + routing + CSS
├── database.py         # SQLite DB init, seed data, CRUD helpers
├── requirements.txt    # Python dependencies
├── ctms.db             # SQLite database (auto-created on first run)
├── pages/
│   ├── dashboard.py        # 🏠 Overview & KPIs
│   ├── bus_tracking.py     # 🗺️ Folium live map + location simulation
│   ├── student_routes.py   # 🛣️ Routes & student enrollment
│   ├── driver_details.py   # 🚗 Driver profiles & assignments
│   └── admin_panel.py      # ⚙️ Secure admin controls, reports, complaints
└── README.md
```

---

## 🎯 Features

| Module | Features |
|--------|----------|
| **Dashboard** | Fleet KPIs, bus status table, departure schedule, recent enrollments |
| **Bus Tracking** | Interactive Folium map, route polylines, stop markers, location simulation |
| **Student Routes** | Route details with stop-by-stop view, student directory with search/filter, enrollment form |
| **Driver Details** | Driver cards with license expiry alerts, add/edit/delete drivers, assignment management |
| **Admin Panel** | Login-protected, bus fleet management, utilization reports, fee reports, complaint system, password change |

---

## 🛠️ Technology Stack
- **Frontend:** Streamlit
- **Backend:** Python 3.10+
- **Database:** SQLite (via Python's built-in `sqlite3`)
- **Mapping:** Folium + streamlit-folium
- **Data Processing:** Pandas

---

## 🗃️ Database Tables
- `buses` — Fleet records
- `routes` — Bus routes with stops
- `drivers` — Driver profiles & assignments
- `students` — Student enrollment & fee status
- `admin_users` — Authenticated admin accounts
- `complaints` — Student complaints & resolution tracking
- `attendance` — Driver attendance log

---

## 🌍 Real-Life Industry Usage
- **Colleges & Universities** — Manage daily student transport
- **Transport Departments** — Fleet, driver, and route administration
- **School Boards** — Bus tracking and parent communication

---

*Built for Engineering College, Jodhpur, Rajasthan · Academic Year 2025–26*
