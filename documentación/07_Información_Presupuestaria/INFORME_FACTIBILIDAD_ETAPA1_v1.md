# INFORME DE FACTIBILIDAD — ETAPA 1

**Proyecto:** Portal de Transparencia Trazable — Municipalidad de Coronel  
**Ámbito:** Información Presupuestaria 2023–2025  
**Fecha de cierre de la prueba:** 14 de noviembre de 2026  
**Estado:** Etapa 1 finalizada; Etapa 2 no iniciada.

## 1. Conclusión

**La extracción es técnicamente factible, con condiciones.** Los cuatro BEP de diciembre se parsearon mediante coordenadas y reglas del formulario, con trazabilidad completa. Los 20 controles de totales impresos calzan exactamente; la jerarquía calza en 96,0 % de los controles y la aritmética de saldo en 99,7 % de las líneas.

La principal condición es normativa: el catálogo vigente representa subtítulo, ítem y asignación, pero no los niveles 4 y 5 presentes en los PDF. Además, hay 66 ocurrencias (33 códigos únicos) de niveles 1–3 ausentes del catálogo, registradas como hallazgos de cobertura/versionado normativo. No se remapeó ni corrigió ningún código o monto.

Esta conclusión se limita a los cuatro BEP analizados. No demuestra todavía la factibilidad de los ESP, de otros meses ni del procesamiento masivo. La autoevaluación no constituye aprobación del usuario ni autorización para iniciar la Etapa 2.

## 2. Muestras e identidad de las fuentes

Se eligieron los cortes acumulados al 31 de diciembre de 2023 y 2025 para maximizar la cobertura de cuentas. Los montos se expresan en miles de pesos (M$), tal como están impresos.

| Muestra | Formulario detectado | Corte declarado | Archivo | SHA-256 |
|---|---|---|---|---|
| Gastos 2023 | 0102 | 31/12/2023 | 2023bep dic municipalidad gastos.pdf | `cc5e1d9f0c71fcf35c2fefa32d58e1fb46857d20473cfb2147496f04d3b74854` |
| Ingresos 2023 | 0101 | 31/12/2023 | 2023bep dic municipalidad ingreso.pdf | `248251b16b0a113ff56e3bbfaeab0920848ff15eceac6f99edb1a68cc6d95314` |
| Gastos 2025 | 0102 | 31/12/2025 | bep dic municipalidad gastos.pdf | `1ddeb76d8893184eeddb7b03ab714d8dad0be303a43797cd6a02b0fd64cffe74` |
| Ingresos 2025 | 0101 | 31/12/2025 | bep dic municipalidad ingresos.pdf | `96eb67fb918b477743ceae5b9765edc7528dff5197f8d773e3e14437dbce6cc8` |

Los documentos de gastos usan el Formulario 0102; los de ingresos, el Formulario 0101. En consecuencia, ingresos se valida con **Percibidos / Saldo / Por percibir**, no con Devengado / Exigible. Los cuatro ejemplares indican “TRIMESTRE CUARTO” y corte acumulado al 31/12.

## 3. Método y trazabilidad

1. Extracción de palabras y coordenadas con `pdfplumber`; no se utilizó el orden lineal del texto para asignar columnas.
2. Detección del encabezado de cada página y de cinco columnas por anclas horizontales.
3. Reconstrucción del código por posición y contexto jerárquico entre páginas, incluidas líneas que imprimen dos niveles a la vez.
4. Conservación del código, denominación y cifras literales del PDF, junto con archivo, ruta relativa, página, línea textual y SHA-256.
5. Controles independientes: catálogo, suma de hijas directas por cada padre y métrica, y comparación entre TOTALES impresos y suma de subtítulos parseados.
6. Verificación independiente desde los CSV: unicidad, campos de trazabilidad, hashes de las fuentes, pertenencia al catálogo y totales.

Resultado de la verificación independiente: **OK**; 728/728 registros con trazabilidad completa y 728/728 hashes coincidentes con los PDF originales.

## 4. Nivel (a): existencia en el catálogo oficial

El archivo `clasificador.json` contiene 451 rutas jerárquicas únicas y representa subtítulo/ítem/asignación. Se reportan dos tasas: la **bruta**, sobre todas las líneas, y la **comparable**, que excluye los niveles 4/5 no representados por ese catálogo.

| Muestra | Líneas | En catálogo | Detalle 4/5 no representado | Fuera de catálogo, niveles 1–3 | Tasa bruta | Tasa comparable |
|---|---:|---:|---:|---:|---:|---:|
| Gastos 2023 | 269 | 158 | 95 | 16 | 58,7 % | 90,8 % |
| Ingresos 2023 | 98 | 55 | 26 | 17 | 56,1 % | 76,4 % |
| Gastos 2025 | 266 | 157 | 93 | 16 | 59,0 % | 90,8 % |
| Ingresos 2025 | 95 | 56 | 22 | 17 | 58,9 % | 76,7 % |
| **Total** | **728** | **426** | **236** | **66** | **58,5 %** | **86,6 %** |

