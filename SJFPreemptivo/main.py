import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comum"))

import Trace  # noqa: E402
from FilaQuantum import FilaIO, FilaProntos  # noqa: E402
from processoModel import Processo  # noqa: E402
from Simulador import SimuladorSJFPreemptivo  # noqa: E402
from GeradorProcessos import GeradorProcessos  # noqa: E402
from Relatorio import ImprimirGantt, ImprimirTurnaround  # noqa: E402

MAX_PROCESSOS = 10
PROCESSOS_PADRAO = 3
ARQUIVO_TRACE = "../visualizador/public/trace-sjf.json"

fila_prontos = FilaProntos()
fila_IO = FilaIO()

# exemplo do slide 11 (SRTF), serve para conferir se o algoritmo está correto
processosSlide: list[Processo] = [
    Processo(pid=1, chegada=0, tempo_cpu=8),
    Processo(pid=2, chegada=1, tempo_cpu=4),
    Processo(pid=3, chegada=2, tempo_cpu=9),
    Processo(pid=4, chegada=3, tempo_cpu=5),
]
# turnarounds esperados desse exemplo, média 13
# P1 - 17
# P2 - 4
# P3 - 24
# P4 - 7


def LerArgumentos():
    parser = argparse.ArgumentParser(
        description="Simulador de escalonamento SJF preemptivo (SRTF)")
    parser.add_argument("-p", "--processos", type=int, default=PROCESSOS_PADRAO,
                        help=f"quantidade de processos a gerar (padrao: {PROCESSOS_PADRAO}, maximo: {MAX_PROCESSOS})")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="semente aleatoria, para repetir exatamente a mesma simulacao")
    parser.add_argument("-t", "--trace", default=ARQUIVO_TRACE,
                        help="arquivo onde gravar o trace JSON")
    return parser.parse_args()


if __name__ == "__main__":

    # SimuladorSJFPreemptivo(processosSlide, fila_prontos, fila_IO)

    argumentos = LerArgumentos()

    gerador: GeradorProcessos = GeradorProcessos(
        MAX_PROCESSOS, max_eventos_io=2, tempo_cpu_min=5, tempo_cpu_max=30, chegada_min=0, chegada_max=10, seed=argumentos.seed)
    processosGerados: list[Processo] = gerador.GerarProcessos(
        argumentos.processos)
    finalizados: list[Processo] = SimuladorSJFPreemptivo(
        processosGerados, fila_prontos, fila_IO)

    ImprimirTurnaround(finalizados)
    ImprimirGantt(Trace.Dados())
    Trace.Salvar(argumentos.trace)
