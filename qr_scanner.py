import cv2
import numpy as np
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk

def scan_qr(callback):
    import tkinter as tk
    root = tk._default_root
    root.after(0, lambda: _open_qr_window(root, callback))

def _open_qr_window(root, callback):
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "XBGR8888"}
    )
    picam2.configure(config)
    picam2.start()

    win = tk.Toplevel(root)
    win.title("Escanear QR - Q para cancelar")
    win.geometry("640x480")

    label = tk.Label(win)
    label.pack()

    start_time = time.time()
    TIMEOUT = 25

    def update_frame():
        if not win.winfo_exists():
            picam2.stop()
            picam2.close()
            return

        if time.time() - start_time > TIMEOUT:
            print("⏰ Timeout QR sin detectar")
            picam2.stop()
            picam2.close()
            win.destroy()
            return

        frame = picam2.capture_array()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        qr_codes = decode(frame_rgb)
        detected = None
        for qr in qr_codes:
            detected = qr.data.decode("utf-8")
            print(f"✅ QR detectado: {detected}")
            pts = [(p.x, p.y) for p in qr.polygon]
            for i in range(len(pts)):
                cv2.line(frame_rgb, pts[i], pts[(i+1) % len(pts)], (0, 255, 0), 3)

        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.config(image=imgtk)

        if detected:
            picam2.stop()
            picam2.close()
            win.destroy()
            root.after(0, lambda: callback(detected))  # ✅ callback en hilo principal
            return

        win.after(30, update_frame)

    win.after(500, update_frame)  # esperar 500ms que estabilice la cámara