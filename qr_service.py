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
def scan_qr_rpi(callback):

    print("📷 Opening camera preview...")

    # Abrir preview REAL
    preview = subprocess.Popen([
        "rpicam-hello",
        "-t", "0"
    ])

    try:
        while True:

            subprocess.run([
                "rpicam-still",
                "-o", "frame.jpg",
                "--nopreview",
                "-t", "100"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            frame = cv2.imread("frame.jpg")

            if frame is None:
                continue

            qr_codes = decode(frame)

            for qr in qr_codes:
                data = qr.data.decode("utf-8")
                print("QR detectado:", data)

                preview.terminate()
                callback(data)
                return

    finally:
        preview.terminate()