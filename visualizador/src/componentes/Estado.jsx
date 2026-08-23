import Pid from './Pid'
import { UI } from '../ui'

function Marca({ pid, sufixo }) {
  return (
    <span className="inline-flex items-center gap-1.5 border border-border px-1.5 py-px font-mono text-[10px]">
      <Pid pid={pid} />
      <span className="text-[9px] text-muted-foreground">{sufixo}</span>
    </span>
  )
}

function Linha({ rotulo, itens, vazio, marca }) {
  return (
    <div className="flex items-start gap-3 border-b border-border/40 py-1.5">
      <span className={`${UI.microRotulo} w-40 shrink-0 pt-0.5`}>{rotulo}</span>
      <div className="flex flex-wrap gap-1.5">
        {itens.length === 0 ? <span className={UI.meta}>{vazio}</span> : itens.map(marca)}
      </div>
    </div>
  )
}

export default function Estado({ rotulos, passo }) {
  const cpu = passo.cpu

  return (
    <div>
      <Linha
        rotulo="CPU"
        vazio="ociosa"
        itens={cpu === null ? [] : [cpu]}
        marca={(p) => (
          <Marca
            key={p.pid}
            pid={p.pid}
            sufixo={
              p.quantum_restante > 0
                ? `CPU ${p.cpu_restante} · quantum ${p.quantum_restante}`
                : `CPU ${p.cpu_restante}`
            }
          />
        )}
      />

      {passo.prontos.map((fila, i) => (
        <Linha
          key={i}
          rotulo={rotulos[i]}
          itens={fila}
          vazio="vazia"
          marca={(p) => <Marca key={p.pid} pid={p.pid} sufixo={`${p.cpu_restante} u.t.`} />}
        />
      ))}

      <Linha
        rotulo="Fila de E/S"
        itens={passo.io}
        vazio="vazia"
        marca={(p) => <Marca key={p.pid} pid={p.pid} sufixo={`${p.tipo} · ${p.restante} u.t.`} />}
      />
    </div>
  )
}
