import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Specify the CSV file path
csv_file_path = 'C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\nodereddata.csv'

# Read the CSV file and assign column names
df = pd.read_csv(csv_file_path, header=None, names=['x', 'y', 'z'])

# Plot each column separately
fig, axs = plt.subplots(3, figsize=(12, 18))

# Plot 'x'
axs[0].plot(df.index, df['x'], label='x')
axs[0].set_xlabel('Points')
axs[0].set_ylabel('Values')
axs[0].legend()
plt.yticks(rotation=90)  # Rotate y-axis labels

# Plot 'y'
axs[1].plot(df.index, df['y'], label='y')
axs[1].set_xlabel('Points')
axs[1].set_ylabel('Values')
axs[1].legend()
plt.yticks(rotation=90)  # Rotate y-axis labels

# Plot 'z'
axs[2].plot(df.index, df['z'], label='z')
axs[2].set_xlabel('Points')
axs[2].set_ylabel('Values')
axs[2].legend()
plt.yticks(rotation=90)  # Rotate y-axis labels

plt.tight_layout()  # Adjust subplot parameters to give specified padding
plt.show()