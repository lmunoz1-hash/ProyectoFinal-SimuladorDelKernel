
from collections import deque


# ============================================================
# MODULO: CONCURRENCIA Y SEMAFORO BINARIO
# ============================================================
# Este modulo simula el acceso exclusivo de los procesos
# a una seccion critica mediante un semaforo binario.
#
# ORIGEN DE LOS PROCESOS:
# Los procesos son creados manualmente desde main.py
# mediante la opcion 1 del menu principal.
#
# El programa principal proporciona los objetos PCB
# existentes al semaforo.
#
# Este modulo NO crea procesos nuevos ni utiliza
# procesos de prueba independientes.
#
# Los cambios de estado realizados sobre cada PCB
# se reflejan en los mismos procesos administrados
# por el programa principal.
# ============================================================


class SemaforoBinario:
    """
    Simula un semaforo binario para controlar el acceso
    exclusivo a una seccion critica.

    Atributos:
        valor: 1 significa libre y 0 significa ocupado.
        propietario: PCB que actualmente posee el recurso.
        cola_espera: Procesos bloqueados esperando acceso.
        siguiente_turno: Proceso con acceso reservado.
        variable_compartida: Recurso protegido por el semaforo.
    """

    def __init__(self):

        # Inicialmente el semaforo esta disponible.
        self.valor = 1

        # Ningun proceso posee el recurso al inicio.
        self.propietario = None

        # Cola FIFO de procesos que esperan el recurso.
        self.cola_espera = deque()

        # Reserva el turno para el siguiente proceso.
        self.siguiente_turno = None

        # Variable protegida por la seccion critica.
        self.variable_compartida = 0

    def wait(self, proceso):
        """
        Solicita acceso exclusivo a la seccion critica.

        Recibe un objeto PCB creado previamente desde
        el menu principal.

        Funcionamiento:
        1. Comprueba si el proceso ya posee el semaforo.
        2. Rechaza procesos terminados o abortados.
        3. Si el recurso esta libre, permite el acceso.
        4. Si esta ocupado, bloquea el proceso.
        5. Respeta los turnos reservados.

        Retorna True si obtiene el recurso.
        """

        # Comprobar si el proceso ya es propietario.
        if proceso is self.propietario:
            print(f"PID {proceso.pid} ya posee el semáforo.")
            return True

        # Evitar el acceso de procesos finalizados.
        if proceso.estado in ("ABORTADO", "TERMINADO"):
            print(f"ERROR: PID {proceso.pid} no puede entrar.")
            return False

        # Verificar si el semaforo esta disponible.
        if self.valor == 1:

            # Respetar el turno reservado a otro proceso.
            if (
                self.siguiente_turno is not None
                and proceso is not self.siguiente_turno
            ):

                # Evitar duplicados en la cola de espera.
                if not any(p is proceso for p in self.cola_espera):
                    proceso.estado = "BLOQUEADO"
                    self.cola_espera.append(proceso)

                print(f"PID {proceso.pid} espera su turno.")
                return False

            # Ocupar el semaforo.
            self.valor = 0

            # Guardar la referencia al PCB propietario.
            self.propietario = proceso

            # Eliminar la reserva del turno anterior.
            self.siguiente_turno = None

            # Actualizar el estado del mismo PCB.
            proceso.estado = "EJECUTANDO"

            print(f"PID {proceso.pid} entra a la sección crítica.")
            return True

        # Verificar si el proceso ya esta esperando.
        if any(p is proceso for p in self.cola_espera):
            print(f"PID {proceso.pid} ya está en espera.")
            return False

        # Bloquear el proceso porque el recurso esta ocupado.
        proceso.estado = "BLOQUEADO"

        # Agregar el PCB a la cola de espera.
        self.cola_espera.append(proceso)

        print(f"PID {proceso.pid} bloqueado: semáforo ocupado.")
        return False

    def modificar_variable(self, proceso):
        """
        Modifica la variable compartida protegida.

        Solo el proceso propietario del semaforo
        puede acceder y modificar esta variable.

        La comparacion utiliza la identidad del PCB
        para verificar que sea el mismo proceso.
        """

        # Impedir modificaciones no autorizadas.
        if proceso is not self.propietario:
            print("ERROR: Acceso no autorizado a sección crítica.")
            return False

        # Simular una operacion sobre el recurso compartido.
        self.variable_compartida += 1

        print(
            f"PID {proceso.pid} incrementó la variable "
            f"a {self.variable_compartida}."
        )
        return True

    def signal(self, proceso):
        """
        Libera el semaforo ocupado por un proceso.

        Funcionamiento:
        1. Verifica que el proceso sea el propietario.
        2. Libera el recurso compartido.
        3. Cambia el estado del propietario a LISTO.
        4. Si existen procesos esperando, selecciona
           el primero de la cola.
        5. Reserva el siguiente turno para ese proceso.

        No crea procesos ni modifica sus identificadores.
        """

        # Solo el propietario puede liberar el recurso.
        if proceso is not self.propietario:
            print("ERROR: El proceso no posee el semáforo.")
            return False

        print(f"PID {proceso.pid} libera la sección crítica.")

        # Liberar el semaforo.
        self.propietario = None
        self.valor = 1

        # Actualizar el estado del PCB que libero el recurso.
        proceso.estado = "LISTO"

        # Verificar si existen procesos bloqueados.
        if self.cola_espera:

            # Obtener el primer proceso de la cola.
            siguiente = self.cola_espera.popleft()

            # Cambiar su estado a LISTO.
            siguiente.estado = "LISTO"

            # Reservar el recurso para este proceso.
            self.siguiente_turno = siguiente

            print(f"PID {siguiente.pid} sale de la cola de espera.")
            print(f"Turno reservado para PID {siguiente.pid}.")

        else:

            # No existen procesos pendientes.
            self.siguiente_turno = None

        return True
