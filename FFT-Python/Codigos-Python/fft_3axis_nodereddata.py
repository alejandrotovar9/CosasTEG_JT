import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file and assign column names
df = pd.read_csv('C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\outputambiental.csv')

# Extract the x, y, z columns
x = df['Column1']
y = df['Column2']
z = df['Column3']

def split_into_chunks(data, chunk_size=1024):
    """Split the data into chunks of the specified size."""
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size) if len(data[i:i+chunk_size]) == chunk_size]

# Split the data into chunks of 1024 points
x_chunks = split_into_chunks(x)
y_chunks = split_into_chunks(y)
z_chunks = split_into_chunks(z)

# Apply windowing function to each chunk
x_chunks = [np.hanning(1024) * chunk for chunk in x_chunks]
y_chunks = [np.hanning(1024) * chunk for chunk in y_chunks]
z_chunks = [np.hanning(1024) * chunk for chunk in z_chunks]

# Concatenate the chunks back together
x_windowed = np.concatenate(x_chunks)
y_windowed = np.concatenate(y_chunks)
z_windowed = np.concatenate(z_chunks)

# Plot the data
fig, ax = plt.subplots()
ax.plot(df.index[:len(x_windowed)], x_windowed, label='x')
ax.plot(df.index[:len(y_windowed)], y_windowed, label='y')
ax.plot(df.index[:len(z_windowed)], z_windowed, label='z')
ax.set_xlabel('Datos')
ax.set_ylabel('Aceleración (m/s^2)')
ax.set_title('Registro concatenado de aceleración en los 3 ejes')
ax.legend()

# Plot the form of the windowing function
fig, ax = plt.subplots()
ax.plot(np.hanning(1024))
ax.set_xlabel('Datos')
ax.set_ylabel('Amplitud')
ax.set_title('Ventana Hanning')

plt.show()

# # Read the CSV file and assign column names
# df = pd.read_csv(csv_file_path, header=None, names=['x', 'y', 'z'])

# # Extract the x, y, z columns
# x = df['x']
# y = df['y']
# z = df['z']

# Perform FFT on each windowed data set
fft_set1 = np.fft.fft(x_windowed)
fft_set2 = np.fft.fft(y_windowed)
fft_set3 = np.fft.fft(z_windowed)

xfil_psd = np.abs(fft_set1)**2
yfil_psd = np.abs(fft_set2)**2
zfil_psd = np.abs(fft_set3)**2

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
plt.plot(positive_freq, np.abs(fft_set1[:len(positive_freq)]), label='Eje X')
plt.plot(positive_freq, np.abs(fft_set2[:len(positive_freq)]), label='Eje Y')
plt.plot(positive_freq, np.abs(fft_set3[:len(positive_freq)]), label='Eje Z')

# Annotate the maximum values
plt.annotate(f'Fmax_X: {max_freq1:.2f}', xy=(max_freq1, np.max(np.abs(fft_set1))), xytext=(10, 10), textcoords='offset points')
plt.annotate(f'Fmax_Y: {max_freq2:.2f}', xy=(max_freq2, np.max(np.abs(fft_set2))), xytext=(10, 10), textcoords='offset points')
plt.annotate(f'Fmax_Z: {max_freq3:.2f}', xy=(max_freq3, np.max(np.abs(fft_set3))), xytext=(10, 10), textcoords='offset points')


plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Espectro en frecuencia')
plt.legend()
plt.show()

# Plot the PSD
plt.figure(figsize=(10, 6))
plt.plot(positive_freq, xfil_psd[:len(positive_freq)], label='X-Axis')
plt.plot(positive_freq, yfil_psd[:len(positive_freq)], label='Y-Axis')
plt.plot(positive_freq, zfil_psd[:len(positive_freq)], label='Z-Axis')

plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD [V**2 / Hz]')
plt.title('Power Spectral Density')
plt.legend()
plt.grid(True)
plt.show()