import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
        
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        number = max(0, min(int(number), 255))
        binary_str = bin(number)[2:].zfill(8)
        
        for i in range(8):
            bit = int(binary_str[i])
            GPIO.output(self.gpio_bits[i], bit)
            
        if self.verbose:
            print(f"На ЦАП подано число: {number} (bin: {binary_str})")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage}В выходит за пределы (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            self.set_number(0)
            return

        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)

if __name__ == "__main__":
    dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.16, True)
    
    try:
        while True:
            try:
                user_input = input("Введите напряжение в Вольтах (или Ctrl+C для выхода): ")
                voltage = float(user_input)
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    except KeyboardInterrupt:
        print("\nЗавершение работы по команде пользователя.")
        
    finally:
        dac.deinit()
