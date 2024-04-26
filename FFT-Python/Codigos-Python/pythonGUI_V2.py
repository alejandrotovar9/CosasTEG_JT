import tkinter as tk
import tkinter.filedialog as fd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Create a tkinter window
window = tk.Tk()
window.title("Acceleration Data Visualization")

# Get a list of files in the specific folder
folder_path = "C:\\Users\\jatov\\Documents\\Universidad\\TEG\CosasTEG_JT\\FFT-Python"
file_names = os.listdir(folder_path)

# Create a StringVar object to hold the selected file name
selected_file_name = tk.StringVar(window)

# Create an OptionMenu widget
option_menu = tk.OptionMenu(window, selected_file_name, *file_names)
option_menu.grid(column=0, row=1)

# Create a figure and axis for plotting
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
widget = canvas.get_tk_widget()
widget.grid(column=0, row=0)

# Create a second figure and axis for plotting the FFT
fig_fft, ax_fft = plt.subplots()
canvas_fft = FigureCanvasTkAgg(fig_fft, master=window)
widget_fft = canvas_fft.get_tk_widget()
widget_fft.grid(column=1, row=0)

def update_plots():
    # Get the selected file name
    file_name = selected_file_name.get()

    # Read the CSV file and assign column names
    df = pd.read_csv(os.path.join(folder_path, file_name), header=None, names=['x', 'y', 'z'])

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

    # Clear the previous plots
    ax.clear()
    ax_fft.clear()

    # Plot the new data
    ax.plot(x, label='Eje X')
    ax.plot(y, label='Eje Y')
    ax.plot(z, label='Eje Z')
    ax_fft.plot(positive_freq, np.abs(fft_1[:len(positive_freq)]), label='FFT del Eje X')
    ax_fft.plot(positive_freq, np.abs(fft_2[:len(positive_freq)]), label='FFT del Eje Y')
    ax_fft.plot(positive_freq, np.abs(fft_3[:len(positive_freq)]), label='FFT del Eje Z')

    # Get the frequencies from the highest amplitude for each axis
    max_freq1 = positive_freq[np.argmax(np.abs(fft_1[:len(positive_freq)]))]
    max_freq2 = positive_freq[np.argmax(np.abs(fft_2[:len(positive_freq)]))]
    max_freq3 = positive_freq[np.argmax(np.abs(fft_3[:len(positive_freq)]))]

    ax.legend()

    # Redraw the plots
    canvas.draw()
    canvas_fft.draw()

# Create a button that calls the update_plots function when clicked
button = tk.Button(window, text="Update plots", command=update_plots)
button.grid(column=1, row=1)

# Start the tkinter main loop
window.mainloop()