import socket
import threading

# Estructura requerida: clientes[socket] = ID_CLIENTE
clientes = {}

def procesar_operacion(operacion, valor):
    try:
        val = int(valor)
        if operacion == "SQR": return val ** 2
        if operacion == "CUBE": return val ** 3
        if operacion == "NEG": return val * -1
        return "ERROR: Operación no válida"
    except ValueError:
        return "ERROR: Valor no numérico"

def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break # Desconexión de cliente
            
            # Formato esperado: <ID_CLIENTE>:<OPERACIÓN>:<VALOR>
            partes = data.strip().split(':')
            if len(partes) == 3:
                id_cliente, operacion, valor = partes
                
                # Requerimiento: Asociar ID con el socket
                clientes[conn] = id_cliente
                
                resultado = procesar_operacion(operacion, valor)
                respuesta = f"{id_cliente}:{resultado}"
                conn.send(respuesta.encode('utf-8'))
            else:
                conn.send("ERROR: Formato inválido".encode('utf-8'))
                
    except Exception as e:
        print(f"[ERROR] Con {addr}: {e}")
    finally:
        print(f"[DESCONEXIÓN] {addr} se ha ido.")
        if conn in clientes:
            del clientes[conn]
        conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen()
    print("[SERVER] TCP escuchando en puerto 5000...")
    
    while True:
        conn, addr = server.accept() # Aquí ocurre la demultiplexación explícita (nuevo socket)
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
