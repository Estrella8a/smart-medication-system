import tkinter as tk
from dose_service import get_last_60_min_logs, register_dose
from ui.patient_panel import PatientPanel
from tkinter import messagebox, simpledialog
import queue


import tkinter as tk
import queue
import datetime

from ui.patient_panel import PatientPanel

from qr_scanner import scan_qr
from nurse_service import get_nurse_by_id
from dose_service import register_dose
from database import connect_db
import threading


import os
import platform

def ajustar_orientacion():
    # Solo intentamos rotar si estamos en Linux (la Raspberry)
    if platform.system() == "Linux":
        print("🔄 Rotando pantalla a modo vertical (izquierda)...")
        # El comando 'xrandr' gira la interfaz gráfica
        os.system("DISPLAY=:0 xrandr --output HDMI-1 --rotate left")

# En el __init__ de tu clase MainWindow, llama a la función:
class MainWindow:
    def __init__(self, root):
        ajustar_orientacion()
        self.root = root
        
        self.root = root
        self.root.title("Smart Medication System")
        self.current_alarm = None
        self.alarm_confirmed = False

        self.current_alarm = None
        self.alarm_confirmed = False

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        width = int(screen_width * 0.8)
        height = int(screen_height * 0.85)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(480, 700)

        root.configure(bg="#F5F5F5")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        
        self.notification_history = []  # Para almacenar eventos de notificación recientes

        self.ui_event_queue = queue.Queue()

        self.create_layout()
        self.start_ui_event_loop()

        self.history_window = None
        self.qr_active = False



    def create_layout(self):

        # CONTENEDOR PRINCIPAL
        self.container = tk.Frame(self.root, bg="#F5F5F5")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=0)  # banner
        self.container.rowconfigure(1, weight=0)  # botones
        self.container.rowconfigure(2, weight=1)  # contenido

        # =========================
        # 🔴 BANNER (ALERTA)
        # =========================
        banner_frame = tk.Frame(self.container, bg="#D32F2F")
        banner_frame.grid(row=0, column=0, sticky="ew")

        banner_frame.columnconfigure(0, weight=1)
        banner_frame.columnconfigure(1, weight=0)

        analytics_button = tk.Button(
            banner_frame,
            text="📊",
            font=("Arial", 14),
            command=self.open_analytics,
            bg="#D32F2F",
            fg="white",
            relief="flat"
        )
        analytics_button.grid(row=0, column=2, sticky="e", padx=5)

        self.reminder_label = tk.Label(
            banner_frame,
            text="",
            bg="#D32F2F",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=5
        )
        self.reminder_label.grid(row=0, column=0, sticky="w", padx=10)

        history_button = tk.Button(
            banner_frame,
            text="🔔",
            font=("Arial", 14),
            command=self.open_history,
            bg="#D32F2F",
            fg="white",
            relief="flat"
        )
        history_button.grid(row=0, column=1, sticky="e", padx=10)

        # =========================
        # 🔵 BOTONES (DEBAJO DEL BANNER)
        # =========================
        self.button_frame = tk.Frame(self.container, bg="#F5F5F5")
        self.button_frame.grid(row=1, column=0, sticky="ew", pady=5)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.confirm_button = tk.Button(
            self.button_frame,
            text="Confirm (QR)",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            command=self.start_qr_scan
        )
        self.confirm_button.grid(row=0, column=0, padx=10, sticky="ew")
        self.confirm_button.grid_remove()  # solo aparece con alerta

        self.confirm_manual_button = tk.Button(
            self.button_frame,
            text="✔ Confirm Pending",
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            command=self.confirm_pending_manual
        )
        self.confirm_manual_button.grid(row=0, column=1, padx=10, sticky="ew")
        # 👇 ESTE YA NO SE OCULTA
        # siempre visible

        # =========================
        # 🧩 CONTENIDO PRINCIPAL
        # =========================
        self.patient_panel = PatientPanel(self.container)
        self.patient_panel.grid(row=2, column=0, sticky="nsew")

    def open_analytics(self):
        from ai_service import get_missed_doses_by_hour, get_nurse_performance, get_worst_nurse
        win = tk.Toplevel(self.root)
        win.title("AI Analytics")
        win.geometry("500x500")

        text = tk.Text(win)
        text.pack(fill="both", expand=True)

        # Horas
        text.insert("end", "=== Missed by Hour ===\n")
        stats = get_missed_doses_by_hour()
        for h, d in sorted(stats.items()):
            ratio = d["missed"] / d["total"] if d["total"] else 0
            text.insert("end", f"{h}:00 → missed {d['missed']}/{d['total']} ({ratio:.2f})\n")

        # Enfermeros
        text.insert("end", "\n=== Nurse Performance ===\n")
        nstats = get_nurse_performance()
        for n, d in nstats.items():
            ratio = d["missed"] / d["total"] if d["total"] else 0
            text.insert("end", f"Nurse {n} → {d['missed']}/{d['total']} ({ratio:.2f})\n")

        worst, r = get_worst_nurse()
        text.insert("end", f"\nWorst nurse: {worst} ({r:.2f})\n")

    def start_qr_scan(self):
        if self.qr_active:
            return
        self.qr_active = True

        def on_qr_done(data):
            self.qr_active = False
            self.alarm_confirmed = True        # ✅ evita que marque missed
            self.process_qr(data)              # ya estamos en hilo principal

        scan_qr(on_qr_done)
            
    def confirm_with_qr(self):
        scan_qr(self.process_qr)

    def process_qr(self, data):
        print("QR RAW:", data)

        try:
            nurse_id = int(data)

            from nurse_service import get_nurse_by_id
            nurse = get_nurse_by_id(nurse_id)

            if not nurse:
                print("❌ Nurse no encontrado")
                return

            print("✅ Nurse:", nurse)

            if not self.current_alarm:
                return

            from dose_service import confirm_dose_late

            confirm_dose_late(
                self.current_alarm["patient_id"],
                self.current_alarm["medication_id"],
                nurse_id
            )

            self.alarm_confirmed = True

            self.reminder_label.config(text="✅ Confirmed")
            self.confirm_button.grid_remove()

            self.open_history()


        except Exception as e:
            print("❌ ERROR QR:", e)

    def start_ui_event_loop(self):
        self.process_ui_events()

    def process_ui_events(self):

        while not self.ui_event_queue.empty():
            event = self.ui_event_queue.get()
            self.show_reminder(event)

        self.update_pending_button()
        self.root.after(500, self.process_ui_events)
        

    def add_to_history(self, event):
        import datetime

        now = datetime.datetime.now()

        event_record = {
            "time_triggered": now,
            "patient_name": event["patient_name"],
            "medication_name": event["medication_name"],
            "scheduled_time": event["time"]
        }

        self.notification_history.append(event_record)

        # Mantener solo los últimos 30 minutos
        cutoff = now - datetime.timedelta(minutes=30)
        self.notification_history = [
            e for e in self.notification_history
            if e["time_triggered"] > cutoff
        ]

    def open_history(self):

        # Si ya existe y sigue abierta → traer al frente
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            self.history_window.focus_force()
            return

        # Crear nueva ventana
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("Alarm History")
        self.history_window.geometry("400x400")

        # Cuando se cierre → limpiar referencia
        def on_close():
            self.history_window.destroy()
            self.history_window = None

        self.history_window.protocol("WM_DELETE_WINDOW", on_close)

        # -------------------------
        # CONTENIDO
        # -------------------------
        text = tk.Text(self.history_window)
        text.pack(fill="both", expand=True)

        try:
            from dose_service import get_last_60_min_logs

            logs = get_last_60_min_logs()

            for patient, med, time, status, ts in logs:
                icon = "✔" if status == "taken" else "⏳"
                text.insert("end", f"{time} | {patient} | {med} | {icon}\n")

        except Exception as e:
            text.insert("end", f"Error loading logs: {e}")

    def show_reminder(self, event):

        # -------------------------
        # RESET ESTADO
        # -------------------------
        self.alarm_confirmed = False
        self.current_alarm = event

        # -------------------------
        # 🚨 EARLY ALERT (IA)
        # -------------------------
        if event.get("early_warning"):

            self.reminder_label.config(
                text=f"⚠ SOON TO TAKE: {event['patient_name']} - {event['medication_name']} ({event['time']})",
                bg="#FFA000"
            )

            # 🔔 buzzer corto
            try:
                from buzzer_service import buzz_async
                buzz_async(2)
            except:
                pass

            # ❌ IMPORTANTE:
            # - NO guardar en DB
            # - NO activar timer
            # - NO mostrar botones
            # - NO pending
            # - NO missed

            self.current_alarm = None
            self.alarm_confirmed = True

            return  # 🔥 corta aquí toda la lógica

        # -------------------------
        # 🔔 ALERTA NORMAL
        # -------------------------
        self.reminder_label.config(
            text=f"🔔 {event['patient_name']} - {event['medication_name']} ({event['time']})",
            bg="#D32F2F"
        )

        # -------------------------
        # GUARDAR EN DB (PENDING)
        # -------------------------
        try:
            from dose_service import register_dose

            print("💾 Guardando PENDING en DB")

            register_dose(
                event["patient_id"],
                event["medication_id"],
                None,
                "pending"
            )

        except Exception as e:
            print("❌ Error guardando dose:", e)

        # -------------------------
        # BOTONES
        # -------------------------
        self.confirm_button.grid()
        self.confirm_manual_button.grid()

        # -------------------------
        # TIMER PARA MISSED
        # -------------------------
        self.root.after(30000, self.check_alarm_timeout)

        # -------------------------
        # BUZZER NORMAL
        # -------------------------
        try:
            from buzzer_service import buzz_async
            buzz_async(5)
        except:
            pass

    def get_nurse_shift(hour):
        hour = int(hour)

        if 7 <= hour < 19:
            return 1  # día
        else:
            return 2  # noche
        
    def get_shift_performance():
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT time, status
            FROM dose_logs
        """)

        data = cursor.fetchall()
        conn.close()

        stats = {"day": {"missed": 0, "total": 0},
                "night": {"missed": 0, "total": 0}}

        for time, status in data:
            hour = int(time[:2])

            shift = "day" if 7 <= hour < 19 else "night"

            stats[shift]["total"] += 1

            if status != "taken":
                stats[shift]["missed"] += 1

        return stats    

    def confirm_pending_manual(self):
        from dose_service import confirm_last_pending

        success = confirm_last_pending()

        if success:
            self.reminder_label.config(text="✔ Pending confirmed")
        else:
            self.reminder_label.config(text="⚠ No pending doses")

        self.open_history()

    def update_pending_button(self):
        from database import connect_db

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM dose_logs WHERE status='pending' LIMIT 1")
        has_pending = cursor.fetchone()

        conn.close()

        if has_pending:
            self.confirm_manual_button.config(bg="#2196F3")
        else:
            self.confirm_manual_button.config(bg="gray")

    def check_alarm_timeout(self):
            if self.alarm_confirmed:
                return

            self.reminder_label.config(text="❌ Dose missed")
            self.confirm_button.grid_remove()

            print("⏰ Dose missed")

    def on_close(self):
        try:
            from buzzer_service import cleanup
            cleanup()
        except Exception as e:
            print(f"Cleanup skipped: {e}")
        finally:
            self.root.destroy()