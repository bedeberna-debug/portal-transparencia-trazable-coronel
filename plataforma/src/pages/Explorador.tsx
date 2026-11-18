import { useEffect, useMemo, useState } from 'react'
import { ChevronLeft, ChevronRight, Download, FilterX, Search } from 'lucide-react'
import { Link, useSearchParams } from 'react-router'
import type { Categoria, CommonData, ExplorerRow } from '../types'
import { CATEGORIAS } from '../types'
import { combineTraces, loadExplorerYear, money, number, decimal, recordTrace } from '../lib/data'
import { DataDisclosure, GenderLegend, Loading, Metric, Notice, PageHeading, ZeroNote } from '../components/Common'
import { GlossaryCard } from '../components/Glossary'
import { SourceButton } from '../components/Source'
import { estadoInforme } from '../lib/format'

interface Filters {
  desde: string
  hasta: string
  categoria: string
  estamento: string
  cargo: string
  brutoMin: string
  brutoMax: string
  horasMin: string
  horasMax: string
  termino: string
}
const initialFilters: Filters = { desde: '2023-01', hasta: '2025-12', categoria: 'Todas', estamento: 'Todos', cargo: '', brutoMin: '', brutoMax: '', horasMin: '', horasMax: '', termino: 'Todos' }
const PAGE_SIZE = 50
export default function Explorador({ data }: { data: CommonData }) {
  const [searchParams] = useSearchParams()
  const queryCategory = searchParams.get('categoria')
  const [filters, setFilters] = useState<Filters>({ ...initialFilters, categoria: queryCategory && CATEGORIAS.includes(queryCategory as Categoria) ? queryCategory : 'Todas' })
  const [records, setRecords] = useState<ExplorerRow[]>([])
  const [loadedYears, setLoadedYears] = useState(0)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  useEffect(() => {
    let active = true
    setLoadedYears(0)
    Promise.all([2023, 2024, 2025].map(async year => {
      const rows = await loadExplorerYear(year)
      if (active) setLoadedYears(value => value + 1)
      return rows
    })).then(years => { if (active) setRecords(years.flat()) }).catch(reason => { if (active) setError(reason.message) })
    return () => { active = false }
  }, [])
  const estamentos = useMemo(() => [...new Set(records.map(row => row.estamento))].sort(), [records])
  const filtered = useMemo(() => records.filter(row => {
    if (row.periodo < filters.desde || row.periodo > filters.hasta) return false
    if (filters.categoria !== 'Todas' && row.categoria !== filters.categoria) return false
    if (filters.estamento !== 'Todos' && row.estamento !== filters.estamento) return false
    if (filters.cargo && !row.cargo_funcion.toLocaleLowerCase('es').includes(filters.cargo.toLocaleLowerCase('es'))) return false
    if ((filters.brutoMin || filters.brutoMax) && row.remuneracion_bruta_clp === 0) return false
    if (filters.brutoMin && row.remuneracion_bruta_clp < Number(filters.brutoMin)) return false
    if (filters.brutoMax && row.remuneracion_bruta_clp > Number(filters.brutoMax)) return false
    if ((filters.horasMin || filters.horasMax) && row.horas_extra_horas_total === null) return false
    if (filters.horasMin && (row.horas_extra_horas_total || 0) < Number(filters.horasMin)) return false
    if (filters.horasMax && (row.horas_extra_horas_total || 0) > Number(filters.horasMax)) return false
    if (filters.termino !== 'Todos' && row.fecha_termino_tipo !== filters.termino) return false
    return true
  }).sort((a, b) => b.periodo.localeCompare(a.periodo) || a.nombre_original.localeCompare(b.nombre_original)), [records, filters])
  useEffect(() => { setPage(1) }, [filters])
  const summary = useMemo(() => {
    const informed = filtered.filter(row => row.remuneracion_bruta_clp > 0).map(row => row.remuneracion_bruta_clp).sort((a, b) => a - b)
    const middle = Math.floor(informed.length / 2)
    const median = informed.length ? informed.length % 2 ? informed[middle] : (informed[middle - 1] + informed[middle]) / 2 : null
    return { bruto: filtered.reduce((sum, row) => sum + row.remuneracion_bruta_clp, 0), noInforma: filtered.filter(row => row.remuneracion_bruta_clp === 0).length, median }
  }, [filtered])
  const individualFilter = Boolean(filters.cargo || filters.brutoMin || filters.brutoMax || filters.horasMin || filters.horasMax || filters.termino !== 'Todos')
  const gender = useMemo(() => {
    if (individualFilter) return null
    const rows = data.genero.filter(row => row.periodo >= filters.desde && row.periodo <= filters.hasta && (filters.categoria === 'Todas' || row.categoria === filters.categoria) && (filters.estamento === 'Todos' || row.estamento === filters.estamento))
    return { femenino: rows.reduce((s, r) => s + r.femenino, 0), masculino: rows.reduce((s, r) => s + r.masculino, 0), registros: rows.reduce((s, r) => s + r.registros, 0), trace: combineTraces(rows.map(r => r.trazabilidad)) }
  }, [data.genero, filters, individualFilter])
  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const visible = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)
  const update = (key: keyof Filters, value: string) => setFilters(current => ({ ...current, [key]: value }))
  const exportCSV = () => {
    if (!filtered.length) return
    const columns = [...new Set(filtered.flatMap(row => Object.keys(row)))].filter(column => column !== 'ficha_habilitada')
    const escape = (value: unknown) => {
      const text = value !== null && typeof value === 'object' ? JSON.stringify(value) : String(value ?? '')
      return `"${text.replaceAll('"', '""')}"`
    }
    const csv = '﻿' + [columns.map(escape).join(';'), ...filtered.map(row => columns.map(column => escape(row[column])).join(';'))].join('\r\n')
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `personal_coronel_filtrado_${filters.desde}_${filters.hasta}.csv`
    anchor.click()
    URL.revokeObjectURL(url)
  }
  if (error) return <div className="container page"><Notice title="No se pudieron cargar los detalles anuales" tone="warning"><p>{error}</p></Notice></div>
  if (!records.length) return <div className="container page"><Loading label={`Cargando detalle anual: ${loadedYears} de 3 archivos…`} /><p className="loading-note">El resto del sitio usa agregados ligeros; esta vista descarga los registros públicos para permitir filtros arbitrarios.</p></div>
  return <div className="container page wide-page">
    <PageHeading eyebrow="Explorador transversal" title="Busque en todo el universo de personal"><p>Filtre 22.940 registros persona-mes y exporte el subconjunto con su trazabilidad. El género no es un filtro ni forma parte del detalle individual.</p><div className="glossary-inline"><GlossaryCard entries={data.glosario} term="Persona-mes" label="Unidad de conteo" /><GlossaryCard entries={data.glosario} term="Estamento" label="Qué es el estamento" /><GlossaryCard entries={data.glosario} term="Estamento estimado" label="Sobre la estimación" /><GlossaryCard entries={data.glosario} term="Asignaciones especiales" label="Sobre las asignaciones" /></div><p className="estimated-legend">{data.meta.estamento_estimado.leyenda_fija} Se muestra como «estimado» solo en Código del Trabajo y Honorarios.</p></PageHeading>
    <section className="filter-panel" aria-label="Filtros del explorador"><div className="filter-grid">
      <label>Período desde<input type="month" min="2023-01" max="2025-12" value={filters.desde} onChange={e => update('desde', e.target.value)} /></label>
      <label>Período hasta<input type="month" min="2023-01" max="2025-12" value={filters.hasta} onChange={e => update('hasta', e.target.value)} /></label>
      <label>Categoría<select value={filters.categoria} onChange={e => { update('categoria', e.target.value); update('estamento', 'Todos') }}><option>Todas</option>{CATEGORIAS.map(item => <option key={item}>{item}</option>)}</select></label>
      <label>Estamento<select value={filters.estamento} onChange={e => update('estamento', e.target.value)}><option>Todos</option>{estamentos.filter(item => filters.categoria === 'Todas' || records.some(row => row.categoria === filters.categoria && row.estamento === item)).map(item => <option key={item}>{item}</option>)}</select></label>
      <label className="filter-wide">Cargo o función<input type="search" placeholder="Ej.: secretaria, profesional, conductor" value={filters.cargo} onChange={e => update('cargo', e.target.value)} /></label>
      <label>Bruto mínimo CLP<input type="number" min="0" placeholder="Sin mínimo" value={filters.brutoMin} onChange={e => update('brutoMin', e.target.value)} /></label>
      <label>Bruto máximo CLP<input type="number" min="0" placeholder="Sin máximo" value={filters.brutoMax} onChange={e => update('brutoMax', e.target.value)} /></label>
      <label>Horas extra mínimas<input type="number" min="0" step="0.01" placeholder="Sin mínimo" value={filters.horasMin} onChange={e => update('horasMin', e.target.value)} /></label>
      <label>Horas extra máximas<input type="number" min="0" step="0.01" placeholder="Sin máximo" value={filters.horasMax} onChange={e => update('horasMax', e.target.value)} /></label>
      <label>Tipo de término<select value={filters.termino} onChange={e => update('termino', e.target.value)}><option>Todos</option><option value="indefinido">Indefinido</option><option value="fecha">Fecha</option><option value="no_informa">No informa</option><option value="no_especificado">No especificado</option><option value="otro">Otro</option></select></label>
    </div><div className="filter-actions"><span><Search size={16} />{number.format(filtered.length)} registros seleccionados</span><button className="button ghost" onClick={() => setFilters({ ...initialFilters, categoria: filters.categoria })}><FilterX size={16} /> Limpiar filtros</button></div></section>
    {filters.desde > filters.hasta && <Notice title="Rango de períodos invertido" tone="warning"><p>La fecha inicial es posterior a la final. Ajuste el rango para obtener registros.</p></Notice>}

    <section className="data-section"><div className="metrics-grid four"><Metric label="Registros" value={number.format(filtered.length)} note="persona-mes; no personas únicas" source={<SourceButton trace={combineTraces(filtered.map(recordTrace))} title="Subconjunto filtrado" compact />} /><Metric label="Gasto bruto" value={money.format(summary.bruto)} note={`${summary.noInforma} registros con 0 canónico`} source={<SourceButton trace={combineTraces(filtered.map(recordTrace))} title="Gasto del subconjunto" compact />} /><Metric label="Mediana bruta informada" value={summary.median === null ? 'Sin datos' : money.format(summary.median)} note="Excluye 0 canónico / no informa" source={<SourceButton trace={combineTraces(filtered.filter(r => r.remuneracion_bruta_clp > 0).map(recordTrace))} title="Mediana del subconjunto" compact />} />
      {gender && gender.registros ? <Metric label="Género agregado" value={`${decimal.format(gender.femenino / gender.registros * 100)}% F`} note={`${decimal.format(gender.masculino / gender.registros * 100)}% M · ${number.format(gender.registros)} registros`} source={<SourceButton trace={gender.trace} title="Género agregado del subconjunto" compact />} /> : <div className="metric unavailable"><span className="metric-label">Género agregado</span><strong className="metric-value small-value">No calculable</strong><span className="metric-note">Los filtros individuales no se cruzan con género para proteger D-14.</span></div>}
      </div><ZeroNote count={summary.noInforma} entries={data.glosario} />{gender && <GenderLegend text={data.meta.privacidad.leyenda} />}{individualFilter && <Notice title="Ausencia de porcentaje por privacidad"><p>El porcentaje exacto está disponible con filtros de período, categoría y estamento. Al filtrar por cargo, monto, horas o término no se expone género individual para calcularlo.</p></Notice>}</section>

    <section className="data-section"><div className="table-toolbar"><div><h2>Registros persona-mes</h2><p>Página {page} de {pageCount} · {number.format(filtered.length)} resultados</p></div><button className="button primary" disabled={!filtered.length} onClick={exportCSV}><Download size={17} /> Exportar CSV trazable</button></div>
      <div className="table-scroll explorer-table"><table><thead><tr><th>Período</th><th>Nombre / ficha</th><th>Categoría</th><th>Estamento</th><th>Cargo</th><th>Bruto CLP</th><th>Horas extra</th><th>Término</th><th>Fuente</th><th>Detalle</th></tr></thead><tbody>{visible.map(row => <tr key={row.registro_id} data-record={row.registro_id}><td className="nowrap">{row.periodo}</td><td className="person-cell"><Link to={`/ficha/${encodeURIComponent(row.id_trabajador)}`} title={row.ficha_habilitada ? 'Abrir trayectoria individual' : 'Ficha deshabilitada por validación de unicidad'}>{row.nombre_original}</Link><small>{row.ficha_habilitada ? 'Abrir ficha' : 'Ficha bloqueada'}</small></td><td>{row.categoria}</td><td>{row.estamento}{['Código del Trabajo', 'Honorarios'].includes(row.categoria) && <small className="estimated-individual">Estimado: {row.estamento_estimado || 'No clasificable'}</small>}</td><td>{row.cargo_funcion}</td><td className="numeric nowrap">{row.remuneracion_bruta_clp === 0 ? <span className="missing-value">No informa <small>(0)</small></span> : money.format(row.remuneracion_bruta_clp)}</td><td className="numeric">{row.horas_extra_horas_total === null ? <span className="missing-value">No publica</span> : decimal.format(row.horas_extra_horas_total)}</td><td>{row.fecha_termino_tipo.replaceAll('_', ' ')}</td><td><SourceButton trace={recordTrace(row)} title={`${row.nombre_original}, ${row.periodo}`} compact /></td><td><DataDisclosure title="Campos"><RecordDetail row={row} /></DataDisclosure></td></tr>)}</tbody></table>{!visible.length && <div className="empty-state"><h3>No hay registros para esta selección</h3><p>Modifique o limpie los filtros. Ningún resultado se completó con valores estimados.</p></div>}</div>
      <div className="pagination"><button className="button secondary" disabled={page <= 1} onClick={() => setPage(value => value - 1)}><ChevronLeft size={16} /> Anterior</button><span>Página {page} / {pageCount}</span><button className="button secondary" disabled={page >= pageCount} onClick={() => setPage(value => value + 1)}>Siguiente <ChevronRight size={16} /></button></div>
    </section>
  </div>
}

