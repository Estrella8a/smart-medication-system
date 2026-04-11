from database import connect_db
import random

conn = connect_db()
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO nurses (id, name) VALUES (1, 'Enfermero 1')")
cursor.execute("INSERT OR IGNORE INTO nurses (id, name) VALUES (2, 'Enfermero 2')")

# Horas de RIESGO: 3pm, 4pm, 5pm y 8pm
risky_hours = ['15', '16', '17', '20', '21', '22']  # Agregamos 9pm y 10pm como horas de riesgo también

# Horas NORMALES
normal_hours = ['07', '08', '09', '10', '11', '12', '13', '14', '18', '19', '21', '22']

# 15 registros por hora de riesgo (70% missed)
for hour in risky_hours:
    for i in range(15):
        minute = str(random.randint(0, 59)).zfill(2)
        status = random.choices(['missed', 'pending', 'taken'], weights=[70, 15, 15])[0]
        nurse_id = random.choice([1, 2])
        cursor.execute(
            'INSERT INTO dose_logs (patient_id, medication_id, time, status, nurse_id) VALUES (?, ?, ?, ?, ?)',
            (1, 1, f'{hour}:{minute}', status, nurse_id)
        )

# 5 registros por hora normal (80% taken)
for hour in normal_hours:
    for i in range(5):
        minute = str(random.randint(0, 59)).zfill(2)
        status = random.choices(['taken', 'missed', 'pending'], weights=[80, 10, 10])[0]
        nurse_id = random.choice([1, 2])
        cursor.execute(
            'INSERT INTO dose_logs (patient_id, medication_id, time, status, nurse_id) VALUES (?, ?, ?, ?, ?)',
            (1, 1, f'{hour}:{minute}', status, nurse_id)
        )

conn.commit()

cursor.execute('SELECT COUNT(*) FROM dose_logs')
print(f'Total dose_logs: {cursor.fetchone()[0]}')
cursor.execute('SELECT * FROM nurses')
print('Nurses:', cursor.fetchall())

conn.close()
print('✅ Datos insertados correctamente')