Los 236 registros de niveles 4/5 no se interpretan automáticamente como códigos normativos inválidos: el catálogo entregado no contiene esos niveles. Las 66 ocurrencias restantes sí requieren cotejo de cobertura/versionado; corresponden a 33 códigos únicos, detallados en el registro de hallazgos.

## 5. Nivel (b): suma de cuentas hijas al padre

Cada control compara una métrica de un padre con la suma de sus hijas directas. La diferencia se define como `valor del padre − suma de hijas`.

| Muestra | Controles padre–métrica | Calzan | No calzan | Tasa de éxito |
|---|---:|---:|---:|---:|
| Gastos 2023 | 415 | 396 | 19 | 95,4 % |
| Ingresos 2023 | 155 | 155 | 0 | 100,0 % |
| Gastos 2025 | 415 | 388 | 27 | 93,5 % |
| Ingresos 2025 | 165 | 165 | 0 | 100,0 % |
| **Total** | **1150** | **1104** | **46** | **96,0 %** |

Hay 46 diferencias concentradas en 24 relaciones documento–padre, todas en gastos: 44 de magnitud 1 M$ y 2 de magnitud 2 M$; máximo absoluto 2 M$. Son compatibles con diferencias de redondeo de la fuente, pero su causa no se presume ni se corrige. El detalle completo está en `REGISTRO_HALLAZGOS_ETAPA1_v1.md` y en el CSV asociado.

## 6. Nivel (c): totales impresos contra lo parseado

Cada celda de la tabla representa `total impreso = suma de subtítulos parseados`. Los 20 controles calzan sin diferencia.

| Muestra | Inicial | Vigente | Ejecutado | Saldo | Quinta columna | Resultado |
|---|---:|---:|---:|---:|---:|---|
| Gastos 2023 | 37.938.207 | 51.614.659 | Devengado: 42.498.728 | 9.115.931 | Exigible: 928.023 | 5/5 |
| Ingresos 2023 | 37.938.207 | 51.614.659 | Percibidos: 50.436.486 | 1.178.173 | Por percibir: 3.045.889 | 5/5 |
| Gastos 2025 | 61.538.548 | 63.419.502 | Devengado: 52.575.249 | 10.844.253 | Exigible: 1.060.948 | 5/5 |
| Ingresos 2025 | 61.538.548 | 63.419.502 | Percibidos: 56.254.675 | 7.164.827 | Por percibir: 3.572.709 | 5/5 |
| **Total** | — | — | — | — | — | **20/20 (100,0 %)** |

## 7. Control aritmético complementario

Se comprobó además `saldo = vigente − ejecutado` para cada línea. No reemplaza ninguno de los tres niveles solicitados.

| Muestra | Líneas que calzan | Total de líneas | Tasa |
|---|---:|---:|---:|
| Gastos 2023 | 269 | 269 | 100,0 % |
| Ingresos 2023 | 98 | 98 | 100,0 % |
| Gastos 2025 | 264 | 266 | 99,2 % |
| Ingresos 2025 | 95 | 95 | 100,0 % |
| **Total** | **726** | **728** | **99,7 %** |

Las dos excepciones están en gastos 2025: `22.06` presenta saldo 784.425 frente a 784.424 calculado, y `22.06.004` presenta 73.303 frente a 73.302; ambas diferencias son +1 M$ y se conservaron como impresas.

## 8. Condiciones para una eventual escala

- Conservar el código literal del PDF y su nivel; no forzar correspondencias con el catálogo.
- Separar la validación de niveles 1–3 de la de subniveles no representados, y someter los 33 códigos únicos a cotejo normativo.
- Incorporar reglas específicas para Formulario 0101 y 0102; validar por separado cualquier variante mensual/trimestral y los ESP antes de extrapolar.
- Mantener como compuertas los tres controles y registrar las diferencias de fuente sin ajustar montos.
- Conservar archivo, página, línea y SHA-256 por registro, y verificar los hashes antes de procesar.

## 9. Evidencias y reproducción

- Parser: `scripts/factibilidad_bep_etapa1.py`.
- Verificador independiente: `scripts/verificar_factibilidad_bep_etapa1.py`.
- Datos parseados y controles: `trabajo/07_Información_Presupuestaria/factibilidad/`.
- Registro íntegro: `documentación/07_Información_Presupuestaria/REGISTRO_HALLAZGOS_ETAPA1_v1.csv` (350 ocurrencias).
- Detalle narrativo y tablas de fallidos: `documentación/07_Información_Presupuestaria/REGISTRO_HALLAZGOS_ETAPA1_v1.md`.

Comandos ejecutados desde la raíz del workspace:

```bash
python "scripts/factibilidad_bep_etapa1.py"
python "scripts/verificar_factibilidad_bep_etapa1.py"
```

**Parada obligatoria:** no se procesaron los 143 PDF, ni ESP, ni julio de 2025, ni la republicación v2; no se generaron datos canónicos ni series mensuales de Etapa 2.
