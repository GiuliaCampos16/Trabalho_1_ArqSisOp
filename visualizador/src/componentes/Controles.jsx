import { UI } from '../ui'

const VELOCIDADES = [
  { ms: 900, rotulo: 'Lento' },
  { ms: 500, rotulo: 'Normal' },
  { ms: 200, rotulo: 'Rápido' },
]

export default function Controles({ indice, ultimo, tocando, velocidade, irPara, alternarPlay, setVelocidade }) {
  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-2">
        <button className={UI.botao} onClick={() => irPara(0)} disabled={indice === 0}>Início</button>
        <button className={UI.botao} onClick={() => irPara(indice - 1)} disabled={indice === 0}>Anterior</button>

        <button className={`${UI.botaoAtivo} w-24`} onClick={alternarPlay}>
          {tocando ? 'Pausar' : indice >= ultimo ? 'Repetir' : 'Executar'}
        </button>

        <button className={UI.botao} onClick={() => irPara(indice + 1)} disabled={indice >= ultimo}>Próximo</button>
        <button className={UI.botao} onClick={() => irPara(ultimo)} disabled={indice >= ultimo}>Fim</button>

        <input
          type="range"
          min={0}
          max={ultimo}
          value={indice}
          onChange={(e) => irPara(Number(e.target.value))}
          className="h-1 min-w-[160px] flex-1 cursor-pointer accent-foreground"
        />

        <div className="flex gap-1">
          {VELOCIDADES.map((v) => (
            <button
              key={v.ms}
              onClick={() => setVelocidade(v.ms)}
              className={v.ms === velocidade ? UI.botaoAtivo : UI.botao}
            >
              {v.rotulo}
            </button>
          ))}
        </div>
      </div>

      <p className={UI.microRotulo}>
        setas para andar &middot; espaço para executar &middot; clique no gráfico para saltar
      </p>
    </div>
  )
}
