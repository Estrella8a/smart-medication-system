from database import connect_db
import random

conn = connect_db()
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO nurses (id, name) VALUES (1, 'Enfermero 1')")
cursor.execute("INSERT OR IGNORE INTO nurses (id, name) VALUES (2, 'Enfermero 2')")

hours = ['07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22']
statuses = ['taken', 'taken', 'taken', 'missed', 'pending']

for i in range(50):
    hour = random.choice(hours)
    minute = str(random.randint(0, 59)).zfill(2)
    time = f'{hour}:{minute}'
    status = random.choice(statuses)
    nurse_id = random.choice([1, 2])
    cursor.execute(
        'INSERT INTO dose_logs (patient_id, medication_id, time, status, nurse_id) VALUES (?, ?, ?, ?, ?)',
        (1, 1, time, status, nurse_id)
    )

conn.commit()

cursor.execute('SELECT COUNT(*) FROM dose_logs')
print('Total dose_logs:', cursor.fetchone()[0])
cursor.execute('SELECT * FROM nurses')
print('Nurses:', cursor.fetchall())
cursor.execute('SELECT time, status, nurse_id FROM dose_logs LIMIT 5')
print('Sample logs:', cursor.fetchall())

conn.close()
print('✅ Datos falsos insertados correctamente')