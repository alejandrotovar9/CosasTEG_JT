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
from scipy.signal import butter, filtfilt
from scipy.integrate import cumtrapz

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

ctk.set_appearance_mode("Light")   
ctk.set_default_color_theme("green")  
 
#VENTANA PRINCIPAL
window = ctk.CTk()
window.title("INTERFAZ DE MONITOREO DE CONTROL - SISTEMA ESP32 JOSE TOVAR")


#Crea 2 tabs
notebook = ctk.CTkTabview(window, anchor="nw")

# Frames de cada tab
tab1 = notebook.add('Tab 1')
tab2 = notebook.add('Tab 2')

#columnas
tab1.columnconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)
tab1.columnconfigure(2, weight=1)


image = Image.open("C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\Codigos-Python\\IMME.jpg")
background_image = ctk.CTkImage(image, size=(100, 100))
# Create a label with the image
image_label = ctk.CTkLabel(tab1, image=background_image, text="")
# Place the label in the grid
image_label.grid(column=0, row=0, sticky='n')


image2 = Image.open("C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\Codigos-Python\\angulos.png")
pruebaang = ctk.CTkImage(image2, size=(130, 130))
# Create a label with the image
image_label = ctk.CTkLabel(tab2, image=pruebaang, text="")
# Place the label in the grid
image_label.grid(column=0, row=2, sticky='n')


#SECCION DE CONTROL
control_frame = ctk.CTkFrame(tab1)
control_frame.grid(column=0, row=0, sticky='n', pady=170, padx=10)
#Crea label para seccion de control
control_label = ctk.CTkLabel(control_frame, text="Sección de \n Control", font=("Arial", 14, "bold"))
control_label.pack()
#Crea boton para seccion de control
control_button = ctk.CTkButton(control_frame, text="Obtener registro", command=send_mqtt_message)
control_button.pack(pady=10)

#LISTA DE ARCHIVOS
folder_path = "C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\DatosACL_P1"
file_names = os.listdir(folder_path)

#crea el frame para los archivos
frameArchivos = ctk.CTkFrame(tab1)
frameArchivos.grid(column=1, row=3)

label = ctk.CTkLabel(frameArchivos, text="No hay registros nuevos")
label.grid(column=0, row=1, padx = 5)

selected_file_name = ctk.StringVar(tab1)
selected_file_name.set("Seleccione un registro")
#MENU DROPDOWN PARA ESCOGER ARCHIVO
option_menu = ctk.CTkOptionMenu(master=frameArchivos, variable=selected_file_name, values=file_names)
option_menu.grid(column=0, row=2)

