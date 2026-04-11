import cv2
import subprocess
import time
import os
from pyzbar.pyzbar import decode


# -------------------------
# ENTRY POINT
# -------------------------
def scan_qr(callback):

    is_raspberry = os.path.exists("/usr/bin/rpicam-still")

    if is_raspberry:
        print("📷 Raspberry mode")
        scan_qr_rpi(callback)
    else:
        print("💻 Webcam fallback")
        scan_qr_webcam(callback)


# -------------------------
# RASPBERRY IMPLEMENTATION
# -------------------------
def scan_qr_rpi(callback):

    print("📷 Abriendo preview...")

    preview = subprocess.Popen([
        "rpicam-hello",
        "-t", "0"
    ])

    start_time = time.time()
    timeout = 30  # 🔥 máximo 30 segundos

    try:
        time.sleep(2)  # pequeño tiempo de preparación

        while True:

            # ⏱️ TIMEOUT GLOBAL
            if time.time() - start_time > timeout:
                print("⏰ Timeout QR")
                return

            # 📸 CAPTURA
            subprocess.run([
                "rpicam-still",
                "-o", "frame.jpg",
                "--nopreview",
                "-t", "400"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            time.sleep(0.5)

            frame = cv2.imread("frame.jpg")

            if frame is None:
                print("❌ Frame inválido")
                continue

            qr_codes = decode(frame)

            if qr_codes:
                data = qr_codes[0].data.decode("utf-8")
                print("✅ QR detectado:", data)

                callback(data)
                return

    except Exception as e:
        print("❌ Error QR:", e)

    finally:
        # 🔥 cerrar cámara SIEMPRE (una sola vez)
        try:
            preview.terminate()
        except:
            pass

        # 🔥 limpiar archivo temporal
        try:
            if os.path.exists("frame.jpg"):
                os.remove("frame.jpg")
        except:
            pass


# -------------------------
# WEBCAM FALLBACK (PC)
# -------------------------
def scan_qr_webcam(callback):

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No webcam disponible")
        return

    start_time = time.time()
    timeout = 20

    while True:

        if time.time() - start_time > timeout:
            print("⏰ Timeout webcam")
            break

        ret, frame = cap.read()
        if not ret:
            continue

        qr_codes = decode(frame)

        if qr_codes:
            data = qr_codes[0].data.decode("utf-8")
            print("✅ QR detectado:", data)

            callback(data)
            break

    cap.release()

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