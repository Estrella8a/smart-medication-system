import cv2
from pyzbar.pyzbar import decode

def scan_qr(callback):
    cap = cv2.VideoCapture(0)

    print("Escaneando QR...")

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ No se pudo leer frame")
            break

        # 🔍 Detectar QR
        qr_codes = decode(frame)

        for qr in qr_codes:
            data = qr.data.decode('utf-8')
            print("QR detectado:", data)

            cap.release()
            cv2.destroyAllWindows()

            callback(data)
            return  # ✅ SOLO aquí

        # 🔥 ESTO FALTABA
        cv2.imshow("QR Scanner", frame)

        # ESC para salir
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()