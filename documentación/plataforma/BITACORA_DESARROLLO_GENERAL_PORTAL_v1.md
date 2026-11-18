# Bitácora de desarrollo general — Portal de Transparencia Trazable

**Versión documental:** v1 · 17-11-2026  
**Responsabilidad:** portada, shell de navegación, presentación de módulos y preparación de despliegue.  
**Estado:** v0.1 local preparada para revisión en círculo cerrado; **sin despliegue público, sin remoto y sin commits**.  
**Frontera aplicada:** no se modificaron las vistas internas ni los datos del módulo Personal y Remuneraciones.

---

## 1. Insumos vinculantes y alcance

Se leyeron y aplicaron `gobernanza/registro_de_decisiones.md`, `diseño/GLOSARIO_DEFINICIONES_v1.md` y `documentación/plataforma/BITACORA_CONSTRUCCION_MODULO_PERSONAL_v1.md`.

| Decisión | Aplicación |
|---|---|
| D-05 | La portada declara la reutilización estructurada y conserva el acceso a datos y fuentes del módulo disponible. |
| D-11 modificada | Personal aparece disponible; Normativa y Estructura Organizacional es el siguiente eje; Presupuesto y los demás módulos son placeholders activos. |
| D-16 | El pie declara código MIT y datos agregados/artefactos derivados CC-BY 4.0 con atribución. Se añadieron `LICENSE` y `LICENSE-DATA.md`. |
| D-18 | Portada, marca, barra institucional y metadatos usan “Portal de Transparencia Trazable”; la transparencia activa se presenta como fuente, no como nombre del producto. |
| D-19 | El repositorio y el flujo de GitHub Pages quedaron preparados, pero no se creó remoto ni se ejecutó despliegue. El flujo es exclusivamente manual. |
| D-20 | El Tema C seleccionado tras SC-08 es el sistema visual definitivo: papel cálido, tinta oscura, azul institucional y cobre reservado para trazabilidad. |

La estética conserva Source Sans 3 y Source Serif 4, así como la paleta funcional de categorías y gráficos de Personal. La muestra comparativa SC-08 y la posterior adopción del Tema C se documentan en las secciones 12 y 13.

## 2. Compuerta de narrativa fundacional

Se creó `documentación/plataforma/NARRATIVA_FUNDACIONAL_v1.md` con las secciones requeridas:

- necesidad observada;
- motivación personal;
- propósito de bien público;
- método;
- invitación a fiscalizar;
- alcance y continuidad;
- registro de compuerta.

El 17-11-2026 el propietario aprobó el texto de motivación personal. Se incorporó verbatim entre “Necesidad observada” y “Propósito de bien público”, sin reescritura ni contenido inferido. En el registro se marcó únicamente la casilla de motivación personal; la aprobación de la narrativa completa, la autorización de fragmentos publicables y la identificación de la versión de publicación siguen pendientes.

**Controles de no publicación:**

1. El documento está fuera de `plataforma/docs/` y no se copia a `dist/`.
2. La verificación de navegador comprobó que `dist/docs/NARRATIVA_FUNDACIONAL_v1.md` no existe.
3. `.gitignore` excluye expresamente el archivo para evitar que una futura publicación del repositorio eluda la compuerta; `git check-ignore` confirmó la regla.
4. La portada no reproduce la narrativa bajo compuerta.

La aprobación de la motivación no abre la compuerta. La publicación de cualquier fragmento requiere una aprobación expresa adicional del propietario.

## 3. Portada y estructura de rutas

Se añadió `plataforma/src/pages/PortalHome.tsx` y la hoja `plataforma/src/portal.css`. La portada presenta identidad, fuente, brújula, módulos y criterios de lectura sin inventar cifras agregadas ni estados de avance.

| Ruta | Contenido | Intervención |
|---|---|---|
| `/` | Nueva portada general del portal | Nueva |
| `/personal` | Portada existente de Personal y Remuneraciones | Solo cambió su ruta de entrada |
| `/panel` | Vista interna de Personal | Sin cambios |
| `/explorador` | Vista interna de Personal | Sin cambios |
| `/estamento/:categoria` | Vista interna de Personal | Sin cambios |
| `/ficha/:id` | Vista interna de Personal | Sin cambios |
| `/metodologia` | Vista interna de Personal | Sin cambios |

`plataforma/src/components/Layout.tsx` cambia la marca y el pie a shell global. Dentro de Personal conserva los cuatro accesos internos y la leyenda global del glosario; en la portada general ofrece acceso al módulo disponible.

En `plataforma/scripts/verify-modulo.mjs` solo se actualizó la URL de entrada de la portada de Personal desde `/` hacia `/personal`. No se alteraron sus afirmaciones funcionales, sus datos ni sus criterios de aceptación.

## 4. Presentación de módulos

La portada contiene seis presentaciones. Personal es la única tarjeta con enlace de entrada. Los módulos futuros no muestran botones ni enlaces ficticios.

