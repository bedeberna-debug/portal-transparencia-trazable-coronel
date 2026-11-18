import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const plataforma = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const workspace = resolve(plataforma, '..');
const dist = join(plataforma, 'dist');
const dataDir = join(dist, 'data');
const evidenciaDir = join(workspace, 'documentación', 'plataforma', 'evidencia');
const sha256 = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');
const readJson = (path) => JSON.parse(readFileSync(path, 'utf8'));
const walk = (directory) => readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
  const path = join(directory, entry.name);
  return entry.isDirectory() ? walk(path) : [path];
});

const files = walk(dist);
const jsonFiles = readdirSync(dataDir).filter((name) => extname(name) === '.json');
const csvFiles = files.filter((path) => extname(path).toLowerCase() === '.csv');
const documentos = readdirSync(join(dist, 'docs')).filter((name) => extname(name) === '.md');
const meta = readJson(join(dataDir, 'meta.json'));
const fuentes = readJson(join(dataDir, 'fuentes.json'));
const estimado = readJson(join(dataDir, 'composicion_estamento_estimado.json'));
const navegador = readJson(join(evidenciaDir, 'verificacion_navegador.json'));
const index = readFileSync(join(dist, 'index.html'), 'utf8');

const hashesJson = Object.entries(meta.artefactos).every(([name, artifact]) => {
  const path = join(dataDir, name);
  return existsSync(path) && statSync(path).size === artifact.bytes && sha256(path) === artifact.sha256;
});
const fuentesProcesadas = fuentes.registros.filter((source) => source.estado === 'procesado_en_modulo');
const hashesCsv = fuentesProcesadas.every((source) => {
  const original = join(workspace, ...source.ruta_relativa.split(/[\\/]/));
  const copia = join(dist, ...source.url_respaldo.split('/'));
  return existsSync(original) && existsSync(copia)
    && sha256(original) === source.fuente_sha256
    && sha256(copia) === source.fuente_sha256;
});
const documentosEnlazados = navegador.controles.find((control) => control.control === 'documentacion_enlazada_disponible');
const fichasDir = join(dataDir, 'fichas');
const fichasIndividuales = existsSync(fichasDir) ? walk(fichasDir).filter((path) => extname(path) === '.json').length : 0;
const estadoFichas = readJson(join(dataDir, 'fichas_estado.json'));
const hashesFichas = estadoFichas.fichas.length === fichasIndividuales && estadoFichas.fichas.every((ficha) => {
  const path = join(dataDir, ...ficha.archivo.split('/'));
  return existsSync(path) && statSync(path).size === ficha.bytes && sha256(path) === ficha.sha256;
});
const totalLiquido = Object.values(meta.totales_por_categoria)
  .reduce((total, category) => total + category.gasto_liquido_clp, 0);
const langValido = /<html\s+lang="es-CL">/.test(index);

const reporte = {
  fecha_verificacion: new Date().toISOString(),
  json_raiz: jsonFiles.length,
  json_fichas: fichasIndividuales,
  json_total: jsonFiles.length + fichasIndividuales,
  entradas_hash: Object.keys(meta.artefactos).length,
  meta_autorreferenciada: Object.hasOwn(meta.artefactos, 'meta.json'),
  hashes_validos: hashesJson,
  hashes_fichas_validos: hashesFichas,
  csv: csvFiles.length,
  csv_originales_y_copias_sha256_validos: hashesCsv,
  documentos_md: documentos.length,
  documentos_enlazados_verificados: documentosEnlazados?.evidencia?.length ?? 0,
  nojekyll: existsSync(join(dist, '.nojekyll')),
  idioma_html: 'es-CL',
  idioma_html_valido: langValido,
  bytes_dist: files.reduce((total, path) => total + statSync(path).size, 0),
  bytes_explorador: Object.entries(meta.artefactos)
    .filter(([name]) => name.startsWith('explorador_'))
    .map(([, artifact]) => artifact.bytes),
  registros_totales: meta.conteos.registros_totales,
  registros_en_proyeccion_trayectoria: meta.conteos.registros_en_proyeccion_trayectoria,
  versiones_alternas: meta.conteos.versiones_alternas,
  total_liquido_calculado: totalLiquido,
  estamento_estimado: {
    version_mapeo: estimado.version_mapeo,
    sha256_mapeo: estimado.fuente_mapeo.sha256,
    leyenda_fija: estimado.leyenda_fija,
    registros: estimado.registros.reduce((total, row) => total + row.dotacion_registros, 0),
    no_clasificable: estimado.registros.filter(row => row.estamento_estimado === 'No clasificable').reduce((total, row) => total + row.dotacion_registros, 0),
    cobertura: estimado.cobertura,
  },
  validacion_agregados: meta.validacion_agregados,
  ficha_individual: {
    ...meta.ficha_individual,
    archivos_json_individuales: fichasIndividuales,
  },
  verificacion_navegador: navegador.resumen,
};

const aprobado = reporte.json_raiz === 19
  && reporte.json_fichas === 1068
  && reporte.json_total === 1087
  && reporte.entradas_hash === 18
  && !reporte.meta_autorreferenciada
  && reporte.hashes_validos
  && reporte.hashes_fichas_validos
  && reporte.csv === 144
  && reporte.csv_originales_y_copias_sha256_validos
  && reporte.documentos_md === 9
  && reporte.documentos_enlazados_verificados === 8
  && reporte.nojekyll
  && reporte.idioma_html_valido
  && reporte.registros_totales === 22940
  && reporte.registros_en_proyeccion_trayectoria === 22938
  && reporte.versiones_alternas === 2
  && reporte.total_liquido_calculado === 26599752237
  && reporte.estamento_estimado.version_mapeo === 'D-17_v1.1'
  && reporte.estamento_estimado.sha256_mapeo === '99a357539d830d1e83f1c89b8e12ee50ea1f57a0576d538e8a8284dc1a571548'
  && reporte.estamento_estimado.registros === 10397
  && reporte.estamento_estimado.no_clasificable === 3957
  && meta.glosario.entradas_aprobadas === 16
  && meta.asignaciones_especiales.conceptos === 394
  && meta.asignaciones_especiales.cobertura.registros_con_codigos === 13476
  && meta.asignaciones_especiales.cobertura.registros_completamente_decodificados === 13475
  && meta.asignaciones_especiales.cobertura.registros_con_anomalias === 1
  && meta.licencias.decision === 'D-16'
  && meta.licencias.codigo === 'MIT'
  && meta.licencias.datos_derivados === 'CC BY 4.0'
  && reporte.validacion_agregados.controles === 77
  && reporte.validacion_agregados.aprobadas === 77
  && reporte.validacion_agregados.fallas === 0
  && reporte.ficha_individual.habilitada
  && reporte.ficha_individual.colisiones_id_periodo === 0
  && reporte.ficha_individual.colisiones_originales_id_periodo === 2
  && reporte.ficha_individual.archivos_json_individuales === 1068
  && reporte.verificacion_navegador.controles === 132
  && reporte.verificacion_navegador.aprobadas === 132
  && reporte.verificacion_navegador.fallas === 0;
reporte.resultado = aprobado ? 'APROBADO' : 'RECHAZADO';
writeFileSync(join(evidenciaDir, 'verificacion_paquete.json'), `${JSON.stringify(reporte, null, 2)}\n`);
console.log(JSON.stringify(reporte, null, 2));
if (!aprobado) process.exitCode = 1;
