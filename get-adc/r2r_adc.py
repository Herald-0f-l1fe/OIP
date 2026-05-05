import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def number_to_dac(self, number):
        if not (0 <= number <= 255):
            raise ValueError("Число должно быть в диапазоне 0..255")
        for i in range(8):
            bit = (number >> (7 - i)) & 1
            GPIO.output(self.bits_gpio[i], bit)

    def sequential_counting_adc(self):
        for code in range(256):
            self.number_to_dac(code)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:   # 1 означает Vdac > Vin
                if self.verbose:
                    voltage_dac = (code / 255.0) * self.dynamic_range
                    print(f"[DEBUG] Превышение при коде {code} (напряжение ЦАП: {voltage_dac:.3f} В)")
                return code
        if self.verbose:
            print("[DEBUG] Входное напряжение выше динамического диапазона, возвращаем 255")
        return 255

    def get_sc_voltage(self): #Методои последовательного счёта
        code = self.sequential_counting_adc()
        voltage = (code / 255.0) * self.dynamic_range
        return voltage
    
    def successive_approximation_adc(self):
        code = 0
        for bit in range(7, -1, -1):          # от MSB (вес 128) до LSB (вес 1)
            test_code = code | (1 << bit)      # устанавливаем текущий бит
            self.number_to_dac(test_code)
            time.sleep(self.compare_time)      # ждём стабилизации компаратора
            if GPIO.input(self.comp_gpio) == 0:   # 0 = Vdac < Vin  (компаратор говорит, что ЦАП ниже входа)
                code = test_code                # оставляем бит установленным
            # иначе (Vdac > Vin) – сбрасываем бит, ничего не делаем
        return code

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        voltage = (code / 255.0) * self.dynamic_range
        if self.verbose:
            print(f"[DEBUG] SAR: код = {code}, напряжение = {voltage:.3f} В")
        return voltage

    def close(self):
        self.number_to_dac(0)
        GPIO.cleanup()

    def __del__(self):
        self.close()


if __name__ == "__main__":
    DYNAMIC_RANGE = 3.295

    adc = None
    try:
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.001, verbose=False)
        print("Измерение напряжения методом последовательного приближения (SAR). Ctrl+C для выхода.")
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nПрограмма остановлена.")
    finally:
        if adc:
            adc.close()
            print("GPIO очищены.")