| Módulo | Estado visible | Contenido activo del placeholder |
|---|---|---|
| Personal y Remuneraciones | Disponible | Preguntas, fuente CSV mensual, cobertura 2023—2025 y acceso al módulo. |
| Normativa y Estructura Organizacional | Siguiente · en desarrollo | Potestades, normas, unidades y funciones; fuentes oficiales; especificación, saneamiento, vinculación y revisión TP-19 pendientes. |
| Información Presupuestaria | En desarrollo | Ingresos, gastos y partidas; ESP/BEP; especificación e integración visual pendientes. |
| Transferencias de fondos | En desarrollo | Destinatarios, instrumentos y rendiciones; inventario, especificación y trazabilidad pendientes. |
| Trámites ante el organismo | En desarrollo | Requisitos, plazos y canales; inventario, vigencia, enlaces y especificación pendientes. |
| Juntas de Vecinos · Ley 21.146 | En desarrollo | Información municipal y relación con el organismo; alcance, fuentes, privacidad y especificación pendientes. |

Cada placeholder futuro presenta de forma visible tres bloques: **preguntas que responderá, fuente prevista y qué falta**. La verificación contó 15 bloques para los cinco módulos no disponibles.

## 5. Corrección D-18 y reporte al módulo Personal

### Shell corregido

- Se reemplazó “Transparencia activa · 2023—2025” por una declaración de fuente: MU068, Ley 20.285 e IGTA.
- La marca ya no presenta Personal como producto principal: ahora es “Portal de Transparencia Trazable — Municipalidad de Coronel”.
- `plataforma/index.html` actualizó título, descripción y color de tema.
- La portada declara: “datos de transparencia activa del portal municipal (MU068), Ley 20.285 e IGTA”.
- No quedan en el shell ocurrencias del encabezado ambiguo “Transparencia activa 2023-2025” ni equivalentes.

### Ocurrencias internas reportadas, no modificadas

1. `plataforma/src/pages/Metodologia.tsx`, sección “Cómo citar”, contiene “Portal de Transparencia Activa MU068”. La ocurrencia nombra la fuente y no un encabezado de producto; se reporta para revisión terminológica del chat propietario.
2. La misma página interna declara que no existe licencia aprobada. Ese texto quedó desactualizado frente a D-16 y debe corregirlo el chat de Personal.
3. La ausencia de licencia se alimenta además desde `plataforma/data/ausencias.json`; no se modificó ese dato ni su presentación interna.

El pie global sí aplica D-16 en todas las rutas, sin usar esa corrección para encubrir la inconsistencia interna reportada.

## 6. Licencias y repositorio

Se añadieron:

- `LICENSE`: texto MIT.
- `LICENSE-DATA.md`: alcance CC-BY 4.0, atribución y distinción respecto de los datos municipales de origen.
- `.gitignore`: exclusión de dependencias, builds, datos de trabajo, evidencia local y narrativa bajo compuerta.
- `plataforma/README.md`: arquitectura, rutas, build, verificación, licencias y compuerta de despliegue.
- `.github/workflows/deploy-pages.yml`: instalación limpia, build, verificación de paquete, auditoría y despliegue manual a Pages.

El pie enlaza los textos oficiales de MIT y CC-BY 4.0 y muestra la atribución “Portal de Transparencia Trazable — Municipalidad de Coronel”.

**Estado Git comprobado:** repositorio local inicializado, rama `main`, sin commits y sin remoto. No se ejecutó `git push`, no se creó un repositorio GitHub y no se ejecutó el flujo de Pages.

## 7. Build reproducible e integridad

Se comprobó una instalación limpia y la compilación posterior:

```bash
npm ci
npm run build
npm run verify:package
```

**Resultado:** correcto con Node.js 24 y Vite 7.3.8. El build genera `dist/`, copia datos, fuentes y documentos y crea `.nojekyll`.

Durante la primera instalación limpia, Windows mantuvo bloqueados archivos nativos de esbuild/Rollup dejados por el servidor temporal. Se cerró solamente el proceso esbuild asociado al workspace y se aisló el directorio residual dentro de `plataforma/`; la instalación limpia posterior terminó correctamente. El archivo `plataforma/.rollup-bloqueado.tmp/rollup.win32-x64-msvc.node` permanece bloqueado por Windows y no pudo eliminarse mediante los comandos normales intentados. El directorio está excluido de Git, no forma parte de `dist/` y no contiene código fuente ni datos del proyecto. No se usaron privilegios elevados ni se modificó el sistema; su eliminación local queda pendiente de que el sistema libere el archivo.

Resultado de `verify-package.mjs`:

- 18 JSON raíz y 1.068 fichas: **1.086 JSON** con hashes válidos.
- 144 CSV originales y copias con SHA-256 coincidente.
- 69/69 controles de agregados aprobados.
- `.nojekyll` presente e idioma HTML `es-CL` válido.
- 22.940 registros totales y 22.938 en proyección de trayectoria, sin cambios.
- Resultado global **APROBADO**.

Vite mantiene una advertencia no bloqueante por el chunk JavaScript principal de 806,82 kB. No se declaró una optimización que no se realizó.

## 8. Verificación visual y funcional

Se añadió `plataforma/scripts/verify-portal.mjs` para el shell. Resultado final: **16/16 controles aprobados**.

