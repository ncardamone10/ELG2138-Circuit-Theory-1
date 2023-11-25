import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time

# Doesn't work


def perform_bode_plot_analysis(visa_address, start_freq=100, end_freq=100000, points=50):  # Reduced points for testing
    try:
        # Setup connection
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource(visa_address)

        # Increase the timeout to 20 seconds
        scope.timeout = 20000

        # Frequency sweep parameters
        frequencies = np.logspace(np.log10(start_freq), np.log10(end_freq), num=points)

        # Data lists
        magnitudes = []
        phases = []

        # Set horizontal scale for clear waveform display
        initial_freq = start_freq
        time_base = 1 / (4 * initial_freq)  # Four cycles per division
        scope.write(f":TIMebase:SCALe {time_base}")

        # Set vertical scale for Channel 1 based on initial measurement
        scope.write(":WGEN:FREQuency {initial_freq}")
        time.sleep(0.5)  # Wait for stabilization
        input_voltage_pp = float(scope.query(":MEASure:VPP? CHANnel1"))
        ch1_scale = input_voltage_pp / 8  # Fit waveform in 8 divisions
        scope.write(f":CHANnel1:SCALe {ch1_scale}")

        for freq in frequencies:
            # Update the function generator frequency
            scope.write(f":WGEN:FREQuency {freq}")
            time.sleep(1)  # Wait for the scope and circuit to stabilize

            # Update the time base for the new frequency
            time_base = 1 / (4 * freq)  # Four cycles per division
            scope.write(f":TIMebase:SCALe {time_base}")
            time.sleep(1)  # Additional delay after setting frequency and time base

            # Dynamically adjust the vertical scale for Channel 2
            output_voltage_pp = float(scope.query(":MEASure:VPP? CHANnel2"))
            ch2_scale = output_voltage_pp / 8  # Fit waveform in 8 divisions
            scope.write(f":CHANnel2:SCALe {ch2_scale}")

            # Measure response
            input_voltage = float(scope.query(":MEASure:VPP? CHANnel1"))
            output_voltage = float(scope.query(":MEASure:VPP? CHANnel2"))
            phase_difference = float(scope.query(":MEASure:PHASedifference? CHANnel1,CHANnel2"))

            # Calculate magnitude in dB and phase
            magnitude_db = 20 * np.log10(output_voltage / input_voltage)
            magnitudes.append(magnitude_db)
            phases.append(phase_difference)

        # Plot Bode Plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ax1.semilogx(frequencies, magnitudes, '-b')
        ax1.set_title('Bode Plot of the Circuit')
        ax1.set_ylabel('Magnitude (dB)')
        ax1.grid(True)

        ax2.semilogx(frequencies, phases, '-r')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Phase (Degrees)')
        ax2.grid(True)

        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

# VISA address of your Keysight scope
visa_address = "USB0::0x0957::0x1799::MY55280380::0::INSTR"

# Perform Bode plot analysis
perform_bode_plot_analysis(visa_address)
