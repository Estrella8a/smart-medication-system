from database import connect_db
import sqlite3

def medication_exists(patient_id, name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM medications WHERE patient_id = ? AND LOWER(name) = LOWER(?)",
        (patient_id, name)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists
# ---------------------
# CREATE // ADD MEDICATION
# ---------------------

def add_medication(patient_id, name, dosage):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO medications (patient_id, name, dosage) VALUES (?, ?, ?)",
            (patient_id, name, dosage)
        )
        conn.commit()
        return True  # Insertado correctamente

    except sqlite3.IntegrityError:
        return False  # Duplicado detectado

    finally:
        conn.close()

# ---------------------
# READ
# ---------------------

def get_medications_by_patient(patient_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, dosage
        FROM medications
        WHERE patient_id = ?
    """, (patient_id,))

    meds = cursor.fetchall()
    conn.close()

    return meds

# ---------------------
# UPDATE
# ---------------------

def update_medication(medication_id, new_name=None, new_dosage=None):
    conn = connect_db()
    cursor = conn.cursor()

    if new_name is not None:
        cursor.execute(
            "UPDATE medications SET name = ? WHERE id = ?",
            (new_name, medication_id)
        )

    if new_dosage is not None:
        cursor.execute(
            "UPDATE medications SET dosage = ? WHERE id = ?",
            (new_dosage, medication_id)
        )

    conn.commit()
    conn.close()

# ---------------------
# DELETE
# ---------------------

def delete_medication(medication_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM medications WHERE id = ?",
        (medication_id,)
    )

    conn.commit()
    conn.close()

# ---------------------
# ADD SCHEDULE
# ---------------------

def add_schedule(medication_id, time_str):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO schedules (medication_id, time) VALUES (?, ?)",
        (medication_id, time_str)
    )

    conn.commit()
    conn.close()


# ---------------------
# GET SCHEDULES
# ---------------------

def get_schedules_by_medication(medication_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, time FROM schedules WHERE medication_id = ?",
        (medication_id,)
    )

    schedules = cursor.fetchall()
    conn.close()

    return schedules


# ---------------------
# DELETE SCHEDULE
# ---------------------

def delete_schedule(schedule_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM schedules WHERE id = ?",
        (schedule_id,)
    )

    conn.commit()
    conn.close()