Cobertura:

- identidad D-18 en H1 y metadatos;
- diferenciación entre producto y fuente;
- brújula visible;
- seis módulos y sus estados;
- 15 bloques de placeholders activos;
- licencias y atribución;
- narrativa ausente del paquete;
- ausencia de enlaces vacíos;
- navegación portada → Personal → portada;
- navegación interna conservada;
- menú móvil y cierre al navegar;
- 375, 768, 1024 y 1440 px sin desplazamiento horizontal;
- cero errores de consola, ejecución, solicitudes y respuestas HTTP fallidas.

Las capturas `00_portal_1440.png` y `00_portal_375.png` fueron revisadas visualmente. No se detectaron defectos de jerarquía, legibilidad, contenido o composición que exigieran una nueva iteración.

La suite de Personal volvió a pasar **124/124 controles** tras la integración. La verificación del paquete confirmó además los 69 controles de agregados y la integridad documental. Evidencia local:

- `documentación/plataforma/evidencia/verificacion_portal.json`;
- `documentación/plataforma/evidencia/verificacion_navegador.json`;
- `documentación/plataforma/evidencia/verificacion_paquete.json`;
- capturas PNG del portal y del módulo.

## 9. Reporte de vulnerabilidades npm

### Secuencia ejecutada

1. `npm audit` inicial: **16 vulnerabilidades** —1 baja, 3 moderadas y 12 altas— con corrección no forzada disponible.
2. Dos ejecuciones de `npm audit fix`, **sin `--force`**, seguidas de build.
3. Verificación final mediante `npm audit --omit=dev` y `npm audit`.

### Resultado final

| Alcance | Resultado |
|---|---|
| Dependencias de producción (`npm audit --omit=dev`) | **0 vulnerabilidades conocidas** |
| Árbol completo, incluidas herramientas de desarrollo (`npm audit`) | **18 incidencias altas** |

Las 18 incidencias restantes corresponden a rutas de dependencia afectadas por la misma alerta de `picomatch`: **GHSA-fc5q-39xc-vjpf**, ReDoS mediante extglobs de una sola rama repetidos. npm solo ofrece como resolución automática `npm audit fix --force`, con instalación de Vite 6.2.7 y cambio incompatible. **No se ejecutó.**

El build de producción y la revisión funcional terminaron correctamente, pero eso no elimina ni resuelve la alerta de desarrollo. La autorización de despliegue debe considerar explícitamente este resultado y reevaluar el reporte vigente en esa fecha.

## 10. Reglas de código y límites

La revisión acotada de los archivos modificados del shell terminó sin errores:

```bash
npx eslint src/App.tsx src/components/Layout.tsx src/pages/PortalHome.tsx src/main.tsx
```

`npm run lint` completo conserva **15 errores preexistentes** en componentes internos o de plantilla: exportaciones incompatibles con Fast Refresh, una impureza en `components/ui/sidebar.tsx` y actualizaciones de estado dentro de efectos en vistas internas. No se modificaron esos archivos por la frontera de propiedad. Estos errores no impidieron la compilación ni las pruebas de navegador, pero quedan como deuda técnica declarada.

## 11. Compuerta de despliegue

El flujo `.github/workflows/deploy-pages.yml` solo tiene el disparador `workflow_dispatch`. Prepara el mismo paquete estático, verifica integridad y emite auditorías antes del paso de Pages.

**No autorizado ni realizado en esta iteración:**

- creación de repositorio remoto;
- commit o push;
- activación o ejecución de GitHub Pages;
- difusión pública de una URL;
- publicación de narrativa fundacional.

Antes de una ejecución autorizada se debe:

1. revisar y aprobar la narrativa si se pretende publicarla, incluida la motivación personal escrita o aprobada por el propietario;
2. resolver o aceptar explícitamente el reporte npm vigente, sin ocultar las incidencias de desarrollo;
3. coordinar la corrección interna de licencia en Metodología con el chat de Personal;
4. repetir build, verificación de paquete y pruebas de navegador sobre el estado exacto a publicar;
5. ejecutar el flujo manual solo con autorización expresa y coordinación del propietario.

---

## 12. SC-08 — muestra comparativa de tema, fase de decisión

**Fecha:** 17-11-2026.  
**Estado:** fase cerrada; el propietario seleccionó posteriormente el Tema C, implementado conforme a D-20 y documentado en la sección 13.  
**Alcance:** portada `/` y Panel general `/panel`, a 1440 y 375 px. No se modificaron `Panel.tsx`, `Charts.tsx`, datos, lógica de visualización ni vistas internas adicionales.

### Implementación temporal y retiro