# Funcion para actualizar lista de archivos
def update_file_list(option_menu):
    #Consigue la lista de archivos disponibles
    file_names = os.listdir(folder_path)

    # Sort the files by modification time
    file_names.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    
    # Destroy the existing CTkOptionMenu widget
    option_menu.destroy()
    
    # Create a new CTkOptionMenu widget with the updated options
    option_menu = ctk.CTkOptionMenu(master=frameArchivos, variable=selected_file_name, values=file_names)
    option_menu.grid(column=1, row=1)

    #Actualiza cada 10 segundos
    tab1.after(10000, lambda: update_file_list(option_menu)) 

    # #Configura un timer para actualizar la lista cada 5 segundos
    # tab1.after(5000, update_file_list)

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
fig_fft.suptitle('ESPECTRO EN FRECUENCIA DEL REGISTRO', fontsize=10, fontweight='bold')
#fig.set_facecolor('lightgray')
canvas_fft = FigureCanvasTkAgg(fig_fft, master=tab1)
widget_fft = canvas_fft.get_tk_widget()
widget_fft.grid(column=2, row=0)
widget_fft.config(bd = 2, relief = "groove") #'flat', 'raised', 'sunken', 'ridge', 'groove' and 'solid'.

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
frameVentanas.grid(column=2, row=2)
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
    df = pd.read_csv(os.path.join( folder_path, file_name), header=None, names=['x', 'y', 'z', 'temp', 'hum', 'yaw', 'pitch', 'roll', 'time'])

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

    if(pitch < -1 or pitch > 1):
        label_nivel.configure(text="El sensor no está a nivel en el eje y (Phi).", font=("Arial", 14, "bold"))
    elif(roll < -1 or roll > 1):
        label_nivel.configure(text="El sensor no está a nivel en el eje x (Omega).", font=("Arial", 14, "bold"))
    else:
        label_nivel.configure(text="El sensor está a nivel.", font=("Arial", 14, "bold"))
        

    #Lista de angulos
    angles = [pitch, roll]
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

    # Genera eje de tiempo
    start_time = datetime.fromtimestamp(df['time'].iloc[0])

    timearr = [start_time + timedelta(seconds=i/200) for i in range(len(x))]

    #Grafica los nuevos datos

    #ACELERACION
    ax.plot(timearr, x, label='ACL X')
    ax.plot(timearr, y, label='ACL Y')
    ax.plot(timearr, z, label='ACL Z')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Aceleración (m/s^2)')
    ax.grid(True)

    #FFT SIN FILTRAR

    xfil = fft_1
    yfil = fft_2
    zfil = fft_3

    #FFT filtrada
    # xfil = filtros.butter_lowpass_filter(fft_1, 40, 200, 5)
    # yfil = filtros.butter_lowpass_filter(fft_2, 40, 200, 5)
    # zfil = filtros.butter_lowpass_filter(fft_3, 40, 200, 5)

    #FFT
    ax_fft.plot(positive_freq, np.abs(xfil[:len(positive_freq)]), label='Espectro Eje X')
    ax_fft.plot(positive_freq, np.abs(yfil[:len(positive_freq)]), label='Espectro Eje Y')
    ax_fft.plot(positive_freq, np.abs(zfil[:len(positive_freq)]), label='Espectro Eje Z')

    ax_fft.set_xlabel('Frecuencia (Hz)')
    ax_fft.set_ylabel('Amplitud')
    ax_fft.grid(True)

    #Grafica la densidad espectral de potencia
    ax_psd.plot(positive_freq, np.abs(xfil_psd[:len(positive_freq)]), label='Densidad Espectral X')
    ax_psd.plot(positive_freq, np.abs(yfil_psd[:len(positive_freq)]), label='Densidad Espectral Y')
    ax_psd.plot(positive_freq, np.abs(zfil_psd[:len(positive_freq)]), label='Densidad Espectral Z')
    #ax_psd.set_yscale('log')
    ax_psd.set_xlabel('Frequency (Hz)')
    ax_psd.set_ylabel('Power Spectral Density')
    ax_psd.grid(True)

    #Grafico de barras para inclinacion
    ax_bar.axhline(1, color='r', linestyle='--')  
    ax_bar.axhline(-1, color='r', linestyle='--') 
    ax_bar.bar(labels, angles)
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

    #Frecuencias maximas en PSD
    ax_psd.annotate(f'Fmax_X: {max_freq1:.2f}', xy=(max_freq1, np.max(np.abs(xfil_psd[:len(positive_freq)]))), xytext=(-10 if max_freq1 > median_freq else 10,30), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax_psd.annotate(f'Fmax_Y: {max_freq2:.2f}', xy=(max_freq2, np.max(np.abs(yfil_psd[:len(positive_freq)]))), xytext=(-10 if max_freq2 > median_freq else 10,10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax_psd.annotate(f'Fmax_Z: {max_freq3:.2f}', xy=(max_freq3, np.max(np.abs(zfil_psd[:len(positive_freq)]))), xytext=(-10 if max_freq3 > median_freq else 10,-10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    
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

notebook.pack(expand=True, fill='both')

#Loop principal de la ventana
window.mainloop()