import type { CommonData, ExplorerRow, FichaData, Trazabilidad } from '../types'

const base = import.meta.env.BASE_URL || './'
export async function fetchJSON<T>(file: string): Promise<T> {
  const response = await fetch(`${base}data/${file}`)
  if (!response.ok) throw new Error(`No se pudo cargar ${file}: HTTP ${response.status}`)
  return response.json() as Promise<T>
}

interface Artifact<T> { registros: T[] }
export async function loadCommonData(): Promise<CommonData> {
  const [meta, panel, estamentos, estamentosEstimados, genero, horas, resumen, ausencias, fuentes, desvinculacion, glosario] = await Promise.all([
    fetchJSON<CommonData['meta']>('meta.json'),
    fetchJSON<Artifact<CommonData['panel'][number]>>('panel_general_mensual.json'),
    fetchJSON<Artifact<CommonData['estamentos'][number]>>('composicion_estamento.json'),
    fetchJSON<Artifact<CommonData['estamentosEstimados'][number]>>('composicion_estamento_estimado.json'),
    fetchJSON<Artifact<CommonData['genero'][number]>>('composicion_genero_agregada.json'),
    fetchJSON<Artifact<CommonData['horas'][number]>>('horas_extra_mensual.json'),
    fetchJSON<{ categorias: CommonData['resumen'] }>('resumen_estamental.json'),
    fetchJSON<CommonData['ausencias']>('ausencias.json'),
    fetchJSON<CommonData['fuentes']>('fuentes.json'),
    fetchJSON<Artifact<CommonData['desvinculacion'][number]>>('codigo_desvinculacion_mensual.json'),
    fetchJSON<Artifact<CommonData['glosario'][number]>>('glosario_definiciones.json'),
  ])
  return { meta, panel: panel.registros, estamentos: estamentos.registros, estamentosEstimados: estamentosEstimados.registros, genero: genero.registros, horas: horas.registros, resumen: resumen.categorias, ausencias, fuentes, desvinculacion: desvinculacion.registros, glosario: glosario.registros }
}

export async function loadExplorerYear(year: number): Promise<ExplorerRow[]> {
  const data = await fetchJSON<Artifact<ExplorerRow>>(`explorador_${year}.json`)
  return data.registros
}

export async function loadFicha(id: string): Promise<FichaData> {
  return fetchJSON<FichaData>(`fichas/${encodeURIComponent(id)}.json`)
}

export function recordTrace(row: ExplorerRow): Trazabilidad {
  const source = row.fuente_ruta_relativa.replaceAll('\\', '/')
  const marker = 'datos crudos/04_Personal_y_Remuneraciones/'
  const relative = source.includes(marker) ? source.split(marker)[1] : row.fuente_archivo
  return {
    portal_oficial: 'https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=MU068',
    fuentes: [{
      archivo: row.fuente_archivo,
      ruta_relativa: row.fuente_ruta_relativa,
      url_respaldo: `fuentes/${relative}`,
      sha256: row.fuente_sha256,
      filas_csv: [row.fuente_fila_csv],
      registros: 1,
      periodos: [row.periodo],
    }],
  }
}

export const money = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 })
export const number = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 0 })
export const decimal = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 2 })
const monthNames = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
export function periodLabel(period: string) {
  const [year, month] = period.split('-')
  return `${monthNames[Number(month) - 1]} ${year}`
}
export function compactMoney(value: number) {
  if (Math.abs(value) >= 1_000_000_000) return `$${decimal.format(value / 1_000_000_000)} mil M`
  if (Math.abs(value) >= 1_000_000) return `$${decimal.format(value / 1_000_000)} M`
  return money.format(value)
}
export function combineTraces(traces: Trazabilidad[]): Trazabilidad {
  const map = new Map<string, { fuentes: import('../types').Fuente }>()
  const result: Trazabilidad = { portal_oficial: traces[0]?.portal_oficial || '', fuentes: [] }
  for (const trace of traces) for (const fuente of trace.fuentes) {
    const key = `${fuente.ruta_relativa}|${fuente.sha256}`
    if (!map.has(key)) {
      map.set(key, { fuentes: { ...fuente, filas_csv: [...fuente.filas_csv], periodos: [...fuente.periodos] } })
    } else {
      const existing = map.get(key)!.fuentes
      existing.filas_csv = [...new Set([...existing.filas_csv, ...fuente.filas_csv])].sort((a, b) => a - b)
      existing.periodos = [...new Set([...existing.periodos, ...fuente.periodos])].sort()
      existing.registros = existing.filas_csv.length
    }
  }
  result.fuentes = [...map.values()].map(v => v.fuentes).sort((a, b) => a.archivo.localeCompare(b.archivo))
  return result
}
export function publicUrl(path: string) {
  return `${base}${path.split('/').map(encodeURIComponent).join('/')}`
}
