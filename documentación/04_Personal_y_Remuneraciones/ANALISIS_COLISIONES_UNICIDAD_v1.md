# Análisis forense de colisiones persona-período — propuesta D-15

**Categoría:** Personal y Remuneraciones  
**Fecha:** 2026-11-17  
**Insumos:** cuatro CSV originales y maestros `canonico_v1.0.0`  
**Estado:** propuesta para evaluación en coordinación; **no aplicada** a maestros ni al pipeline  
**Compuerta:** las cuatro filas se conservan; no se borra, promedia ni altera ninguna cifra

## 1. Conclusión ejecutiva

Las dos colisiones presentan el mismo patrón documental: una fila cuyo `Año`/`Mes` declarado coincide con el período nominal de su archivo y otra fila del mismo trabajador y período incorporada como **única fila fuera de período y en la última posición** del archivo del mes siguiente.

No son duplicados exactos. En Código del Trabajo cambia únicamente el líquido; en Planta cambian las asignaciones especiales, el bruto y el líquido. Ambas versiones posteriores podrían ser correcciones o reajustes retroactivos, pero **ninguna contiene una observación, fecha de rectificación u otro marcador que lo demuestre**.

Se propone D-15 como regla de **selección para visualización de trayectoria**, no como depuración del dataset:

> Dentro de una colisión `categoria + id_trabajador + periodo`, si existe exactamente una versión cuyo período declarado coincide con el período nominal de su archivo, esa versión alimenta la trayectoria. Las demás se rotulan `version_alterna` y permanecen íntegramente disponibles con su trazabilidad.

La opción contraria —asumir que la publicación posterior es una corrección oficial— se descarta como regla automática porque la presunta posterioridad deriva solo del nombre del archivo y no existe evidencia formal de rectificación. Se contempla una excepción documentada para cuando sí exista esa evidencia.

## 2. Método, alcance y reproducibilidad

Se ejecutó:

```bash
python "scripts/analizar_colisiones_unicidad.py"
```

El script:

1. Lee los cuatro CSV con la misma rutina de decodificación del saneamiento.
2. Extrae todos los campos de las cuatro filas y sus equivalentes canónicos, incluidos campos `_raw`, observaciones, asignaciones y trazabilidad.
3. Calcula la distribución `Año`/`Mes` de cada archivo completo y las filas fuera de su período nominal.
4. Compara cada par campo por campo, tanto en crudo como en el canónico.
5. Revisa las 22.940 filas canónicas por nombre y período, distinguiendo colisiones dentro de categoría y transversales.
6. Simula la selección propuesta sin escribir en los maestros.

La evidencia completa, incluidas las filas íntegras y las comparaciones exactas, quedó en:

`trabajo/04_Personal_y_Remuneraciones/analisis_colisiones_unicidad.json`

La numeración usada considera el encabezado como fila CSV 1. No se encontraron PDF de estas planillas en `datos crudos` ni copias documentales equivalentes en `archivo externo`; por tanto, este análisis se limita a los CSV y al canónico disponible. No se afirma un cotejo independiente contra el PDF o el portal.

## 3. Evidencia de los cuatro archivos

| Archivo | Fila analizada | Filas de datos | Distribución por contenido | Posición de la excepción | SHA-256 |
|---|---:|---:|---|---|---|
| `05_CODTrabajo_Mayo_2025.csv` | 9 | 27 | 27 en 2025-05 | No hay excepciones | `9643364813d70e193efa40eaf7739fccbb04eafa3fc250b3ed50b385ef0880d8` |
| `07_CODTrabajo_Julio_2025.csv` | 29 | 28 | 27 en 2025-07; 1 en 2025-05 | Última fila; única fuera de 2025-07 | `5dd2c396042e17cd6c1a45955cfa6c22c65e2d37d87f161447c77f77d5fbd4b7` |
| `11_Planta_Noviembre_2024.csv` | 25 | 131 | 131 en 2024-11 | No hay excepciones | `878d2cfa3b86c141a813724d00680c9de85686e403971d1518e464f5c73e84c1` |
| `12_Planta_Diciembre_2024.csv` | 132 | 131 | 130 en 2024-12; 1 en 2024-11 | Última fila; única fuera de 2024-12 | `bad153e30fec298ba714282e3c60048fc44137a74cd4d47161f48cd72da8144f` |

