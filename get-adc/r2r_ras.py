import time
import r2r_adc          
import adc_plot         

def main():
    DYNAMIC_RANGE = 3.295   
    DURATION = 3.0         # продолжительность измерений (секунд)
    COMPARE_TIME = 0.001   # время стабилизации компаратора (с)

    adc = r2r_adc.R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=COMPARE_TIME, verbose=False)

    voltage_values = []
    time_values = []

    try:
        start_time = time.time()
        print(f"Измерение напряжения SAR в течение {DURATION} секунд...")
        while time.time() - start_time < DURATION:
            v = adc.get_sar_voltage()          
            t = time.time() - start_time
            voltage_values.append(v)
            time_values.append(t)
        print("Измерение завершено. Строим графики...")
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
        adc_plot.plot_sampling_period_hist(time_values)
    except KeyboardInterrupt:
        print("\nПрерывание пользователем.")
    finally:
        adc.close()
        print("Ресурсы GPIO освобождены.")

if __name__ == "__main__":
    main()