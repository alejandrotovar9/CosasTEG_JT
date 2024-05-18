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
from tkinter import PhotoImage
import filtros
from datetime import datetime,timedelta

#Funcion callback cuando se recibe un mensaje MQTT con el payload received
def on_message(client, userdata, message):
    #Chequea si el payload es "received"
    if message.payload.decode() == "received":
        #Crea el label con el texto y lo muestra en pantalla
        label.config(text="Nuevo registro disponible!")

#Funcion para enviar comando via MQTT al topico esp32/command 
def send_mqtt_message():
    #Publica el mensaje al topico
    client.publish("esp32/command", "ON")

    #Desactiva el boton temporalmente
    control_button.config(state="disabled")

    #Reactiva el boton luego de 5 segundos
    window.after(5000, lambda: control_button.config(state="normal"))

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

#VENTANA PRINCIPAL
window = tk.Tk()
window.title("INTERFAZ DE MONITOREO DE CONTROL - SISTEMA ESP32 JOSE TOVAR")
img = PhotoImage(file="C:\\Users\\jatov\\Documents\\Universidad\\TEG\\CosasTEG_JT\\FFT-Python\\Codigos-Python\\logoingenieria.png")
window.iconphoto(False, img)

#COLUMNAS
window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

#LISTA DE ARCHIVOS A ESCOGER
folder_path = "C:\\Users\\jatov\\Documents\\Universidad\\TEG\\Pruebas_DatosAceleracion\\DatosACL_P1"
#StringVar para guardar el archivo seleccionado
file_names = os.listdir(folder_path)

#Crea el frame para los archivos
frameArchivos = tk.Frame(window)
#Coloca el frame en pantalla en posicion deseada
frameArchivos.grid(column=1, row=3)

label = tk.Label(frameArchivos, text="No hay registros nuevos")
label.grid(column=0, row=1)

selected_file_name = tk.StringVar(window)
#Configura el titulo del menu dropdown
selected_file_name.set("Seleccione un registro")

#Funcion para actualizar la lista de archivos dispo
def update_file_list():
    #Consigue la lista de archivos disponibles
    file_names = os.listdir(folder_path)

    #Actualiza el widget de menu
    menu = option_menu["menu"]
    menu.delete(0, "end")
    for file_name in file_names:
        menu.add_command(label=file_name, command=lambda value=file_name: selected_file_name.set(value))

    #Configura un timer para actualizar la lista cada 5 segundos
    window.after(5000, update_file_list)

#MENU DROPDOWN PARA ESCOGER ARCHIVO
option_menu = tk.OptionMenu(frameArchivos, selected_file_name, *file_names)
option_menu.grid(column=1, row=1)

#FIGURA DE ACELERACION
fig, ax = plt.subplots()
fig.suptitle('REGISTRO DE ACELERACIÓN EN TIEMPO', fontsize=10, fontweight='bold')
canvas = FigureCanvasTkAgg(fig, master=window)
widget = canvas.get_tk_widget()
widget.grid(column=1, row=0)

#FIGURA PARA FFT
fig_fft, ax_fft = plt.subplots()
fig_fft.suptitle('ESPECTRO EN FRECUENCIA DEL REGISTRO ESCOGIDO USANDO FFT', fontsize=10, fontweight='bold')
canvas_fft = FigureCanvasTkAgg(fig_fft, master=window)
widget_fft = canvas_fft.get_tk_widget()
widget_fft.grid(column=2, row=0)

#SECCION DE CONTROL
control_frame = tk.Frame(window)
control_frame.grid(column=0, row=0, sticky='n', pady=150)
#Crea label para seccion de control
control_label = tk.Label(control_frame, text="Sección de \n Control", font=("Arial", 14))
control_label.pack()
#Crea boton para seccion de control
control_button = tk.Button(control_frame, text="Obtener registro", command=send_mqtt_message)
control_button.pack()

#SECCION DE ALERTAS
# alert_frame = tk.Frame(window)
# alert_frame.grid(column=0, row=1, sticky='n', pady=150)
# #Crea label para seccion de alertas
# alert_label = tk.Label(alert_frame, text="Sección de \n Alertas", font=("Arial", 14))
# alert_label.pack()
# #Crea label para alertas
# alert_text = tk.Label(alert_frame, text="Alertas: \n", font=("Arial", 12))
# alert_text.pack()



#AVENTANAMIENTO
windowing_functions = ['Ninguno','Hanning', 'Hamming', 'Blackman']
#Guarda aventanamiento seleccionado
selected_windowing_function = tk.StringVar()
#Configura el aventanamiento default
selected_windowing_function.set(windowing_functions[0])
#Crea el menu dropdown de aventanamientos
windowing_menu = tk.OptionMenu(window, selected_windowing_function, *windowing_functions)
windowing_menu.grid(column=2, row=2)  # Adjust the grid position as needed

#FUNCION DE GUARDADO EN CSV
def save_file():
    #Pregunta al usuario el archivo a escoger
    dest_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")

    #Si el usuario no cancela el dialogo
    if dest_filename:
        #Copia el archivo actual en la direccion especificada
        shutil.copyfile(folder_path + "\\" + selected_file_name.get(), dest_filename)

