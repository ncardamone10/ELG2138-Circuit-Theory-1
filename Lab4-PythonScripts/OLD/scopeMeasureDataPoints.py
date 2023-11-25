import pyvisa
import matplotlib.pyplot as plt
import numpy as np

def fetch_and_plot_oscilloscope_data(visa_address):
    try:
        # Connect to the instrument
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource(visa_address)

        # Prepare the scope to send data
        scope.write(":WAVeform:SOURce CHANnel1")
        scope.write(":WAVeform:FORMat ASCII")

        # Fetch the data
        raw_data = scope.query(":WAVeform:DATA?")
        
        # Parse the header to find where the numerical data begins
        header_len = int(raw_data[1])  # Get the length of the length field
        data_start = 2 + header_len  # Calculate the starting index of the data

        # Extract and convert the data
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
visa_address = 'USB0::2391::6041::MY55280378::INSTR'

# Fetch and plot the data
fetch_and_plot_oscilloscope_data(visa_address)
