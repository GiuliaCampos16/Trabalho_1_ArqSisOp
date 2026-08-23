from queue import Queue
from processoModel import Processo


class FilaQuantum:
    def __init__(self, quantum):
        self.quantum = quantum
        self.fila: Queue[Processo] = Queue()

    def PrintFila(self):
        print(f"Fila de Quantum {self.quantum}:")
        for processo in list(self.fila.queue):
            print(
                f"Processo P{processo.pid} | Tempo Restante: {processo.tempo_restante} | Tempo de Quantum: {processo.tempo_quantum}")
        print("------------------------------")


class FilaIO:
    def __init__(self):
        self.fila: Queue[Processo] = Queue()

    def PrintFila(self):
        print("Fila de E/S:")
        for processo in list(self.fila.queue):
            print(f"Processo P{processo.pid} | Tempo Rest.: {processo.tempo_restante} | Tempo de Quantum: {processo.tempo_quantum} | Tipo de E/S: {processo.io_atual.tipo.name} | Duração E/S: {processo.io_atual.duracao}")
        print("------------------------------")
