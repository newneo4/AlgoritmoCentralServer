import socket
import logging
import uuid
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class CentralizedClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = None
        self.client_id = str(uuid.uuid4())

    def connect(self):
        """Establecer conexión con el servidor"""
        try:
            logging.info(f"🔔 Proceso cliente {self.client_id[:8]} iniciando conexión")
            
            # Crear socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Conectar al servidor
            self.client_socket.connect((self.host, self.port))
            
            logging.info(f"✅ Conexión establecida con éxito (ID: {self.client_id[:8]})")
            return True
        
        except Exception as e:
            logging.error(f"❌ Error de conexión: {e}")
            return False

    def send_request(self, request):
        """Enviar solicitud al servidor"""
        try:
            # Loguear el envío de la solicitud
            logging.info(f"📤 Enviando comando: {request}")
            
            # Enviar solicitud
            self.client_socket.send(request.encode('utf-8'))
            
            # Recibir respuesta
            response = self.client_socket.recv(1024).decode('utf-8')
            
            # Loguear la respuesta
            logging.info(f"📥 Respuesta recibida: {response}")
            
            return response
        
        except Exception as e:
            logging.error(f"❗ Error al procesar solicitud: {e}")
            return None

    def close(self):
        """Cerrar conexión"""
        if self.client_socket:
            logging.info(f"🔚 Cerrando conexión del cliente {self.client_id[:8]}")
            self.client_socket.close()

def main():
    # Crear cliente
    client = CentralizedClient()
    
    try:
        # Conectar al servidor
        if not client.connect():
            return

        # Realizar operaciones de ejemplo
        operations = [
            "SET:usuario:Juan",
            "GET:usuario",
            "SET:edad:30",
            "GET:edad",
            "SET:ciudad:Madrid"
        ]

        # Ejecutar operaciones
        for op in operations:
            client.send_request(op)
            time.sleep(0.5)  # Pequeña pausa entre solicitudes

    except Exception as e:
        logging.error(f"❗ Error en operaciones del cliente: {e}")
    
    finally:
        # Cerrar conexión
        client.close()

if __name__ == "__main__":
    main()