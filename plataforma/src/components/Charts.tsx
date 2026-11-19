import { useState } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { Categoria, EstamentoEstimadoRow, EstamentoRow, GlosarioEntry, PanelRow } from '../types'
import { CATEGORIAS } from '../types'
import { compactMoney, decimal, money, number, periodLabel } from '../lib/data'
import { useIsMobile } from '../hooks/use-mobile'
import { GlossaryCard } from './Glossary'

export const COLORS: Record<Categoria, string> = {
  Planta: '#123c4a',
  Contrata: '#16756f',
  'Código del Trabajo': '#bd6b2e',
  Honorarios: '#7c8794',
}
const ESTAMENTO_COLORS: Record<string, string> = {
  Directivo: '#123c4a',
  Jefatura: '#175f68',
  Profesional: '#16756f',
  Técnico: '#48a49a',
  Administrativo: '#bd6b2e',
  Auxiliar: '#dfab68',
  Alcalde: '#5e4778',
  Otro: '#7c8794',
  Honorarios: '#a2adb7',
  'No clasificable': '#d2d9dc',
}
export type MetricaBarra = 'dotacion_registros' | 'gasto_bruto_clp'
export type DimensionEstamento = 'estamento' | 'estamento_estimado'
type SegmentRow = EstamentoRow | EstamentoEstimadoRow
interface ChartPoint { periodo: string; label: string; shortLabel: string; __total: number; [key: string]: string | number }
interface TooltipItem { dataKey?: string | number; payload?: ChartPoint }

const shortPeriodLabel = (periodo: string) => `${periodLabel(periodo).slice(0, 3)} ${periodo.slice(2, 4)}`

function SegmentTooltip({ active, payload, hovered, metric }: { active?: boolean; payload?: TooltipItem[]; hovered: string; metric: MetricaBarra }) {
  const item = payload?.find(entry => String(entry.dataKey) === hovered)
  const point = item?.payload
  if (!active || !point || !hovered) return null
  const value = Number(point[hovered] || 0)
  const noInforma = Number(point[`__noInforma_${hovered}`] || 0)
  const percentage = point.__total ? value / point.__total * 100 : 0
  return <div className="segment-tooltip" data-testid="segment-tooltip" data-estamento={hovered}>
    <strong>{hovered}</strong>
    <span>Período: {point.periodo}</span>
    <span>{metric === 'gasto_bruto_clp' ? 'Remuneración bruta' : 'Dotación'}: <b>{metric === 'gasto_bruto_clp' ? money.format(value) : number.format(value)}</b></span>
    <span>{decimal.format(percentage)}% de esta barra</span>
    {metric === 'gasto_bruto_clp' && <span>Incluye {number.format(noInforma)} registro(s) «No informa»</span>}
  </div>
}

function useMobileBarAxis(metric: MetricaBarra) {
  const isMobile = useIsMobile()
  return {
    isMobile,
    height: isMobile ? 420 : 360,
    margin: isMobile ? { top: 12, right: 0, left: 0, bottom: 0 } : { top: 12, right: 8, left: 8, bottom: 0 },
    xAxis: <XAxis dataKey={isMobile ? 'shortLabel' : 'label'} interval={isMobile ? 3 : 2} tick={{ fontSize: isMobile ? 10 : 11, fill: '#4c5c61' }} tickLine={false} axisLine={{ stroke: '#aab8bb' }} angle={isMobile ? -60 : 0} textAnchor={isMobile ? 'end' : 'middle'} height={isMobile ? 88 : 30} tickMargin={8} />,
    yAxis: <YAxis tickFormatter={value => metric === 'gasto_bruto_clp' ? compactMoney(Number(value)) : number.format(Number(value))} width={isMobile ? 56 : 82} tick={{ fontSize: isMobile ? 10 : 11, fill: '#4c5c61' }} tickLine={false} axisLine={false} />,
  }
}