- `src/components/Layout.tsx` incorporó el conmutador “SC-08 · Muestra provisional · solo desarrollo”, con **Tema actual**, **Tema B** y **Tema C**. Usó `useSearchParams`, conservó los demás parámetros y expuso `aria-pressed`; los tres botones midieron al menos 44 px de alto.
- La muestra solo se habilitó con `import.meta.env.DEV` y en `/` o `/panel`. Los valores fueron `#/?tema=b`, `#/?tema=c`, `#/panel?tema=b` y `#/panel?tema=c`.
- `.site-shell` recibió `data-tema-muestra="b|c"` y `data-vista-muestra="portal|panel"` únicamente en ese contexto. “Tema actual” eliminó el parámetro y el atributo.
- `src/main.tsx` importó `src/sc08.css` después de las hojas existentes. Toda la muestra cromática quedó aislada en esa hoja.
- El build de producción no mostró el conmutador ni aplicó los atributos, incluso con querystring. Se comprobó sobre `dist/` en portada y Panel con ambos valores.

### Variables base modificadas por cada muestra

| Variable | Tema B | Tema C |
|---|---|---|
| `--p-ink` | `#151e32` | `#182634` |
| `--p-brand-deep` | `#0b1120` | no se añadió |
| `--p-teal` | `#4f46e5` | `#155bb5` |
| `--p-paper` | `#f4f6fa` | `#fdfbf6` |
| `--p-line` | `#d7ddea` | `#ddd6c8` |
| `--background` | `#f4f6fa` | `#fdfbf6` |
| `--surface` | `#fbfcfe` | `#fffefa` |
| `--surface-muted` | `#eef1f7` | `#f3efe5` |
| `--text` | `#151e32` | `#182634` |
| `--text-secondary` | `#46536b` | `#4c5a64` |
| `--accent` | `#4f46e5` | `#155bb5` |
| `--accent-dark` | `#4338ca` | `#104b94` |
| `--border` | `#d7ddea` | `#ddd6c8` |

B reservó `#151e32` y `#0b1120` para marca/encabezados; el fondo general de lectura permaneció claro. C usó papel cálido y azul institucional en barra, marca y hero. Ninguna muestra cambió `--font-body` ni `--font-display`: se conservaron Source Sans 3 y Source Serif 4.

### Variables provisionales de apoyo

Todas llevaron prefijo `sc08` para distinguirlas del sistema definitivo.

| Variable | Tema B | Tema C |
|---|---|---|
| `--sc08-chrome` | `#151e32` | `#155bb5` |
| `--sc08-hero-bg` | `#151e32` | `#155bb5` |
| `--sc08-hero-surface` | `#202b46` | `#1c64ba` |
| `--sc08-hero-border` | `#56627b` | `#8eb4dd` |
| `--sc08-hero-accent` | `#c7d2fe` | `#e8f1fb` |
| `--sc08-on-dark` | `#f4f6fa` | `#fdfbf6` |
| `--sc08-on-dark-secondary` | `#cbd3e2` | `#d9e5f3` |
| `--sc08-dark-link` | `#e0e7ff` | `#e8f1fb` |
| `--sc08-trace` | `#4338ca` | `#8a5a0b` |
| `--sc08-trace-solid` | no se añadió | `#c98a1e` |
| `--sc08-trace-bg` | `#eef0ff` | `#f7edd8` |
| `--sc08-trace-bg-hover` | `#e0e4ff` | `#f1e0bd` |
| `--sc08-trace-border` | `#a5b4fc` | `#c98a1e` |
| `--sc08-trace-border-on-dark` | `#a5b4fc` | `#c98a1e` |
| `--sc08-available-bg` | `#e9eafb` | `#e7eef8` |
| `--sc08-available-border` | `#a5b4fc` | `#9fb9d8` |
| `--sc08-verified-bg` | `#e8f5ee` | `#e8f3e8` |
| `--sc08-verified-border` | `#84b899` | `#79a47a` |
| `--sc08-selection` | `#c7d2fe` | `#eadfca` |

En C, el cobre exacto `#c98a1e` se limitó a bordes o marcas de trazabilidad. El texto pequeño de fuentes usó el derivado oscuro `#8a5a0b` sobre superficie clara; sobre azul, la fuente conservó texto claro y el cobre quedó solo en el borde. El verde añadido por la muestra se limitó a `.validation-banner`, asociado a verificación aprobada. Los verdes ya existentes en gráficos y categorías funcionales no se alteraron.

### Selectores tocados

La raíz fue `.site-shell[data-tema-muestra][data-vista-muestra]`; las variables se declararon en los selectores con `data-tema-muestra="b"` y `data-tema-muestra="c"`. Se añadió también el estilo propio de `.theme-lab`, `.theme-lab-inner` y `.theme-lab-options`.

Dentro de la muestra se sobrescribieron solamente presentaciones del shell y valores OKLCH rígidos que no heredaban las variables:

- foco y selección: `:focus-visible`, `::selection`;
- estructura: `.institution-bar`, `.brand-mark`, `.site-footer`;
- encabezados oscuros: `.portal-hero`, `.home-hero`, `.explorer-cta`, `.portal-compass`, `.portal-source-line`, `.hero-proof`, sus textos, overlines, iconos, enlaces y botones asociados;
- portada: `.portal-module.available`, `.available .module-status`, `.portal-module.next`;
- superficies: `.notice` y `tbody tr:hover`;
- trazabilidad: `.source-button`, `.source-file code`, `.source-facts code`, `.hash`;
- verificación: `.validation-banner`;
- pie: `.footer-grid strong`, `.footer-grid a`, `.footer-label`, `.footer-license`, `.footer-license a`, `.glossary-global-note` y `.glossary-global-note > span`.

