import { corProcesso } from '../cores'
import { UI } from '../ui'

function Linha({ texto }) {
  const partes = texto.split(/(\[P\d+\])/g)

  return (
    <li className="border-l-2 border-border py-0.5 pl-2.5 font-mono text-[11px] leading-[1.65]">
      {partes.map((p, i) => {
        const m = p.match(/^\[P(\d+)\]$/)
        if (!m) return <span key={i}>{p}</span>
        return (
          <span key={i} className="font-bold" style={{ color: corProcesso(Number(m[1])) }}>
            P{m[1]}
          </span>
        )
      })}
    </li>
  )
}

export default function Eventos({ eventos }) {
  if (eventos.length === 0) {
    return <p className={UI.meta}>Nenhum evento nesta unidade de tempo.</p>
  }

  return (
    <ul className="space-y-1.5">
      {eventos.map((e, i) => <Linha key={i} texto={e} />)}
    </ul>
  )
}
