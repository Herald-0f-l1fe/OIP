import time as t
import math


def get_sin_wave_amplitude(freq, time):
    return (math.sin(2 * math.pi * freq * time) + 1) / 2

def get_triange_wave_amplitude(freq, time):
    return 1 - abs((time * freq) % 1 * 2 - 1)

def wait_for_sampling_period(sampling_freq):
    t.sleep(1/sampling_freq)