# Portal de Transparencia Trazable — Municipalidad de Coronel

Portada, shell global y módulo de Personal y Remuneraciones. La fuente de origen son los datos de transparencia activa del portal municipal (MU068), Ley 20.285 e IGTA.

## Arquitectura

- React + TypeScript + Vite, completamente estático.
- `HashRouter`, sin backend ni reglas de reescritura.
- Tipografías Source Sans 3 y Source Serif 4 servidas localmente.
- Tema C definitivo en `src/tema-c.css`, conforme a D-20: papel cálido, azul institucional y cobre reservado para trazabilidad.
- Datos JSON, fuentes CSV y documentos copiados a `dist/` durante la compilación.
- `.nojekyll` generado para GitHub Pages.

## Rutas

- `/`: portada general del portal y presentación de módulos.
- `/personal`: portada del módulo Personal y Remuneraciones.
- `/panel`, `/explorador`, `/estamento/:categoria`, `/ficha/:id` y `/metodologia`: rutas internas del módulo, conservadas.

En la URL del navegador las rutas aparecen después de `#/`, por ejemplo `#/personal`.

## Compilación reproducible

Requisitos: Node.js 24 y npm.

```bash
npm ci
npm run build
```

El resultado queda en `plataforma/dist/`. La compilación utiliza los artefactos estáticos versionados en `plataforma/data/`, `plataforma/fuentes/` y `plataforma/docs/`; no regenera los maestros canónicos ni modifica sus datos.

Para revisar localmente el paquete compilado:

```bash
npm run preview -- --host 127.0.0.1 --port 7100
```

Para desarrollo, `npm run dev` acepta los argumentos estándar de host y puerto de Vite.

## Verificación

Con el paquete servido en el puerto 7100:

```bash
node scripts/verify-portal.mjs
node scripts/verify-tema-c.mjs
QA_BASE_URL=http://127.0.0.1:7100 CHECK_DOCS=1 node scripts/verify-modulo.mjs
node scripts/verify-package.mjs
```

La verificación del shell cubre identidad D-18, módulos y placeholders, licencias D-16, navegación, cuatro anchos, ausencia de enlaces vacíos, errores de consola y solicitudes fallidas. La verificación de Personal conserva sus controles funcionales y visuales; solo se actualizó su URL de portada a `/personal` por la integración del shell.

## Despliegue por hitos

`.github/workflows/deploy-pages.yml` prepara y despliega GitHub Pages **solo mediante `workflow_dispatch`**. No hay despliegue automático por push ni por calendario. La ejecución requiere autorización expresa del propietario y coordinación previa conforme a D-19.

Antes de autorizar se deben revisar la bitácora de plataforma, las licencias visibles, la compilación reproducible y el reporte npm vigente. No se utiliza `npm audit fix --force`.

## Licencias

- Código: MIT, según `LICENSE`.
- Datos agregados y artefactos derivados: CC-BY 4.0, según `LICENSE-DATA.md`.
- Atribución: Portal de Transparencia Trazable — Municipalidad de Coronel.

Los datos de origen conservan su referencia al portal municipal MU068 y su trazabilidad documental.
