
class AdministradorDeadlock:
    """Simula dos recursos exclusivos y detecta espera circular."""

    def __init__(self):
        self.recursos = {1: None, 2: None}
        self.esperando = {}
        self.procesos = {}

    def registrar(self, proceso):
        if proceso.pid in self.procesos:
            print(f"ERROR: PID {proceso.pid} ya registrado.")
            return False

        self.procesos[proceso.pid] = proceso
        return True

    def solicitar(self, pid, recurso):
        if pid not in self.procesos:
            print("ERROR: Proceso no registrado.")
            return False

        proceso = self.procesos[pid]

        if proceso.estado in ("ABORTADO", "TERMINADO"):
            print(f"ERROR: PID {pid} no puede solicitar recursos.")
            return False

        if recurso not in self.recursos:
            print("ERROR: Recurso inexistente.")
            return False

        if self.recursos[recurso] == pid:
            print(f"PID {pid} ya posee recurso {recurso}.")
            return True

        if pid in self.esperando:
            print(
                f"ERROR: PID {pid} ya espera "
                f"recurso {self.esperando[pid]}."
            )
            return False

        propietario = self.recursos[recurso]

        if propietario is None:
            self.recursos[recurso] = pid
            print(f"PID {pid} obtiene recurso {recurso}.")
            return True

        self.esperando[pid] = recurso
        proceso.estado = "BLOQUEADO"
        print(f"PID {pid} espera recurso {recurso}.")
        return False

    def detectar(self):
        for pid, recurso in self.esperando.items():
            propietario = self.recursos[recurso]

            if propietario is None:
                continue

            recurso_esperado = self.esperando.get(propietario)

            if recurso_esperado is not None:
                if self.recursos[recurso_esperado] == pid:
                    print("\nALERTA: DEADLOCK DETECTADO")
                    print(f"PID {pid} espera a PID {propietario}.")
                    print(f"PID {propietario} espera a PID {pid}.")
                    return True

        print("\nNo se detectó deadlock.")
        return False

    def abortar(self, pid):
        if pid not in self.procesos:
            print("ERROR: Proceso no encontrado.")
            return False

        proceso = self.procesos[pid]

        if proceso.estado == "ABORTADO":
            print(f"ERROR: PID {pid} ya fue abortado.")
            return False

        proceso.estado = "ABORTADO"
        self.esperando.pop(pid, None)

        for recurso, propietario in self.recursos.items():
            if propietario == pid:
                self.recursos[recurso] = None
                print(f"Recurso {recurso} liberado.")

        for otro_pid, recurso in list(self.esperando.items()):
            if self.recursos[recurso] is None:
                self.esperando.pop(otro_pid)
                self.procesos[otro_pid].estado = "LISTO"
                print(f"PID {otro_pid} desbloqueado.")

        print(f"Proceso {pid} abortado.")
        return True
