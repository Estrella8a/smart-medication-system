import cv2
import subprocess
from pyzbar.pyzbar import decode
import os
import time

def scan_qr(callback):
    is_raspberry = os.path.exists("/usr/bin/rpicam-still")
    if is_raspberry:
        print("📷 Raspberry Pi Camera detectada")
        scan_qr_rpi(callback)
    else:
        print("💻 No camera available (not Raspberry Pi)")

def scan_qr_rpi(callback):
    print("📷 Iniciando escaneo QR...")

    MAX_ATTEMPTS = 20
    TIMEOUT = 60
    TEMP_FILE = "/tmp/qr_frame.jpg"  # /tmp es más seguro que el directorio raíz

    start_time = time.time()
    attempts = 0

    while attempts < MAX_ATTEMPTS:

        # Timeout global
        if time.time() - start_time > TIMEOUT:
            print("⏰ Timeout: 60s sin detectar QR")
            break

        try:
            # Captura
            subprocess.run([
                "rpicam-still",
                "-o", TEMP_FILE,
                "--nopreview",
                "-t", "200"       # 200ms: balance entre velocidad y estabilidad
            ], timeout=5)         # sin check=True para no tronar por errores menores

            time.sleep(0.3)       # esperar escritura real del archivo

            frame = cv2.imread(TEMP_FILE)

            if frame is None:
                print(f"⚠️ Frame inválido (intento {attempts + 1})")
                attempts += 1
                continue

            qr_codes = decode(frame)

            if qr_codes:
                data = qr_codes[0].data.decode("utf-8")
                print(f"✅ QR detectado: {data}")
                callback(data)
                return  # salir limpio

            else:
                print(f"🔍 Sin QR (intento {attempts + 1}/{MAX_ATTEMPTS})")
                attempts += 1

        except subprocess.TimeoutExpired:
            print("⚠️ rpicam-still tardó demasiado, reintentando...")
            attempts += 1

        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            attempts += 1

    # Limpieza final
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

    print("❌ Escaneo terminado sin detectar QR")