No se añadieron reglas para `.category-tabs`, `.tone-panel`, `.tone-explorer`, `.tone-estamental`, `.tone-method` ni para componentes de gráficos. Las pruebas compararon los colores computados de pestañas y tonos de navegación entre B y C y entre anchos, sin diferencias.

### Evidencia visual

Se creó `scripts/capture-sc08.mjs`. Las ocho imágenes PNG de página completa quedaron en `documentación/plataforma/evidencia/`:

- `sc08_portada_tema-b_1440.png` y `sc08_portada_tema-b_375.png`;
- `sc08_portada_tema-c_1440.png` y `sc08_portada_tema-c_375.png`;
- `sc08_panel_tema-b_1440.png` y `sc08_panel_tema-b_375.png`;
- `sc08_panel_tema-c_1440.png` y `sc08_panel_tema-c_375.png`.

Las ocho se abrieron y revisaron visualmente, incluidos recortes a resolución nativa del encabezado y el inicio de cada vista. No se observaron solapamientos, cortes, fondos oscuros de lectura en B, usos textuales pequeños de cobre sobre azul en C ni defectos que exigieran recapturar.

### Verificación y regresión

- SC-08 desarrollo: **59/59 controles aprobados** en `evidencia/sc08_verificacion.json`. Incluye paletas, tipografías, ocho capturas, ausencia de desborde horizontal, botones táctiles, conservación de query params, retorno a Tema actual, exclusión de otras vistas y cero errores de consola/red.
- SC-08 producción: **7/7 controles aprobados** en `evidencia/sc08_verificacion_produccion.json`; sin laboratorio ni atributos en el DOM compilado, aun con `?tema=b` o `?tema=c`.
- Shell: **16/16 controles aprobados**.
- Personal: **124/124 controles aprobados**, sin errores de consola, ejecución o red.
- Paquete: **APROBADO**; 1.086 JSON y 144 CSV válidos, hashes correctos y 69/69 controles de agregados.
- `npm run build`: correcto; TypeScript y Vite 7.3.8. Persistió la advertencia no bloqueante por el chunk principal, entonces de 806,93 kB.
- ESLint acotado a `Layout.tsx` y `main.tsx`: sin errores.

Los servidores temporales de desarrollo y producción se detuvieron. No se desplegó, no se creó remoto y no se hicieron commits. Esta sección conserva la evidencia histórica de la comparación; el laboratorio fue retirado al adoptar C.

---

## 13. Tema C definitivo — implementación posterior a SC-08

**Fecha de aprobación e implementación:** 17-11-2026.  
**Decisión:** el propietario eligió la opción C. Quedó registrada como D-20.  
**Alcance:** sistema visual global aplicado mediante shell y variables CSS, sin editar componentes internos, datos ni lógica de Personal.

### Implementación permanente

- Se eliminaron del shell el conmutador, `useSearchParams`, los tipos y atributos de muestra. Los parámetros históricos `?tema=b` y `?tema=c` ya no cambian la presentación.
- Se retiraron `src/sc08.css` y `scripts/capture-sc08.mjs`; la evidencia comparativa de la sección 12 se conserva como registro histórico.
- Se añadió `src/tema-c.css`, importado después de las hojas base. Declara en `:root` la paleta C y variables semánticas permanentes para marca, hero, texto sobre azul, trazabilidad, disponibilidad, verificación y selección.
- Los valores base son los documentados para C en la sección 12. Las variables provisionales `--sc08-*` se reemplazaron por nombres semánticos: `--brand-chrome`, `--hero-*`, `--on-dark*`, `--dark-link`, `--trace-*`, `--available-*`, `--verified-*` y `--selection`.
- El cobre `#c98a1e` permanece en bordes y marcas de procedencia; `#8a5a0b` se usa para texto pequeño de trazabilidad sobre fondo claro. La verificación automática midió contraste AA en los botones de fuente.
- `index.html` actualizó `theme-color` a `#155bb5`.
- Se conservaron Source Sans 3, Source Serif 4, las pestañas funcionales y el sistema de gráficos. Se añadieron reglas de impresión para que los encabezados azules vuelvan a fondo blanco y texto negro.

### Verificación final sobre producción

Se añadió `scripts/verify-tema-c.mjs` y se ejecutó contra el build servido desde `dist/`:

- **33/33 controles aprobados** en `evidencia/verificacion_tema_c.json`: paleta, metadatos, tipografías, contraste de trazabilidad, ausencia de laboratorio y atributos, parámetros históricos inertes, categorías constantes, cuatro capturas, revisión de otras rutas y cero errores de consola/red.
- Shell: **16/16 controles aprobados**.
- Personal: **124/124 controles aprobados**, incluidos los contrastes de tarjetas y pestañas con la nueva tinta.
- Paquete: **APROBADO**; 1.086 JSON, 144 CSV, hashes válidos y 69/69 controles de agregados.
- `npm run build`: correcto; chunk principal de 806,82 kB con la advertencia no bloqueante ya declarada.
- ESLint acotado a `Layout.tsx` y `main.tsx`: sin errores.

