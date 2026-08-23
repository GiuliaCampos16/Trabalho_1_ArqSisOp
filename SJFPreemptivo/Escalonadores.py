## Escalonador do SJF preemptivo (SRTF): escolhe sempre o processo com menor
## tempo de CPU restante. Empate fica com quem entrou antes na fila.

from FilaQuantum import FilaProntos
from processoModel import Processo, Status


def EscalonadorSJF(fila_prontos: FilaProntos) -> Processo:

    if len(fila_prontos.fila) == 0:
        return None

    processo = MenorTempoRestante(fila_prontos)
    fila_prontos.fila.remove(processo)
    processo.status = Status.EXECUTANDO

    print(f"Processo [P{processo.pid}] foi selecionado com {processo.TempoCpuRestante()} u.t. de CPU restante.\n")
    return processo


def MenorTempoRestante(fila_prontos: FilaProntos) -> Processo:

    if len(fila_prontos.fila) == 0:
        return None

    return min(fila_prontos.fila, key=lambda processo: processo.TempoCpuRestante())
