import { UI } from '../ui'

export default function Secao({ titulo, meta, children }) {
  return (
    <section className="space-y-2.5">
      <div className="flex items-baseline justify-between gap-3 border-b border-border pb-1.5">
        <h2 className={UI.rotuloSecao}>{titulo}</h2>
        {meta && <span className={UI.meta}>{meta}</span>}
      </div>
      {children}
    </section>
  )
}
