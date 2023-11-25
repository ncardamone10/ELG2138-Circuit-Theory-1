# Oscilloscope Control Script (ChatGPT Autogenerated)

## Overview

This Python script provides an interface for controlling an oscilloscope via a VISA interface. It includes a `Scope` class that encapsulates various oscilloscope functions such as setting the time base, adjusting trigger settings, reading measurements, and fetching waveform data. This script is designed to be user-friendly for students new to Python and oscilloscope operations.

## Prerequisites

Before using this script, ensure you have the following installed:

- Python
- pyvisa package
- numpy package
- matplotlib package
- tabulate package

## Installation

1. **Install Python 3.x**: Download and install Python 3.x from [python.org](https://www.python.org/downloads/).
2. **Set up a Python environment**: (Optional, but recommended)
   - Open a terminal or command prompt (new terminal in VS code, PyCharm can do this automatically for you).
   - Navigate to your project directory.
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment:
     - Windows: `.\venv\Scripts\activate`
     - MacOS/Linux: `source venv/bin/activate`
3. **Install required packages**:
   - Run `pip install pyvisa numpy matplotlib tabulate`.

## Configuration

- Ensure the oscilloscope is connected to the computer via USB or a network.
- Identify the VISA address of your oscilloscope. This can typically be done using the NI MAX utility or similar VISA configuration tools.
- Update the `visa_address` parameter in the `Scope` class initializer with your oscilloscope's VISA address.

## Usage

1. Import the `Scope` class from the script.
2. Create an instance of the `Scope` class.
3. Call methods on the instance to control the oscilloscope. For example:
   ```python
   oscilloscope = Scope('Your VISA Address Here')
   oscilloscope.set_time_base(1e-3)
   waveform_data = oscilloscope.grab_data(channel=1)
   ```

## Features

- **Connection to Oscilloscope**: Establish a connection to the oscilloscope using its VISA address.
- **Control Time Base**: Set and get the time base of the oscilloscope.
- **Adjust Trigger Settings**: Configure trigger settings like channel, level, type, and slope.
- **Read Measurements**: Read various measurements from a specified channel such as Vpp, Vmax, Vmin, etc.
- **Fetch Waveform Data**: Retrieve waveform data from a specified channel.
- **Auto Scale**: Perform auto-scaling on the oscilloscope.
- **Default Setup**: Reset the oscilloscope to default settings.

## Note

- The script is configured for a specific model of oscilloscope. Modifications may be necessary for different models or brands.
- Some functions are commented out and may require additional setup or customization.