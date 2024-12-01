import socket
import threading
import logging
from datetime import datetime
import uuid

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class CentralizedServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        
        # Almacén centralizado de datos
        self.centralized_data = {}
        
        # Lista de clientes y permisos
        self.clients = {}
        
        # Registro de accesos
        self.access_log = {}

    def generate_client_id(self):
        """Generar ID único para cada cliente"""
        return str(uuid.uuid4())

    def validate_access(self, client_id):
        """Simular validación de acceso"""
        # En un escenario real, aquí iría la lógica de autenticación
        return True

    def log_access_request(self, client_id, address):
        """Registrar solicitud de acceso"""
        timestamp = datetime.now()
        self.access_log[client_id] = {
            'address': address,
            'timestamp': timestamp,
            'status': 'Pendiente'
        }
        logging.info(f"🔔 Proceso {client_id[:8]} solicitando acceso desde {address}")

    def grant_access(self, client_id):
        """Conceder acceso al cliente"""
        if self.validate_access(client_id):
            self.access_log[client_id]['status'] = 'Autorizado'
            logging.info(f"✅ Permiso concedido al proceso {client_id[:8]}")
            return True
        else:
            self.access_log[client_id]['status'] = 'Denegado'
            logging.warning(f"❌ Acceso denegado al proceso {client_id[:8]}")
            return False

    def start(self):
        """Iniciar el servidor"""
        self.server_socket.listen()
        logging.info(f"🌐 Servidor centralizado iniciado en {self.host}:{self.port}")
        
        while True:
            # Aceptar nueva conexión de cliente
            client_socket, address = self.server_socket.accept()
            
            # Generar ID de cliente
            client_id = self.generate_client_id()
            
            # Registrar solicitud de acceso
            self.log_access_request(client_id, address)
            
            # Manejar cada cliente en un hilo separado
            client_thread = threading.Thread(
                target=self.handle_client, 
                args=(client_socket, client_id, address)
            )
            client_thread.start()

    def handle_client(self, client_socket, client_id, address):
        """Manejar las solicitudes de cada cliente"""
        try:
            # Conceder acceso
            if not self.grant_access(client_id):
                client_socket.close()
                return

            logging.info(f"🔗 Cliente {client_id[:8]} conectado desde {address}")
            
            while True:
                # Recibir mensaje del cliente
                message = client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                logging.info(f"📥 Procesando solicitud de {client_id[:8]}: {message}")
                
                # Procesar solicitud
                response = self.process_request(message)
                
                logging.info(f"📤 Enviando respuesta a {client_id[:8]}: {response}")
                
                # Enviar respuesta
                client_socket.send(response.encode('utf-8'))
        
        except Exception as e:
            logging.error(f"❗ Error con cliente {client_id[:8]}: {e}")
        
        finally:
            # Cerrar conexión del cliente
            logging.info(f"🔚 Desconectando cliente {client_id[:8]}")
            client_socket.close()

    def process_request(self, request):
        """Procesar solicitudes centralizadas"""
        parts = request.split(':')
        command = parts[0]

        logging.info(f"🔍 Analizando comando: {command}")

        if command == 'SET':
            key, value = parts[1], parts[2]
            self.centralized_data[key] = value
            return f"Dato guardado: {key} = {value}"
        
        elif command == 'GET':
            key = parts[1]
            value = self.centralized_data.get(key, "No encontrado")
            return f"Valor para {key}: {value}"
        
        else:
            logging.warning(f"⚠️ Comando no reconocido: {command}")
            return "Comando no reconocido"

def main():
    server = CentralizedServer()
    server.start()

if __name__ == "__main__":
    main()