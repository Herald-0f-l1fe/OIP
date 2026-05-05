import time
import r2r_adc          
import adc_plot

def main():
    DYNAMIC_RANGE = 3.295
    DURATION = 3.0         

    adc = r2r_adc.R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.001, verbose=False)

    voltage_values = []
    time_values = []

    try:
        start_time = time.time()
        print(f"Измерение напряжения в течение {DURATION} секунд...")
        while time.time() - start_time < DURATION:
            v = adc.get_sc_voltage()           # измеряем напряжение
            t = time.time() - start_time       # относительное время
            voltage_values.append(v)
            time_values.append(t)
        print("Измерение завершено. Строим график...")
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    except KeyboardInterrupt:
        print("\nПрерывание пользователем.")
    finally:
        adc.close()
        print("Ресурсы GPIO освобождены.")

if __name__ == "__main__":
    main()