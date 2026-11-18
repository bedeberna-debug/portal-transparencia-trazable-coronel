export function rowRanges(rows: number[]): string {
  if (!rows.length) return 'Sin filas'
  const sorted = [...new Set(rows)].sort((a, b) => a - b)
  const ranges: string[] = []
  let start = sorted[0]
  let previous = sorted[0]
  for (let index = 1; index <= sorted.length; index += 1) {
    const current = sorted[index]
    if (current === previous + 1) { previous = current; continue }
    ranges.push(start === previous ? `${start}` : `${start}–${previous}`)
    start = current
    previous = current
  }
  return ranges.join(', ')
}

export function estadoInforme(estado?: string) {
  return ({
    descargado: 'PDF verificado en respaldo',
    sin_url: 'Sin URL publicada',
    dropbox_file_deleted: 'Eliminado en fuente',
    dropbox_link_temporarily_disabled: 'Suspendido temporalmente en fuente',
  } as Record<string, string>)[estado || ''] || estado || 'Estado no informado'
}
