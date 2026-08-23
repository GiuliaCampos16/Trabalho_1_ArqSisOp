# Visualizador

Player passo a passo das simulações, em React + Tailwind.

Ele **não** implementa escalonamento nenhum. Os simuladores em Python gravam um trace
JSON — um snapshot por unidade de tempo — e esta tela apenas navega por esses snapshots.
A lógica continua tendo uma fonte da verdade só, do lado do Python.

## Como usar

Primeiro gere os traces rodando os simuladores:

```bash
cd ../FilasMultiniveisComRetroalimentacao && python main.py
cd ../SJFPreemptivo && python main.py
```

Cada um escreve em `public/trace-mlfq.json` e `public/trace-sjf.json`.

Depois:

```bash
pnpm install
pnpm dev
```

Para apresentar sem depender do servidor de desenvolvimento, `pnpm build` gera
`dist/`, que abre direto do arquivo (o `vite.config.js` usa `base: './'`).

## O que a tela mostra

- **Gráfico de Gantt** — uma linha por processo, tempo no eixo horizontal. Cada célula mostra em que estado o processo estava naquela unidade de tempo: executando, pronto esperando CPU, ocupando o dispositivo de E/S ou na fila do dispositivo. É onde a preempção e o gargalo da E/S ficam visíveis. Clique em qualquer célula para navegar.
- **Estado** — no instante selecionado: quem está na CPU, o conteúdo de cada fila de prontos e da fila de E/S.
- **Eventos** — o que aconteceu naquele intervalo, o mesmo texto que sai no terminal.
- **Processos criados** — chegada, tempo de CPU e eventos de E/S de cada processo.
- **Turnaround** — tabela final com a média.

O seletor MLFQ / SJF no topo troca de algoritmo. Como o formato do trace é o mesmo, a
mesma tela serve os dois — no MLFQ aparecem duas filas de prontos, no SJF apenas uma.

## Formato do trace

```json
{
  "algoritmo": "Filas multiníveis com retroalimentação",
  "filas": ["Prioridade 0 (q=2)", "Prioridade 1 (q=5)"],
  "processos": [{ "pid": 1, "chegada": 0, "tempo_cpu": 16, "eventos_io": [{ "disparo": 4, "tipo": "FITA", "duracao": 7 }] }],
  "passos": [
    {
      "tempo": 7,
      "eventos": ["Processo [P2] solicitou E/S do tipo IMPRESSORA no tempo 8."],
      "cpu": { "pid": 3, "cpu_restante": 5, "quantum_restante": 1 },
      "io_ativo": 2,
      "prontos": [[{ "pid": 1, "cpu_restante": 4 }], []],
      "io": [{ "pid": 2, "tipo": "IMPRESSORA", "restante": 9 }]
    }
  ],
  "resultado": [{ "pid": 1, "chegada": 0, "termino": 55, "turnaround": 55 }]
}
```

`prontos` é uma lista por fila de prontos, na mesma ordem de `filas` — por isso o
mesmo player serve tanto um algoritmo de duas filas quanto um de fila única.
`cpu` é `null` quando a CPU está ociosa. `io_ativo` é o PID que ocupou o dispositivo
de E/S naquele intervalo — os demais processos em `io` estão apenas na fila, esperando
a vez. Essa distinção é o que deixa o gargalo do dispositivo único visível no Gantt.

Quem grava é `comum/Trace.py`: `Evento()` imprime no terminal e guarda a mensagem,
e `FecharPasso()` fecha o snapshot no fim de cada iteração do laço de tempo.
