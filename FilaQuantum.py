from queue import Queue
from processoModel import Processo

class FilaQuantum:
    def __init__(self, quantum):
        self.quantum = quantum
        self.fila : Queue[Processo] = Queue()

class FilaIO:
    def __init__(self):
        self.fila : Queue[Processo] = Queue()