El período dominante coincide con el nominal en los cuatro archivos. Julio de 2025 no contiene una reedición completa de mayo: contiene 27 filas de julio y una de mayo. Diciembre de 2024 tampoco reedita noviembre: contiene 130 filas de diciembre y una de noviembre.

## 4. Caso COT-2023-0015 — 2025-05

**Persona:** FERNANDEZ CIFUENTES, GAIL MIRASLAVA BERNARDA.

Se compararon los 20 campos crudos, incluidos cargo, grado/jornada, calificación, región, asignaciones, importes, derecho y montos de horas extra, fechas, observaciones y la columna auxiliar vacía. También se contrastaron sus campos canónicos y `_raw`.

| Campo | Mayo, fila 9 | Julio, fila 29 | Diferencia posterior − nominal |
|---|---|---|---:|
| Período declarado | 2025 / Mayo | 2025 / Mayo | Igual |
| Asignaciones especiales | `(131)` | `(131)` | Igual |
| Remuneración bruta | $1.541.381 | $1.541.381 | $0 |
| **Remuneración líquida** | **$1.394.922** | **$1.394.849** | **−$73** |
| Cargo | SECRETARIA DEPTO CONTABILIDAD | Igual | — |
| Calificación | SECRETARIA EJECUTIVA | Igual | — |
| Fecha de inicio / término | 01/01/2025 / Indefinido | Igual | — |
| Horas extraordinarias | No / No tiene | Igual | — |
| Observaciones | Sin Observaciones | Sin Observaciones | Igual |

Todos los demás campos crudos son iguales. En el canónico solo cambian `remuneracion_liquida_raw`, `remuneracion_liquida_clp`, el identificador del registro y la trazabilidad de fuente.

**Caracterización:** republicación aislada de un registro fuera del período nominal del archivo, con una diferencia menor de líquido. Es compatible con una corrección posterior, pero también con otra variante de captura. No es un duplicado exacto y no hay evidencia suficiente para declarar una corrección oficial. El traslape período-contenido versus período-archivo sí está demostrado.

## 5. Caso PLT-2023-0032 — 2024-11

**Persona:** CARO PARRA, CARMEN SALOME.

Se compararon los 22 campos crudos y sus equivalentes canónicos. Las diferencias sustantivas son:

| Campo | Noviembre, fila 25 | Diciembre, fila 132 | Diferencia posterior − nominal |
|---|---|---|---:|
| Período declarado | 2024 / Noviembre | 2024 / Noviembre | Igual |
| Estamento | Profesional | Profesional | Igual |
| Asignaciones especiales | `(37)(131)` | `(33)(37)(131)` | Se agrega `(33)` |
| **Remuneración bruta** | **$2.094.352** | **$2.796.012** | **+$701.660** |
| **Remuneración líquida** | **$2.225.384** | **$2.225.573** | **+$189** |
| Cargo | JEFA DEPTO. GAB. PSICOTÉCNICO | Igual | — |
| Calificación | MEDICO CIRUJANO | Igual | — |
| Fecha de inicio / término | 01/02/1995 / Indefinido | Igual | — |
| Horas extraordinarias | No / No tiene en las tres clases | Igual | — |
| Observaciones | `Sin Observaciones` | `SIN OBSERVACIONES` | Solo capitalización |

Los demás campos sustantivos son iguales. En el canónico cambian `asignaciones_especiales_raw`, bruto raw/CLP, líquido raw/CLP, identificador y trazabilidad. Las cifras se reproducen como fueron publicadas; no se infiere una explicación aritmética ni se ajusta el bruto o el líquido.

