import time
import threading

# Detectar si estamos en Raspberry Pi
try:
    import RPi.GPIO as GPIO
    IS_PI = True
except ImportError:
    IS_PI = False

BUZZER_PIN = 18

# Configuración GPIO solo en Raspberry Pi
if IS_PI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

def buzz(duration=3):
    if IS_PI:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    else:
        print(f"🔊 BUZZER SIMULADO por {duration} segundos")

def buzz_async(duration=3):
    threading.Thread(target=buzz, args=(duration,), daemon=True).start()

def cleanup():
    if IS_PI:
        GPIO.cleanup()
        print("GPIO cleaned up.")
    else:
        print("GPIO cleanup simulated.")