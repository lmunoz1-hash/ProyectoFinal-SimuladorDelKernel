
# ============================================================
# PROYECTO FINAL: SIMULADOR DE FUNCIONES DEL KERNEL
# CURSO: SISTEMAS OPERATIVOS I
# ============================================================
#
# DESCRIPCION GENERAL:
# Este programa simula funciones fundamentales de un
# sistema operativo:
#
# 1. Creacion y administracion de procesos mediante PCB.
# 2. Planificacion de CPU utilizando Round Robin.
# 3. Administracion de memoria RAM mediante First Fit.
# 4. Concurrencia utilizando un semaforo binario.
# 5. Simulacion, deteccion y resolucion de Deadlock.
#
# INTEGRACION DE PROCESOS:
# Los procesos son ingresados manualmente por el usuario
# desde la opcion 1 del menu principal.
#
# Cada proceso se almacena en un diccionario llamado
# procesos, utilizando su PID como identificador.
#
# Los modulos de planificacion, semaforo y Deadlock
# reciben referencias a los mismos objetos PCB.
#
# El administrador de memoria utiliza el PID y la
# cantidad de memoria solicitada por cada proceso.
#
# IMPORTANTE:
# Las simulaciones del programa principal NO crean
# procesos de prueba independientes.
# ============================================================


# Importar la funcion encargada de crear los PCB.
from procesos import crear_proceso

# Importar el administrador de memoria RAM.
from memoria import AdministradorMemoria

# Importar el planificador Round Robin.
from planificador import PlanificadorRoundRobin

# Importar el semaforo binario.
from semaforo import SemaforoBinario

# Importar el administrador de Deadlock.
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

    """
    Simula la concurrencia utilizando dos procesos existentes.

    ORIGEN DE LOS PROCESOS:
    Los procesos provienen del diccionario central "procesos",
    donde fueron registrados manualmente desde la opcion 1.

    Funcionamiento:
    1. Identifica los procesos en estado LISTO.
    2. Solicita al usuario dos PID diferentes.
    3. Recupera los objetos PCB existentes.
    4. Simula el acceso a una seccion critica.
    5. Utiliza un semaforo binario para controlar
       el acceso a la variable compartida.
    6. Devuelve los procesos LISTOS a Round Robin.

    Esta funcion NO crea procesos adicionales.
    """

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

    # Recuperar los PCB originales del diccionario central.
    # No se crean nuevos procesos ni se duplican los existentes.

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

    """
    Simula un Deadlock utilizando procesos creados manualmente.

    ORIGEN DE LOS PROCESOS:
    Los procesos se obtienen del diccionario central
    "procesos", creado en la funcion main().

    Funcionamiento:
    1. Identifica los procesos que estan en estado LISTO.
    2. Solicita al usuario dos PID diferentes.
    3. Comprueba que ambos PID existan.
    4. Recupera los PCB originales.
    5. Registra esos PCB en el administrador de Deadlock.
    6. Asigna el recurso 1 al primer proceso.
    7. Asigna el recurso 2 al segundo proceso.
    8. Cada proceso solicita el recurso del otro.
    9. Ambos quedan BLOQUEADOS por espera circular.
    10. Retira los procesos de la cola de Round Robin.

    IMPORTANTE:
    Esta funcion NO crea procesos automaticamente.
    Utiliza los mismos objetos PCB registrados
    manualmente desde la opcion 1.

    La informacion del interbloqueo permanece en el
    administrador para su deteccion en la opcion 7.
    """

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

    # Obtener los PCB originales creados desde la opcion 1.
    # No se crean ni duplican procesos.
    # Los cambios de estado afectaran a la tabla PCB general.

    p1 = procesos[pid1]
    p2 = procesos[pid2]

    # Registrar las referencias a los mismos PCB existentes.
    # El administrador de Deadlock no crea otros procesos.

    gestor.registrar(p1)
    gestor.registrar(p2)

    # Asignar inicialmente un recurso a cada proceso.

    gestor.solicitar(pid1, 1)
    gestor.solicitar(pid2, 2)

    # Provocar la espera circular:
    # PID 1 espera el recurso que posee PID 2.
    # PID 2 espera el recurso que posee PID 1.

    gestor.solicitar(pid1, 2)
    gestor.solicitar(pid2, 1)

    planificador.retirar_proceso(pid1)
    planificador.retirar_proceso(pid2)

    print("\nDeadlock simulado correctamente.")
    print("Ambos procesos quedaron BLOQUEADOS.")


