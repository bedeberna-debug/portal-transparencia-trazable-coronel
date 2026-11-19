import { chromium } from '@playwright/test'
import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const plataforma = resolve(fileURLToPath(new URL('..', import.meta.url)))
const raiz = resolve(plataforma, '..')
const evidencia = resolve(raiz, 'documentación/plataforma/evidencia')
const base = process.env.QA_BASE_URL || 'http://127.0.0.1:7101'
mkdirSync(evidencia, { recursive: true })
const controles = []
const erroresConsola = []
const erroresPagina = []
const respuestasFallidas = []
const solicitudesFallidas = []
const check = (control, condicion, detalle) => {
  controles.push({ control, resultado: condicion ? 'APROBADO' : 'FALLA', evidencia: detalle })
  console.log(`${condicion ? 'OK' : 'FALLA'} ${control}: ${typeof detalle === 'string' ? detalle : JSON.stringify(detalle)}`)
}
const rutas = [
  ['portada', '/personal', 'Personas, contratos y remuneraciones'],
  ['panel', '/panel', 'La dotación completa'],
  ['explorador', '/explorador', 'Busque en todo el universo'],
  ['planta', '/estamento/Planta', 'Planta'],
  ['contrata', '/estamento/Contrata', 'Contrata'],
  ['codigo_trabajo', '/estamento/C%C3%B3digo%20del%20Trabajo', 'Código del Trabajo'],
  ['honorarios', '/estamento/Honorarios', 'Honorarios'],
  ['ficha_planta', '/ficha/PLT-2023-0032', 'CARO PARRA, CARMEN SALOME'],
  ['ficha_codigo', '/ficha/COT-2023-0015', 'FERNANDEZ CIFUENTES, GAIL MIRASLAVA BERNARDA'],
  ['metodologia', '/metodologia', 'El dato importa'],
]
const browser = await chromium.launch({ headless: true })
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true, reducedMotion: 'reduce', locale: 'es-CL' })
const page = await context.newPage()
page.on('console', msg => { if (msg.type() === 'error') erroresConsola.push(msg.text()) })
page.on('pageerror', error => erroresPagina.push(error.message))
page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) respuestasFallidas.push({ estado: response.status(), url: response.url() }) })
page.on('requestfailed', request => { if (request.url().startsWith(base)) solicitudesFallidas.push({ url: request.url(), error: request.failure()?.errorText }) })
async function abrir(ruta) {
  await page.goto(`${base}/#${ruta}`, { waitUntil: 'networkidle' })
  await page.locator('h1').waitFor()
  if (ruta.startsWith('/explorador')) await page.locator('.explorer-table tbody tr').first().waitFor({ timeout: 30000 })
  await page.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0) })
  await page.waitForTimeout(250)
}
async function captura(nombre) {
  await page.evaluate(() => window.scrollTo(0, 0))
  await page.waitForTimeout(100)
  await page.screenshot({ path: resolve(evidencia, `${nombre}.png`), animations: 'disabled' })
}
async function sinDesborde() {
  return page.evaluate(() => ({ viewport: innerWidth, documento: document.documentElement.scrollWidth, cuerpo: document.body.scrollWidth }))
}
async function rgbDeColores(colores) {
  return page.evaluate(valores => {
    const canvas = document.createElement('canvas')
    canvas.width = valores.length
    canvas.height = 1
    const ctx = canvas.getContext('2d', { willReadFrequently: true })
    if (!ctx) throw new Error('Canvas no disponible para medir colores')
    valores.forEach((color, index) => {
      ctx.fillStyle = color
      ctx.fillRect(index, 0, 1, 1)
    })
    const pixels = ctx.getImageData(0, 0, valores.length, 1).data
    return valores.map((color, index) => ({ color, rgb: [...pixels.slice(index * 4, index * 4 + 3)] }))
  }, colores)
}
function contrasteAA(primero, segundo) {
  const luminancia = rgb => {
    const canales = rgb.map(valor => {
      const canal = valor / 255
      return canal <= 0.04045 ? canal / 12.92 : ((canal + 0.055) / 1.055) ** 2.4
    })
    return canales[0] * 0.2126 + canales[1] * 0.7152 + canales[2] * 0.0722
  }
  const a = luminancia(primero)
  const b = luminancia(segundo)
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)
}

