import threading
from tkinter import Tk, Button
import socket
import numpy as np
import cv2
import struct

# Variable global para controlar el cliente activo
active_client = 0  # 0 para el cliente inicial, 1 para el cliente alternativo

def switch_client():
    global active_client
    active_client = 1 - active_client  # Alternar entre 0 y 1
    print(f"Cambiando a cliente {'2' if active_client else '1'}")

def run_server():
    global active_client

    # Configuración del servidor para recibir la pantalla del cliente
    server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket1.bind(('0.0.0.0', 5000))
    server_socket1.listen(1)
    print("Esperando conexión del Cliente 1...")
    client_socket1, _ = server_socket1.accept()
    print("Cliente 1 conectado.")

    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2.bind(('0.0.0.0', 5002))
    server_socket2.listen(1)
    print("Esperando conexión del Cliente 2...")
    client_socket2, _ = server_socket2.accept()
    print("Cliente 2 conectado.")

    # Configuración para retransmitir a la tercera computadora (receptor)
    transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transmit_socket.bind(('0.0.0.0', 5001))  # Puerto para retransmisión
    transmit_socket.listen(1)
    print("Esperando conexión del receptor...")
    receiver_socket, _ = transmit_socket.accept()
    print("Receptor conectado. Retransmitiendo la pantalla...")

    data1 = b""
    data2 = b""
    payload_size = struct.calcsize(">L")

    try:
        while True:
            # Seleccionar el cliente activo
            if active_client == 0:
                data = data1
                client_socket = client_socket1
            else:
                data = data2
                client_socket = client_socket2

            # Recibir el tamaño de la imagen del cliente activo
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            # Recibir la imagen del cliente activo
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Guardar datos para el cliente correspondiente
            if active_client == 0:
                data1 = data
            else:
                data2 = data

            # Retransmitir el tamaño de la imagen al receptor
            receiver_socket.sendall(struct.pack(">L", msg_size))
            # Retransmitir los datos de la imagen al receptor
            receiver_socket.sendall(frame_data)

            # Decodificar y mostrar la imagen en el servidor (opcional)
            img = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (800, 450))  # Ajustar el tamaño de la ventana de visualización
            cv2.imshow("Pantalla Remota en el Servidor", img_resized)

            if cv2.waitKey(1) == 27:  # Presiona ESC para salir
                break

    except KeyboardInterrupt:
        print("Retransmisión detenida.")

    finally:
        client_socket1.close()
        client_socket2.close()
        receiver_socket.close()
        server_socket1.close()
        server_socket2.close()
        transmit_socket.close()
        cv2.destroyAllWindows()
        print("Conexión cerrada.")

def start_gui():
    # Crear la interfaz gráfica
    root = Tk()
    root.title("Servidor de Retransmisión")

    # Botón para alternar la dirección de transmisión
    switch_button = Button(root, text="Cambiar Cliente Activo", command=switch_client, font=("Arial", 16), bg="lightblue")
    switch_button.pack(pady=20)

    # Ejecutar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    # Iniciar el servidor en un hilo separado
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Iniciar la interfaz gráfica
    start_gui()
