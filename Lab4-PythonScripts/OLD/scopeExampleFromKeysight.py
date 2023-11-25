# -*- coding: utf-8 -*-
# DO NOT CHANGE ABOVE LINE

'''
# Python for Test and Measurement
#
# Requires VISA installed on Control PC
# 'keysight.com/find/iosuite'
# Requires PyVISA to use VISA in Python
# 'http://PyVISA.sourceforge.net/PyVISA/'

# =============================================================================
# Copyright © 2019 Keysight Technologies Inc. All rights reserved.
#
# You have a royalty-free right to use, modify, reproduce and distribute this
# example files (and/or any modified version) in any way you find useful,
# provided that you agree that Keysight has no warranty, obligations or
# liability for any Sample Application Files.
#
# =============================================================================

# =============================================================================
# Intro, general comments, and instructions
# =============================================================================

This example program is provided as-is and without support.  Keysight is not
responsible for modifications.

Tested with:

    Keysight IO Libraries Suite 18.1.24715.0
    Anaconda Python 2.7.17 64-bit
    PyVISA 1.9.0
    Windows 10 Enterprise, 64-bit
    InfiniiVision MSOX3104T with 7.30.2019051434 firmware

Compatibility notes:

    This script is for use with Keysight (and Agilent) InfiniiVision 2000,
    3000A, 3000T, 4000, and 6000 X-series oscilloscopes with an available
    Measurement Trend math function.

    Licensing requirements for Measurement Trends:
        - 2000 X-series models require a DSOX2PLUS license
        - 2000 X-series models purchased 3/5/18 or later either shipped with a
          DSOX2PLUS license or are entitled to one (contact support as needed)
        - 3000A X-series models require a DSOX3ADVMATH license
        - 3000T, 4000, and 6000 X-series models do not require a license

Description of functionality:

    This script sets up the oscilloscope with a Measurement Trend function,
    which plots the value of select cycle-by-cycle measurements versus time.
    It imports the measurement values in the trend waveform into a "trends"
    array and writes the corresponding time values to a "time_axis" array.

    These values can optionally be saved to a CSV file and/or a Numpy binary
    file at the end of each run.  Each file has a unique file name derived
    from the date and time of the run.

    The CSV and binary files can optionally be loaded back into Python.

    Example application:
        A clock with a 30% duty cycle is toggling between two frequencies (2.2
        kHz and 2.8 kHz) twice per second.  We want to trigger on the frequency
        change and measure the frequency of every captured cycle before and
        after the trigger.  We use the following User Inputs:
            TIMESCALE = 0.005  # (s/div)
            MEAS = ':MEASure:FREQuency CHANnel1'
            FREQUENCY1 = 2200  # Use an integer in Hz
            FREQUENCY2 = 2800  # Use an integer in Hz
            DUTY_CYCLE = '30%'  # Used to calculate Pulse Width trigger values
            TRIGGER_ON = 'FREQUENCY2'
            MIN_TIME_BETWEEN_FREQS = 0.5  # (seconds)

Getting started:

    1.  Set up your Python 2.7 environment, using the following instructions as
        needed:
        https://www.dropbox.com/s/zrf9x11parjzuke/Python_2-7.pdf?dl=1

    2.  Install the Quantiphy package from a Python command prompt:
        pip install quantiphy

    3.  Open Keysight Connection Expert.  Find the oscilloscope’s VISA address
        (e.g. ‘USB0::0x2A8D::0x1770::MY56311141::0::INSTR’) and copy it to the
        clipboard

    4.  Find the SCOPE_VISA_ADDRESS constant in the 'User Inputs' section of
        the script and paste the address from step 3

    5.  Review the comments for the remaining constants under 'User Inputs'
        and define the values as needed for your application.

    6.  Run the script and observe the output in the console window

    7.  ALWAYS DO SOME TEST RUNS before making important measurements to ensure
        you are getting the data you need!

'''

# =============================================================================
# Import Python modules
# =============================================================================

