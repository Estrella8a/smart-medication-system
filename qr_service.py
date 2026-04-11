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
        print("💻 no camara")
        # Aquí implementar una versión para webcam usando OpenCV
        # scan_qr_webcam(callback)
    

# -------------------------
# RASPBERRY (rpicamera)
# -------------------------
import subprocess
import time
import cv2
from pyzbar.pyzbar import decode


def scan_qr_rpi(callback):

    print("📷 Abriendo preview...")

    #  ABRIR PREVIEW UNA SOLA VEZ
    preview = subprocess.Popen([
        "rpicam-hello",
        "-t", "0"
    ])

    try:
        print("Apunta el QR...")

        time.sleep(4)  #  tiempo para que el usuario se prepare
        # 4 segundos para que el preview esté listo y el usuario pueda apuntar el QR

        while True:

            #  CAPTURA
            subprocess.run([
                "rpicam-still",
                "-o", "frame.jpg",
                "--nopreview",
                "-t", "500"
            ])

            time.sleep(0.7)  # (esperar escritura real)

            frame = cv2.imread("frame.jpg")

            if frame is None:
                print("❌ Frame inválido")
                continue

            qr_codes = decode(frame)

            if qr_codes:
                data = qr_codes[0].data.decode("utf-8")
                print("✅ QR detectado:", data)

                preview.terminate()  # cerrar cámara
                callback(data)
                return

    except Exception as e:
        print("❌ Error QR:", e)

    finally:
        preview.terminate()