import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Specify the CSV file path
csv_file_path = 'C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\nodereddata1.csv'

# Read the CSV file and assign column names
df = pd.read_csv(csv_file_path, header=None, names=['x', 'y', 'z'])

# Extract the x, y, z columns
x = df['x']
y = df['y']
z = df['z']

# Perform FFT on each data set
fft_set1 = np.fft.fft(x)
fft_set2 = np.fft.fft(y)
fft_set3 = np.fft.fft(z)

# Get the positive frequencies
freq = np.fft.fftfreq(len(x), d=1/200)  # d is the inverse of the sampling rate
positive_freq = freq[:len(freq)//2]

# Get the frequencies from the highest amplitude for each axis
max_freq1 = positive_freq[np.argmax(np.abs(fft_set1[:len(positive_freq)]))]
max_freq2 = positive_freq[np.argmax(np.abs(fft_set2[:len(positive_freq)]))]
max_freq3 = positive_freq[np.argmax(np.abs(fft_set3[:len(positive_freq)]))]

print("Max Frequency for X-Axis:", max_freq1)
print("Max Frequency for Y-Axis:", max_freq2)
print("Max Frequency for Z-Axis:", max_freq3)

# Plot the FFT results
plt.plot(positive_freq, np.abs(fft_set1[:len(positive_freq)]), label='X-Axis')
plt.plot(positive_freq, np.abs(fft_set2[:len(positive_freq)]), label='Y-Axis')
plt.plot(positive_freq, np.abs(fft_set3[:len(positive_freq)]), label='Z-Axis')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend()
plt.show()