**Caracterización:** republicación aislada fuera de período con una modificación sustantiva de la composición del bruto y una variación pequeña del líquido. La incorporación de `(33)` hace plausible una corrección o un reajuste retroactivo, pero no lo prueba. No es duplicado exacto ni una reedición del archivo completo; el traslape de período está demostrado.

## 6. Revisión de casos análogos

### 6.1 Dentro de una misma categoría

El barrido por `categoria + nombre_normalizado + periodo` encontró:

| Resultado | Grupos |
|---|---:|
| Grupos con más de una fila | 2 |
| Grupos con el mismo `id_trabajador` | 2 |
| Grupos con IDs distintos | **0** |

Los dos grupos son exactamente COT-2023-0015 / 2025-05 y PLT-2023-0032 / 2024-11. **No existen otros pares análogos dentro de una categoría que colisionen por nombre+período pero no por ID.** Por tanto, la regla propuesta no tiene más casos bloqueantes que estos dos en el canónico actual.

### 6.2 Entre categorías

Existen 24 grupos nombre+período con IDs distintos entre categorías, que involucran 49 registros:

- 22 grupos Código del Trabajo–Planta.
- 2 grupos Contrata–Planta.

No son equivalentes a las colisiones bloqueantes: los IDs heredados tienen alcance por categoría y una misma persona puede tener publicaciones en estamentos distintos. Tampoco debe fusionarse gente solo por nombre. Estos grupos quedan **fuera del alcance de D-15**.

Las 56 advertencias de identidad transversal descritas en `VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md` constituyen otro problema de gobernanza. D-15 no las resuelve ni habilita por sí sola una ficha global.

## 7. Propuesta de decisión D-15

### 7.1 Alcance

La regla opera únicamente sobre una proyección destinada a trayectoria individual, agrupada por:

`categoria + id_trabajador + periodo`

No opera por nombre global, no cruza estamentos y no modifica el período obtenido del contenido conforme a D-07.

### 7.2 Regla de selección

1. Identificar el período nominal del archivo como metadato de procedencia, sin usarlo para sustituir `Año`/`Mes` del contenido.
2. Si el grupo contiene **exactamente una** versión cuyo período declarado coincide con ese período nominal, marcarla `canonica_trayectoria`.
3. Marcar las demás versiones del grupo como `version_alterna`, con el motivo `periodo_contenido_distinto_de_periodo_nominal_archivo` y referencia a la versión seleccionada.
4. Si hay cero o más de una versión nominalmente coincidente, la colisión permanece sin resolver automáticamente. No usar orden de fila, monto mayor, líquido mayor ni posterioridad presumida como desempate.
5. Si existe evidencia formal de rectificación —observación explícita, metadato de versión, fecha de publicación o confirmación documental— evaluar una excepción que seleccione la versión corregida. La excepción debe quedar justificada registro por registro.

Etiquetas conceptuales para una futura proyección, no agregadas en este encargo:

| Campo | Contenido propuesto |
|---|---|
| `rol_trayectoria` | `canonica_trayectoria` o `version_alterna` |
| `regla_resolucion` | `D-15_coincidencia_periodo_nominal` |
| `version_alterna_de` | `registro_id` de la fila seleccionada |
| `motivo_version_alterna` | Explicación visible y trazabilidad de la otra publicación |

### 7.3 Preservación y efectos

- Las 22.940 filas canónicas permanecen intactas.
- Las cuatro versiones siguen disponibles para consulta y auditoría.
- Los agregados continúan calculándose conforme a D-07, con ambas filas; D-15 no cambia sumas ni totales.
- La ficha debe mostrar la versión alterna bajo una sección como “Otra publicación del mismo período”, nunca ocultarla.
- La trayectoria seleccionada no debe presentarse como prueba de cuál cifra es jurídicamente correcta; es una convención documental explícita.
- Como los agregados y la proyección de trayectoria tienen reglas distintas, la interfaz debe evitar presentar la suma de fichas como reconciliación de los agregados.

## 8. Alternativas evaluadas

