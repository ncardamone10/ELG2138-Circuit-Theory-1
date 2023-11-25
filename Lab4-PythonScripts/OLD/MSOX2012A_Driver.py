import pyvisa
import time

class KeysightScopeDriver:
    def __init__(self, visa_address):
        self.rm = pyvisa.ResourceManager()
        self.scope = self.rm.open_resource(visa_address)
        self.scope.timeout = 20000  # Set a default timeout (in milliseconds)

    def set_horizontal_scale(self, scale):
        """Set the horizontal scale of the oscilloscope."""
        self.scope.write(f":TIMebase:SCALe {scale}")

    def enable_function_generator(self, frequency, amplitude):
        """Enable the function generator with the given frequency and amplitude."""
        self.scope.write(":WGEN:OUTPUT ON")
        self.scope.write(f":WGEN:FREQuency {frequency}")
        self.scope.write(f":WGEN:VOLTage {amplitude}")

    def disable_function_generator(self):
        """Disable the function generator."""
        self.scope.write(":WGEN:OUTPUT OFF")

    def set_vertical_scale(self, channel, scale):
        """Set the vertical scale for a specified channel."""
        self.scope.write(f":CHANnel{channel}:SCALe {scale}")

    def measure_voltage_pp(self, channel):
        """Measure the peak-to-peak voltage on a specified channel."""
        return float(self.scope.query(f":MEASure:VPP? CHANnel{channel}"))

    def close(self):
        """Close the VISA connection."""
        self.scope.close()

# Example usage:
visa_address = "USB0::0x0957::0x1799::MY55280380::0::INSTR"
scope = KeysightScopeDriver(visa_address)

try:
    # Set horizontal scale to 1ms/div
    scope.set_horizontal_scale(0.001)  

    # Enable function generator with 1 kHz frequency and 1 Vpp amplitude
    scope.enable_function_generator(1000, 1) 

    # Measure peak-to-peak voltage on Channel 1
    vpp = scope.measure_voltage_pp(1)
    print(f"Peak-to-Peak Voltage on Channel 1: {vpp} V")

    # Disable function generator
    scope.disable_function_generator()

finally:
    scope.close()  # Ensure the session is closed properly
