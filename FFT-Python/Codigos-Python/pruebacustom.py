import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as fd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import shutil
#import tkinter.filedialog
import paho.mqtt.client as mqtt
from tkinter import PhotoImage
import filtros
from datetime import datetime,timedelta
from tkinter import ttk
from PIL import Image

#Funcion callback cuando se recibe un mensaje MQTT con el payload received
def on_message(client, userdata, message):
    #Chequea si el payload es "received"
    if message.payload.decode() == "received":
        #Crea el label con el texto y lo muestra en pantalla
        label.configure(text="Nuevo registro disponible!")

#Funcion para enviar comando via MQTT al topico esp32/command 
def send_mqtt_message():
    #Publica el mensaje al topico
    client.publish("esp32/command", "ON")

    #Desactiva el boton temporalmente
    control_button.configure(state="disabled")

    #Reactiva el boton luego de 5 segundos
    tab1.after(5000, lambda: control_button.configure(state="normal"))

#CLIENTE MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#Se conecta al broker
client.connect("127.0.0.1", 1883, 60) #El broker esta en localhost
#Configura la funcion callback a llamar cuando se recibe mensaje
client.on_message = on_message
#Se suscribe al topico de alerta o notificacion de recepcion
client.subscribe("esp32/alerta_rx")
#Inicia el loop que mantiene la conexion de MQTT y gestiona los mensajes
client.loop_start()

# "System" sets the appearance mode to 
# the appearance mode of the system
ctk.set_appearance_mode("Light")   
 
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue    
ctk.set_default_color_theme("green")   
# MAIN WINDOW
window = ctk.CTk()
window.title("INTERFAZ DE MONITOREO DE CONTROL - SISTEMA ESP32 JOSE TOVAR")
# img = PhotoImage(file="C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\Codigos-Python\\logoingenieria.png")
# window.iconphoto(False, img)



#Create two tabs
# Create a notebook (tabbed interface)
notebook = ctk.CTkTabview(window, anchor="nw")

# Create frames for each tab
tab1 = notebook.add('Tab 1')
tab2 = notebook.add('Tab 2')

# Add the frames to the notebook as tabs


# COLUMNS
tab1.columnconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)
tab1.columnconfigure(2, weight=1)

image = Image.open("C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\Codigos-Python\\logoingenieria.png")
background_image = ctk.CTkImage(image, size=(100, 100))
# Create a label with the image
image_label = ctk.CTkLabel(tab1, image=background_image, text="")
# Place the label in the grid
image_label.grid(column=0, row=0, sticky='n')
# # Create a label with the image
# titulo_label = ctk.CTkLabel(tab1, text="Sistema de monitoreo y \n control de sensor \n inteligente", font=("Arial", 15, "bold"))
# # Place the label in the grid
# titulo_label.grid(column=0, row=1, sticky='n')

#SECCION DE CONTROL
control_frame = ctk.CTkFrame(tab1)
control_frame.grid(column=0, row=0, sticky='n', pady=170, padx=10)
#Crea label para seccion de control
control_label = ctk.CTkLabel(control_frame, text="Sección de \n Control", font=("Arial", 14, "bold"))
control_label.pack()
#Crea boton para seccion de control
control_button = ctk.CTkButton(control_frame, text="Obtener registro", command=send_mqtt_message)
control_button.pack(pady=10)

# LIST OF FILES TO CHOOSE
folder_path = "C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\DatosACL_P1"
# StringVar to save the selected file
file_names = os.listdir(folder_path)

# Create the frame for the files
frameArchivos = ctk.CTkFrame(tab1)
# Place the frame on the screen in the desired position
frameArchivos.grid(column=1, row=3)

label = ctk.CTkLabel(frameArchivos, text="No hay registros nuevos")
label.grid(column=0, row=1, padx = 5)

selected_file_name = ctk.StringVar(tab1)
# Set the title of the dropdown menu
selected_file_name.set("Seleccione un registro")
#MENU DROPDOWN PARA ESCOGER ARCHIVO
option_menu = ctk.CTkOptionMenu(master=frameArchivos, variable=selected_file_name, values=file_names)
option_menu.grid(column=0, row=2)

# Function to update the list of available files
def update_file_list(option_menu):
    #Consigue la lista de archivos disponibles
    file_names = os.listdir(folder_path)

    # #Actualiza el widget de menu
    # menu = option_menu["menu"]
    # menu.delete(0, "end")
    # for file_name in file_names:
    #     menu.add_command(label=file_name, command=lambda value=file_name: selected_file_name.set(value))

    # Assume that file_names is a list that contains the updated options
    #file_names = ["new_file1", "new_file2", "new_file3"]
    
    # Destroy the existing CTkOptionMenu widget
    option_menu.destroy()
    
    # Create a new CTkOptionMenu widget with the updated options
    option_menu = ctk.CTkOptionMenu(master=frameArchivos, variable=selected_file_name, values=file_names)
    option_menu.grid(column=1, row=1)

    #Configura un timer para actualizar la lista cada 5 segundos
    tab1.after(5000, update_file_list)

