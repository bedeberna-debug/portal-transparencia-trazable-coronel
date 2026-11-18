# BITÁCORA DE TRANSFORMACIONES — INFORMACIÓN PRESUPUESTARIA

**Proyecto:** Portal de Transparencia Trazable – Municipalidad de Coronel  
**Versión del esquema:** canonico_v1.0.0  
**Fecha:** 2026-11-15  
**Criterio rector:** fuentes originales intocables, trazabilidad total y ausencias declaradas.

## 1. Congelar fuentes e inventariar

Se inventariaron **141 PDF** con ruta, tamaño y SHA-256: 71 BEP y 70 ESP. La referencia inicial de 143 difiere del inventario físico; no se completaron registros. Julio de 2025 no está publicado en ninguna familia ni tipo.

## 2. Comparar nombre y período del contenido

El período se obtiene del encabezado impreso y se contrasta con el nombre. La v2 BEP de enero de 2023 carece de encabezado: se asoció documentalmente al original, se conservó por separado y quedó en cuarentena por contenido distinto (95 versus 97 líneas). Los 70 ESP tienen fecha de corte y título en el contenido.

## 3. Perfilar formularios, columnas y catálogos

Los BEP usan Formulario 0101/0102, cinco columnas en M$. Los ESP son Estados Presupuestarios: gastos tiene 11 columnas e ingresos 9, todas en CLP. Se validaron contra `clasificador.json`; nunca contra `plan_municipal.json`. No se infirió un número de formulario para ESP.

## 4. Definir claves y versionado

La clave canónica es documento–código; `registro_id` añade SHA-256, página y línea. Original y republicación se conservan separados. Para la serie BEP de enero de 2023 se usa el original aceptado, no la v2 cuarentenada.

## 5. Contrastar filas y totales

BEP aceptado: 330/330 totales. ESP de gastos: 385/385 totales con umbrales estrictos. En ingresos, las ocho métricas distintas de saldo por percibir calzan 280/280; el noveno total se rige por D-13. Cada uno de los 35 documentos reprodujo individualmente las tres condiciones: ocho totales, identidad del total oficial y reconciliación exacta con la cuenta 15. Se rehabilitaron 35 y permanecen 0 en cuarentena. Los controles clásicos agregados se reportan como informativos, no como criterio D-13.

## 6. Restaurar campos sin sobrescribir

No se corrigieron cifras ni se modificaron PDF. Las salidas son archivos nuevos; los parseos y controles de cuarentena permanecen en `trabajo`.

## 7. Aplicar esquema canónico y conservar raw

BEP conserva siete métricas en M$; ESP conserva la unión de 15 métricas en CLP. Cada métrica tiene `_raw`. Los campos no aplicables quedan vacíos. No se remapearon códigos ni se imputaron ausencias.

## 8. Añadir trazabilidad

El canónico BEP contiene 11616 registros y el ESP 32112. Cada registro incluye archivo, ruta, página, línea y SHA-256. Cada delta BEP enlaza IDs y trazabilidad de ambos cortes. Cada ESP documenta además el título literal y su ubicación.

## 9. Separar decisiones no reproducibles o pendientes

No hubo correcciones manuales. Los códigos fuera del catálogo se conservan como hallazgo de cobertura/versionado. Los ESP son tipo documental separado. D-13 documenta la regla de agregación del saldo por percibir en ingresos y la rehabilitación condicionada por documento; no altera cifras ni remapea cuentas. TP-18 queda descartada porque el mecanismo está explicado y no hay vacío que requiera solicitud.

## 10. Ejecutar controles, tolerancia BEP y cuarentenas

BEP: 66 aceptados y 5 en cuarentena. La política refinada incorporó 28 gastos con diferencias jerárquicas ≤2 M$, anexo permanente y verificación visual 10/10.

ESP: 35 gastos aceptados por umbrales estrictos y 35 ingresos aceptados por D-13; 0 ESP en cuarentena. La tolerancia BEP de 2 M$ no se aplicó a ESP. D-13 no cambia los ceros de la cuenta 15 ni ningún otro dato impreso. El canónico y la tabla de totales conservan `total_saldo_por_percibir_oficial_clp` y `saldo_por_percibir_suma_detalle_clp` como campos distintos.

## 11. Registrar hallazgos y derivar deltas

Se generaron 52.200 deltas BEP, 57636 deltas ESP de cuentas y 340 deltas ESP de totales. Se registraron 53 cuentas sin delta por ausencia en un corte; no se imputaron ceros. Solo se unen meses consecutivos aceptados. Julio de 2025 no genera datos y agosto no salta julio. La serie oficial y la suma del detalle permanecen separadas.

## 12. Versionar entregables y reproducción

Entregables v1 actualizados: canónicos BEP/ESP, controles D-13, tabla de ambos totales, series BEP y ESP de ingresos, coberturas, hallazgos, diccionario, bitácora, gobernanza D-13/TP-18 y validación final. Reproducción desde la raíz: `python scripts/aplicar_rehabilitacion_d13_esp.py`; `python scripts/construir_canonico_esp_etapa2.py`; `python scripts/construir_series_d13_esp.py`; repetir la construcción del canónico para consolidar hallazgos de deltas; `python scripts/documentar_rehabilitacion_d13.py`; `python scripts/validar_final_etapa2.py`. Los PDF originales permanecen intocables.
