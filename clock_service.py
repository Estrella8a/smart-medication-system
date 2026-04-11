import time
import threading
import datetime
from datetime import timedelta
from database import connect_db
from ai_service import get_risky_hours

def get_all_schedules():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT schedules.time,
               medications.name,
               patients.name,
               patients.id,
               medications.id,
               schedules.id
        FROM schedules
        JOIN medications ON schedules.medication_id = medications.id
        JOIN patients ON medications.patient_id = patients.id
    """)
    schedules = cursor.fetchall()
    conn.close()
    return schedules

def check_schedules(ui_queue, stop_event):
    triggered_today = set()
    triggered_early = set()
    print("⏰ Clock service running...")

    while not stop_event.is_set():
        print("⏰ Checking schedules...")
        now = datetime.datetime.now().strftime("%H:%M")
        today = datetime.date.today()

        try:
            risky_hours = get_risky_hours()
        except:
            risky_hours = []

        schedules = get_all_schedules()

        for schedule_time, med_name, patient_name, patient_id, med_id, schedule_id in schedules:
            if not schedule_time:
                continue

            key = (schedule_id, today)
            early_key = ("early", schedule_id, today)

            schedule_hour = schedule_time[:2]

            schedule_dt = datetime.datetime.strptime(schedule_time, "%H:%M")
            early_dt = (schedule_dt - timedelta(minutes=10)).strftime("%H:%M")

            # ⚠ EARLY ALERT (IA) - solo si la hora es de riesgo
            if (
                schedule_hour in risky_hours
                and now == early_dt
                and early_key not in triggered_early
            ):
                triggered_early.add(early_key)
                event = {
                    "patient_name": patient_name,
                    "medication_name": med_name,
                    "time": schedule_time,
                    "patient_id": patient_id,
                    "medication_id": med_id,
                    "schedule_id": schedule_id,
                    "early_warning": True
                }
                print("⚠ EARLY ALERT (IA):", event)
                ui_queue.put(event)

            # 🔔 ALERTA NORMAL
            if schedule_time == now and key not in triggered_today:
                triggered_today.add(key)
                event = {
                    "patient_name": patient_name,
                    "medication_name": med_name,
                    "time": schedule_time,
                    "patient_id": patient_id,
                    "medication_id": med_id,
                    "schedule_id": schedule_id
                }
                print("🔔 NORMAL ALERT:", event)
                ui_queue.put(event)

        time.sleep(30)

def start_clock(ui_queue):
    stop_event = threading.Event()
    thread = threading.Thread(
        target=check_schedules,
        args=(ui_queue, stop_event),
        daemon=True
    )
    thread.start()
    print("⏰ Clock service started...")
    return stop_event  # ✅ esto faltaba