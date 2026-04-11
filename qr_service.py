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

    print("📷 Starting camera preview (rpicam-vid)...")

    process = subprocess.Popen(
        [
            "rpicam-vid",
            "--inline",
            "--nopreview",
            "-t", "0",
            "--width", "640",
            "--height", "480",
            "--framerate", "30",
            "-o", "-"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    try:
        while True:

            # Leer bytes del stream
            data = process.stdout.read(640 * 480 * 3)

            if not data:
                continue

            frame = np.frombuffer(data, dtype=np.uint8)
            frame = frame.reshape((480, 640, 3))

            # Mostrar preview
            cv2.imshow("QR Scanner", frame)

            qr_codes = decode(frame)

            for qr in qr_codes:
                qr_data = qr.data.decode("utf-8")
                print("QR detectado:", qr_data)

                process.terminate()
                cv2.destroyAllWindows()

                callback(qr_data)
                return

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        process.terminate()
        cv2.destroyAllWindows()