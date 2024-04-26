import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import matplotlib.pyplot as plt

# Specify the CSV file path
csv_file_path = 'C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\nodereddata1.csv'

# Read the CSV file and assign column names
df = pd.read_csv(csv_file_path, header=None, names=['x', 'y', 'z'])

# Extract the x, y, z columns
x = df['x']
y = df['y']
z = df['z']

# Compute the FFT of the acceleration data sets using numpy
fft_1 = np.fft.fft(x)
fft_2 = np.fft.fft(y)
fft_3 = np.fft.fft(z)

# Get the positive frequencies
freq = np.fft.fftfreq(len(x), d=1/200)  # d is the inverse of the sampling rate
positive_freq = freq[:len(freq)//2]

# Create a tkinter window
window = tk.Tk()
window.title("Acceleration Data Visualization")

# Create a figure and axis for plotting
fig, ax = plt.subplots()

# Plot the acceleration data sets
ax.plot(x, label='Acceleration 1')
ax.plot(y, label='Acceleration 2')
ax.plot(z, label='Acceleration 3')

# Set the labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Acceleration')
ax.set_title('Acceleration Data')

# Add a legend
ax.legend()

# Create a canvas and add it to the window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
widget = canvas.get_tk_widget()
widget.grid(column=0, row=0)  # Use grid instead of pack

# Create a second figure and axis for plotting the FFT
fig_fft, ax_fft = plt.subplots()

# Plot the FFT of the acceleration data sets
ax_fft.plot(positive_freq, np.abs(fft_1[:len(positive_freq)]), label='FFT of Acceleration 1')
ax_fft.plot(positive_freq, np.abs(fft_2[:len(positive_freq)]), label='FFT of Acceleration 2')
ax_fft.plot(positive_freq, np.abs(fft_3[:len(positive_freq)]), label='FFT of Acceleration 3')

# Set the labels and title for the FFT plot
ax_fft.set_xlabel('Frequency')
ax_fft.set_ylabel('Amplitude')

# Create a second canvas and add it to the window
canvas_fft = FigureCanvasTkAgg(fig_fft, master=window)
canvas_fft.draw()
widget_fft = canvas_fft.get_tk_widget()
widget_fft.grid(column=1, row=0)  # Use grid instead of pack

# Start the tkinter main loop
window.mainloop()