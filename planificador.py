
from collections import deque


class PlanificadorRoundRobin:
    """Planificador Round Robin con quantum fijo de 3."""

    def __init__(self):
        self.quantum = 3
        self.cola_listos = deque()
        self.tiempo_actual = 0
        self.numero_ejecuciones = 0

    def agregar_proceso(self, proceso):
        if proceso.estado != "LISTO":
            print(f"Proceso {proceso.pid} no está listo.")
            return False

        self.cola_listos.append(proceso)
        print(f"Proceso {proceso.pid} agregado a la cola.")
        return True

    def ejecutar(self):
        if not self.cola_listos:
            print("\nNo hay procesos listos para ejecutar.")
            return

        self.numero_ejecuciones += 1

        # Guardar el tiempo antes de iniciar esta ejecución
        tiempo_inicio = self.tiempo_actual

        print("\n===== PLANIFICACION ROUND ROBIN =====")
        print(f"Quantum: {self.quantum}")
        print(f"Ejecucion numero: {self.numero_ejecuciones}")

        while self.cola_listos:
            proceso = self.cola_listos.popleft()

            proceso.estado = "EJECUTANDO"

            tiempo = min(
                self.quantum,
                proceso.rafaga_restante
            )

            print(f"\nTiempo actual: {self.tiempo_actual}")
            print(f"Ejecutando proceso PID {proceso.pid}")
            print(f"Tiempo asignado: {tiempo}")

            proceso.rafaga_restante -= tiempo
            self.tiempo_actual += tiempo

            if proceso.rafaga_restante == 0:
                proceso.estado = "TERMINADO"
                print(f"Proceso {proceso.pid} terminado.")

            else:
                proceso.estado = "LISTO"

                print(
                    f"PID {proceso.pid}: quedan "
                    f"{proceso.rafaga_restante} unidades."
                )

                print("Cambio de contexto simulado.")
                self.cola_listos.append(proceso)

        # Calcular el tiempo utilizado en esta ejecución
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
