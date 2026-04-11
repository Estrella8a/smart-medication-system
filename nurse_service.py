from database import connect_db

def get_nurse_by_id(nurse_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM nurses WHERE id=?", (nurse_id,))
    nurse = cursor.fetchone()

    conn.close()
    return nurse