import { UI } from '../ui'

export default function Eventos({ eventos }) {
  if (eventos.length === 0) {
    return <p className={UI.meta}>Nenhum evento nesta unidade de tempo.</p>
  }

  return (
    <ul className="space-y-1">
      {eventos.map((evento, i) => (
        <li key={i} className="font-mono text-[10px] leading-[1.6] text-foreground">
          {evento}
        </li>
      ))}
    </ul>
  )
}
