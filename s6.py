import socket

# Estructura para asociar dirección de red con identificadores
# Requerimiento: clientes[(IP, puerto)] = ID_CLIENTE
clientes_udp = {}

def procesar_operacion(operacion, valor):
    """Lógica aritmética compartida con TCP."""
    try:
        val = int(valor)
        if operacion == "SQR": return val ** 2
        elif operacion == "CUBE": return val ** 3
        elif operacion == "NEG": return val * -1
        else: return "ERROR: Operación no válida"
    except ValueError:
        return "ERROR: Valor no numérico"

def iniciar_servidor_udp():
    # Creación del socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Enlace a todas las interfaces en el puerto 5001 (distinto a TCP)
    udp_socket.bind(('0.0.0.0', 5001))
    
    print("[SERVER UDP] Escuchando en puerto 5001 (Iterativo, un solo socket)...")

    while True:
        try:
            # Demultiplexación implícita: recvfrom() nos da datos y address
            data, addr = udp_socket.recvfrom(1024) 
            
            # Parsing del mensaje: ID_CLIENTE:OPERACIÓN:VALOR
            mensaje = data.decode('utf-8').strip()
            print(f"[UDP] Datagrama recibido desde {addr}")
            
            partes = mensaje.split(':')
            if len(partes) == 3:
                id_cliente, operacion, valor = partes
                
                # Requerimiento de asociación usando la tupla (IP, puerto)
                clientes_udp[addr] = id_cliente 
                print(f"[UDP] Cliente identificado: ID={id_cliente}, Addr={addr}")
                
                # Procesamiento y cálculo
                resultado = procesar_operacion(operacion, valor)
                
                # Formato de respuesta: <ID_CLIENTE>:<RESULTADO>
                respuesta = f"{id_cliente}:{resultado}"
                
                # Envío de respuesta usando la información de transporte (addr)
                udp_socket.sendto(respuesta.encode('utf-8'), addr)
            else:
                # Evento: Mensaje inválido
                error_msg = f"D4:ERROR: Formato inválido"
                udp_socket.sendto(error_msg.encode('utf-8'), addr)
                
        except Exception as e:
            print(f"[ERROR UDP] {e}")

if __name__ == "__main__":
    iniciar_servidor_udp()
