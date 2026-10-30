
from procesos import crear_proceso
from memoria import AdministradorMemoria
from planificador import PlanificadorRoundRobin
from semaforo import SemaforoBinario
from deadlock import AdministradorDeadlock


def mostrar_menu():
    print("\n========================================")
    print("     SIMULADOR DE FUNCIONES DEL KERNEL")
    print("          SISTEMAS OPERATIVOS I")
    print("========================================")
    print("1. Crear nuevo proceso")
    print("2. Mostrar procesos y PCB")
    print("3. Ejecutar Round Robin (q = 3)")
    print("4. Mostrar memoria RAM")
    print("5. Simular concurrencia y semaforo")
    print("6. Simular Deadlock")
    print("7. Detectar y resolver Deadlock")
    print("0. Salir")


def leer_entero_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("ERROR: Ingrese un numero mayor que cero.")
        except ValueError:
            print("ERROR: Debe ingresar un numero entero.")



def probar_semaforo(procesos, planificador):
    print("\n===== SIMULACION DE CONCURRENCIA =====")

    disponibles = [
        p for p in procesos.values()
        if p.estado == "LISTO"
    ]

    if len(disponibles) < 2:
        print("ERROR: Se necesitan al menos dos procesos LISTOS.")
        return

    print("\nProcesos disponibles:")
    for p in disponibles:
        print(f"PID {p.pid} | Estado: {p.estado}")

    pid1 = leer_entero_positivo("\nIngrese el primer PID: ")
    pid2 = leer_entero_positivo("Ingrese el segundo PID: ")

    if pid1 == pid2:
        print("ERROR: Debe seleccionar dos procesos diferentes.")
        return

    if (
        pid1 not in procesos
        or pid2 not in procesos
        or procesos[pid1].estado != "LISTO"
        or procesos[pid2].estado != "LISTO"
    ):
        print("ERROR: Seleccione dos procesos LISTOS existentes.")
        return

    p1 = procesos[pid1]
    p2 = procesos[pid2]

    semaforo = SemaforoBinario()

    # Retirar temporalmente ambos procesos de Round Robin.
    planificador.retirar_proceso(pid1)
    planificador.retirar_proceso(pid2)

    # Primer proceso obtiene el semaforo.
    semaforo.wait(p1)

    # Segundo proceso queda bloqueado.
    semaforo.wait(p2)

    # Solo el propietario puede modificar la variable.
    semaforo.modificar_variable(p1)
    semaforo.modificar_variable(p2)

    # Primer proceso libera el semaforo.
    semaforo.signal(p1)

    # Segundo proceso obtiene su turno.
    if semaforo.wait(p2):
        semaforo.modificar_variable(p2)
        semaforo.signal(p2)

    # Ambos procesos regresan a la cola de CPU.
    for p in (p1, p2):
        if p.estado == "LISTO":
            planificador.agregar_proceso(p)

    print("\nVariable compartida:",
          semaforo.variable_compartida)

    print("Simulacion de concurrencia finalizada.")


def simular_deadlock(gestor, procesos, planificador):
    print("\n===== SIMULACION DE DEADLOCK =====")

    disponibles = [
        p for p in procesos.values()
        if p.estado == "LISTO"
    ]

    if len(disponibles) < 2:
        print("ERROR: Se necesitan al menos dos procesos LISTOS.")
        return

    print("\nProcesos disponibles:")
    for p in disponibles:
        print(f"PID {p.pid} | Estado: {p.estado}")

    pid1 = leer_entero_positivo("\nIngrese el primer PID: ")
    pid2 = leer_entero_positivo("Ingrese el segundo PID: ")

    if pid1 == pid2:
        print("ERROR: Debe seleccionar dos procesos diferentes.")
        return

    if (
        pid1 not in procesos
        or pid2 not in procesos
        or procesos[pid1].estado != "LISTO"
        or procesos[pid2].estado != "LISTO"
    ):
        print("ERROR: Seleccione dos procesos LISTOS existentes.")
        return

    p1 = procesos[pid1]
    p2 = procesos[pid2]

    gestor.registrar(p1)
    gestor.registrar(p2)

    gestor.solicitar(pid1, 1)
    gestor.solicitar(pid2, 2)

    gestor.solicitar(pid1, 2)
    gestor.solicitar(pid2, 1)

    planificador.retirar_proceso(pid1)
    planificador.retirar_proceso(pid2)

    print("\nDeadlock simulado correctamente.")
    print("Ambos procesos quedaron BLOQUEADOS.")


