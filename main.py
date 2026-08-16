## essas coisas vão ser definidas pelo usuario na entrada posteriormente
from FilaQuantum import FilaIO, FilaQuantum
from processoModel import EventoIO, Processo, Prioridade, TipoIO
from Simulador import SimuladorTeste, SimuladorIOMultiFila

MAX_PROCESSOS = 5

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
    SimuladorIOMultiFila(processosIO, filaQuantum_high, filaQuantum_low, fila_IO)

    print("This is the main module.")