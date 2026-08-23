import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comum"))

import Trace  # noqa: E402
from FilaQuantum import FilaIO, FilaQuantum  # noqa: E402
from processoModel import EventoIO, Processo, Prioridade, TipoIO  # noqa: E402
from Simulador import SimuladorIOMultiFila  # noqa: E402
from SimuladorTeste import SimuladorTeste  # noqa: E402
from GeradorProcessos import GeradorProcessos  # noqa: E402
from Relatorio import ImprimirTurnaround  # noqa: E402

MAX_PROCESSOS = 10
PROCESSOS_PADRAO = 3
ARQUIVO_TRACE = "../visualizador/public/trace-mlfq.json"

QUANTUM_ALTA = 2
QUANTUM_MEDIA = 4
QUANTUM_BAIXA = 6

# teste inicial de processos para abter com o exemplo da professora para montar o step-by-step inicial

processos: list[Processo] = [
    Processo(pid=1, chegada=0, tempo_cpu=5),
    Processo(pid=2, chegada=0, tempo_cpu=4),
    Processo(pid=3, chegada=1, tempo_cpu=8),
    Processo(pid=4, chegada=4, tempo_cpu=6),
]
# resultado esperado final desse exemplo de testes usando o simuladorTeste, algoritmo de exemplo da prof
# P1 - 11
# P2 - 13
# P3 - 23
# P4 - 21

# a ideia dessa classe é caso seja necessario criar mais ou menos filas colocar em uma estrtura/lista
filaQuantum_2 = FilaQuantum(2)
filaQuantum_4 = FilaQuantum(4)
filaQuantum_6 = FilaQuantum(6)

fila_IO = FilaIO()

filaQuantum_high = FilaQuantum(QUANTUM_ALTA)
filaQuantum_media = FilaQuantum(QUANTUM_MEDIA)
filaQuantum_low = FilaQuantum(QUANTUM_BAIXA)

processosIO: list[Processo] = [
    Processo(pid=1, chegada=0, tempo_cpu=5, prioridade=Prioridade.ALTA, eventos_io=[
             # tempo total deve ser 5 + 3 = 8
             EventoIO(tempo_cpu_disparo=2, tipo=TipoIO.DISCO)]),
    Processo(pid=2, chegada=0, tempo_cpu=4, prioridade=Prioridade.MEDIA,
             eventos_io=[EventoIO(tempo_cpu_disparo=1, tipo=TipoIO.FITA)]),
    # Processo(pid=3, chegada=1, tempo_cpu=8, prioridade=Prioridade.BAIXA, eventos_io=[EventoIO(tempo_cpu_disparo=3, tipo=TipoIO.IMPRESSORA)]),
]


def LerArgumentos():
    parser = argparse.ArgumentParser(
        description="Simulador de escalonamento por filas multiniveis com retroalimentacao")
    parser.add_argument("-p", "--processos", type=int, default=PROCESSOS_PADRAO,
                        help=f"quantidade de processos a gerar (padrao: {PROCESSOS_PADRAO}, maximo: {MAX_PROCESSOS})")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="semente aleatoria, para repetir exatamente a mesma simulacao")
    parser.add_argument("-t", "--trace", default=ARQUIVO_TRACE,
                        help="arquivo onde gravar o trace JSON")
    return parser.parse_args()


if __name__ == "__main__":

    # SimuladorTeste(processos, filaQuantum_2, filaQuantum_4, filaQuantum_6)

    # colocar input ou outro metodo de passar o tempo, pode colocar uma classe para fazer management de teste tambem, fica "mais modular"
    # SimuladorIOMultiFila(processosIO, [filaQuantum_high, filaQuantum_media, filaQuantum_low], fila_IO)  ## processo teste manual

    argumentos = LerArgumentos()

    gerador: GeradorProcessos = GeradorProcessos(
        MAX_PROCESSOS, max_eventos_io=2, tempo_cpu_min=5, tempo_cpu_max=30, chegada_min=0, chegada_max=10, seed=argumentos.seed)
    processosGerados: list[Processo] = gerador.GerarProcessos(
        argumentos.processos)
    finalizados: list[Processo] = SimuladorIOMultiFila(
        processosGerados, [filaQuantum_high, filaQuantum_media, filaQuantum_low], fila_IO)

    ImprimirTurnaround(finalizados)
    Trace.Salvar(argumentos.trace)
