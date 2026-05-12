import smbus
import time
import adc_plot as plt

class MCP3021:
    def __init__ (self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose
    def deinit(self):
        self.bus.close()
    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)

        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}")

        return number
    def get_voltage(self):
        number = self.get_number()

        if self.verbose:
            print(f"Напряжение: {(number/1024)*self.dynamic_range:.3f}В")
        return (number/1024)*self.dynamic_range

if __name__ == "__main__":
    adc = MCP3021(3.3)

    voltage_values = []
    time_values = []
    duration = 10.0

    try:
        start_time = time.time()
        current_time = 0

        while(current_time < duration):
            current_time = time.time() - start_time

            voltage = adc.get_voltage()
            voltage_values.append(voltage)

            time_values.append(current_time)

        plt.plot_voltage_vs_time(time_values, voltage_values, 3.3)
        plt.plot_sampling_period_hist(time_values)
    finally:
        adc.deinit()

        