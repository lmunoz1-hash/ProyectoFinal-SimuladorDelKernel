
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


def probar_semaforo():
    print("\n===== SIMULACION DE CONCURRENCIA =====")

    p1 = crear_proceso(101, 10, 5)
    p2 = crear_proceso(102, 10, 5)
    semaforo = SemaforoBinario()

    semaforo.wait(p1)
    semaforo.wait(p2)

    semaforo.modificar_variable(p1)
    semaforo.modificar_variable(p2)

    semaforo.signal(p1)

    if semaforo.wait(p2):
        semaforo.modificar_variable(p2)
        semaforo.signal(p2)

    print("\nVariable compartida:",
          semaforo.variable_compartida)


def simular_deadlock(gestor):
    print("\n===== SIMULACION DE DEADLOCK =====")

    p1 = crear_proceso(201, 10, 5)
    p2 = crear_proceso(202, 10, 5)

    gestor.registrar(p1)
    gestor.registrar(p2)

    gestor.solicitar(201, 1)
    gestor.solicitar(202, 2)

    gestor.solicitar(201, 2)
    gestor.solicitar(202, 1)

    print("\nDeadlock simulado correctamente.")


def resolver_deadlock(gestor):
    print("\n===== DETECCION Y RECUPERACION =====")

    if gestor.detectar():
        print("\nResolviendo mediante aborto del PID 202...")
        gestor.abortar(202)

        print("\nVerificando nuevamente:")
        gestor.detectar()
    else:
        print("No es necesario realizar recuperacion.")


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
            probar_semaforo()

        elif opcion == "6":
            gestor_deadlock = AdministradorDeadlock()
            simular_deadlock(gestor_deadlock)

        elif opcion == "7":
            resolver_deadlock(gestor_deadlock)

        elif opcion == "0":
            print("\nCerrando simulador del kernel...")
            break

        else:
            print("ERROR: Opcion no valida.")


if __name__ == "__main__":
    main()
