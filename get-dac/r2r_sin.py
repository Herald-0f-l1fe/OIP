import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2          
signal_frequency = 10    
sampling_frequency = 1000 

dac_pins = [16, 20, 21, 25, 26, 17, 27, 22]
max_v = 3.3

import numpy as np
import time

def get_sin_wave_amplitude(freq, t):
    # Формула: (sin(2 * pi * f * t) + 1) / 2
    sin_val = np.sin(2 * np.pi * freq * t)
    return (sin_val + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)


try:
    dac = r2r.R2R_DAC(dac_pins, max_v)
    
    start_time = time.time()
    
    print(f"Генерация синуса: {signal_frequency}Гц, амплитуда {amplitude}В")
    print("Нажмите Ctrl+C для остановки")

    while True:
        current_time = time.time() - start_time
        
        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        
        target_voltage = norm_amp * amplitude
        dac.set_voltage(target_voltage)
        
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nГенерация остановлена пользователем")

finally:
    dac.deinit()