# Import python modules - Not all of these are used in this program; provided
# for reference
import sys
import visa  # PyVisa info @ http://PyVisa.readthedocs.io/en/stable/
import time
import numpy as np
import re
from quantiphy import Quantity  # pip install quantiphy
import os

# =============================================================================
# Initialize values (some to be overwritten by User Inputs below)
# =============================================================================

VERBOSE_MODE = True
START_FROM_RESET = True
IMPORT_SAVED_FILES = False
trends = False
FREQUENCY1 = 0
FREQUENCY2 = 0
DUTY_CYCLE = '50%'
trig_on_freq_change = False

# =============================================================================
# User Inputs (used with every run)
# =============================================================================

# Set VERBOSE_MODE = False for a more concise console output.  Comment this
# line to display additional info (useful for debug):
#VERBOSE_MODE = False

# Instrument VISA address:
SCOPE_VISA_ADDRESS = 'USB0::0x0957::0x1799::MY55280380::0::INSTR'  # MSOX3104T

# I/O timeout in milliseconds:
GENERAL_TIMEOUT = 6000

# Number of waveforms to acquire and transfer:
NUMBER_WAVEFORMS = 5

# Set waveform data format to ASCii (for demo) or WORD (recommended):
WAVEFORM_FORMAT = 'WORD'
#WAVEFORM_FORMAT = 'ASCii'

# Enter a delay in seconds to wait between queries when polling for run status.
# Shorter values provide more accurate time tags but use more CPU resources.
POLLING_INTERVAL = 0.5  # (s)

# Set format for output file to save waveform data:
OUTPUT_FILE = 'CSV'  # CSV, BINARY, BOTH, or NONE

# Load data from output file(s) back into Python:
#IMPORT_SAVED_FILES = True

# If one or more CSV files are saved, open the last one:
OPEN_CSV_FILE = True

# Define save location:
DIRECTORY = 'C:\\Users\\ncard\OneDrive - University of Ottawa\\University Archive\\Masters\\Circuit Theory TA\\Scope USB Connection Testing -- Lab 4'

# Comment this to reset the scope and perform the setup under initialize():
#START_FROM_RESET = False

# =============================================================================
# User Inputs (used only when START_FROM_RESET = True)
# =============================================================================

# Set the vertical scale:
VERTICAL_SCALE = 1  # (V/div)
# Set the horizontal scale.  Note this directly impacts measurement resolution
# and accuracy.  Generally, smaller timescales produce fewer measurements that
# are more accurate, whereas larger timescales produce more measurements that
# are less accurate.  No logic has been implemented to report the resolution or
# accuracy to the user.
TIMESCALE = 0.005  # (s/div)

# Define the measurement for the measurement trend:
#MEAS = ':MEASure:VAVerage CYCLe, CHANnel1'
#MEAS = ':MEASure:VRMS CYCLe,AC,CHANnel1'
#MEAS = ':MEASure:VRATio CYCLe,CHANnel1,CHANnel3'  # TODO: Deal with 2-ch meas
#MEAS = ':MEASure:PERiod CHANnel1'
MEAS = ':MEASure:FREQuency CHANnel1'
#MEAS = ':MEASure:PWIDth CHANnel1'
#MEAS = ':MEASure:DUTYcycle CHANnel1'
#MEAS = ':MEASure:RISetime CHANnel1'
#MEAS = ':MEASure:FALLtime CHANnel1'

# To trigger on a change between two clock frequencies, define the values here.
# Or, comment these lines to default to a simple edge trigger:
FREQUENCY1 = 2200  # Use an integer in Hz
FREQUENCY2 = 2800  # Use an integer in Hz
DUTY_CYCLE = '30%'  # Used to calculate Pulse Width trigger values
# Define whether to trigger when FREQUENCY1 or FREQUENCY2 is detected:
#TRIGGER_ON = 'FREQUENCY1'
TRIGGER_ON = 'FREQUENCY2'
# To trigger consistently at the point of change, enter the minimum expected
# time between frequency changes (this is used to set trigger holdoff time):
MIN_TIME_BETWEEN_FREQS = 0.5  # (seconds)

# =============================================================================
# Helper functions
# =============================================================================


