import socket
import time

def realizar_pruebas_udp():
    # Configuración: IP y Puerto del servidor UDP
    # Asegúrate de que coincida con el puerto del servidor (5001)
    target_host = 'localhost'
    target_port = 5001
    server_address = (target_host, target_port)
    
    # Lista de mensajes de prueba con el formato <ID_CLIENTE>:<OPERACIÓN>:<VALOR>
    pruebas = [
        "A1:SQR:5",        # Prueba válida (Cuadrado)
        "B2:CUBE:2",       # Prueba válida (Cubo)
        "C3:NEG:-15",      # Prueba válida (Negativo)
        "D4:SUMAR:10",     # Error: Operación no válida
        "E5:SQR:abc"       # Error: Valor no numérico
    ]
    
    try:
        # 1. Crear el socket UDP (SOCK_DGRAM)
        # Nota: UDP no requiere .connect() previo
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Establecemos un tiempo de espera de 2 segundos para no bloquearnos
        client_socket.settimeout(2)
        
        print(f"--- Iniciando pruebas UDP hacia {target_host}:{target_port} ---\n")
        
        for mensaje in pruebas:
            print(f"Cliente enviando: {mensaje}")
            
            # 2. Enviar datos (sendto requiere la dirección del destino)
            client_socket.sendto(mensaje.encode('utf-8'), server_address)
            
            try:
                # 3. Recibir respuesta y dirección del servidor
                datos, addr = client_socket.recvfrom(1024)
                respuesta = datos.decode('utf-8')
                print(f"Servidor ({addr}) responde: {respuesta}\n")
            
            except socket.timeout:
                print("Error: Tiempo de espera agotado (el paquete pudo perderse)\n")
            
            # Pausa breve para que los logs en la terminal sean legibles
            time.sleep(0.8)
            
        # 4. Cerrar el socket local
        client_socket.close()
        print("--- Pruebas finalizadas ---")
        
    except Exception as e:
        print(f"Ocurrió un error en el cliente: {e}")

if __name__ == "__main__":
    realizar_pruebas_udp()
