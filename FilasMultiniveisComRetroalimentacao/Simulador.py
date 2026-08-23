import Trace
from processoModel import Processo, Status, TipoIO
from FilaQuantum import FilaIO, FilaQuantum
from Escalonadores import EscalonadorGenerico


def SimuladorIOMultiFila(lista_processos: list[Processo], filas: list[FilaQuantum], fila_IO: FilaIO) -> list[Processo]:
    # Observação: como é uma fila de IO, não tem prioridade e 1 IO é tratado de cada vez, caso o contrario todos os IOs seriam tratado simultaneamente
    # em teoria cada periferico teria sua propria fila de IO mas vamos simplificar e tratar todos os IOs como uma unica fila de IO, mas o ideal seria ter uma fila para cada tipo de IO, mas vamos simplificar por enquanto

    tempo = 0
    finalizados: list[Processo] = []
    processoAtualCPU: Processo = None

    fila_alta: FilaQuantum = filas[0]

    Trace.Iniciar(
        "Filas multiníveis com retroalimentação",
        [f"Prioridade {i} (q={fila.quantum})" for i, fila in enumerate(filas)],
        lista_processos
    )

    # enquanto todos os processos não forem finalizados, o simulador continua rodando
    while len(finalizados) < len(lista_processos):

        # input()

        # poderia ter uma maneira aqui de só pular essa sexecução caso n tenham amis processos entrarem
        ProcessarChegada(lista_processos, tempo, fila_alta)

        if processoAtualCPU is None:
            # pega o processo da fila de CPU com maior prioridade que tenha algum processo esperando, caso não tenha nenhum processo esperando, retorna None
            processoAtualCPU = EscalonadorGenerico(filas)

        # gerenciamento da fila de IO, caso tenha algum processo na fila de IO, ele vai ser processado e colocado na fila de CPU apropriada
        processo: Processo | None = ProcessarIO(fila_IO, tempo)
        if processo is not None:
            if processo.status != Status.BLOQUEADO:
                if processo.Concluido():
                    processo.status = Status.TERMINADO
                    processo.tempo_termino = tempo + 1
                    finalizados.append(processo)
                    Trace.Evento(
                        f"Processo [P{processo.pid}] terminou de executar no tempo {tempo + 1}.")
                else:
                    # pega o primeiro processo da fila de IO e coloca na fila de CPU apropriada
                    GerenciarFilaPosIO(processo, filas)

        executouNaCPU: Processo = processoAtualCPU

        if processoAtualCPU is not None:

            status: Status = ProcessarExecucao(processoAtualCPU, tempo)
            if status == Status.TERMINADO:
                finalizados.append(processoAtualCPU)
                processoAtualCPU = None

            # checa se o processo atual solicitou E/S
            solicitou_io: bool = ChecarSolicitarIO(processoAtualCPU, tempo)
            if solicitou_io == True:
                fila_IO.fila.put(processoAtualCPU)
                processoAtualCPU.GerenciarIO()
                Trace.Evento(
                    f"Processo [P{processoAtualCPU.pid}] foi movido para a fila de E/S.")
                processoAtualCPU = None

            # coloca o processo atual de volta na fila apropriada caso ele tenha sido preemptado
            preempted: bool = GerenciaFilaGenerica(processoAtualCPU, filas)
            if preempted == True:
                processoAtualCPU = None

        Trace.FecharPasso(tempo, executouNaCPU, filas, fila_IO, processo)

        tempo += 1

    Trace.Finalizar(finalizados)

    for processo in finalizados:
        print(
            f"Processo [P{processo.pid}] terminou no tempo {processo.tempo_termino}.")

    # retorna a lista de processos finalizados para fazer os resultados finais
    return finalizados


# usando o algoritmo do trabalho sempre quando um processo chega na fila ele é colocado na fila de alta prioridade
def ProcessarChegada(processos: list[Processo], tempo: int, fila_alta: FilaQuantum):

    processo: Processo

    for processo in processos:
        if processo.chegada == tempo and processo.status == Status.NOVO:
            # adiciona o processo na fila de alta prioridade
            fila_alta.fila.put(processo)
            processo.DefinirFila(fila_alta, 0)
            processo.status = Status.PRONTO
            Trace.Evento(
                f"Processo [P{processo.pid}] Inicializou na fila de alta prioridade no tempo {tempo}.")


def ProcessarExecucao(processo: Processo, tempo: int) -> Status:

    # se o processo ainda tem tempo de CPU para gastar
    if processo.TempoCpuRestante() > 0:
        processo.tempo_restante -= 1
        processo.tempo_cpu_executado += 1
        processo.tempo_quantum -= 1

        Trace.Evento(
            f"Processo [P{processo.pid}] está executando "
            f"no intervalo [{tempo}, {tempo + 1}]. "
            f"CPU restante: {processo.TempoCpuRestante()}. "
            f"Tempo restante (CPU+E/S): {processo.tempo_restante}. "
            f"Quantum restante: {processo.tempo_quantum}."
        )

        # print(f"Processo P{processo.pid} está executando no tempo {tempo}. Tempo restante: {processo.tempo_restante}. Tempo de quantum: {processo.tempo_quantum}.")

    # se o processo terminou de executar (toda a CPU gasta e nenhuma E/S pendente)
    if processo.Concluido():
        processo.status = Status.TERMINADO
        # processo.tempo_termino = tempo checando pois o teste n tava batendo com os tempo sem usar tempo +1
        # print(f"Processo P{processo.pid} terminou de executar no tempo {tempo}.")
        processo.tempo_termino = tempo + 1
        Trace.Evento(
            f"Processo [P{processo.pid}] terminou de executar no tempo {tempo + 1}.")

    return processo.status


