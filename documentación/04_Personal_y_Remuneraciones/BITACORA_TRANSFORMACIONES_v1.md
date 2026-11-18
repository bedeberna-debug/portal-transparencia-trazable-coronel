# Bitácora de transformaciones — Personal y Remuneraciones

**Proyecto:** Portal de Transparencia Trazable – Municipalidad de Coronel  
**Versión del esquema:** canonico_v1.0.0  
**Fecha de corte:** 2026-11-14  
**Criterio rector:** trazabilidad total y fuentes originales intocables.

## 1. Alcance y fuentes

Se inspeccionaron **168 CSV** y **4 maestros XLSX manuales**. Por categoría: Planta 36 CSV, Contrata 36, Código del Trabajo 36, Honorarios 36 y Autoridades 24. Autoridades no tiene 2023; queda pendiente Wayback Machine (H-001).

Los archivos de `datos crudos` se abrieron en modo lectura. `INVENTARIO_FUENTES_v1.xlsx` registra ruta, filas, codificación, delimitador, contenido y SHA-256 de cada fuente y maestro original. Las salidas se escriben únicamente en `datos procesados` y `documentación`; los PDF se archivan en `archivo externo`.

## 2. Lectura y reglas comunes

1. Decodificación probada en orden UTF-8-SIG, CP1252 y Latin-1; separador detectado entre `;`, coma, tabulador y `|`. Los 168 CSV se leyeron sin errores.
2. Se verificó que las 166 columnas `Unnamed` estuvieran completamente vacías antes de excluirlas.
3. La vinculación usa nombre de archivo + nombre normalizado para cruce (mayúsculas, Unicode y espacios, sin acentos solo en la clave) + número de ocurrencia. El nombre original se conserva. Las ocurrencias múltiples no se eliminan automáticamente.
4. El período proviene de `Año` y `Mes` **dentro del contenido**, nunca del prefijo o nombre del archivo. El nombre físico queda en la trazabilidad.
5. Importes: se eliminan moneda y separadores; punto = miles y coma = decimales; se conservan pesos enteros. `No tiene`, `No informa`, `-` y vacío se transforman en 0 en columnas `_clp`; el texto original queda en `_raw`.
6. Horas: expresión sobre el segmento `monto : N,NN hrs`; la coma decimal se transforma en punto. Si no hay horas publicadas, el valor derivado es 0. Nunca se reparten horas genéricas entre diurnas/nocturnas/festivas.
7. Fechas: interpretación día/mes/año a ISO `AAAA-MM-DD`; el original y la clasificación de término se preservan. `Indefinido` no se convierte en una fecha ficticia.
8. Toda fila canónica incorpora archivo, ruta, fila CSV (encabezado = 1), SHA-256, codificación y separador. `registro_id` es único por ruta + fila; `id_trabajador` se conserva del maestro manual.

## 3. Correcciones manuales conocidas y su tratamiento

El encargo antecedente informa **deduplicación manual** e **inferencia de género por nombre con revisión manual de ambiguos**. No existen en la carpeta tablas separadas que permitan reejecutar esas decisiones; por ello se documentan como antecedentes conocidos, no como transformaciones independientemente reproducidas en este lote. Los IDs, nombres depurados, primeros nombres y géneros se conservaron. No se volvió a inferir género ni se aplicó una nueva deduplicación. Las repeticiones H-005 y H-006 se conservaron por tener valores o fuentes distintos.

## 4. Tarea 1 — Integridad de Código del Trabajo

- Los 36 CSV suman **933 filas**, exactamente las 933 del maestro; la cobertura mensual coincide en 36/36 meses.
- El cruce por período + nombre + ocurrencia vinculó 933/933 filas, sin registros huérfanos.
- Se detectó que **15 columnas crudas** estaban vacías en los tres años y `_archivo_origen` también, no solo en 2024-2025. Se restauraron **14.928 celdas** (13.995 de campos crudos + 933 de origen) en una versión nueva.
- Los siete importes numéricos y `he_horas_num` coinciden con el recálculo desde CSV en todas las filas: **0 diferencias**.
- La v2 conserva ID, nombre depurado, primer nombre, género, estamento, observaciones y numéricos del maestro; incorpora ruta, fila y SHA-256.
- Las anomalías de nombres 2024/2025 se resolvieron por contenido. Además se encontró una fila de mayo dentro del CSV de julio de 2025 (H-005); no se deduplicó.

**Salida:** `MAESTRO_CODTrabajo_Coronel_2023-2025_v2_corregido.xlsx`, con hojas de control, diferencias, cobertura y anomalías.

## 5. Tarea 2 — Recuperación de horas extra

Se comprobó que el texto raw de Planta y Contrata coincide con el CSV en las tres clases de horas. Resultados:

| Maestro | Tipo | Registros con horas | Horas totales | Monto total CLP | Monto positivo sin horas |
|---|---:|---:|---:|---:|---:|
| Planta | Diurnas | 2,763 | 35,754 | 197,986,085 | 0 |
| Planta | Nocturnas | 2,405 | 70,601 | 381,035,987 | 0 |
| Planta | Festivas | 0 | 0 | 0 | 0 |
| Contrata | Diurnas | 5,223 | 72,946 | 367,326,488 | 0 |
| Contrata | Nocturnas | 4,651 | 116,920 | 620,332,740 | 0 |
| Contrata | Festivas | 0 | 0 | 0 | 0 |

Código del Trabajo ya tenía `he_horas_num`; se validó contra el raw con 0 diferencias. Su fuente no distingue tipo, por lo que el canónico usa `horas_extra_horas` y `horas_extra_desagregacion=sin_desagregacion`.

