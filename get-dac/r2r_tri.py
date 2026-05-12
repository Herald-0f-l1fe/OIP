import RPi.GPIO as GPIO
import time
import sys

AMPLITUDE = 2.5        # Амплитуда сигнала (В) – должно быть меньше dynamic_range
FREQ = 100             # Частота треугольного сигнала (Гц)
SAMPLE_RATE = 10000    # Частота дискретизации (Гц) – сколько раз в секунду обновляем ЦАП
DYNAMIC_RANGE = 3.3    # Максимальное напряжение ЦАП (В) – измерьте реальное значение

BITS_GPIO = [16, 20, 21, 25, 26, 17, 27, 22]


def init_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in BITS_GPIO:
        GPIO.setup(pin, GPIO.OUT, initial=0)

def number_to_dac(value):
    if not (0 <= value <= 255):
        raise ValueError("Value must be 0..255")
    for i, pin in enumerate(BITS_GPIO):
        bit = (value >> (7 - i)) & 1
        GPIO.output(pin, bit)

def cleanup():
    number_to_dac(0)
    GPIO.cleanup()


def generate_triangle_values(amplitude_V, max_V, num_samples):
    max_code = 255
    amplitude_code = int((amplitude_V / max_V) * max_code)
    samples_per_period = num_samples
    half = samples_per_period // 2

    values = []
    for i in range(samples_per_period):
        if i <= half:
            val = int((i / half) * amplitude_code)
        else:
            val = int(((samples_per_period - i) / half) * amplitude_code)
        values.append(val)
    return values


def main():
    print("Генерация треугольного сигнала на R2R-ЦАП")
    print(f"Амплитуда: {AMPLITUDE} В, частота: {FREQ} Гц, частота дискретизации: {SAMPLE_RATE} Гц")

    samples_per_period = int(SAMPLE_RATE / FREQ)
    if samples_per_period < 2:
        print("Ошибка: частота дискретизации должна быть хотя бы в 2 раза выше частоты сигнала")
        sys.exit(1)

    triangle_table = generate_triangle_values(AMPLITUDE, DYNAMIC_RANGE, samples_per_period)
    period_time = 1.0 / FREQ              # длительность одного периода (с)
    sample_interval = 1.0 / SAMPLE_RATE   # интервал между обновлениями ЦАП (с)

    init_gpio()
    try:
        while True:
            for code in triangle_table:
                number_to_dac(code)
                time.sleep(sample_interval)
    except KeyboardInterrupt:
        print("\nОстановка пользователем.")
    finally:
        cleanup()
        print("GPIO очищены.")

if __name__ == "__main__":
    main()