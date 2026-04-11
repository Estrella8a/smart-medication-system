from database import connect_db
import datetime

def register_dose(patient_id, medication_id, nurse_id, status):

    conn = connect_db()
    cursor = conn.cursor()

    current_time = datetime.datetime.now().strftime("%H:%M")

    cursor.execute("""
        INSERT INTO dose_logs (patient_id, medication_id, nurse_id, time, status, timestamp)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (
        patient_id,
        medication_id,
        nurse_id,
        current_time,   # 🔥 ESTE ES EL FIX
        status
    ))

    conn.commit()
    conn.close()

    print("💾 GUARDADO:", current_time, patient_id, medication_id, status)

def get_last_60_min_logs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name, m.name, d.time, d.status, d.timestamp
        FROM dose_logs d
        JOIN patients p ON d.patient_id = p.id
        JOIN medications m ON d.medication_id = m.id
        WHERE d.timestamp >= datetime('now', '-60 minutes')
        ORDER BY d.timestamp DESC
    """)

    results = cursor.fetchall()
    conn.close()
    return results

def confirm_dose_late(patient_id, medication_id, nurse_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM dose_logs
        WHERE patient_id = ?
        AND medication_id = ?
        AND status = 'pending'
        ORDER BY timestamp DESC
        LIMIT 1
    """, (patient_id, medication_id))

    row = cursor.fetchone()

    if row:
        cursor.execute("""
            UPDATE dose_logs
            SET status = 'taken', nurse_id = ?
            WHERE id = ?
        """, (nurse_id, row[0]))

    conn.commit()
    conn.close()

def confirm_last_pending():
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM dose_logs
            WHERE status = 'pending'
            ORDER BY timestamp DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        if not row:
            conn.close()
            return False

        cursor.execute("""
            UPDATE dose_logs
            SET status = 'taken'
            WHERE id = ?
        """, (row[0],))

        conn.commit()
        conn.close()

        return True

def confirm_last_pending():
        from database import connect_db

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM dose_logs
            WHERE status = 'pending'
            ORDER BY timestamp DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        if not row:
            conn.close()
            return False

        cursor.execute("""
            UPDATE dose_logs
            SET status = 'taken'
            WHERE id = ?
        """, (row[0],))

        conn.commit()
        conn.close()

        return True