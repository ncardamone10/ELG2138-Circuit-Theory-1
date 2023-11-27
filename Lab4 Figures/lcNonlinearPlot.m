% Parameters for the model
C0 = 1e-6;  % Initial capacitance in Farads (1 µF)
k = 1e-3;  % Constant to define the rate of change of capacitance

% Voltage range for plotting
V = linspace(0, 50, 100);  % Voltages from 0 to 10 V

% Capacitance model
C = C0 ./ (1 + k * V.^2);

% Convert capacitance from Farads to microFarads
C_uF = C * 1e6;  % 1 F = 1e6 µF


% Parameters for the model
L0 = 1e-3;  % Initial inductance in Henry (1 mH)
Isat = 1; % Saturation current in Amperes
alpha = 0.1; % Constant defining rate of inductance decrease

% Current range for plotting
I = linspace(0, 10, 100);  % Currents from 0 to 1 A

% Inductance model
% L decreases as current increases beyond Isat
L = L0 ./ (1 + alpha * max(I - Isat, 0).^2);


subplot(1,2,1);
% Plotting
plot(I, L * 1e3, 'LineWidth', 2); % Convert inductance to milliHenry for plotting
xlabel('Current (A)');
ylabel('Inductance (mH)');
title('Non-Linear Behavior of a Typical 1 mH Power Inductor');
grid on;
ylim([0,1.1])

subplot(1,2,2);
% Plotting
plot(V, C_uF, 'LineWidth', 2);
xlabel('Voltage (V)');
ylabel('Capacitance (µF)');
title('Non-Linear Behavior of a Typical 25V 1uF Rated Ceramic Capacitor');
ylim([0.1 1.1]);  % Set y-axis range
grid on;