| Alternativa | Fundamento a favor | Objeción | Evaluación |
|---|---|---|---|
| **Coincidencia con período nominal** | Reproducible; usa el contexto documental sin alterar el período de contenido; distingue la publicación mensual nativa de una fila excepcional anexada en otro archivo | El nombre de archivo puede contener errores y no prueba cuál cifra es correcta | **Propuesta**, con las condiciones y excepciones anteriores |
| **Prevalencia de la publicación posterior como corrección oficial** | En Planta se agrega `(33)` y podría representar un reajuste; en COT la diferencia de $73 podría ser una rectificación | No hay fecha independiente de publicación ni marca de rectificación. La “posterioridad” también se infiere del nombre; convertiría una hipótesis en regla | No automática. Admitir solo con evidencia formal |
| Mantener siempre ambas en la trayectoria | No requiere elegir | Mantiene dos valores para un mismo mes y la compuerta rechazada | No resuelve el problema de producto |
| Borrar, promediar o escoger por monto | Produciría una cifra única | Destruye evidencia o inventa un valor no publicado | Rechazada |
| Regla global por nombre+período | Detectaría más coincidencias | Puede mezclar personas o estamentos y no respeta el alcance de los IDs | Rechazada |

## 9. Aplicación simulada a los dos casos

| Caso | `canonica_trayectoria` | `version_alterna` | Motivo |
|---|---|---|---|
| COT-2023-0015 / 2025-05 | `COT-202505-8DA800BA00`; mayo fila 9; bruto $1.541.381; líquido $1.394.922 | `COT-202505-9D0CE3F70A`; julio fila 29; bruto $1.541.381; líquido $1.394.849 | La versión de mayo coincide contenido/archivo; la de julio es la única fila fuera de período |
| PLT-2023-0032 / 2024-11 | `PLT-202411-8247F5515D`; noviembre fila 25; bruto $2.094.352; líquido $2.225.384 | `PLT-202411-3B54A1958D`; diciembre fila 132; bruto $2.796.012; líquido $2.225.573 | La versión de noviembre coincide contenido/archivo; la de diciembre es la única fila fuera de período |

## 10. Trayectoria resultante

Las tablas siguientes muestran únicamente las filas que alimentarían la trayectoria. Las versiones alternas permanecen en las tablas anteriores y en el canónico. Los importes están en CLP.

### 10.1 COT-2023-0015

| Período | Bruto | Líquido | Fuente |
|---|---:|---:|---|
| 2025-01 | 1.541.381 | 1.412.556 | `01_CODTrabajo_Enero_2025.csv`, fila 14 |
| 2025-02 | 1.541.381 | 1.412.483 | `02_CODTrabajo_Febrero_2025.csv`, fila 13 |
| 2025-03 | 1.541.381 | 1.394.755 | `03_CODTrabajo_Marzo_2025.csv`, fila 12 |
| 2025-04 | 1.541.381 | 1.394.829 | `03_CODTrabajo_Abril_2025.csv`, fila 9 |
| **2025-05** | **1.541.381** | **1.394.922** | `05_CODTrabajo_Mayo_2025.csv`, fila 9 |
| 2025-09 | 61.552 | 61.552 | `09_CODTrabajo_Septiembre_2025.csv`, fila 10 |
| 2025-12 | 36.427 | 36.427 | `12_CODTrabajo_Diciembre_2025.csv`, fila 12 |

Resultado: 7 períodos únicos. La fila de julio con contenido 2025-05 queda disponible como alterna. No hay registros de este ID en 2023-2024 ni en 2025-06, 2025-07, 2025-08, 2025-10 o 2025-11; esas ausencias no se imputan.

### 10.2 PLT-2023-0032

