# Verificación del índice oficial de asignaciones especiales

**Versión:** v1.  
**Fecha de obtención de fuentes:** 2026-11-18.  
**Resultado:** índice oficial decodificado y contraste reproducible con el canónico.  
**Compuerta:** no se modificó el canónico ni la plataforma.

## 1. Fuentes, fecha y hashes

La fuente primaria es la Guía Operativa de Publicación de Personal y Remuneraciones del CPLT y sus archivos asociados al Oficio N.° 22.003/2025. El libro `Tipologias-y-Asignaciones-Especiales.xlsx`, hoja `Asignaciones especiales`, contiene **394 conceptos (01–394)** y es la fuente del índice. El PDF municipal de Quintero contiene 131 conceptos y se usa solo como respaldo histórico.

| Insumo | URL | Fecha de obtención | SHA-256 |
|---|---|---|---|
| guia_cplt.html | https://www.consejotransparencia.cl/portal-de-transparencia/guia-pte-publicacion-remuneraciones/ | 2026-11-18T01:37:29.912076-03:00 | `b907bb38749468c67ae77812086e1341477635eaaee83905a1812f603e1b7b41` |
| OficioN22003-2025.pdf | https://www.consejotransparencia.cl/transparencia_activa/AvisosPortal/OficioN22003-2025.pdf | 2026-11-18T01:37:30.125979-03:00 | `2855abd88245a40f3092196c0f465f298b4575c1daddb4d3ff30c3c8bd977528` |
| Tipologias-y-Asignaciones-Especiales.xlsx | https://www.consejotransparencia.cl/transparencia_activa/datoabierto/archivos/Tipologias-y-Asignaciones-Especiales.xlsx | 2026-11-18T01:37:30.289466-03:00 | `0e3ae33f0735a0f596741b639654cf73017e7dd9f61f08c11765b8491664ddd1` |
| ListasCamposCsv.xlsx | https://www.consejotransparencia.cl/transparencia_activa/datoabierto/archivos/ListasCamposCsv.xlsx | 2026-11-18T01:37:30.414606-03:00 | `1236e5f4494c57d98cc03a3f8ce9bfc4283d300d46f06630be509811ead922e4` |
| Asignaciones_Especiales_muniquintero.pdf | http://discap.muniquintero.cl/gobiernotransparente/archivos%20compartidos/5.%20Dotacion%20de%20Personal/5.1%20Personal%20Ilustre%20Municipalidad%20de%20Quintero/Asignaciones%20Especiales.pdf | 2026-11-18T01:37:30.576168-03:00 | `9d312bd497632f3b78eaf0479c0033a5cb52a5f7ceb7355444b398fd978f4456` |

El Oficio instruye publicar el código de cada asignación en la columna correspondiente (numeral 15) y permite el código 01 cuando no hubo percepción (numeral 16). La guía enlaza expresamente el libro de tipologías y asignaciones.

## 2. Artefacto de decodificación

Se generó `asignaciones_indice.json` con 394 entradas. Cada entrada contiene código, nombre oficial literal, base legal cuando hay una referencia en el propio nombre, y archivo/hoja/fila SHA-256 de origen. El libro no declara una versión interna; por ello `version_tabla` es un identificador de proyecto basado en el Oficio y la fecha de descarga, no una versión oficial supuesta.

La hoja oficial no tiene una columna independiente de base legal. Para no inventar contenido, `base_legal` conserva una subcadena literal del nombre desde la primera referencia normativa detectada; si no hay referencia, es `null`. Los nombres no fueron corregidos ni interpretados.

### Irregularidades literales de la fuente oficial

Se conservó `codigo_fuente_literal` y se normalizó únicamente el identificador `codigo_cplt`. Las diferencias siguientes pertenecen al archivo oficial; no se modificó el insumo.

| Fila XLSX | Literal fuente | Identificador normalizado | Concepto oficial |
|---|---|---|---|
| 286 | 285) | (285) | Bonificación Ley 15.386 Art. 19 |

### Comparación con el respaldo de Quintero

Los códigos 01–131 están presentes en ambas fuentes. Al comparar nombres normalizando solo espacios, acentos, mayúsculas y puntuación, **129 coinciden** y **2 presentan diferencias textuales**. Una diferencia textual no se traduce automáticamente en cambio de significado.

