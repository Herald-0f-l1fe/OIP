import RPi.GPIO as GPIO

dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]

dynamic_range = 3.16

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_bits, GPIO.OUT)

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    binary_str = bin(number)[2:].zfill(8)
    
    for i in range(8):
        bit = int(binary_str[i])
        GPIO.output(dac_bits[i], bit)

try:
    while True:
        try:
            user_input = input("Введите напряжение в Вольтах (или 'q' для выхода): ")
            if user_input.lower() == 'q':
                break
                
            voltage = float(user_input)
            number = voltage_to_number(voltage)
            
            print(f"Подаем на ЦАП число: {number}")
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()
    print("\nПрограмма завершена, GPIO очищены.")
