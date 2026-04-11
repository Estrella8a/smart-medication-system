from database import connect_db

def get_schedules_by_medication(med_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, time FROM schedules WHERE medication_id = ?",
        (med_id,)
    )
    data = cursor.fetchall()
    conn.close()
    return data


def add_schedule(med_id, time):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO schedules (medication_id, time) VALUES (?, ?)",
        (med_id, time)
    )
    conn.commit()
    conn.close()


def delete_schedule(schedule_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM schedules WHERE id = ?",
        (schedule_id,)
    )
    conn.commit()
    conn.close()