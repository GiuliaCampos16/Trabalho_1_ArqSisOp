import json

_trace = {}
_eventos = []


def Iniciar(algoritmo: str, rotulos_filas: list[str], processos: list):
    global _trace, _eventos

    _eventos = []
    _trace = {
        "algoritmo": algoritmo,
        "filas": rotulos_filas,
        "processos": [DescreverProcesso(processo) for processo in processos],
        "passos": [],
        "resultado": []
    }


def DescreverProcesso(processo) -> dict:
    return {
        "pid": processo.pid,
        "chegada": processo.chegada,
        "tempo_cpu": processo.tempo_cpu,
        "eventos_io": [
            {"disparo": evento.tempo_cpu_disparo,
                "tipo": evento.tipo.name, "duracao": evento.duracao}
            for evento in processo.eventos_io
        ]
    }


def Evento(mensagem: str):
    print(mensagem)
    _eventos.append(mensagem.strip())


def FecharPasso(tempo: int, processo_cpu, filas_prontos: list, fila_io):
    global _eventos

    _trace["passos"].append({
        "tempo": tempo,
        "eventos": [linha for linha in _eventos if linha != ""],
        "cpu": DescreverCPU(processo_cpu),
        "prontos": [[DescreverPronto(p) for p in ProcessosDaFila(f)] for f in filas_prontos],
        "io": [DescreverIO(p) for p in ProcessosDaFila(fila_io)]
    })
    _eventos = []


def ProcessosDaFila(fila) -> list:
    # FilaQuantum e FilaIO usam queue.Queue; FilaProntos usa list
    interna = fila.fila
    return list(interna.queue) if hasattr(interna, "queue") else list(interna)


def DescreverCPU(processo) -> dict | None:
    if processo is None:
        return None

    return {
        "pid": processo.pid,
        "cpu_restante": processo.TempoCpuRestante(),
        "quantum_restante": processo.tempo_quantum
    }


def DescreverPronto(processo) -> dict:
    return {"pid": processo.pid, "cpu_restante": processo.TempoCpuRestante()}


def DescreverIO(processo) -> dict:
    return {
        "pid": processo.pid,
        "tipo": processo.io_atual.tipo.name,
        "restante": processo.tempo_io_restante
    }


def Finalizar(finalizados: list):
    _trace["resultado"] = [
        {
            "pid": processo.pid,
            "chegada": processo.chegada,
            "termino": processo.tempo_termino,
            "turnaround": processo.CalcularTurnaroundTime()
        }
        for processo in sorted(finalizados, key=lambda processo: processo.pid)
    ]


def Salvar(caminho: str):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(_trace, arquivo, ensure_ascii=False, indent=2)

    print(f"\nTrace salvo em {caminho} ({len(_trace['passos'])} passos).")
