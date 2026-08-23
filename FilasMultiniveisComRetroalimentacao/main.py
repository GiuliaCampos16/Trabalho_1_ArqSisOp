## essas coisas vão ser definidas pelo usuario na entrada posteriormente
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comum"))

from FilaQuantum import FilaIO, FilaQuantum
from processoModel import EventoIO, Processo, Prioridade, TipoIO
from Simulador import SimuladorIOMultiFila
from SimuladorTeste import SimuladorTeste
from GeradorProcessos import GeradorProcessos
from Relatorio import ImprimirTurnaround
import Trace

MAX_PROCESSOS = 10 ## poderia ser requisitado do usuario
ARQUIVO_TRACE = "../visualizador/public/trace-mlfq.json"

QUANTUM_ALTA = 2
QUANTUM_MEDIA = 4
QUANTUM_BAIXA = 6

## teste inicial de processos para abter com o exemplo da professora para montar o step-by-step inicial

processos : list[Processo] = [
    Processo(pid=1, chegada=0, tempo_cpu=5),
    Processo(pid=2, chegada=0, tempo_cpu=4),
    Processo(pid=3, chegada=1, tempo_cpu=8),
    Processo(pid=4, chegada=4, tempo_cpu=6),
]
## resultado esperado final desse exemplo de testes usando o simuladorTeste, algoritmo de exemplo da prof
# P1 - 11
# P2 - 13
# P3 - 23
# P4 - 21

## a ideia dessa classe é caso seja necessario criar mais ou menos filas colocar em uma estrtura/lista
filaQuantum_2 = FilaQuantum(2)
filaQuantum_4 = FilaQuantum(4)
filaQuantum_6 = FilaQuantum(6)

fila_IO = FilaIO()

filaQuantum_high    = FilaQuantum(QUANTUM_ALTA) ## 2 de quantum
filaQuantum_low     = FilaQuantum(5) ## 5 de quantum

processosIO : list[Processo] = [
    Processo(pid=1, chegada=0, tempo_cpu=5, prioridade=Prioridade.ALTA, eventos_io=[EventoIO(tempo_cpu_disparo=2, tipo=TipoIO.DISCO)]), ## tempo total deve ser 5 + 3 = 8
    Processo(pid=2, chegada=0, tempo_cpu=4, prioridade=Prioridade.MEDIA, eventos_io=[EventoIO(tempo_cpu_disparo=1, tipo=TipoIO.FITA)]),
    # Processo(pid=3, chegada=1, tempo_cpu=8, prioridade=Prioridade.BAIXA, eventos_io=[EventoIO(tempo_cpu_disparo=3, tipo=TipoIO.IMPRESSORA)]),
]

if __name__ == "__main__":

    ## TODO: criar um criador automatico de processos e randomizar tempos de CPU e tempos de IO

    # SimuladorTeste(processos, filaQuantum_2, filaQuantum_4, filaQuantum_6)

    ## colocar input ou outro metodo de passar o tempo, pode colocar uma classe para fazer management de teste tambem, fica "mais modular"
    # SimuladorIOMultiFila(processosIO, filaQuantum_high, filaQuantum_low, fila_IO) ## processo teste manual

    gerador: GeradorProcessos           = GeradorProcessos(MAX_PROCESSOS, max_eventos_io=2, tempo_cpu_min=5, tempo_cpu_max=30, chegada_min=0, chegada_max=10)
    processosGerados : list[Processo]   = gerador.GerarProcessos() ## se não colocar nada ele pega um valor aleatorio de processos a serem criados
    finalizados: list[Processo]         = SimuladorIOMultiFila(processosGerados, filaQuantum_high, filaQuantum_low, fila_IO)

    ImprimirTurnaround(finalizados)
    Trace.Salvar(ARQUIVO_TRACE)

    