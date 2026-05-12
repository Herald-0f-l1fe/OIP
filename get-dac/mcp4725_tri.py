import smbus
import time
import sys

AMPLITUDE = 3.0        # Амплитуда (В) – не больше DYNAMIC_RANGE
FREQ = 50              # Частота (Гц)
SAMPLE_RATE = 5000     # Частота дискретизации (Гц)
I2C_ADDRESS = 0x61     # I2C адрес MCP4725
DYNAMIC_RANGE = 5.0    # Опорное напряжение (В)

class SimpleMCP4725:
    def __init__(self, dynamic_range, address=0x61):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.dynamic_range = dynamic_range
    
    def set_voltage(self, voltage):
        code = int((voltage / self.dynamic_range) * 4095)
        code = max(0, min(4095, code))
        first_byte = 0x00 | (code >> 8)
        second_byte = code & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
    
    def close(self):
        self.bus.close()

def triangle_wave(t, freq, amplitude):
    period = 1.0 / freq
    t_norm = (t % period) / period
    triangle_norm = 1.0 - 4.0 * abs(t_norm - 0.5)
    return triangle_norm * amplitude

def main():
    print(f"Треугольный сигнал: {AMPLITUDE} В, {FREQ} Гц, {SAMPLE_RATE} Гц")
    
    dac = SimpleMCP4725(DYNAMIC_RANGE, I2C_ADDRESS)
    sample_interval = 1.0 / SAMPLE_RATE
    t = 0.0
    
    try:
        while True:
            voltage = triangle_wave(t, FREQ, AMPLITUDE)
            dac.set_voltage(voltage)
            t += sample_interval
            time.sleep(sample_interval)
    except KeyboardInterrupt:
        print("\nОстановка.")
    finally:
        dac.set_voltage(0)
        dac.close()
        print("Завершено.")

if __name__ == "__main__":
    main()