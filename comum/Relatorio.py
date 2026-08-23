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
