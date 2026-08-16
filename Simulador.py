from processoModel import Processo, Status, TipoIO
from FilaQuantum import FilaIO, FilaQuantum
from Escalonadores import EscalonadorTeste, EscalonadorGenerico

## simulador criado para tentar simular o algoritmo do trabalho da professora de
#  Escalonamento com filas multiníveis com retroalimentação
def SimuladorTeste(lista_processos : list[Processo], fila_alta : FilaQuantum, fila_media : FilaQuantum, fila_baixa : FilaQuantum):
    tempo = 0

    finalizados : list[Processo] = []

    processoAtualCPU : Processo = None

    ## enquanto todos os processos não forem finalizados, o simulador continua rodando
    while len(finalizados) < len(lista_processos): 

        input()

        ## poderia ter uma maneira aqui de só pular essa sexecução caso n tenham amis processos entrarem
        ProcessarChegada(lista_processos, tempo, fila_alta) 

        if processoAtualCPU is None:
            processoAtualCPU = EscalonadorTeste(fila_alta, fila_media, fila_baixa)

        if processoAtualCPU is not None:
            
            status : Status = ProcessarExecucao(processoAtualCPU, tempo)
            if status == Status.TERMINADO:
                finalizados.append(processoAtualCPU)
                processoAtualCPU = None

            preempted: bool = GerenciarFila(processoAtualCPU, fila_alta, fila_media, fila_baixa)
            if preempted == True:
                processoAtualCPU = None
        
        tempo += 1

    for processo in finalizados:
        print(f"Processo P{processo.pid} terminou no tempo {processo.tempo_termino}.")


def SimuladorIOMultiFila(lista_processos : list[Processo], fila_alta : FilaQuantum, fila_baixa : FilaQuantum, fila_IO : FilaIO):
    ## Observação: como é uma fila de IO, não tem prioridade e 1 IO é tratado de cada vez, caso o contrario todos os IOs seriam tratado simultaneamente
    ## em teoria cada periferico teria sua propria fila de IO mas vamos simplificar e tratar todos os IOs como uma unica fila de IO, mas o ideal seria ter uma fila para cada tipo de IO, mas vamos simplificar por enquanto

    tempo = 0
    finalizados : list[Processo] = []
    processoAtualCPU : Processo = None

    filas : list[FilaQuantum] = [fila_alta, fila_baixa] ## só deixando dessa maneira atualmente caso seja necessário adicionar mais filas futuramente, mas atualmente só tem duas filas de CPU



    ## enquanto todos os processos não forem finalizados, o simulador continua rodando
    while len(finalizados) < len(lista_processos): 

        #input()

        ## poderia ter uma maneira aqui de só pular essa sexecução caso n tenham amis processos entrarem
        ProcessarChegada(lista_processos, tempo, fila_alta) 

        if processoAtualCPU is None:
            ## pega o processo da fila de CPU com maior prioridade que tenha algum processo esperando, caso não tenha nenhum processo esperando, retorna None
            processoAtualCPU = EscalonadorGenerico(filas)

        ## gerenciamento da fila de IO, caso tenha algum processo na fila de IO, ele vai ser processado e colocado na fila de CPU apropriada
        processo : Processo | None = ProcessarIO(fila_IO, tempo)
        if processo is not None:
            if processo.status != Status.BLOQUEADO:
                GerenciarFilaPosIO(processo, filas) ## pega o primeiro processo da fila de IO e coloca na fila de CPU apropriada
        

        if processoAtualCPU is not None:
            
            status : Status = ProcessarExecucao(processoAtualCPU, tempo)
            if status == Status.TERMINADO:
                finalizados.append(processoAtualCPU)
                processoAtualCPU = None

            
            ## checa se o processo atual solicitou E/S
            solicitou_io : bool = ChecarSolicitarIO(processoAtualCPU, tempo)
            if solicitou_io == True:
                fila_IO.fila.put(processoAtualCPU)
                processoAtualCPU.GerenciarIO()

                print(f"Processo P{processoAtualCPU.pid} foi movido para a fila de E/S.\n")
                processoAtualCPU = None

            # coloca o processo atual de volta na fila apropriada caso ele tenha sido preemptado
            preempted: bool = GerenciaFilaGenerica(processoAtualCPU, filas)
            if preempted == True:
                processoAtualCPU = None

        tempo += 1

    for processo in finalizados:
        print(f"Processo P{processo.pid} terminou no tempo {processo.tempo_termino}.")

    pass


