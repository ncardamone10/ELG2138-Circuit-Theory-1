from msox2000aSeriesScopeDriver import Scope
import time
import numpy as np
import os
import matplotlib.pyplot as plt
from pyvisa import VisaIOError
import pyvisa


# Initialize the oscilloscope
visa_address = 'USB0::2391::6039::MY56271217::INSTR'  # Replace with your actual address
scope = Scope(visa_address)

# Perform default setup
scope.default_setup()

# Set up channels
scope.set_vertical_divisions(1, 1)  # 1 V/div for Channel 1
scope.set_vertical_divisions(0.5, 2)  # 0.5 V/div for Channel 2

# Set the timebase
scope.set_time_base(1e-3)  # 1 ms/div

# Set up the function generator
func_gen_settings = {
    'waveform': 'SIN',
    'frequency': 1000,  # 1 kHz
    'amplitude': 1,  # 1 Vpp
    'output': True  # Enable function generator
}
scope.set_function_generator_settings(func_gen_settings)

# Set the trigger
trigger_settings = {
    'channel': 1,
    'level': 0.5,  # 0.5 V
    'type': 'EDGE',
    'slope': 'POS'
}
scope.set_trigger_settings(**trigger_settings)

print("Oscilloscope and function generator configured successfully.")
