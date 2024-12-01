from mpi4py import MPI

# Inicialización de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Cola de solicitudes de los procesos
request_queue = []

def server():
    while True:
        # Esperar a recibir solicitudes de acceso
        for i in range(size - 1):  # Ignorar la solicitud del propio servidor
            msg = comm.recv(source=MPI.ANY_SOURCE)
            sender = msg[0]  # 'msg' es una lista, tomamos el primer elemento (el rank)
            print(f"[Servidor] Recibida solicitud de acceso de proceso {sender}")
            request_queue.append(sender)

        # Conceder acceso a la región crítica al primer proceso de la cola
        if request_queue:
            next_process = request_queue.pop(0)
            print(f"[Servidor] Concediendo acceso al proceso {next_process}")
            comm.send('PERMISSION', dest=next_process)

        # Si hay procesos esperando, liberar la región crítica después de que el proceso termine
        # Este código es un ejemplo simplificado, en un caso real, el servidor esperaría que los procesos informen de su finalización.

if rank == 0:
    # El servidor ejecuta este código
    server()
else:
    # Los clientes (procesos que desean acceder a la región crítica)
    while True:
        # Enviar solicitud de acceso al servidor
        print(f"[Proceso {rank}] Enviando solicitud al servidor...")
        comm.send([rank], dest=0)  # Enviamos una lista con el rank del cliente
        
        # Esperar la respuesta del servidor
        msg = comm.recv(source=0)
        if msg == 'PERMISSION':
            print(f"[Proceso {rank}] Acceso concedido a la región crítica.")
            # Aquí se simula el trabajo en la región crítica
            print(f"[Proceso {rank}] Está trabajando en la región crítica...")
            # Simulamos un poco de trabajo
            import time
            time.sleep(2)
            print(f"[Proceso {rank}] Terminó el trabajo en la región crítica.")
