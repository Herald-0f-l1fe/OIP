import time
import adc_plot as plt
from r2r_adc import R2R_ADC

if __name__ == "__main__":
    adc = R2R_ADC(3.3)

    voltage_values = []
    time_values = []
    duration = 10.0

    try:
        start_time = time.time()

        while(time.time() - start_time < duration):
            current_time = time.time() - start_time

            voltage = adc.get_sc_voltage()
            voltage_values.append(voltage)

            time_values.append(current_time)

        plt.plot_voltage_vs_time(time_values, voltage_values, 3.3)
        plt.plot_sampling_period_hist(time_values)
    finally:
        adc.deinit()
        