def banner(banner_text='', banner_char='='):
    if banner_text == '':
        print(banner_char*79)
    else:
        char_count = 79 - int(len(banner_text)+2)
        half_banner = int(char_count/2)
        banner_str = str(
            banner_char*half_banner+' {} '
            .format(banner_text)+banner_char*half_banner)
        if int(len(banner_str)) == 78:
            print(banner_str+banner_char)
        else:
            print(banner_str)


def initialize():
    print('Initializing {} from reset...'.format(model))
    KsInfiniiVisionX.query('*RST; *OPC?')
    # Turn on only the channel to be used:
    if channel_int != 1:
        KsInfiniiVisionX.write(':CHANnel1:DISPlay OFF')
        KsInfiniiVisionX.write(':{}:DISPlay ON'.format(channel))
    KsInfiniiVisionX.query(':TRIGger:SOURce {}; *OPC?'.format(channel))
    if trig_on_freq_change:
        KsInfiniiVisionX.write(':TRIGger:MODE GLITch')  # Pulse Width trigger
        KsInfiniiVisionX.query(':TRIGger:GLITch:SOURce {}; *OPC?'
                               .format(channel))
        # Trigger on pulse width less than the time value:
        KsInfiniiVisionX.write(':TRIGger:GLITch:LESSthan {}'
                               .format(pwidth_threshold))
        # Trigger on pulse width greater than the time value:
        KsInfiniiVisionX.write(':TRIGger:GLITch:GREaterthan {}'
                               .format(pwidth_threshold))
        # Choose > or < for the Pulse Width trigger:
        KsInfiniiVisionX.write(':TRIGger:GLITch:QUALifier {}'
                               .format(qualifier))
        KsInfiniiVisionX.write(':TRIGger:HOLDoff {}'.format(holdoff))
    KsInfiniiVisionX.write(':TRIGger:SWEep NORMal')
    KsInfiniiVisionX.query('*OPC?')
    KsInfiniiVisionX.write(':DISPlay:SIDebar MEASurements')
    KsInfiniiVisionX.write('{}:SCALe {}'
                           .format(channel, VERTICAL_SCALE))
    KsInfiniiVisionX.query('*OPC?')
    KsInfiniiVisionX.write(':MEASure:CLEar')
    KsInfiniiVisionX.write('{}'.format(MEAS))
#    KsInfiniiVisionX.write(':MEASure:PWIDth {}'.format(channel))
    KsInfiniiVisionX.query('*OPC?')
    KsInfiniiVisionX.write(':TIMebase:SCALe {}'.format(TIMESCALE))
    KsInfiniiVisionX.query('*OPC?')
    time.sleep(1)  # Pause to let trend plot scale correctly
    KsInfiniiVisionX.write(':FUNCtion1:DISPlay ON')
    KsInfiniiVisionX.write(':FUNCtion1:OPERation TRENd')
    KsInfiniiVisionX.write(':FUNCtion1:TRENd:NMEasurement MEAS1')
    # Do error check:
    setup_error = error_check()
    if len(setup_error) == 0:
        print('Scope setup completed without error.\n')
        del setup_error
    else:
        safe_exit_custom_message(
            'Setup has errors.  Properly closing scope and exiting script.')
    return bool(KsInfiniiVisionX.query('*OPC?'))


def time_tag():
    time_stamp = time.localtime()
    year = time_stamp[0]
    month = time_stamp[1]
    day = time_stamp[2]
    hour = time_stamp[3]
    minute = time_stamp[4]
    second = time_stamp[5]
    time_tag = '{:d}'.format(year) + '-' + '{:0>2d}'.format(month) + '-' + \
               '{:0>2d}'.format(day) + '_' + '{:0>2d}'.format(hour) + '-' + \
               '{:0>2d}'.format(minute) + '-' + '{:0>2d}'.format(second)
    return time_tag


def wait_for_trigger():
    triggered = 0
    while triggered == 0:  # Poll the scope until it returns a 1
        triggered = int(KsInfiniiVisionX.query(':TER?'))
        time.sleep(POLLING_INTERVAL)  # Pause to prevent excessive queries
    return()


