from logging import root
import tkinter as tk
import queue
from ui.main_window import MainWindow
from database import initialize_db
from clock_service import start_clock

# Este archivo se puede usar para ejecutar la aplicación con interfaz gráfica
# Si quieres usar la versión de consola, ejecuta main_console.py en su lugar.

# ----------------------
# MAIN APPLICATION
# ----------------------

import tkinter as tk
from ui.main_window import MainWindow
from database import initialize_db
from clock_service import start_clock

def main():
    initialize_db()  # 🔥 Crea todas las tablas antes de usarlas

    root = tk.Tk()
    app = MainWindow(root)

    stop_event = start_clock(app.ui_event_queue)

    def on_close():
        print("Closing application...")
        stop_event.set()
        app.on_close()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()