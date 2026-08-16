from enum import Enum

import FilaQuantum

class Status(Enum):
    NOVO        = 1
    PRONTO      = 2
    EXECUTANDO  = 3
    BLOQUEADO   = 4
    TERMINADO   = 5

class Prioridade(Enum):
    ALTA        = 0
    MEDIA       = 1
    BAIXA       = 2
    ULTRA_BAIXA = 3

class TipoIO(Enum):
    DISCO       = 0
    FITA        = 1
    IMPRESSORA  = 2

class EventoIO:

    def __init__(
        self,
        tempo_cpu_disparo: int,
        tipo: TipoIO
    ):
        # Quantas unidades de CPU o processo precisa ter 0# executado para solicitar esta E/S
        self.tempo_cpu_disparo: int = tempo_cpu_disparo
        self.tipo: TipoIO           = tipo
        self.duracao: int           = 0
        self.CalculateDuracao()

    def CalculateDuracao(self) -> int:
        # fazendo amnualmente aqui mas o ideal é que fosse um dict ou algo do tipo para mapear os tipos de E/S para suas durações
        if self.tipo == TipoIO.DISCO:
            self.duracao = 3
        elif self.tipo == TipoIO.FITA:
            self.duracao = 7
        elif self.tipo == TipoIO.IMPRESSORA:
            self.duracao = 10
        else:
            raise ValueError("Tipo de E/S inválido.")
        
        return self.duracao

class Processo:

    def __init__(self, pid : int, chegada: int, tempo_cpu: int, prioridade: Prioridade = Prioridade.ALTA, eventos_io: list[EventoIO] = None):

        self.pid   : int         = pid
        self.ppid  : int         = 0

        self.chegada        : int = chegada ## unidade de tempo que o processo chega na fila de pronto

        self.tempo_cpu      : int = tempo_cpu
        self.tempo_restante : int = 0 ## tempo total que o processo deve ser executado na CPU, incluindo o tempo de E/S

        self.tempo_cpu_executado : int = 0

        self.prioridade     : Prioridade = prioridade

        self.status         : Status     = Status.NOVO

        ## esse daqui é o tempo que vai executar na CPU baseado em qual fila estava
        self.tempo_quantum : int         = 0 
        self.tempo_termino : int         = -1 ## tempo global em unidade de tempo

        ## fila de origme para saber em qual fila o processo estava antes de ser executado e colocar para a proxima:
        self.filaAtual    : FilaQuantum = None

        ## feito dessa maneira para os eventos poderem serem aleatoriamente criados no algoritmo
        self.eventos_io: list[EventoIO] = eventos_io
        # proximo IO
        self.indice_proximo_io: int = 0
        # IO atual
        self.io_atual: EventoIO | None = None
        # tempo restante de IO
        self.tempo_io_restante: int = 0

        self.CalcularTempoTotal()

    def GerenciarIO(self):
        self.status             = Status.BLOQUEADO ## bloqueado esperando IO
        self.io_atual           = self.eventos_io[self.indice_proximo_io]
        self.tempo_io_restante  = self.io_atual.duracao
        self.indice_proximo_io += 1

    def CalcularTempoTotal(self) -> int:
        self.tempo_restante = self.tempo_cpu
        if self.eventos_io is not None:
            for evento in self.eventos_io:
                self.tempo_restante += evento.duracao
