import { useEffect, useState } from 'react'
import { ArrowRight } from 'lucide-react'
import { Link, Navigate, useParams } from 'react-router'
import type { Categoria, CommonData } from '../types'
import { CATEGORIAS } from '../types'
import { combineTraces, compactMoney, decimal, money, number, periodLabel } from '../lib/data'
import { COLORS, EstamentoStackedChart, SimpleBars } from '../components/Charts'
import type { DimensionEstamento, MetricaBarra } from '../components/Charts'
import { DataDisclosure, GenderLegend, Metric, Notice, PageHeading, SectionHeading, ZeroNote } from '../components/Common'
import { GlossaryCard } from '../components/Glossary'
import { SourceButton } from '../components/Source'
import { estadoInforme } from '../lib/format'

export default function Estamental({ data }: { data: CommonData }) {
  const { categoria: raw } = useParams()
  const categoria = decodeURIComponent(raw || '') as Categoria
  const [metric, setMetric] = useState<MetricaBarra>('dotacion_registros')
  const [dimension, setDimension] = useState<DimensionEstamento>(categoria === 'Honorarios' ? 'estamento_estimado' : 'estamento')
  useEffect(() => { setDimension(categoria === 'Honorarios' ? 'estamento_estimado' : 'estamento') }, [categoria])
  if (!CATEGORIAS.includes(categoria)) return <Navigate to="/estamento/Planta" replace />
  const supportsEstimated = data.meta.estamento_estimado.categorias_cubiertas.includes(categoria)
  const effectiveDimension: DimensionEstamento = supportsEstimated ? dimension : 'estamento'
  const rows = data.panel.filter(row => row.categoria === categoria)
  const latest = rows.find(row => row.periodo === data.meta.ultimo_periodo)!
  const allSegments = (effectiveDimension === 'estamento' ? data.estamentos : data.estamentosEstimados).filter(row => row.categoria === categoria)
  const latestEstamento = allSegments.filter(row => row.periodo === latest.periodo)
  const segmentLabel = (row: (typeof allSegments)[number]) => 'estamento' in row ? row.estamento : row.estamento_estimado
  const genderRows = data.genero.filter(row => row.categoria === categoria && row.periodo === latest.periodo)
  const femenino = genderRows.reduce((s, r) => s + r.femenino, 0)
  const masculino = genderRows.reduce((s, r) => s + r.masculino, 0)
  const totalGenero = femenino + masculino + genderRows.reduce((s, r) => s + r.no_clasificado, 0)
  const resumen = data.resumen[categoria]
  const horas = data.horas.filter(row => row.categoria === categoria && row.periodo.startsWith('2025'))
  const horasTotal = horas.reduce((s, r) => s + (r.horas || 0), 0)
  const montoHoras = horas.reduce((s, r) => s + (r.monto_clp || 0), 0)
  const desvinculacion = data.desvinculacion.filter(row => row.periodo.startsWith('2025'))
  const controls = <div className="chart-controls">
    <label className="select-inline">Métrica<select data-testid="estamental-metric" value={metric} onChange={event => setMetric(event.target.value as MetricaBarra)}><option value="dotacion_registros">Dotación</option><option value="gasto_bruto_clp">Remuneración bruta</option></select></label>
    {supportsEstimated && <label className="select-inline">Clasificación<select data-testid="estamental-dimension" value={effectiveDimension} onChange={event => setDimension(event.target.value as DimensionEstamento)}><option value="estamento">Estamento publicado</option><option value="estamento_estimado">Estamento estimado</option></select></label>}
  </div>
  const estimatedLegend = effectiveDimension === 'estamento_estimado' && <div className="estimated-block"><p className="estimated-legend">{data.meta.estamento_estimado.leyenda_fija}</p><GlossaryCard entries={data.glosario} term="Estamento estimado" label="Sobre la estimación" /></div>
  return <div className="container page">
    <PageHeading eyebrow="Vista estamental" title={categoria}><p>Serie mensual, remuneraciones y campos efectivamente publicados por la fuente.</p><div className="glossary-inline"><GlossaryCard entries={data.glosario} term={categoria} /><GlossaryCard entries={data.glosario} term="Persona-mes" label="Unidad de conteo" /></div></PageHeading>
    <nav className="category-tabs" aria-label="Seleccionar categoría">{CATEGORIAS.map(item => <Link key={item} data-category={item} className={item === categoria ? 'active' : ''} style={{ '--category-color': COLORS[item] } as import('react').CSSProperties} to={`/estamento/${encodeURIComponent(item)}`}>{item}</Link>)}</nav>

    <section className="data-section"><div className="metrics-grid four">
      <Metric label={`Registros, ${periodLabel(latest.periodo)}`} value={number.format(latest.dotacion_registros)} note="persona-mes publicados" source={<SourceButton trace={latest.trazabilidad} title={`${categoria}, dotación ${latest.periodo}`} compact />} />
      <Metric label="Bruto del último mes" value={compactMoney(latest.gasto_bruto_clp)} note={`${latest.registros_bruta_no_informa} ceros canónicos`} source={<SourceButton trace={latest.trazabilidad} title={`${categoria}, bruto ${latest.periodo}`} compact />} />
      <Metric label="Horas extra, 2025" value={categoria === 'Honorarios' ? 'No publica' : decimal.format(horasTotal)} note={categoria === 'Honorarios' ? 'Ausencia declarada' : `${money.format(montoHoras)} publicados`} source={<SourceButton trace={combineTraces(horas.map(r => r.trazabilidad))} title={`${categoria}, horas extra 2025`} compact />} />
      <Metric label="Identificadores heredados" value={number.format(data.meta.conteos.trabajadores_id_por_categoria[categoria])} note="No equivalen a identidad global validada" source={<SourceButton trace={combineTraces(rows.map(r => r.trazabilidad))} title={`${categoria}, identificadores heredados 2023-2025`} compact />} />
    </div><ZeroNote count={latest.registros_bruta_no_informa} entries={data.glosario} /></section>

    <section className="data-section"><SectionHeading title="Evolución mensual por estamento" description="Barras apiladas absolutas; el tooltip informa solo el segmento bajo el cursor y su participación en la barra." action={controls} />
      <EstamentoStackedChart rows={allSegments} metric={metric} dimension={effectiveDimension} glossary={data.glosario} />
      {estimatedLegend}
      {metric === 'gasto_bruto_clp' && <ZeroNote count={allSegments.reduce((sum, row) => sum + row.registros_bruta_no_informa, 0)} entries={data.glosario} />}
      <DataDisclosure title="Datos mensuales por segmento y fuentes"><div className="table-scroll tall"><table><thead><tr><th>Período</th><th>{effectiveDimension === 'estamento' ? 'Estamento publicado' : 'Estamento estimado'}</th><th>{metric === 'dotacion_registros' ? 'Registros' : 'Bruto CLP'}</th>{metric === 'gasto_bruto_clp' && <th>No informa</th>}<th>Fuente</th></tr></thead><tbody>{allSegments.map(row => <tr key={`${row.periodo}-${segmentLabel(row)}`}><td>{row.periodo}</td><td>{segmentLabel(row)}</td><td>{metric === 'dotacion_registros' ? number.format(row.dotacion_registros) : money.format(row.gasto_bruto_clp)}</td>{metric === 'gasto_bruto_clp' && <td>{number.format(row.registros_bruta_no_informa)}</td>}<td><SourceButton trace={row.trazabilidad} title={`${segmentLabel(row)}, ${categoria}, ${row.periodo}`} compact /></td></tr>)}</tbody></table></div></DataDisclosure>
    </section>

    <section className="data-section two-columns"><div><SectionHeading title={effectiveDimension === 'estamento' ? 'Estamento publicado' : 'Estamento estimado'} description={`${metric === 'dotacion_registros' ? 'Registros' : 'Remuneración bruta'} de ${periodLabel(latest.periodo)}.`} /><SimpleBars items={latestEstamento.map(row => ({ label: segmentLabel(row), value: row[metric], color: COLORS[categoria] }))} valueLabel={metric === 'dotacion_registros' ? 'registros' : 'CLP'} formatValue={metric === 'gasto_bruto_clp' ? (value => money.format(value)) : undefined} />{estimatedLegend}<DataDisclosure title="Fuentes por estamento">{latestEstamento.map(row => <div className="source-line" key={segmentLabel(row)}><span>{segmentLabel(row)}{metric === 'gasto_bruto_clp' ? `: ${number.format(row.registros_bruta_no_informa)} No informa` : ''}</span><SourceButton trace={row.trazabilidad} title={`${segmentLabel(row)}, ${latest.periodo}`} compact /></div>)}</DataDisclosure></div>
      <div><SectionHeading title="Género agregado" /><GenderLegend text={data.meta.privacidad.leyenda} /><div className="gender-item"><div className="gender-title"><h3>{categoria}</h3><SourceButton trace={combineTraces(genderRows.map(r => r.trazabilidad))} title={`Género agregado ${categoria}, ${latest.periodo}`} compact /></div><div className="gender-bar"><span style={{ width: `${femenino / totalGenero * 100}%` }} /><span style={{ width: `${masculino / totalGenero * 100}%` }} /></div><div className="gender-values"><span>Femenino <strong>{decimal.format(femenino / totalGenero * 100)}%</strong></span><span>Masculino <strong>{decimal.format(masculino / totalGenero * 100)}%</strong></span></div></div></div></section>

    <section className="data-section two-columns"><div><SectionHeading title="Distribución de remuneraciones" description={`Rangos de bruto en ${periodLabel(latest.periodo)}.`} /><SimpleBars items={resumen.distribucion_remuneraciones.map(row => ({ label: row.rango, value: row.registros }))} /><DataDisclosure title="Fuentes por rango">{resumen.distribucion_remuneraciones.map(row => <div className="source-line" key={row.rango}><span>{row.rango}</span><SourceButton trace={row.trazabilidad} title={`${row.rango}, ${categoria}`} compact /></div>)}</DataDisclosure></div>
      <div><SectionHeading title="Antigüedad: año de inicio" description="Seis años iniciales visibles; el resto se despliega. No se imputan fechas ausentes." /><SimpleBars items={resumen.antiguedad_por_anio_inicio.slice(0, 6).map(row => ({ label: row.anio_inicio, value: row.registros }))} />{resumen.antiguedad_por_anio_inicio.length > 6 && <DataDisclosure title={`Mostrar ${resumen.antiguedad_por_anio_inicio.length - 6} años restantes`}><SimpleBars items={resumen.antiguedad_por_anio_inicio.slice(6).map(row => ({ label: row.anio_inicio, value: row.registros }))} /></DataDisclosure>}<DataDisclosure title="Fuentes por año de inicio">{resumen.antiguedad_por_anio_inicio.map(row => <div className="source-line" key={row.anio_inicio}><span>{row.anio_inicio}</span><SourceButton trace={row.trazabilidad} title={`Inicio ${row.anio_inicio}, ${categoria}`} compact /></div>)}</DataDisclosure></div></section>

    {categoria === 'Honorarios' ? <HonorariosEspecifico data={data} /> : categoria === 'Código del Trabajo' ? <section className="data-section"><SectionHeading title="Monto de desvinculación, 2025" description="Suma mensual publicada fuera de la remuneración bruta." /><div className="metrics-grid three">{desvinculacion.map(row => <Metric key={row.periodo} label={periodLabel(row.periodo)} value={compactMoney(row.monto_desvinculacion_clp)} note={`${row.registros_cero_canonico} ceros canónicos`} source={<SourceButton trace={row.trazabilidad} title={`Desvinculación ${row.periodo}`} compact />} />)}</div></section> : <HorasEspecifico data={data} categoria={categoria} />}

    <section className="data-section explorer-cta"><div><h2>Registros de {categoria}</h2><p>Abra el mismo explorador transversal con esta categoría ya aplicada. Podrá combinar período, estamento, cargo, bruto, horas y tipo de término.</p></div><Link className="button primary" to={`/explorador?categoria=${encodeURIComponent(categoria)}`}>Filtrar {categoria} <ArrowRight size={17} /></Link></section>
  </div>
}

