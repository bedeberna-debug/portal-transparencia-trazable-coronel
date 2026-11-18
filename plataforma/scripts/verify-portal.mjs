import { chromium } from '@playwright/test'
import { existsSync } from 'node:fs'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const plataforma = resolve(fileURLToPath(new URL('..', import.meta.url)))
const raiz = resolve(plataforma, '..')
const evidencia = resolve(raiz, 'documentación/plataforma/evidencia')
const base = process.env.QA_BASE_URL || 'http://127.0.0.1:7100'
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
const browser = await chromium.launch({ headless: true })
const context = await browser.newContext({ viewport: { width: 1440, height: 1100 }, reducedMotion: 'reduce', locale: 'es-CL' })
const page = await context.newPage()
page.on('console', msg => { if (msg.type() === 'error') erroresConsola.push(msg.text()) })
page.on('pageerror', error => erroresPagina.push(error.message))
page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) respuestasFallidas.push({ estado: response.status(), url: response.url() }) })
page.on('requestfailed', request => { if (request.url().startsWith(base)) solicitudesFallidas.push({ url: request.url(), error: request.failure()?.errorText }) })
async function abrir(ruta) {
  await page.goto(`${base}/#${ruta}`, { waitUntil: 'networkidle' })
  await page.locator('h1').waitFor()
  await page.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0) })
}
async function sinDesborde() {
  return page.evaluate(() => ({ viewport: innerWidth, documento: document.documentElement.scrollWidth, cuerpo: document.body.scrollWidth }))
}
try {
  await abrir('/')
  check('portada_identidad_d18', await page.locator('h1').innerText() === 'Portal de Transparencia Trazable', await page.locator('h1').innerText())
  const tituloDocumento = await page.title()
  check('metadatos_identidad_d18', tituloDocumento === 'Portal de Transparencia Trazable — Municipalidad de Coronel', tituloDocumento)
  const escudo = page.locator('.brand-mark img')
  check('escudo_municipal_en_marca', await escudo.count() === 1 && await escudo.getAttribute('alt') === '' && await escudo.evaluate(imagen => imagen.complete && imagen.naturalWidth > 0), 'Escudo municipal visible en la marca y accesible desde su etiqueta')
  const textoPortada = await page.locator('body').innerText()
  check('fuente_producto_diferenciada', textoPortada.includes('datos de transparencia activa del portal municipal (MU068), Ley 20.285 e IGTA.') && !textoPortada.includes('Transparencia activa · 2023—2025'), 'Fuente MU068, Ley 20.285 e IGTA; rótulo ambiguo ausente')
  check('brujula_visible', textoPortada.includes('Toda cifra, perseguible hasta su fuente.') && textoPortada.includes('Toda ausencia, declarada.'), 'Brújula visible en portada')
  const modulos = page.locator('.portal-module')
  const estados = await modulos.locator('.module-status').allInnerTexts()
  check('seis_modulos_con_estados', await modulos.count() === 6 && estados[0] === 'DISPONIBLE' && estados[1].includes('SIGUIENTE') && estados.slice(2).every(estado => estado === 'EN DESARROLLO'), estados)
  const placeholders = modulos.locator('.module-placeholder-facts section')
  check('placeholders_activos_completos', await placeholders.count() === 15 && await modulos.nth(1).locator('.module-placeholder-facts section').count() === 3 && await modulos.locator('a').count() === 1, { secciones: await placeholders.count(), enlaces_en_tarjetas: await modulos.locator('a').count() })
  check('licencias_d16_visibles', textoPortada.includes('Código: MIT') && textoPortada.includes('CC-BY 4.0') && textoPortada.includes('Atribución: Portal de Transparencia Trazable — Municipalidad de Coronel.'), 'MIT, CC-BY 4.0 y atribución visibles')
  check('narrativa_no_publicada', !existsSync(resolve(plataforma, 'dist/docs/NARRATIVA_FUNDACIONAL_v1.md')), 'NARRATIVA_FUNDACIONAL_v1.md ausente de dist/docs')
  const enlacesVacios = await page.locator('a[href="#"], a[href=""]').count()
  check('sin_enlaces_muertos', enlacesVacios === 0, { enlaces_vacios: enlacesVacios })
  const medidas = []
  for (const width of [1440, 1024, 768, 375]) {
    await page.setViewportSize({ width, height: 1000 })
    await abrir('/')
    const medida = await sinDesborde()
    medidas.push(medida)
    if (width === 1440 || width === 375) await page.screenshot({ path: resolve(evidencia, `00_portal_${width}.png`), fullPage: true, animations: 'disabled' })
  }
  check('responsive_sin_desborde_horizontal', medidas.every(medida => medida.documento <= medida.viewport && medida.cuerpo <= medida.viewport), medidas)
  await page.setViewportSize({ width: 1440, height: 1000 })
  await abrir('/')
  await page.getByRole('link', { name: 'Explorar Personal y Remuneraciones' }).click()
  await page.getByRole('heading', { name: /Personas, contratos y remuneraciones/ }).waitFor()
  check('cta_abre_modulo_personal', page.url().includes('#/personal') && (await page.locator('h1').innerText()).includes('Personas, contratos y remuneraciones'), page.url())
  check('navegacion_interna_conservada', await page.locator('.main-nav .nav-link').count() === 5 && await page.locator('.glossary-global-note').count() === 1, { enlaces: await page.locator('.main-nav .nav-link').count() })
  await page.screenshot({ path: resolve(evidencia, 'coronel_personal_1440.png'), fullPage: true, animations: 'disabled' })
  await page.getByRole('link', { name: 'Panel general', exact: true }).click()
  await page.getByRole('link', { name: 'Inicio', exact: true }).click()
  await page.getByRole('heading', { name: /Personas, contratos y remuneraciones/ }).waitFor()
  check('inicio_modulo_vuelve_a_personal', page.url().includes('#/personal'), page.url())
  await page.getByRole('link', { name: 'Portal de Transparencia Trazable, portada' }).click()
  await page.getByRole('heading', { name: 'Portal de Transparencia Trazable', exact: true }).waitFor()
  check('marca_vuelve_a_portada', page.url().endsWith('#/') && await page.locator('h1').innerText() === 'Portal de Transparencia Trazable', page.url())
  await page.getByRole('link', { name: 'Actualizaciones', exact: true }).click()
  await page.getByRole('heading', { name: 'Actualizaciones de la plataforma', exact: true }).waitFor()
  const registroActualizaciones = await page.locator('.update-entry').allTextContents()
  check('actualizaciones_publica_v01', page.url().includes('#/actualizaciones') && registroActualizaciones.length === 1 && registroActualizaciones[0].includes('v0.1') && registroActualizaciones[0].includes('18 de noviembre de 2026') && registroActualizaciones[0].includes('Módulos afectados'), { entradas: registroActualizaciones.length })
  await page.screenshot({ path: resolve(evidencia, 'coronel_actualizaciones_1440.png'), fullPage: true, animations: 'disabled' })
  await page.setViewportSize({ width: 375, height: 812 })
  await abrir('/actualizaciones')
  await page.screenshot({ path: resolve(evidencia, 'coronel_actualizaciones_375.png'), fullPage: true, animations: 'disabled' })
  await page.setViewportSize({ width: 768, height: 1000 })
  await abrir('/personal')
  await page.getByRole('button', { name: 'Abrir navegación' }).click()
  check('menu_personal_768_abre', await page.locator('.main-nav.open').count() === 1 && await page.getByRole('link', { name: 'Inicio', exact: true }).isVisible() && await page.getByRole('link', { name: 'Metodología y fuentes', exact: true }).isVisible(), 'Navegación completa de Personal visible a 768 px')
  await page.screenshot({ path: resolve(evidencia, 'coronel_menu_personal_768.png'), fullPage: false, animations: 'disabled' })
  await page.getByRole('link', { name: 'Inicio', exact: true }).click()
  check('menu_personal_768_cierra', await page.locator('.main-nav.open').count() === 0, 'Menú de Personal cerrado tras seleccionar Inicio')
  await page.setViewportSize({ width: 375, height: 812 })
  await abrir('/')
  await page.getByRole('button', { name: 'Abrir navegación' }).click()
  check('menu_movil_abre', await page.locator('.main-nav.open').count() === 1 && await page.getByRole('link', { name: 'Personal y Remuneraciones', exact: true }).isVisible(), 'Menú y acceso a Personal visibles')
  await page.getByRole('link', { name: 'Personal y Remuneraciones', exact: true }).click()
  await page.locator('h1').waitFor()
  check('menu_movil_navega_y_cierra', page.url().includes('#/personal') && await page.locator('.main-nav.open').count() === 0, page.url())
  const recursos = await page.evaluate(() => performance.getEntriesByType('resource').map(recurso => ({ nombre: recurso.name, bytes: recurso.encodedBodySize || 0 })))
  check('cero_errores_consola_y_red', erroresConsola.length === 0 && erroresPagina.length === 0 && respuestasFallidas.length === 0 && solicitudesFallidas.length === 0, { erroresConsola, erroresPagina, respuestasFallidas, solicitudesFallidas })
  const resultado = {
    fecha: new Date().toISOString(),
    base,
    aprobadas: controles.filter(control => control.resultado === 'APROBADO').length,
    total: controles.length,
    controles,
    erroresConsola,
    erroresPagina,
    respuestasFallidas,
    solicitudesFallidas,
    rendimiento: { solicitudes: recursos.length, bytes_codificados: recursos.reduce((suma, recurso) => suma + recurso.bytes, 0) },
  }
  writeFileSync(resolve(evidencia, 'verificacion_portal.json'), JSON.stringify(resultado, null, 2), 'utf8')
  if (controles.some(control => control.resultado === 'FALLA')) process.exitCode = 1
} finally {
  await browser.close()
}
