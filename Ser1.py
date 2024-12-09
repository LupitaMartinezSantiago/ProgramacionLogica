import socket
import tkinter as tk
from PIL import Image, ImageTk
import io

# Funciones de plantilla (asegurarse de que existan en tu archivo plantilla.py)
from plantilla import centrar_frame_principal, crear_label, create_entry, create_button

def start_screen_monitoring_client(host, port): 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")
        return

    def update_image():
        try:
            # Recibir el tamaño de la imagen (4 bytes)
            size_data = client_socket.recv(4)
            if not size_data:
                print("Conexión cerrada o no se recibió datos.")
                return
            size = int.from_bytes(size_data, byteorder='big')

            # Recibir la imagen en paquetes
            image_data = b''
            while len(image_data) < size:
                packet = client_socket.recv(size - len(image_data))
                if not packet:
                    print("Error en la recepción de datos.")
                    return
                image_data += packet

            # Verificar si la imagen se recibió completamente
            if len(image_data) == size:
                # Mostrar la imagen
                image = Image.open(io.BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)
                label.config(image=photo)
                label.image = photo

            # Actualizar la imagen en la interfaz cada 100 ms
            root.after(100, update_image)
        except Exception as e:
            print(f"Error: {e}")

    # Crear la interfaz gráfica
    root = tk.Tk()
    root.title("Monitoreo de Pantalla Remota")

    label = tk.Label(root)
    label.pack()

    # Iniciar la actualización de la imagen
    root.after(100, update_image)
    root.mainloop()

    client_socket.close()

def connect_to_server():
    host = ip_entry.get()
    port = int(port_entry.get())
    connect_window.destroy()  # Cerrar la ventana de conexión antes de iniciar la recepción
    start_screen_monitoring_client(host, port)

# Crear la interfaz para ingresar la IP y el puerto
connect_window = tk.Tk()
connect_window.title("Conectar al Servidor")
connect_window.configure(bg="#0f1440")  # Fondo con un tono más oscuro
connect_window.geometry("600x300")

# Titulo
label = tk.Label(connect_window, text="Ver pantalla servidor", font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440")
label.pack(pady=(30))

crear_label("IP del Servidor:", connect_window).pack()
ip_entry = create_entry(connect_window)
ip_entry.pack(pady=10, padx=10)

crear_label("Puerto:", connect_window).pack()
port_entry = create_entry(connect_window)
port_entry.pack(pady=10, padx=10)

connect_button = create_button(connect_window,"Conectar", connect_to_server)
connect_button.pack(pady=10, padx=10)

#-----------Ajustar el tamaño de la ventana--------
centrar_frame_principal(connect_window)

connect_window.mainloop()