No se detectaron diferencias textuales en los códigos observados en el canónico al contrastarlos con el respaldo.

## 3. Diseño de verificación

- Muestra determinista: 30 registros por categoría-año, `random_state=20261118`, en Planta, Contrata y Código del Trabajo para 2023, 2024 y 2025: **270 registros**.
- Honorarios no posee la columna `asignaciones_especiales_raw`; sus tres estratos se declaran **no aplica por ausencia estructural del campo**, no se muestrean como si tuvieran código 01.
- Se extrajeron únicamente tokens entre paréntesis. Los códigos numéricos se normalizaron a dos dígitos para 01–99; se conservaron tokens inválidos y residuos como anomalías, sin forzar conversiones.
- Como control complementario se censaron todos los códigos de los **13.476 registros** que sí poseen el campo, sin sustituir la muestra solicitada.
- Las sospechas semánticas son señales de revisión, no errores probados: el canónico no contiene unidad/departamento, y un cargo administrativo puede pertenecer a un área sanitaria o al JPL.

### Cobertura por estrato

| Categoría | Año | Registros | Estado | Muestra | Códigos distintos | Sin correspondencia | Malformados | Sospecha semántica |
|---|---|---|---|---|---|---|---|---|
| Contrata | 2023 | 2284 | muestreado | 30 | 11 | 0 | 0 | 6 |
| Contrata | 2024 | 2659 | muestreado | 30 | 8 | 0 | 0 | 0 |
| Contrata | 2025 | 2673 | muestreado | 30 | 8 | 0 | 0 | 0 |
| Código del Trabajo | 2023 | 281 | muestreado | 30 | 7 | 0 | 0 | 0 |
| Código del Trabajo | 2024 | 285 | muestreado | 30 | 7 | 0 | 0 | 0 |
| Código del Trabajo | 2025 | 367 | muestreado | 30 | 6 | 0 | 0 | 0 |
| Honorarios | 2023 | 3051 | no_aplica_campo_ausente | 0 | N/A | N/A | N/A | N/A |
| Honorarios | 2024 | 3076 | no_aplica_campo_ausente | 0 | N/A | N/A | N/A | N/A |
| Honorarios | 2025 | 3337 | no_aplica_campo_ausente | 0 | N/A | N/A | N/A | N/A |
| Planta | 2023 | 1800 | muestreado | 30 | 11 | 0 | 0 | 7 |
| Planta | 2024 | 1606 | muestreado | 30 | 8 | 0 | 0 | 0 |
| Planta | 2025 | 1521 | muestreado | 30 | 8 | 0 | 0 | 0 |

## 4. Códigos sin correspondencia o malformados

- Muestra: **0 códigos sin correspondencia** y **0 registros malformados**.
- Censo complementario: **0 códigos sin correspondencia** y **1 registro malformado**.

Todos los códigos observados existen en la tabla oficial de 394 conceptos. No se completó ninguna correspondencia por inferencia.

Registros malformados de la muestra:

Ninguno en la muestra de 270 registros.

Registros malformados detectados en el censo complementario:

| Categoría | Año | Registro | Raw | Tokens inválidos | Residuo | CSV fuente | Fila CSV |
|---|---|---|---|---|---|---|---|
| Planta | 2023 | PLT-202301-95B4374AC0 | -4 |  | -4 | 01_Planta_Enero_2023.csv | 11 |

Contraste directo con los CSV crudos, en modo de solo lectura:

- `PLT-202301-95B4374AC0`: el valor `-4` ya aparece en la columna `Asignaciones especiales del mes (inc. en rem. bruta)` de `datos crudos\04_Personal_y_Remuneraciones\01_Personal_Planta\2023\01_Planta_Enero_2023.csv`, fila física 11. El SHA-256 del CSV, `28bb47540d30eeb2dd44aa989bbfd3bd388acf798f0da62ccfc7bc976c888313`, coincide con el registrado en el canónico; por tanto, el valor malformado proviene del crudo y no de esta verificación.

El registro se conserva sin corrección ni descarte. Su interpretación requiere revisar la publicación original o el acto de pago; no se transformó `-4` en un código CPLT.

## 5. Sospechas de versión de tabla distinta por año

