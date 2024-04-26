import tkinter as tk
import tkinter.filedialog as fd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import shutil
import tkinter.filedialog
import paho.mqtt.client as mqtt

# Function to send an MQTT message
def send_mqtt_message():
    # Publish a message to a certain topic
    client.publish("esp32/command", "ON")

    # Disable the button
    control_button.config(state="disabled")

    # Enable the button after 5000 milliseconds (5 seconds)
    window.after(5000, lambda: control_button.config(state="normal"))

# Create an MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Connect to the MQTT broker
client.connect("127.0.0.1", 1883, 60)  # Replace with your broker's address and port

# Create a tkinter window
window = tk.Tk()
window.title("Acceleration Data Visualization")

# Set the weight of the columns
window.columnconfigure(0, weight=1)  # Make column 0 expand
window.columnconfigure(1, weight=1)  # Make column 1 expand
window.columnconfigure(2, weight=1)  # Make column 2 expand

# Get a list of files in the specific folder
folder_path = "C:\\Users\\jatov\\Documents\\Universidad\\TEG\CosasTEG_JT\\FFT-Python"
file_names = os.listdir(folder_path)

# Create a StringVar object to hold the selected file name
selected_file_name = tk.StringVar(window)

# Create a label for the OptionMenu widget
label = tk.Label(window, text="Select a file:")
label.grid(column=1, row=2)

# Create an OptionMenu widget
option_menu = tk.OptionMenu(window, selected_file_name, *file_names)
option_menu.grid(column=1, row=3)

# Create a figure and axis for plotting
fig, ax = plt.subplots()
 # Assuming fig is your Figure object
fig.suptitle('INTERFAZ DE MONITOREO DE CONTROL - SISTEMA ESP32 JOSE TOVAR', fontsize=10, fontweight='bold')

canvas = FigureCanvasTkAgg(fig, master=window)
widget = canvas.get_tk_widget()
widget.grid(column=1, row=0)

# Create a second figure and axis for plotting the FFT
fig_fft, ax_fft = plt.subplots()
canvas_fft = FigureCanvasTkAgg(fig_fft, master=window)
widget_fft = canvas_fft.get_tk_widget()
widget_fft.grid(column=2, row=0)

# Create a frame for the control section
control_frame = tk.Frame(window)
control_frame.grid(column=0, row=0, sticky='n')

# Create a label for the control section
control_label = tk.Label(control_frame, text="Control Section", font=("Arial", 14))
control_label.pack()

# Create a button in the control section
control_button = tk.Button(control_frame, text="Obtener registro", command=send_mqtt_message)
control_button.pack()

# Function to save the current file
def save_file():
    # Ask the user for the destination file name
    dest_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")

    # If the user didn't cancel the dialog
    if dest_filename:
        # Copy the current file to the destination file (current file is the complete path to the file opened)
        shutil.copyfile(folder_path + "\\" + selected_file_name.get(), dest_filename)

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

    # Generate the time axis for the plot using the amount of data points divided by the sample frequency
    time = np.arange(0, len(x)/200, 1/200)

    # Plot the new data
    ax.plot(time, x, label='Eje X')
    ax.plot(time, y, label='Eje Y')
    ax.plot(time, z, label='Eje Z')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Aceleración')
    ax_fft.plot(positive_freq, np.abs(fft_1[:len(positive_freq)]), label='FFT del Eje X')
    ax_fft.plot(positive_freq, np.abs(fft_2[:len(positive_freq)]), label='FFT del Eje Y')
    ax_fft.plot(positive_freq, np.abs(fft_3[:len(positive_freq)]), label='FFT del Eje Z')
    ax_fft.set_xlabel('Frequency (Hz)')
    ax_fft.set_ylabel('Amplitude')

    # Get the frequencies from the highest amplitude for each axis
    max_freq1 = positive_freq[np.argmax(np.abs(fft_1[:len(positive_freq)]))]
    max_freq2 = positive_freq[np.argmax(np.abs(fft_2[:len(positive_freq)]))]
    max_freq3 = positive_freq[np.argmax(np.abs(fft_3[:len(positive_freq)]))]

    median_freq = positive_freq[len(positive_freq)//2]

    # Annotate the maximum frequencies on the FFT plots without overlapping using the median
    ax_fft.annotate(f'FmaxX: {max_freq1:.2f}', xy=(max_freq1, np.max(np.abs(fft_1[:len(positive_freq)]))), xytext=(-10 if max_freq1 > median_freq else 10,30), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax_fft.annotate(f'FmaxY): {max_freq2:.2f}', xy=(max_freq2, np.max(np.abs(fft_2[:len(positive_freq)]))), xytext=(-10 if max_freq2 > median_freq else 10,10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax_fft.annotate(f'FmaxZ: {max_freq3:.2f}', xy=(max_freq3, np.max(np.abs(fft_3[:len(positive_freq)]))), xytext=(-10 if max_freq3 > median_freq else 10,-10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))


    ax.legend()
    ax_fft.legend()

    # Redraw the plots
    canvas.draw()
    canvas_fft.draw()

# Create a button that calls the save_file function when clicked
save_button = tk.Button(window, text="Save CSV", command=save_file)
save_button.grid(column=2, row=1)

# Create a button that calls the update_plots function when clicked
button = tk.Button(window, text="Update plots", command=update_plots)
button.grid(column=1, row=1)

# Schedule the function to be called after 1000 milliseconds
window.after(10000, update_plots)

# Start the tkinter main loop
window.mainloop()