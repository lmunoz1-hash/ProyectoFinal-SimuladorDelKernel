
# ============================================================
# MODULO: ADMINISTRACION DE MEMORIA RAM
# ============================================================
# Este modulo simula una memoria RAM de 100 MB utilizando
# asignacion continua y el algoritmo First Fit.
#
# ORIGEN DE LOS DATOS:
# Los procesos son creados manualmente desde main.py.
#
# El programa principal proporciona:
# - PID: Identificador del proceso.
# - tamano: Memoria solicitada por el proceso en MB.
#
# Estos valores corresponden a los atributos pid y
# tamano_memoria del PCB definido en procesos.py.
#
# Este modulo NO crea procesos nuevos.
# Unicamente administra la memoria asociada a los PID
# que recibe desde el programa principal.
#
# IMPORTANTE:
# La relacion entre los PID y sus PCB es administrada
# por main.py. Este modulo mantiene su propio registro
# de asignaciones de memoria.
# ============================================================


class AdministradorMemoria:
    """
    Simula la administracion de 100 MB de memoria RAM.

    Utiliza asignacion continua y el algoritmo First Fit,
    que selecciona el primer bloque libre suficientemente
    grande para almacenar el proceso.

    Atributos:
        memoria_total: Capacidad total de RAM en MB.
        procesos: Diccionario de PID y memoria asignada.
        bloques: Distribucion de bloques libres y ocupados.
    """

    def __init__(self):

        # Capacidad fija de memoria RAM.
        self.memoria_total = 100

        # Registro de asignaciones de memoria.
        # Formato: {PID: cantidad_de_memoria}
        # No almacena objetos PCB completos.
        self.procesos = {}

        # Inicialmente toda la memoria esta disponible.
        # PID None indica que el bloque esta libre.
        self.bloques = [
            {"inicio": 0, "tamano": 100, "pid": None}
        ]

    def memoria_usada(self):
        """
        Calcula la cantidad total de memoria asignada.

        Suma los tamaños registrados para los procesos
        que actualmente ocupan memoria RAM.
        """

        return sum(self.procesos.values())

    def memoria_disponible(self):
        """
        Calcula la memoria RAM disponible.

        Resta la memoria utilizada de la capacidad total.
        """

        return self.memoria_total - self.memoria_usada()

    def asignar(self, pid, tamano):
        """
        Asigna memoria a un proceso existente.

        Parametros:
            pid: Identificador del proceso.
            tamano: Memoria solicitada en MB.

        Los datos deben ser proporcionados por main.py,
        tomando como referencia el PCB del proceso.

        Funcionamiento:
        1. Verifica que el PID no tenga memoria asignada.
        2. Valida que el tamaño solicitado sea positivo.
        3. Comprueba la memoria total disponible.
        4. Busca el primer bloque libre suficiente.
        5. Registra la asignacion utilizando el PID.

        Retorna True si la asignacion es exitosa.
        """

        # Evitar asignaciones duplicadas.
        if pid in self.procesos:
            print(f"ERROR: El proceso {pid} ya tiene memoria.")
            return False

        # Validar la cantidad de memoria solicitada.
        if tamano <= 0:
            print("ERROR: El tamano debe ser positivo.")
            return False

        # Verificar si existe suficiente RAM disponible.
        if tamano > self.memoria_disponible():
            print(
                f"ERROR: Out of Memory. "
                f"RAM disponible: {self.memoria_disponible()} MB"
            )
            return False

        # Aplicar el algoritmo First Fit.
        # Buscar el primer bloque libre suficientemente grande.
        for indice, bloque in enumerate(self.bloques):

            if bloque["pid"] is None and bloque["tamano"] >= tamano:

                # Guardar la posicion inicial del bloque.
                inicio = bloque["inicio"]

                # Calcular la memoria que quedara disponible.
                espacio_restante = bloque["tamano"] - tamano

                # Marcar el bloque como ocupado por el PID.
                bloque["tamano"] = tamano
                bloque["pid"] = pid

                # Si sobra espacio, crear un nuevo bloque libre.
                if espacio_restante > 0:
                    self.bloques.insert(
                        indice + 1,
                        {
                            "inicio": inicio + tamano,
                            "tamano": espacio_restante,
                            "pid": None
                        }
                    )

                # Registrar la memoria asignada al PID.
                self.procesos[pid] = tamano

                print(
                    f"Memoria asignada al PID {pid}: "
                    f"{tamano} MB | Inicio: {inicio} MB"
                )
                return True

        # La memoria libre puede estar dividida en bloques
        # pequeños que no permiten una asignacion continua.
        print(
            "ERROR: Out of Memory por fragmentacion externa. "
            "No existe un bloque continuo suficiente."
        )
        return False

    def liberar(self, pid):
        """
        Libera la memoria asignada a un proceso.

        Recibe el PID del proceso cuya memoria se liberara.

        Funcionamiento:
        1. Verifica que el PID tenga memoria asignada.
        2. Marca su bloque como libre.
        3. Elimina su registro de memoria.
        4. Fusiona bloques libres consecutivos.

        No elimina el PCB del programa principal.
        """

        # Verificar que exista una asignacion para el PID.
        if pid not in self.procesos:
            print(f"ERROR: Proceso {pid} no encontrado.")
            return False

        # Buscar el bloque ocupado y marcarlo como libre.
        for bloque in self.bloques:
            if bloque["pid"] == pid:
                bloque["pid"] = None
                break

        # Eliminar el registro de asignacion.
        del self.procesos[pid]

        # Fusionar bloques libres contiguos.
        indice = 0

        while indice < len(self.bloques) - 1:

            actual = self.bloques[indice]
            siguiente = self.bloques[indice + 1]

            # Si ambos bloques estan libres, unirlos.
            if actual["pid"] is None and siguiente["pid"] is None:
                actual["tamano"] += siguiente["tamano"]
                self.bloques.pop(indice + 1)

            else:
                indice += 1

        print(f"Memoria del proceso {pid} liberada.")
        return True

    def mostrar_estado(self):
        """
        Muestra el estado actual de la memoria RAM.

        Presenta:
        - Capacidad total.
        - Memoria utilizada.
        - Memoria disponible.
        - Distribucion de bloques libres y ocupados.

        Los bloques ocupados se identifican mediante
        el PID del proceso al que pertenecen.
        """

        print("\n===== ESTADO DE MEMORIA RAM =====")
        print(f"Memoria total: {self.memoria_total} MB")
        print(f"Memoria usada: {self.memoria_usada()} MB")
        print(f"Memoria libre: {self.memoria_disponible()} MB")

        print("\n===== MAPA DE MEMORIA =====")

        # Recorrer todos los bloques de memoria.
        for bloque in self.bloques:

            inicio = bloque["inicio"]
            fin = inicio + bloque["tamano"] - 1

            # Identificar si el bloque esta libre u ocupado.
            if bloque["pid"] is None:
                estado = "LIBRE"
            else:
                estado = f"PID {bloque['pid']}"

            # Mostrar el rango y tamaño del bloque.
            print(
                f"[{inicio:02d} - {fin:02d}] "
                f"{estado} | {bloque['tamano']} MB"
            )
