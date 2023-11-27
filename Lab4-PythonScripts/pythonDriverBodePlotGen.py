import numpy as np
import matplotlib.pyplot as plt
import time
from msox2000aSeriesScopeDriver import Scope

# Initialize the oscilloscope
visa_address = 'USB0::2391::6039::MY56271217::INSTR'
scope = Scope(visa_address)

# Bode plot parameters
start_freq = 0.1e3  # Start frequency: 1 kHz
end_freq = 100e3   # End frequency: 10 kHz
#step_freq = 0.1e3   # Frequency step: 1 kHz
amplitude = 1     # Amplitude: 1 Vpp
number_of_points = 1000

# Frequency sweep
#frequencies = np.arange(start_freq, end_freq + step_freq, step_freq)
frequencies = np.logspace(np.log10(start_freq), np.log10(end_freq), number_of_points)
input_vpp = amplitude  # Input voltage (constant)
output_vpp = []
input_vpp_measured = []

# Configure the function generator
scope.set_function_generator_settings({
    'waveform': 'SIN',
    'amplitude': amplitude,
    'output': True
})

# Measurement loop
for freq in frequencies:
    # Set function generator frequency
    scope.set_function_generator_settings({'frequency': freq})

    # Allow some time for the scope to adjust to the new frequency
    time.sleep(0.1)

    # Measure output peak-to-peak voltage on Channel 2
    measured_vpp = scope.measure_vpp(2)
    measured_vpp_input = scope.measure_vpp(1)
    output_vpp.append(measured_vpp)
    input_vpp_measured.append(measured_vpp_input)

# Generate Bode plot
gain = 20 * np.log10(np.array(output_vpp) / input_vpp_measured)
plt.semilogx(frequencies/1e3, gain)
plt.xlabel('Frequency (kHz)')
plt.ylabel('Gain (dB)')
plt.title('Bode Plot')
plt.grid(which='both', axis='both')
plt.show()
