import { chromium } from '@playwright/test'
import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const raiz = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const evidencia = resolve(raiz, '..', 'documentación', 'plataforma', 'evidencia')
const base = process.env.QA_BASE_URL ?? 'http://127.0.0.1:7100'
await mkdir(evidencia, { recursive: true })

const navegador = await chromium.launch({ headless: true })
const pagina = await navegador.newPage()
const resultados = []
const errores = { consola: [], pagina: [], red: [] }
let vistaActual = 'inicio'

pagina.on('console', mensaje => {
  if (mensaje.type() === 'error') errores.consola.push({ vista: vistaActual, texto: mensaje.text() })
})
pagina.on('pageerror', error => errores.pagina.push({ vista: vistaActual, texto: error.message }))
pagina.on('requestfailed', solicitud => errores.red.push({ vista: vistaActual, url: solicitud.url(), error: solicitud.failure()?.errorText }))
pagina.on('response', respuesta => {
  if (respuesta.status() >= 400) errores.red.push({ vista: vistaActual, url: respuesta.url(), estado: respuesta.status() })
})

function control(nombre, condicion, detalle) {
  resultados.push({ control: nombre, ok: Boolean(condicion), detalle })
}

async function abrir(ruta, width, sufijo = '') {
  vistaActual = `${ruta}${sufijo} · ${width}`
  await pagina.setViewportSize({ width, height: width === 375 ? 812 : 1000 })
  await pagina.goto(`${base}/#${ruta}${sufijo}`, { waitUntil: 'networkidle' })
  await pagina.evaluate(() => document.fonts.ready)
  await pagina.locator('main').waitFor({ state: 'visible' })
}

async function estadoVisual() {
  return pagina.evaluate(() => {
    const shell = document.querySelector('.site-shell')
    if (!(shell instanceof HTMLElement)) return { error: 'No existe .site-shell' }
    const css = getComputedStyle(shell)
    const fuente = document.querySelector('.source-button')
    const institucion = document.querySelector('.institution-bar')
    const textoInstitucion = document.querySelector('.institution-inner span')
    const header = document.querySelector('.main-header')
    const headerInner = document.querySelector('.header-inner')
    const navLink = document.querySelector('.nav-link')
    const marca = document.querySelector('.brand strong')
    const subtitulo = document.querySelector('.brand small')
    const footer = document.querySelector('.site-footer')
    const textoFooter = document.querySelector('.footer-license p')
    const hero = document.querySelector('.portal-hero')
    const tituloHero = document.querySelector('.portal-hero h1')
    const texturas = [...document.querySelectorAll('.local-texture')]
    return {
      laboratorios: document.querySelectorAll('.theme-lab').length,
      temaMuestra: shell.getAttribute('data-tema-muestra'),
      vistaMuestra: shell.getAttribute('data-vista-muestra'),
      variables: {
        background: css.getPropertyValue('--background').trim(),
        surface: css.getPropertyValue('--surface').trim(),
        ink: css.getPropertyValue('--p-ink').trim(),
        accent: css.getPropertyValue('--accent').trim(),
        trace: css.getPropertyValue('--trace-ink').trim(),
        traceSolid: css.getPropertyValue('--trace-solid').trim(),
      },
      fondoBody: getComputedStyle(document.body).backgroundColor,
      fondoInstitucion: institucion ? getComputedStyle(institucion).backgroundColor : null,
      textoInstitucion: textoInstitucion ? getComputedStyle(textoInstitucion).color : null,
      hero: hero ? {
        altura: hero.getBoundingClientRect().height,
        fondo: getComputedStyle(hero).backgroundColor,
        titulo: tituloHero ? getComputedStyle(tituloHero).color : null,
      } : null,
      chrome: {
        posicion: header ? getComputedStyle(header).position : null,
        altura: headerInner?.getBoundingClientRect().height,
        navAltura: navLink ? parseFloat(getComputedStyle(navLink).minHeight) : 0,
        navRadio: navLink ? getComputedStyle(navLink).borderRadius : null,
        marca: marca ? getComputedStyle(marca).fontSize : null,
        subtitulo: subtitulo ? getComputedStyle(subtitulo).fontSize : null,
        footer: textoFooter ? getComputedStyle(textoFooter).fontSize : null,
        footerFondo: footer ? getComputedStyle(footer).backgroundColor : null,
      },
      texturas: texturas.map(textura => ({
        opacidad: Number(getComputedStyle(textura).opacity),
        puntero: getComputedStyle(textura).pointerEvents,
        oculta: textura.getAttribute('aria-hidden'),
        svg: textura.querySelectorAll('svg').length,
        detalles: [...textura.querySelectorAll('.texture-detail')].map(detalle => getComputedStyle(detalle).display),
      })),
      fuente: fuente ? {
        texto: getComputedStyle(fuente).color,
        fondo: getComputedStyle(fuente).backgroundColor,
        borde: getComputedStyle(fuente).borderTopColor,
      } : null,
      categorias: [...document.querySelectorAll('.category-tabs a')].map(enlace => getComputedStyle(enlace).getPropertyValue('--category-color').trim()),
      tipografia: {
        cuerpo: getComputedStyle(document.body).fontFamily,
        titulo: document.querySelector('h1') ? getComputedStyle(document.querySelector('h1')).fontFamily : null,
      },
      metaTema: document.querySelector('meta[name="theme-color"]')?.getAttribute('content'),
      overflow: { documento: document.documentElement.scrollWidth, viewport: innerWidth },
    }
  })
}

