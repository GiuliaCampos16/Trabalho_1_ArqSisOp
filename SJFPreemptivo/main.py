import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comum"))

import Trace
from FilaQuantum import FilaIO, FilaProntos
from processoModel import Processo
from Simulador import SimuladorSJFPreemptivo
from GeradorProcessos import GeradorProcessos
from Relatorio import ImprimirTurnaround

MAX_PROCESSOS = 10
ARQUIVO_TRACE = "../visualizador/public/trace-sjf.json"

fila_prontos = FilaProntos()
fila_IO = FilaIO()

## exemplo do slide 11 (SRTF), serve para conferir se o algoritmo está correto
processosSlide: list[Processo] = [
    Processo(pid=1, chegada=0, tempo_cpu=8),
    Processo(pid=2, chegada=1, tempo_cpu=4),
    Processo(pid=3, chegada=2, tempo_cpu=9),
    Processo(pid=4, chegada=3, tempo_cpu=5),
]
## turnarounds esperados desse exemplo, média 13
# P1 - 17
# P2 - 4
# P3 - 24
# P4 - 7

if __name__ == "__main__":

    # SimuladorSJFPreemptivo(processosSlide, fila_prontos, fila_IO)

    gerador: GeradorProcessos = GeradorProcessos(MAX_PROCESSOS, max_eventos_io=2, tempo_cpu_min=5, tempo_cpu_max=30, chegada_min=0, chegada_max=10)
    processosGerados: list[Processo] = gerador.GerarProcessos()
    finalizados: list[Processo] = SimuladorSJFPreemptivo(processosGerados, fila_prontos, fila_IO)

    ImprimirTurnaround(finalizados)
    Trace.Salvar(ARQUIVO_TRACE)