const formatoNumero = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 0 })
const formatoMoneda = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 })
async function verificarGraficoMovil(ruta, nombre) {
  await page.setViewportSize({ width: 375, height: 812 })
  await abrir(ruta)
  const chart = page.locator(`[data-chart="${nombre}"]`)
  await chart.locator('.recharts-wrapper').waitFor()
  await page.waitForTimeout(200)
  const medicion = await chart.evaluate(root => {
    const caja = root.getBoundingClientRect()
    const wrapper = root.querySelector('.recharts-responsive-container').getBoundingClientRect()
    const grid = root.querySelector('.recharts-cartesian-grid')?.getBoundingClientRect()
    const ticks = [...root.querySelectorAll('.recharts-xAxis .recharts-cartesian-axis-tick text')].map(node => {
      const rect = node.getBoundingClientRect()
      return { texto: node.textContent, izquierda: rect.left, derecha: rect.right, arriba: rect.top, abajo: rect.bottom, fuente: parseFloat(getComputedStyle(node).fontSize) }
    })
    const solapes = []
    for (let i = 0; i < ticks.length; i++) for (let j = i + 1; j < ticks.length; j++) {
      const a = ticks[i], b = ticks[j]
      if (a.izquierda < b.derecha - 1 && a.derecha > b.izquierda + 1 && a.arriba < b.abajo - 1 && a.abajo > b.arriba + 1) solapes.push([a.texto, b.texto])
    }
    return {
      ancho_contenedor: caja.width,
      ancho_recharts: wrapper.width,
      espacio_muerto_derecho: caja.right - wrapper.right,
      espacio_muerto_trazado: grid ? wrapper.right - grid.right : null,
      ticks: ticks.length,
      fuente_minima: Math.min(...ticks.map(tick => tick.fuente)),
      solapes,
    }
  })
  const legible = medicion.solapes.length === 0 && medicion.ticks >= 5 && medicion.fuente_minima >= 10
  const anchoCompleto = medicion.ancho_recharts >= medicion.ancho_contenedor - 3 && medicion.espacio_muerto_derecho <= 3 && medicion.espacio_muerto_trazado !== null && medicion.espacio_muerto_trazado <= 3
  const vista = decodeURIComponent(ruta.split('/').at(-1)).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()
  check(`grafico_movil_${vista}_etiquetas_y_ancho`, legible && anchoCompleto, { ruta, ...medicion, legible, ancho_completo: anchoCompleto })
  await chart.screenshot({ path: resolve(evidencia, `11_grafico_${vista}_375.png`), animations: 'disabled' })
}
try {
  await abrir('/personal')
  const inicio = await page.evaluate(() => {
    const recursos = performance.getEntriesByType('resource')
    return {
      solicitudes: recursos.length,
      bytes_codificados: recursos.reduce((suma, r) => suma + (r.encodedBodySize || 0), 0),
      explorador_precargado: recursos.some(r => r.name.includes('/data/explorador_')),
      viewport_meta: Boolean(document.querySelector('meta[name="viewport"]')),
    }
  })
  check('carga_inicial_liviana_y_diferida', !inicio.explorador_precargado && inicio.viewport_meta, inicio)
  const tarjetasAcceso = page.locator('.navigation-cards > a')
  const fondosAcceso = await tarjetasAcceso.evaluateAll(nodes => nodes.map(node => getComputedStyle(node).backgroundColor))
  const titulosAcceso = await tarjetasAcceso.locator('strong').allInnerTexts()
  check('portada_cuatro_accesos_cromaticos', await tarjetasAcceso.count() === 4 && new Set(fondosAcceso).size === 4 && titulosAcceso.join('|') === 'Panel general|Explorador del personal|Vistas estamentales|Metodología y fuentes', { fondos: fondosAcceso, titulos: titulosAcceso })
  const estilosAcceso = await tarjetasAcceso.evaluateAll(nodes => nodes.map(node => {
    const estilo = getComputedStyle(node)
    const franja = getComputedStyle(node, '::before')
    const icono = node.querySelector('svg')
    return {
      tarjeta: node.querySelector('strong')?.textContent,
      fondo: estilo.backgroundColor,
      texto: getComputedStyle(node.querySelector('strong')).color,
      acento: estilo.getPropertyValue('--card-accent').trim(),
      franja: franja.height,
      franja_color: franja.backgroundColor,
      icono_fondo: icono ? getComputedStyle(icono).backgroundColor : '',
    }
  }))
  const coloresAcceso = await rgbDeColores(estilosAcceso.flatMap(item => [item.fondo, item.texto]))
  const contrasteAcceso = estilosAcceso.map((item, index) => ({
    ...item,
    razon_contraste: Number(contrasteAA(coloresAcceso[index * 2].rgb, coloresAcceso[index * 2 + 1].rgb).toFixed(2)),
  }))
  check('portada_tarjetas_contraste_aa_y_refuerzo_no_cromatico', contrasteAcceso.every(item => item.razon_contraste >= 4.5 && parseFloat(item.franja) >= 7 && item.franja_color !== 'rgba(0, 0, 0, 0)' && item.icono_fondo !== 'rgba(0, 0, 0, 0)'), contrasteAcceso)
  const estiloComprobante = await page.locator('.home-access-section .hero-proof').evaluate(node => ({
    texto: getComputedStyle(node).color,
    destacado: getComputedStyle(node.querySelector('strong')).color,
    icono: getComputedStyle(node.querySelector('svg')).color,
    fondo: getComputedStyle(document.body).backgroundColor,
  }))
  const coloresComprobante = await rgbDeColores([estiloComprobante.texto, estiloComprobante.destacado, estiloComprobante.icono, estiloComprobante.fondo])
  const contrasteComprobante = {
    ...estiloComprobante,
    texto: Number(contrasteAA(coloresComprobante[0].rgb, coloresComprobante[3].rgb).toFixed(2)),
    destacado: Number(contrasteAA(coloresComprobante[1].rgb, coloresComprobante[3].rgb).toFixed(2)),
    icono: Number(contrasteAA(coloresComprobante[2].rgb, coloresComprobante[3].rgb).toFixed(2)),
  }
  check('portada_comprobante_controles_contraste_aa', contrasteComprobante.texto >= 4.5 && contrasteComprobante.destacado >= 4.5 && contrasteComprobante.icono >= 3, contrasteComprobante)
  const ordenPortada = await page.evaluate(() => {
    const hero = document.querySelector('.home-hero')
    const accesos = document.querySelector('.home-access-section')
    const indicadores = document.querySelector('#titulares')?.closest('section')
    return {
      hero_antes_accesos: Boolean(hero && accesos && (hero.compareDocumentPosition(accesos) & Node.DOCUMENT_POSITION_FOLLOWING)),
      accesos_antes_indicadores: Boolean(accesos && indicadores && (accesos.compareDocumentPosition(indicadores) & Node.DOCUMENT_POSITION_FOLLOWING)),
      ultimo_mes_rotulado: indicadores?.textContent?.includes('Último mes publicado') && indicadores?.textContent?.includes('dic 2025'),
    }
  })
  check('portada_intro_accesos_luego_ultimo_mes', Object.values(ordenPortada).every(Boolean), ordenPortada)
  const iconosGlosario = await page.locator('.glossary-card.icon-only > summary').evaluateAll(nodes => nodes.map(node => ({ texto: node.textContent.trim(), aria: node.getAttribute('aria-label'), ancho: node.getBoundingClientRect().width, alto: node.getBoundingClientRect().height })))
  const notaGlosario = await page.locator('.glossary-global-note').allTextContents()
  check('glosario_simbolo_y_leyenda_global_unica', iconosGlosario.length > 0 && iconosGlosario.every(item => item.texto === '¡' && item.aria?.startsWith('Definición de ') && item.ancho >= 44 && item.alto >= 44) && notaGlosario.length === 1 && notaGlosario[0].replace(/\s+/g, ' ').trim() === '¡ El símbolo ¡ abre una tarjeta con la definición del término y su fuente normativa.', { iconos: iconosGlosario, leyendas_globales: notaGlosario })
  await page.locator('.navigation-cards').screenshot({ path: resolve(evidencia, '01b_portada_accesos_1440.png'), animations: 'disabled' })
  await page.setViewportSize({ width: 375, height: 812 })
  await page.waitForTimeout(150)
  const geometriaAccesos = await tarjetasAcceso.evaluateAll(nodes => nodes.map(node => { const r = node.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), ancho: Math.round(r.width), alto: Math.round(r.height) } }))
  const filasAccesos = new Set(geometriaAccesos.map(item => item.y)).size
  const columnasAccesos = new Set(geometriaAccesos.map(item => item.x)).size
  check('portada_accesos_movil_cuadricula_2x2', filasAccesos === 2 && columnasAccesos === 2, geometriaAccesos)
  await page.locator('.navigation-cards').screenshot({ path: resolve(evidencia, '01c_portada_accesos_375.png'), animations: 'disabled' })
  await page.setViewportSize({ width: 1440, height: 1000 })

  const leerNavegacion = selector => page.locator(selector).evaluateAll(nodes => nodes.map(node => {
    const estilo = getComputedStyle(node)
    return { texto: node.textContent, tono: [...node.classList].find(clase => clase.startsWith('tone-')), fondo: estilo.backgroundColor, texto_color: estilo.color, activa: node.classList.contains('active'), franja: getComputedStyle(node, '::before').height }
  }))
  const estilosNavegacion = await leerNavegacion('.main-nav .nav-link')
  for (const ruta of ['/panel', '/explorador', '/estamento/Planta', '/metodologia']) {
    await abrir(ruta)
    estilosNavegacion.push(...await leerNavegacion('.main-nav .nav-link.active'))
  }
  const coloresNavegacion = await rgbDeColores(estilosNavegacion.flatMap(item => [item.fondo, item.texto_color]))
  const contrasteNavegacion = estilosNavegacion.map((item, index) => ({ ...item, razon_contraste: Number(contrasteAA(coloresNavegacion[index * 2].rgb, coloresNavegacion[index * 2 + 1].rgb).toFixed(2)) }))
  check('navegacion_superior_paleta_portada_y_contraste_aa', contrasteNavegacion.length === 9 && contrasteNavegacion.filter(item => item.activa).length === 5 && new Set(contrasteNavegacion.slice(0, 5).map(item => item.fondo)).size === 5 && contrasteNavegacion.every(item => item.tono && item.razon_contraste >= 4.5 && parseFloat(item.franja) >= 3), contrasteNavegacion)
  await abrir('/personal')
  await page.locator('.main-nav').screenshot({ path: resolve(evidencia, '00b_navegacion_superior_1440.png'), animations: 'disabled' })
  await page.setViewportSize({ width: 375, height: 812 })
  await page.getByRole('button', { name: 'Abrir navegación' }).click()
  await page.locator('.main-nav').screenshot({ path: resolve(evidencia, '00c_navegacion_superior_375.png'), animations: 'disabled' })
  await page.getByRole('button', { name: 'Cerrar navegación' }).click()
  await page.setViewportSize({ width: 1440, height: 1000 })

  await page.getByRole('button', { name: /¿De dónde sale este dato\? Dotación total/ }).click()
  const dialogo = page.locator('dialog.source-dialog')
  await dialogo.waitFor({ state: 'visible' })
  check('fuente_abre_con_archivo_fila_periodo_y_sha', await dialogo.locator('.source-file').count() > 0 && (await dialogo.innerText()).includes('Filas CSV') && (await dialogo.innerText()).includes('SHA-256'), await dialogo.locator('h2').innerText())
  const primerArchivo = dialogo.locator('.source-file').first()
  const sha = await primerArchivo.locator('dt', { hasText: 'SHA-256' }).locator('..').locator('dd').innerText()
  const href = await primerArchivo.getByRole('link', { name: /Abrir CSV fuente/ }).getAttribute('href')
  const respuestaCsv = await context.request.get(new URL(href, page.url()).href)
  const hashDescargado = createHash('sha256').update(await respuestaCsv.body()).digest('hex')
  check('csv_fuente_http_y_sha', respuestaCsv.status() === 200 && hashDescargado === sha.trim(), { estado: respuestaCsv.status(), sha_declarado: sha.trim(), sha_descargado: hashDescargado })
  await page.getByRole('button', { name: 'Cerrar fuente' }).click()
  check('fuente_cierra_con_boton', !(await dialogo.isVisible()), 'Botón Cerrar fuente')
  await page.getByRole('button', { name: /¿De dónde sale este dato\? Dotación total/ }).click()
  await page.keyboard.press('Escape')
  check('fuente_cierra_con_escape', !(await dialogo.isVisible()), 'Tecla Escape')
  await page.getByRole('button', { name: /¿De dónde sale este dato\? Dotación total/ }).click()
  await page.mouse.click(2, 2)
  check('fuente_cierra_con_backdrop', !(await dialogo.isVisible()), 'Clic fuera del contenido')

  const meta = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/meta.json'), 'utf8'))
  const panelJson = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/panel_general_mensual.json'), 'utf8')).registros
  const estamentosJson = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/composicion_estamento.json'), 'utf8')).registros
  const estimadosJson = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/composicion_estamento_estimado.json'), 'utf8')).registros
  const glosarioJson = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/glosario_definiciones.json'), 'utf8')).registros
  const asignacionesIndice = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/asignaciones_indice.json'), 'utf8'))
  const ausenciasJson = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/ausencias.json'), 'utf8')).registros
  check('asignaciones_indice_publicado_y_cobertura_exacta', asignacionesIndice.total_conceptos === 394 && asignacionesIndice.conceptos.length === 394 && asignacionesIndice.cobertura_modulo.registros_con_codigos === 13476 && asignacionesIndice.cobertura_modulo.registros_completamente_decodificados === 13475 && asignacionesIndice.cobertura_modulo.ocurrencias_decodificadas === 61548 && asignacionesIndice.anomalias_observadas.length === 1, asignacionesIndice.cobertura_modulo)
  await abrir('/panel')
  check('panel_dona_serie_y_cuatro_indicadores', await page.getByTestId('category-donut').count() === 1 && (await page.locator('.chart-wrap').first().getAttribute('aria-label')).includes('por categoría de vínculo') && await page.locator('.category-indicator').count() === 4, { donas: await page.getByTestId('category-donut').count(), indicadores: await page.locator('.category-indicator').count() })
  const indicadoresCoinciden = await Promise.all(panelJson.filter(row => row.periodo === meta.ultimo_periodo).map(async row => {
    const texto = await page.getByTestId(`indicator-${row.categoria}`).innerText()
    return texto.includes(formatoNumero.format(row.dotacion_registros)) && texto.includes(formatoMoneda.format(row.promedio_bruto_clp)) && texto.includes(formatoMoneda.format(row.mediana_bruta_clp)) && texto.includes(formatoNumero.format(row.registros_bruta_no_informa))
  }))
  check('panel_indicadores_calzan_json', indicadoresCoinciden.every(Boolean), { periodo: meta.ultimo_periodo, categorias_verificadas: indicadoresCoinciden.length })
  await page.getByTestId('panel-period').selectOption('2023-01')
  check('panel_mes_controla_dona_indicadores_y_comparativa', (await page.getByTestId('category-donut').getAttribute('aria-label')).includes('2023-01') && (await page.locator('#indicadores-categoria').locator('..').locator('h2').innerText()).includes('ene 2023') && (await page.locator('#comparativa-estamental').locator('..').innerText()).includes('ene 2023'), 'Mes cambiado de dic 2025 a ene 2023')
  await page.getByTestId('panel-period').selectOption(meta.ultimo_periodo)
  await page.locator('.recharts-bar-rectangle path').first().hover({ force: true })
  const tooltipPanel = page.getByTestId('segment-tooltip')
  await tooltipPanel.waitFor({ state: 'visible' })
  check('panel_tooltip_categoria_y_porcentaje', (await tooltipPanel.getAttribute('data-estamento')) === 'Planta' && (await tooltipPanel.innerText()).includes('% de esta barra'), await tooltipPanel.innerText())
  await page.getByTestId('panel-metric').selectOption('gasto_bruto_clp')
  await page.locator('.recharts-bar-rectangle path').first().hover({ force: true })
  check('panel_monto_tooltip_declara_no_informa', (await tooltipPanel.innerText()).includes('No informa') && (await tooltipPanel.innerText()).includes('Remuneración bruta'), await tooltipPanel.innerText())
  const areaDona = await page.locator('.donut-chart .recharts-wrapper').boundingBox()
  if (!areaDona) throw new Error('No se encontró el área gráfica de la dona')
  await page.mouse.move(areaDona.x + areaDona.width / 2, areaDona.y + areaDona.height / 2 - 100)
  const tooltipDona = page.getByTestId('donut-tooltip')
  await tooltipDona.waitFor({ state: 'visible' })
  check('panel_dona_monto_declara_no_informa', (await tooltipDona.innerText()).includes('% del total') && (await tooltipDona.innerText()).includes('No informa'), await tooltipDona.innerText())

  const comparativaPlanta = estamentosJson.filter(row => row.periodo === meta.ultimo_periodo && row.categoria === 'Planta')
  const filasPlanta = await page.locator('.estamento-stats tbody tr').allInnerTexts()
  const statsPlantaCalzan = comparativaPlanta.length === filasPlanta.length && comparativaPlanta.every((row, index) => filasPlanta[index].includes(row.estamento) && filasPlanta[index].includes(formatoMoneda.format(row.gasto_bruto_clp)) && filasPlanta[index].includes(formatoMoneda.format(row.promedio_bruto_clp)) && filasPlanta[index].includes(formatoMoneda.format(row.mediana_bruta_clp)))
  check('panel_comparativa_solo_planta_y_estadisticas_exactas', statsPlantaCalzan && (await page.locator('#comparativa-estamental').locator('..').locator('h2').innerText()).includes('dentro de Planta'), { segmentos: filasPlanta.length, periodo: meta.ultimo_periodo })

  const tarjetaPlanta = page.locator('.category-donut details.glossary-card[data-term="Planta"]')
  await tarjetaPlanta.locator('summary').click()
  const entradaPlanta = glosarioJson.find(entry => entry.termino === 'Planta')
  const textoTarjetaPlanta = await tarjetaPlanta.innerText()
  check('glosario_definicion_y_fuente_exactas', textoTarjetaPlanta.includes(entradaPlanta.definicion) && textoTarjetaPlanta.includes(entradaPlanta.fuente), { termino: entradaPlanta.termino, fuente: entradaPlanta.fuente })
  check('glosario_placeholder_modulo_normativo', (await tarjetaPlanta.locator('.module-placeholder').innerText()).includes('módulo en desarrollo') && await tarjetaPlanta.getByRole('link', { name: 'Glosario canónico' }).isVisible(), await tarjetaPlanta.locator('.glossary-links').innerText())
  await tarjetaPlanta.screenshot({ path: resolve(evidencia, '02b_panel_glosario_1440.png'), animations: 'disabled' })
  await tarjetaPlanta.locator('summary').click()

  await page.getByTestId('panel-category').selectOption('Honorarios')
  check('panel_honorarios_estimado_por_defecto', (await page.getByTestId('panel-dimension').inputValue()) === 'estamento_estimado' && (await page.locator('.estimated-legend').first().innerText()) === meta.estamento_estimado.leyenda_fija, 'D-17 y leyenda fija en Honorarios')
  const comparativaHonorarios = estimadosJson.filter(row => row.periodo === meta.ultimo_periodo && row.categoria === 'Honorarios')
  const filasHonorarios = await page.locator('.estamento-stats tbody tr').allInnerTexts()
  const statsHonorariosCalzan = comparativaHonorarios.length === filasHonorarios.length && comparativaHonorarios.every((row, index) => filasHonorarios[index].includes(row.estamento_estimado) && filasHonorarios[index].includes(formatoMoneda.format(row.gasto_bruto_clp)) && filasHonorarios[index].includes(formatoMoneda.format(row.promedio_bruto_clp)) && filasHonorarios[index].includes(formatoMoneda.format(row.mediana_bruta_clp)))
  check('panel_honorarios_no_clasificable_y_estadisticas_exactas', statsHonorariosCalzan && filasHonorarios.some(texto => texto.includes('No clasificable')), { segmentos: filasHonorarios.length, no_clasificable_visible: filasHonorarios.some(texto => texto.includes('No clasificable')) })
  const horasJson = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/horas_extra_mensual.json'), 'utf8')).registros
  const formatoDecimal = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 2 })
  const resumenHorasInicial = await page.getByTestId('hours-summary').innerText()
  const horasUltimoMesCalzan = ['Planta', 'Contrata', 'Código del Trabajo'].every(categoria => {
    const esperado = horasJson.filter(row => row.periodo === meta.ultimo_periodo && row.categoria === categoria).reduce((sum, row) => sum + (row.horas || 0), 0)
    return resumenHorasInicial.includes(formatoDecimal.format(esperado))
  })
  check('horas_extra_inicia_ultimo_mes_y_calza_json', (await page.getByTestId('hours-mode').inputValue()) === 'mes' && (await page.getByTestId('hours-period').inputValue()) === meta.ultimo_periodo && resumenHorasInicial.includes('dic 2025') && horasUltimoMesCalzan, { periodo: meta.ultimo_periodo, horas_por_categoria_verificadas: 3 })
  await page.getByTestId('hours-period').selectOption('2023-01')
  check('horas_extra_cambia_de_mes', (await page.getByTestId('hours-summary').locator('h2').innerText()).includes('ene 2023') && (await page.locator('.data-disclosure summary', { hasText: 'Detalle del mes y fuentes, ene 2023' }).count()) === 1, 'Selector dic 2025 → ene 2023')
  await page.getByTestId('hours-mode').selectOption('anio')
  await page.getByTestId('hours-year').selectOption('2023')
  check('horas_extra_cambia_de_anio', (await page.locator('.data-disclosure summary', { hasText: 'Detalle mensual y fuentes, 2023' }).count()) === 1, 'Modo anual, selector 2023')
  await page.getByTestId('hours-year').selectOption('2025')
  check('leyenda_genero_panel', (await page.locator('.gender-legend').innerText()) === meta.privacidad.leyenda, meta.privacidad.leyenda)

  await abrir('/explorador')
  check('explorador_carga_50_filas_iniciales', await page.locator('.explorer-table tbody tr').count() === 50, `${await page.locator('.explorer-table tbody tr').count()} filas`)
  const primaryFilters = page.getByTestId('primary-filters')
  const advancedFilters = page.getByTestId('advanced-filters')
  const explorerIndicators = page.getByTestId('explorer-indicators')
  const chips = page.getByTestId('active-filter-chips')
  const textoChipsInicial = (await chips.innerText()).replace(/\s+/g, ' ')
  check('explorador_paneles_plegados_chips_y_tabla_inmediata', !(await primaryFilters.evaluate(node => node.open)) && !(await advancedFilters.evaluate(node => node.open)) && !(await explorerIndicators.evaluate(node => node.open)) && textoChipsInicial.includes('22.940 registros seleccionados') && await page.locator('.explorer-table').isVisible(), textoChipsInicial)
  const primerEnlaceFicha = page.locator('.explorer-table tbody tr').first().locator('.person-cell')
  check('explorador_enlaza_fichas_habilitadas', (await primerEnlaceFicha.innerText()).includes('Abrir ficha') && (await primerEnlaceFicha.locator('a').getAttribute('href'))?.includes('/ficha/'), await primerEnlaceFicha.innerText())
  const textoFiltros = await page.locator('.filter-panel').allInnerTexts()
  const encabezados = await page.locator('.explorer-table thead').innerText()
  check('genero_ausente_de_filtros_y_tabla', !/género|genero/i.test(textoFiltros.join(' ') + encabezados), 'Sin filtro ni columna de género')
  await page.locator('.explorer-table tbody tr').first().getByText('Campos', { exact: true }).click()
  const detalle = await page.locator('.explorer-table tbody tr').first().locator('.record-detail').innerText()
  check('genero_ausente_de_detalle_individual', !/genero|género|primer_nombre|nombre_normalizado/i.test(detalle), 'Detalle de campos sin género ni derivados de nombre')
  check('explorador_estimado_rotulado_y_con_leyenda', await page.locator('.explorer-table .estimated-individual').count() > 0 && (await page.locator('.page-heading .estimated-legend').innerText()).includes(meta.estamento_estimado.leyenda_fija), `${await page.locator('.explorer-table .estimated-individual').count()} filas visibles con estimación rotulada`)

  await page.getByTestId('explorer-search').fill('CARO PARRA, CARMEN SALOME')
  await page.waitForTimeout(100)
  const nombresBusqueda = await page.locator('.explorer-table .person-cell a').allInnerTexts()
  check('explorador_busca_por_nombre', nombresBusqueda.length > 0 && nombresBusqueda.every(nombre => nombre.includes('CARO PARRA, CARMEN SALOME')) && (await chips.innerText()).includes('Búsqueda: CARO PARRA'), { resultados_visibles: nombresBusqueda.length })
  await page.getByTestId('explorer-search').fill('MEDICO PSICOTECNICO')
  await page.waitForTimeout(100)
  const cargosBusqueda = await page.locator('.explorer-table tbody tr td:nth-child(5)').allInnerTexts()
  check('explorador_busca_por_cargo', cargosBusqueda.length > 0 && cargosBusqueda.every(cargo => cargo.includes('MEDICO PSICOTECNICO')), { resultados_visibles: cargosBusqueda.length })
  await page.getByRole('button', { name: /Limpiar filtros/ }).click()
  await page.locator('.pagination button').nth(1).click()
  check('paginacion_siguiente_y_anterior', (await page.locator('.pagination').innerText()).includes('Página 2 /'), await page.locator('.pagination').innerText())
  await page.locator('.pagination button').nth(0).click()

  await primaryFilters.locator(':scope > summary').click()
  await page.getByLabel('Período desde').fill('2025-01')
  await page.getByLabel('Período hasta').fill('2025-12')
  await primaryFilters.locator('select').nth(0).selectOption('Planta')
  await primaryFilters.locator('select').nth(1).selectOption('Administrativo')
  await page.getByTestId('explorer-search').fill('a')
  const registros2025 = JSON.parse(readFileSync(resolve(plataforma, 'dist/data/explorador_2025.json'), 'utf8')).registros
  const esperadoFiltrado = registros2025.filter(r => r.categoria === 'Planta' && r.estamento === 'Administrativo' && (r.cargo_funcion.toLocaleLowerCase('es').includes('a') || r.nombre_original.toLocaleLowerCase('es').includes('a'))).length
  const textoSeleccion = (await chips.innerText()).replace(/\s+/g, ' ')
  check('filtros_combinables_conteo_exacto_y_busqueda_sobre_subconjunto', textoSeleccion.includes(`${new Intl.NumberFormat('es-CL').format(esperadoFiltrado)} registros seleccionados`) && textoSeleccion.includes('Planta') && textoSeleccion.includes('Administrativo'), { esperado: esperadoFiltrado, interfaz: textoSeleccion })
  await explorerIndicators.locator(':scope > summary').click()
  check('genero_no_calculable_con_filtro_individual', (await page.locator('.metric.unavailable').innerText()).includes('No calculable') && await page.getByText('Ausencia de porcentaje por privacidad').isVisible(), 'Búsqueda individual activada')
  const promesaDescarga = page.waitForEvent('download')
  await page.getByRole('button', { name: /Exportar CSV trazable/ }).click()
  const descarga = await promesaDescarga
  const flujo = await descarga.createReadStream()
  const chunks = []
  for await (const chunk of flujo) chunks.push(chunk)
  const csv = Buffer.concat(chunks).toString('utf8')
  const cabeceraCsv = csv.split(/\r?\n/, 1)[0].toLocaleLowerCase('es')
  check('exportacion_csv_filtrada_y_sin_genero', csv.split(/\r?\n/).length - 1 === esperadoFiltrado && !/genero|género|primer_nombre|nombre_normalizado/.test(cabeceraCsv), { archivo: descarga.suggestedFilename(), registros: esperadoFiltrado, columnas: cabeceraCsv })
  check('exportacion_csv_asignaciones_serializadas', cabeceraCsv.includes('asignaciones_decodificadas') && csv.includes('""codigo""') && !csv.includes('[object Object]'), { columna_decodificada: cabeceraCsv.includes('asignaciones_decodificadas'), escape_csv: csv.includes('""codigo""'), sin_objetos_genericos: !csv.includes('[object Object]') })
  await page.getByRole('button', { name: /Limpiar filtros/ }).click()
  const textoLimpieza = (await chips.innerText()).replace(/\s+/g, ' ')
  check('limpiar_filtros_conserva_categoria_y_recupera_universo', textoLimpieza.includes('4.927 registros seleccionados') && await page.locator('.gender-legend').isVisible(), textoLimpieza)
  await page.getByLabel('Período desde').fill('2025-12')
  await page.getByLabel('Período hasta').fill('2023-01')
  check('rango_invertido_declara_ausencia_de_resultados', await page.getByText('Rango de períodos invertido').isVisible() && await page.getByText('No hay registros para esta selección').isVisible(), 'Sin interpolación ni resultados ficticios')

  await page.getByLabel('Período desde').fill('2023-01')
  await page.getByLabel('Período hasta').fill('2023-01')
  await page.getByTestId('explorer-search').fill('JEFA DEPTO. GAB. PSICOTECNICO')
  const filaAsignaciones = page.locator('tr[data-record="PLT-202301-2261B85B00"]')
  await filaAsignaciones.waitFor()
  await filaAsignaciones.getByText('Campos', { exact: true }).click()
  const detalleAsignaciones = filaAsignaciones.locator('.record-detail')
  const textoAsignaciones = await detalleAsignaciones.innerText()
  check('explorador_asignaciones_decodificadas_y_raw_visible', textoAsignaciones.includes('(39)(11)(10)(08)(07)(06)(04)(04)') && textoAsignaciones.includes('Incentivo Juez Policía Local') && textoAsignaciones.match(/Bono de subrogación/g)?.length === 2 && !textoAsignaciones.includes('[object Object]'), textoAsignaciones.match(/Asignaciones especiales publicadas[\s\S]*?(?=Bruto publicado)/)?.[0] || textoAsignaciones.slice(0, 500))
  await detalleAsignaciones.screenshot({ path: resolve(evidencia, '03b_explorador_asignaciones_decodificadas_1440.png'), animations: 'disabled' })
  await page.getByTestId('explorer-search').fill('MEDICO PSICOTECNICO')
  const filaAnomala = page.locator('tr[data-record="PLT-202301-95B4374AC0"]')
  await filaAnomala.waitFor()
  await filaAnomala.getByText('Campos', { exact: true }).click()
  const detalleAnomalo = filaAnomala.locator('.record-detail')
  const textoAnomalo = await detalleAnomalo.innerText()
  check('explorador_anomalia_menos4_sin_decodificar', textoAnomalo.includes('Código sin decodificar') && textoAnomalo.includes('Código fuera del formato') && /Asignaciones especiales publicadas \(_raw\)\n-4/.test(textoAnomalo), textoAnomalo.match(/Asignaciones especiales publicadas[\s\S]*?(?=Bruto publicado)/)?.[0] || 'No se aisló el bloque')
  await detalleAnomalo.screenshot({ path: resolve(evidencia, '03c_explorador_asignacion_anomala_1440.png'), animations: 'disabled' })

  await abrir('/estamento/Honorarios')
  check('honorarios_declara_horas_no_publicadas', (await page.locator('.metrics-grid').first().innerText()).includes('No publica'), 'Métrica Horas extra, 2025')
  check('cifras_secundarias_honorarios_con_fuente', await page.getByRole('button', { name: /Tipo de pago de Honorarios|Número de cuotas de Honorarios|Estados de informes de Honorarios|Honorarios, identificadores heredados/ }).count() === 4, 'Cuatro accesos directos a fuente')
  await page.getByRole('button', { name: /Honorarios, identificadores heredados/ }).click()
  check('fuente_identificadores_heredados_con_respaldo', await dialogo.locator('.source-file').count() > 0, `${await dialogo.locator('.source-file').count()} archivos en la trazabilidad`)
  await page.getByRole('button', { name: 'Cerrar fuente' }).click()
  check('fichas_habilitadas_tras_d15', meta.ficha_individual.habilitada && meta.ficha_individual.colisiones_id_periodo === 0 && meta.ficha_individual.colisiones_resueltas_d15 === 2, meta.ficha_individual)
  check('honorarios_estimado_por_defecto_y_publicado_disponible', (await page.getByTestId('estamental-dimension').inputValue()) === 'estamento_estimado' && (await page.getByTestId('estamental-dimension').locator('option').allInnerTexts()).includes('Estamento publicado'), await page.getByTestId('estamental-dimension').inputValue())
  check('honorarios_leyenda_y_no_clasificable', (await page.locator('.estimated-legend').first().innerText()) === meta.estamento_estimado.leyenda_fija && (await page.locator('.chart-wrap').first().locator('.chart-legend').innerText()).includes('No clasificable'), 'Leyenda D-17 y categoría visible')
  const excepcionGlosario = page.locator('.glossary-card.with-label[data-term="Estamento estimado"] > summary').first()
  const textoExcepcion = await excepcionGlosario.innerText()
  check('glosario_excepcion_conserva_icono_y_texto', textoExcepcion.includes('¡') && textoExcepcion.includes('Sobre la estimación') && (await excepcionGlosario.getAttribute('aria-label')) === 'Definición de Estamento estimado', textoExcepcion)
  await page.locator('.recharts-bar').nth(4).locator('path').first().hover({ force: true })
  const tooltipHonorarios = page.getByTestId('segment-tooltip')
  await tooltipHonorarios.waitFor({ state: 'visible' })
  check('honorarios_tooltip_solo_segmento_no_clasificable', (await tooltipHonorarios.getAttribute('data-estamento')) === 'No clasificable' && (await tooltipHonorarios.locator('strong').count()) === 1 && (await tooltipHonorarios.innerText()).includes('% de esta barra'), await tooltipHonorarios.innerText())
  await page.getByTestId('estamental-metric').selectOption('gasto_bruto_clp')
  await page.locator('.recharts-bar').nth(4).locator('path').first().hover({ force: true })
  check('honorarios_tooltip_monto_y_no_informa_segmento', (await tooltipHonorarios.getAttribute('data-estamento')) === 'No clasificable' && (await tooltipHonorarios.innerText()).includes('No informa'), await tooltipHonorarios.innerText())
  await abrir('/estamento/Planta')
  const leerPestanas = selector => page.locator(selector).evaluateAll(nodes => nodes.map(node => {
    const estilo = getComputedStyle(node)
    return { categoria: node.getAttribute('data-category'), color_categoria: estilo.getPropertyValue('--category-color').trim(), fondo: estilo.backgroundColor, texto: estilo.color, activa: node.classList.contains('active'), radio: estilo.borderRadius }
  }))
  const estilosPestanas = await leerPestanas('.category-tabs a')
  for (const categoria of ['Contrata', 'Código del Trabajo', 'Honorarios']) {
    await abrir(`/estamento/${encodeURIComponent(categoria)}`)
    estilosPestanas.push(...await leerPestanas('.category-tabs a.active'))
  }
  const coloresPestanas = await rgbDeColores(estilosPestanas.flatMap(item => [item.fondo, item.texto]))
  const contrastePestanas = estilosPestanas.map((item, index) => ({ ...item, razon_contraste: Number(contrasteAA(coloresPestanas[index * 2].rgb, coloresPestanas[index * 2 + 1].rgb).toFixed(2)) }))
  const paletaCategoria = { Planta: '#123c4a', Contrata: '#16756f', 'Código del Trabajo': '#bd6b2e', Honorarios: '#7c8794' }
  check('pestanas_categoria_paleta_charts_y_contraste_aa', contrastePestanas.length === 7 && contrastePestanas.filter(item => item.activa).length === 4 && contrastePestanas.every(item => item.color_categoria === paletaCategoria[item.categoria] && item.razon_contraste >= 4.5 && item.radio === '999px') && new Set(contrastePestanas.slice(0, 4).map(item => item.fondo)).size === 4, contrastePestanas)
  await abrir('/estamento/Planta')
  await page.locator('.category-tabs').screenshot({ path: resolve(evidencia, '04b_pestanas_categorias_1440.png'), animations: 'disabled' })
  await page.setViewportSize({ width: 375, height: 812 })
  await page.locator('.category-tabs').screenshot({ path: resolve(evidencia, '04c_pestanas_categorias_375.png'), animations: 'disabled' })
  await page.setViewportSize({ width: 1440, height: 1000 })
  await abrir('/panel')
  const estilosSelectores = await page.locator('.select-inline').evaluateAll(nodes => nodes.map(node => {
    const estilo = getComputedStyle(node)
    const selector = node.querySelector('select')
    return { texto: node.textContent, fondo: estilo.backgroundColor, radio: estilo.borderRadius, selector_fondo: selector ? getComputedStyle(selector).backgroundColor : '', selector_radio: selector ? getComputedStyle(selector).borderRadius : '' }
  }))
  check('selectores_periodo_metrica_pildora_neutra_uniforme', estilosSelectores.length >= 4 && estilosSelectores.some(item => item.texto?.startsWith('Mes')) && estilosSelectores.some(item => item.texto?.startsWith('Métrica')) && new Set(estilosSelectores.map(item => item.fondo)).size === 1 && estilosSelectores.every(item => item.radio === '999px' && item.selector_radio === '999px' && item.selector_fondo === 'rgba(0, 0, 0, 0)'), estilosSelectores)
  await abrir('/estamento/Planta')
  const seccionAntiguedad = page.locator('section.data-section.two-columns').filter({ has: page.getByRole('heading', { name: 'Antigüedad: año de inicio' }) })
  const columnaAntiguedad = seccionAntiguedad.locator(':scope > div').nth(1)
  check('antiguedad_seis_iniciales_y_resto_colapsado', await columnaAntiguedad.locator('.simple-bars').first().locator('.bar-row').count() === 6 && await columnaAntiguedad.getByText(/Mostrar \d+ años restantes/).isVisible(), 'Seis años visibles y desplegable cerrado')
  await columnaAntiguedad.getByText(/Mostrar \d+ años restantes/).click()
  check('antiguedad_despliega_todos_los_anios', await columnaAntiguedad.locator('.simple-bars .bar-row').count() > 6, `${await columnaAntiguedad.locator('.simple-bars .bar-row').count()} años visibles tras abrir`)

  await verificarGraficoMovil('/panel', 'monthly-category')
  await verificarGraficoMovil('/estamento/Planta', 'monthly-estamento')
  await verificarGraficoMovil('/estamento/Contrata', 'monthly-estamento')
  await verificarGraficoMovil('/estamento/C%C3%B3digo%20del%20Trabajo', 'monthly-estamento')
  await verificarGraficoMovil('/estamento/Honorarios', 'monthly-estamento')
  await page.setViewportSize({ width: 1440, height: 1000 })

  await abrir('/ficha/PLT-2023-0032')
  const convencionD15 = page.locator('details.trajectory-convention')
  check('d15_banner_reemplazado_por_nota_desplegable', (await convencionD15.locator(':scope > summary').innerText()) === 'Convención de trayectoria D-15 — detalles' && !(await convencionD15.evaluate(node => node.open)), await convencionD15.locator(':scope > summary').innerText())
  await convencionD15.locator(':scope > summary').click()
  const fichaPlt = await page.locator('main').innerText()
  check('ficha_planta_encabezado_y_no_reconciliacion', fichaPlt.includes('CARO PARRA, CARMEN SALOME') && fichaPlt.includes('la suma de fichas no reconcilia con los agregados'), 'Encabezado y advertencia D-15 dentro del desplegable')
  const tarjetaTrayectoria = convencionD15.locator('details.glossary-card[data-term="Trayectoria (convención D-15)"]')
  await tarjetaTrayectoria.locator('summary').click()
  await tarjetaTrayectoria.screenshot({ path: resolve(evidencia, '08b_ficha_glosario_1440.png'), animations: 'disabled' })
  await tarjetaTrayectoria.locator('summary').click()
  const resumenPlt = await page.locator('.metrics-grid.three').innerText()
  check('ficha_planta_conteos_visibles', resumenPlt.includes('22') && resumenPlt.includes('14') && resumenPlt.includes('1'), resumenPlt)
  check('ficha_planta_36_meses_sin_imputar', await page.locator('.month-record').count() === 22 && await page.locator('.trajectory-absence').count() === 14, { publicados: await page.locator('.month-record').count(), ausencias: await page.locator('.trajectory-absence').count() })
  const huecosPlt = await page.locator('.trajectory-absence').evaluateAll(nodes => nodes.map(node => node.dataset.period))
  const esperadosHuecosPlt = []
  for (const anio of [2023, 2024, 2025]) for (let mes = 1; mes <= 12; mes++) {
    const periodo = `${anio}-${String(mes).padStart(2, '0')}`
    if ((periodo >= '2023-08' && periodo <= '2024-08') || periodo === '2024-12') esperadosHuecosPlt.push(periodo)
  }
  check('ficha_planta_huecos_exactos_y_septiembre_presente', JSON.stringify(huecosPlt) === JSON.stringify(esperadosHuecosPlt) && await page.locator('.month-record[data-period="2024-09"]').count() === 1, { esperados: esperadosHuecosPlt, interfaz: huecosPlt })
  await page.locator('.month-record[data-period="2024-11"] > summary').click()
  const alternaPlt = page.locator('.month-record[data-period="2024-11"] .alternate-publication')
  const textoAlternaPlt = await alternaPlt.innerText()
  check('ficha_planta_version_alterna_visible', textoAlternaPlt.includes('Otra publicación del mismo período') && textoAlternaPlt.includes('PLT-202411-8247F5515D') && textoAlternaPlt.includes('version_alterna') && textoAlternaPlt.includes('2024-12'), 'Versión alterna, seleccionada, rol y archivo nominal visibles')
  await alternaPlt.getByRole('button', { name: /Versión alterna de CARO PARRA/ }).click()
  const fuenteAlternaPlt = await dialogo.innerText()
  check('ficha_planta_fuente_alterna_trazable', fuenteAlternaPlt.includes('12_Planta_Diciembre_2024.csv') && fuenteAlternaPlt.includes('132') && fuenteAlternaPlt.includes('bad153e30fec298ba714282e3c60048fc44137a74cd4d47161f48cd72da8144f'), 'Diciembre de 2024, fila 132 y SHA-256')
  const trazabilidadAlternaDirecta = await alternaPlt.locator('.month-source').innerText()
  check('ficha_alterna_archivo_fila_sha_sin_desplegar', trazabilidadAlternaDirecta.includes('12_Planta_Diciembre_2024.csv') && trazabilidadAlternaDirecta.includes('132') && trazabilidadAlternaDirecta.includes('bad153e30fec298ba714282e3c60048fc44137a74cd4d47161f48cd72da8144f'), 'Trazabilidad alterna visible fuera de + indicadores')
  await page.getByRole('button', { name: 'Cerrar fuente' }).click()
  await alternaPlt.screenshot({ path: resolve(evidencia, '08_ficha_planta_alterna_1440.png'), animations: 'disabled' })
  const detallesPlt = (await page.locator('.record-detail').allInnerTexts()).join('\n')
  check('ficha_planta_sin_genero_ni_derivados', !/genero|género|primer_nombre|nombre_normalizado/i.test(detallesPlt), 'Detalles seleccionados y alternos sin género')
  const respuestaFichaPlt = await context.request.get(`${base}/data/fichas/PLT-2023-0032.json`)
  const jsonPlt = await respuestaFichaPlt.json()
  check('ficha_planta_json_http_y_campos_d15', respuestaFichaPlt.status() === 200 && jsonPlt.conteos.periodos_publicados === 22 && jsonPlt.trayectoria.find(e => e.periodo === '2024-11').versiones_alternas[0].version_alterna_de === 'PLT-202411-8247F5515D', { estado: respuestaFichaPlt.status(), periodos: jsonPlt.conteos.periodos_publicados })
  await page.locator('.month-record[data-period="2023-01"] > summary').click()
  const mesAsignaciones = page.locator('.month-record[data-period="2023-01"]')
  const textoMesAsignaciones = await mesAsignaciones.innerText()
  check('ficha_asignaciones_nombres_raw_y_duplicado_preservado', textoMesAsignaciones.includes('(39)(11)(10)(08)(07)(06)(04)(04)') && textoMesAsignaciones.includes('Incentivo Juez Policía Local') && textoMesAsignaciones.match(/Bono de subrogación/g)?.length === 2 && !textoMesAsignaciones.includes('[object Object]'), { ocurrencias_bono_subrogacion: textoMesAsignaciones.match(/Bono de subrogación/g)?.length, raw_visible: textoMesAsignaciones.includes('(39)(11)(10)(08)(07)(06)(04)(04)') })
  const camposPrimarios = ['estamento', 'cargo_funcion', 'grado_eus_jornada', 'calificacion_profesional', 'fecha_inicio', 'fecha_termino', 'asignaciones_decodificadas', 'remuneracion_bruta_clp', 'remuneracion_liquida_clp', 'viaticos_clp', 'horas_extra_horas_total']
  const primariosPresentes = await Promise.all(camposPrimarios.map(async campo => (await mesAsignaciones.locator(`.month-primary-facts [data-field="${campo}"]`).count()) === 1))
  const registroEneroPlt = jsonPlt.trayectoria.find(entry => entry.periodo === '2023-01').registro
  const trazabilidadEnero = await mesAsignaciones.locator('.month-source').innerText()
  const indicadoresAdicionales = mesAsignaciones.locator('.month-facts > .data-disclosure')
  check('ficha_campos_primarios_resto_plegado_y_fuente_siempre_visible', primariosPresentes.every(Boolean) && !(await indicadoresAdicionales.evaluate(node => node.open)) && (await indicadoresAdicionales.locator(':scope > summary').innerText()) === '+ indicadores' && trazabilidadEnero.includes(registroEneroPlt.fuente_archivo) && trazabilidadEnero.includes(String(registroEneroPlt.fuente_fila_csv)) && trazabilidadEnero.includes(registroEneroPlt.fuente_sha256), { campos: camposPrimarios.length, archivo: registroEneroPlt.fuente_archivo, fila: registroEneroPlt.fuente_fila_csv, sha256: registroEneroPlt.fuente_sha256 })
  await indicadoresAdicionales.locator(':scope > summary').click()
  check('ficha_indicadores_adicionales_disponibles', (await mesAsignaciones.locator('.month-additional-facts').innerText()).includes('Región del Biobío') && (await mesAsignaciones.locator('.month-source').isVisible()), 'Resto de campos desplegable; fuente permanece visible')
  await indicadoresAdicionales.locator(':scope > summary').click()
  await mesAsignaciones.locator('.month-primary-facts').screenshot({ path: resolve(evidencia, '08c_ficha_asignaciones_decodificadas_1440.png'), animations: 'disabled' })
  const entradaAsignaciones = glosarioJson.find(entry => entry.termino === 'Asignaciones especiales')
  const tarjetaAsignaciones = page.locator('.page-heading details.glossary-card[data-term="Asignaciones especiales"]')
  await tarjetaAsignaciones.locator('summary').click()
  const textoTarjetaAsignaciones = await tarjetaAsignaciones.innerText()
  check('ficha_glosario_asignaciones_limitacion_y_fuente_exactas', textoTarjetaAsignaciones.includes(entradaAsignaciones.definicion) && textoTarjetaAsignaciones.includes(entradaAsignaciones.fuente) && textoTarjetaAsignaciones.includes('no el monto de cada uno') && textoTarjetaAsignaciones.includes('remuneración bruta'), { definicion: entradaAsignaciones.definicion, fuente: entradaAsignaciones.fuente })
  await tarjetaAsignaciones.locator('summary').click()

  await abrir('/ficha/COT-2023-0015')
  const resumenCot = await page.locator('.metrics-grid.three').innerText()
  check('ficha_codigo_siete_periodos_y_ausencias', await page.locator('.month-record').count() === 7 && await page.locator('.trajectory-absence').count() === 29 && resumenCot.includes('7') && resumenCot.includes('29'), { publicados: await page.locator('.month-record').count(), ausencias: await page.locator('.trajectory-absence').count() })
  await page.locator('.month-record[data-period="2025-05"] > summary').click()
  const textoAlternaCot = await page.locator('.month-record[data-period="2025-05"] .alternate-publication').innerText()
  check('ficha_codigo_version_alterna_visible', textoAlternaCot.includes('COT-202505-8DA800BA00') && textoAlternaCot.includes('COT-202505-9D0CE3F70A') && textoAlternaCot.includes('periodo_contenido_distinto_de_periodo_nominal_archivo'), 'Selección de mayo y versión alterna de julio visibles')
  const detallesCot = (await page.locator('.record-detail').allInnerTexts()).join('\n')
  check('ficha_codigo_sin_genero_ni_derivados', !/genero|género|primer_nombre|nombre_normalizado/i.test(detallesCot), 'Detalles seleccionados y alternos sin género')
  check('ficha_codigo_estamento_estimado_individual', (await page.locator('.estimated-individual').innerText()).startsWith('Estimado:') && (await page.locator('.estimated-legend').innerText()) === meta.estamento_estimado.leyenda_fija, await page.locator('.estimated-individual').innerText())

  const respuestaFichaHon = await context.request.get(`${base}/data/fichas/HON-0593.json`)
  const jsonHon = await respuestaFichaHon.json()
  const primerPeriodoHon = jsonHon.trayectoria.find(entry => entry.registro)?.periodo
  await abrir('/ficha/HON-0593')
  await page.locator(`.month-record[data-period="${primerPeriodoHon}"] > summary`).click()
  const mesHon = page.locator(`.month-record[data-period="${primerPeriodoHon}"]`)
  const camposHon = await mesHon.locator('.month-primary-facts [data-field="tipo_pago"], .month-primary-facts [data-field="descripcion_pago"], .month-primary-facts [data-field="numero_cuotas"]').count()
  check('ficha_honorarios_tipo_descripcion_cuotas_primarios', camposHon === 3 && (await mesHon.locator('.month-source').innerText()).includes(jsonHon.trayectoria.find(entry => entry.periodo === primerPeriodoHon).registro.fuente_sha256), { id: 'HON-0593', periodo: primerPeriodoHon, campos: camposHon })

  await abrir('/ficha/COT-2023-0008')
  await page.locator('.month-record[data-period="2023-06"] > summary').click()
  const variante = page.locator('.month-record[data-period="2023-06"] .writing-variant')
  check('cargo_variante_escritura_inicia_colapsada', !(await variante.evaluate(node => node.open)) && (await variante.locator('summary').innerText()).includes('Variante de escritura'), 'JEFA DEPTO. GAB. PSICOTÉCNICO / PSICOTECNICO')
  await variante.locator('summary').click()
  const textoVariante = await variante.innerText()
  check('cargo_variante_conserva_grafias_y_normalizacion', textoVariante.includes('JEFA DEPTO. GAB. PSICOTECNICO') && textoVariante.includes('JEFA DEPARTAMENTO GABINETE PSICOTECNICO'), textoVariante)

  await abrir('/ficha/COT-2023-0001')
  await page.locator('.month-record[data-period="2025-08"] > summary').click()
  const posible = page.locator('.month-record[data-period="2025-08"]')
  check('cargo_posible_variante_requiere_verificacion', (await posible.locator('.cargo-review').innerText()) === 'Posible variante, requiere verificación' && (await posible.locator('.cargo-comparison').innerText()).includes('AUXILIAR DE SERVICIO') && (await posible.locator('.month-role').innerText()) === 'AUXILIAR DE SERVICIO CEMENTERIO', await posible.locator('.cargo-comparison').innerText())

  await abrir('/ficha/COT-2023-0005')
  await page.locator('.month-record[data-period="2025-02"] > summary').click()
  const cambio = page.locator('.month-record[data-period="2025-02"]')
  check('cargo_cambio_real_marcado_sin_fusion', (await cambio.locator('.cargo-change').innerText()).includes('Cambio de cargo') && (await cambio.locator('.month-role').innerText()) === 'MEDICO DIRECCIÓN DE TRANSITO' && await cambio.locator('.cargo-review').count() === 0, await cambio.locator('.month-role').innerText())

  await abrir('/metodologia')
  check('totales_metodologicos_con_fuente', await page.locator('table').first().locator('.source-button').count() === 5, 'Cuatro categorías y total general')
  check('metodologia_declara_no_reconciliacion_d15', (await page.locator('.absence-list').innerText()).includes('La suma de fichas no reconcilia') || (await page.locator('main').innerText()).includes('la suma de fichas no reconcilia'), 'Límite de reconciliación visible en metodología')
  const textoV011 = await page.getByTestId('iteration-v011').innerText()
  check('metodologia_normalizacion_candidata_no_integrada', textoV011.includes('31 fusiones') && textoV011.includes('Ninguna fusión está integrada') && textoV011.includes('pendiente de aprobación') && meta.version === 'modulo_personal_v1.4.0', { version_productiva: meta.version, estado: '31 candidatas; 0 integradas' })
  const enlaceControl = await page.getByRole('link', { name: /Control JSON/ }).getAttribute('href')
  const respuestaControl = await context.request.get(new URL(enlaceControl, page.url()).href)
  check('control_agregados_json_disponible', respuestaControl.status() === 200, { estado: respuestaControl.status() })
  const textoReutilizacion = await page.locator('.reuse-note').innerText()
  check('metodologia_atribucion_d18_y_licencias_d16', textoReutilizacion.includes('datos de transparencia activa del portal municipal') && textoReutilizacion.includes('Producto derivado:') && textoReutilizacion.includes('Portal de Transparencia Trazable') && textoReutilizacion.includes('MIT') && textoReutilizacion.includes('CC BY 4.0') && textoReutilizacion.includes('Ley 20.285') && !textoReutilizacion.includes('Portal de Transparencia Activa MU068') && !textoReutilizacion.includes('No hay una licencia'), textoReutilizacion)
  const ausenciaLicencia = ausenciasJson.find(row => row.dimension === 'licencia_reutilizacion')
  check('ausencias_licencia_coherente_con_d16', ausenciaLicencia?.estado === 'declarada_D16' && ausenciaLicencia.causa.includes('MIT') && ausenciaLicencia.causa.includes('CC BY 4.0') && ausenciaLicencia.causa.includes('no se atribuyen al municipio') && meta.licencias.decision === 'D-16', ausenciaLicencia)

  for (const [nombre, ruta, titulo] of rutas) {
    await page.setViewportSize({ width: 1440, height: 1000 })
    await abrir(ruta)
    check(`vista_${nombre}_desktop`, (await page.locator('h1').innerText()).includes(titulo), await page.locator('h1').innerText())
    await captura(`${String(rutas.findIndex(r => r[0] === nombre) + 1).padStart(2, '0')}_${nombre}_1440`)
    const anchoDesktop = await sinDesborde()
    check(`sin_desborde_${nombre}_1440`, anchoDesktop.documento <= 1441, anchoDesktop)
    await page.setViewportSize({ width: 375, height: 812 })
    await page.waitForTimeout(150)
    await captura(`${String(rutas.findIndex(r => r[0] === nombre) + 1).padStart(2, '0')}_${nombre}_375`)
    const anchoMovil = await sinDesborde()
    check(`sin_desborde_${nombre}_375`, anchoMovil.documento <= 376, anchoMovil)
  }

  for (const ancho of [768, 1024]) {
    await page.setViewportSize({ width: ancho, height: 900 })
    for (const [nombre, ruta] of rutas) {
      await abrir(ruta)
      const medidas = await sinDesborde()
      check(`sin_desborde_${nombre}_${ancho}`, medidas.documento <= ancho + 1, medidas)
    }
  }

  await page.setViewportSize({ width: 375, height: 812 })
  await abrir('/personal')
  await page.getByRole('button', { name: 'Abrir navegación' }).click()
  check('menu_movil_abre_y_navega', await page.getByRole('navigation', { name: 'Navegación del módulo' }).isVisible(), 'Botón de navegación a 375 px')
  await page.getByRole('link', { name: 'Panel general', exact: true }).click()
  await page.locator('h1', { hasText: 'La dotación completa' }).waitFor()
  await page.keyboard.press('Tab')
  const foco = await page.evaluate(() => { const e = document.activeElement; const s = e ? getComputedStyle(e) : null; return { elemento: e?.tagName, contorno: s?.outlineStyle, ancho: s?.outlineWidth, sombra: s?.boxShadow } })
  check('foco_visible_con_teclado', foco.contorno !== 'none' || foco.sombra !== 'none', foco)

  if (process.env.CHECK_DOCS === '1') {
    await abrir('/metodologia')
    const enlaces = await page.locator('.document-list a').evaluateAll(nodes => nodes.map(n => ({ texto: n.textContent, href: n.href })))
    const estadosDocs = []
    for (const enlace of enlaces) {
      const response = await context.request.get(enlace.href)
      estadosDocs.push({ documento: enlace.texto, estado: response.status(), bytes: (await response.body()).length })
    }
    check('documentacion_enlazada_disponible', estadosDocs.length === 10 && estadosDocs.every(d => d.estado === 200 && d.bytes > 100), estadosDocs)
  }

  check('cero_errores_de_consola', erroresConsola.length === 0, erroresConsola)
  check('cero_errores_de_ejecucion', erroresPagina.length === 0, erroresPagina)
  check('cero_respuestas_http_fallidas', respuestasFallidas.length === 0, respuestasFallidas)
  check('cero_solicitudes_fallidas', solicitudesFallidas.length === 0, solicitudesFallidas)
} catch (error) {
  controles.push({ control: 'ejecucion_completa', resultado: 'FALLA', evidencia: String(error.stack || error) })
  console.error(error)
} finally {
  const informe = {
    fecha_verificacion: new Date().toISOString(),
    base,
    build: 'dist/ servido como sitio estático',
    viewports: [375, 768, 1024, 1440],
    resumen: { controles: controles.length, aprobadas: controles.filter(c => c.resultado === 'APROBADO').length, fallas: controles.filter(c => c.resultado !== 'APROBADO').length },
    controles,
    errores_consola: erroresConsola,
    errores_pagina: erroresPagina,
    respuestas_fallidas: respuestasFallidas,
    solicitudes_fallidas: solicitudesFallidas,
  }
  writeFileSync(resolve(evidencia, 'verificacion_navegador.json'), JSON.stringify(informe, null, 2) + '\n', 'utf8')
  await browser.close()
  console.log(JSON.stringify(informe.resumen))
  if (informe.resumen.fallas) process.exitCode = 1
}