# # Create a new frame for the plots
# plot_frame = ctk.CTkFrame(window, bg_color="your_color")  # Replace "your_color" with the color you want
# plot_frame.pack()

#FIGURA DE ACELERACION
fig, ax = plt.subplots()
fig.suptitle('REGISTRO DE ACELERACIÓN EN TIEMPO', fontsize=10, fontweight='bold')
#fig.set_facecolor('lightgray')
#fig.set_edgecolor('black')
fig.set_alpha(0.5)
canvas = FigureCanvasTkAgg(fig, master=tab1)
widget = canvas.get_tk_widget()
widget.grid(column=1, row=0)
widget.config(bd = 2, relief = "groove")

#FIGURA PARA FFT
fig_fft, ax_fft = plt.subplots()
fig_fft.suptitle('ESPECTRO EN FRECUENCIA DEL REGISTRO USANDO FFT', fontsize=10, fontweight='bold')
#fig.set_facecolor('lightgray')
canvas_fft = FigureCanvasTkAgg(fig_fft, master=tab1)
widget_fft = canvas_fft.get_tk_widget()
widget_fft.grid(column=2, row=0)
widget_fft.config(bd = 2, relief = "groove") #'flat', 'raised', 'sunken', 'ridge', 'groove' and 'solid'.

# #FIGURA DE PSD
# figpsd, ax_psd = plt.subplots()
# figpsd.suptitle('DENSIDAD ESPECTRAL DE POTENCIA', fontsize=10, fontweight='bold')
# #figpsd.set_facecolor('lightgray')
# #figpsd.set_edgecolor('black')
# figpsd.set_alpha(0.5)
# canvas_psd = FigureCanvasTkAgg(figpsd, master=tab2)
# widget_psd = canvas_psd.get_tk_widget()
# widget_psd.pack()
# widget_psd.config(bd = 2, relief = "groove")

#FIGURA DE PSD
figpsd, ax_psd = plt.subplots()
figpsd.suptitle('DENSIDAD ESPECTRAL DE POTENCIA', fontsize=10, fontweight='bold')
#figpsd.set_facecolor('lightgray')
#figpsd.set_edgecolor('black')
figpsd.set_alpha(0.5)
canvas_psd = FigureCanvasTkAgg(figpsd, master=tab2)
widget_psd = canvas_psd.get_tk_widget()
widget_psd.grid(column=1, row=0)
widget_psd.config(bd = 2, relief = "groove")

#FIGURA DE BARRA
figbar, ax_bar = plt.subplots()
figbar.suptitle('GRÁFICA DE BARRAS PARA VER INCLINACIÓN EN SENSOR INTELIGENTE', fontsize=10, fontweight='bold')
#figpsd.set_facecolor('lightgray')
#figpsd.set_edgecolor('black')
figbar.set_alpha(0.5)
canvas_bar = FigureCanvasTkAgg(figbar, master=tab2)
widget_bar = canvas_bar.get_tk_widget()
widget_bar.grid(column=0, row=0)
widget_bar.config(bd = 2, relief = "groove")

label_nivel = ctk.CTkLabel(master=tab2, text="No se ha seleccionado un archivo.", font=("Arial", 14, "bold"))
label_nivel.grid(column=0, row=1)



#FRAME DE ABAJO A LA DERECHA
frameVentanas = ctk.CTkFrame(tab1)
# Place the frame on the screen in the desired position
frameVentanas.grid(column=2, row=2)
# Create a label for the dropdown menu
windowing_label = ctk.CTkLabel(master=frameVentanas, text="Aventanamiento")
windowing_label.grid(column=1, row=1, padx=5,pady= 5)  # Adjust the grid position as needed

#AVENTANAMIENTO
windowing_functions = ['Ninguno','Hanning', 'Hamming', 'Blackman']
#Guarda aventanamiento seleccionado
selected_windowing_function = ctk.StringVar()
#Configura el aventanamiento default
selected_windowing_function.set(windowing_functions[0])

#Crea el menu dropdown de aventanamientos
windowing_menu = ctk.CTkOptionMenu(master=frameVentanas, variable=selected_windowing_function, values=windowing_functions)
windowing_menu.grid(column=2, row=1, padx=5, pady= 5)  # Adjust the grid position as needed

