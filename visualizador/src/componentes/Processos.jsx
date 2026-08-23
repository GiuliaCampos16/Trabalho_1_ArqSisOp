import Pid from './Pid'
import { UI } from '../ui'

function descreverIO(eventos) {
  if (eventos.length === 0) return '—'
  return eventos.map((e) => `${e.tipo} após ${e.disparo} u.t. de CPU (dura ${e.duracao})`).join(' · ')
}

export default function Processos({ processos }) {
  return (
    <div className="overflow-x-auto">
      <table className={UI.tabela}>
        <thead>
          <tr>
            <th className={UI.th}>Processo</th>
            <th className={UI.th}>Chegada</th>
            <th className={UI.th}>Tempo de CPU</th>
            <th className={UI.th}>Eventos de E/S</th>
          </tr>
        </thead>
        <tbody>
          {processos.map((p) => (
            <tr key={p.pid}>
              <td className={UI.td}><Pid pid={p.pid} /></td>
              <td className={UI.td}>{p.chegada}</td>
              <td className={UI.td}>{p.tempo_cpu}</td>
              <td className={`${UI.td} text-muted-foreground`}>{descreverIO(p.eventos_io)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
