from database import connect_db

conn = connect_db()
cursor = conn.cursor()

# Inserta MUCHOS registros fallidos en 14:00
for _ in range(50):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 1, '14:00', 'pending', datetime('now'))
    """)

# Algunos correctos (para que no sea 100% extremo)
for _ in range(10):
    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (1, 1, 1, '14:00', 'taken', datetime('now'))
    """)

conn.commit()
conn.close()

print("Mock 14:00 inserted")