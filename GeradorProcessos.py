## Objetivo desse arquivo é criar processos de teste automaticamente para simular o algoritmo de escalonamento de processos
import random

from processoModel import Processo, EventoIO, TipoIO

import random

from processoModel import (
    Processo,
    EventoIO,
    TipoIO
)


class GeradorProcessos:

    def __init__(self, max_processos: int, max_eventos_io: int, tempo_cpu_min: int = 5, tempo_cpu_max: int = 30, chegada_min: int = 0, chegada_max: int = 10, seed: int | None = None):

        self.max_processos  = max_processos
        self.max_eventos_io = max_eventos_io
        self.tempo_cpu_min  = tempo_cpu_min
        self.tempo_cpu_max  = tempo_cpu_max
        self.chegada_min    = chegada_min
        self.chegada_max    = chegada_max

        if seed is not None:
            random.seed(seed)


    def GerarEventosIO(self, tempo_cpu: int) -> list[EventoIO]:
        ## Só gera eventos com o limite de tempo que a cpu tem
        ## ou seja se o processo tem 20 u.t. só pode gerar um evento de IO até 19 u.t interno do processo
        quantidade_pontos_validos = tempo_cpu - 1
        quantidade_maxima = min(self.max_eventos_io, quantidade_pontos_validos)
        quantidade_eventos = random.randint(1, quantidade_maxima) ## tem que ter no minimo 1 IO requerimento da professora
 
        if quantidade_eventos == 0:
            return []

        # gera uma lista de inteiros que representam os momentos de eventos que vão ter naquele processo
        momentos_io = random.sample(range(1, tempo_cpu),quantidade_eventos)
        momentos_io.sort() 
        eventos: list[EventoIO] = []

        for momento in momentos_io:
            ## escolhe um tipo de IO aleatoriamente
            tipo = random.choice(list(TipoIO))
            evento = EventoIO(tempo_cpu_disparo=momento, tipo=tipo)
            eventos.append(evento)

        return eventos


    def GerarProcesso(self, pid: int) -> Processo:

        ## cria um momento de chegada aleatorio do processo para entrar na fila de alta prioridade
        chegada = random.randint(self.chegada_min, self.chegada_max)

        ## gera o tempo de CPU que aquele processo deve executar
        tempo_cpu = random.randint(self.tempo_cpu_min, self.tempo_cpu_max)

        ## gera os eventos que o processo vai ter
        eventos_io = self.GerarEventosIO(tempo_cpu)

        return Processo(pid=pid, chegada=chegada, tempo_cpu=tempo_cpu, eventos_io=eventos_io)


    def GerarProcessos(self, quantidade: int | None = None) -> list[Processo]:

        if quantidade is None:

            quantidade = random.randint(2,self.max_processos)

        if quantidade <= 0:
            raise ValueError(
                "Quantidade deve ser maior que zero."
            )


        if quantidade > self.max_processos:

            raise ValueError(
                f"Máximo permitido: "
                f"{self.max_processos} processos."
            )


        processos: list[Processo] = []

        ## gera a lista de processos
        for pid in range(1, quantidade + 1):
            processos.append(self.GerarProcesso(pid))

        self.LogProcessos(processos)
        return processos


    def LogProcessos(self, processos: list[Processo]):

        print("\n========================================")
        print("     PROCESSOS GERADOS PARA SIMULACAO")
        print("========================================")

        for processo in processos:

            print(
                f"\nP{processo.pid}"
                f" | Chegada: {processo.chegada}"
                f" | CPU: {processo.tempo_cpu}"
                f" | I/Os: {len(processo.eventos_io)}"
            )

            if not processo.eventos_io:
                print("   Nenhum evento de E/S.")
                continue

            ## printa a lista de eventos daquele processo
            for i, evento in enumerate(processo.eventos_io,start=1):

                print(
                    f"   IO {i}: "
                    f"CPU={evento.tempo_cpu_disparo}"
                    f" | {evento.tipo.name}"
                    f" | duração={evento.duracao}"
                )

        print("\n========================================")