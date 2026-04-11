import cv2
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import time
import threading

def scan_qr(callback):
    threading.Thread(target=_scan, args=(callback,), daemon=True).start()

def _scan(callback):
    print("📷 Iniciando cámara...")

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(1)

    TIMEOUT = 25
    start_time = time.time()
    detected = None

    print("📷 Apunta el QR a la cámara...")

    while True:
        if time.time() - start_time > TIMEOUT:
            print("⏰ Timeout QR sin detectar")
            break

        frame = picam2.capture_array()

        if frame is None:
            continue

        qr_codes = decode(frame)
        for qr in qr_codes:
            detected = qr.data.decode("utf-8")
            print(f"✅ QR detectado: {detected}")
            break

        if detected:
            break

    picam2.stop()
    picam2.close()

    if detected:
        callback(detected)