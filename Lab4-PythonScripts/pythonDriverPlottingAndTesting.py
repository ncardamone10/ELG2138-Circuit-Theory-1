
from tabulate import tabulate


from msox2000aSeriesScopeDriver import Scope
import time
import numpy as np
import os
import matplotlib.pyplot as plt
from pyvisa import VisaIOError
import pyvisa

# Initialize the oscilloscope
visa_address = 'USB0::2391::6041::MY55280378::INSTR'  # Replace with your actual address
scope = Scope(visa_address)

# Specify the channels to measure
channels = [1, 2]

# Perform measurements
measurements = {}
for channel in channels:
    measurements[channel] = {
        'Vpp': scope.measure_vpp(channel),
        'Vmax': scope.measure_vmax(channel),
        'Vmin': scope.measure_vmin(channel),
        'Vamplitude': scope.measure_vamplitude(channel),
        'Vaverage (Display)': scope.measure_vaverage_display(channel),
        'Vrms (Cycle AC)': scope.measure_vrms_cycle_ac(channel),
        'Vrms (Display AC)': scope.measure_vrms_display_ac(channel),
        'Period': scope.measure_period(channel),
        'Frequency': scope.measure_frequency(channel),
        'Positive Width': scope.measure_positive_width(channel),
        'Negative Width': scope.measure_negative_width(channel),
        'Duty Cycle': scope.measure_duty_cycle(channel),
        'Rise Time': scope.measure_rise_time(channel),
        'Fall Time': scope.measure_fall_time(channel)
    }

# Display measurements in a table
headers = ["Measurement", "Channel 1", "Channel 2"]
data = [[key, measurements[1][key], measurements[2][key]] for key in measurements[1]]
print(tabulate(data, headers=headers))

# Plotting the waveforms
time_scale = np.arange(0, len(scope.grab_data(1)), 1)
plt.plot(time_scale, scope.grab_data(1), label='Channel 1')
plt.plot(time_scale, scope.grab_data(2), label='Channel 2')
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title('Channel 1 and Channel 2 Waveforms')
plt.legend()
plt.show()
