import { corProcesso } from '../cores'

export default function Pid({ pid }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className="h-3 w-[3px]" style={{ backgroundColor: corProcesso(pid) }} />
      <span className="font-bold">P{pid}</span>
    </span>
  )
}