def resolver_deadlock(gestor, procesos, memoria, planificador):

    """
    Detecta y resuelve un Deadlock entre procesos existentes.

    ORIGEN DE LOS PROCESOS:
    Utiliza el mismo administrador de Deadlock que
    participo en la simulacion de la opcion 6.

    Los procesos registrados corresponden a los PCB
    creados manualmente desde la opcion 1.

    Funcionamiento:
    1. Detecta si existe una espera circular.
    2. Muestra los PID involucrados.
    3. Solicita al usuario seleccionar un PID.
    4. Aborta el proceso seleccionado.
    5. Libera los recursos que tenia asignados.
    6. Libera su memoria RAM.
    7. Reincorpora los procesos desbloqueados
       a la cola de Round Robin.
    8. Verifica que el Deadlock haya desaparecido.

    IMPORTANTE:
    Esta funcion NO crea procesos nuevos.
    Trabaja con los mismos PCB registrados
    durante la simulacion de Deadlock.
    """

    print("\n===== DETECCION Y RECUPERACION =====")

    # Consultar el mismo administrador utilizado en la opcion 6.
    # Se revisan las asignaciones y esperas existentes

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

        # Abortar el PCB original seleccionado por el usuario.
        # El administrador libera los recursos que posee
        # y actualiza los estados de los procesos afectados.
        
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
    """
    Funcion principal del simulador.

    Inicializa los administradores del sistema y mantiene
    el registro central de procesos durante toda la
    ejecucion del programa.
    """

    # Administrador de los 100 MB de memoria RAM.
    memoria = AdministradorMemoria()

    # Planificador de CPU con algoritmo Round Robin.
    planificador = PlanificadorRoundRobin()

    # Registro central de procesos creados manualmente.
    # Formato: {PID: objeto_PCB}
    #
    # Este diccionario permite que los distintos modulos
    # utilicen los mismos procesos y compartan sus estados.
    procesos = {}

    # Administrador de recursos y deteccion de Deadlock.
    gestor_deadlock = AdministradorDeadlock()

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            # =================================================
            # OPCION 1: CREACION MANUAL DE PROCESOS
            # =================================================
            # El usuario ingresa los datos del proceso.
            #
            # El PCB creado se almacena en el diccionario
            # central "procesos" y se utiliza posteriormente
            # en los demas modulos del simulador.
            # =================================================

            # Solicitar el identificador del proceso.
            pid = leer_entero_positivo("Ingrese PID: ")

            # Evitar identificadores duplicados.
            if pid in procesos:
                print("ERROR: Ese PID ya existe.")
                continue

            # Solicitar memoria y rafaga de CPU.
            tamano = leer_entero_positivo("Memoria (MB): ")
            rafaga = leer_entero_positivo("Rafaga CPU: ")

            # Crear el PCB con los datos ingresados.
            # No se generan procesos automaticamente.
            proceso = crear_proceso(pid, tamano, rafaga)

            # Solicitar memoria RAM para el mismo PID.
            if memoria.asignar(pid, tamano):

                # Cambiar el estado inicial a LISTO.
                proceso.estado = "LISTO"

                # Registrar el PCB en el diccionario central.
                procesos[pid] = proceso

                # Enviar la referencia del mismo PCB
                # al planificador Round Robin.
                planificador.agregar_proceso(proceso)

                print("Proceso creado correctamente.")

            else:
                # Rechazar el proceso si no hay memoria.
                print("Proceso rechazado por falta de memoria.")

        elif opcion == "2":
            # =================================================
            # OPCION 2: MOSTRAR PROCESOS Y PCB
            # =================================================
            # Muestra todos los procesos creados manualmente
            # desde la opcion 1 del menu principal.
            #
            # Los datos se obtienen directamente del
            # diccionario central "procesos".
            #
            # Los estados mostrados reflejan los cambios
            # realizados por los diferentes modulos.
            # =================================================

            print("\n===== TABLA DE PROCESOS PCB =====")

            # Verificar si existen procesos registrados.
            if not procesos:
                print("No hay procesos registrados.")

            # Recorrer los PCB almacenados.
            for p in procesos.values():
                print(
                    f"PID: {p.pid} | "
                    f"Estado: {p.estado} | "
                    f"RAM: {p.tamano_memoria} MB | "
                    f"CPU: {p.rafaga_restante}/{p.rafaga_total}"
                )

        elif opcion == "3":
            # =================================================
            # OPCION 3: PLANIFICACION ROUND ROBIN
            # =================================================
            # Ejecuta los procesos ingresados manualmente
            # que se encuentran en la cola de CPU.
            #
            # El planificador utiliza los mismos objetos
            # PCB almacenados en el programa principal.
            #
            # Cada proceso recibe un maximo de 3 unidades
            # de CPU por turno.
            # =================================================

            # Verificar que existan procesos en la cola.
            if not planificador.cola_listos:
                print("No hay procesos listos.")

            else:
                # Ejecutar el algoritmo Round Robin.
                planificador.ejecutar()

                # Revisar los estados actualizados de los PCB.
                for p in procesos.values():

                    # Liberar la RAM de procesos terminados.
                    if p.estado == "TERMINADO":

                        if p.pid in memoria.procesos:
                            memoria.liberar(p.pid)

        elif opcion == "4":
            # =================================================
            # OPCION 4: MOSTRAR MEMORIA RAM
            # =================================================
            # Presenta la distribucion de los 100 MB de RAM.
            #
            # Las asignaciones se identifican mediante los
            # PID de los procesos creados manualmente.
            #
            # El modulo memoria.py administra los bloques
            # utilizando el algoritmo First Fit.
            # =================================================

            # Mostrar memoria total, utilizada, disponible
            # y mapa de bloques libres y ocupados.
            memoria.mostrar_estado()

        elif opcion == "5":
            # =================================================
            # OPCION 5: CONCURRENCIA Y SEMAFORO
            # =================================================
            # Utiliza los procesos creados manualmente
            # desde la opcion 1 del menu principal.
            #
            # La funcion recibe el diccionario central
            # de procesos y el planificador existente.
            #
            # El usuario selecciona dos PID en estado LISTO.
            # No se crean procesos adicionales.
            # =================================================

            probar_semaforo(procesos, planificador)

        elif opcion == "6":
            # =================================================
            # OPCION 6: SIMULAR DEADLOCK
            # =================================================
            # Utiliza los PCB creados manualmente.
            #
            # La funcion simular_deadlock solicita dos PID
            # existentes y registra sus objetos PCB en el
            # administrador de Deadlock.
            #
            # Los mismos procesos solicitan dos recursos
            # exclusivos hasta producir una espera circular.
            #
            # Los cambios de estado se reflejan en la
            # tabla general de procesos.
            # =================================================

            # Evitar iniciar otra simulacion mientras
            # exista un Deadlock pendiente de resolver.
            if gestor_deadlock.detectar():
                print("ERROR: Primero resuelva el Deadlock actual.")

            else:
                # Preparar una nueva simulacion.
                # Se conserva la misma instancia para
                # utilizarla posteriormente en la opcion 7.
                gestor_deadlock = AdministradorDeadlock()

                # Simular utilizando los PCB existentes.
                simular_deadlock(
                    gestor_deadlock,
                    procesos,
                    planificador
                )

        elif opcion == "7":
            # =================================================
            # OPCION 7: DETECTAR Y RESOLVER DEADLOCK
            # =================================================
            # Utiliza el mismo administrador de Deadlock
            # que fue empleado en la opcion 6.
            #
            # No crea procesos ni recursos adicionales.
            #
            # Permite detectar la espera circular y
            # seleccionar manualmente el PID que sera
            # abortado para resolver el interbloqueo.
            #
            # Actualiza el estado del PCB original,
            # libera la memoria del proceso abortado y
            # reincorpora los procesos desbloqueados
            # a la cola de Round Robin.
            # =================================================

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