export function EstamentoStackedChart({ rows, metric, dimension, glossary = [] }: { rows: SegmentRow[]; metric: MetricaBarra; dimension: DimensionEstamento; glossary?: GlosarioEntry[] }) {
  const [hovered, setHovered] = useState('')
  const axis = useMobileBarAxis(metric)
  const segmentName = (row: SegmentRow) => 'estamento' in row ? row.estamento : row.estamento_estimado
  const periods = [...new Set(rows.map(row => row.periodo))].sort()
  const labels = [...new Set(rows.map(segmentName))].sort((a, b) => a.localeCompare(b, 'es'))
  const data: ChartPoint[] = periods.map(periodo => {
    const point: ChartPoint = { periodo, label: periodLabel(periodo), shortLabel: shortPeriodLabel(periodo), __total: 0 }
    for (const estamento of labels) {
      const row = rows.find(item => item.periodo === periodo && segmentName(item) === estamento)
      const value = row?.[metric] || 0
      point[estamento] = value
      point[`__noInforma_${estamento}`] = row?.registros_bruta_no_informa || 0
      point.__total += value
    }
    return point
  })
  return <div className={`chart-wrap${axis.isMobile ? ' chart-mobile' : ''}`} data-chart="monthly-estamento" aria-label={`Serie mensual apilada por ${dimension === 'estamento' ? 'estamento publicado' : 'estamento estimado'}`}>
    <ResponsiveContainer width="100%" height={axis.height}>
      <BarChart data={data} margin={axis.margin}>
        <CartesianGrid vertical={false} stroke="#dce4e5" />
        {axis.xAxis}
        {axis.yAxis}
        <Tooltip content={<SegmentTooltip hovered={hovered} metric={metric} />} cursor={{ fill: 'transparent' }} />
        {labels.map(estamento => <Bar key={estamento} dataKey={estamento} stackId="total" fill={ESTAMENTO_COLORS[estamento] || '#7c8794'} onMouseEnter={() => setHovered(estamento)} onClick={() => setHovered(estamento)} isAnimationActive={false} />)}
      </BarChart>
    </ResponsiveContainer>
    <div className="chart-legend">{labels.map(estamento => <span key={estamento}><i style={{ background: ESTAMENTO_COLORS[estamento] || '#7c8794' }} />{estamento}<GlossaryCard entries={glossary} term={estamento} /></span>)}</div>
  </div>
}

interface CategoryChartPoint { periodo: string; label: string; shortLabel: string; __total: number; [key: string]: string | number }
export function MonthlyStackedChart({ rows, metric }: { rows: PanelRow[]; metric: MetricaBarra }) {
  const [hovered, setHovered] = useState('')
  const axis = useMobileBarAxis(metric)
  const periods = [...new Set(rows.map(row => row.periodo))].sort()
  const data: CategoryChartPoint[] = periods.map(periodo => {
    const point: CategoryChartPoint = { periodo, label: periodLabel(periodo), shortLabel: shortPeriodLabel(periodo), __total: 0 }
    for (const categoria of CATEGORIAS) {
      const row = rows.find(item => item.periodo === periodo && item.categoria === categoria)
      const value = row?.[metric] || 0
      point[categoria] = value
      point[`__noInforma_${categoria}`] = row?.registros_bruta_no_informa || 0
      point.__total += value
    }
    return point
  })
  return <div className={`chart-wrap${axis.isMobile ? ' chart-mobile' : ''}`} data-chart="monthly-category" aria-label={`Serie mensual apilada de ${metric === 'dotacion_registros' ? 'dotación' : 'gasto bruto'} por categoría de vínculo`}>
    <ResponsiveContainer width="100%" height={axis.height}>
      <BarChart data={data} margin={axis.margin}>
        <CartesianGrid vertical={false} stroke="#dce4e5" />
        {axis.xAxis}
        {axis.yAxis}
        <Tooltip content={<SegmentTooltip hovered={hovered} metric={metric} />} cursor={{ fill: 'transparent' }} />
        {CATEGORIAS.map((categoria, index) => <Bar key={categoria} dataKey={categoria} stackId="total" fill={COLORS[categoria]} radius={index === CATEGORIAS.length - 1 ? [2, 2, 0, 0] : 0} onMouseEnter={() => setHovered(categoria)} onClick={() => setHovered(categoria)} isAnimationActive={false} />)}
      </BarChart>
    </ResponsiveContainer>
    <div className="chart-legend">{CATEGORIAS.map(categoria => <span key={categoria}><i style={{ background: COLORS[categoria] }} />{categoria}</span>)}</div>
  </div>
}