### Evidencia visual definitiva

Las cuatro capturas se revisaron a página completa y en recortes a resolución nativa:

- `tema-c_definitivo_portada_1440.png` y `tema-c_definitivo_portada_375.png`;
- `tema-c_definitivo_panel_1440.png` y `tema-c_definitivo_panel_375.png`.

No se observaron desbordes, solapamientos, restos del laboratorio ni cambios de jerarquía. La compuerta de narrativa permanece cerrada. No se desplegó, no se creó remoto y no se hicieron commits.


---

## 14. Incidente de vista previa — recuperación de Vite/esbuild

**Fecha:** 17-11-2026.  
**Síntoma:** la vista previa no recargaba y mostraba `[plugin:vite:esbuild] The service is no longer running` al solicitar `src/main.tsx`.

### Diagnóstico y recuperación

- El proceso de Vite administrado por Kimi seguía escuchando en el puerto 7100, pero no tenía un proceso esbuild asociado. La portada entregaba HTML y título, aunque `#root` permanecía vacío; `GET /src/main.tsx` respondía HTTP 500 con el error informado.
- La transformación directa con el paquete esbuild instalado funcionó correctamente. No fue necesario reinstalar dependencias ni modificar la configuración.
- Se detuvo únicamente el proceso huérfano identificado (PID 23636) y se inició una instancia limpia y temporal de Vite para validación.
- `GET /src/main.tsx` respondió HTTP 200 con JavaScript transformado. La verificación `QA_BASE_URL=http://localhost:7100 node scripts/verify-tema-c.mjs` aprobó **33/33 controles**, sin errores de consola ni de red.
- En el navegador integrado de Kimi se comprobó la portada renderizada, el acceso a Personal y la apertura del panel general (`#/panel`) con sus cifras y gráficos.

No se modificaron código, datos, dependencias ni el Tema C. La instancia temporal se detuvo y el puerto 7100 quedó libre para que Kimi administre un nuevo arranque desde la tarjeta de vista previa. No se desplegó, no se creó remoto y no se hicieron commits.


---

## 15. D-20 definitiva — Tema Coronel y chrome de familia

**Fecha de cierre e implementación:** 18-11-2026.  
**Decisión aplicada:** C ajustado, con azul profundo apagado, chrome compacto e iconografía local de Coronel.  
**Alcance efectivo:** `Layout.tsx`, `tema-c.css`, metadatos, portada mediante estilos del shell y texturas nuevas. No se modificaron componentes internos, datos, lógica ni gráficos de Personal; no quedaron pendientes coordinados para este ajuste.

### Paleta y roles finales

| Variable | Valor | Rol |
|---|---|---|
| `--background`, `--p-paper` | `#fdfbf6` | Superficie papel cálido, sin cambios respecto de C. |
| `--surface` | `#fffefa` | Tarjetas y superficies de lectura. |
| `--surface-muted` | `#f3efe5` | Superficies secundarias. |
| `--text`, `--p-ink` | `#182634` | Tinta principal y marino del pie. |
| `--text-secondary` | `#4c5a64` | Texto secundario sobre superficies claras. |
| `--border`, `--p-line` | `#ddd6c8` | Bordes cálidos. |
| `--accent`, `--p-teal`, `--brand-chrome`, `--hero-bg` | `#143d6d` | Azul profundo apagado definitivo; reemplaza `#155bb5`. |
| `--accent-dark` | `#103154` | Variante oscura para enlaces y acentos. |
| `--hero-surface` | `#1a4778` | Superficie secundaria dentro de bandas azules. |
| `--hero-border` | `#91a9c4` | Bordes sobre azul. |
| `--hero-accent`, `--dark-link` | `#e8eef5` | Overlines y enlaces claros. |
| `--on-dark` | `#fdfbf6` | Texto principal sobre azul o marino. |
| `--on-dark-secondary` | `#dce5ef` | Texto secundario sobre azul o marino. |
| `--trace-solid`, `--trace-border`, `--trace-border-on-dark` | `#c98a1e` | Cobre reservado a marcas y bordes de trazabilidad. |
| `--trace-ink` | `#8a5a0b` | Texto accesible de fuentes y hashes sobre fondo claro. |
| `--trace-bg` / `--trace-bg-hover` | `#f7edd8` / `#f1e0bd` | Fondo normal y hover de botones Fuente. |
| `--available-bg` / `--available-border` | `#e7eef8` / `#9fb9d8` | Estado disponible. |
| `--verified-bg` / `--verified-border` | `#e8f3e8` / `#79a47a` | Verde exclusivo de verificación aprobada. |
| `--selection` | `#eadfca` | Selección de texto. |

`index.html` actualizó `theme-color` a `#143d6d`. Source Sans 3, Source Serif 4 y la paleta funcional de categorías y gráficos se conservaron.

### Dimensiones del chrome

