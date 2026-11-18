# Registro de hallazgos — Personal y Remuneraciones

**Fecha de corte:** 2026-11-14

Los estados “resuelto” se refieren al saneamiento en archivos nuevos; ningún CSV o maestro original fue modificado.

## H-001 — Sin publicación 2023 en el portal oficial

- **Categoría:** Autoridades
- **Tipo / severidad:** Cobertura / Alta
- **Estado:** Pendiente verificación externa
- **Evidencia:** No existe directorio 2023 en datos crudos/05_Autoridades_de_Eleccion_Popular; solo hay 2024 y 2025.
- **Impacto:** Serie 2023-2025 incompleta para autoridades.
- **Decisión / acción:** Verificar disponibilidad histórica en Wayback Machine; no reconstruir ni imputar registros.
- **Pendiente:** Revisión Wayback Machine y eventual captura con fecha/URL de archivo.

## H-002 — Prefijo 03 duplicado en 2025 y ausencia de prefijo 04

- **Categoría:** Código del Trabajo
- **Tipo / severidad:** Nombre de archivo / Baja
- **Estado:** Resuelto por contenido
- **Evidencia:** 03_CODTrabajo_Marzo_2025.csv y 03_CODTrabajo_Abril_2025.csv; el segundo contiene 27 filas, todas Mes=Abril.
- **Impacto:** Riesgo de asignar abril a marzo si se usa el prefijo.
- **Decisión / acción:** Usar Año/Mes del contenido y conservar nombre físico como fuente.
- **Pendiente:** No renombrar el original; opcionalmente solicitar corrección al publicador.

## H-003 — Archivo de noviembre de 2024 con nombre contradictorio

- **Categoría:** Código del Trabajo
- **Tipo / severidad:** Nombre de archivo / Baja
- **Estado:** Resuelto por contenido
- **Evidencia:** 2024/10_CODTrabajo_Enero_2024 Noviembre.csv contiene 23 filas, todas Mes=Noviembre.
- **Impacto:** Riesgo de clasificación errónea como enero u octubre.
- **Decisión / acción:** Asignar 2024-11 por contenido y mantener trazabilidad al archivo real.
- **Pendiente:** No renombrar el original.

## H-004 — Campos crudos y origen vacíos en los tres años

- **Categoría:** Código del Trabajo
- **Tipo / severidad:** Maestro incompleto / Alta
- **Estado:** Corregido en v2 y canónico
- **Evidencia:** Las 15 columnas textuales crudas estaban vacías en 933/933 filas; _archivo_origen también estaba vacío en 933/933, incluido 2023.
- **Impacto:** Pérdida de contexto publicado y de trazabilidad directa en el maestro manual.
- **Decisión / acción:** Restaurar 14.928 celdas (incluido origen) desde CSV; conservar ID, nombre depurado, género, estamento y numéricos. Control numérico: 0 diferencias.
- **Pendiente:** Ninguno para la restauración; el original permanece intacto.

## H-005 — Una fila de mayo de 2025 está en el CSV de julio

- **Categoría:** Código del Trabajo
- **Tipo / severidad:** Período en contenido / Media
- **Estado:** Documentado y trazado
- **Evidencia:** 07_CODTrabajo_Julio_2025.csv, fila CSV 29: FERNANDEZ CIFUENTES, GAIL MIRASLAVA BERNARDA, Año=2025, Mes=Mayo. La fila de mayo en 05_CODTrabajo_Mayo_2025.csv, fila 9, tiene igual bruto pero líquido distinto ($1.394.922 vs $1.394.849).
- **Impacto:** Dos registros para la misma persona y período; no son duplicados exactos.
- **Decisión / acción:** Conservar ambos, con período 2025-05 y archivos/filas distintos; no deduplicar sin respaldo.
- **Pendiente:** Solicitar aclaración al publicador si se requiere una única cifra oficial para ese mes.

## H-006 — Una fila de noviembre de 2024 está en el CSV de diciembre

- **Categoría:** Planta
- **Tipo / severidad:** Período en contenido / Media
- **Estado:** Documentado y trazado
- **Evidencia:** 12_Planta_Diciembre_2024.csv, fila CSV 132: CARO PARRA, CARMEN SALOME, Mes=Noviembre. También existe registro en 11_Planta_Noviembre_2024.csv, fila 25; brutos y líquidos difieren.
- **Impacto:** Dos registros para la misma persona y período; no son duplicados exactos.
- **Decisión / acción:** Conservar ambos con período 2024-11 y trazabilidad separada; no deduplicar.
- **Pendiente:** Solicitar aclaración al publicador si se requiere una única cifra oficial para ese mes.