def GerenciaFilaGenerica(processo: Processo, lista_filas: list[FilaQuantum]) -> bool:

    if processo is None:
        # continua para a proxima iteração do loop, pois não há processo em execução
        return False

    # se o processo ainda não terminou de executar, ele é colocado na fila de prioridade inferior
    # se o processo foi preemptado, a função retorna True, caso contrário, retorna False
    if not processo.Concluido():
        if processo.tempo_quantum <= 0:
            # encontra a fila atual do processo na lista de filas
            for i in range(len(lista_filas)):
                if processo.filaAtual == lista_filas[i]:
                    # se o processo está na última fila, ele permanece nela
                    if i == len(lista_filas) - 1:
                        lista_filas[i].fila.put(processo)
                        processo.status = Status.PRONTO
                        processo.DefinirFila(lista_filas[i], i)
                        Trace.Evento(
                            f"Processo [P{processo.pid}] permaneceu na fila de prioridade {i}.")
                        return True

                    else:
                        # move o processo para a próxima fila
                        lista_filas[i + 1].fila.put(processo)
                        processo.status = Status.PRONTO
                        processo.DefinirFila(lista_filas[i + 1], i + 1)
                        Trace.Evento(
                            f"Processo [P{processo.pid}] foi movido para a fila de prioridade {i + 1}.")
                        return True

    return False


def ChecarSolicitarIO(processo: Processo, tempo: int) -> bool:
    if processo is None:
        return False

    # se ainda existe algum evento de E/S que o processo não solicitou
    if processo.TemIOPendente():

        evento_io = processo.eventos_io[processo.indice_proximo_io]

        # checa para ver se o processo solicitou E/S no tempo atual
        if processo.tempo_cpu_executado == evento_io.tempo_cpu_disparo:
            # tempo + 1 para bater com o fim do intervalo [tempo, tempo + 1] que acabou de executar
            Trace.Evento(
                f"Processo [P{processo.pid}] solicitou E/S do tipo {evento_io.tipo.name} no tempo {tempo + 1}.")
            return True  # coloca o processo atual na fila de E/S e retorna True para indicar que o processo solicitou E/S

    return False


def ProcessarIO(fila_io: FilaIO, tempo: int) -> Processo | None:
    # se a fila de IO não estiver vazia, processa o primeiro processo da fila
    if fila_io.fila.qsize() > 0:
        # pega o primeiro processo da fila sem removê-lo
        processo: Processo = fila_io.fila.queue[0]

        # se o processo ainda não terminou de executar
        if processo.tempo_io_restante > 0:
            processo.tempo_io_restante -= 1
            # tempo total do processo diminui também, pois o tempo de E/S é contado no tempo total do processo
            processo.tempo_restante -= 1
            Trace.Evento(
                f"Processo [P{processo.pid}] está realizando E/S do tipo {processo.io_atual.tipo.name} no intervalo [{tempo}, {tempo + 1}]. Tempo restante de E/S: {processo.tempo_io_restante}.")

        # se o processo terminou de executar
        if processo.tempo_io_restante == 0:
            processo.status = Status.PRONTO
            fila_io.fila.get()  # remove o processo da fila de IO
            Trace.Evento(
                f"Processo [P{processo.pid}] terminou a E/S do tipo {processo.io_atual.tipo.name} no tempo {tempo + 1}.")

        return processo

    return None


def GerenciarFilaPosIO(processo: Processo, lista_filas: list[FilaQuantum]) -> bool:

    if processo is None:
        # continua para a proxima iteração do loop, pois não há processo em execução
        return False

    # se o processo ainda não terminou de executar, ele é colocado na fila de prioridade inferior
    # se o processo foi preemptado, a função retorna True, caso contrário, retorna False
    if not processo.Concluido():
        if processo.io_atual.tipo == TipoIO.DISCO:
            # coloca na fila de baixa prioridade, que é a ultima fila da lista de filas
            lista_filas[len(lista_filas) - 1].fila.put(processo)
            processo.status = Status.PRONTO
            processo.DefinirFila(lista_filas[-1], len(lista_filas) - 1)
            Trace.Evento(
                f"Processo [P{processo.pid}] foi movido para a fila de prioridade {len(lista_filas) - 1} após E/S do tipo DISCO.")
            return True

        elif processo.io_atual.tipo == TipoIO.FITA:
            # coloca na fila de alta prioridade, que é a primeira fila da lista de filas
            lista_filas[0].fila.put(processo)
            processo.status = Status.PRONTO
            processo.DefinirFila(lista_filas[0], 0)
            Trace.Evento(
                f"Processo [P{processo.pid}] foi movido para a fila de prioridade 0 após E/S do tipo FITA.")
            return True

        elif processo.io_atual.tipo == TipoIO.IMPRESSORA:
            # coloca na fila de alta prioridade, que é a primeira fila da lista de filas
            lista_filas[0].fila.put(processo)
            processo.status = Status.PRONTO
            processo.DefinirFila(lista_filas[0], 0)
            Trace.Evento(
                f"Processo [P{processo.pid}] foi movido para a fila de prioridade 0 após E/S do tipo IMPRESSORA.")
            return True

    return False
