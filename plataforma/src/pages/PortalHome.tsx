import { ArrowLeftRight, ArrowRight, BookOpenCheck, ClipboardList, Compass, Database, ExternalLink, FileSearch, Network, UsersRound, WalletCards } from 'lucide-react'
import { Link } from 'react-router'

const modules = [
  {
    title: 'Normativa y Estructura Organizacional',
    status: 'Siguiente · en desarrollo',
    icon: BookOpenCheck,
    questions: '¿Qué normas y actos regulan las potestades municipales? ¿Cómo se organizan las unidades y qué funciones se les atribuyen?',
    source: 'Actos y documentos oficiales, marco normativo, organigrama y documentos de funciones publicados por el municipio.',
    missing: 'Especificación del módulo, saneamiento y vinculación de las fuentes locales, y revisión de los manuales de funciones identificados en TP-19.',
    next: true,
  },
  {
    title: 'Información Presupuestaria',
    status: 'En desarrollo',
    icon: WalletCards,
    questions: '¿Cómo evolucionan los ingresos y los gastos? ¿Qué programas, subtítulos y partidas componen cada variación?',
    source: 'Estados Presupuestarios (ESP) y Balances de Ejecución Presupuestaria (BEP) publicados por el municipio.',
    missing: 'Ficha de especificación e integración visual del canónico presupuestario, manteniendo visibles las diferencias y los documentos en cuarentena cuando corresponda.',
  },
  {
    title: 'Transferencias de fondos',
    status: 'En desarrollo',
    icon: ArrowLeftRight,
    questions: '¿Qué fondos transfiere el municipio, a qué destinatarios y mediante qué instrumentos? ¿Qué antecedentes de rendición se publican?',
    source: 'Convenios, actos y registros de transferencias publicados en el portal municipal MU068.',
    missing: 'Inventario de fuentes, ficha de especificación, saneamiento documental y reglas de trazabilidad para convenios y rendiciones.',
  },
  {
    title: 'Trámites ante el organismo',
    status: 'En desarrollo',
    icon: ClipboardList,
    questions: '¿Qué trámites pueden realizarse ante el municipio y qué requisitos, plazos y canales se declaran para cada uno?',
    source: 'Nómina de trámites y documentos publicados por la Municipalidad de Coronel.',
    missing: 'Inventario y verificación de vigencia y enlaces, además de la ficha de especificación y las reglas para declarar información ausente.',
  },
  {
    title: 'Juntas de Vecinos · Ley 21.146',
    status: 'En desarrollo',
    icon: Network,
    questions: '¿Qué información municipal se publica sobre las juntas de vecinos y su relación con el organismo?',
    source: 'Registros y documentos municipales asociados a juntas de vecinos, en el marco de la Ley 21.146.',
    missing: 'Delimitación del alcance, inventario de fuentes, revisión de privacidad y ficha de especificación antes de construir visualizaciones.',
  },
]

export default function PortalHome() {
  return <>
    <section className="portal-hero">
      <div className="container portal-hero-grid">
        <div className="portal-hero-copy">
          <span className="overline">Municipalidad de Coronel · información pública verificable</span>
          <h1>Portal de Transparencia Trazable</h1>
          <p>Información municipal estructurada para consultar, comparar y comprobar. La fuente de origen y las decisiones de transformación permanecen visibles.</p>
          <div className="hero-actions">
            <Link className="button primary" to="/personal">Explorar Personal y Remuneraciones <ArrowRight size={17} /></Link>
            <a className="button secondary" href="https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=MU068" target="_blank" rel="noreferrer">Abrir fuente MU068 <ExternalLink size={16} /></a>
          </div>
        </div>
        <aside className="portal-compass" aria-labelledby="brujula-portal">
          <Compass size={28} aria-hidden="true" />
          <h2 id="brujula-portal">La brújula del portal</h2>
          <p><strong>Toda cifra, perseguible hasta su fuente.</strong> Archivo, fila y huella digital para reconstruir su procedencia.</p>
          <p><strong>Toda ausencia, declarada.</strong> Lo que no está publicado o no puede calcularse no se reemplaza por un cero silencioso.</p>
        </aside>
      </div>
      <div className="container portal-source-line">
        <Database size={18} aria-hidden="true" />
        <p><strong>Fuente:</strong> datos de transparencia activa del portal municipal (MU068), Ley 20.285 e IGTA.</p>
      </div>
    </section>

    <section className="container page-section" aria-labelledby="modulos-portal">
      <div className="section-heading">
        <div><h2 id="modulos-portal">Módulos y preguntas de fiscalización</h2><p>Cada módulo declara su disponibilidad, las preguntas que busca responder, la fuente prevista y el trabajo que aún falta.</p></div>
      </div>
      <div className="portal-module-grid">
        <article className="portal-module available">
          <div className="module-heading">
            <UsersRound size={25} aria-hidden="true" />
            <div><span className="module-status">Disponible</span><h3>Personal y Remuneraciones</h3></div>
          </div>
          <div className="module-facts">
            <div><h4>Preguntas que responde</h4><p>¿Cómo evolucionan la dotación y las remuneraciones? ¿Qué registros, categorías y estamentos componen cada cifra?</p></div>
            <div><h4>Fuente utilizada</h4><p>CSV mensuales de Personal y Remuneraciones publicados en MU068, con trazabilidad por archivo, fila y SHA-256.</p></div>
            <div><h4>Cobertura declarada</h4><p>Período 2023—2025. Las ausencias, las versiones alternas y los límites de cada visualización se presentan dentro del módulo.</p></div>
          </div>
          <Link className="text-link module-entry" to="/personal">Entrar al módulo <ArrowRight size={16} /></Link>
        </article>

        {modules.map(({ title, status, icon: Icon, questions, source, missing, next }) => <article className={`portal-module${next ? ' next' : ''}`} key={title}>
          <div className="module-heading">
            <Icon size={24} aria-hidden="true" />
            <div><span className="module-status">{status}</span><h3>{title}</h3></div>
          </div>
          <div className="module-placeholder-facts">
            <section><h4>Preguntas que responderá</h4><p>{questions}</p></section>
            <section><h4>Fuente prevista</h4><p>{source}</p></section>
            <section><h4>Qué falta</h4><p>{missing}</p></section>
          </div>
        </article>)}
      </div>
    </section>

    <section className="container page-section portal-principles" aria-labelledby="como-leer">
      <div className="section-heading"><div><h2 id="como-leer">Cómo leer esta plataforma</h2><p>Producto, fuente y método se presentan como elementos distintos y comprobables.</p></div></div>
      <div className="portal-principle-grid">
        <article><FileSearch size={22} aria-hidden="true" /><h3>La fuente sigue abierta</h3><p>El portal municipal es el origen de los datos. Esta plataforma los estructura y enlaza para facilitar su revisión, sin sustituir los documentos oficiales.</p></article>
        <article><Database size={22} aria-hidden="true" /><h3>Los datos se pueden reutilizar</h3><p>Los módulos disponibles ofrecen datos estructurados y exportaciones con sus columnas de trazabilidad. La metodología documenta las transformaciones.</p></article>
        <article><Compass size={22} aria-hidden="true" /><h3>Los límites son parte del resultado</h3><p>Una ausencia, una discrepancia o una comparación no calculable se muestran como tales. Ningún módulo futuro se presenta como si ya estuviera disponible.</p></article>
      </div>
      <div className="portal-method-link"><Link className="button secondary" to="/metodologia">Revisar metodología y fuentes de Personal <ArrowRight size={16} /></Link></div>
    </section>
  </>
}
