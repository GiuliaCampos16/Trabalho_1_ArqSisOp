import { UI } from '../ui'

export default function Controles({ indice, total, tocando, setIndice, setTocando }) {
  const ir = (i) => {
    setTocando(false)
    setIndice(i)
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <button className={UI.botao} onClick={() => ir(0)} disabled={indice === 0}>Início</button>
      <button className={UI.botao} onClick={() => ir(indice - 1)} disabled={indice === 0}>Anterior</button>

      <button className={`${UI.botaoAtivo} w-24`} onClick={() => setTocando(!tocando)}>
        {tocando ? 'Pausar' : 'Executar'}
      </button>

      <button className={UI.botao} onClick={() => ir(indice + 1)} disabled={indice >= total - 1}>Próximo</button>
      <button className={UI.botao} onClick={() => ir(total - 1)} disabled={indice >= total - 1}>Fim</button>

      <input
        type="range"
        min={0}
        max={total - 1}
        value={indice}
        onChange={(e) => ir(Number(e.target.value))}
        className="h-1 min-w-[160px] flex-1 cursor-pointer accent-foreground"
      />
    </div>
  )
}