def binblock_raw(data_in):
    # This function interprets the header for a definite binary block
    # and returns the raw data for both definite and indefinite binary blocks
    startpos = data_in.find('#')
    if startpos < 0:
        raise IOError('No start of block found')
    lenlen = int(data_in[startpos+1:startpos+2])  # Get the data length
    # If it's a definite length binary block
    if lenlen > 0:
        # Get the length from the header
        offset = startpos+2+lenlen
        datalen = int(data_in[startpos+2:startpos+2+lenlen])
    else:
        # If an indefinite length binblock, get length from the transfer itself
        offset = startpos+2
        datalen = len(data_in)-offset-1
    data_out = data_in[offset:offset+datalen]
    if format == 'ascii':
        return np.fromstring(data_out, sep=',')
    else:
        return np.array(data_out)
    return data_out


def error_check():
    # Error Check function
    my_error = []
    error_list = KsInfiniiVisionX.query(':SYSTem:ERRor?').split(',')
    error = error_list[0]
    while int(error) != 0:
        print('\nError #: ' + error_list[0])
        print('Error Description: ' + error_list[1])
        my_error.append(error_list[0])
        my_error.append(error_list[1])
        error_list = KsInfiniiVisionX.query(':SYSTem:ERRor?').split(',')
        error = error_list[0]
        my_error = list(my_error)
    return my_error


def safe_exit_custom_message(message):
    # Safe exit function
    KsInfiniiVisionX.clear()
    KsInfiniiVisionX.query(':STOP;*OPC?')
    KsInfiniiVisionX.clear()
    KsInfiniiVisionX.close()
    sys.exit(message)


# =============================================================================
# Misc tasks
# =============================================================================

# Display User Inputs:
if VERBOSE_MODE:
    print('')
    banner('InfiniiVision_Meas_Trend.py')
    print('')
    banner('User Inputs', '-')
    print('    {:32} {} (Set False to suppress this list)'
          .format('VERBOSE_MODE:', VERBOSE_MODE))
    print('    {:32} {}'.format('SCOPE_VISA_ADDRESS:', SCOPE_VISA_ADDRESS))
    print('    {:32} {}'
          .format('GENERAL_TIMEOUT:', Quantity(GENERAL_TIMEOUT/1000, 's')))
    print('    {:32} {}'.format('NUMBER_WAVEFORMS:', NUMBER_WAVEFORMS))
    print('    {:32} {}'.format('WAVEFORM_FORMAT:', WAVEFORM_FORMAT))
    print('    {:32} {}'
          .format('POLLING_INTERVAL:', Quantity(POLLING_INTERVAL, 's')))
    print('    {:32} {}'.format('OUTPUT_FILE:', OUTPUT_FILE))
    print('    {:32} {}'.format('IMPORT_SAVED_FILES:', IMPORT_SAVED_FILES))
    print('    {:32} {}'.format('OPEN_CSV_FILE:', OPEN_CSV_FILE))
    print('    {:32} {}'.format('DIRECTORY:', DIRECTORY))
    print('    {:32} {}'.format('START_FROM_RESET:', START_FROM_RESET))
    if START_FROM_RESET:
        print('    {:32} {}'
              .format('-> VERTICAL_SCALE:', Quantity(VERTICAL_SCALE, 'V/div')))
        print('    {:32} {}'
              .format('-> TIMESCALE:', Quantity(TIMESCALE, 's/div')))
        print('    {:32} {}'.format('-> MEAS:', MEAS))
        if FREQUENCY1 > 0 and FREQUENCY2 > 0:
            print('    {:32} {}'
                  .format('-> FREQUENCY1:', Quantity(FREQUENCY1, 'Hz')))
            print('    {:32} {}'
                  .format('-> FREQUENCY2:', Quantity(FREQUENCY2, 'Hz')))
            print('    {:32} {}'.format('-> DUTY_CYCLE:', DUTY_CYCLE))
            if TRIGGER_ON == 'FREQUENCY1':
                print('    {:32} {}'.format('-> TRIGGER_ON:',
                      '{} ({})'
                      .format(TRIGGER_ON, Quantity(FREQUENCY1, 'Hz'))))
            else:
                print('    {:32} {}'.format('-> TRIGGER_ON:',
                      '{} ({})'
                      .format(TRIGGER_ON, Quantity(FREQUENCY2, 'Hz'))))
            print('    {:32} {}'.format('-> MIN_TIME_BETWEEN_FREQS:',
                  Quantity(MIN_TIME_BETWEEN_FREQS, 's')))
    banner('', '-')