def resolver_deadlock(gestor, procesos, memoria, planificador):
    print("\n===== DETECCION Y RECUPERACION =====")

    if not gestor.detectar():
        print("No es necesario realizar recuperacion.")
        return

    print("\nProcesos involucrados en el Deadlock:")

    for pid in gestor.esperando:
        print(f"PID {pid}")

    while True:
        pid = leer_entero_positivo(
            "\nIngrese el PID que desea abortar: "
        )

        if pid not in gestor.esperando:
            print(
                "ERROR: Seleccione un proceso "
                "involucrado en el Deadlock."
            )
            continue

        print(f"\nResolviendo mediante aborto del PID {pid}...")

        if not gestor.abortar(pid):
            print("ERROR: No se pudo abortar el proceso.")
            return

        # El proceso abortado no debe volver a ejecutarse.
        planificador.retirar_proceso(pid)

        # Liberar la memoria RAM del proceso abortado.
        if pid in memoria.procesos:
            memoria.liberar(pid)

        # Reincorporar los procesos que quedaron LISTOS.
        for proceso in gestor.procesos.values():
            if proceso.estado == "LISTO":
                if not any(
                    p.pid == proceso.pid
                    for p in planificador.cola_listos
                ):
                    planificador.agregar_proceso(proceso)

        break

    print("\nVerificando nuevamente:")
    gestor.detectar()


def main():
    memoria = AdministradorMemoria()
    planificador = PlanificadorRoundRobin()
    procesos = {}
    gestor_deadlock = AdministradorDeadlock()

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            pid = leer_entero_positivo("Ingrese PID: ")

            if pid in procesos:
                print("ERROR: Ese PID ya existe.")
                continue

            tamano = leer_entero_positivo("Memoria (MB): ")
            rafaga = leer_entero_positivo("Rafaga CPU: ")

            proceso = crear_proceso(pid, tamano, rafaga)

            if memoria.asignar(pid, tamano):
                proceso.estado = "LISTO"
                procesos[pid] = proceso
                planificador.agregar_proceso(proceso)
                print("Proceso creado correctamente.")
            else:
                print("Proceso rechazado por falta de memoria.")

        elif opcion == "2":
            print("\n===== TABLA DE PROCESOS PCB =====")

            if not procesos:
                print("No hay procesos registrados.")

            for p in procesos.values():
                print(
                    f"PID: {p.pid} | "
                    f"Estado: {p.estado} | "
                    f"RAM: {p.tamano_memoria} MB | "
                    f"CPU: {p.rafaga_restante}/{p.rafaga_total}"
                )

        elif opcion == "3":
            if not planificador.cola_listos:
                print("No hay procesos listos.")
            else:
                planificador.ejecutar()

                for p in procesos.values():
                    if p.estado == "TERMINADO":
                        if p.pid in memoria.procesos:
                            memoria.liberar(p.pid)

        elif opcion == "4":
            memoria.mostrar_estado()

        elif opcion == "5":
            probar_semaforo(procesos, planificador)

        elif opcion == "6":
            if gestor_deadlock.detectar():
                print("ERROR: Primero resuelva el Deadlock actual.")
            else:
                gestor_deadlock = AdministradorDeadlock()
                simular_deadlock(
                    gestor_deadlock,
                    procesos,
                    planificador
                )

        elif opcion == "7":
            resolver_deadlock(
                gestor_deadlock,
                procesos,
                memoria,
                planificador
            )

        elif opcion == "0":
            print("\nCerrando simulador del kernel...")
            break

        else:
            print("ERROR: Opcion no valida.")


if __name__ == "__main__":
    main()
