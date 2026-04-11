from pyzbar.pyzbar import decode
import time
import threading

def scan_qr(callback):
    threading.Thread(target=_scan, args=(callback,), daemon=True).start()

def _scan(callback):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    TIMEOUT = 25
    start_time = time.time()
    detected = None

    print("📷 Apunta el QR a la cámara...")

    cv2.namedWindow("Escanear QR - Q para cancelar", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Escanear QR - Q para cancelar", 640, 480)

    while True:
        if time.time() - start_time > TIMEOUT:
            print("⏰ Timeout QR sin detectar")
            break

        ret, frame = cap.read()
        if not ret:
            continue

        qr_codes = decode(frame)
        for qr in qr_codes:
            detected = qr.data.decode("utf-8")
            pts = [(p.x, p.y) for p in qr.polygon]
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i+1) % len(pts)], (0,255,0), 3)
            cv2.putText(frame, f"✅ {detected}",
                        (qr.rect.left, qr.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.putText(frame, "Apunta el QR | Q = cancelar",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255,255,255), 2)

        cv2.imshow("Escanear QR - Q para cancelar", frame)

        if detected:
            time.sleep(0.4)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if detected:
        callback(detected)