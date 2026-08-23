export function corProcesso(pid, alfa = 1) {
  const cor = `--proc-${((pid - 1) % 10) + 1}`;
  return alfa === 1 ? `hsl(var(${cor}))` : `hsl(var(${cor}) / ${alfa})`;
}

export function hachuraIO(pid, atendido) {
  const traco = corProcesso(pid, atendido ? 0.7 : 0.35);
  const fundo = corProcesso(pid, 0.08);
  return {
    backgroundImage: `repeating-linear-gradient(45deg, ${traco} 0 1px, ${fundo} 1px ${atendido ? 4 : 7}px)`,
  };
}

export function estadoDoProcesso(passo, pid) {
  if (passo.cpu !== null && passo.cpu.pid === pid) return "executando";
  if (passo.io_ativo === pid) return "io";
  if (passo.io.some((p) => p.pid === pid)) return "espera_io";
  if (passo.prontos.some((fila) => fila.some((p) => p.pid === pid)))
    return "pronto";
  return null;
}
