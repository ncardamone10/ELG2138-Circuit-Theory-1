import pyvisa
import time
import numpy as np
import os
from pyvisa import VisaIOError
from datetime import datetime
#from msox2000aSeriesScopeDriver import Scope
# scope = Scope('USB0::2391::6041::MY55280378::INSTR')
class Scope:
    def __init__(self, visa_address='USB0::2391::6041::MY55280378::INSTR'):
        # Connection
        try:
            self.address = visa_address
            self.rm = pyvisa.ResourceManager()
            self.scope = self.rm.open_resource(self.address,  write_termination = '\n',read_termination='\n')
            self.identity = self.scope.query("*IDN?")
            print('Scope VISA Interface Opened (yay, this only took forever to get here)')
            print(f'Connected to {self.identity}')
        except VisaIOError as e:
            print(f"Error initializing the oscilloscope: {e}")
            raise
        # self.rm = pyvisa.ResourceManager()
        # self.scope = self.rm.open_resource(visa_address)

        # Overall settings
        self.identity = None
        self.address = None
        self.scope_mode = "STOP"
        self.time_base = 1e-3
        self.time_scroll = 0
        self.time_base_mode = "NORMAL"
        self.vertical_divisions = 9
        self.horizontal_divisions = 11
        self.trigger_settings = {
            'channel': 1,
            'level': 1,
            'type': "EDGE",
            'slope': "POSITIVE"
        }

        # Channel settings
        self.channels = [
            {
                'enabled': False,
                'off_screen_voltage': False,
                'off_screen_time': False,
                'probe_attenuation': None,
                'coupling': 'DC',
                'vertical_divisions': None,
                'bias': None,
                'measurements': {}
            },
            {
                'enabled': False,
                'off_screen_voltage': False,
                'off_screen_time': False,
                'probe_attenuation': None,
                'coupling': 'DC',
                'vertical_divisions': None,
                'bias': None,
                'measurements': {}
            }
        ]

        # Builtin function generator settings
        self.function_generator = {
            'enabled': False,
            'waveform': None,
            'frequency': None,
            'amplitude': None,
            'offset': None,
            'output_load': 'high z'
        }

        # Math channel settings
        self.math_channel = {
            'enabled': False,
            'operation': None,
            'channels': [],
            'measurements': {}
        }

    # Overall settings getters and setters
    # def get_scope_mode(self):
    #     try:
    #         #self.scope.write(":STATus?")
    #         self.scope_mode = self.scope.query("*STATus?")
    #         return self.scope_mode
    #     except VisaIOError as e:
    #         print(f"Error getting scope mode: {e}")


    def set_scope_mode(self, mode):
        try:
            if mode.upper() == "RUN":
                self.scope.write(":RUN")
            elif mode.upper() == "STOP":
                self.scope.write(":STOP")
            elif mode.upper() == "SINGLE":
                self.scope.write(":SINGle")
            else:
                raise ValueError(f"Invalid mode: {mode}")
            # # Check to see if this is done
            # scopeMode = self.get_scope_mode()
            # if scopeMode != mode:
            #     print(f'SCOPE MODE NOT SET CORRECTLY. SCOPE MODE: {scopeMode} SHOULD BE: {mode}')
        except VisaIOError as e:
            print(f"Error setting scope mode to {mode}: {e}")
            
    def get_time_base(self):
        try:
            self.time_base = float(self.scope.query(":TIMebase:SCALe?"))
            return self.time_base
        except VisaIOError as e:
            print(f"Error getting time base: {e}")

    def set_time_base(self, time_base):
        try:
            self.scope.write(f":TIMebase:SCALe {time_base}")
            # Check if done correctly
            timeBase = self.get_time_base()
            if timeBase != time_base:
                print(f'ERROR SETTING TIME BASE, FROM SCOPE: f{timeBase}, SHOULD BE: {time_base}')
        except VisaIOError as e:
            print(f"Error setting time base: {e}")

    def get_time_scroll(self):
        try:
            self.time_scroll =  float(self.scope.query(":TIMebase:POSition?"))
            return self.time_scroll
        except VisaIOError as e:
            print(f"Error getting time scroll: {e}")

    def set_time_scroll(self, time_scroll):
        try:
            self.scope.write(f":TIMebase:POSition {time_scroll}")
            timeScroll = self.get_time_scroll()
            if timeScroll != time_scroll:
                print("TIME SCROLL NOT SET CORRECTLY")
        except VisaIOError as e:
            print(f"Error setting time scroll: {e}")

    def get_time_base_mode(self):
        try:
            self.scope_mode = self.scope.query(":TIMebase:MODE?").strip() # Save the mode to self.scope_mode
            return self.scope_mode
        except VisaIOError as e:
            print(f"Error getting time base mode: {e}")

    def set_time_base_mode(self, mode):
        try:
            # Check if the provided mode is one of the valid options
            valid_modes = ["MAIN", "XY", "WIND", "ROLL"]
            if mode.upper() not in valid_modes:
                raise ValueError(f"Invalid time base mode: {mode}. Valid modes are {', '.join(valid_modes)}")

            # Send the SCPI command to set the time base mode
            self.scope.write(f":TIMebase:MODE {mode.upper()}")

        except VisaIOError as e:
            print(f"Error setting time base mode to {mode}: {e}")

    def get_vertical_divisions(self, channel):
        try:
            command = f":CHANnel{channel}:SCALe?"
            divisions = float(self.scope.query(command))
            # Save the result to self.channels
            self.channels[channel - 1]['vertical_divisions'] = divisions
            return divisions
        except VisaIOError as e:
            print(f"Error getting vertical divisions for channel {channel}: {e}")

    def set_vertical_divisions(self, divisions, channel):
        try:
            command = f":CHANnel{channel}:SCALe {divisions}"
            self.scope.write(command)
            # Check if divisions were set correctly
            actual_divisions = self.get_vertical_divisions(channel)
            if actual_divisions != divisions:
                print(f"Error setting vertical divisions for channel {channel}")
        except VisaIOError as e:
            print(f"Error setting vertical divisions for channel {channel}: {e}")

    def get_trigger_settings(self):
        try:
            # Query each trigger setting
            channel_response = self.scope.query(":TRIGger:EDGE:SOURce?").strip()
            # Extract the channel number from the response
            channel = int(channel_response.split('CHAN')[-1]) if 'CHAN' in channel_response else None

            level = float(self.scope.query(":TRIGger:EDGE:LEVel?").strip())
            slope = self.scope.query(":TRIGger:EDGE:SLOPe?").strip()

            # As the 'type' is not directly queried, you may consider omitting it or setting a default
            type = "EDGE"  # Assuming 'EDGE' as the default type

            # Aggregate the settings into a dictionary
            self.trigger_settings = {
                'channel': channel,
                'level': level,
                'type': type,
                'slope': slope
            }

            return self.trigger_settings

        except VisaIOError as e:
            print(f"Error getting trigger settings: {e}")
            return None

    def set_trigger_settings(self, channel, level, type, slope):
        try:
            # Validate channel
            if channel not in [1, 2]:
                raise ValueError("Channel must be 1 or 2")

            # Validate level
            if not (-12 <= level <= 12):
                raise ValueError("Level must be between -12 and 12")

            # Validate type
            if type.upper() != "EDGE":
                raise ValueError("Type must be 'EDGE'")

            # Validate slope
            if slope.upper() not in ["POS", "NEG"]:
                raise ValueError("Slope must be 'POS' or 'NEG'")

            # Set trigger settings
            self.scope.write(f":TRIGger:EDGE:SOURce CHAN{channel}")
            self.scope.write(f":TRIGger:EDGE:LEVel {level}")
            self.scope.write(f":TRIGger:EDGE:SLOPe {slope}")

            # Error checking
            actual_channel = int(self.scope.query(":TRIGger:EDGE:SOURce?").strip().split('CHAN')[-1])
            actual_level = float(self.scope.query(":TRIGger:EDGE:LEVel?"))
            actual_slope = self.scope.query(":TRIGger:EDGE:SLOPe?").strip()

            if actual_channel != channel or actual_level != level or actual_slope.upper() != slope.upper():
                print(f"Error: Trigger settings not set correctly. "
                    f"Actual settings - Channel: {actual_channel}, Level: {actual_level}, Slope: {actual_slope}")

        except VisaIOError as e:
            print(f"Error setting trigger settings: {e}")
        except ValueError as e:
            print(f"Invalid parameter: {e}")

    def get_channel_settings(self, channel_number):
        if channel_number not in [1, 2]:
            raise ValueError("Channel number must be 1 or 2")

        try:
            settings = {}

            # Check if the channel is enabled
            display_status = self.scope.query(f":CHANnel{channel_number}:DISPlay?")
            settings['enabled'] = display_status.strip() == '1'

            # Get probe attenuation
            probe_attenuation = self.scope.query(f":CHANnel{channel_number}:PROBe?")
            settings['probe_attenuation'] = probe_attenuation.strip()

            # Get coupling
            coupling = self.scope.query(f":CHANnel{channel_number}:COUPling?")
            settings['coupling'] = coupling.strip()

            # Add more settings as needed, such as vertical_divisions, bias, etc.

            return settings

        except VisaIOError as e:
            print(f"Error getting settings for channel {channel_number}: {e}")
            return None

    def set_channel_settings(self, channel_number, settings):
        if channel_number not in [1, 2]:
            raise ValueError("Channel number must be 1 or 2")

        try:
            # Check and set each setting
            if 'enabled' in settings:
                self.scope.write(f":CHANnel{channel_number}:DISPlay {'1' if settings['enabled'] else '0'}")

            if 'probe_attenuation' in settings:
                self.scope.write(f":CHANnel{channel_number}:PROBe {settings['probe_attenuation']}")

            if 'coupling' in settings:
                self.scope.write(f":CHANnel{channel_number}:COUPling {settings['coupling']}")

            # Add more settings as needed

        except VisaIOError as e:
            print(f"Error setting channel {channel_number} settings: {e}")

    # Function generator getters and setters
    def get_function_generator_settings(self):
        try:
            settings = {}

            # Assuming your oscilloscope uses these standard SCPI commands
            settings['waveform'] = self.scope.query("FUNCtion:WAVeform?").strip()
            settings['frequency'] = float(self.scope.query("FUNCtion:FREQuency?").strip())
            settings['amplitude'] = float(self.scope.query("FUNCtion:VOLTage:AMPLitude?").strip())
            settings['offset'] = float(self.scope.query("FUNCtion:VOLTage:OFFSet?").strip())
            settings['output_load'] = self.scope.query("FUNCtion:OUTPut:LOAD?").strip()
            settings['enabled'] = self.scope.query("FUNCtion:OUTPut:STATe?").strip() == '1'

            self.function_generator = settings
            return self.function_generator

        except VisaIOError as e:
            print(f"Error getting function generator settings: {e}")
            return None

    def set_function_generator_settings(self, settings):
        try:
            # Waveform type
            if 'waveform' in settings:
                self.scope.write(f":WGEN:FUNC {settings['waveform']}")

            # Frequency
            if 'frequency' in settings:
                self.scope.write(f":WGEN:FREQ {settings['frequency']}")

            # Amplitude
            if 'amplitude' in settings:
                self.scope.write(f":WGEN:VOLT {settings['amplitude']}")

            # High voltage level
            if 'voltage_high' in settings:
                self.scope.write(f":WGEN:VOLT:HIGH {settings['voltage_high']}")

            # Low voltage level
            if 'voltage_low' in settings:
                self.scope.write(f":WGEN:VOLT:LOW {settings['voltage_low']}")

            # Offset voltage
            if 'offset' in settings:
                self.scope.write(f":WGEN:VOLT:OFFS {settings['offset']}")

            # Output on/off
            if 'output' in settings:
                output_state = 'ON' if settings['output'] else 'OFF'
                self.scope.write(f":WGEN:OUTP {output_state}")

            # Output load
            if 'output_load' in settings:
                self.scope.write(f":WGEN:OUTP:LOAD {settings['output_load']}")

            # Add more settings as needed for modulation and other features

        except VisaIOError as e:
            print(f"Error setting function generator settings: {e}")
    
    def measure_vpp(self, channel):
        """Measure peak-to-peak voltage on a specific channel."""
        return float(self.scope.query(f":MEASure:VPP? CHANnel{channel}"))

    def measure_vmax(self, channel):
        """Measure maximum voltage on a specific channel."""
        return float(self.scope.query(f":MEASure:VMAX? CHANnel{channel}"))

    def measure_vmin(self, channel):
        """Measure minimum voltage on a specific channel."""
        return float(self.scope.query(f":MEASure:VMIN? CHANnel{channel}"))

    def measure_vamplitude(self, channel):
        """Measure amplitude on a specific channel."""
        return float(self.scope.query(f":MEASure:VAMPLitude? CHANnel{channel}"))

    def measure_vaverage_display(self, channel):
        """Measure average voltage over the full screen on a specific channel."""
        return float(self.scope.query(f":MEASure:VAVerage? DISPlay, CHANnel{channel}"))

    def measure_vrms_cycle_ac(self, channel):
        """Measure AC RMS over a cycle on a specific channel."""
        return float(self.scope.query(f":MEASure:VRMS? CYCLe,AC, CHANnel{channel}"))

    def measure_vrms_display_ac(self, channel):
        """Measure AC RMS over the full screen on a specific channel."""
        return float(self.scope.query(f":MEASure:VRMS? DISPlay,AC, CHANnel{channel}"))

    def measure_period(self, channel):
        """Measure the period of the waveform on a specific channel."""
        return float(self.scope.query(f":MEASure:PERiod? CHANnel{channel}"))

    def measure_frequency(self, channel):
        """Measure the frequency of the waveform on a specific channel."""
        return float(self.scope.query(f":MEASure:FREQuency? CHANnel{channel}"))

    def measure_positive_width(self, channel):
        """Measure the positive pulse width on a specific channel."""
        return float(self.scope.query(f":MEASure:PWIDth? CHANnel{channel}"))

    def measure_negative_width(self, channel):
        """Measure the negative pulse width on a specific channel."""
        return float(self.scope.query(f":MEASure:NWIDth? CHANnel{channel}"))

    def measure_duty_cycle(self, channel):
        """Measure the positive duty cycle on a specific channel."""
        return float(self.scope.query(f":MEASure:DUTYcycle? CHANnel{channel}"))

    def measure_rise_time(self, channel):
        """Measure the rise time on a specific channel."""
        return float(self.scope.query(f":MEASure:RISetime? CHANnel{channel}"))

    def measure_fall_time(self, channel):
        """Measure the fall time on a specific channel."""
        return float(self.scope.query(f":MEASure:FALLtime? CHANnel{channel}"))
    # Math channel getters and setters
    # def get_math_channel_settings(self):
    #     pass

    # def set_math_channel_settings(self, settings):
    #     pass

    def auto_scale(self):
        try:
            # Send the command to the oscilloscope to activate auto-scaling
            self.scope.write(":AUToscale")

            # Optional: You can add a delay here to allow the oscilloscope time to adjust
            # import time
            time.sleep(2)  # Delay for 2 seconds (adjust as needed)

            print("Auto-scaling performed on the oscilloscope.")

        except VisaIOError as e:
            print(f"Error during auto-scaling: {e}")

    def default_setup(self):
        try:
            # Send the command to the oscilloscope to reset to default settings
            self.scope.write(":SYSTem:PRESet")

            # Optional: Add a delay to allow the oscilloscope time to reset
            # import time
            # time.sleep(2)  # Adjust the delay time as necessary

            print("Oscilloscope reset to default settings.")

        except VisaIOError as e:
            print(f"Error during default setup: {e}")

    def grab_data(self, channel):
        """
        Fetches waveform data from the specified channel of the oscilloscope.

        Args:
            channel (int): The oscilloscope channel to grab data from.

        Returns:
            np.array: The waveform data as a numpy array.
        """
        try:
            # Set the source to the specified channel and the format to ASCII
            self.scope.write(f":WAVeform:SOURce CHANnel{channel}")
            self.scope.write(":WAVeform:FORMat ASCII")

            # Fetch the data
            raw_data = self.scope.query(":WAVeform:DATA?")
            
            # Parse the header to find where the numerical data begins
            header_len = int(raw_data[1])  # Get the length of the length field
            data_start = 2 + header_len  # Calculate the starting index of the data

            # Extract and convert the data
            waveform_data = np.array([float(val) for val in raw_data[data_start:].split(',')])

            return waveform_data

        except VisaIOError as e:
            print(f"Error fetching data from the oscilloscope: {e}")
            return None



      # Doesn't work (yet)  
    # def get_screenshot(self):
    #     """
    #     Fetches a screenshot from the oscilloscope and saves it as a PNG file.
    #     """
    #     try:
    #         # Format the current time into a string suitable for a filename
    #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #         filename = f"oscilloscope_screenshot_{timestamp}.png"

    #         # Save the current timeout
    #         original_timeout = self.scope.timeout
    #         self.scope.timeout = 10000  # Increase timeout for the screenshot command

    #         # Set the oscilloscope to output the screen data in PNG format
    #         self.scope.write(":HARDcopy:INKSaver OFF")  # Ensure ink saver is off
    #         screenshot_data = self.scope.query_binary_values(':DISPlay:DATA? PNG,SCReen,1,NORMal', datatype='B', header_fmt='ieee', container=bytes)

    #         # Reset the timeout to its original value
    #         self.scope.timeout = original_timeout

    #         # Validate and save the data to a file
    #         if screenshot_data:
    #             with open(filename, "wb") as file:
    #                 file.write(screenshot_data)
    #             print(f"Screenshot saved to {filename}")
    #         else:
    #             print("No data received from oscilloscope.")

    #     except VisaIOError as e:
    #         print(f"Error fetching screenshot from the oscilloscope: {e}")
    #     finally:
    #         # Reset the timeout to its original value
    #         self.scope.timeout = original_timeout
    