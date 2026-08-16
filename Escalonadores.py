## Nesse arquivo aqui vai ter os varios tipos de escalonadores 
## que são os algoritmos que vão selecionar quem vai entrar na CPU


## Esse primeiro escalonador é só para testar o exemplo da professora,
#  para ver se o algoritmo está funcionando corretamente
from FilaQuantum import FilaQuantum
from processoModel import Processo, Status


## primeira versão essa versão é bem rudimentar
def EscalonadorTeste(
    fila_alta: FilaQuantum,
    fila_media: FilaQuantum,
    fila_baixa: FilaQuantum
) -> Processo:

    processo : Processo

    if fila_alta.fila.qsize() > 0:

        processo = fila_alta.fila.get()
        processo.prioridade = 0
        processo.tempo_quantum = fila_alta.quantum
        processo.filaAtual = fila_alta

    elif fila_media.fila.qsize() > 0:
        processo = fila_media.fila.get()
        processo.prioridade = 1
        processo.tempo_quantum = fila_media.quantum
        processo.filaAtual = fila_media


    elif fila_baixa.fila.qsize() > 0:
        processo = fila_baixa.fila.get()
        processo.prioridade = 2
        processo.tempo_quantum = fila_baixa.quantum
        processo.filaAtual = fila_baixa

    else:
        return None

    processo.status = Status.EXECUTANDO

    return processo

def EscalonadorGenerico(
    filas: list[FilaQuantum]
) -> Processo:

    ## iterando pelas filas em ordem de prioridade, da mais alta para a mais baixa
    ## se tem um item esperando na mais alta ele vai pegar o processo da fila de mais alta prioridade e assim em diante
    for fila in filas:
        if fila.fila.qsize() > 0:
            processo = fila.fila.get()
            processo.tempo_quantum = fila.quantum
            processo.filaAtual = fila
            processo.status = Status.EXECUTANDO
            print(f"Processo P{processo.pid} foi selecionado da fila de prioridade {filas.index(fila)} com quantum {fila.quantum}.\n")
            return processo

    return None