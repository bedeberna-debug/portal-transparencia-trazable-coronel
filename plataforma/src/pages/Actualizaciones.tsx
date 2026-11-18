import { ArrowRight, Clock3, Compass } from 'lucide-react'
import { Link } from 'react-router'

const updates = [
  {
    version: 'v0.1',
    label: 'Primera versión',
    date: '2026-11-18',
    dateLabel: '18 de noviembre de 2026',
    summary: 'Primera versión del portal. Incluye un módulo disponible y presenta de forma abierta qué se está construyendo y qué falta.',
    changes: [
      'Se habilitó Personal y Remuneraciones: evolución mensual de dotación y gasto, filtros sobre 22.940 registros públicos, vistas por categoría y fichas individuales con trayectoria y versiones alternas.',
      'Cada cifra clave ofrece su fuente: archivo mensual, fila y huella digital. También se pueden exportar subconjuntos y verificar los CSV públicos del municipio.',
      'Se publicaron 1.068 trayectorias individuales. Las versiones alternas quedaron visibles y los agregados conservan las 22.940 filas, sin sobrescribir discrepancias.',
      'Las asignaciones especiales se muestran con códigos y nombres descifrados, conservando el texto original cuando corresponde y declarando los casos que no pueden interpretarse.',
      'La portada presenta Personal como disponible y cinco módulos en desarrollo. Cada módulo declara qué preguntas responderá, qué fuente usará y qué trabajo falta.',
      'Se aplicó el Tema Coronel y una navegación consistente para escritorio y móvil, con acceso Inicio dentro del módulo.',
      'Antes de publicarse, las cifras agregadas pasaron 77 controles y la interfaz superó 132 pruebas automáticas de navegación, contraste, responsive e integridad del paquete.',
    ],
    modules: ['Personal y Remuneraciones', 'Portada y navegación', 'Presentación de módulos'],
  },
]

export default function Actualizaciones() {
  return <>
    <section className="updates-hero">
      <div className="container updates-hero-copy">
        <span className="overline">Qué cambió y cuándo</span>
        <h1>Actualizaciones de la plataforma</h1>
        <p>Registro público de las versiones del Portal de Transparencia Trazable. Las entradas resumen cambios sustantivos en lenguaje ciudadano, indican qué módulos afectan y no exponen rutas internas de trabajo.</p>
      </div>
    </section>

    <section className="container page-section updates-page" aria-labelledby="registro-actualizaciones">
      <div className="section-heading">
        <div><h2 id="registro-actualizaciones">Versiones publicadas</h2><p>Orden cronológico inverso: primero aparece la versión más reciente.</p></div>
      </div>

      <ol className="updates-timeline">
        {updates.map(update => <li key={update.version}>
          <article className="update-entry">
            <header>
              <div className="update-title"><span className="update-version">{update.version}</span><h3>{update.label}</h3></div>
              <time dateTime={update.date}><Clock3 size={15} aria-hidden="true" />{update.dateLabel}</time>
            </header>
            <p className="update-summary">{update.summary}</p>
            <div className="update-details">
              <section aria-labelledby={`cambios-${update.version}`}>
                <h4 id={`cambios-${update.version}`}>Qué cambió</h4>
                <ul>{update.changes.map(change => <li key={change}>{change}</li>)}</ul>
              </section>
              <section aria-labelledby={`modulos-${update.version}`}>
                <h4 id={`modulos-${update.version}`}>Módulos afectados</h4>
                <div className="update-modules">{update.modules.map(module => <span key={module}>{module}</span>)}</div>
              </section>
            </div>
          </article>
        </li>)}
      </ol>

      <div className="updates-method-link">
        <p><Compass size={17} aria-hidden="true" /> Las actualizaciones describen el producto; el origen y la metodología de los datos se mantienen en las vistas correspondientes.</p>
        <Link className="button secondary" to="/metodologia">Revisar metodología y fuentes de Personal <ArrowRight size={16} /></Link>
      </div>
    </section>
  </>
}
