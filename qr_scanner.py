import cv2
import numpy as np
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk

def scan_qr(callback):
    threading.Thread(target=_scan, args=(callback,), daemon=True).start()

def _scan(callback):
    print("📷 Iniciando cámara...")

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "XBGR8888"}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(1)

    TIMEOUT = 25
    start_time = time.time()
    detected = None

    # Ventana tkinter para mostrar cámara
    win = tk.Toplevel()
    win.title("Escanear QR - Q para cancelar")
    win.geometry("640x480")

    label = tk.Label(win)
    label.pack()

    def update_frame():
        nonlocal detected

        if time.time() - start_time > TIMEOUT:
            print("⏰ Timeout QR sin detectar")
            win.destroy()
            return

        frame = picam2.capture_array()

        # Convertir XBGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        # Buscar QR
        qr_codes = decode(frame_rgb)
        for qr in qr_codes:
            detected = qr.data.decode("utf-8")
            print(f"✅ QR detectado: {detected}")
            pts = [(p.x, p.y) for p in qr.polygon]
            for i in range(len(pts)):
                cv2.line(frame_rgb, pts[i], pts[(i+1) % len(pts)], (0,255,0), 3)

        # Mostrar en ventana
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.config(image=imgtk)

        if detected:
            time.sleep(0.4)
            win.destroy()
            picam2.stop()
            picam2.close()
            callback(detected)
            return

        win.after(30, update_frame)

    win.after(0, update_frame)
    win.mainloop()

    if not detected:
        picam2.stop()
        picam2.close()