## usando o algoritmo do trabalho sempre quando um processo chega na fila ele é colocado na fila de alta prioridade
def ProcessarChegada(processos : list[Processo], tempo: int, fila_alta : FilaQuantum):

    processo : Processo

    for processo in processos:
        if processo.chegada == tempo and processo.status == Status.NOVO:
            ## adiciona o processo na fila de alta prioridade
            fila_alta.fila.put(processo)
            processo.status = Status.PRONTO
            print(f"Processo P{processo.pid} Inicializou na fila de alta prioridade no tempo {tempo}.\n")

    

def ProcessarExecucao(processo : Processo, tempo: int) -> Status:

    ## se o processo ainda não terminou de executar
    if processo.tempo_restante > 0:
        processo.tempo_restante -= 1
        processo.tempo_cpu_executado += 1
        processo.tempo_quantum -= 1

        print(
            f"Processo P{processo.pid} está executando "
            f"no intervalo [{tempo}, {tempo + 1}]. "
            f"Tempo restante: {processo.tempo_restante}. "
            f"Quantum restante: {processo.tempo_quantum}."
        )

        # print(f"Processo P{processo.pid} está executando no tempo {tempo}. Tempo restante: {processo.tempo_restante}. Tempo de quantum: {processo.tempo_quantum}.\n")
    
    ## se o processo terminou de executar
    if processo.tempo_restante == 0:
        processo.status = Status.TERMINADO
        # processo.tempo_termino = tempo checando pois o teste n tava batendo com os tempo sem usar tempo +1
        # print(f"Processo P{processo.pid} terminou de executar no tempo {tempo}.\n")
        processo.tempo_termino = tempo + 1
        print(f"Processo P{processo.pid} terminou de executar no tempo {tempo + 1}.\n")

    return processo.status

## Preemptivo: se o processo ainda não terminou de executar, ele é colocado na fila de prioridade inferior
def GerenciarFila(processo : Processo, fila_alta : FilaQuantum, fila_media : FilaQuantum, fila_baixa : FilaQuantum) -> bool:

    if processo is None:
        ## continua para a proxima iteração do loop, pois não há processo em execução
        return False

    ## se o processo ainda não terminou de executar, ele é colocado na fila de prioridade inferior
    ## se o processo foi preemptado, a função retorna True, caso contrário, retorna False
    if processo.tempo_restante > 0:
        if processo.tempo_quantum <= 0:
            if processo.filaAtual == fila_alta:
                fila_media.fila.put(processo)
                processo.status = Status.PRONTO
                processo.filaAtual = fila_media
                print(f"Processo P{processo.pid} foi movido para a fila de prioridade média.\n")
                return True
            
            elif processo.filaAtual == fila_media:
                fila_baixa.fila.put(processo)
                processo.status = Status.PRONTO
                processo.filaAtual = fila_baixa 
                print(f"Processo P{processo.pid} foi movido para a fila de prioridade baixa.\n")
                return True
            
            elif processo.filaAtual == fila_baixa:
                fila_baixa.fila.put(processo)
                processo.status = Status.PRONTO
                processo.filaAtual = fila_baixa
                print(f"Processo P{processo.pid} permaneceu na fila de prioridade baixa.\n")
                return True

    return False

def GerenciaFilaGenerica(processo : Processo, lista_filas: list[FilaQuantum]) -> bool:

    if processo is None:
        ## continua para a proxima iteração do loop, pois não há processo em execução
        return False

    ## se o processo ainda não terminou de executar, ele é colocado na fila de prioridade inferior
    ## se o processo foi preemptado, a função retorna True, caso contrário, retorna False
    if processo.tempo_restante > 0:
        if processo.tempo_quantum <= 0:
            ## encontra a fila atual do processo na lista de filas
            for i in range(len(lista_filas)):
                if processo.filaAtual == lista_filas[i]:
                    ## se o processo está na última fila, ele permanece nela
                    if i == len(lista_filas) - 1:
                        lista_filas[i].fila.put(processo)
                        processo.status = Status.PRONTO
                        processo.filaAtual = lista_filas[i]
                        print(f"Processo P{processo.pid} permaneceu na fila de prioridade {i}.\n")
                        return True
                    
                    else:
                        ## move o processo para a próxima fila
                        lista_filas[i + 1].fila.put(processo)
                        processo.status = Status.PRONTO
                        processo.filaAtual = lista_filas[i + 1]
                        print(f"Processo P{processo.pid} foi movido para a fila de prioridade {i + 1}.\n")
                        return True

    return False

