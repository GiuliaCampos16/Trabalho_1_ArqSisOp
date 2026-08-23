import Pid from './Pid'
import { UI } from '../ui'

export default function Turnaround({ resultado }) {
  if (resultado.length === 0) return null

  const media = resultado.reduce((soma, p) => soma + p.turnaround, 0) / resultado.length

  return (
    <div className="overflow-x-auto">
      <table className={UI.tabela}>
        <thead>
          <tr>
            <th className={UI.th}>Processo</th>
            <th className={UI.th}>Chegada</th>
            <th className={UI.th}>Término</th>
            <th className={UI.th}>Turnaround</th>
          </tr>
        </thead>
        <tbody>
          {resultado.map((p) => (
            <tr key={p.pid}>
              <td className={UI.td}><Pid pid={p.pid} /></td>
              <td className={UI.td}>{p.chegada}</td>
              <td className={UI.td}>{p.termino}</td>
              <td className={`${UI.td} font-bold`}>{p.turnaround}</td>
            </tr>
          ))}
          <tr>
            <td className={`${UI.td} ${UI.microRotulo}`} colSpan={3}>Turnaround médio</td>
            <td className={`${UI.td} font-bold`}>{media.toFixed(2)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
