## Relatório final exigido pelo enunciado: turnaround de cada processo.


def ImprimirTurnaround(finalizados: list):

    print("\n========================================")
    print("       TURNAROUND DOS PROCESSOS")
    print("========================================")
    print(f"\n{'PID':<6}{'Chegada':<10}{'CPU':<7}{'Término':<10}{'Turnaround':<12}")

    processos = sorted(finalizados, key=lambda processo: processo.pid)

    for processo in processos:
        print(
            f"P{processo.pid:<5}"
            f"{processo.chegada:<10}"
            f"{processo.tempo_cpu:<7}"
            f"{processo.tempo_termino:<10}"
            f"{processo.CalcularTurnaroundTime():<12}"
        )

    media = sum(processo.CalcularTurnaroundTime() for processo in processos) / len(processos)
    print(f"\nTurnaround médio: {media:.2f} u.t.")
    print("========================================")


SIMBOLOS = {
    "executando": "#",
    "pronto": "-",
    "io": "/",
    "espera_io": ":",
    None: " ",
}


def EstadoNoPasso(passo: dict, pid: int):
    ## a CPU vem primeiro: quem sai da CPU neste intervalo ja aparece na fila de
    ## prontos ou de E/S no snapshot, que e tirado no fim do tique
    if passo["cpu"] is not None and passo["cpu"]["pid"] == pid:
        return "executando"
    if passo["io_ativo"] == pid:
        return "io"
    if any(p["pid"] == pid for p in passo["io"]):
        return "espera_io"
    if any(p["pid"] == pid for fila in passo["prontos"] for p in fila):
        return "pronto"
    return None


def ImprimirGantt(trace: dict):

    passos = trace["passos"]
    margem = 7

    print("\n========================================")
    print("            GRÁFICO DE GANTT")
    print("========================================\n")

    regua = " " * margem
    for passo in passos:
        if passo["tempo"] % 10 == 0:
            regua += "|"
        elif passo["tempo"] % 5 == 0:
            regua += "."
        else:
            regua += " "
    print(regua)

    for processo in trace["processos"]:
        linha = "".join(SIMBOLOS[EstadoNoPasso(p, processo["pid"])] for p in passos)
        print(f"P{processo['pid']:<{margem - 1}}{linha}")

    print("\n  #  executando          -  pronto, esperando CPU")
    print("  /  usando o dispositivo de E/S")
    print("  :  na fila do dispositivo de E/S")
    print("========================================")