function HorasEspecifico({ data, categoria }: { data: CommonData; categoria: Categoria }) {
  const rows = data.horas.filter(row => row.categoria === categoria && row.periodo.startsWith('2025'))
  return <section className="data-section"><SectionHeading title="Horas extra por tipo, 2025" description="Desagregación publicada por la fuente." /><div className="metrics-grid three">{['Diurnas', 'Nocturnas', 'Festivas'].map(tipo => { const subset = rows.filter(r => r.tipo === tipo); return <Metric key={tipo} label={tipo} value={decimal.format(subset.reduce((s, r) => s + (r.horas || 0), 0))} note={`${money.format(subset.reduce((s, r) => s + (r.monto_clp || 0), 0))} · ${subset.reduce((s, r) => s + (r.registros_cero_canonico || 0), 0)} ceros canónicos`} source={<SourceButton trace={combineTraces(subset.map(r => r.trazabilidad))} title={`${tipo}, ${categoria}, 2025`} compact />} /> })}</div><DataDisclosure title="Detalle mensual y fuentes"><div className="table-scroll tall"><table><thead><tr><th>Período</th><th>Tipo</th><th>Horas</th><th>Monto</th><th>Fuente</th></tr></thead><tbody>{rows.map(row => <tr key={`${row.periodo}-${row.tipo}`}><td>{row.periodo}</td><td>{row.tipo}</td><td>{decimal.format(row.horas || 0)}</td><td>{money.format(row.monto_clp || 0)}</td><td><SourceButton trace={row.trazabilidad} title={`${row.tipo}, ${row.periodo}`} compact /></td></tr>)}</tbody></table></div></DataDisclosure></section>
}
function HonorariosEspecifico({ data }: { data: CommonData }) {
  const especifico = data.resumen.Honorarios.especificos
  const estados = Object.entries(especifico.informes_estados || {})
  const ultimoMes = combineTraces(data.panel.filter(row => row.categoria === 'Honorarios' && row.periodo === data.meta.ultimo_periodo).map(row => row.trazabilidad))
  const serieCompleta = combineTraces(data.panel.filter(row => row.categoria === 'Honorarios').map(row => row.trazabilidad))
  return <section className="data-section"><SectionHeading title="Pagos e informes de funciones" description="Estado del respaldo verificado para los 9.464 registros de Honorarios." /><div className="two-columns"><div><div className="gender-title"><h3 className="chart-subtitle">Tipo de pago, último mes</h3><SourceButton trace={ultimoMes} title="Tipo de pago de Honorarios, último mes" compact /></div><SimpleBars items={(especifico.tipo_pago || []).map(row => ({ label: row.valor, value: row.registros }))} /><div className="gender-title"><h3 className="chart-subtitle spaced">Número de cuotas, último mes</h3><SourceButton trace={ultimoMes} title="Número de cuotas de Honorarios, último mes" compact /></div><SimpleBars items={(especifico.numero_cuotas || []).map(row => ({ label: row.valor, value: row.registros }))} /></div><div><div className="gender-title"><h3 className="chart-subtitle">Informes de funciones, serie completa</h3><SourceButton trace={serieCompleta} title="Estados de informes de Honorarios, 2023-2025" compact /></div><SimpleBars items={estados.map(([estado, value]) => ({ label: estadoInforme(estado), value }))} /><Notice title="Respaldo documental, no contenido republicado"><p>{especifico.nota_respaldo} El explorador muestra estado, ruta y SHA-256 por registro; no se presenta como enlace activo un archivo que no está incluido en esta distribución.</p></Notice></div></div></section>
}