# Set formatting for console output:
try:
    Quantity.set_preferences(prec=3, spacer=' ')  # Causes errors on some PCs
except Exception:
    try:
        Quantity.set_prefs(prec=3, spacer=' ')  # Causes errors on some PCs
    except Exception:
        sys.exit(
            'Quantiphy package may not be installed.  Enter at command prompt:'
            'pip install quantiphy')

# A bit of format polishing for those with OCD:
if NUMBER_WAVEFORMS > 1:
    s_if_plural = 's'
    s_if_plural_not = ''
else:
    s_if_plural = ''
    s_if_plural_not = 's'

if re.search('ASCii', WAVEFORM_FORMAT, re.IGNORECASE):
    format = 'ascii'
else:
    format = 'word'

# Get channel number from MEAS:
temp = re.findall(r'\d+', MEAS)
channel_int = map(int, temp)[0]
channel = str('CHANnel{}'.format(channel_int))

# Calculate pulse width trigger values:
if FREQUENCY1 > 0 and FREQUENCY2 > 0:
    trig_on_freq_change = True
    period1 = round(1./FREQUENCY1, 9)
    period2 = round(1./FREQUENCY2, 9)
    dutycycle = round(float(DUTY_CYCLE.strip('%'))/100, 3)
    pwidth1 = round(dutycycle * period1, 9)
    pwidth2 = round(dutycycle * period2, 9)
    if pwidth1 > pwidth2:
        pwidth_threshold = round(pwidth2 + (pwidth1-pwidth2)/2, 9)
    else:
        pwidth_threshold = round(pwidth1 + (pwidth2-pwidth1)/2, 9)
    if TRIGGER_ON == 'FREQUENCY1':
        if FREQUENCY1 > FREQUENCY2:
            qualifier = 'LESSthan'
        else:
            qualifier = 'GREaterthan'
        qualifier = 'GREaterthan'
    if TRIGGER_ON == 'FREQUENCY2':
        if FREQUENCY2 > FREQUENCY1:
            qualifier = 'LESSthan'
        else:
            qualifier = 'GREaterthan'
    if MIN_TIME_BETWEEN_FREQS > 4E-8:
        holdoff = MIN_TIME_BETWEEN_FREQS
    else:
        holdoff = 'MINimum'

# =============================================================================
# Connect and initialize scope
# =============================================================================

# Define VISA Resource Manager
# This directory will need to be changed if VISA was installed somewhere else:
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll')

# Open connection to the scope by its VISA address:
try:
    print('\nConnecting to: {}'.format(SCOPE_VISA_ADDRESS))
    KsInfiniiVisionX = rm.open_resource(SCOPE_VISA_ADDRESS)
except Exception:
    print('Unable to connect to oscilloscope at {}.  Aborting.\n'
          .format(SCOPE_VISA_ADDRESS))
    sys.exit()

KsInfiniiVisionX.timeout = GENERAL_TIMEOUT

# Clear the remote interface:
KsInfiniiVisionX.clear()

IDN = str(KsInfiniiVisionX.query('*IDN?'))
print('Connected to: {}'.format(IDN))
IDN = IDN.split(',')
model = IDN[1]

if START_FROM_RESET:
    initialize()

# =============================================================================
# Set up data export - For repetitive acquisitions, this only needs to be done
# once unless settings are changed
# =============================================================================

print('Waiting for triggered capture of initial test waveform...')
KsInfiniiVisionX.write('*CLS;:SINGle')
wait_for_trigger()
print('Done capturing test waveform.\n')

