
from collections import deque


class SemaforoBinario:
    """Controla el acceso a una sección crítica simulada."""

    def __init__(self):
        self.valor = 1
        self.propietario = None
        self.cola_espera = deque()
        self.variable_compartida = 0

    def wait(self, proceso):
        """Solicita acceso exclusivo a la sección crítica."""

        if self.valor == 1:
            self.valor = 0
            self.propietario = proceso
            proceso.estado = "EJECUTANDO"

            print(f"PID {proceso.pid} entra a la sección crítica.")
            return True

        if proceso is self.propietario:
            print(f"PID {proceso.pid} ya posee el semáforo.")
            return True

        if any(p is proceso for p in self.cola_espera):
            print(f"PID {proceso.pid} ya está en espera.")
            return False

        proceso.estado = "BLOQUEADO"
        self.cola_espera.append(proceso)

        print(f"PID {proceso.pid} bloqueado: semáforo ocupado.")
        return False

    def modificar_variable(self, proceso):
        """Solo el propietario puede modificar el recurso."""

        if proceso is not self.propietario:
            print("ERROR: Acceso no autorizado a sección crítica.")
            return False

        self.variable_compartida += 1

        print(
            f"PID {proceso.pid} incrementó la variable "
            f"a {self.variable_compartida}."
        )
        return True

    def signal(self, proceso):
        """Libera el semáforo y despierta al siguiente proceso."""

        if proceso is not self.propietario:
            print("ERROR: El proceso no posee el semáforo.")
            return False

        print(f"PID {proceso.pid} libera la sección crítica.")

        self.propietario = None
        self.valor = 1

        if self.cola_espera:
            siguiente = self.cola_espera.popleft()
            siguiente.estado = "LISTO"

            print(f"PID {siguiente.pid} sale de la cola de espera.")

        return True
