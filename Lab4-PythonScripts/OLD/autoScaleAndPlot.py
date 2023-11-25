# import pyvisa
# import matplotlib.pyplot as plt
# import numpy as np
# import time

# def setup_and_plot_waveform(visa_address):
#     try:
#         # Connect to the instrument
#         rm = pyvisa.ResourceManager()
#         scope = rm.open_resource(visa_address)

#         # Reset the time base to a known, broader setting
#         # This value might need adjustment
#         scope.write(":TIMebase:SCALe 0.001")  # For example, 10 ms/div
#         time.sleep(1)  # Wait for the scope to apply the setting

#         # Query the frequency and amplitude of the waveform
#         frequency = float(scope.query(":MEASure:FREQuency?").strip())
#         vpp = float(scope.query(":MEASure:VPP?").strip())

#         # Adjust the time base and vertical scale
#         time_per_div = 8 / (10 * frequency)  # Adjusted for a wider view
#         volts_per_div = vpp / 32              # To fill 8 vertical divisions

#         # Set the oscilloscope time base and vertical scale
#         scope.write(f":TIMebase:SCALe {time_per_div}")
#         scope.write(f":CHANnel1:SCALe {volts_per_div}")

#         # Add a delay to allow the oscilloscope to settle
#         time.sleep(0.5)  # Adjust based on your oscilloscope

#         # Prepare the scope to send data
#         scope.write(":WAVeform:SOURce CHANnel1")
#         scope.write(":WAVeform:FORMat ASCII")

#         # Fetch the data
#         raw_data = scope.query(":WAVeform:DATA?")
        
#         # Process the header and data
#         header_len = int(raw_data[1])  # Length of the length field
#         data_start = 2 + header_len    # Start of the data
#         waveform_data = np.array([float(val) for val in raw_data[data_start:].split(',')])

#         # Plot the data
#         plt.plot(waveform_data)
#         plt.title("Oscilloscope Channel 1 Waveform")
#         plt.xlabel("Time")
#         plt.ylabel("Voltage")
#         plt.grid(True)
#         plt.show()

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # VISA address of your Keysight scope
# # visa_address = "USB0::0x0957::0x1799::MY55280380::0::INSTR"
# #visa_address = "USB0::2391::6041::MY55280396::0::INSTR"
# visa_address = "USB0::2391::6041::MY55280370::INSTR"

# # Setup oscilloscope and plot the data
# setup_and_plot_waveform(visa_address)

import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import time

def setup_and_plot_waveform(visa_address):
    try:
        # Connect to the instrument
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource(visa_address)

        # Use the auto-scale feature of the oscilloscope
        scope.write(":AUToscale")
        # Add a delay to allow the oscilloscope to complete auto-scaling
        time.sleep(2)  # Adjust this based on your oscilloscope's response time

        # Prepare the scope to send data
        scope.write(":WAVeform:SOURce CHANnel1")
        scope.write(":WAVeform:FORMat ASCII")

        # Fetch the data
        raw_data = scope.query(":WAVeform:DATA?")
        
        # Process the header and data
        header_len = int(raw_data[1])  # Length of the length field
        data_start = 2 + header_len    # Start of the data
        waveform_data = np.array([float(val) for val in raw_data[data_start:].split(',')])

        # Plot the data
        plt.plot(waveform_data)
        plt.title("Oscilloscope Channel 1 Waveform")
        plt.xlabel("Time")
        plt.ylabel("Voltage")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

# VISA address of your Keysight scope
# visa_address = "USB0::0x0957::0x1799::MY55280380::0::INSTR"
# visa_address = "USB0::2391::6041::MY55280396::0::INSTR"
visa_address = "USB0::2391::6041::MY55280370::INSTR"

# Setup oscilloscope and plot the data
setup_and_plot_waveform(visa_address)