La presencia de códigos superiores a 131 no es una anomalía: significa que el respaldo histórico no basta y debe usarse la tabla oficial completa. La evaluación considera correspondencia por año, cambios de nombres entre fuentes y concentración temporal de anomalías.

| Categoría | Año | Códigos distintos | No presentes en respaldo | Códigos observados (censo) |
|---|---|---|---|---|
| Contrata | 2023 | 15 |  | (03) (04) (07) (12) (13) (26) (31) (32) (33) (37) (39) (40) (42) (43) (131) |
| Contrata | 2024 | 13 |  | (03) (04) (07) (12) (13) (26) (33) (37) (42) (48) (49) (72) (131) |
| Contrata | 2025 | 8 |  | (03) (12) (13) (33) (37) (42) (72) (131) |
| Código del Trabajo | 2023 | 9 | (139) | (13) (16) (33) (36) (37) (42) (87) (131) (139) |
| Código del Trabajo | 2024 | 7 | (139) | (13) (33) (37) (42) (87) (131) (139) |
| Código del Trabajo | 2025 | 7 | (139) | (03) (12) (13) (42) (87) (131) (139) |
| Planta | 2023 | 23 |  | (03) (04) (06) (07) (08) (10) (11) (12) (13) (16) (26) (28) (31) (32) (33) (36) (37) (39) (40) (42) (44) (45) (131) |
| Planta | 2024 | 8 |  | (03) (12) (13) (33) (37) (42) (72) (131) |
| Planta | 2025 | 8 |  | (03) (12) (13) (33) (37) (42) (72) (131) |

**Conclusión de versión:** no hay códigos huérfanos ni evidencia técnica de una tabla incompatible por año. Los códigos >131 tienen correspondencia en el libro oficial, aunque no en el respaldo histórico. De **1156 ocurrencias** con sospecha semántica en el censo, **1154 (99,8 %)** corresponden a 2023 y **2** a 2024; por registros, son **850 de 852 (99,8 %)** en 2023. Este fuerte predominio y la mayor diversidad de códigos de Planta y Contrata en 2023 constituyen una **sospecha de cambio de práctica de codificación o de versión**, no una prueba. El código 39 solo se observa en 2023, pero el código 26 persiste en Contrata 2024: no corresponde generalizar su desaparición. Como los nombres de los códigos usados coinciden entre CPLT y Quintero, tampoco puede atribuirse automáticamente el patrón a un cambio de leyenda. Resolver esta sospecha exige contrastar publicaciones y actos de los años involucrados, no inferir una versión.

## 6. Sospechas semánticas para el estamento o cargo

Reglas conservadoras aplicadas a la muestra y, como control complementario de frecuencia, al censo:

1. Concepto explícitamente de salud en estamento Administrativo/Auxiliar y cargo sin término sanitario.
2. Concepto de Juez de Policía Local (códigos 38/39) sin referencia JPL/juez/policía en el cargo.
3. Concepto que declara Código del Trabajo en Planta o Contrata.

Estas reglas no prueban improcedencia; identifican combinaciones que requieren revisar unidad, acto de pago y publicación original.

### Detalle en la muestra