| Variable / elemento | Valor final |
|---|---|
| `--chrome-height` | 64 px; encabezado principal sticky. |
| `--brand-title-size` | 1,1 rem (17,6 px) en escritorio; 1 rem en móvil. |
| `--brand-subtitle-size` | 0,78 rem (12,48 px). |
| Navegación | Píldoras con radio 999 px y mínimo de 44 px, incluida la variante móvil. |
| `--footer-text-size` | 0,78 rem (12,48 px). |
| Pie | Franja marino `#182634`, línea principal de identidad/origen y línea de créditos con MIT y CC-BY 4.0. |
| Héroe de portada | Banda de 348,69 px a 1440 px; título compacto y contenido modular como protagonista. En móvil usa una sola columna. |

### Iconografía local

Se añadieron dos SVG originales de line-art monocromo:

- `plataforma/src/assets/coronel-mar.svg`: olas, peces y embarcación de pesca para la banda de encabezado.
- `plataforma/src/assets/coronel-industria.svg`: carbón, herramientas y carro de minería, e industria para el pie.

`plataforma/src/components/CoronelTexture.tsx` importa ambos archivos como texto y los inserta como SVG en línea. Los contenedores usan `aria-hidden="true"`; los SVG incluyen `focusable="false"`. CSS aplica `pointer-events: none`, sin interactividad. `--texture-opacity` es **8 %** en escritorio y **6 %** en móvil; los grupos `.texture-detail` se ocultan hasta 520 px para conservar una franja simplificada. Las texturas se omiten al imprimir.

La revisión visual a resolución nativa confirmó que las siluetas no compiten con el título ni con el contenido. El cobre de los botones Fuente permanece visible y diferenciado.

### Verificación y evidencia

Se amplió `scripts/verify-tema-c.mjs` para comprobar paleta, metadatos, chrome, texturas, contraste, cobre, responsive, ausencia del laboratorio y conservación tipográfica/funcional.

- Tema Coronel: **47/47 controles aprobados** en `evidencia/verificacion_tema_coronel.json`.
- Contraste texto secundario claro sobre `#143d6d`: **8,60:1**.
- Contraste del título del héroe sobre `#143d6d`: **10,59:1**.
- Contraste de texto cobre oscuro sobre fondo de Fuente: **5,09:1**; borde `#c98a1e` confirmado.
- Portal: **16/16 controles aprobados**.
- Personal con `CHECK_DOCS=1`: **124/124 controles aprobados**, incluidos ocho documentos enlazados y cero errores de consola/ejecución/red.
- Paquete: **APROBADO**; 1.086 JSON, 144 CSV, hashes válidos y 69/69 controles de agregados.
- `npm run build`: correcto; chunk principal de 808,90 kB con la advertencia no bloqueante ya declarada.
- ESLint acotado a `Layout.tsx`, `CoronelTexture.tsx` y `main.tsx`: sin errores.

Capturas revisadas a página completa y en recortes nativos:

- `tema-coronel_portada_1440.png` y `tema-coronel_portada_375.png`;
- `tema-coronel_panel_1440.png` y `tema-coronel_panel_375.png`.

La primera captura detectó que la regla del héroe conservaba dos columnas en móvil por especificidad; se corrigió a una columna y se repitieron build y pruebas. La corrida integral de paquete se ejecutó finalmente con la revisión documental activada. No se desplegó, no se creó remoto y no se hicieron commits.


---

## 16. Corrección de navegación responsive y proporción de Personal

**Fecha:** 18-11-2026.  
**Alcance:** shell y navegación global; no se modificaron vistas internas, datos, lógica ni gráficos de Personal.

### Cambios aplicados

- Se corrigió el menú desplegable a media pantalla y móvil. La causa era `overflow: hidden` en `.site-shell .main-header`, que recortaba `.main-nav.open` al estar posicionado con `top: 100%`. El encabezado ahora usa `overflow: visible`; `.local-texture` conserva su propio `overflow: hidden`, por lo que la textura decorativa sigue recortada.
- Se compactó exclusivamente desde `tema-c.css` la banda `.home-hero` de la portada interna de Personal: padding de **36/28 px** en escritorio y **28/24 px** hasta 800 px; título con máximo de **3 rem** en escritorio y **2,25 rem** hasta 520 px; márgenes y prueba de validación reducidos. No se modificó `Home.tsx`.
- Se añadió **Inicio** como primer enlace de `personalNav`, con icono local y destino `/personal`. La marca global continúa llevando a `/`. El tono `tone-home` es neutro y no altera la paleta funcional de las cuatro categorías.
- `verify-portal.mjs` ahora exige cinco enlaces, comprueba el retorno desde Panel general mediante Inicio y verifica el menú completo de Personal a 768 px. `verify-modulo.mjs` actualizó su control de navegación para nueve estados medidos —cinco iniciales y cuatro activos adicionales— conservando las exigencias de contraste.

### Verificación y evidencia