function luminancia(rgb) {
  const valores = rgb.match(/[\d.]+/g)?.slice(0, 3).map(Number) ?? []
  const [r, g, b] = valores.map(v => {
    const c = v / 255
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

function contraste(rgbTexto, rgbFondo) {
  const a = luminancia(rgbTexto)
  const b = luminancia(rgbFondo)
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)
}

try {
  const estados = {}
  for (const ruta of ['/', '/panel']) {
    const vista = ruta === '/' ? 'portada' : 'panel'
    for (const width of [1440, 375]) {
      await abrir(ruta, width)
      const estado = await estadoVisual()
      estados[`${vista}-${width}`] = estado
      await pagina.screenshot({ path: resolve(evidencia, `tema-coronel_${vista}_${width}.png`), fullPage: true, animations: 'disabled' })
      control(`Tema Coronel definitivo: ${vista}-${width}`,
        estado.variables.background === '#fdfbf6' && estado.variables.surface === '#fffefa' && estado.variables.ink === '#182634' && estado.variables.accent === '#143d6d' && estado.variables.trace === '#8a5a0b' && estado.variables.traceSolid === '#c98a1e',
        estado.variables)
      control(`Sin laboratorio ni atributos: ${vista}-${width}`, estado.laboratorios === 0 && estado.temaMuestra === null && estado.vistaMuestra === null, estado)
      control(`Fondo, azul atenuado y metadatos: ${vista}-${width}`, estado.fondoBody === 'rgb(253, 251, 246)' && estado.fondoInstitucion === 'rgb(20, 61, 109)' && estado.metaTema === '#143d6d', estado)
      const contrasteAzul = contraste(estado.textoInstitucion, estado.fondoInstitucion)
      control(`Contraste AA del azul atenuado: ${vista}-${width}`, contrasteAzul >= 4.5, { texto: estado.textoInstitucion, fondo: estado.fondoInstitucion, contraste: Number(contrasteAzul.toFixed(2)) })
      control(`Chrome compacto y píldoras táctiles: ${vista}-${width}`,
        estado.chrome.posicion === 'sticky' && Math.abs(estado.chrome.altura - 64) < 1 && estado.chrome.navAltura >= 44 && estado.chrome.navRadio === '999px' && estado.chrome.marca === (width === 375 ? '16px' : '17.6px') && estado.chrome.subtitulo === '12.48px' && estado.chrome.footer === '12.48px' && estado.chrome.footerFondo === 'rgb(24, 38, 52)',
        estado.chrome)
      const opacidadEsperada = width === 375 ? 0.06 : 0.08
      control(`Texturas SVG subordinadas y no interactivas: ${vista}-${width}`,
        estado.texturas.length === 2 && estado.texturas.every(textura => textura.opacidad === opacidadEsperada && textura.puntero === 'none' && textura.oculta === 'true' && textura.svg === 1 && (width !== 375 || textura.detalles.every(display => display === 'none'))),
        estado.texturas)
      control(`Sin desborde horizontal: ${vista}-${width}`, estado.overflow.documento <= estado.overflow.viewport, estado.overflow)
      control(`Tipografías conservadas: ${vista}-${width}`, estado.tipografia.cuerpo.includes('Source Sans 3') && estado.tipografia.titulo?.includes('Source Serif 4'), estado.tipografia)
      if (estado.hero) {
        const contrasteHero = contraste(estado.hero.titulo, estado.hero.fondo)
        control(`Héroe bajo y contraste del título: ${vista}-${width}`, estado.hero.fondo === 'rgb(20, 61, 109)' && contrasteHero >= 4.5 && (width === 375 || estado.hero.altura <= 360), { ...estado.hero, contraste: Number(contrasteHero.toFixed(2)) })
      }
      if (estado.fuente) {
        const ratio = contraste(estado.fuente.texto, estado.fuente.fondo)
        control(`Trazabilidad cobre destacada y contraste AA: ${vista}-${width}`, estado.fuente.texto === 'rgb(138, 90, 11)' && estado.fuente.borde === 'rgb(201, 138, 30)' && estado.fuente.fondo === 'rgb(247, 237, 216)' && ratio >= 4.5, { ...estado.fuente, contraste: Number(ratio.toFixed(2)) })
      }
    }
    control(`Categorías funcionales conservadas: ${vista}`, JSON.stringify(estados[`${vista}-1440`].categorias) === JSON.stringify(estados[`${vista}-375`].categorias), estados[`${vista}-1440`].categorias)

    await abrir(ruta, 1440, '?tema=b')
    const conParametroB = await estadoVisual()
    control(`Parámetro histórico tema=b inerte: ${vista}`, JSON.stringify(conParametroB.variables) === JSON.stringify(estados[`${vista}-1440`].variables) && conParametroB.laboratorios === 0 && conParametroB.temaMuestra === null, conParametroB)
  }

  for (const ruta of ['/personal', '/explorador', '/estamento/Planta', '/actualizaciones', '/metodologia']) {
    await abrir(ruta, 375)
    const estado = await estadoVisual()
    control(`Tema Coronel global y sin laboratorio: ${ruta}`, estado.variables.background === '#fdfbf6' && estado.variables.accent === '#143d6d' && estado.laboratorios === 0 && estado.temaMuestra === null && estado.overflow.documento <= estado.overflow.viewport, estado)
  }

  control('Sin errores de consola', errores.consola.length === 0, errores.consola)
  control('Sin excepciones de página', errores.pagina.length === 0, errores.pagina)
  control('Sin respuestas o solicitudes fallidas', errores.red.length === 0, errores.red)
} catch (error) {
  control('Ejecución completada', false, error instanceof Error ? error.stack : String(error))
} finally {
  await navegador.close()
}

const informe = {
  fecha: new Date().toISOString(),
  base,
  resumen: { total: resultados.length, correctos: resultados.filter(r => r.ok).length, fallos: resultados.filter(r => !r.ok).length },
  resultados,
}
await writeFile(resolve(evidencia, 'verificacion_tema_coronel.json'), `${JSON.stringify(informe, null, 2)}\n`, 'utf8')
console.log(JSON.stringify(informe.resumen))
for (const fallo of resultados.filter(r => !r.ok)) console.error(JSON.stringify(fallo))
if (informe.resumen.fallos > 0) process.exitCode = 1
