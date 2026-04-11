from database import connect_db
import random

conn = connect_db()
cursor = conn.cursor()

# Nurses
cursor.execute("INSERT OR IGNORE INTO nurses (id, name) VALUES (1, 'Enfermero 1')")
cursor.execute("INSERT OR IGNORE INTO nurses (id, name) VALUES (2, 'Enfermero 2')")

# Horas de RIESGO: 01-05 y 08 → mayoría missed
risky_hours = ['01', '02', '03', '04', '05', '08']

# Horas NORMALES → mayoría taken
normal_hours = ['06', '07', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']

# 15 registros por hora de riesgo (80% missed)
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
total = cursor.fetchone()[0]
print(f'Total dose_logs: {total}')
cursor.execute('SELECT * FROM nurses')
print('Nurses:', cursor.fetchall())

# Verificar horas de riesgo
cursor.execute("SELECT time[:2], COUNT(*), SUM(CASE WHEN status != 'taken' THEN 1 ELSE 0 END) FROM dose_logs GROUP BY substr(time,1,2)")
print('\nHora | Total | Missed')
for row in cursor.fetchall():
    print(f'{row[0]}:00 | {row[1]} | {row[2]}')

conn.close()
print('\n✅ Datos insertados correctamente')