import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__ (self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    def number_to_dac(self, number):
        output = [int(element) for element in bin(number)[2:].zfill(8)]
        for i in range (8):
            GPIO.output(self.bits_gpio[i], output[i])
    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)

            time.sleep(self.compare_time)
        return 0
    def get_sc_voltage(self):
        voltage = (self.sequential_counting_adc()/256)*self.dynamic_range
        if self.verbose:
            print(f"Напряжение: {voltage:.3f}В")
        return voltage

    def successive_approximation_adc(self):
        left = 0
        right = 255
        result = 255

        while left <= right:
            mid = (left + right) // 2
            self.number_to_dac(mid)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == GPIO.HIGH:
                result = mid
                right = mid - 1
            else:
                left = mid + 1
        return result
    
    def get_sar_voltage(self):
        voltage = (self.successive_approximation_adc()/256)*self.dynamic_range
        if self.verbose:
            print(f"Напряжение: {voltage:.3f}В")
        return voltage


    
if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.3, verbose=True)

        while True:
            # adc.get_sar_voltage()
            adc.get_sc_voltage()
    finally:
        adc.deinit()
