import cv2
import subprocess
import numpy as np
from pyzbar.pyzbar import decode
import os


def scan_qr(callback):

    # Detectar si está en Raspberry
    is_raspberry = os.path.exists("/usr/bin/rpicam-still")
    if is_raspberry:
        print("📷 Using Raspberry Pi Camera (libcamera)")
        scan_qr_rpi(callback)
    else:
        print("💻 Using Laptop Camera (OpenCV)")
        scan_qr_pc(callback)


# -------------------------
# LAPTOP (OpenCV)
# -------------------------
def scan_qr_pc(callback):

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        qr_codes = decode(frame)

        for qr in qr_codes:
            data = qr.data.decode('utf-8')
            print("QR detectado:", data)

            cap.release()
            cv2.destroyAllWindows()

            callback(data)
            return

        cv2.imshow("QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# -------------------------
# RASPBERRY (rpicamera)
# -------------------------
import subprocess
import time
import cv2
from pyzbar.pyzbar import decode


def scan_qr_rpi(callback):

    print("📷 Abriendo cámara...")

    try:
        while True:

            # 🔥 PREVIEW REAL (BLOQUEANTE)
            subprocess.run([
                "rpicam-hello",
                "-t", "1500"   # 1.5 segundos
            ])

            # 🔥 CAPTURA
            subprocess.run([
                "rpicam-still",
                "-o", "frame.jpg",
                "--nopreview",
                "-t", "300"
            ])

            time.sleep(0.5)

            frame = cv2.imread("frame.jpg")

            if frame is None:
                print("❌ No se pudo leer frame")
                continue

            qr_codes = decode(frame)

            for qr in qr_codes:
                data = qr.data.decode("utf-8")
                print("✅ QR detectado:", data)

                callback(data)
                return

    except Exception as e:
        print("❌ Error QR:", e)