| Categoría | Año | Código | Concepto | Estamento | Cargo | Regla | N |
|---|---|---|---|---|---|---|---|
| Contrata | 2023 | 26 | Asignación de atención primaria de salud | Administrativo | ENCARGADO MERCADO MUNICIPAL | concepto_salud_en_cargo_administrativo_auxiliar_sin_texto_sanitario | 1 |
| Contrata | 2023 | 26 | Asignación de atención primaria de salud | Administrativo | OFICIAL ADMINISTRATIVO | concepto_salud_en_cargo_administrativo_auxiliar_sin_texto_sanitario | 1 |
| Contrata | 2023 | 39 | Incentivo Juez Policía Local | Profesional | ARQUITECTO SECPLAN | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Contrata | 2023 | 39 | Incentivo Juez Policía Local | Técnico | ENCARG. DEPTO. TRANSPARENCIA | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Contrata | 2023 | 39 | Incentivo Juez Policía Local | Profesional | ENCARGADA EGIS | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Contrata | 2023 | 39 | Incentivo Juez Policía Local | Administrativo | ENCARGADO MERCADO MUNICIPAL | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Contrata | 2023 | 39 | Incentivo Juez Policía Local | Administrativo | OFICIAL ADMINISTRATIVO | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Contrata | 2023 | 39 | Incentivo Juez Policía Local | Profesional | PROFESIONAL ALCALDIA | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Planta | 2023 | 26 | Asignación de atención primaria de salud | Auxiliar | AUXILIAR | concepto_salud_en_cargo_administrativo_auxiliar_sin_texto_sanitario | 1 |
| Planta | 2023 | 26 | Asignación de atención primaria de salud | Administrativo | INSPECTOR MUNICIPAL | concepto_salud_en_cargo_administrativo_auxiliar_sin_texto_sanitario | 1 |
| Planta | 2023 | 26 | Asignación de atención primaria de salud | Administrativo | JEFE SERVICIOS GENERALES | concepto_salud_en_cargo_administrativo_auxiliar_sin_texto_sanitario | 1 |
| Planta | 2023 | 26 | Asignación de atención primaria de salud | Administrativo | OFICIAL ADMINISTRATIVO | concepto_salud_en_cargo_administrativo_auxiliar_sin_texto_sanitario | 1 |
| Planta | 2023 | 39 | Incentivo Juez Policía Local | Profesional | APOYO PROF. OFIC. VIVIENDA | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Planta | 2023 | 39 | Incentivo Juez Policía Local | Profesional | ARQUITECTO | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Planta | 2023 | 39 | Incentivo Juez Policía Local | Administrativo | INSPECTOR MUNICIPAL | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Planta | 2023 | 39 | Incentivo Juez Policía Local | Jefatura | JEFE DPTO. CONTAB. Y PPTO. | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Planta | 2023 | 39 | Incentivo Juez Policía Local | Administrativo | JEFE SERVICIOS GENERALES | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |
| Planta | 2023 | 39 | Incentivo Juez Policía Local | Administrativo | OFICIAL ADMINISTRATIVO | concepto_jpl_sin_referencia_jpl_en_cargo | 1 |

### Frecuencia en el censo complementario

| Categoría | Año | Ocurrencias | Registros distintos |
|---|---|---|---|
| Contrata | 2023 | 639 | 468 |
| Contrata | 2024 | 2 | 2 |
| Planta | 2023 | 515 | 382 |

## 7. Reproducibilidad y archivos

- `documentación/04_Personal_y_Remuneraciones/asignaciones_indice.json`: índice oficial decodificado.
- `trabajo/04_Personal_y_Remuneraciones/verificacion_asignaciones_muestra_v1.csv`: 270 registros muestrales y trazabilidad al CSV de origen.
- `trabajo/04_Personal_y_Remuneraciones/verificacion_asignaciones_censo_codigos_v1.csv`: ocurrencias censales por código.
- `trabajo/04_Personal_y_Remuneraciones/fuentes_asignaciones/manifest_fuentes.json`: manifiesto de fuentes.
- `trabajo/04_Personal_y_Remuneraciones/construir_indice_verificar_asignaciones.py`: extracción, muestreo y verificación.

Comando desde la raíz del workspace:

```bash
python "trabajo/04_Personal_y_Remuneraciones/construir_indice_verificar_asignaciones.py"
```

### SHA-256 de maestros verificados antes y después

| Categoría | SHA-256 |
|---|---|
| Planta | `9fc5e4a1784a9b43284c1af1c47de117f3abd9576d61e9b206ecb1135bf45a8e` |
| Contrata | `578061f907e8f584f01ae5220302037a1c3f1836dca154b279903036c2d57fda` |
| Código del Trabajo | `c843d1759055b68c281f9d88886b28d67f5e072905d759228002ff1d8a21f6ea` |
| Honorarios | `860d1fc0d005be9a3722451cef15f56dc79ff21b5c00734c8801a04e676d3bde` |

SHA-256 del índice JSON: `185b40dcdd929274521bbe1b7af452d34442e019e480ed5db83fcc5daee480ab`.

## 8. Limitaciones

La verificación demuestra existencia del código en la tabla, no procedencia jurídica ni conciliación del monto. Las reglas semánticas dependen del texto del cargo y estamento publicado; sin unidad/departamento no permiten afirmar que una asignación sea indebida. Para resolver las sospechas se requieren los documentos de pago o la unidad de destino, no una nueva inferencia de códigos.
