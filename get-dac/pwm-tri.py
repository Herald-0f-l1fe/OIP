import RPi.GPIO as GPIO
import time
import sys
import math

AMPLITUDE = 2.5        # Амплитуда (В)
FREQ = 100             # Частота (Гц)
SAMPLE_RATE = 10000    # Частота дискретизации (Гц)
PWM_FREQ = 100000      # Базовая частота ШИМ (Гц)
PWM_PIN = 12           # GPIO с ШИМ
DYNAMIC_RANGE = 3.3    # Максимальное напряжение (В)

def set_voltage(pwm, voltage_V):
    duty = (voltage_V / DYNAMIC_RANGE) * 100.0
    duty = max(0, min(100, duty))  # ограничение 0-100
    pwm.ChangeDutyCycle(duty)

def triangle_wave(t, freq, amplitude):
    period = 1.0 / freq
    t_norm = (t % period) / period
    triangle_norm = 1.0 - 4.0 * abs(t_norm - 0.5)
    return triangle_norm * amplitude

def main():
    print("Генерация треугольного сигнала на PWM DAC (упрощённая версия)")
    print(f"Амплитуда: {AMPLITUDE} В, частота: {FREQ} Гц, частота дискретизации: {SAMPLE_RATE} Гц")
    
    if AMPLITUDE > DYNAMIC_RANGE:
        print(f"Ошибка: амплитуда слишком большая!")
        sys.exit(1)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN, GPIO.OUT)
    pwm = GPIO.PWM(PWM_PIN, PWM_FREQ)
    pwm.start(0)
    
    sample_interval = 1.0 / SAMPLE_RATE
    t = 0.0
    
    print("\nГенерация запущена. Ctrl+C для остановки.")
    
    try:
        while True:
            voltage = triangle_wave(t, FREQ, AMPLITUDE)
            set_voltage(pwm, voltage)
            t += sample_interval
            time.sleep(sample_interval)
    except KeyboardInterrupt:
        print("\nОстановка пользователем.")
    finally:
        set_voltage(pwm, 0)
        pwm.stop()
        GPIO.cleanup()
        print("Завершено.")

if __name__ == "__main__":
    main()