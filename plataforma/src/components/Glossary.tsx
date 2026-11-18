import { BookOpen } from 'lucide-react'
import type { GlosarioEntry } from '../types'
import { publicUrl } from '../lib/data'

export function GlossaryCard({ entries, term, label }: { entries: GlosarioEntry[]; term: string; label?: string }) {
  const entry = entries.find(item => item.termino === term)
  if (!entry) return null
  return <details className={`glossary-card${label ? ' with-label' : ' icon-only'}`} data-term={term}>
    <summary aria-label={`Definición de ${term}`}><span className="glossary-symbol" aria-hidden="true">¡</span>{label && <span className="glossary-label">{label}</span>}</summary>
    <div className="glossary-content">
      <strong>{entry.termino}</strong>
      <p>{entry.definicion}</p>
      <p className="glossary-source"><strong>Fuente:</strong> {entry.fuente}</p>
      <div className="glossary-links">
        <a href={publicUrl('docs/GLOSARIO_DEFINICIONES_v1.md')} target="_blank" rel="noreferrer">Glosario canónico</a>
        {entry.modulo_normativo && <span className="module-placeholder" aria-label="Marco normativo: módulo en desarrollo"><BookOpen size={14} /> Marco normativo · módulo en desarrollo</span>}
      </div>
    </div>
  </details>
}