**Salidas:** versiones nuevas `v2_horas` de Planta y Contrata. No se copiaron resúmenes heredados que pudieran quedar desactualizados.

## 6. Tarea 3 — Esquema canónico

Se adoptó `snake_case` en español, sin acentos en nombres técnicos. Núcleo común: `categoria`, `registro_id`, `id_trabajador`, `anio`, `mes_numero`, `mes_nombre`, `periodo`, identidad, estamento, cargo, fechas raw/ISO, importes raw/CLP y trazabilidad. Los conceptos específicos conservan sufijos por tipo de hora y los campos de pago/enlace de Honorarios.

| Maestro | Filas | Columnas canónicas | Vinculación CSV | Diferencias numéricas heredadas |
|---|---:|---:|---:|---:|
| Planta | 4,927 | 51 | 100 % | 0 |
| Contrata | 7,616 | 51 | 100 % | 0 |
| Código del Trabajo | 933 | 48 | 100 % | 0 |
| Honorarios | 9,464 | 42 | 100 % | 0 |
| **Total** | **22,940** | — | **100 %** | **0** |

`MAPEO_ESQUEMA_CANONICO_v1.xlsx` documenta columna original del maestro, columna CSV, nombre canónico y regla. Las hojas analíticas antiguas no se copiaron. En particular, el resumen de Planta tiene 757 filas para 178 IDs y no se consideró confiable (H-007).

## 7. Informes de funciones de Honorarios

El inventario se extrae directamente de `Enlace funciones desarrolladas`, conservando trabajador, período, URL, archivo y fila. La descarga se realiza por lotes a `archivo externo/informes_funciones_honorarios/AAAA/MM/`. El manifiesto registra fecha, URL de descarga, HTTP, estado, bytes, SHA-256 y ruta local; solo se declara `descargado` con HTTP 200 y firma PDF válida.

La ejecución v1 **ya reescribió los parámetros `dl=0` a `dl=1`**. Una prueba controlada con tres URL recuperadas mostró respuestas variables de Dropbox: la misma URL con `dl=1` entregó PDF o HTML en distintas solicitudes, con ambos agentes de usuario. En consecuencia, el artefacto no se atribuye al parámetro `dl=0` ni a un cliente específico, y los estados no terminales se reintentan nuevamente al reanudar. Para descartar un artefacto técnico en H-010, v2 reintentó los 5,099 objetos sin PDF nuevamente con `dl=1`, registrando URL final, HTTP, tipo de contenido, título HTML y SHA-256 de la respuesta. Solo cuando no existía una eliminación explícita se probaron además `raw=1` y el host directo. Resultado: 4,794 PDF recuperados, 123 objetos con `File Deleted`, 182 con `Link Temporarily Disabled` y 0 con otros estados. Las respuestas `File Deleted` se clasifican como eliminación explícita, no como previsualizaciones ni como una inferencia genérica de enlaces rotos.

Los 3,094 registros sin URL se mantienen separados: no son fallos de Dropbox. `MANIFIESTO_DESCARGAS_v1.xlsx` se conserva como antecedente de auditoría; `REINTENTOS_DROPBOX_H010_v1.xlsx` y `MANIFIESTO_DESCARGAS_v2.xlsx` constituyen la evidencia vigente, junto con `INVENTARIO_INFORMES_HONORARIOS_v1.xlsx` y H-010.

## 8. Validación y límites

- 22,940 registros canónicos vinculados a fuente; 0 IDs de registro duplicados.
- Todos los importes y horas heredados comparados contra CSV: 0 diferencias.
- Fechas de inicio no vacías no parseadas: 0 en los cuatro maestros.
- Las cifras de personas, períodos repetidos o resúmenes no deben interpretarse como nómina única sin reglas adicionales; hay dos pares período-nombre conservados y documentados.
- Autoridades no forma parte de los cuatro maestros canónicos solicitados. Su ausencia de 2023 y el período no informado de diciembre de 2025 quedan pendientes.

## 9. Plantilla replicable para futuras categorías

1. Congelar fuentes; inventariar ruta, filas, esquema, codificación y SHA-256.
2. Comparar nombre de archivo contra período del contenido; registrar anomalías sin renombrar originales.
3. Perfil de columnas: vacíos, `Unnamed`, tipos, catálogos y formatos monetarios/horarios.
4. Definir clave de cruce y ocurrencia; no deduplicar solo por persona-período.
5. Contrastar filas por mes y totales por columna contra el maestro anterior.
6. Restaurar campos en archivo nuevo; nunca sobrescribir el manual ni el CSV.
7. Aplicar esquema canónico, conservar `_raw` y agregar derivados con reglas explícitas.
8. Añadir trazabilidad archivo/ruta/fila/SHA-256 a cada registro.
9. Documentar correcciones manuales conocidas y separar las que no son reproducibles.
10. Ejecutar controles de filas, huérfanos, duplicados, importes, horas, fechas y apertura/verificación XLSX.
11. Registrar hallazgos con severidad, evidencia, impacto, decisión y pendiente.
12. Versionar entregables y conservar manifiestos de descargas externas.

## 10. Scripts de reproducción

Los scripts quedan en `scripts/`: inspección, auditoría de Código del Trabajo, corrección, recuperación de horas, normalización, inventario/descargas y validación. Su ejecución utiliza únicamente las fuentes del espacio de trabajo y vuelve a crear archivos procesados, nunca los originales.
