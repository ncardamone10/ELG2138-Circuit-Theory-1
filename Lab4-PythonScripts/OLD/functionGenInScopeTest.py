import pyvisa

def setup_function_generator(visa_address):
    try:
        # Connect to the instrument
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource(visa_address)

        # Set the function generator
        # Frequency to 1 kHz
        scope.write(":WGEN:FREQuency 5000")

        # Set the amplitude to 1 Vpp
        scope.write(":WGEN:VOLTage 1")

        # Turn on the function generator
        scope.write(":WGEN:OUTPut ON")

        print("Function generator is set to 1 kHz, 1 Vpp, and turned on.")
    except Exception as e:
        print(f"An error occurred: {e}")

# VISA address of your Keysight scope
# visa_address = "USB0::0x0957::0x1799::MY55280380::0::INSTR"
visa_address = "USB0::2391::6041::MY55280370::INSTR"
# Call the function to setup the function generator
setup_function_generator(visa_address)