| Período | Bruto | Líquido | Fuente |
|---|---:|---:|---|
| 2023-01 | 993.499 | 829.500 | `01_Planta_Enero_2023.csv`, fila 32 |
| 2023-02 | 993.499 | 829.374 | `02_Planta_Febrero_2023.csv`, fila 31 |
| 2023-03 | 993.499 | 829.473 | `03_Planta_Marzo_2023.csv`, fila 31 |
| 2023-04 | 993.499 | 829.461 | `04_Planta_Abril_2023.csv`, fila 27 |
| 2023-05 | 1.028.347 | 864.161 | `05_Planta_Mayo_2023.csv`, fila 27 |
| 2023-06 | 1.028.347 | 864.199 | `06_Planta_Junio_2023.csv`, fila 27 |
| 2023-07 | 993.499 | 829.584 | `07_Planta_Julio_2023.csv`, fila 27 |
| 2024-09 | 832.117 | 711.294 | `09_Planta_Septiembre_2024.csv`, fila 25 |
| 2024-10 | 2.094.352 | 2.238.811 | `10_Planta_Octubre_2024.csv`, fila 25 |
| **2024-11** | **2.094.352** | **2.225.384** | `11_Planta_Noviembre_2024.csv`, fila 25 |
| 2025-01 | 3.232.165 | 2.626.946 | `01_Planta_Enero_2025.csv`, fila 25 |
| 2025-02 | 2.913.402 | 2.322.081 | `02_Planta_Febrero_2025.csv`, fila 25 |
| 2025-03 | 2.913.402 | 2.322.016 | `03_Planta_Marzo_2025.csv`, fila 25 |
| 2025-04 | 2.913.402 | 2.321.563 | `04_Planta_Abril_2025.csv`, fila 26 |
| 2025-05 | 2.913.402 | 2.334.866 | `05_Planta_Mayo_2025.csv`, fila 25 |
| 2025-06 | 2.930.399 | 2.347.881 | `06_Planta_Junio_2025.csv`, fila 26 |
| 2025-07 | 2.930.399 | 2.348.086 | `07_Planta_Julio_2025.csv`, fila 26 |
| 2025-08 | 2.930.399 | 2.347.678 | `08_Planta_Agosto_2025.csv`, fila 25 |
| 2025-09 | 2.991.951 | 2.410.141 | `09_Planta_Septiembre_2025.csv`, fila 25 |
| 2025-10 | 2.930.399 | 2.348.589 | `10_Planta_Octubre_2025.csv`, fila 25 |
| 2025-11 | 2.930.399 | 2.349.149 | `11_Planta_Noviembre_2025.csv`, fila 25 |
| 2025-12 | 2.966.826 | 2.386.707 | `12_Planta_Diciembre_2025.csv`, fila 25 |

Resultado: 22 períodos únicos. La fila de diciembre con contenido 2024-11 queda disponible como alterna. No se imputan los períodos sin registro: 2023-08 a 2023-12, 2024-01 a 2024-08 y 2024-12.

## 11. Huellas de los maestros analizados

| Maestro canónico | SHA-256 |
|---|---|
| `MAESTRO_Planta_Coronel_2023-2025_canonico_v1.xlsx` | `9fc5e4a1784a9b43284c1af1c47de117f3abd9576d61e9b206ecb1135bf45a8e` |
| `MAESTRO_CODTrabajo_Coronel_2023-2025_canonico_v1.xlsx` | `c843d1759055b68c281f9d88886b28d67f5e072905d759228002ff1d8a21f6ea` |
| `MAESTRO_Contrata_Coronel_2023-2025_canonico_v1.xlsx` | `578061f907e8f584f01ae5220302037a1c3f1836dca154b279903036c2d57fda` |
| `MAESTRO_Honorarios_Coronel_2023-2025_canonico_v1.xlsx` | `860d1fc0d005be9a3722451cef15f56dc79ff21b5c00734c8801a04e676d3bde` |

## 12. Decisión requerida y límites

Se propone registrar D-15 en coordinación con la regla de coincidencia nominal, sus condiciones de no resolución y la excepción por rectificación documentada. Solo después de esa aprobación correspondería implementar una proyección de trayectoria y repetir la validación.

La simulación elimina las dos colisiones dentro de la proyección, dejando 7 y 22 períodos únicos respectivamente, sin eliminar ninguna fila del canónico. **No resuelve la identidad transversal ni autoriza por sí sola la ficha global.** No se modificaron los maestros canónicos, los CSV originales ni el pipeline.
