from mpi4py import MPI
import time

# Inicialización de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def client():
    while True:
        # Enviar solicitud de acceso al servidor
        print(f"[Proceso {rank}] Enviando solicitud al servidor...")
        comm.send(rank, dest=0)  # Enviamos la solicitud al servidor (rank 0)
        
        # Esperar la respuesta del servidor (PERMISSION)
        msg = comm.recv(source=0)
        if msg == 'PERMISSION':
            print(f"[Proceso {rank}] Acceso concedido a la región crítica.")
            
            # Simulación de trabajo en la región crítica
            print(f"[Proceso {rank}] Está trabajando en la región crítica...")
            time.sleep(2)  # Simulamos el tiempo de trabajo
            print(f"[Proceso {rank}] Terminó el trabajo en la región crítica.")
            
            # Después de terminar, vuelve a solicitar acceso (este comportamiento se repite indefinidamente)
            # Esto es opcional, y depende de cómo quieras que se comporte el cliente (puedes poner un tiempo de espera para evitar loops innecesarios).

if __name__ == "__main__":
    client()