#FUNCION DE GUARDADO EN CSV
def save_file():
    #Pregunta al usuario el archivo a escoger
    #dest_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")
    dest_filename = ctk.filedialog.asksaveasfilename(defaultextension=".csv")

    #Si el usuario no cancela el dialogo
    if dest_filename:
        #Copia el archivo actual en la direccion especificada
        shutil.copyfile(folder_path + "\\" + selected_file_name.get(), dest_filename)

#Crea el boton para guardar CSV en pantalla
save_button = ctk.CTkButton(tab1, text="Guardar CSV", command=save_file)
save_button.grid(column=2, row=3)

#VALORES ACTUALES DE TEMPERATURA Y HUMEDAD
#Crea frame de temperatura y humedad
frameTH = ctk.CTkFrame(tab1, bg_color="lightgray")
frameTH.grid(column=2, row=1, pady = 5)
#Crea los labels de temperatura y humedad con color
current_value_label_x = ctk.CTkLabel(frameTH, text="Variables ambientales:", font=("Arial", 14, "bold"))
current_value_label_x.grid(column=1, row=1, padx=5)
current_value_label_x = ctk.CTkLabel(frameTH, text="Humedad relativa:", font=("Arial", 14, "bold"), corner_radius=50, fg_color="darkgray")
current_value_label_x.grid(column=2, row=1, padx=10)
current_value_label_y = ctk.CTkLabel(frameTH, text="Temperatura:", font=("Arial", 14, "bold"), corner_radius=50, fg_color="darkgray")
current_value_label_y.grid(column=3, row=1, padx=10)

#VALORES ACTUALES DE INCLINACION
#Crea el frame donde se mostraran las inclinaciones
frameInc = ctk.CTkFrame(tab1, bg_color="lightgray")
frameInc.grid(column=1, row=1, pady = 5)
#Labels de valor actual de inclinacion
current_value_label_inc = ctk.CTkLabel(frameInc, text="Inclinación:", font=("Arial", 14, "bold"))
current_value_label_inc.grid(column=1, row=1, padx=5)

current_value_label_roll = ctk.CTkLabel(frameInc, text="Omega (ω):", font=("Arial", 14, "bold"), corner_radius=50, fg_color="darkgray")
current_value_label_roll.grid(column=2, row=1, padx=10)
current_value_label_pitch = ctk.CTkLabel(frameInc, text="Phi (ϕ):", font=("Arial", 14, "bold"), corner_radius=50, fg_color="darkgray")
current_value_label_pitch.grid(column=3, row=1, padx=10)
current_value_label_yaw = ctk.CTkLabel(frameInc, text="Kappa (κ):", font=("Arial", 14, "bold"), corner_radius=50, fg_color="darkgray")
current_value_label_yaw.grid(column=4, row=1, padx=10)

#FECHA Y HORA DE REGISTRO
time_label = ctk.CTkLabel(tab1, text="No se ha escogido ningún registro")
time_label.grid(column=1, row=4)

