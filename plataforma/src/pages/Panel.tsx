import { useEffect, useMemo, useState } from 'react'
import type { Categoria, CommonData } from '../types'
import { CATEGORIAS } from '../types'
import { combineTraces, compactMoney, decimal, money, number, periodLabel } from '../lib/data'
import { CategoryDonut, MonthlyStackedChart } from '../components/Charts'
import type { DimensionEstamento, MetricaBarra } from '../components/Charts'
import { DataDisclosure, GenderLegend, Metric, Notice, PageHeading, SectionHeading, ZeroNote } from '../components/Common'
import { GlossaryCard } from '../components/Glossary'
import { SourceButton } from '../components/Source'

const statisticMoney = (value: number | null) => value === null ? 'Sin datos' : money.format(value)

export default function Panel({ data }: { data: CommonData }) {
  const [year, setYear] = useState(2025)
  const [selectedPeriod, setSelectedPeriod] = useState(data.meta.ultimo_periodo)
  const [metric, setMetric] = useState<MetricaBarra>('dotacion_registros')
  const [category, setCategory] = useState<Categoria>('Planta')
  const [dimension, setDimension] = useState<DimensionEstamento>('estamento')
  const [hoursMode, setHoursMode] = useState<'mes' | 'anio'>('mes')
  const [hoursPeriod, setHoursPeriod] = useState(data.meta.ultimo_periodo)
  useEffect(() => { setDimension(category === 'Honorarios' ? 'estamento_estimado' : 'estamento') }, [category])

  const periods = [...new Set(data.panel.map(row => row.periodo))].sort()
  const selected = data.panel.filter(row => row.periodo === selectedPeriod)
  const supportsEstimated = data.meta.estamento_estimado.categorias_cubiertas.includes(category)
  const effectiveDimension: DimensionEstamento = supportsEstimated ? dimension : 'estamento'
  const selectedSegments = (effectiveDimension === 'estamento' ? data.estamentos : data.estamentosEstimados)
    .filter(row => row.periodo === selectedPeriod && row.categoria === category)
  const segmentLabel = (row: (typeof selectedSegments)[number]) => 'estamento' in row ? row.estamento : row.estamento_estimado
  const noInformaSegmentos = selectedSegments.reduce((sum, row) => sum + row.registros_bruta_no_informa, 0)
  const selectedGender = useMemo(() => CATEGORIAS.map(categoria => {
    const rows = data.genero.filter(row => row.periodo === selectedPeriod && row.categoria === categoria)
    return { categoria, femenino: rows.reduce((s, r) => s + r.femenino, 0), masculino: rows.reduce((s, r) => s + r.masculino, 0), registros: rows.reduce((s, r) => s + r.registros, 0), trace: combineTraces(rows.map(r => r.trazabilidad)) }
  }), [data.genero, selectedPeriod])
  const yearHours = data.horas.filter(row => row.periodo.startsWith(String(year)))
  const summaryHours = hoursMode === 'mes' ? data.horas.filter(row => row.periodo === hoursPeriod) : yearHours
  const hoursByCategory = CATEGORIAS.map(categoria => {
    const rows = summaryHours.filter(row => row.categoria === categoria)
    return { categoria, rows, horas: rows.reduce((s, r) => s + (r.horas || 0), 0), monto: rows.reduce((s, r) => s + (r.monto_clp || 0), 0), ceros: rows.reduce((s, r) => s + (r.registros_cero_canonico || 0), 0), trace: combineTraces(rows.map(r => r.trazabilidad)) }
  })
  const hoursScope = hoursMode === 'mes' ? hoursPeriod : String(year)
  const hoursTitle = hoursMode === 'mes' ? periodLabel(hoursPeriod) : String(year)
  const detailHours = hoursMode === 'mes' ? summaryHours : yearHours

  const compositionControls = <div className="chart-controls">
    <label className="select-inline">Mes<select data-testid="panel-period" value={selectedPeriod} onChange={event => setSelectedPeriod(event.target.value)}>{periods.map(periodo => <option key={periodo} value={periodo}>{periodLabel(periodo)}</option>)}</select></label>
    <label className="select-inline">Métrica<select data-testid="panel-metric" value={metric} onChange={event => setMetric(event.target.value as MetricaBarra)}><option value="dotacion_registros">Dotación</option><option value="gasto_bruto_clp">Remuneración bruta</option></select></label>
  </div>
  const comparisonControls = <div className="chart-controls">
    <label className="select-inline">Categoría<select data-testid="panel-category" value={category} onChange={event => setCategory(event.target.value as Categoria)}>{CATEGORIAS.map(categoria => <option key={categoria}>{categoria}</option>)}</select></label>
    {supportsEstimated && <label className="select-inline">Clasificación<select data-testid="panel-dimension" value={effectiveDimension} onChange={event => setDimension(event.target.value as DimensionEstamento)}><option value="estamento">Estamento publicado</option><option value="estamento_estimado">Estamento estimado</option></select></label>}
  </div>
  const hoursControls = <div className="chart-controls">
    <label className="select-inline">Resumen<select data-testid="hours-mode" value={hoursMode} onChange={event => setHoursMode(event.target.value as 'mes' | 'anio')}><option value="mes">Mes</option><option value="anio">Año</option></select></label>
    {hoursMode === 'mes' ? <label className="select-inline">Mes<select data-testid="hours-period" value={hoursPeriod} onChange={event => { setHoursPeriod(event.target.value); setYear(Number(event.target.value.slice(0, 4))) }}>{periods.map(periodo => <option key={periodo} value={periodo}>{periodLabel(periodo)}</option>)}</select></label> : <label className="select-inline">Año<select data-testid="hours-year" aria-label="Año de horas extra" value={year} onChange={event => setYear(Number(event.target.value))}><option value={2023}>2023</option><option value={2024}>2024</option><option value={2025}>2025</option></select></label>}
  </div>

  return <div className="container page">
    <PageHeading eyebrow="Panel general" title="La dotación completa, sin silos estamentales"><p>Compare 36 meses de registros persona-mes y gasto publicado. Las dos colisiones documentadas permanecen incluidas; por eso la dotación no se presenta como un conteo de personas únicas.</p><GlossaryCard entries={data.glosario} term="Persona-mes" label="Qué es una persona-mes" /></PageHeading>

    <section className="data-section" aria-labelledby="composicion-categoria"><SectionHeading title="Composición por categoría de vínculo" description={`Dona de ${periodLabel(selectedPeriod)} y serie histórica apilada de 36 meses. La métrica seleccionada controla ambas visualizaciones.`} action={compositionControls} />
      <div className="category-composition" id="composicion-categoria"><CategoryDonut rows={selected} metric={metric} glossary={data.glosario} /><MonthlyStackedChart rows={data.panel} metric={metric} /></div>
      {metric === 'gasto_bruto_clp' && <ZeroNote count={selected.reduce((sum, row) => sum + row.registros_bruta_no_informa, 0)} entries={data.glosario} />}
      <DataDisclosure title="Datos y fuentes de la serie por categoría"><div className="table-scroll tall"><table><thead><tr><th>Período</th><th>Categoría</th><th>Dotación</th><th>Bruto CLP</th><th>No informa</th><th>Fuente</th></tr></thead><tbody>{data.panel.map(row => <tr key={`${row.periodo}-${row.categoria}`}><td>{row.periodo}</td><td>{row.categoria}</td><td>{number.format(row.dotacion_registros)}</td><td>{money.format(row.gasto_bruto_clp)}</td><td>{number.format(row.registros_bruta_no_informa)}</td><td><SourceButton trace={row.trazabilidad} title={`${row.categoria}, ${row.periodo}`} compact /></td></tr>)}</tbody></table></div></DataDisclosure>
    </section>

    <section className="data-section" aria-labelledby="indicadores-categoria"><SectionHeading title={`Indicadores por categoría · ${periodLabel(selectedPeriod)}`} description="Promedio y mediana consideran solo remuneraciones brutas informadas; los ceros canónicos se declaran y se excluyen de ambos cálculos." />
      <div className="category-indicators" id="indicadores-categoria">{selected.map(row => <article className="category-indicator" data-testid={`indicator-${row.categoria}`} key={row.categoria}>
        <div className="category-indicator-title"><h3>{row.categoria}</h3><GlossaryCard entries={data.glosario} term={row.categoria} /></div>
        <dl><div><dt>Dotación</dt><dd>{number.format(row.dotacion_registros)}</dd></div><div><dt>Gasto bruto</dt><dd>{compactMoney(row.gasto_bruto_clp)}</dd></div><div><dt>Promedio de bruta</dt><dd>{statisticMoney(row.promedio_bruto_clp)}</dd></div><div><dt>Mediana de bruta</dt><dd>{statisticMoney(row.mediana_bruta_clp)}</dd></div></dl>
        <p><strong>{number.format(row.registros_bruta_no_informa)}</strong> registro(s) «No informa» · {number.format(row.registros_bruta_informada)} con bruta informada.</p>
        <SourceButton trace={row.trazabilidad} title={`Indicadores ${row.categoria}, ${selectedPeriod}`} compact />
      </article>)}</div>
      <ZeroNote count={selected.reduce((sum, row) => sum + row.registros_bruta_no_informa, 0)} entries={data.glosario} />
    </section>

    <section className="data-section" aria-labelledby="comparativa-estamental"><SectionHeading title={`Comparativa estamental dentro de ${category}`} description={`Gasto total, promedio y mediana de bruta en ${periodLabel(selectedPeriod)}. No se mezclan categorías de vínculo en una barra general.`} action={comparisonControls} />
      <div className="glossary-inline" id="comparativa-estamental"><GlossaryCard entries={data.glosario} term="Estamento" label="Qué es el estamento" />{effectiveDimension === 'estamento_estimado' && <GlossaryCard entries={data.glosario} term="Estamento estimado" label="Sobre la estimación" />}</div>
      {effectiveDimension === 'estamento_estimado' && <><p className="estimated-legend">{data.meta.estamento_estimado.leyenda_fija}</p><Notice title={category === 'Honorarios' ? 'En Honorarios el estamento es estimado' : 'Cobertura parcial de la dimensión estimada'}><p>{category === 'Honorarios' ? 'La comparación seleccionada clasifica el cargo publicado conforme a D-17; no corresponde a una clasificación oficial del municipio.' : 'Esta selección comprende únicamente Código del Trabajo y Honorarios. No reclasifica a Planta o Contrata.'}</p></Notice></>}
      <div className="table-scroll estamento-stats"><table><thead><tr><th>{effectiveDimension === 'estamento' ? 'Estamento publicado' : 'Estamento estimado'}</th><th>Gasto total</th><th>Promedio bruto</th><th>Mediana bruta</th><th>Bruta informada</th><th>No informa</th><th>Fuente</th></tr></thead><tbody>{selectedSegments.map(row => <tr key={segmentLabel(row)}><td><span className="term-with-definition">{segmentLabel(row)}<GlossaryCard entries={data.glosario} term={segmentLabel(row)} /></span></td><td>{money.format(row.gasto_bruto_clp)}</td><td>{statisticMoney(row.promedio_bruto_clp)}</td><td>{statisticMoney(row.mediana_bruta_clp)}</td><td>{number.format(row.registros_bruta_informada)}</td><td>{number.format(row.registros_bruta_no_informa)}</td><td><SourceButton trace={row.trazabilidad} title={`${segmentLabel(row)}, ${category}, ${selectedPeriod}`} compact /></td></tr>)}</tbody></table></div>
      <ZeroNote count={noInformaSegmentos} entries={data.glosario} />
    </section>

    <section className="data-section"><SectionHeading title="Composición por género agregada" description={`Porcentaje de registros de ${periodLabel(selectedPeriod)}; no representa autoidentificación ni nómina única.`} /><GenderLegend text={data.meta.privacidad.leyenda} />
      <div className="gender-grid">{selectedGender.map(row => <article className="gender-item" key={row.categoria}><div className="gender-title"><h3>{row.categoria}</h3><GlossaryCard entries={data.glosario} term={row.categoria} /><SourceButton trace={row.trace} title={`Género agregado ${row.categoria}, ${selectedPeriod}`} compact /></div><div className="gender-bar" aria-label={`${decimal.format(row.femenino / row.registros * 100)}% femenino, ${decimal.format(row.masculino / row.registros * 100)}% masculino`}><span style={{ width: `${row.femenino / row.registros * 100}%` }} /><span style={{ width: `${row.masculino / row.registros * 100}%` }} /></div><div className="gender-values"><span>Femenino <strong>{decimal.format(row.femenino / row.registros * 100)}%</strong></span><span>Masculino <strong>{decimal.format(row.masculino / row.registros * 100)}%</strong></span></div><small>{number.format(row.registros)} registros agregados</small></article>)}</div>
    </section>

    <section className="data-section" data-testid="hours-summary"><SectionHeading title={`Horas extra del sistema · ${hoursTitle}`} description="Consulte totales del último mes cargado, cambie de mes o vuelva al resumen anual. La tabla conserva horas, montos, ceros canónicos y fuentes." action={hoursControls} />
      <div className="metrics-grid four">{hoursByCategory.map(item => <Metric key={item.categoria} label={item.categoria} value={item.categoria === 'Honorarios' ? 'No publica' : compactMoney(item.monto)} note={item.categoria === 'Honorarios' ? 'Ausencia de la fuente' : `${decimal.format(item.horas)} horas · ${item.ceros} ceros canónicos`} source={<SourceButton trace={item.trace} title={`Horas extra ${item.categoria}, ${hoursScope}`} compact />} />)}</div>
      <Notice title="La comparación tiene distinta granularidad"><p>Planta y Contrata distinguen horas diurnas, nocturnas y festivas. Código del Trabajo publica un total sin desagregar. Honorarios no publica horas extra.</p></Notice>
      <DataDisclosure title={hoursMode === 'mes' ? `Detalle del mes y fuentes, ${hoursTitle}` : `Detalle mensual y fuentes, ${year}`}><div className="table-scroll tall"><table><thead><tr><th>Período</th><th>Categoría</th><th>Tipo</th><th>Horas</th><th>Monto CLP</th><th>0 canónico</th><th>Fuente</th></tr></thead><tbody>{detailHours.map(row => <tr key={`${row.periodo}-${row.categoria}-${row.tipo}`}><td>{row.periodo}</td><td>{row.categoria}</td><td>{row.tipo}</td><td>{row.horas === null ? 'No publica' : decimal.format(row.horas)}</td><td>{row.monto_clp === null ? 'No publica' : money.format(row.monto_clp)}</td><td>{row.registros_cero_canonico ?? 'No aplica'}</td><td><SourceButton trace={row.trazabilidad} title={`Horas ${row.tipo}, ${row.categoria}, ${row.periodo}`} compact /></td></tr>)}</tbody></table></div></DataDisclosure>
    </section>
  </div>
}
