
from collections import deque


class SemaforoBinario:
    """Controla el acceso exclusivo a una sección crítica."""

    def __init__(self):
        self.valor = 1
        self.propietario = None
        self.cola_espera = deque()
        self.siguiente_turno = None
        self.variable_compartida = 0

    def wait(self, proceso):
        """Solicita acceso exclusivo a la sección crítica."""

        if proceso is self.propietario:
            print(f"PID {proceso.pid} ya posee el semáforo.")
            return True

        if proceso.estado in ("ABORTADO", "TERMINADO"):
            print(f"ERROR: PID {proceso.pid} no puede entrar.")
            return False

        if self.valor == 1:
            if (
                self.siguiente_turno is not None
                and proceso is not self.siguiente_turno
            ):
                if not any(p is proceso for p in self.cola_espera):
                    proceso.estado = "BLOQUEADO"
                    self.cola_espera.append(proceso)

                print(f"PID {proceso.pid} espera su turno.")
                return False

            self.valor = 0
            self.propietario = proceso
            self.siguiente_turno = None
            proceso.estado = "EJECUTANDO"

            print(f"PID {proceso.pid} entra a la sección crítica.")
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
        """Libera el semáforo y reserva el turno siguiente."""

        if proceso is not self.propietario:
            print("ERROR: El proceso no posee el semáforo.")
            return False

        print(f"PID {proceso.pid} libera la sección crítica.")

        self.propietario = None
        self.valor = 1
        proceso.estado = "LISTO"

        if self.cola_espera:
            siguiente = self.cola_espera.popleft()
            siguiente.estado = "LISTO"
            self.siguiente_turno = siguiente

            print(f"PID {siguiente.pid} sale de la cola de espera.")
            print(f"Turno reservado para PID {siguiente.pid}.")
        else:
            self.siguiente_turno = None

        return True
