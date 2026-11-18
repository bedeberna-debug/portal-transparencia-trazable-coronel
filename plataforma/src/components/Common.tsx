import type { ReactNode } from 'react'
import { AlertTriangle, Info } from 'lucide-react'
import type { GlosarioEntry } from '../types'
import { number } from '../lib/data'
import { GlossaryCard } from './Glossary'

export function PageHeading({ eyebrow, title, children, actions }: { eyebrow?: string; title: string; children: ReactNode; actions?: ReactNode }) {
  return <div className="page-heading"><div>{eyebrow && <span className="overline">{eyebrow}</span>}<h1>{title}</h1><div className="page-lead">{children}</div></div>{actions && <div className="page-actions">{actions}</div>}</div>
}
export function SectionHeading({ title, description, action }: { title: string; description?: string; action?: ReactNode }) {
  return <div className="section-heading"><div><h2>{title}</h2>{description && <p>{description}</p>}</div>{action}</div>
}
export function Metric({ label, value, note, source }: { label: ReactNode; value: string; note?: ReactNode; source?: ReactNode }) {
  return <article className="metric"><span className="metric-label">{label}</span><strong className="metric-value">{value}</strong>{note && <span className="metric-note">{note}</span>}{source && <div className="metric-source">{source}</div>}</article>
}
export function Notice({ title, children, tone = 'info' }: { title: string; children: ReactNode; tone?: 'info' | 'warning' }) {
  return <div className={`notice ${tone}`} role={tone === 'warning' ? 'alert' : 'note'}>{tone === 'warning' ? <AlertTriangle size={21} /> : <Info size={21} />}<div><strong>{title}</strong><div>{children}</div></div></div>
}
export function ZeroNote({ count, subject = 'remuneración bruta', entries = [] }: { count: number; subject?: string; entries?: GlosarioEntry[] }) {
  return <div className="zero-explanation"><p className="zero-note">La suma incluye <strong>{number.format(count)}</strong> registro(s) con 0 canónico en {subject}, equivalente a «No informa / No tiene» en la fuente. No se interpreta como cero real.</p><GlossaryCard entries={entries} term="No informa / No tiene" label="Qué significa «No informa»" /></div>
}
export function GenderLegend({ text }: { text: string }) {
  return <p className="gender-legend"><Info size={16} />{text}</p>
}
export function DataDisclosure({ title = 'Ver datos y fuentes', children }: { title?: string; children: ReactNode }) {
  return <details className="data-disclosure"><summary>{title}</summary><div className="disclosure-content">{children}</div></details>
}
export function Loading({ label = 'Cargando datos verificados…' }) {
  return <div className="loading" role="status"><span className="loading-line" /><p>{label}</p></div>
}
export function ErrorState({ message, retry }: { message: string; retry?: () => void }) {
  return <div className="container page"><Notice title="No fue posible cargar la vista" tone="warning"><p>{message}</p>{retry && <button className="button secondary" onClick={retry}>Reintentar</button>}</Notice></div>
}
