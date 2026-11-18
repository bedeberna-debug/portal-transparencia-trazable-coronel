import { Check, Download, ExternalLink, FileText } from 'lucide-react'
import type { CommonData } from '../types'
import { CATEGORIAS } from '../types'
import { combineTraces, number, publicUrl } from '../lib/data'
import { SourceButton } from '../components/Source'
import { DataDisclosure, Notice, PageHeading, SectionHeading } from '../components/Common'

const steps = [
  'Congelar fuentes e inventariar ruta, filas, esquema, codificación y SHA-256.',
  'Comparar nombre de archivo y período del contenido; registrar anomalías sin renombrar.',
  'Perfilar columnas, vacíos, tipos, catálogos y formatos monetarios/horarios.',
  'Definir clave de cruce y ocurrencia; no deduplicar solo por persona-período.',
  'Contrastar filas por mes y totales por columna contra el maestro anterior.',
  'Restaurar campos en archivos nuevos; nunca sobrescribir el manual ni el CSV.',
  'Aplicar esquema canónico, conservar _raw y agregar derivados con reglas explícitas.',
  'Añadir trazabilidad archivo, ruta, fila y SHA-256 a cada registro.',
  'Documentar correcciones manuales conocidas y separar las no reproducibles.',
  'Ejecutar controles de filas, huérfanos, duplicados, importes, horas y fechas.',
  'Registrar hallazgos con severidad, evidencia, impacto, decisión y pendiente.',
  'Versionar entregables y conservar manifiestos de descargas externas.',
]
const docs = [
  ['Diccionario de datos v1', 'DICCIONARIO_DATOS_v1.md'],
  ['Validación final del canónico', 'VALIDACION_FINAL_v1.md'],
  ['Bitácora de transformaciones', 'BITACORA_TRANSFORMACIONES_v1.md'],
  ['Registro de hallazgos', 'REGISTRO_HALLAZGOS_v1.md'],
  ['Validación de unicidad persona-período', 'VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md'],
  ['Bitácora de construcción del módulo', 'BITACORA_CONSTRUCCION_MODULO_PERSONAL_v1.md'],
  ['Checklist de verificación de la beta', 'CHECKLIST_VERIFICACION_MODULO_PERSONAL_v1.md'],
  ['Glosario canónico de definiciones', 'GLOSARIO_DEFINICIONES_v1.md'],
]
export default function Metodologia({ data }: { data: CommonData }) {
  return <div className="container page">
    <PageHeading eyebrow="Metodología y fuentes" title="El dato importa; también el camino que recorrió."><p>Este módulo no recalcula cifras desde planillas ocultas en el navegador: publica agregados reproducibles desde el canónico v1.0.0 y abre el detalle solo en el explorador.</p></PageHeading>
    <section className="data-section"><SectionHeading title="Controles de esta construcción" description="Comparación automática de los agregados contra VALIDACION_FINAL_v1." action={<a className="button secondary small" href={publicUrl('data/validacion_agregados.json')} target="_blank" rel="noreferrer">Control JSON <ExternalLink size={15} /></a>} /><div className="validation-banner"><span><Check size={25} /><strong>{data.meta.validacion_agregados.aprobadas} / {data.meta.validacion_agregados.controles} controles aprobados</strong></span><small>Generado: {new Date(data.meta.fecha_generacion).toLocaleString('es-CL')}</small></div><div className="table-scroll"><table><thead><tr><th>Categoría</th><th>Registros</th><th>IDs heredados</th><th>Bruto acumulado CLP</th><th>Bruto con 0 canónico</th><th>Fuente</th></tr></thead><tbody>{CATEGORIAS.map(categoria => <tr key={categoria}><td>{categoria}</td><td>{number.format(data.meta.conteos.registros_por_categoria[categoria])}</td><td>{data.meta.conteos.trabajadores_id_por_categoria[categoria]}</td><td>{number.format(data.meta.totales_por_categoria[categoria].gasto_bruto_clp)}</td><td>{data.meta.totales_por_categoria[categoria].registros_bruta_no_informa}</td><td><SourceButton trace={combineTraces(data.panel.filter(row => row.categoria === categoria).map(row => row.trazabilidad))} title={`Totales ${categoria}, 2023-2025`} compact /></td></tr>)}</tbody><tfoot><tr><th>Total</th><th>{number.format(data.meta.conteos.registros_totales)}</th><th>No sumable globalmente</th><th>{number.format(Object.values(data.meta.totales_por_categoria).reduce((s, r) => s + r.gasto_bruto_clp, 0))}</th><th>{data.meta.conteos.registros_bruta_no_informa}</th><td><SourceButton trace={combineTraces(data.panel.map(row => row.trazabilidad))} title="Totales del módulo, 2023-2025" compact /></td></tr></tfoot></table></div></section>

    <section className="data-section"><SectionHeading title="Pipeline reproducible en doce pasos" description="Del CSV original al canónico trazable; los agregados del sitio se regeneran además con un solo comando." /><ol className="method-steps">{steps.map((step, index) => <li key={step}><span>{String(index + 1).padStart(2, '0')}</span><p>{step}</p></li>)}</ol><div className="code-block"><span>Desde la raíz del proyecto</span><code>python scripts/build_modulo_personal.py</code></div></section>

    <section className="data-section"><SectionHeading title="Ausencias y límites declarados" description="Ninguna ausencia se interpola ni se transforma silenciosamente en cero." /><div className="absence-list">{data.ausencias.registros.filter(row => ['unidad_organizacional', 'cobertura', 'reconciliacion_fichas_agregados', 'licencia_reutilizacion'].includes(row.dimension)).map(row => <article key={`${row.dimension}-${row.periodo}-${row.categoria}`}><span>{row.categoria} · {row.periodo}</span><h3>{row.dimension.replaceAll('_', ' ')}</h3><p>{row.causa}</p></article>)}<article><span>Honorarios · 36 meses</span><h3>Horas extra no publicadas</h3><p>La fuente no publica horas extra. Código del Trabajo publica horas y monto sin desagregación por tipo.</p></article><article><span>Honorarios · informes de funciones</span><h3>Disponibilidad documental</h3><p>6.057 registros tienen PDF verificado en el respaldo; 3.094 no publican URL; 127 fueron eliminados en fuente y 186 están temporalmente deshabilitados. La distribución estática no duplica los 2,36 GB de PDF.</p></article></div><Notice title="Cobertura mensual"><p>Las cuatro categorías incluidas tienen archivos para los 36 meses. No hay huecos mensuales que completar. La categoría Autoridades está fuera del panel.</p></Notice></section>

    <section className="data-section"><SectionHeading title="Inventario de fuentes" description="168 CSV inventariados: 144 procesados en este módulo y 24 de Autoridades fuera de alcance." action={<a className="button secondary small" href={data.meta.portal_oficial} target="_blank" rel="noreferrer">Portal oficial <ExternalLink size={15} /></a>} /><DataDisclosure title="Abrir inventario archivo por archivo"><div className="table-scroll tall"><table><thead><tr><th>Categoría</th><th>Archivo</th><th>Filas</th><th>Estado</th><th>SHA-256</th></tr></thead><tbody>{data.fuentes.registros.map((row, index) => <tr key={index}><td>{String(row.categoria_inventario)}</td><td>{String(row.archivo)}</td><td>{String(row.filas)}</td><td>{String(row.estado)}</td><td className="hash truncate">{String(row.fuente_sha256)}</td></tr>)}</tbody></table></div></DataDisclosure></section>

    <section className="data-section"><SectionHeading title="Documentación y reutilización" /><div className="document-list">{docs.map(([label, file]) => <a key={file} href={publicUrl(`docs/${file}`)} target="_blank" rel="noreferrer"><FileText size={19} /><span>{label}</span><Download size={16} /></a>)}</div><div className="reuse-note"><h3>Cómo citar</h3><p><strong>Fuente:</strong> Municipalidad de Coronel, datos de transparencia activa del portal municipal, organismo MU068, categoría y período del registro; archivo, fila CSV y huella SHA-256 indicados en cada cifra. <strong>Producto derivado:</strong> Portal de Transparencia Trazable, módulo Personal y Remuneraciones, esquema canónico v1.0.0 y versión {data.meta.version}.</p><h3>Formatos</h3><p>JSON agregado y detalle anual para reutilización estructurada; exportación CSV del subconjunto filtrado con columnas de trazabilidad; CSV originales enlazados desde cada cifra.</p><h3>Licencia y atribución (D-16)</h3><p>El código de la plataforma se publica bajo licencia MIT. Los datos agregados y artefactos derivados del proyecto —JSON y CSV exportables— se ofrecen bajo CC BY 4.0, con atribución al Portal de Transparencia Trazable. Estas licencias no se atribuyen al municipio ni modifican la condición de los datos originales, que son datos públicos obtenidos por transparencia activa conforme a la Ley 20.285.</p></div></section>
  </div>
}