- Build de producción: correcto; chunk principal de **809,19 kB**, con la advertencia no bloqueante ya declarada.
- Portal: **19/19 controles aprobados**, incluidos menú a 768/375 px, retorno de Inicio, responsive y cero errores de consola/red.
- Tema Coronel: **47/47 controles aprobados**.
- Personal con `CHECK_DOCS=1`: **124/124 controles aprobados**.
- Paquete: **APROBADO**; 1.086 JSON, 144 CSV, hashes válidos y 69/69 controles de agregados.
- ESLint acotado a `Layout.tsx`, `CoronelTexture.tsx` y `main.tsx`: sin errores.
- Capturas revisadas: `coronel_personal_1440.png`, `coronel_menu_personal_768.png` y `00_portal_375.png`. La portada interna presenta una banda compacta y el menú desplegable muestra sus cinco enlaces sin recorte.

No se desplegó, no se creó remoto y no se hicieron commits. El servidor temporal de validación se detuvo al finalizar.


---

## 17. Página pública de actualizaciones — v0.1

**Fecha:** 18-11-2026.  
**Alcance:** shell global, enrutamiento y nueva página pública. No se modificaron vistas internas, datos, lógica ni gráficos de Personal.

### Implementación

Se añadió la ruta pública `/actualizaciones` mediante `src/pages/Actualizaciones.tsx`. La página presenta un registro cronológico inverso con versión, fecha, resumen, cambios sustantivos y módulos afectados. La primera entrada es **v0.1**, fechada el 18-11-2026.

El contenido se redactó en lenguaje ciudadano desde las bitácoras vigentes: habilitación del módulo Personal, trazabilidad por archivo/fila/huella, trayectorias y versiones alternas, decodificación de asignaciones especiales, portada con placeholders activos, Tema Coronel, navegación Inicio y controles vigentes. No se exponen rutas internas de trabajo ni procesos de construcción.

El pie incorpora el enlace permanente **Actualizaciones**, entre la fuente municipal y Metodología. La página usa las variables y proporciones del Tema Coronel: banda azul baja, papel cálido, tinta, tarjetas y pie marino. Los estilos están aislados en `portal.css` con breakpoints a 800 y 520 px.

### Verificación y evidencia

Se añadió a `verify-portal.mjs` un control de contenido v0.1 y capturas a 1440/375 px; `verify-tema-c.mjs` incluye `/actualizaciones` en el barrido de rutas.

- Portal: **20/20 controles aprobados**, incluido el enlace pie → actualizaciones y el registro v0.1.
- Tema Coronel: **48/48 controles aprobados**.
- Personal con `CHECK_DOCS=1`: **132/132 controles aprobados**; sus vistas internas quedaron intactas.
- Paquete: **APROBADO**; 1.087 JSON, 144 CSV, hashes válidos, 77/77 controles de agregados y verificación de navegador 132/132.
- Build de producción: correcto; chunk principal de **817,02 kB**, con la advertencia no bloqueante ya declarada.
- ESLint acotado a `App.tsx`, `Layout.tsx` y `Actualizaciones.tsx`: sin errores.
- Capturas revisadas: `coronel_actualizaciones_1440.png` y `coronel_actualizaciones_375.png`, sin desbordes ni defectos visibles.

No se desplegó, no se creó remoto y no se hicieron commits. El servidor temporal de validación se detuvo al finalizar.


---

## 18. Escudo municipal en la marca — ajuste previo a despliegue

**Fecha:** 18-11-2026.  
**Solicitud:** incorporar la imagen del escudo de la Municipalidad de Coronel en el logotipo del encabezado, en reemplazo del icono genérico de escudo con palomita.  
**Alcance:** shell global; no se modificaron vistas internas, datos, lógica ni gráficos de Personal.

### Implementación

La imagen entregada por el propietario se copió a `plataforma/src/assets/escudo-coronel.png` y se generó una versión recortada y compacta para marca en `plataforma/src/assets/escudo-coronel-marca.png`. El original entregado no se modificó. La versión usada mantiene la proporción del escudo y pesa **71,56 kB** en el paquete compilado.

`Layout.tsx` incorpora la imagen con texto alternativo vacío, porque el enlace de marca conserva su etiqueta accesible completa. La insignia del encabezado pasó de azul sólido con icono a una pieza blanca con borde cálido, manteniendo 36 × 36 px y el chrome D-20. La imagen se muestra a 22 px de ancho, con altura automática para no deformar la corona y el cuerpo del escudo.

Se añadió a `verify-portal.mjs` el control `escudo_municipal_en_marca`, que exige una única imagen visible, texto alternativo vacío y carga efectiva.

### Verificación y evidencia

- Portal: **21/21 controles aprobados**, incluido el escudo municipal.
- Tema Coronel: **48/48 controles aprobados**.
- Paquete: **APROBADO**; hashes, JSON, CSV y controles de agregados válidos.
- Build de producción: correcto; chunk principal de **816,87 kB**, con la advertencia no bloqueante ya declarada.
- ESLint acotado a `Layout.tsx`: sin errores.
- Capturas `00_portal_1440.png` y `00_portal_375.png` revisadas, incluidos recortes nativos del encabezado. El escudo permanece reconocible y alineado con el título en escritorio y móvil.

No se desplegó, no se creó remoto y no se hicieron commits. El servidor temporal se detuvo al finalizar.
