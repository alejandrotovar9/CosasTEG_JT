import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Specify the CSV file path
csv_file_path = 'C:\\Users\\jatov\\Documents\\Universidad\\TEG\\FFT-Python\\nodereddata.csv'

# Specify the sampling frequency
sampling_freq = 200  # Replace with your actual sampling frequency

# Read the CSV file and assign column names
df = pd.read_csv(csv_file_path, header=None, names=['x', 'y', 'z'])


# Compute the frequencies associated with the FFT values
freq = np.fft.fftfreq(df.index.shape[-1], d=1/sampling_freq)

# Perform FFT on each column
x_fft = np.fft.fft(df['x'])
y_fft = np.fft.fft(df['y'])
z_fft = np.fft.fft(df['z'])

# # Compute the frequencies associated with the FFT values
# freq = np.fft.fftfreq(df.index.shape[-1])

# # Plot each column separately
# fig, axs = plt.subplots(3, figsize=(12, 18))

# # Plot 'x'
# axs[0].plot(df.index, df['x'], label='x')
# axs[0].set_xlabel('Points')
# axs[0].set_ylabel('Values')
# axs[0].legend()
# plt.yticks(rotation=90)  # Rotate y-axis labels

# # Plot 'y'
# axs[1].plot(df.index, df['y'], label='y')
# axs[1].set_xlabel('Points')
# axs[1].set_ylabel('Values')
# axs[1].legend()
# plt.yticks(rotation=90)  # Rotate y-axis labels

# # Plot 'z'
# axs[2].plot(df.index, df['z'], label='z')
# axs[2].set_xlabel('Points')
# axs[2].set_ylabel('Values')
# axs[2].legend()
# plt.yticks(rotation=90)  # Rotate y-axis labels

# Plot the FFT of each column separately
fig, axs = plt.subplots(3, figsize=(12, 18))

# Plot FFT of 'x'
axs[0].plot(freq, np.abs(x_fft), label='x')
axs[0].set_xlabel('Frequency')
axs[0].set_ylabel('Amplitude')
axs[0].legend()
axs[0].tick_params(axis='y', rotation=90)  # Rotate y-axis labels

# Plot FFT of 'y'
axs[1].plot(freq, np.abs(y_fft), label='y')
axs[1].set_xlabel('Frequency')
axs[1].set_ylabel('Amplitude')
axs[1].legend()
axs[1].tick_params(axis='y', rotation=90)  # Rotate y-axis labels

# Plot FFT of 'z'
axs[2].plot(freq, np.abs(z_fft), label='z')
axs[2].set_xlabel('Frequency')
axs[2].set_ylabel('Amplitude')
axs[2].legend()
axs[2].tick_params(axis='y', rotation=90)  # Rotate y-axis labels


plt.tight_layout()  # Adjust subplot parameters to give specified padding
plt.show()