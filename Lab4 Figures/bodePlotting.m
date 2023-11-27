% Parameters for the low-pass filter
R = 1e3;  % Resistance in ohms (1 kOhm)
C = 1e-6; % Capacitance in farads (1 µF)

% Transfer function of the LPF
s = tf('s');
H = 1 / (1 + R*C*s);

% Generate the Bode plot
figure;
h = bodeplot(H);
setoptions(h, 'FreqUnits', 'Hz'); % Set frequency units to Hz

% Find all line objects and set their line width
ax = findall(gcf, 'Type', 'axes');
lines = findall(ax, 'Type', 'line');
set(lines, 'LineWidth', 2);

grid on;
title('Bode Plot of a Low-Pass Filter');
