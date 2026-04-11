import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "med_system.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

MAX_DRAWERS = 4

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        drawer_number INTEGER NOT NULL UNIQUE
    )
    """)

    # Medications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        UNIQUE(patient_id, name)
    )
    """)

    # Schedules table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication_id INTEGER NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (medication_id) REFERENCES medications(id)
    )
    """)

    # ===== NURSES TABLE =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nurses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")

    # ===== DOSE LOGS TABLE =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dose_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        medication_id INTEGER,
        time TEXT,
        status TEXT,
        nurse_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    
    conn.commit()
    conn.close()

def get_next_available_drawer():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT drawer_number FROM patients")
    used = [row[0] for row in cursor.fetchall()]
    conn.close()

    for i in range(1, MAX_DRAWERS + 1):
        if i not in used:
            return i

    return None