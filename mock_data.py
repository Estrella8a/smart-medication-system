from database import connect_db

conn = connect_db()
cursor = conn.cursor()

# -------------------------
# 14:00 (MUY ALTO RIESGO)
# -------------------------
for _ in range(60):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 1, '14:00', 'pending', datetime('now'))
    """)

for _ in range(5):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 1, '14:00', 'taken', datetime('now'))
    """)


# -------------------------
# 15:00 (ALTO RIESGO)
# -------------------------
for _ in range(50):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 2, '15:00', 'pending', datetime('now'))
    """)

for _ in range(10):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 2, '15:00', 'taken', datetime('now'))
    """)


# -------------------------
# 16:00 (RIESGO MEDIO-ALTO)
# -------------------------
for _ in range(40):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 1, '16:00', 'pending', datetime('now'))
    """)

for _ in range(20):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 1, '16:00', 'taken', datetime('now'))
    """)


# -------------------------
# 17:00 (RIESGO MODERADO)
# -------------------------
for _ in range(30):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 2, '17:00', 'pending', datetime('now'))
    """)

for _ in range(25):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 2, '17:00', 'taken', datetime('now'))
    """)


conn.commit()
conn.close()

print(" Mock data 14:00–17:00 inserted")