
from procesos import crear_proceso
from memoria import AdministradorMemoria
from planificador import PlanificadorRoundRobin


def main():
    print("====================================")
    print(" SIMULADOR DEL KERNEL - PROYECTO FINAL")
    print("====================================")

    memoria = AdministradorMemoria()
    planificador = PlanificadorRoundRobin()

    # Procesos de prueba
    procesos = [
        crear_proceso(1, 30, 8),
        crear_proceso(2, 40, 6),
        crear_proceso(3, 50, 9)
    ]

    # Admisión de procesos a memoria
    for proceso in procesos:
        print(f"\nIntentando cargar proceso {proceso.pid}")

        if memoria.asignar(
            proceso.pid,
            proceso.tamano_memoria
        ):
            proceso.estado = "LISTO"
            planificador.agregar_proceso(proceso)
        else:
            proceso.estado = "RECHAZADO"

    memoria.mostrar_estado()

    # Ejecutar planificación
    planificador.ejecutar()

    print("\n===== ESTADO FINAL DE PROCESOS =====")

    for proceso in procesos:
        print(
            f"PID {proceso.pid} | "
            f"Estado: {proceso.estado} | "
            f"Rafaga restante: {proceso.rafaga_restante}"
        )


if __name__ == "__main__":
    main()
