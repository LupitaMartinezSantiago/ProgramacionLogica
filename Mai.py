import socket
import struct
import numpy as np
import cv2

def run_receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.connect(('192.168.203.72', 5001))  # Reemplaza 'IP_DEL_SERVIDOR' con la IP del servidor
    print("Conectado al servidor para recibir la pantalla.")

    data = b""
    payload_size = struct.calcsize(">L")

    try:
        while True:

            while len(data) < payload_size:
                data += receiver_socket.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("Tamaño de imagen recibida en el receptor (esperado):", msg_size)

            # Recibir la imagen
            while len(data) < msg_size:
                data += receiver_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            print("Tamaño de datos de imagen recibidos en el receptor (real):", len(frame_data))

            # Decodificar y mostrar la imagen
            img = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is not None:
                img_resized = cv2.resize(img, (800, 450))  # Ajusta el tamaño de la ventana de visualización
                cv2.imshow("Pantalla Remota en el Receptor", img_resized)
            else:
                print("Error en la decodificación de la imagen en el receptor.")

            if cv2.waitKey(1) == 27:  # Presiona ESC para salir
                break

    except KeyboardInterrupt:
        print("Visualización detenida.")

    finally:
        receiver_socket.close()
        cv2.destroyAllWindows()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_receiver()