# Count pulses to approximate the number of unique measurements to expect.  In
# 7.30 firmware, it seems the most reliable way to get the correct number of
# trend points from the scope is to count the number of cycles captured and
# use that.  Using :WAVEFORM POINTS ALL is hit and miss, and specifying a large
# number of points typically returns many duplicate values.
ppulses = int(KsInfiniiVisionX.query_ascii_values(
        ':MEASure:PPULses? {}'.format(channel))[0])
npulses = int(KsInfiniiVisionX.query_ascii_values(
        ':MEASure:PPULses? {}'.format(channel))[0])
if ppulses > npulses:
    number_points_requested = npulses
else:
    number_points_requested = ppulses

KsInfiniiVisionX.write(':WAVeform:FORMat {}'.format(WAVEFORM_FORMAT))
if format == 'word':
    KsInfiniiVisionX.write(':WAVeform:BYTeorder LSBFirst')
    KsInfiniiVisionX.write(':WAVeform:UNSigned 0')
KsInfiniiVisionX.write(':WAVeform:SOURce FUNCtion1')
KsInfiniiVisionX.write(':WAVeform:POINts:MODE NORMal')
KsInfiniiVisionX.write(':WAVeform:POINts {}'.format(number_points_requested))
points_to_retrieve = int(KsInfiniiVisionX.query_ascii_values(
        ':WAVeform:POINts?')[0])

if VERBOSE_MODE:
    print('Number of trend points requested: {}'
          .format(number_points_requested))
    print('Number of trend points to retrieve: {:,}\n'
          .format(points_to_retrieve))

Pre = KsInfiniiVisionX.query(':WAVeform:PREamble?').split(',')
X_INCrement = float(Pre[4])
X_ORigin = float(Pre[5])
X_REFerence = float(Pre[6])
if format == 'word':
    Y_INCrement = float(Pre[7])
    Y_ORigin = float(Pre[8])
    Y_REFerence = float(Pre[9])

time_axis = ((np.linspace(0, points_to_retrieve - 1,
             points_to_retrieve)-X_REFerence) * X_INCrement) + X_ORigin

# =============================================================================
# Get trend data
# =============================================================================

i = 0  # iteration counter
trends = np.zeros((points_to_retrieve, NUMBER_WAVEFORMS))

print('Waiting for triggered capture of {:,} waveform{}...'
      .format(NUMBER_WAVEFORMS, s_if_plural))

while i < NUMBER_WAVEFORMS:
    KsInfiniiVisionX.write('*CLS;:SINGle')
    wait_for_trigger()
    if VERBOSE_MODE:
        print('    Waveforms captured: {:,} / {:,}'.format(
                      i+1, NUMBER_WAVEFORMS))
    if format == 'word':
        trend_data = np.array(KsInfiniiVisionX.query_binary_values(
                ':WAVeform:DATA?', 'h', False))
    elif format == 'ascii':
        temp_values = KsInfiniiVisionX.query(
                ':WAVeform:DATA?')
        trend_data = binblock_raw(temp_values)
    trends[:, i] = trend_data
    i += 1

print('Done capturing waveform{} and importing {:,} trend function{}.\n'
      .format(s_if_plural, NUMBER_WAVEFORMS, s_if_plural))

time_axis = ((np.linspace(0, points_to_retrieve-1,
             points_to_retrieve)-X_REFerence)*X_INCrement)+X_ORigin
if format == 'word':
    if VERBOSE_MODE:
        print('Scaling {:,} trend function{}...'
              .format(NUMBER_WAVEFORMS, s_if_plural))
    trends = ((trends-Y_REFerence)*Y_INCrement)+Y_ORigin

