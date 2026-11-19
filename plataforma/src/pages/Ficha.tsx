import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, BriefcaseBusiness, CalendarX2, Clock3, FileLock2 } from 'lucide-react'
import { Link, useParams } from 'react-router'
import { CartesianGrid, Line, LineChart, ReferenceDot, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { CommonData, FichaData, TrayectoriaEntry } from '../types'
import { combineTraces, compactMoney, decimal, loadFicha, money, number, periodLabel, publicUrl, recordTrace } from '../lib/data'
import { DataDisclosure, Loading, Metric, Notice, PageHeading, SectionHeading, ZeroNote } from '../components/Common'
import { GlossaryCard } from '../components/Glossary'
import { SourceButton } from '../components/Source'
import { RecordDetail } from './Explorador'

export default function Ficha({ data }: { data: CommonData }) {
  const { id = '' } = useParams()
  const [ficha, setFicha] = useState<FichaData | null>(null)
  const [error, setError] = useState('')
  const habilitada = data.meta.ficha_individual.habilitada
  useEffect(() => {
    let active = true
    setFicha(null)
    setError('')
    if (habilitada && id) loadFicha(id).then(result => { if (active) setFicha(result) }).catch(reason => { if (active) setError(reason.message) })
    return () => { active = false }
  }, [habilitada, id])

  if (!habilitada) return <div className="container page narrow-page">
    <Link className="back-link" to="/explorador"><ArrowLeft size={16} /> Volver al explorador</Link>
    <PageHeading eyebrow="Compuerta 1 · Ficha individual" title="Trayectoria individual deshabilitada"><p>La validación de unicidad persona-período no fue aprobada para esta publicación.</p></PageHeading>
    <div className="locked-record"><FileLock2 size={40} /><h2>No se publicó una ficha para este identificador</h2><p>La proyección conserva {data.meta.ficha_individual.colisiones_id_periodo} colisiones sin resolver. Ninguna versión se eligió por monto, orden de fila o posterioridad.</p></div>
    <a className="button secondary" href={publicUrl('docs/VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md')} target="_blank" rel="noreferrer">Abrir validación de unicidad</a>
  </div>
  if (error) return <div className="container page narrow-page"><Link className="back-link" to="/explorador"><ArrowLeft size={16} /> Volver al explorador</Link><Notice title="No existe una ficha para este identificador" tone="warning"><p>{error}</p></Notice></div>
  if (!ficha) return <Loading label="Cargando trayectoria individual y sus fuentes…" />
  return <FichaPublicada ficha={ficha} data={data} />
}

function FichaPublicada({ ficha, data }: { ficha: FichaData; data: CommonData }) {
  const publicadas = useMemo(() => ficha.trayectoria.filter((entry): entry is TrayectoriaEntry & { registro: NonNullable<TrayectoriaEntry['registro']> } => Boolean(entry.registro)), [ficha])
  const alternas = useMemo(() => ficha.trayectoria.flatMap(entry => entry.versiones_alternas), [ficha])
  const trazabilidad = useMemo(() => combineTraces([...publicadas.map(entry => recordTrace(entry.registro)), ...alternas.map(recordTrace)]), [publicadas, alternas])
  const cambiosCargo = useMemo(() => publicadas.filter(entry => entry.registro.analisis_cargo?.estado === 'cambio_cargo'), [publicadas])
  const conHoras = useMemo(() => publicadas.filter(entry => (entry.registro.horas_extra_horas_total || 0) > 0), [publicadas])
  const chartRows = ficha.trayectoria.map(entry => ({
    periodo: entry.periodo,
    bruto: entry.registro && entry.registro.remuneracion_bruta_clp > 0 ? entry.registro.remuneracion_bruta_clp : null,
  }))
  const primerPeriodo = publicadas[0]?.periodo
  const ultimoPeriodo = publicadas.at(-1)?.periodo
  const ceros = publicadas.filter(entry => entry.registro.remuneracion_bruta_clp === 0).length
  const tieneEstimado = data.meta.estamento_estimado.categorias_cubiertas.includes(ficha.categoria)
  const estimados = [...new Set(publicadas.map(entry => entry.registro.estamento_estimado || 'No clasificable'))].sort()

  return <div className="container page wide-page ficha-page">
    <Link className="back-link" to={`/explorador?categoria=${encodeURIComponent(ficha.categoria)}`}><ArrowLeft size={16} /> Volver a {ficha.categoria}</Link>
    <PageHeading eyebrow={`${ficha.categoria} · ${ficha.id_trabajador}`} title={ficha.nombre_original}>
      <p>Trayectoria mensual construida solo con publicaciones municipales. Los meses sin registro permanecen vacíos y toda versión alterna se conserva.</p>
      <div className="glossary-inline"><GlossaryCard entries={data.glosario} term="Asignaciones especiales" label="Sobre las asignaciones" /></div>
    </PageHeading>

    <section className="identity-strip" aria-label="Identidad y clasificación publicada">
      <div><span>Categoría</span><strong>{ficha.categoria}</strong></div>
      <div><span>Estamento publicado</span><strong>{ficha.estamentos.join(' · ')}</strong>{tieneEstimado && <small className="estimated-individual">Estimado: {estimados.join(' · ')}</small>}</div>
      <div className="identity-role"><span>Cargo(s) publicado(s)</span><strong>{ficha.cargos.join(' · ')}</strong></div>
    </section>
    <div className="glossary-inline"><GlossaryCard entries={data.glosario} term={ficha.categoria} /><GlossaryCard entries={data.glosario} term="Estamento" label="Qué es el estamento" />{tieneEstimado && <GlossaryCard entries={data.glosario} term="Estamento estimado" label="Sobre la estimación" />}</div>
    {tieneEstimado && <p className="estimated-legend">{data.meta.estamento_estimado.leyenda_fija}</p>}
    <details className="trajectory-convention"><summary>Convención de trayectoria D-15 — detalles</summary><div><GlossaryCard entries={data.glosario} term="Trayectoria (convención D-15)" /><p>{ficha.nota_reconciliacion}</p><p>La selección por coincidencia entre período de contenido y archivo nominal es una convención de visualización; no declara cuál versión es jurídicamente correcta.</p></div></details>

    <section className="data-section" aria-labelledby="resumen-ficha">
      <SectionHeading title="Cobertura de la trayectoria" description="36 meses considerados, de enero de 2023 a diciembre de 2025." action={<a className="button secondary small" href={publicUrl(`data/fichas/${ficha.id_trabajador}.json`)} target="_blank" rel="noreferrer">JSON de la ficha</a>} />
      <div className="metrics-grid three" id="resumen-ficha">
        <Metric label="Períodos publicados" value={number.format(ficha.conteos.periodos_publicados)} note="una versión seleccionada por mes" source={<SourceButton trace={combineTraces(publicadas.map(entry => recordTrace(entry.registro)))} title={`Períodos publicados de ${ficha.id_trabajador}`} compact />} />
        <Metric label="Ausencias declaradas" value={number.format(ficha.conteos.ausencias)} note="sin imputación ni interpolación" source={<SourceButton trace={trazabilidad} title={`Cobertura y ausencias de ${ficha.id_trabajador}`} compact />} />
        <Metric label="Versiones alternas" value={number.format(ficha.conteos.versiones_alternas)} note="íntegras y fuera de la línea seleccionada" source={<SourceButton trace={combineTraces(alternas.map(recordTrace))} title={`Versiones alternas de ${ficha.id_trabajador}`} compact />} />
      </div>
      <ZeroNote count={ceros} entries={data.glosario} />
    </section>

    <section className="data-section" aria-labelledby="grafico-trayectoria">
      <SectionHeading title="Remuneración bruta por mes" description="La línea se interrumpe donde no hay registro o donde el bruto es 0 canónico. Nunca conecta esos huecos con valores estimados." />
      <div className="chart-wrap trajectory-chart" id="grafico-trayectoria">
        <ResponsiveContainer width="100%" height={340}>
          <LineChart data={chartRows} margin={{ top: 20, right: 18, left: 8, bottom: 4 }}>
            <CartesianGrid vertical={false} stroke="#dce4e5" />
            <XAxis dataKey="periodo" interval={2} tick={{ fontSize: 11, fill: '#4c5c61' }} tickLine={false} />
            <YAxis tickFormatter={value => compactMoney(Number(value))} width={88} tick={{ fontSize: 11, fill: '#4c5c61' }} axisLine={false} tickLine={false} />
            <Tooltip formatter={value => [money.format(Number(value)), 'Bruto publicado']} labelFormatter={label => `Período: ${label}`} contentStyle={{ border: '1px solid #cbd7d9', borderRadius: 6, background: '#f8faf9' }} />
            <Line type="linear" dataKey="bruto" stroke="#16756f" strokeWidth={2.5} connectNulls={false} dot={{ r: 3, fill: '#16756f' }} activeDot={{ r: 5 }} isAnimationActive={false} />
            {cambiosCargo.map(entry => <ReferenceDot key={`cargo-${entry.periodo}`} x={entry.periodo} y={entry.registro.remuneracion_bruta_clp} r={7} fill="#bd6b2e" stroke="#f8faf9" strokeWidth={2} />)}
            {conHoras.map(entry => <ReferenceDot key={`horas-${entry.periodo}`} x={entry.periodo} y={entry.registro.remuneracion_bruta_clp} r={9} fill="none" stroke="#123c4a" strokeWidth={1.5} />)}
          </LineChart>
        </ResponsiveContainer>
        <div className="chart-legend"><span><i style={{ background: '#16756f' }} />Bruto seleccionado</span><span><i style={{ background: '#bd6b2e' }} />Cambio de cargo</span><span><i className="ring-legend" />Mes con horas extra</span></div>
      </div>
      <DataDisclosure title="Ver los 36 meses, valores y fuentes del gráfico"><div className="table-scroll tall"><table><thead><tr><th>Período</th><th>Estado</th><th>Bruto CLP</th><th>Cargo</th><th>Fuente</th></tr></thead><tbody>{ficha.trayectoria.map(entry => <tr key={entry.periodo}><td>{entry.periodo}</td><td>{entry.registro ? 'Publicado' : 'Sin registro; no imputado'}</td><td className="numeric">{entry.registro ? entry.registro.remuneracion_bruta_clp === 0 ? 'No informa (0)' : money.format(entry.registro.remuneracion_bruta_clp) : '—'}</td><td>{entry.registro?.cargo_funcion || '—'}</td><td>{entry.registro ? <SourceButton trace={recordTrace(entry.registro)} title={`${ficha.nombre_original}, ${entry.periodo}`} compact /> : 'Sin fila fuente para este ID'}</td></tr>)}</tbody></table></div></DataDisclosure>
    </section>

    <section className="data-section" aria-labelledby="detalle-trayectoria">
      <SectionHeading title="Trayectoria mensual y detalle publicado" description="Abra un mes para revisar los campos principales y su fuente. Los demás indicadores quedan plegados; toda otra publicación del período se conserva." />
      <div className="trajectory-years" id="detalle-trayectoria">{[2023, 2024, 2025].map(year => <section key={year} className="trajectory-year" aria-labelledby={`anio-${year}`}>
        <h2 id={`anio-${year}`}>{year}</h2>
        <div className="trajectory-list">{ficha.trayectoria.filter(entry => entry.periodo.startsWith(String(year))).map(entry => <MonthRecord key={entry.periodo} entry={entry} ficha={ficha} primero={entry.periodo === primerPeriodo} ultimo={entry.periodo === ultimoPeriodo} />)}</div>
      </section>)}</div>
    </section>
    <p className="privacy-note">Esta ficha reproduce campos publicados por el municipio. No contiene género ni variables individuales derivadas del nombre.</p>
  </div>
}

const monthlyBaseKeys = [
  'estamento', 'cargo_funcion', 'grado_eus_jornada', 'calificacion_profesional',
  'fecha_inicio', 'fecha_termino', 'asignaciones_especiales_raw', 'asignaciones_decodificadas',
  'remuneracion_bruta_clp', 'remuneracion_liquida_clp', 'viaticos_clp',
  'horas_extra_horas_total', 'horas_extra_monto_total',
  'horas_extra_diurnas_raw', 'horas_extra_diurnas_horas', 'horas_extra_diurnas_clp',
  'horas_extra_nocturnas_raw', 'horas_extra_nocturnas_horas', 'horas_extra_nocturnas_clp',
  'horas_extra_festivas_raw', 'horas_extra_festivas_horas', 'horas_extra_festivas_clp',
  'horas_extra_raw', 'horas_extra_horas', 'horas_extra_clp',
]
const sourceKeys = ['fuente_archivo', 'fuente_fila_csv', 'fuente_sha256']

function MonthRecord({ entry, ficha, primero, ultimo }: { entry: TrayectoriaEntry; ficha: FichaData; primero: boolean; ultimo: boolean }) {
  if (!entry.registro) return <div className="trajectory-absence" data-period={entry.periodo}><CalendarX2 size={18} /><div><strong>{periodLabel(entry.periodo)}</strong><span>Sin registro publicado para este ID y categoría</span><small>{entry.causa_ausencia}</small></div></div>
  const row = entry.registro
  const analisis = row.analisis_cargo
  return <details className="month-record" data-period={entry.periodo}>
    <summary><span className="month-title">{periodLabel(entry.periodo)}</span><span className="month-amount">{row.remuneracion_bruta_clp === 0 ? 'No informa (0)' : money.format(row.remuneracion_bruta_clp)}</span><span className="month-role">{row.cargo_funcion}</span></summary>
    <div className="month-content">
      <div className="month-markers">
        {primero && <span>Primer registro de la secuencia publicada</span>}
        {ultimo && <span>Último registro en el período analizado</span>}
        {analisis?.estado === 'cambio_cargo' && <span className="cargo-change"><BriefcaseBusiness size={14} /> Cambio de cargo respecto del mes publicado anterior</span>}
        {analisis?.estado === 'posible_variante' && <span className="cargo-review">Posible variante, requiere verificación</span>}
        {(row.horas_extra_horas_total || 0) > 0 && <span><Clock3 size={14} /> {decimal.format(row.horas_extra_horas_total || 0)} horas extra</span>}
      </div>
      {analisis?.estado === 'variante_escritura' && <details className="writing-variant"><summary>Variante de escritura — detalles</summary><div><p>{analisis.explicacion}</p><p><strong>Publicación anterior ({analisis.periodo_anterior}):</strong> {analisis.cargo_anterior}</p><p><strong>Normalización usada solo para comparar:</strong> <code>{analisis.cargo_normalizado_proyecto}</code></p></div></details>}
      {analisis?.estado === 'posible_variante' && <div className="cargo-comparison"><p>{analisis.explicacion}</p><small>Publicación anterior ({analisis.periodo_anterior}): {analisis.cargo_anterior}. No se fusionaron ni sobrescribieron los cargos.</small></div>}
      <MonthFacts row={row} sourceTitle={`${ficha.nombre_original}, ${entry.periodo}`} />
      {entry.versiones_alternas.map(alterna => <section className="alternate-publication" key={alterna.registro_id} aria-label={`Otra publicación de ${entry.periodo}`}>
        <h3>Otra publicación del mismo período</h3>
        <p>Esta versión no alimenta la línea de trayectoria: su período de contenido ({alterna.periodo}) difiere del período nominal de su archivo ({alterna.periodo_nominal_archivo || 'no identificable'}). Se conserva íntegra conforme a D-15.</p>
        <dl className="alternate-facts"><div><dt>Registro alterno</dt><dd><code>{alterna.registro_id}</code></dd></div><div><dt>Rol</dt><dd><code>{alterna.rol_trayectoria}</code></dd></div><div><dt>Versión seleccionada</dt><dd><code>{alterna.version_alterna_de}</code></dd></div><div><dt>Motivo</dt><dd><code>{alterna.motivo_version_alterna}</code></dd></div><div><dt>Bruto / líquido de esta publicación</dt><dd>{money.format(alterna.remuneracion_bruta_clp)} / {money.format(alterna.remuneracion_liquida_clp)}</dd></div></dl>
        <MonthFacts row={alterna} sourceTitle={`Versión alterna de ${ficha.nombre_original}, ${entry.periodo}`} />
      </section>)}
    </div>
  </details>
}

function MonthFacts({ row, sourceTitle }: { row: NonNullable<TrayectoriaEntry['registro']>; sourceTitle: string }) {
  const primaryKeys = [
    ...monthlyBaseKeys.slice(0, 1),
    ...(['Código del Trabajo', 'Honorarios'].includes(row.categoria) ? ['estamento_estimado'] : []),
    ...monthlyBaseKeys.slice(1),
    ...(row.categoria === 'Honorarios' ? ['tipo_pago', 'descripcion_pago', 'numero_cuotas'] : []),
  ]
  const additionalKeys = Object.keys(row).filter(key => !primaryKeys.includes(key) && !sourceKeys.includes(key) && !['ficha_habilitada', 'analisis_cargo'].includes(key))
  return <div className="month-facts">
    <RecordDetail row={row} keys={primaryKeys} className="month-primary-facts" />
    <DataDisclosure title="+ indicadores"><RecordDetail row={row} keys={additionalKeys} className="month-additional-facts" /></DataDisclosure>
    <div className="month-source" data-testid="month-source">
      <dl><div><dt>Archivo fuente</dt><dd>{row.fuente_archivo}</dd></div><div><dt>Fila CSV</dt><dd>{row.fuente_fila_csv}</dd></div><div><dt>SHA-256</dt><dd className="hash break-anywhere">{row.fuente_sha256}</dd></div></dl>
      <SourceButton trace={recordTrace(row)} title={sourceTitle} />
    </div>
  </div>
}