#FUNCION PRINCIPAL DE ACTUALIZACION DE PLOTS
def update_plots():
    #Obtiene el nombre del archivo seleccionado
    file_name = selected_file_name.get()

    #Borra los contenidos previos del label para no solapar
    label.configure(text = "No hay registros nuevos")

    #Lee el archivo CSV y asigna nombres a las columnas por orden
    df = pd.read_csv(os.path.join(folder_path, file_name), header=None, names=['x', 'y', 'z', 'temp', 'hum', 'yaw', 'pitch', 'roll', 'time'])

    #Extrae las columnas x,y,z
    x = df['x']
    y = df['y']
    z = df['z']
    temp = df['temp'].iloc[0] #Extrae solo el valor de la primera fila
    hum = df['hum'].iloc[0]
    yaw = df['yaw'].iloc[0]
    pitch = df['pitch'].iloc[0]
    roll = df['roll'].iloc[0]
    time = df['time'].iloc[0]

    if(pitch < -2 or pitch > 2):
        label_nivel.configure(text="El sensor no está a nivel en el eje y (Phi).", font=("Arial", 14, "bold"))
    elif(roll < -2 or roll > 2):
        label_nivel.configure(text="El sensor no está a nivel en el eje x (Omega).", font=("Arial", 14, "bold"))
    else:
        label_nivel.configure(text="El sensor está a nivel.", font=("Arial", 14, "bold"))
        

    # Create a list of the angles
    angles = [pitch, roll]

    # Create a list of labels for the angles
    labels = ['Phi (ϕ)', 'Omega (ω)']

    #Convierte de UNIX epoch a datetime
    time = datetime.fromtimestamp(df['time'].iloc[0]) + timedelta(hours=4) #Diferencia de 4 horas por GMT

    #Actualiza la etiqueta de tiempo
    time_label.configure(text="Fecha y Hora del registro: " + str(time))

    #Actualiza los labels de valores actuales de temperatura, humedad e inclinacion
    current_value_label_x.configure(text="Humedad relativa: " + str(hum) + "%")
    current_value_label_y.configure(text="Temperatura: " + str(temp) + " °C")
    current_value_label_yaw.configure(text="Kappa (κ): " + str(yaw) + "°")
    current_value_label_pitch.configure(text="Omega (ω): " + str(roll) + "°")
    current_value_label_roll.configure(text="Phi (ϕ): " + str(pitch) + "°")

    # Aplica el aventanamiento seleccionado a los datos de aceleracion
    if selected_windowing_function.get() == 'Hanning':
        window = np.hanning(len(x))
    elif selected_windowing_function.get() == 'Hamming':
        window = np.hamming(len(x))
    elif selected_windowing_function.get() == 'Blackman':
        window = np.blackman(len(x))
    elif selected_windowing_function.get() == 'Ninguno':
        window = 1 # No windowing

    windowed_data_x = x * window
    windowed_data_y = y * window
    windowed_data_z = z * window

    # Compute the FFT of the acceleration data sets using numpy
    # fft_1 = np.fft.fft(x)
    # fft_2 = np.fft.fft(y)
    # fft_3 = np.fft.fft(z)
    
    #Aplica FFT en datos aventanados con la funcion escogida
    fft_1 = np.fft.fft(windowed_data_x)
    fft_2 = np.fft.fft(windowed_data_y)
    fft_3 = np.fft.fft(windowed_data_z)

    # Calculate the PSD
    xfil_psd = np.abs(fft_1)**2
    yfil_psd = np.abs(fft_2)**2
    zfil_psd = np.abs(fft_3)**2

    #Obtiene las frecuencias positivas de la FFT
    freq = np.fft.fftfreq(len(x), d=1/200)  # d is the inverse of the sampling rate
    positive_freq = freq[:len(freq)//2]

    #Limpia la grafica anterior
    ax.clear()
    ax_fft.clear()
    ax_psd.clear()
    ax_bar.clear()

    # Generate the time axis for the plot using the amount of data points divided by the sample frequency
    #timearr = np.arange(0, len(x)/200, 1/200)
    # Generate the time axis for the plot using the datetime object and the amount of data points divided by the sample frequency
    # Convert epoch time to datetime
    start_time = datetime.fromtimestamp(df['time'].iloc[0])

    timearr = [start_time + timedelta(seconds=i/200) for i in range(len(x))]

    #Grafica los nuevos datos

    #ACELERACION
    ax.plot(timearr, x, label='Eje X')
    ax.plot(timearr, y, label='Eje Y')
    ax.plot(timearr, z, label='Eje Z')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Aceleración (m/s^2)')
    ax.grid(True)

    xfil = filtros.butter_lowpass_filter(fft_1, 40, 200, 5)
    yfil = filtros.butter_lowpass_filter(fft_2, 40, 200, 5)
    zfil = filtros.butter_lowpass_filter(fft_3, 40, 200, 5)

    #FFT
    ax_fft.plot(positive_freq, np.abs(xfil[:len(positive_freq)]), label='FFT del Eje X filtrada')
    ax_fft.plot(positive_freq, np.abs(yfil[:len(positive_freq)]), label='FFT del Eje Y filtrada')
    ax_fft.plot(positive_freq, np.abs(zfil[:len(positive_freq)]), label='FFT del Eje Z filtrada')

    ax_fft.set_xlabel('Frecuencia (Hz)')
    ax_fft.set_ylabel('Amplitud')
    ax_fft.grid(True)

    #Grafica la densidad espectral de potencia
    ax_psd.plot(positive_freq, np.abs(xfil_psd[:len(positive_freq)]), label='PSD of X-axis')
    ax_psd.plot(positive_freq, np.abs(yfil_psd[:len(positive_freq)]), label='PSD of Y-axis')
    ax_psd.plot(positive_freq, np.abs(zfil_psd[:len(positive_freq)]), label='PSD of Z-axis')
    #ax_psd.set_yscale('log')
    ax_psd.set_xlabel('Frequency (Hz)')
    ax_psd.set_ylabel('Power Spectral Density')
    ax_psd.grid(True)

    # #Get the damping value from the half-power method
    # # Get the peak frequency and power
    # peak_power_index_x = np.argmax(xfil_psd[:len(positive_freq)])
    # peak_power_index_y = np.argmax(yfil_psd[:len(positive_freq)])
    # peak_power_index_z = np.argmax(zfil_psd[:len(positive_freq)])
    # peak_power_x = np.abs(xfil_psd[peak_power_index_x])
    # peak_power_y = np.abs(yfil_psd[peak_power_index_y])
    # peak_power_z = np.abs(zfil_psd[peak_power_index_z])
    # peak_freq_x = positive_freq[peak_power_index_x]
    # peak_freq_y = positive_freq[peak_power_index_y]
    # peak_freq_z = positive_freq[peak_power_index_z]
    # # Calculate the half power
    # half_power_x = peak_power_x / 2
    # half_power_y = peak_power_y / 2
    # half_power_z = peak_power_z / 2
    # # Find the frequencies at which the power is half the peak power
    # half_power_indices_x = np.where(np.isclose(np.abs(xfil_psd[:len(positive_freq)]), half_power_x, atol=1))
    # half_power_freqs_x = positive_freq[half_power_indices_x]
    # half_power_indices_y = np.where(np.isclose(np.abs(yfil_psd[:len(positive_freq)]), half_power_y,  atol=1))
    # half_power_freqs_y = positive_freq[half_power_indices_y]
    # # half_power_indices_z = np.where(np.isclose(np.abs(zfil_psd[:len(positive_freq)]), half_power_z,  atol=1))
    # # half_power_freqs_z = positive_freq[half_power_indices_z]

    # #Print the half power values
    # print(half_power_indices_y)

    # # Calculate the bandwidth
    # bandwidth_x = np.abs(half_power_freqs_x[1] - half_power_freqs_x[0])
    # bandwidth_y = np.abs(half_power_freqs_y[1] - half_power_freqs_y[0])
    # # bandwidth_z = np.abs(half_power_freqs_z[1] - half_power_freqs_z[0])

    # # Calculate the damping ratio
    # damping_ratio_x = bandwidth_x / (2 * peak_freq_x)
    # damping_ratio_y = bandwidth_y / (2 * peak_freq_y)
    # # damping_ratio_z = bandwidth_z / (2 * peak_freq_z)

    # print(damping_ratio_x*100)



    #Grafico de barras para inclinacion
    # Assuming `ax` is your Axes object
    ax_bar.axhline(2, color='r', linestyle='--')  # Draws a dashed red line at y=2
    ax_bar.axhline(-2, color='r', linestyle='--')  # Draws a dashed red line at y=-2
    ax_bar.bar(labels, angles)
    # Set the title and labels
    ax_bar.set_title('Diagrama de barras para inclinación en sensor inteligente')
    ax_bar.set_xlabel('Ángulo')
    ax_bar.set_ylabel('Grados')


    #Obtiene las frecuencias maximas de cada eje
    max_freq1 = positive_freq[np.argmax(np.abs(xfil[:len(positive_freq)]))]
    max_freq2 = positive_freq[np.argmax(np.abs(yfil[:len(positive_freq)]))]
    max_freq3 = positive_freq[np.argmax(np.abs(zfil[:len(positive_freq)]))]

    median_freq = positive_freq[len(positive_freq)//2]

    #Muestra las frecuencias maximas en la grafica
    ax_fft.annotate(f'Fmax_X: {max_freq1:.2f}', xy=(max_freq1, np.max(np.abs(xfil[:len(positive_freq)]))), xytext=(-10 if max_freq1 > median_freq else 10,30), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax_fft.annotate(f'Fmax_Y: {max_freq2:.2f}', xy=(max_freq2, np.max(np.abs(yfil[:len(positive_freq)]))), xytext=(-10 if max_freq2 > median_freq else 10,10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax_fft.annotate(f'Fmax_Z: {max_freq3:.2f}', xy=(max_freq3, np.max(np.abs(zfil[:len(positive_freq)]))), xytext=(-10 if max_freq3 > median_freq else 10,-10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    
    ax.legend()
    ax_fft.legend()

    #Redibuja las graficas
    canvas.draw()
    canvas_fft.draw()
    canvas_bar.draw()
    canvas_psd.draw()

#Crea el boton para actualizar grafica
button = ctk.CTkButton(tab1, text="Actualizar gráfica", command=update_plots)
button.grid(column=1, row=2)

#Ejecuta la funcion de actualizacion de archivos disponibles
update_file_list(option_menu)

# Schedule the function to be called after 1000 milliseconds
#window.after(10000, update_plots)

notebook.pack(expand=True, fill='both')

# Start the tkinter main loop
window.mainloop()