def ChecarSolicitarIO(processo : Processo, tempo: int) -> bool:
    if processo is None:
        return False

    ## se o processo ainda não terminou de executar
    if processo.tempo_restante > 0:
        ## se o processo ainda não terminou de executar e o tempo de CPU do processo for igual ao tempo de CPU do evento de IO
        if processo.indice_proximo_io < len(processo.eventos_io):

            evento_io = processo.eventos_io[processo.indice_proximo_io]

            ## checa para ver se o processo solicitou E/S no tempo atual
            if processo.tempo_cpu_executado == evento_io.tempo_cpu_disparo:
                print(f"Processo P{processo.pid} solicitou E/S do tipo {evento_io.tipo.name} no tempo {tempo}.\n")
                return True ## coloca o processo atual na fila de E/S e retorna True para indicar que o processo solicitou E/S

    return False

def ProcessarIO(fila_io : FilaIO, tempo: int) -> Processo | None:
    ## se a fila de IO não estiver vazia, processa o primeiro processo da fila
    if fila_io.fila.qsize() > 0:
        processo : Processo = fila_io.fila.queue[0] ## pega o primeiro processo da fila sem removê-lo

        ## se o processo ainda não terminou de executar
        if processo.tempo_io_restante > 0:
            processo.tempo_io_restante -= 1
            processo.tempo_restante -= 1 ## tempo total do processo diminui também, pois o tempo de E/S é contado no tempo total do processo
            print(f"Processo P{processo.pid} está realizando E/S do tipo {processo.io_atual.tipo.name} no intervalo [{tempo}, {tempo + 1}]. Tempo restante de E/S: {processo.tempo_io_restante}.\n")

        ## se o processo terminou de executar
        if processo.tempo_io_restante == 0:
            processo.status = Status.PRONTO
            fila_io.fila.get() ## remove o processo da fila de IO
            print(f"Processo P{processo.pid} terminou a E/S do tipo {processo.io_atual.tipo.name} no tempo {tempo + 1}.\n")

        return processo

    return None

def GerenciarFilaPosIO(processo : Processo, lista_filas: list[FilaQuantum]) -> bool:

    if processo is None:
        ## continua para a proxima iteração do loop, pois não há processo em execução
        return False

    ## se o processo ainda não terminou de executar, ele é colocado na fila de prioridade inferior
    ## se o processo foi preemptado, a função retorna True, caso contrário, retorna False
    if processo.tempo_restante > 0:
        if processo.io_atual.tipo == TipoIO.DISCO:
            lista_filas[len(lista_filas) - 1].fila.put(processo) ## coloca na fila de baixa prioridade, que é a ultima fila da lista de filas
            processo.status = Status.PRONTO
            processo.filaAtual = lista_filas[len(lista_filas) - 1]
            print(f"Processo P{processo.pid} foi movido para a fila de prioridade {len(lista_filas) - 1} após E/S do tipo DISCO.\n")
            return True
        
        elif processo.io_atual.tipo == TipoIO.FITA:
            lista_filas[0].fila.put(processo) ## coloca na fila de alta prioridade, que é a primeira fila da lista de filas
            processo.status = Status.PRONTO
            processo.filaAtual = lista_filas[0]
            print(f"Processo P{processo.pid} foi movido para a fila de prioridade 0 após E/S do tipo FITA.\n")
            return True
        
        elif processo.io_atual.tipo == TipoIO.IMPRESSORA:
            lista_filas[0].fila.put(processo) ## coloca na fila de alta prioridade, que é a primeira fila da lista de filas
            processo.status = Status.PRONTO
            processo.filaAtual = lista_filas[0]
            print(f"Processo P{processo.pid} foi movido para a fila de prioridade 0 após E/S do tipo IMPRESSORA.\n")
            return True

    return False