
from dataclasses import dataclass


@dataclass
class PCB:
    """Bloque de Control de Proceso."""

    pid: int
    estado: str
    tamano_memoria: int
    rafaga_total: int
    rafaga_restante: int


def crear_proceso(pid: int, memoria: int, rafaga: int) -> PCB:
    """Crea un PCB con los datos iniciales del proceso."""

    if pid <= 0:
        raise ValueError("El PID debe ser positivo.")

    if memoria <= 0:
        raise ValueError("La memoria debe ser mayor que cero.")

    if rafaga <= 0:
        raise ValueError("La rafaga de CPU debe ser mayor que cero.")

    return PCB(
        pid=pid,
        estado="NUEVO",
        tamano_memoria=memoria,
        rafaga_total=rafaga,
        rafaga_restante=rafaga
    )
