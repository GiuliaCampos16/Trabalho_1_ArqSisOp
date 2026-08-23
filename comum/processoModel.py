from enum import Enum


class Status(Enum):
    NOVO = 1
    PRONTO = 2
    EXECUTANDO = 3
    BLOQUEADO = 4
    TERMINADO = 5


class Prioridade(Enum):
    ALTA = 0
    MEDIA = 1
    BAIXA = 2
    ULTRA_BAIXA = 3


class TipoIO(Enum):
    DISCO = 0
    FITA = 1
    IMPRESSORA = 2


DURACAO_IO = {
    TipoIO.DISCO: 3,
    TipoIO.FITA: 7,
    TipoIO.IMPRESSORA: 10
}


class EventoIO:

    def __init__(self, tempo_cpu_disparo: int, tipo: TipoIO):

        # Quantas unidades de CPU o processo precisa ter
        # executado para solicitar esta E/S
        self.tempo_cpu_disparo: int = tempo_cpu_disparo
        self.tipo: TipoIO = tipo
        self.duracao: int = DURACAO_IO[tipo]


class Processo:

    def __init__(self, pid: int, chegada: int, tempo_cpu: int, prioridade: Prioridade = Prioridade.ALTA, eventos_io: list[EventoIO] = None):

        self.pid: int = pid
        self.ppid: int = 0

        self.chegada: int = chegada  # unidade de tempo que o processo chega na fila de pronto

        self.tempo_cpu: int = tempo_cpu
        # tempo total que o processo deve ser executado na CPU, incluindo o tempo de E/S
        self.tempo_restante: int = 0

        self.tempo_cpu_executado: int = 0

        self.prioridade: Prioridade = prioridade

        self.status: Status = Status.NOVO

        # esse daqui é o tempo que vai executar na CPU baseado em qual fila estava
        self.tempo_quantum: int = 0
        self.tempo_termino: int = -1  # tempo global em unidade de tempo

        # fila de origme para saber em qual fila o processo estava antes de ser executado e colocar para a proxima:
        self.filaAtual = None

        # feito dessa maneira para os eventos poderem serem aleatoriamente criados no algoritmo
        self.eventos_io: list[EventoIO] = eventos_io if eventos_io is not None else [
        ]
        # proximo IO
        self.indice_proximo_io: int = 0
        # IO atual
        self.io_atual: EventoIO | None = None
        # tempo restante de IO
        self.tempo_io_restante: int = 0

        self.CalcularTempoTotal()

    def GerenciarIO(self):
        self.status = Status.BLOQUEADO  # bloqueado esperando IO
        self.io_atual = self.eventos_io[self.indice_proximo_io]
        self.tempo_io_restante = self.io_atual.duracao
        self.indice_proximo_io += 1

    def CalcularTempoTotal(self) -> int:
        # calcula a unidade de tempo total que esse processo deve passar pela CPU + E/S para ser finalizado
        self.tempo_restante = self.tempo_cpu
        for evento in self.eventos_io:
            self.tempo_restante += evento.duracao

    def TempoCpuRestante(self) -> int:
        return self.tempo_cpu - self.tempo_cpu_executado

    def TemIOPendente(self) -> bool:
        return self.indice_proximo_io < len(self.eventos_io)

    def Concluido(self) -> bool:
        return (
            self.TempoCpuRestante() <= 0
            and not self.TemIOPendente()
            and self.tempo_io_restante <= 0
        )

    def CalcularTurnaroundTime(self) -> int:
        if self.tempo_termino == -1:
            return None
        return self.tempo_termino - self.chegada