# Remove first and last points, which are likely invalid.  In 7.30 firmware,
# the first and/or last points of every measurement trend are often invalid
# measurements, possibly due to incomplete cycles.  This is probably a bug.
valid_points = points_to_retrieve - 2
trends = np.delete(trends, points_to_retrieve-1, 0)  # Delete last point
time_axis = np.delete(time_axis, points_to_retrieve-1, 0)
trends = np.delete(trends, 0, 0)  # Delete first point
time_axis = np.delete(time_axis, 0, 0)
if VERBOSE_MODE:
    if NUMBER_WAVEFORMS > 1:
        print('The first and last points for all trend functions have been ' +
              'discarded, since\nthese are often invalid.  {:,}'
              .format(valid_points) +
              ' valid measurements per waveform remain.\n')
    else:
        print('The first and last points for the trend function have been ' +
              'discarded, since\nthese are often invalid.  {:,}'
              .format(valid_points) +
              ' valid measurements remain.\n')

if VERBOSE_MODE:
    print('{:,} time tags saved to array: time_axis'
          .format(valid_points))
    print('{:,} measurements per waveform saved to array: trends\n'
          .format(valid_points))

# =============================================================================
# Create unique file name with date/time tag
# =============================================================================

time_stamp = time.localtime()
year = time_stamp[0]
month = time_stamp[1]
day = time_stamp[2]
hour = time_stamp[3]
minute = time_stamp[4]
second = time_stamp[5]
date_stamp = '{:d}'.format(year) + '-' + '{:0>2d}'.format(month) + '-' + \
            '{:0>2d}'.format(day) + '_' + '{:0>2d}'.format(hour) + '-' + \
            '{:0>2d}'.format(minute) + '-' + '{:0>2d}'.format(second)

filename = DIRECTORY + date_stamp

# =============================================================================
# Save trend data to CSV file and load it back into Python
# =============================================================================

if OUTPUT_FILE == 'CSV' or OUTPUT_FILE == 'BOTH':  # Save CSV file
    print('Saving {:,} trend function{} in CSV format...'.format(
            NUMBER_WAVEFORMS, s_if_plural))
    header = 'Time (s),{}\n'.format(MEAS)
    csv_file = filename + '.csv'
    with open(csv_file, 'w') as filehandle:
        filehandle.write(header)
        np.savetxt(filehandle, np.insert(trends, 0, time_axis, axis=1),
                   delimiter=',')
    print('Done saving {:,} {:,}-point trend function{} to file:'
          .format(NUMBER_WAVEFORMS, valid_points, s_if_plural))
    print('    {}\n'.format(csv_file))
    if IMPORT_SAVED_FILES:
        print('Loading trend data from CSV file back into Python...')
        with open(csv_file, 'r') as filehandle:  # r means open for reading
            recalled_CSV = np.loadtxt(filehandle, delimiter=',', skiprows=1)
        del filehandle, header
        print('Done loading trend data into NumPy array: recalled_CSV\n')

# =============================================================================
# Save waveform data to numpy file and load it back into Python
# =============================================================================

if OUTPUT_FILE == 'BINARY' or OUTPUT_FILE == 'BOTH':  # Save NPY file
    print('Saving {:,} trend function{} in binary (NumPy) format...'
          .format(NUMBER_WAVEFORMS, s_if_plural))
    header = 'Time (s),{}\n'.format(MEAS)
    npy_file = filename + '.npy'
    with open(npy_file, 'wb') as filehandle:
        np.save(filehandle, np.insert(trends, 0, time_axis, axis=1))
    print('Done saving {:,} {:,}-point trend function{} to file:'
          .format(NUMBER_WAVEFORMS, valid_points, s_if_plural))
    print('    {}\n'.format(npy_file))
    if IMPORT_SAVED_FILES:
        print('Loading trend data from {:} back into Python...'
              .format(npy_file))
        with open(npy_file, 'rb') as filehandle:  # rb means read binary
            recalled_NPY = np.load(filehandle)
        del filehandle, npy_file, header
        print('Done loading trend data into NumPy array: recalled_NPY\n')

# =============================================================================
# Open last saved CSV file
# =============================================================================

if OUTPUT_FILE == 'CSV' and OPEN_CSV_FILE:
    print('Opening CSV file for viewing...')
    os.startfile(csv_file)

# =============================================================================
# Done with scope operations - Close connection to scope
# =============================================================================

errors = error_check()

KsInfiniiVisionX.clear()
KsInfiniiVisionX.close()

print('\nDone.')

if VERBOSE_MODE:
    banner()