#Crea el boton para guardar CSV en pantalla
save_button = tk.Button(window, text="Guardar CSV", command=save_file)
save_button.grid(column=2, row=3)

#VALORES ACTUALES DE TEMPERATURA Y HUMEDAD
#Crea frame de temperatura y humedad
frameTH = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
frameTH.grid(column=2, row=1, )

#Crea los labels de temperatura y humedad con color
current_value_label_x = tk.Label(frameTH, text="Humedad relativa:", font=("Arial Bold", 12), background="#e0e0e0")
current_value_label_x.grid(column=1, row=1, padx=10)
current_value_label_y = tk.Label(frameTH, text="Temperatura:", font=("Arial Bold", 12), background="#e0e0e0")
current_value_label_y.grid(column=2, row=1, padx=10)

#VALORES ACTUALES DE INCLINACION
#Crea el frame donde se mostraran las inclinaciones
frameInc = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
frameInc.grid(column=1, row=1)
#Labels de valor actual de inclinacion
current_value_label_yaw = tk.Label(frameInc, text="Kappa (κ):", font=("Arial Bold", 12), background="#e0e0e0")
current_value_label_yaw.grid(column=1, row=1, padx=10)
current_value_label_pitch = tk.Label(frameInc, text="Phi (ϕ):", font=("Arial Bold", 12), background="#e0e0e0")
current_value_label_pitch.grid(column=2, row=1, padx=10)
current_value_label_roll = tk.Label(frameInc, text="Omega (ω):", font=("Arial Bold", 12), background="#e0e0e0")
current_value_label_roll.grid(column=3, row=1, padx=10)

#FECHA Y HORA DE REGISTRO
time_label = tk.Label(window)
time_label.grid(column=1, row=4)

#FUNCION PRINCIPAL DE ACTUALIZACION DE PLOTS
def update_plots():
    #Obtiene el nombre del archivo seleccionado
    file_name = selected_file_name.get()

    #Borra los contenidos previos del label para no solapar
    label.config(text = "No hay registros nuevos")

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

    #Convierte de UNIX epoch a datetime
    time = datetime.fromtimestamp(df['time'].iloc[0]) + timedelta(hours=4) #Diferencia de 4 horas por GMT

    #Actualiza la etiqueta de tiempo
    time_label.config(text="Fecha y Hora del registro: " + str(time))

    #Actualiza los labels de valores actuales de temperatura, humedad e inclinacion
    current_value_label_x.config(text="Humedad relativa: " + str(hum) + "%")
    current_value_label_y.config(text="Temperatura: " + str(temp) + " °C")
    current_value_label_yaw.config(text="Kappa (κ): " + str(yaw) + "°")
    current_value_label_pitch.config(text="Phi (ϕ): " + str(pitch) + "°")
    current_value_label_roll.config(text="Omega (ω): " + str(roll) + "°")

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

    #Obtiene las frecuencias positivas de la FFT
    freq = np.fft.fftfreq(len(x), d=1/200)  # d is the inverse of the sampling rate
    positive_freq = freq[:len(freq)//2]

    #Limpia la grafica anterior
    ax.clear()
    ax_fft.clear()

    # Generate the time axis for the plot using the amount of data points divided by the sample frequency
    #timearr = np.arange(0, len(x)/200, 1/200)
    # Generate the time axis for the plot using the datetime object and the amount of data points divided by the sample frequency
    # Convert epoch time to datetime
    start_time = datetime.fromtimestamp(df['time'].iloc[0])

    timearr = [start_time + timedelta(seconds=i/200) for i in range(len(x))]

    #Grafica los nuevos datos
    ax.plot(timearr, x, label='Eje X')
    ax.plot(timearr, y, label='Eje Y')
    ax.plot(timearr, z, label='Eje Z')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Aceleración (m/s^2)')
    ax.grid(True)

    xfil = filtros.butter_lowpass_filter(fft_1, 40, 200, 5)
    yfil = filtros.butter_lowpass_filter(fft_2, 40, 200, 5)
    zfil = filtros.butter_lowpass_filter(fft_3, 40, 200, 5)

    ax_fft.plot(positive_freq, np.abs(xfil[:len(positive_freq)]), label='FFT del Eje X filtrada')
    ax_fft.plot(positive_freq, np.abs(yfil[:len(positive_freq)]), label='FFT del Eje Y filtrada')
    ax_fft.plot(positive_freq, np.abs(zfil[:len(positive_freq)]), label='FFT del Eje Z filtrada')

    ax_fft.set_xlabel('Frecuencia (Hz)')
    ax_fft.set_ylabel('Amplitud')
    ax_fft.grid(True)

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

#Crea el boton para actualizar grafica
button = tk.Button(window, text="Actualizar gráfica", command=update_plots)
button.grid(column=1, row=2)

#Ejecuta la funcion de actualizacion de archivos disponibles
update_file_list()

# Schedule the function to be called after 1000 milliseconds
#window.after(10000, update_plots)

# Start the tkinter main loop
window.mainloop()