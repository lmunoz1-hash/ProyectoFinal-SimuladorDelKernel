
class AdministradorMemoria:
    """Simula una RAM de 100 MB."""

    def __init__(self):
        self.memoria_total = 100
        self.procesos = {}

    def memoria_usada(self):
        return sum(self.procesos.values())

    def memoria_disponible(self):
        return self.memoria_total - self.memoria_usada()

    def asignar(self, pid, tamano):
        if pid in self.procesos:
            print(f"ERROR: El proceso {pid} ya tiene memoria.")
            return False

        if tamano <= 0:
            print("ERROR: El tamaño debe ser positivo.")
            return False

        if tamano > self.memoria_disponible():
            print(
                f"ERROR: Out of Memory. "
                f"RAM disponible: {self.memoria_disponible()} MB"
            )
            return False

        self.procesos[pid] = tamano
        print(f"Memoria asignada al proceso {pid}: {tamano} MB")
        return True

    def liberar(self, pid):
        if pid not in self.procesos:
            print(f"ERROR: Proceso {pid} no encontrado.")
            return False

        del self.procesos[pid]
        print(f"Memoria del proceso {pid} liberada.")
        return True

    def mostrar_estado(self):
        print("\n===== ESTADO DE MEMORIA RAM =====")
        print(f"Memoria total: {self.memoria_total} MB")
        print(f"Memoria usada: {self.memoria_usada()} MB")
        print(f"Memoria libre: {self.memoria_disponible()} MB")
