import { useEffect, useState } from 'react'
import Controles from './componentes/Controles'
import Estado from './componentes/Estado'
import Eventos from './componentes/Eventos'
import Gantt from './componentes/Gantt'
import Processos from './componentes/Processos'
import Secao from './componentes/Secao'
import Turnaround from './componentes/Turnaround'
import { UI } from './ui'

const TRACES = [
  { id: 'mlfq', curto: 'MLFQ', pasta: 'FilasMultiniveisComRetroalimentacao', arquivo: 'trace-mlfq.json' },
  { id: 'sjf', curto: 'SJF', pasta: 'SJFPreemptivo', arquivo: 'trace-sjf.json' },
]

const VELOCIDADE = 320

export default function App() {
  const [escolhido, setEscolhido] = useState(TRACES[0])
  const [trace, setTrace] = useState(null)
  const [erro, setErro] = useState(false)
  const [indice, setIndice] = useState(0)
  const [tocando, setTocando] = useState(false)

  useEffect(() => {
    setTrace(null)
    setErro(false)
    setIndice(0)
    setTocando(false)

    fetch(`./${escolhido.arquivo}`)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.statusText))))
      .then(setTrace)
      .catch(() => setErro(true))
  }, [escolhido])

  useEffect(() => {
    if (!tocando || trace === null) return

    const timer = setInterval(() => {
      setIndice((atual) => {
        if (atual >= trace.passos.length - 1) {
          setTocando(false)
          return atual
        }
        return atual + 1
      })
    }, VELOCIDADE)

    return () => clearInterval(timer)
  }, [tocando, trace])

  const passo = trace ? trace.passos[indice] : null

  return (
    <div className="min-h-screen bg-background font-mono text-foreground">
      <div className="mx-auto max-w-5xl space-y-8 px-4 py-8 sm:px-6">

        <header className="flex flex-wrap items-end justify-between gap-4 border-b border-border pb-4">
          <div>
            <h1 className="text-[13px] font-bold uppercase tracking-[1.5px] text-foreground">
              Simulador de Escalonamento de Processos
            </h1>
            <p className={`${UI.meta} mt-1`}>
              Arquitetura de Sistemas Operacionais — UERJ
              {trace && ` · ${trace.algoritmo} · ${trace.passos.length} u.t.`}
            </p>
          </div>

          <div className="flex gap-1.5">
            {TRACES.map((t) => (
              <button
                key={t.id}
                onClick={() => setEscolhido(t)}
                className={t.id === escolhido.id ? UI.botaoAtivo : UI.botao}
              >
                {t.curto}
              </button>
            ))}
          </div>
        </header>

        {erro && (
          <div className="border border-border bg-secondary p-4">
            <p className={UI.rotuloSecao}>Trace não encontrado</p>
            <p className={`${UI.meta} mt-2`}>
              Rode o simulador em Python para gerar <code>public/{escolhido.arquivo}</code>:
            </p>
            <pre className="mt-2 border border-border bg-background p-2 font-mono text-[10px] text-foreground">
              cd {escolhido.pasta}{'\n'}python main.py
            </pre>
          </div>
        )}

        {trace === null && !erro && <p className={UI.meta}>Carregando…</p>}

        {trace !== null && (
          <>
            <Secao titulo="Gráfico de Gantt" meta={`t = ${passo.tempo}`}>
              <Controles
                indice={indice}
                total={trace.passos.length}
                tocando={tocando}
                setIndice={setIndice}
                setTocando={setTocando}
              />
              <Gantt trace={trace} indice={indice} setIndice={setIndice} />
            </Secao>

            <Secao titulo={`Estado em t = ${passo.tempo}`}>
              <Estado rotulos={trace.filas} passo={passo} />
            </Secao>

            <Secao titulo={`Eventos no intervalo [${passo.tempo}, ${passo.tempo + 1}]`}>
              <Eventos eventos={passo.eventos} />
            </Secao>

            <Secao titulo="Processos criados">
              <Processos processos={trace.processos} />
            </Secao>

            <Secao titulo="Turnaround">
              <Turnaround resultado={trace.resultado} />
            </Secao>
          </>
        )}
      </div>
    </div>
  )
}
