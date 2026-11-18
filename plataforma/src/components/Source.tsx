import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from 'react'
import { Database, ExternalLink, FileSpreadsheet, X } from 'lucide-react'
import type { Trazabilidad } from '../types'
import { publicUrl } from '../lib/data'
import { rowRanges } from '../lib/format'

interface SourceState { trace: Trazabilidad; title: string }
const SourceContext = createContext<{ open: (trace: Trazabilidad, title: string) => void }>({ open: () => undefined })
export const useSource = () => useContext(SourceContext)

export function SourceProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<SourceState | null>(null)
  const dialog = useRef<HTMLDialogElement>(null)
  useEffect(() => {
    const element = dialog.current
    if (!element) return
    if (state && !element.open) element.showModal()
    if (!state && element.open) element.close()
  }, [state])
  return <SourceContext.Provider value={{ open: (trace, title) => setState({ trace, title }) }}>
    {children}
    <dialog ref={dialog} className="source-dialog" aria-labelledby="source-title" onCancel={() => setState(null)} onClick={event => { if (event.target === event.currentTarget) setState(null) }}>
      {state && <div className="source-dialog-inner">
        <div className="dialog-heading">
          <div><span className="overline">Trazabilidad verificable</span><h2 id="source-title">{state.title}</h2></div>
          <button className="icon-button" aria-label="Cerrar fuente" onClick={() => setState(null)}><X size={20} /></button>
        </div>
        <p className="source-intro">Estas son las filas exactas que componen la cifra. El SHA-256 identifica los bytes del CSV fuente; el número de fila incluye el encabezado como fila 1.</p>
        <div className="source-list">
          {state.trace.fuentes.map(fuente => <article className="source-file" key={`${fuente.ruta_relativa}-${fuente.sha256}`}>
            <div className="source-file-title"><FileSpreadsheet size={19} /><h3>{fuente.archivo}</h3></div>
            <dl className="source-facts">
              <div><dt>Período(s) del contenido</dt><dd>{fuente.periodos.join(', ')}</dd></div>
              <div><dt>Filas CSV</dt><dd className="break-anywhere">{rowRanges(fuente.filas_csv)}</dd></div>
              <div><dt>Registros</dt><dd>{fuente.registros}</dd></div>
              <div><dt>SHA-256</dt><dd className="hash break-anywhere">{fuente.sha256}</dd></div>
              <div><dt>Ruta original</dt><dd className="break-anywhere">{fuente.ruta_relativa}</dd></div>
            </dl>
            <div className="source-actions">
              {fuente.url_respaldo && <a className="text-link" href={publicUrl(fuente.url_respaldo)} target="_blank" rel="noreferrer">Abrir CSV fuente <ExternalLink size={14} /></a>}
              <a className="text-link" href={state.trace.portal_oficial} target="_blank" rel="noreferrer">Portal oficial MU068 <ExternalLink size={14} /></a>
            </div>
          </article>)}
        </div>
        {!state.trace.fuentes.length && <p>No hay archivos asociados a esta selección.</p>}
      </div>}
    </dialog>
  </SourceContext.Provider>
}

export function SourceButton({ trace, title, compact = false }: { trace: Trazabilidad; title: string; compact?: boolean }) {
  const { open } = useSource()
  return <button className={compact ? 'source-button compact' : 'source-button'} onClick={() => open(trace, title)} aria-label={`¿De dónde sale este dato? ${title}`}>
    <Database size={15} /><span>{compact ? 'Fuente' : '¿De dónde sale este dato?'}</span>
  </button>
}
