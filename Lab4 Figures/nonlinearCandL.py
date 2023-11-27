# Adjusting the script to ensure the y-axis scale displays absolute values properly

import numpy as np
import matplotlib.pyplot as plt

def plot_capacitance_vs_voltage():
    # Parameters for the model
    C0 = 1e-6  # Initial capacitance in Farads (1 µF)
    k = 1e-12  # Constant to define the rate of change of capacitance

    # Voltage range for plotting
    V = np.linspace(0, 10, 100)  # Voltages from 0 to 10 V

    # Capacitance model
    C = C0 / (1 + k * V**2)

    # Convert capacitance from Farads to microFarads
    C_uF = C * 1e6  # 1 F = 1e6 µF

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(V, C_uF, label='Capacitance vs. Voltage')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Capacitance (µF)')
    plt.title('Non-Linear Behavior of Capacitance with Voltage')
    #plt.ylim(0.1, 1)  # Set y-axis range
    plt.grid(True)
    plt.ticklabel_format(style='plain', axis='y')  # Use plain format for y-axis
    plt.legend()
    plt.show()

# Run the function to plot
plot_capacitance_vs_voltage()
