import socket

def enviar_prueba(mensaje):
    # Configuración del cliente
    host = 'localhost'
    port = 5000
    
    try:
        # 1. Crear el socket TCP
        obj_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 2. Conectar al servidor
        obj_socket.connect((host, port))
        print(f"--- Conectado al servidor en {host}:{port} ---")
        
        # 3. Enviar el mensaje
        print(f"Enviando: {mensaje}")
        obj_socket.send(mensaje.encode('utf-8'))
        
        # 4. Recibir respuesta
        respuesta = obj_socket.recv(1024).decode('utf-8')
        print(f"Respuesta del servidor: {respuesta}")
        
        # 5. Cerrar conexión
        obj_socket.close()
        print("--- Conexión cerrada ---\n")
        
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    # Prueba 1: Operación SQR
    enviar_prueba("A1:SQR:4")
    
    # Prueba 2: Operación CUBE
    enviar_prueba("B2:CUBE:3")
    
    # Prueba 3: Operación NEG
    enviar_prueba("C3:NEG:-10")
    
    # Prueba 4: Error (Formato inválido)
    enviar_prueba("D4:SUMAR:10")