## H-007 — Resumen Trabajadores contiene repeticiones masivas de ID

- **Categoría:** Planta
- **Tipo / severidad:** Resumen heredado / Alta
- **Estado:** Excluido de salidas nuevas
- **Evidencia:** La hoja Resumen Trabajadores tiene 757 filas pero solo 178 ID_Trabajador únicos; 579 filas repiten un ID. Datos Completos tiene 178 IDs y 178 nombres normalizados únicos.
- **Impacto:** Los agregados de esa hoja no son una tabla única confiable por trabajador.
- **Decisión / acción:** No copiar hojas analíticas heredadas a v2/canónico; recalcular desde Datos cuando se necesiten.
- **Pendiente:** Reconstruir resumen solo bajo una regla explícita de unicidad.

## H-008 — Diciembre de 2025 tiene Año y Mes sin informar

- **Categoría:** Autoridades
- **Tipo / severidad:** Período faltante en contenido / Media
- **Estado:** Pendiente aclaración
- **Evidencia:** 12_ElectosyOtros_Diciembre_2025.csv contiene 8 registros con Año=- y Mes=-; renta bruta publicada como UTM 15,60.
- **Impacto:** El período solo puede inferirse del nombre/ruta, no del contenido; la renta bruta está expresada en UTM.
- **Decisión / acción:** No incorporar a los cuatro maestros canónicos ni imputar Año/Mes; conservar evidencia.
- **Pendiente:** Confirmar período y conversión UTM aplicable antes de integrar autoridades.

## H-009 — Columnas Unnamed vacías

- **Categoría:** Todas
- **Tipo / severidad:** Estructura CSV / Informativa
- **Estado:** Verificado
- **Evidencia:** Se detectaron 166 columnas Unnamed en los CSV y 0 celdas no vacías en ellas.
- **Impacto:** Separadores finales generan columnas auxiliares sin información.
- **Decisión / acción:** Excluirlas tras verificar que están completamente vacías.
- **Pendiente:** Repetir esta verificación en cada nueva categoría/lote.

## H-010 — Informes eliminados en Dropbox y ausencia histórica de enlaces

- **Categoría:** Honorarios
- **Tipo / severidad:** Disponibilidad de enlaces / Alta
- **Estado:** Verificado con reintento directo
- **Evidencia:** 9464 relaciones trabajador-mes-URL procesadas: 6057 registros tienen PDF confirmado (5991 archivos únicos). La descarga v1 ya reescribía dl=0 a dl=1. Una prueba controlada sobre tres URL recuperadas mostró que la misma dirección con dl=1 puede alternar PDF y HTML con ambos agentes de usuario; por tanto, el artefacto se vincula a respuestas variables de Dropbox y no al parámetro dl=0 ni a un cliente específico. En v2 se reintentaron 5,099 objetos con dl=1: 4,794 PDF recuperados, 123 con respuesta explícita File Deleted, 182 con Link Temporarily Disabled y 0 con otros estados. El reintento redujo en 4,853 los registros inicialmente clasificados como no recuperables. Quedan 313 registros con URL sin PDF ({'dropbox_link_temporarily_disabled': 186, 'dropbox_file_deleted': 127}) y 3094 registros sin URL: 3051 de 2023 y 43 de 2024-2025. Evidencia en REINTENTOS_DROPBOX_H010_v1.xlsx y MANIFIESTO_DESCARGAS_v2.xlsx.
- **Impacto:** La eliminación explícita de un archivo, otros errores de descarga y la ausencia de URL son condiciones distintas. No toda respuesta HTML HTTP 200 equivale a un archivo eliminado: la clasificación File Deleted se basa en el título explícito devuelto por Dropbox tras solicitar dl=1; las deshabilitaciones temporales y otros estados se mantienen separados.
- **Decisión / acción:** Conservar URL original, URL efectiva, variantes, códigos HTTP, títulos, fechas y SHA-256. Incorporar únicamente respuestas con firma PDF válida; mantener v1 como antecedente y v2 como manifiesto vigente.
- **Pendiente:** Solicitar reposición o rehabilitación de los documentos eliminados o temporalmente deshabilitados y gestionar la ausencia histórica de enlaces de 2023. Revisar por separado cualquier otro estado residual.

## Duplicados período–nombre conservados

Las dos situaciones de Código del Trabajo y Planta descritas en H-005 y H-006 permanecen porque difieren en valores y/o archivo fuente. La hoja `Duplicados período-nombre` del registro Excel contiene los identificadores y cifras.