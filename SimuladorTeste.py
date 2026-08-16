## Esse Simulador aqui foi para testar o algoritmo de escalonamento de quantum sem E/S, da professora 
## para alinhar o passo a passo de execução base do algoritmo de Escalonamento com filas multiníveis com retroalimentação

from processoModel import Processo, Status
from FilaQuantum import FilaQuantum
from Escalonadores import EscalonadorTeste

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
        print(f"Processo [P{processo.pid}] terminou no tempo {processo.tempo_termino}.")


## usando o algoritmo do trabalho sempre quando um processo chega na fila ele é colocado na fila de alta prioridade
def ProcessarChegada(processos : list[Processo], tempo: int, fila_alta : FilaQuantum):

    processo : Processo

    for processo in processos:
        if processo.chegada == tempo and processo.status == Status.NOVO:
            ## adiciona o processo na fila de alta prioridade
            fila_alta.fila.put(processo)
            processo.status = Status.PRONTO
            print(f"Processo [P{processo.pid}] Inicializou na fila de alta prioridade no tempo {tempo}.")


def ProcessarExecucao(processo : Processo, tempo: int) -> Status:

    ## se o processo ainda não terminou de executar
    if processo.tempo_restante > 0:
        processo.tempo_restante -= 1
        processo.tempo_cpu_executado += 1
        processo.tempo_quantum -= 1

        print(
            f"Processo [P{processo.pid}] está executando "
            f"no intervalo [{tempo}, {tempo + 1}]. "
            f"Tempo restante: {processo.tempo_restante}. "
            f"Quantum restante: {processo.tempo_quantum}."
        )

        # print(f"Processo [P{processo.pid}] está executando no tempo {tempo}. Tempo restante: {processo.tempo_restante}. Tempo de quantum: {processo.tempo_quantum}.")
    
    ## se o processo terminou de executar
    if processo.tempo_restante == 0:
        processo.status = Status.TERMINADO
        # processo.tempo_termino = tempo checando pois o teste n tava batendo com os tempo sem usar tempo +1
        # print(f"Processo [P{processo.pid}] terminou de executar no tempo {tempo}.")
        processo.tempo_termino = tempo + 1
        print(f"Processo [P{processo.pid}] terminou de executar no tempo {tempo + 1}.")

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
                print(f"Processo [P{processo.pid}] foi movido para a fila de prioridade média.")
                return True
            
            elif processo.filaAtual == fila_media:
                fila_baixa.fila.put(processo)
                processo.status = Status.PRONTO
                processo.filaAtual = fila_baixa 
                print(f"Processo [P{processo.pid}] foi movido para a fila de prioridade baixa.")
                return True
            
            elif processo.filaAtual == fila_baixa:
                fila_baixa.fila.put(processo)
                processo.status = Status.PRONTO
                processo.filaAtual = fila_baixa
                print(f"Processo [P{processo.pid}] permaneceu na fila de prioridade baixa.")
                return True

    return False

