# Trabalho_1_ArqSisOp

Trabalho de arquitetura de sistema operacional

## Algoritmos implementados

- [`FilasMultiniveisComRetroalimentacao/`](FilasMultiniveisComRetroalimentacao/) — MLFQ, preemptivo por quantum, com E/S em disco, fita e impressora
- [`SJFPreemptivo/`](SJFPreemptivo/) — SJF preemptivo (SRTF), fila única

```bash
cd FilasMultiniveisComRetroalimentacao
python main.py

cd SJFPreemptivo
python main.py
```

## Validação

Os dois algoritmos reproduzem exemplos resolvidos em aula:

- **MLFQ** — filas 2/4/6, sem E/S: P1=11, P2=13, P3=23, P4=21
- **SRTF** — exemplo do slide 11: P1=17, P2=4, P3=24, P4=7, média 13
