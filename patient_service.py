from database import connect_db, get_next_available_drawer

# ---------------------
# CREATE
# ---------------------

def add_patient(name, age):
    drawer = get_next_available_drawer()

    if drawer is None:
        return None  # No hay cajones disponibles

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO patients (name, age, drawer_number) VALUES (?, ?, ?)",
        (name, age, drawer)
    )

    conn.commit()
    conn.close()

    return drawer  # devuelve cajón asignado


# ---------------------
# READ
# ---------------------

def get_all_patients():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return patients


# ---------------------
# UPDATE
# ---------------------

def update_patient(patient_id, new_name=None, new_age=None):
    conn = connect_db()
    cursor = conn.cursor()

    if new_name is not None:
        cursor.execute(
            "UPDATE patients SET name = ? WHERE id = ?",
            (new_name, patient_id)
        )

    if new_age is not None:
        cursor.execute(
            "UPDATE patients SET age = ? WHERE id = ?",
            (new_age, patient_id)
        )

    conn.commit()
    conn.close()

# ---------------------
# DELETE
# ---------------------

def delete_patient(patient_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id = ?",
        (patient_id,)
    )

    conn.commit()
    conn.close()