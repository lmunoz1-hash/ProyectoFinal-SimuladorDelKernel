
from collections import deque


# ============================================================
# MODULO: PLANIFICACION DE PROCESOS - ROUND ROBIN
# ============================================================
# Este modulo simula la planificacion de CPU utilizando
# el algoritmo Round Robin con un quantum fijo de 3.
#
# ORIGEN DE LOS PROCESOS:
# Los procesos son creados manualmente por el usuario
# desde el menu principal (main.py), mediante la opcion 1.
#
# Cada proceso tiene un PCB definido en procesos.py.
#
# El programa principal envia los procesos existentes
# al planificador mediante el metodo agregar_proceso().
#
# Este modulo NO crea procesos nuevos ni utiliza procesos
# de prueba independientes.
#
# Los cambios realizados al estado y a la rafaga restante
# se reflejan en los mismos objetos PCB administrados
# por el programa principal.
# ============================================================


class PlanificadorRoundRobin:
    """
    Implementa el algoritmo de planificacion Round Robin.

    Utiliza una cola FIFO para administrar los procesos
    que se encuentran en estado LISTO.

    Atributos:
        quantum: Tiempo maximo de CPU por turno.
        cola_listos: Cola de procesos pendientes.
        tiempo_actual: Tiempo total de CPU simulado.
        numero_ejecuciones: Cantidad de veces que se
                            ha ejecutado el planificador.
    """

    def __init__(self):

        # Quantum fijo de 3 unidades de tiempo.
        self.quantum = 3

        # Cola que almacena referencias a los PCB existentes.
        self.cola_listos = deque()

        # Tiempo acumulado de CPU.
        self.tiempo_actual = 0

        # Contador de ejecuciones del planificador.
        self.numero_ejecuciones = 0

    def agregar_proceso(self, proceso):
        """
        Agrega a la cola un proceso creado previamente.

        El parametro proceso corresponde a un PCB
        recibido desde el programa principal.

        Solo se admiten procesos en estado LISTO.
        """

        # Verificar que el proceso pueda ejecutarse.
        if proceso.estado != "LISTO":
            print(f"Proceso {proceso.pid} no está listo.")
            return False

        # Guardar la referencia al mismo PCB.
        self.cola_listos.append(proceso)

        print(f"Proceso {proceso.pid} agregado a la cola.")
        return True

    def retirar_proceso(self, pid):
        """
        Retira un proceso de la cola utilizando su PID.

        No elimina el PCB del programa principal.
        Unicamente lo retira de la cola de CPU.
        """

        # Guardar la cantidad inicial de procesos.
        cantidad_anterior = len(self.cola_listos)

        # Reconstruir la cola excluyendo el PID indicado.
        self.cola_listos = deque(
            proceso
            for proceso in self.cola_listos
            if proceso.pid != pid
        )

        # Confirmar si se retiro algun proceso.
        if len(self.cola_listos) < cantidad_anterior:
            print(f"PID {pid} retirado de la cola de CPU.")
            return True

        return False

    def ejecutar(self):
        """
        Ejecuta los procesos existentes en la cola.

        Funcionamiento:
        1. Obtiene el primer proceso de la cola.
        2. Cambia su estado a EJECUTANDO.
        3. Asigna un maximo de 3 unidades de CPU.
        4. Actualiza la rafaga restante.
        5. Si termina, cambia su estado a TERMINADO.
        6. Si no termina, regresa a la cola como LISTO.

        Los cambios se realizan sobre los mismos PCB
        que administra el programa principal.
        """

        # Verificar si existen procesos disponibles.
        if not self.cola_listos:
            print("\nNo hay procesos listos para ejecutar.")
            return

        # Registrar una nueva ejecucion.
        self.numero_ejecuciones += 1

        # Guardar el tiempo antes de iniciar.
        tiempo_inicio = self.tiempo_actual

        print("\n===== PLANIFICACION ROUND ROBIN =====")
        print(f"Quantum: {self.quantum}")
        print(f"Ejecucion numero: {self.numero_ejecuciones}")

        # Continuar mientras existan procesos en la cola.
        while self.cola_listos:

            # Obtener el primer proceso disponible.
            proceso = self.cola_listos.popleft()

            # Actualizar el estado del mismo PCB.
            proceso.estado = "EJECUTANDO"

            # Asignar como maximo el quantum disponible.
            tiempo = min(
                self.quantum,
                proceso.rafaga_restante
            )

            print(f"\nTiempo actual: {self.tiempo_actual}")
            print(f"Ejecutando proceso PID {proceso.pid}")
            print(f"Tiempo asignado: {tiempo}")

            # Actualizar el tiempo pendiente del proceso.
            proceso.rafaga_restante -= tiempo

            # Acumular el tiempo utilizado por la CPU.
            self.tiempo_actual += tiempo

            # Verificar si el proceso finalizo.
            if proceso.rafaga_restante == 0:

                # El PCB conserva su estado TERMINADO.
                proceso.estado = "TERMINADO"

                print(f"Proceso {proceso.pid} terminado.")

            else:

                # El proceso vuelve al estado LISTO.
                proceso.estado = "LISTO"

                print(
                    f"PID {proceso.pid}: quedan "
                    f"{proceso.rafaga_restante} unidades."
                )

                print("Cambio de contexto simulado.")

                # Reinsertar el mismo PCB al final de la cola.
                self.cola_listos.append(proceso)

        # Calcular el tiempo consumido en esta ejecucion.
        tiempo_ejecucion = self.tiempo_actual - tiempo_inicio

        print("\n===== RESULTADOS ROUND ROBIN =====")
        print("Todos los procesos de la cola terminaron.")

        print(
            f"Tiempo de esta ejecucion: "
            f"{tiempo_ejecucion} unidades"
        )

        print(
            f"Tiempo acumulado del sistema: "
            f"{self.tiempo_actual} unidades"
        )

        print(
            f"Total de ejecuciones realizadas: "
            f"{self.numero_ejecuciones}"
        )
