
# ============================================================
# MODULO: DETECCION Y RESOLUCION DE DEADLOCK
# ============================================================
# Este modulo simula la asignacion de dos recursos exclusivos
# y permite detectar situaciones de interbloqueo (Deadlock).
#
# ORIGEN DE LOS PROCESOS:
# Los procesos son creados manualmente por el usuario desde
# la opcion 1 del menu principal (main.py).
#
# El programa principal proporciona los objetos PCB
# existentes mediante el metodo registrar().
#
# Este modulo NO crea procesos nuevos ni utiliza procesos
# de prueba independientes.
#
# Los cambios de estado se realizan directamente sobre
# los PCB registrados, por lo que pueden reflejarse en
# la tabla general de procesos del programa principal.
#
# Las opciones 6 y 7 del menu principal deben utilizar
# la misma instancia de AdministradorDeadlock para
# conservar los recursos y procesos de la simulacion.
# ============================================================


class AdministradorDeadlock:
    """
    Administra la simulacion de interbloqueo.

    Utiliza dos recursos exclusivos identificados
    como recurso 1 y recurso 2.

    Atributos:
        recursos: Registra el PID propietario de cada recurso.
        esperando: Registra el recurso esperado por cada PID.
        procesos: Almacena referencias a los PCB registrados.
    """

    def __init__(self):

        # Recursos disponibles al iniciar la simulacion.
        # None significa que el recurso esta libre.
        self.recursos = {1: None, 2: None}

        # Procesos que esperan obtener un recurso.
        # Formato: {PID: recurso_solicitado}
        self.esperando = {}

        # Referencias a los PCB proporcionados por main.py.
        # Formato: {PID: objeto_PCB}
        self.procesos = {}

    def registrar(self, proceso):
        """
        Registra un proceso creado previamente.

        Recibe el objeto PCB existente desde main.py.

        No crea un proceso nuevo; solamente conserva
        una referencia al PCB recibido.

        Retorna True si el registro es exitoso.
        """

        # Evitar registrar dos veces el mismo PID.
        if proceso.pid in self.procesos:
            print(f"ERROR: PID {proceso.pid} ya registrado.")
            return False

        # Almacenar la referencia al PCB existente.
        self.procesos[proceso.pid] = proceso
        return True

    def solicitar(self, pid, recurso):
        """
        Simula la solicitud de un recurso exclusivo.

        Parametros:
            pid: Identificador de un proceso registrado.
            recurso: Recurso solicitado (1 o 2).

        Funcionamiento:
        1. Comprueba que el proceso exista.
        2. Verifica que pueda solicitar recursos.
        3. Comprueba que el recurso sea valido.
        4. Si esta libre, lo asigna al PID.
        5. Si esta ocupado, bloquea al proceso.

        Retorna True si obtiene el recurso.
        """

        # Verificar que el PID este registrado.
        if pid not in self.procesos:
            print("ERROR: Proceso no registrado.")
            return False

        # Obtener el mismo PCB registrado anteriormente.
        proceso = self.procesos[pid]

        # Impedir solicitudes de procesos finalizados.
        if proceso.estado in ("ABORTADO", "TERMINADO"):
            print(f"ERROR: PID {pid} no puede solicitar recursos.")
            return False

        # Validar el identificador del recurso.
        if recurso not in self.recursos:
            print("ERROR: Recurso inexistente.")
            return False

        # Comprobar si el proceso ya posee el recurso.
        if self.recursos[recurso] == pid:
            print(f"PID {pid} ya posee recurso {recurso}.")
            return True

        # Evitar solicitudes simultaneas de otros recursos
        # cuando el proceso ya se encuentra esperando.
        if pid in self.esperando:
            print(
                f"ERROR: PID {pid} ya espera "
                f"recurso {self.esperando[pid]}."
            )
            return False

        # Identificar al propietario actual del recurso.
        propietario = self.recursos[recurso]

        # Asignar el recurso si se encuentra disponible.
        if propietario is None:
            self.recursos[recurso] = pid
            print(f"PID {pid} obtiene recurso {recurso}.")
            return True

        # Si el recurso esta ocupado, registrar la espera.
        self.esperando[pid] = recurso

        # Actualizar el estado del PCB a BLOQUEADO.
        proceso.estado = "BLOQUEADO"

        print(f"PID {pid} espera recurso {recurso}.")
        return False

    def detectar(self):
        """
        Detecta una espera circular entre dos procesos.

        Ejemplo:
            PID 1 posee recurso 1 y espera recurso 2.
            PID 2 posee recurso 2 y espera recurso 1.

        Si ambos procesos esperan recursos que posee
        el otro, se identifica un Deadlock.

        Retorna True cuando encuentra el interbloqueo.
        """

        # Recorrer los procesos que esperan recursos.
        for pid, recurso in self.esperando.items():

            # Identificar quien posee el recurso solicitado.
            propietario = self.recursos[recurso]

            # Si el recurso esta libre, continuar.
            if propietario is None:
                continue

            # Verificar si el propietario tambien espera.
            recurso_esperado = self.esperando.get(propietario)

            if recurso_esperado is not None:

                # Comprobar si existe una espera circular.
                if self.recursos[recurso_esperado] == pid:

                    print("\nALERTA: DEADLOCK DETECTADO")
                    print(f"PID {pid} espera a PID {propietario}.")
                    print(f"PID {propietario} espera a PID {pid}.")
                    return True

        # No se encontro una espera circular.
        print("\nNo se detectó deadlock.")
        return False

    def abortar(self, pid):
        """
        Resuelve el interbloqueo abortando un proceso.

        Funcionamiento:
        1. Verifica que el proceso exista.
        2. Cambia su estado a ABORTADO.
        3. Elimina sus solicitudes pendientes.
        4. Libera los recursos que posee.
        5. Desbloquea procesos cuyos recursos
           solicitados quedaron disponibles.

        El PCB original conserva el estado ABORTADO.
        """

        # Verificar que el PID este registrado.
        if pid not in self.procesos:
            print("ERROR: Proceso no encontrado.")
            return False

        # Obtener el PCB registrado.
        proceso = self.procesos[pid]

        # Evitar abortar nuevamente el mismo proceso.
        if proceso.estado == "ABORTADO":
            print(f"ERROR: PID {pid} ya fue abortado.")
            return False

        # Actualizar el estado del PCB original.
        proceso.estado = "ABORTADO"

        # Eliminar solicitudes pendientes del proceso.
        self.esperando.pop(pid, None)

        # Liberar los recursos que pertenecen al PID.
        for recurso, propietario in self.recursos.items():

            if propietario == pid:
                self.recursos[recurso] = None
                print(f"Recurso {recurso} liberado.")

        # Revisar si otros procesos pueden desbloquearse.
        for otro_pid, recurso in list(self.esperando.items()):

            # Si el recurso solicitado quedo disponible,
            # retirar al proceso de la lista de espera.
            if self.recursos[recurso] is None:

                self.esperando.pop(otro_pid)

                # Actualizar el estado del PCB existente.
                self.procesos[otro_pid].estado = "LISTO"

                print(f"PID {otro_pid} desbloqueado.")

        print(f"Proceso {pid} abortado.")
        return True
