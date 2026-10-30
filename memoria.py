
class AdministradorMemoria:
    """Simula 100 MB de RAM con asignacion continua y First Fit."""

    def __init__(self):
        self.memoria_total = 100
        self.procesos = {}

        # Cada bloque contiene inicio, tamano y PID.
        # PID None significa que el bloque esta libre.
        self.bloques = [
            {"inicio": 0, "tamano": 100, "pid": None}
        ]

    def memoria_usada(self):
        return sum(self.procesos.values())

    def memoria_disponible(self):
        return self.memoria_total - self.memoria_usada()

    def asignar(self, pid, tamano):
        """Asigna el primer bloque libre suficientemente grande."""

        if pid in self.procesos:
            print(f"ERROR: El proceso {pid} ya tiene memoria.")
            return False

        if tamano <= 0:
            print("ERROR: El tamano debe ser positivo.")
            return False

        if tamano > self.memoria_disponible():
            print(
                f"ERROR: Out of Memory. "
                f"RAM disponible: {self.memoria_disponible()} MB"
            )
            return False

        # Buscar el primer bloque libre donde quepa el proceso.
        for indice, bloque in enumerate(self.bloques):
            if bloque["pid"] is None and bloque["tamano"] >= tamano:
                inicio = bloque["inicio"]
                espacio_restante = bloque["tamano"] - tamano

                # Convertir el bloque libre en bloque ocupado.
                bloque["tamano"] = tamano
                bloque["pid"] = pid

                # Crear otro bloque si queda espacio libre.
                if espacio_restante > 0:
                    self.bloques.insert(
                        indice + 1,
                        {
                            "inicio": inicio + tamano,
                            "tamano": espacio_restante,
                            "pid": None
                        }
                    )

                self.procesos[pid] = tamano

                print(
                    f"Memoria asignada al PID {pid}: "
                    f"{tamano} MB | Inicio: {inicio} MB"
                )
                return True

        # Puede existir RAM libre, pero fragmentada.
        print(
            "ERROR: Out of Memory por fragmentacion externa. "
            "No existe un bloque continuo suficiente."
        )
        return False

    def liberar(self, pid):
        """Libera la memoria y une bloques libres contiguos."""

        if pid not in self.procesos:
            print(f"ERROR: Proceso {pid} no encontrado.")
            return False

        for bloque in self.bloques:
            if bloque["pid"] == pid:
                bloque["pid"] = None
                break

        del self.procesos[pid]

        # Fusionar bloques libres consecutivos.
        indice = 0

        while indice < len(self.bloques) - 1:
            actual = self.bloques[indice]
            siguiente = self.bloques[indice + 1]

            if actual["pid"] is None and siguiente["pid"] is None:
                actual["tamano"] += siguiente["tamano"]
                self.bloques.pop(indice + 1)
            else:
                indice += 1

        print(f"Memoria del proceso {pid} liberada.")
        return True

    def mostrar_estado(self):
        """Muestra la capacidad y distribucion de la RAM."""

        print("\n===== ESTADO DE MEMORIA RAM =====")
        print(f"Memoria total: {self.memoria_total} MB")
        print(f"Memoria usada: {self.memoria_usada()} MB")
        print(f"Memoria libre: {self.memoria_disponible()} MB")

        print("\n===== MAPA DE MEMORIA =====")

        for bloque in self.bloques:
            inicio = bloque["inicio"]
            fin = inicio + bloque["tamano"] - 1

            if bloque["pid"] is None:
                estado = "LIBRE"
            else:
                estado = f"PID {bloque['pid']}"

            print(
                f"[{inicio:02d} - {fin:02d}] "
                f"{estado} | {bloque['tamano']} MB"
            )
