import Trace
from processoModel import Processo, Status
from FilaQuantum import FilaIO, FilaProntos
from Escalonadores import EscalonadorSJF, MenorTempoRestante


def SimuladorSJFPreemptivo(lista_processos: list[Processo], fila_prontos: FilaProntos, fila_IO: FilaIO) -> list[Processo]:
    # Fila unica de prontos: o enunciado permite quando o segundo algoritmo nao tem
    # niveis de prioridade. Por isso o tipo de E/S nao muda a fila de retorno aqui.

    tempo = 0
    finalizados: list[Processo] = []
    processoAtualCPU: Processo = None

    Trace.Iniciar("SJF preemptivo (SRTF)", ["Prontos"], lista_processos)

    while len(finalizados) < len(lista_processos):

        ProcessarChegada(lista_processos, tempo, fila_prontos)

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
                    GerenciarFilaPosIO(processo, fila_prontos)

        # a preempcao é checada depois das chegadas e dos retornos de E/S, que são os
        # dois momentos em que pode aparecer alguém com menos CPU restante
        processoAtualCPU = ChecarPreempcao(processoAtualCPU, fila_prontos)

        if processoAtualCPU is None:
            processoAtualCPU = EscalonadorSJF(fila_prontos)

        executouNaCPU: Processo = processoAtualCPU

        if processoAtualCPU is not None:

            status: Status = ProcessarExecucao(processoAtualCPU, tempo)
            if status == Status.TERMINADO:
                finalizados.append(processoAtualCPU)
                processoAtualCPU = None

            solicitou_io: bool = ChecarSolicitarIO(processoAtualCPU, tempo)
            if solicitou_io == True:
                fila_IO.fila.put(processoAtualCPU)
                processoAtualCPU.GerenciarIO()
                Trace.Evento(
                    f"Processo [P{processoAtualCPU.pid}] foi movido para a fila de E/S.")
                processoAtualCPU = None

        Trace.FecharPasso(tempo, executouNaCPU, [fila_prontos], fila_IO)

        tempo += 1

    Trace.Finalizar(finalizados)

    for processo in finalizados:
        print(
            f"Processo [P{processo.pid}] terminou no tempo {processo.tempo_termino}.")

    return finalizados


def ProcessarChegada(processos: list[Processo], tempo: int, fila_prontos: FilaProntos):

    processo: Processo

    for processo in processos:
        if processo.chegada == tempo and processo.status == Status.NOVO:
            fila_prontos.fila.append(processo)
            processo.status = Status.PRONTO
            Trace.Evento(
                f"Processo [P{processo.pid}] Inicializou na fila de prontos no tempo {tempo}.")


def ChecarPreempcao(processo: Processo, fila_prontos: FilaProntos) -> Processo:

    if processo is None:
        return None

    candidato: Processo = MenorTempoRestante(fila_prontos)
    if candidato is None:
        return processo

    # só preempta com tempo estritamente menor, senão processos empatados ficariam
    # trocando de lugar na CPU a cada unidade de tempo
    if candidato.TempoCpuRestante() < processo.TempoCpuRestante():
        fila_prontos.fila.append(processo)
        processo.status = Status.PRONTO
        Trace.Evento(
            f"Processo [P{processo.pid}] sofreu preempção de [P{candidato.pid}] e voltou para a fila de prontos.")
        return None

    return processo


def ProcessarExecucao(processo: Processo, tempo: int) -> Status:

    if processo.TempoCpuRestante() > 0:
        processo.tempo_restante -= 1
        processo.tempo_cpu_executado += 1

        Trace.Evento(
            f"Processo [P{processo.pid}] está executando "
            f"no intervalo [{tempo}, {tempo + 1}]. "
            f"CPU restante: {processo.TempoCpuRestante()}. "
            f"Tempo restante (CPU+E/S): {processo.tempo_restante}."
        )

    if processo.Concluido():
        processo.status = Status.TERMINADO
        processo.tempo_termino = tempo + 1
        Trace.Evento(
            f"Processo [P{processo.pid}] terminou de executar no tempo {tempo + 1}.")

    return processo.status


def ChecarSolicitarIO(processo: Processo, tempo: int) -> bool:

    if processo is None:
        return False

    if processo.TemIOPendente():

        evento_io = processo.eventos_io[processo.indice_proximo_io]

        if processo.tempo_cpu_executado == evento_io.tempo_cpu_disparo:
            Trace.Evento(
                f"Processo [P{processo.pid}] solicitou E/S do tipo {evento_io.tipo.name} no tempo {tempo + 1}.")
            return True

    return False


def ProcessarIO(fila_io: FilaIO, tempo: int) -> Processo | None:

    if fila_io.fila.qsize() > 0:
        processo: Processo = fila_io.fila.queue[0]

        if processo.tempo_io_restante > 0:
            processo.tempo_io_restante -= 1
            processo.tempo_restante -= 1
            Trace.Evento(
                f"Processo [P{processo.pid}] está realizando E/S do tipo {processo.io_atual.tipo.name} no intervalo [{tempo}, {tempo + 1}]. Tempo restante de E/S: {processo.tempo_io_restante}.")

        if processo.tempo_io_restante == 0:
            processo.status = Status.PRONTO
            fila_io.fila.get()
            Trace.Evento(
                f"Processo [P{processo.pid}] terminou a E/S do tipo {processo.io_atual.tipo.name} no tempo {tempo + 1}.")

        return processo

    return None


def GerenciarFilaPosIO(processo: Processo, fila_prontos: FilaProntos) -> bool:

    if processo is None:
        return False

    if not processo.Concluido():
        fila_prontos.fila.append(processo)
        processo.status = Status.PRONTO
        Trace.Evento(
            f"Processo [P{processo.pid}] voltou para a fila de prontos após E/S do tipo {processo.io_atual.tipo.name}.")
        return True

    return False
