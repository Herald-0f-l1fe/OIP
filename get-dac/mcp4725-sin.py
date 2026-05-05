import signal_generator as sg
from mcp4725_driver import MCP4725
import time as t

amplitude = 1.2
signal_frequency = 20
sampling_frequency = 1000

def main():
    dac = MCP4725(verbose=False)

    while True:
        try:
            time = t.time_ns()/10e9
            voltage = sg.get_sin_wave_amplitude(signal_frequency, time) * amplitude
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)
        except KeyboardInterrupt:
            print("CTRL + c intercepted, exiting")
            dac.deinit()
            break

if __name__ == "__main__":
    main()
    