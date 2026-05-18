import sqlite3
import hashlib
from datetime import datetime, date

DB_PATH = "ctms.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_number TEXT UNIQUE NOT NULL,
        capacity INTEGER NOT NULL,
        model TEXT,
        status TEXT DEFAULT 'Active',
        last_service DATE,
        latitude REAL DEFAULT 26.2389,
        longitude REAL DEFAULT 73.0243,
        current_route TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_name TEXT NOT NULL,
        route_number TEXT UNIQUE NOT NULL,
        start_point TEXT NOT NULL,
        end_point TEXT NOT NULL,
        stops TEXT,
        distance_km REAL,
        duration_min INTEGER,
        departure_time TEXT,
        bus_id INTEGER,
        status TEXT DEFAULT 'Active',
        FOREIGN KEY (bus_id) REFERENCES buses(id)
    );

    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        employee_id TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        license_number TEXT UNIQUE NOT NULL,
        license_expiry DATE,
        experience_years INTEGER,
        assigned_bus INTEGER,
        assigned_route INTEGER,
        status TEXT DEFAULT 'Active',
        address TEXT,
        joining_date DATE,
        photo_url TEXT,
        FOREIGN KEY (assigned_bus) REFERENCES buses(id),
        FOREIGN KEY (assigned_route) REFERENCES routes(id)
    );

    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_number TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        year INTEGER,
        phone TEXT,
        parent_phone TEXT,
        pickup_stop TEXT,
        drop_stop TEXT,
        route_id INTEGER,
        bus_pass_expiry DATE,
        fee_paid INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (route_id) REFERENCES routes(id)
    );

    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        description TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id)
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id INTEGER,
        date DATE,
        status TEXT,
        FOREIGN KEY (driver_id) REFERENCES drivers(id)
    );
    """)

    # Seed admin
    pw = hashlib.sha256("admin123".encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO admin_users (username, password_hash, role) VALUES (?, ?, ?)",
              ("admin", pw, "superadmin"))

    # Seed buses
    buses = [
        ("BUS-001", 45, "Tata Starbus", "Active", "2025-01-10", 26.2948, 73.0149, "Route-1"),
        ("BUS-002", 40, "Ashok Leyland", "Active", "2025-02-15", 26.2511, 73.0232, "Route-2"),
        ("BUS-003", 50, "Volvo 9400", "Active", "2025-03-20", 26.2389, 73.0543, "Route-3"),
        ("BUS-004", 35, "Force Traveller", "Maintenance", "2024-12-05", 26.2712, 73.0087, "Route-4"),
        ("BUS-005", 45, "Tata Starbus", "Active", "2025-04-01", 26.2600, 73.0400, "Route-5"),
    ]
    c.executemany("""INSERT OR IGNORE INTO buses 
        (bus_number,capacity,model,status,last_service,latitude,longitude,current_route) 
        VALUES (?,?,?,?,?,?,?,?)""", buses)

    # Seed routes
    routes = [
        ("Paota – College", "R-01", "Paota Circle", "Engineering College", "Paota,Sojati Gate,Jalori Gate,College", 12.5, 35, "07:30", 1, "Active"),
        ("Ratanada – College", "R-02", "Ratanada", "Engineering College", "Ratanada,Chopasni,Shastri Nagar,College", 9.0, 28, "07:45", 2, "Active"),
        ("Sardarpura – College", "R-03", "Sardarpura", "Engineering College", "Sardarpura,Nai Sarak,Sojati,College", 10.2, 30, "07:40", 3, "Active"),
        ("Shyam Nagar – College", "R-04", "Shyam Nagar", "Engineering College", "Shyam Nagar,Bhagat Ki Kothi,PWD,College", 14.0, 40, "07:20", 4, "Active"),
        ("Mandore – College", "R-05", "Mandore", "Engineering College", "Mandore,Mahamandir,Clock Tower,College", 11.5, 33, "07:35", 5, "Active"),
    ]
    c.executemany("""INSERT OR IGNORE INTO routes 
        (route_name,route_number,start_point,end_point,stops,distance_km,duration_min,departure_time,bus_id,status) 
        VALUES (?,?,?,?,?,?,?,?,?,?)""", routes)

    # Seed drivers
    drivers = [
        ("Ramesh Kumar", "DRV-001", "9876543210", "RJ14-2019-0012345", "2027-06-30", 8, 1, 1, "Active", "Paota, Jodhpur", "2017-03-15"),
        ("Suresh Bishnoi", "DRV-002", "9812345678", "RJ14-2018-0023456", "2026-09-15", 6, 2, 2, "Active", "Ratanada, Jodhpur", "2019-07-01"),
        ("Mahesh Sharma", "DRV-003", "9823456789", "RJ14-2020-0034567", "2028-03-20", 4, 3, 3, "Active", "Sardarpura, Jodhpur", "2021-01-10"),
        ("Dinesh Yadav", "DRV-004", "9834567890", "RJ14-2017-0045678", "2025-12-01", 12, 4, 4, "On Leave", "Shyam Nagar, Jodhpur", "2013-08-20"),
        ("Pradeep Joshi", "DRV-005", "9845678901", "RJ14-2021-0056789", "2029-07-10", 3, 5, 5, "Active", "Mandore, Jodhpur", "2022-06-01"),
    ]
    c.executemany("""INSERT OR IGNORE INTO drivers 
        (name,employee_id,phone,license_number,license_expiry,experience_years,assigned_bus,assigned_route,status,address,joining_date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""", drivers)

    # Seed students
    students = [
        ("Aarav Mehta", "2024CS001", "Computer Science", 2, "9901234567", "9912345678", "Paota Circle", "College", 1, "2026-03-31", 1),
        ("Priya Sharma", "2024EC002", "Electronics", 2, "9923456789", "9934567890", "Ratanada", "College", 2, "2026-03-31", 1),
        ("Rahul Bishnoi", "2024ME003", "Mechanical", 3, "9945678901", "9956789012", "Sardarpura", "College", 3, "2026-03-31", 1),
        ("Sneha Joshi", "2024CE004", "Civil", 1, "9967890123", "9978901234", "Shyam Nagar", "College", 4, "2026-03-31", 0),
        ("Vikram Rathore", "2024IT005", "IT", 4, "9989012345", "9990123456", "Mandore", "College", 5, "2026-03-31", 1),
        ("Anjali Gehlot", "2024CS006", "Computer Science", 1, "9801234567", "9812345678", "Paota Circle", "College", 1, "2026-03-31", 1),
        ("Kiran Patel", "2024EC007", "Electronics", 3, "9823456789", "9834567890", "Ratanada", "College", 2, "2026-03-31", 0),
        ("Deepak Singh", "2024ME008", "Mechanical", 2, "9845678901", "9856789012", "Sardarpura", "College", 3, "2026-03-31", 1),
        ("Meera Pareek", "2024CE009", "Civil", 4, "9867890123", "9878901234", "Shyam Nagar", "College", 4, "2026-03-31", 1),
        ("Arjun Vyas", "2024IT010", "IT", 2, "9889012345", "9890123456", "Mandore", "College", 5, "2026-03-31", 1),
    ]
    c.executemany("""INSERT OR IGNORE INTO students
        (name,roll_number,department,year,phone,parent_phone,pickup_stop,drop_stop,route_id,bus_pass_expiry,fee_paid)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""", students)

    conn.commit()
    conn.close()

# ---- CRUD helpers ----

def fetch_all(table):
    conn = get_connection()
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def fetch_one(table, id):
    conn = get_connection()
    row = conn.execute(f"SELECT * FROM {table} WHERE id=?", (id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_stats():
    conn = get_connection()
    stats = {
        "total_buses": conn.execute("SELECT COUNT(*) FROM buses").fetchone()[0],
        "active_buses": conn.execute("SELECT COUNT(*) FROM buses WHERE status='Active'").fetchone()[0],
        "total_drivers": conn.execute("SELECT COUNT(*) FROM drivers").fetchone()[0],
        "active_drivers": conn.execute("SELECT COUNT(*) FROM drivers WHERE status='Active'").fetchone()[0],
        "total_students": conn.execute("SELECT COUNT(*) FROM students").fetchone()[0],
        "fee_paid": conn.execute("SELECT COUNT(*) FROM students WHERE fee_paid=1").fetchone()[0],
        "total_routes": conn.execute("SELECT COUNT(*) FROM routes").fetchone()[0],
    }
    conn.close()
    return stats

def add_driver(data):
    conn = get_connection()
    conn.execute("""INSERT INTO drivers (name,employee_id,phone,license_number,license_expiry,
        experience_years,assigned_bus,assigned_route,status,address,joining_date)
        VALUES (:name,:employee_id,:phone,:license_number,:license_expiry,
        :experience_years,:assigned_bus,:assigned_route,:status,:address,:joining_date)""", data)
    conn.commit()
    conn.close()

def update_driver(id, data):
    conn = get_connection()
    conn.execute("""UPDATE drivers SET name=:name,phone=:phone,license_expiry=:license_expiry,
        experience_years=:experience_years,assigned_bus=:assigned_bus,
        assigned_route=:assigned_route,status=:status WHERE id=:id""",
        {**data, "id": id})
    conn.commit()
    conn.close()

def delete_record(table, id):
    conn = get_connection()
    conn.execute(f"DELETE FROM {table} WHERE id=?", (id,))
    conn.commit()
    conn.close()

def add_student(data):
    conn = get_connection()
    conn.execute("""INSERT INTO students (name,roll_number,department,year,phone,parent_phone,
        pickup_stop,drop_stop,route_id,bus_pass_expiry,fee_paid)
        VALUES (:name,:roll_number,:department,:year,:phone,:parent_phone,
        :pickup_stop,:drop_stop,:route_id,:bus_pass_expiry,:fee_paid)""", data)
    conn.commit()
    conn.close()

def add_route(data):
    conn = get_connection()
    conn.execute("""INSERT INTO routes (route_name,route_number,start_point,end_point,stops,
        distance_km,duration_min,departure_time,bus_id,status)
        VALUES (:route_name,:route_number,:start_point,:end_point,:stops,
        :distance_km,:duration_min,:departure_time,:bus_id,:status)""", data)
    conn.commit()
    conn.close()

def add_bus(data):
    conn = get_connection()
    conn.execute("""INSERT INTO buses (bus_number,capacity,model,status,last_service)
        VALUES (:bus_number,:capacity,:model,:status,:last_service)""", data)
    conn.commit()
    conn.close()

def update_bus_location(bus_id, lat, lng):
    conn = get_connection()
    conn.execute("UPDATE buses SET latitude=?, longitude=? WHERE id=?", (lat, lng, bus_id))
    conn.commit()
    conn.close()

def verify_admin(username, password):
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    row = conn.execute("SELECT * FROM admin_users WHERE username=? AND password_hash=?",
                       (username, pw_hash)).fetchone()
    conn.close()
    return dict(row) if row else None

def add_complaint(data):
    conn = get_connection()
    conn.execute("""INSERT INTO complaints (student_id, subject, description)
        VALUES (:student_id, :subject, :description)""", data)
    conn.commit()
    conn.close()

def get_complaints():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.*, s.name as student_name, s.roll_number 
        FROM complaints c LEFT JOIN students s ON c.student_id = s.id
        ORDER BY c.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_complaint_status(id, status):
    conn = get_connection()
    conn.execute("UPDATE complaints SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()
