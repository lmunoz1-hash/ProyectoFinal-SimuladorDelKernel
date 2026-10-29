
from procesos import crear_proceso
from deadlock import AdministradorDeadlock


def main():
    print("===== SIMULACION DE DEADLOCK =====")

    p1 = crear_proceso(1, 10, 5)
    p2 = crear_proceso(2, 10, 5)

    gestor = AdministradorDeadlock()
    gestor.registrar(p1)
    gestor.registrar(p2)

    print("\n1. Asignación inicial")
    gestor.solicitar(1, 1)
    gestor.solicitar(2, 2)

    print("\n2. Crear espera circular")
    gestor.solicitar(1, 2)
    gestor.solicitar(2, 1)

    print("\n3. Detectar deadlock")
    gestor.detectar()

    print("\n4. Resolver abortando PID 2")
    gestor.abortar(2)

    print("\n5. Comprobar resolución")
    gestor.detectar()

    print("\n6. PID 1 solicita recurso liberado")
    gestor.solicitar(1, 2)

    print("\n===== ESTADO FINAL =====")
    print(f"Proceso 1: {p1.estado}")
    print(f"Proceso 2: {p2.estado}")
    print(f"Recursos: {gestor.recursos}")


if __name__ == "__main__":
    main()
