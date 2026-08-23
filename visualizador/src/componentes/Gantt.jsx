import { useEffect, useRef } from 'react'
import Pid from './Pid'
import { corProcesso, hachuraIO, estadoDoProcesso } from '../cores'
import { UI } from '../ui'

const LARGURA = 14
const ALTURA = 20
const INTERVALO_REGUA = 5

const ESTADOS = [
  ['executando', 'Executando'],
  ['pronto', 'Pronto (esperando CPU)'],
  ['io', 'Ocupando o dispositivo de E/S'],
  ['espera_io', 'Na fila do dispositivo de E/S'],
  [null, 'Fora do sistema'],
]

function estiloCelula(pid, estado) {
  if (estado === 'executando') return { backgroundColor: corProcesso(pid) }
  if (estado === 'pronto') return { backgroundColor: corProcesso(pid, 0.22) }
  if (estado === 'io') return hachuraIO(pid, true)
  if (estado === 'espera_io') return hachuraIO(pid, false)
  return {}
}

function Legenda({ pid }) {
  return (
    <div className="flex flex-wrap items-center gap-x-5 gap-y-1.5 pt-1">
      {ESTADOS.map(([estado, rotulo]) => (
        <div key={rotulo} className="flex items-center gap-1.5">
          <span className="h-3 w-5 border border-border" style={estiloCelula(pid, estado)} />
          <span className={UI.microRotulo}>{rotulo}</span>
        </div>
      ))}
    </div>
  )
}

export default function Gantt({ trace, indice, setIndice }) {
  const marcadorRef = useRef(null)

  useEffect(() => {
    marcadorRef.current?.scrollIntoView({ block: 'nearest', inline: 'nearest' })
  }, [indice])

  const passos = trace.passos
  const largura = passos.length * LARGURA

  return (
    <div className="space-y-3">
      <div className="flex">

        <div className="shrink-0 pr-2 font-mono text-[10px]">
          <div style={{ height: ALTURA }} />
          {trace.processos.map((processo) => (
            <div key={processo.pid} className="flex items-center" style={{ height: ALTURA }}>
              <Pid pid={processo.pid} />
            </div>
          ))}
        </div>

        <div className="flex-1 overflow-x-auto">
          <div style={{ width: largura }}>

            <div className="relative border-b border-border" style={{ height: ALTURA }} aria-hidden>
              {passos.map((passo, i) =>
                passo.tempo % INTERVALO_REGUA === 0 ? (
                  <span
                    key={i}
                    className={`absolute bottom-0.5 ${UI.microRotulo} ${
                      i === indice ? 'font-bold text-foreground' : ''
                    }`}
                    style={{ left: i * LARGURA + 1 }}
                  >
                    {passo.tempo}
                  </span>
                ) : null,
              )}
            </div>

            {trace.processos.map((processo, linha) => (
              <div key={processo.pid} className="flex border-b border-border/40">
                {passos.map((passo, i) => {
                  const estado = estadoDoProcesso(passo, processo.pid)
                  const atual = i === indice

                  return (
                    <button
                      key={i}
                      ref={atual && linha === 0 ? marcadorRef : null}
                      onClick={() => setIndice(i)}
                      title={`t=${passo.tempo} · P${processo.pid} · ${estado ?? 'fora do sistema'}`}
                      className={`shrink-0 ${
                        passo.tempo % INTERVALO_REGUA === 0 ? 'border-l border-border/60' : ''
                      } ${atual ? 'ring-1 ring-inset ring-foreground' : ''}`}
                      style={{ width: LARGURA, height: ALTURA, ...estiloCelula(processo.pid, estado) }}
                    />
                  )
                })}
              </div>
            ))}

          </div>
        </div>
      </div>

      <Legenda pid={trace.processos[0].pid} />
    </div>
  )
}
