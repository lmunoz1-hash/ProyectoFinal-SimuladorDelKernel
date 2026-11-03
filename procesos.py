
from dataclasses import dataclass


# ============================================================
# MODULO: GESTION DE PROCESOS
# ============================================================
# Este modulo define la estructura PCB (Bloque de Control de
# Proceso) y permite crear procesos con los datos ingresados
# manualmente por el usuario desde el menu principal.
#
# Los procesos creados se almacenan en main.py y pueden ser
# utilizados por los demas modulos del simulador.
#
# Este modulo NO genera procesos automaticamente.
# ============================================================


@dataclass
class PCB:
    """
    Bloque de Control de Proceso (PCB).

    Almacena la informacion necesaria para identificar
    y administrar cada proceso dentro del simulador.

    Atributos:
        pid: Identificador unico del proceso.
        estado: Estado actual del proceso.
        tamano_memoria: Memoria solicitada en MB.
        rafaga_total: Tiempo total de CPU requerido.
        rafaga_restante: Tiempo de CPU pendiente.

    Los demas modulos pueden consultar o modificar estos
    atributos segun las operaciones realizadas.
    """

    pid: int
    estado: str
    tamano_memoria: int
    rafaga_total: int
    rafaga_restante: int


def crear_proceso(pid: int, memoria: int, rafaga: int) -> PCB:
    """
    Crea un proceso utilizando los datos proporcionados
    manualmente por el usuario.

    Parametros:
        pid: Identificador ingresado por el usuario.
        memoria: Cantidad de memoria solicitada.
        rafaga: Tiempo de CPU requerido.

    Funcionamiento:
        1. Valida que los valores sean positivos.
        2. Crea el PCB con estado inicial NUEVO.
        3. Devuelve el PCB al programa principal.

    El programa main.py administra los procesos creados
    y proporciona sus referencias a los demas modulos.
    """

    # Validar que el identificador sea positivo.
    if pid <= 0:
        raise ValueError("El PID debe ser positivo.")

    # Validar que la memoria solicitada sea mayor que cero.
    if memoria <= 0:
        raise ValueError("La memoria debe ser mayor que cero.")

    # Validar que la rafaga de CPU sea mayor que cero.
    if rafaga <= 0:
        raise ValueError("La rafaga de CPU debe ser mayor que cero.")

    # Crear y devolver el PCB con los datos ingresados.
    # El proceso inicia en estado NUEVO y su rafaga
    # restante es igual a la rafaga total.
    return PCB(
        pid=pid,
        estado="NUEVO",
        tamano_memoria=memoria,
        rafaga_total=rafaga,
        rafaga_restante=rafaga
    )
