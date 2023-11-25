import pyvisa
import matplotlib.pyplot as plt
import numpy as np

# Initialize communication with the oscilloscope
rm = pyvisa.ResourceManager()
scope = rm.open_resource("USB0::2391::6041::MY55280396::0::INSTR")

# Function to set horizontal divisions (time base scale)
def set_timebase_scale(seconds_per_div):
    scope.write(":TIMebase:SCALe {}".format(seconds_per_div))

# Function to set vertical scale for a channel
def set_channel_scale(channel, volts_per_div):
    scope.write(":CHANnel{}:SCALe {}".format(channel, volts_per_div))

# Function to set the trigger type
def set_trigger_type(trigger_type):
    scope.write(":TRIGger:MODE {}".format(trigger_type))

# Function to set the channel attenuation
def set_channel_attenuation(channel, attenuation):
    scope.write(":CHANnel{}:PROBe {}".format(channel, attenuation))

# Function to reset channel offset
def reset_channel_offset(channel):
    scope.write(":CHANnel{}:OFFSet 0".format(channel))

# Function to reset horizontal offset
def reset_horizontal_offset():
    scope.write(":TIMebase:POSition 0")

# Function to perform measurements
def measure_parameter(parameter, channel):
    result = scope.query(":MEASure:{}? CHANnel{}".format(parameter, channel))
    return result.strip()

# Function to get waveform data
def get_waveform_data(channel):
    scope.write(":WAVeform:SOURce CHANnel{}".format(channel))
    scope.write(":WAVeform:FORMat ASCII")
    raw_data = scope.query(":WAVeform:DATA?")
    data_points = np.fromstring(raw_data, sep=',')
    time_step = float(scope.query(":WAVeform:XINCrement?"))
    return data_points * time_step

# Function to perform RMS voltage measurement
def measure_rms_voltage(channel):
    command = ":MEASure:VRMS? DISPLAY,CHANnel{}".format(channel)
    rms_voltage = scope.query(command).strip()
    return rms_voltage



# Example usage
set_timebase_scale(0.001)  # Set horizontal divisions to 1ms/div
set_channel_scale(1, 0.1)  # Set channel 1 to 100mV/div
set_trigger_type('EDGE')   # Set trigger to edge trigger
set_channel_attenuation(1, 10) # Set channel 1 attenuation to 10:1
reset_channel_offset(1)    # Reset channel 1 offset to 0
reset_channel_offset(2)    # Reset channel 2 offset to 0
reset_horizontal_offset()  # Reset horizontal offset to 0

# Get measurements
voltage_measurement = measure_rms_voltage(1)
frequency_measurement = measure_parameter('FREQuency', 1)
rise_time_measurement = measure_parameter('RISetime', 1)
fall_time_measurement = measure_parameter('FALLtime', 1)

# Get and plot waveform data
waveform_data = get_waveform_data(1)
plt.plot(waveform_data)
plt.title('Oscilloscope Channel 1 Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.show()
