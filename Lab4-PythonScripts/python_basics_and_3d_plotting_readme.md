
# Python Basics and 3D Plotting in VS Code

## Overview
This README provides an introduction to Python, instructions on setting up Python with Visual Studio Code (VS Code), and an example to create a 3D plot of the complex function w = exp(j*theta).

## Setting up Python

### Prerequisites
- Python 3.x
- Visual Studio Code

### Python Installation
1. Download and install Python 3.x from [python.org](https://www.python.org/downloads/).
2. During installation, ensure you check the box 'Add Python to PATH'.

### Visual Studio Code Setup
1. Download and install VS Code from [Visual Studio Code](https://code.visualstudio.com/).
2. Open VS Code.
3. Install the Python extension: Go to Extensions (side bar) -> Search for 'Python' -> Install.

### Configuring a Python Environment in VS Code
1. Open VS Code and navigate to your project folder.
2. Press `Ctrl` + `Shift` + `P` and type 'Python: Select Interpreter'.
3. Choose the Python interpreter you installed.
4. To create a virtual environment, open the terminal in VS Code and run: 
   ```
   python -m venv venv
   ```
5. Activate the virtual environment:
   - Windows: `.env\Scriptsctivate`
   - MacOS/Linux: `source venv/bin/activate`
6. Install necessary packages using pip. For the 3D plotting example, you'll need `matplotlib` and `numpy`:
   ```
   pip install matplotlib numpy
   ```

## 3D Plotting Example

### Code Example
Create a new Python file and paste the following code:

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate theta values
theta = np.linspace(0, 2*np.pi, 100)

# Compute w = exp(j*theta)
w = np.exp(1j*theta)

# Extract real and imaginary parts
real_w = np.real(w)
imag_w = np.imag(w)

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(theta, real_w, imag_w)

# Labeling the Axes
ax.set_xlabel('Theta')
ax.set_ylabel('Real Part of w')
ax.set_zlabel('Imaginary Part of w')

# Show plot
plt.show()
```

### Running the Example
1. Save the file.
2. Run the file in VS Code's integrated terminal:
   ```
   python filename.py
   ```
3. A 3D plot window should open showing the plot of w = exp(j*theta).

## Note
- This example is a basic introduction to 3D plotting in Python using matplotlib.
- Feel free to explore more complex plotting and Python functionalities as you progress.

## Support
For any assistance or questions, feel free to reach out or consult the [Python documentation](https://docs.python.org/3/) and [Matplotlib documentation](https://matplotlib.org/).