export function RecordDetail({ row }: { row: ExplorerRow }) {
  const labels: Record<string, string> = {
    registro_id: 'ID de registro', id_trabajador: 'ID heredado', nombre_original: 'Nombre publicado',
    cargo_funcion: 'Cargo o función publicado', cargo_normalizado_proyecto: 'Cargo normalizado (solo comparación)',
    estamento_raw: 'Estamento original', estamento_estimado: 'Estamento estimado (proyecto)',
    estado_clasificacion_estimada: 'Estado de clasificación estimada', regla_estamento_estimado: 'Regla de estimación',
    origen_estamento_estimado: 'Origen de la estimación', justificacion_estamento_estimado: 'Justificación de la estimación',
    asignaciones_especiales_raw: 'Asignaciones especiales publicadas (_raw)', asignaciones_decodificadas: 'Conceptos de asignaciones especiales',
    remuneracion_bruta_raw: 'Bruto publicado (_raw)', remuneracion_liquida_raw: 'Líquido publicado (_raw)',
    fuente_archivo: 'Archivo fuente', fuente_fila_csv: 'Fila CSV', fuente_sha256: 'SHA-256',
    informe_estado: 'Informe de funciones', informe_archivo_respaldo: 'Ruta de respaldo',
    informe_sha256: 'SHA-256 del informe', enlace_funciones_desarrolladas_raw: 'Enlace publicado (_raw)',
  }
  return <div className="record-detail"><dl>{Object.entries(row).filter(([key]) => !['ficha_habilitada', 'informe_respaldo_disponible', 'analisis_cargo'].includes(key)).map(([key, value]) => <div key={key}><dt>{labels[key] || key.replaceAll('_', ' ')}</dt><dd className={key.includes('sha256') ? 'hash break-anywhere' : ''}>{
    key === 'informe_estado' ? estadoInforme(String(value))
      : key === 'asignaciones_decodificadas' ? <AssignmentList row={row} />
        : key === 'estamento_estimado' && row.estado_clasificacion_estimada === 'no_clasificable' ? <span className="missing-value">No clasificable (estimado)</span>
          : value === null || value === undefined || value === '' ? <span className="missing-value">No informa / no aplica</span> : String(value)
  }</dd></div>)}</dl>{row.categoria === 'Honorarios' && <Notice title="Disponibilidad del informe"><p>{estadoInforme(row.informe_estado)}. {row.informe_respaldo_disponible ? 'El PDF está verificado en el respaldo documental del proyecto; no se duplicó dentro de esta distribución estática.' : 'No hay un PDF verificado disponible en el respaldo.'}</p>{typeof row.enlace_funciones_desarrolladas_url === 'string' && row.enlace_funciones_desarrolladas_url && <a className="text-link" href={row.enlace_funciones_desarrolladas_url} target="_blank" rel="noreferrer">Abrir URL publicada originalmente</a>}</Notice>}</div>
}

function AssignmentList({ row }: { row: ExplorerRow }) {
  const assignments = row.asignaciones_decodificadas || []
  if (!assignments.length) return <span className="missing-value">No informa / no aplica</span>
  return <ul className="assignment-list" data-record={row.registro_id}>{assignments.map((assignment, index) => <li key={`${assignment.codigo_raw}-${index}`} className={assignment.estado === 'no_decodificado' ? 'assignment-anomaly' : ''}><code>{assignment.codigo_raw}</code><span>{assignment.nombre || 'Código sin decodificar'}</span>{assignment.nota && <small>{assignment.nota}</small>}</li>)}</ul>
}
