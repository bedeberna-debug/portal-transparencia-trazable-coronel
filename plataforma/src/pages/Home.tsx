import { ArrowRight, BookOpen, FileCheck2, Search, ShieldAlert, UsersRound } from 'lucide-react'
import { Link } from 'react-router'
import type { CommonData } from '../types'
import { combineTraces, decimal, money, number, periodLabel } from '../lib/data'
import { DataDisclosure, GenderLegend, Metric, Notice, PageHeading, SectionHeading, ZeroNote } from '../components/Common'
import { GlossaryCard } from '../components/Glossary'
import { SourceButton } from '../components/Source'

export default function Home({ data }: { data: CommonData }) {
  const latest = data.panel.filter(row => row.periodo === data.meta.ultimo_periodo)
  const latestHours = data.horas.filter(row => row.periodo === data.meta.ultimo_periodo && row.estado === 'publicado')
  const dotacion = latest.reduce((sum, row) => sum + row.dotacion_registros, 0)
  const bruto = latest.reduce((sum, row) => sum + row.gasto_bruto_clp, 0)
  const noInforma = latest.reduce((sum, row) => sum + row.registros_bruta_no_informa, 0)
  const horas = latestHours.reduce((sum, row) => sum + (row.horas || 0), 0)
  const traces = combineTraces(latest.map(row => row.trazabilidad))
  const hourTraces = combineTraces(latestHours.map(row => row.trazabilidad))
  return <>
    <section className="home-hero"><div className="container">
      <PageHeading eyebrow="Transparencia que se puede comprobar" title="Personas, contratos y remuneraciones, mes a mes.">
        <p>Explore 22.940 registros públicos de dotación funcionaria entre enero de 2023 y diciembre de 2025. Cada cifra conserva el archivo, la fila y la huella digital que la respalda.</p>
      </PageHeading>
      <div className="hero-actions"><Link className="button primary" to="/panel">Ver evolución institucional <ArrowRight size={17} /></Link><Link className="button secondary" to="/explorador"><Search size={17} /> Explorar registros</Link></div>
      <div className="hero-proof"><FileCheck2 size={20} /><span><strong>{data.meta.validacion_agregados.aprobadas} controles aprobados</strong> contra la validación final del canónico v1.0.0</span></div>
    </div></section>

    <section className="container page-section" aria-labelledby="titulares">
      <SectionHeading title={`La institución en ${periodLabel(data.meta.ultimo_periodo)}`} description="Dotación medida como registros persona-mes publicados; no como nómina única deduplicada." />
      <GlossaryCard entries={data.glosario} term="Persona-mes" label="Cómo contamos la dotación" />
      <div className="metrics-grid three" id="titulares">
        <Metric label="Dotación publicada" value={number.format(dotacion)} note="registros persona-mes" source={<SourceButton trace={traces} title={`Dotación total, ${data.meta.ultimo_periodo}`} compact />} />
        <Metric label="Gasto bruto del mes" value={money.format(bruto)} note={`${noInforma} registros con 0 canónico`} source={<SourceButton trace={traces} title={`Gasto bruto, ${data.meta.ultimo_periodo}`} compact />} />
        <Metric label="Horas extra publicadas" value={decimal.format(horas)} note="Planta, Contrata y Código del Trabajo" source={<SourceButton trace={hourTraces} title={`Horas extra, ${data.meta.ultimo_periodo}`} compact />} />
      </div>
      <ZeroNote count={noInforma} entries={data.glosario} />
      <DataDisclosure title="Ver el último mes por categoría y fuente"><div className="table-scroll"><table><thead><tr><th>Categoría</th><th>Registros</th><th>Bruto CLP</th><th>No informa</th><th>Fuente</th></tr></thead><tbody>{latest.map(row => <tr key={row.categoria}><td><span className="term-with-definition">{row.categoria}<GlossaryCard entries={data.glosario} term={row.categoria} /></span></td><td>{number.format(row.dotacion_registros)}</td><td>{money.format(row.gasto_bruto_clp)}</td><td>{row.registros_bruta_no_informa}</td><td><SourceButton trace={row.trazabilidad} title={`${row.categoria}, ${row.periodo}`} compact /></td></tr>)}</tbody></table></div></DataDisclosure>
    </section>

    <section className="container page-section" aria-labelledby="confianza">
      <SectionHeading title="Qué está viendo y por qué puede fiscalizarlo" />
      <div className="editorial-grid" id="confianza">
        <article><span className="section-number">01</span><h3>Obligación y origen</h3><p>Información publicada bajo los artículos 34 y 36 de la Ley 18.575 y la IGTA, Resolución Exenta N.° 80/2026. Proviene del portal municipal de transparencia: 168 archivos mensuales inventariados, 144 correspondientes a estas cuatro categorías.</p><Link className="text-link" to="/metodologia">Revisar inventario y método <ArrowRight size={15} /></Link></article>
        <article><span className="section-number">02</span><h3>Unificación sin borrar discrepancias</h3><p>Los CSV se unificaron en un esquema común, conservaron sus valores originales y recibieron trazabilidad SHA-256 por fila. Las diferencias de período se resolvieron por el contenido, no por el nombre del archivo.</p><Link className="text-link" to="/metodologia">Conocer los 12 pasos <ArrowRight size={15} /></Link></article>
        <article><span className="section-number">03</span><h3>Ausencias visibles</h3><p>Honorarios no publica horas extra; Código del Trabajo no las desagrega. No hay unidad departamental y autoridades electas queda fuera. Ninguna de estas ausencias se reemplaza por ceros o estimaciones.</p><Link className="text-link" to="/metodologia">Ver todas las ausencias <ArrowRight size={15} /></Link></article>
      </div>
    </section>

    <section className="container page-section split-section">
      <div><SectionHeading title="Privacidad por diseño" /><GenderLegend text={data.meta.privacidad.leyenda} /><p>El género nunca se incluye en las fichas, los registros individuales descargables ni como filtro. La trayectoria individual se habilitó tras aplicar D-15 y obtener cero colisiones en su proyección.</p><GlossaryCard entries={data.glosario} term="Trayectoria (convención D-15)" label="Cómo se construye una trayectoria" /><Link className="text-link" to="/ficha/PLT-2023-0032"><ShieldAlert size={15} /> Ver una trayectoria con versión alterna</Link></div>
      <Notice title="Fichas habilitadas, agregados intactos"><p>D-15 selecciona una publicación por persona y período solo para la trayectoria. Las dos versiones alternas siguen visibles y los agregados conservan las 22.940 filas; la suma de fichas no reconcilia con ellos.</p></Notice>
    </section>

    <section className="container page-section"><SectionHeading title="Cuatro formas de entrar a los datos" description="Cada acceso abre una forma distinta de fiscalizar la misma fuente trazable." /><div className="navigation-cards">
      <Link className="tone-panel" to="/panel"><FileCheck2 /><strong>Panel general</strong><span>Composición, indicadores y evolución mensual.</span><ArrowRight size={18} /></Link>
      <Link className="tone-explorer" to="/explorador"><Search /><strong>Explorador transversal</strong><span>Filtros combinables y exportación CSV trazable.</span><ArrowRight size={18} /></Link>
      <Link className="tone-estamental" to="/estamento/Planta"><UsersRound /><strong>Vistas estamentales</strong><span>Evolución y gasto dentro de cada vínculo.</span><ArrowRight size={18} /></Link>
      <Link className="tone-method" to="/metodologia"><BookOpen /><strong>Metodología</strong><span>Fuentes, ausencias, controles y reutilización.</span><ArrowRight size={18} /></Link>
    </div></section>
  </>
}
