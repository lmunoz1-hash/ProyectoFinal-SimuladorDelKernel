
from procesos import crear_proceso
from semaforo import SemaforoBinario


def main():
    print("===== PRUEBA DE CONCURRENCIA =====")

    p1 = crear_proceso(1, 10, 5)
    p2 = crear_proceso(2, 10, 5)

    semaforo = SemaforoBinario()

    print("\n1. Proceso 1 solicita el semáforo")
    semaforo.wait(p1)

    print("\n2. Proceso 2 solicita el semáforo")
    semaforo.wait(p2)

    print("\n3. Proceso 1 modifica la variable")
    semaforo.modificar_variable(p1)

    print("\n4. Proceso 2 intenta modificarla")
    semaforo.modificar_variable(p2)

    print("\n5. Proceso 1 libera el semáforo")
    semaforo.signal(p1)

    print("\n6. Proceso 2 vuelve a solicitar acceso")
    if semaforo.wait(p2):
        semaforo.modificar_variable(p2)
        semaforo.signal(p2)

    print("\n===== RESULTADO FINAL =====")
    print(f"Variable compartida: {semaforo.variable_compartida}")
    print(f"Semáforo disponible: {semaforo.valor == 1}")


if __name__ == "__main__":
    main()
