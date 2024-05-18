import pandas as pd

# Specify the CSV file path
#csv_file_path = 'C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion'

# Read the CSV file and assign column names
#df = pd.read_csv(csv_file_path, header=None, names=['x', 'y', 'z'])

#Get the csv files from the specified path
df1 = pd.read_csv('C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\outputambiental.csv', usecols=[0, 1, 2], names=['Column1', 'Column2', 'Column3'])
df2 = pd.read_csv('C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\outputambiental.csv', usecols=[0, 1, 2], names=['Column1', 'Column2', 'Column3'])
df3 = pd.read_csv('C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\outputambiental.csv', usecols=[0, 1, 2], names=['Column1', 'Column2', 'Column3'])

import numpy as np

# Convert the DataFrames to numpy arrays
array1 = df1.to_numpy()
array2 = df2.to_numpy()
array3 = df3.to_numpy()

# Concatenate the arrays
result_array = np.concatenate((array1, array2, array3), axis=0)

# Convert the result back to a DataFrame
result = pd.DataFrame(result_array, columns=['Column1', 'Column2', 'Column3'])

# Check the number of rows in the resulting DataFrame
print(result.shape[0])

# Save the result to a new CSV file
result.to_csv('C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\outputambiental2.csv', index=False)