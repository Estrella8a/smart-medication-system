from database import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("INSERT INTO nurses (name) VALUES (?)", ("Enfermero 1",))
cursor.execute("INSERT INTO nurses (name) VALUES (?)", ("Enfermero 2",))

conn.commit()
conn.close()