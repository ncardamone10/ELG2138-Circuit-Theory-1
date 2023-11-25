# To create virtual env for python
# python -m venv myenv

# activate virtual env
# myenv\Scripts\activate

# to install visa library
# pip install visa
# pip install pyvisa-py
# pip install pyusb
# pip install --upgrade pyvisa-py



#import visa
import pyvisa as visa


# Define the VISA resource string for your USB-connected scope.
# You can typically use 'USB0::0x####::0x####::INSTR', where #### represents the USB interface and device IDs.
#visa_resource_string = 'USB0::0x0957::0x1799::MY55280380::0::INSTR'
# visa_resource_string = 'USB0::0x0957::0x1799::MY55280380::0::INSTR'
visa_resource_string = "USB0::2391::6041::MY55280396::0::INSTR"
# Create a VISA resource manager object.
rm = visa.ResourceManager()

try:
    # Open communication with the instrument.
    scope = rm.open_resource(visa_resource_string)

    # Send a command to query the instrument identification.
    scope.write('*IDN?')

    # Read and display the response from the instrument.
    idn_response = scope.read()
    print('Instrument Identification:', idn_response.strip())
        # Close the communication with the instrument.
    scope.close()
except visa.VisaIOError as e:
    print('Error communicating with the instrument:', e)
    