interface DonutTooltipItem { payload?: PanelRow & { value: number } }
function DonutTooltip({ active, payload, metric, total }: { active?: boolean; payload?: DonutTooltipItem[]; metric: MetricaBarra; total: number }) {
  const row = payload?.[0]?.payload
  if (!active || !row) return null
  return <div className="segment-tooltip" data-testid="donut-tooltip">
    <strong>{row.categoria}</strong>
    <span>{metric === 'gasto_bruto_clp' ? money.format(row.value) : number.format(row.value)}</span>
    <span>{decimal.format(total ? row.value / total * 100 : 0)}% del total</span>
    {metric === 'gasto_bruto_clp' && <span>Incluye {number.format(row.registros_bruta_no_informa)} registro(s) «No informa»</span>}
  </div>
}

export function CategoryDonut({ rows, metric, glossary }: { rows: PanelRow[]; metric: MetricaBarra; glossary: GlosarioEntry[] }) {
  const data = rows.map(row => ({ ...row, value: row[metric] }))
  const total = data.reduce((sum, row) => sum + row.value, 0)
  return <div className="category-donut" data-testid="category-donut" aria-label={`Composición por categoría de ${rows[0]?.periodo || ''}`}>
    <div className="donut-chart">
      <ResponsiveContainer width="100%" height={290}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="categoria" innerRadius="62%" outerRadius="86%" paddingAngle={2} stroke="#f8faf9" strokeWidth={2} isAnimationActive={false}>
            {data.map(row => <Cell key={row.categoria} fill={COLORS[row.categoria]} />)}
          </Pie>
          <Tooltip content={<DonutTooltip metric={metric} total={total} />} />
        </PieChart>
      </ResponsiveContainer>
      <div className="donut-total" aria-hidden="true"><strong>{metric === 'gasto_bruto_clp' ? compactMoney(total) : number.format(total)}</strong><span>{metric === 'gasto_bruto_clp' ? 'bruto total' : 'personas-mes'}</span></div>
    </div>
    <div className="donut-legend">{data.map(row => <div key={row.categoria}><i style={{ background: COLORS[row.categoria] }} /><span><strong>{row.categoria}</strong><small>{metric === 'gasto_bruto_clp' ? money.format(row.value) : number.format(row.value)} · {decimal.format(total ? row.value / total * 100 : 0)}%</small></span><GlossaryCard entries={glossary} term={row.categoria} /></div>)}</div>
  </div>
}

export function SimpleBars({ items, valueLabel = 'registros', formatValue }: { items: { label: string; value: number; color?: string }[]; valueLabel?: string; formatValue?: (value: number) => string }) {
  const max = Math.max(...items.map(item => item.value), 1)
  return <div className="simple-bars">{items.map(item => <div className="bar-row" key={item.label}>
    <div className="bar-label"><span>{item.label}</span><strong>{formatValue ? formatValue(item.value) : number.format(item.value)} <small>{valueLabel}</small></strong></div>
    <div className="bar-track" aria-hidden="true"><span style={{ width: `${Math.max(item.value / max * 100, item.value ? 2 : 0)}%`, background: item.color || '#16756f' }} /></div>
  </div>)}</div>
}
