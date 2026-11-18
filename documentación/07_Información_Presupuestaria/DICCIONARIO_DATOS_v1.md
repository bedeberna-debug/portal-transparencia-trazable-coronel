# DICCIONARIO DE DATOS — INFORMACIÓN PRESUPUESTARIA

**Esquema:** canonico_v1.0.0  
**Alcance:** BEP aceptados, serie mensual BEP y ESP aceptados como Estado Presupuestario separado. Las cuarentenas no integran los canónicos.

## 1. Tabla BEP canónica y serie mensual

- `BEP_2023-2025_canonico_v1.csv`: una fila por documento–cuenta; siete métricas en M$, cada una con `_raw`.
- `BEP_2023-2025_serie_mensual_v1.csv`: formato largo período–tipo–cuenta–métrica. Solo cortes consecutivos aceptados; enero usa base cero como convención explícita. No se imputan cuentas ausentes ni se saltan ausencias o cuarentenas.
- `BEP_2023-2025_documentos_v1.csv`: disposición, política de aceptación, totales impresos y sumas por PDF.
- `BEP_2023-2025_cobertura_v1.csv`: 72 combinaciones período–tipo y computabilidad del delta.

## 2. Tabla ESP canónica

Archivo: `ESP_2023-2025_canonico_v1.csv`. Una fila por documento–cuenta, en CLP. Incluye la unión de 15 métricas: 11 de gastos y 9 de ingresos, con cinco comunes. Una métrica no aplicable queda vacía, tanto en valor como en `_raw`; nunca se rellena con cero.

| Campo | Definición |
|---|---|
| `esquema_version` | Versión canonico_v1.0.0. |
| `categoria` | Categoría informacion_presupuestaria. |
| `subcategoria` | estado_presupuestario; separado del BEP. |
| `registro_id` | ID único con SHA-256, página, línea y código. |
| `documento_id` | ID ESP por período y tipo. |
| `tipo_documental` | Título normalizado del contenido: Estado Presupuestario de Gastos o Ingresos. |
| `tipo` | gastos o ingresos. |
| `version_fuente` | original. |
| `anio` | Año del corte de contenido. |
| `mes_numero` | Mes numérico del corte. |
| `mes_nombre` | Mes en español. |
| `periodo` | Período AAAA-MM. |
| `fecha_corte` | Fecha ISO impresa en el título. |
| `periodo_fuente` | contenido. |
| `formulario_cgr` | Vacío: número de formulario no identificado en el contenido ESP. |
| `formulario_fuente` | Declaración de no identificación; no se infiere el número. |
| `codigo_cuenta_pdf` | Código impreso, sin remapeo. |
| `nivel_jerarquico` | Nivel derivado de los componentes del código. |
| `denominacion_pdf` | Denominación impresa con continuaciones. |
| `catalogo_estado` | Cotejo con clasificador.json, nunca con plan_municipal.json. |
| `catalogo_denominacion` | Denominación oficial si la ruta existe. |
| `unidad_monetaria` | CLP; no convertir a M$. |
| `naturaleza_valor` | acumulado_al_corte. |
| `presupuesto_inicial_clp` | Presupuesto inicial impreso, en CLP. |
| `presupuesto_inicial_clp_raw` | Token monetario original de `presupuesto_inicial_clp`. |
| `modificacion_presupuestaria_clp` | Modificaciones presupuestarias impresas, en CLP. |
| `modificacion_presupuestaria_clp_raw` | Token monetario original de `modificacion_presupuestaria_clp`. |
| `presupuesto_vigente_clp` | Presupuesto vigente impreso, en CLP. |
| `presupuesto_vigente_clp_raw` | Token monetario original de `presupuesto_vigente_clp`. |
| `presupuesto_vigente_mes_clp` | Presupuesto vigente al mes de corte, en CLP. |
| `presupuesto_vigente_mes_clp_raw` | Token monetario original de `presupuesto_vigente_mes_clp`. |
| `obligacion_clp` | Obligaciones de gastos, en CLP; no aplicable a ingresos. |
| `obligacion_clp_raw` | Token monetario original de `obligacion_clp`. |
| `obligacion_devengada_clp` | Obligaciones devengadas de gastos, en CLP; no aplicable a ingresos. |
| `obligacion_devengada_clp_raw` | Token monetario original de `obligacion_devengada_clp`. |
| `pago_clp` | Pagos de gastos, en CLP; no aplicable a ingresos. |
| `pago_clp_raw` | Token monetario original de `pago_clp`. |
| `deuda_exigible_clp` | Deuda exigible de gastos, en CLP; no aplicable a ingresos. |
| `deuda_exigible_clp_raw` | Token monetario original de `deuda_exigible_clp`. |
| `saldo_por_comprometer_clp` | Saldo por comprometer de gastos, en CLP; no aplicable a ingresos. |
| `saldo_por_comprometer_clp_raw` | Token monetario original de `saldo_por_comprometer_clp`. |
| `saldo_por_devengar_clp` | Saldo por devengar, en CLP; presente en gastos e ingresos. |
| `saldo_por_devengar_clp_raw` | Token monetario original de `saldo_por_devengar_clp`. |
| `saldo_por_pagar_clp` | Saldo por pagar de gastos, en CLP; no aplicable a ingresos. |
| `saldo_por_pagar_clp_raw` | Token monetario original de `saldo_por_pagar_clp`. |
| `ingreso_devengado_clp` | Ingreso devengado, en CLP; no aplicable a gastos. |
| `ingreso_devengado_clp_raw` | Token monetario original de `ingreso_devengado_clp`. |
| `ingreso_percibido_clp` | Ingreso percibido, en CLP; no aplicable a gastos. |
| `ingreso_percibido_clp_raw` | Token monetario original de `ingreso_percibido_clp`. |
| `ingreso_por_percibir_clp` | Ingreso por percibir, en CLP; no aplicable a gastos. |
| `ingreso_por_percibir_clp_raw` | Token monetario original de `ingreso_por_percibir_clp`. |
| `saldo_por_percibir_clp` | Saldo por percibir de ingresos, en CLP; no aplicable a gastos. |
| `saldo_por_percibir_clp_raw` | Token monetario original de `saldo_por_percibir_clp`. |
| `identidad_aritmetica_principal` | saldo_comprometer en gastos; saldo_por_percibir en ingresos. |
| `control_aritmetico_principal` | calza/no_calza de la identidad principal. |
| `control_aritmetico_diferencia_clp` | Diferencia de la identidad principal, en CLP, sin corrección. |
| `estado_documento` | Estado vigente del documento; solo aceptado en el canónico. |
| `politica_aceptacion` | Umbral estricto en gastos o `D-13_rehabilitacion_condicionada_cuenta_15` en ingresos. |
| `nota_metodologica` | Regla de agregación y preservación de cifras para documentos rehabilitados por D-13. |
| `politica_aceptacion` | politica_aceptacion |
| `nota_metodologica` | nota_metodologica |
| `fuente_archivo` | Nombre físico original. |
| `fuente_ruta_relativa` | Ruta relativa al workspace. |
| `fuente_pagina` | Página PDF desde 1. |
| `fuente_linea` | Línea de extracción por coordenadas. |
| `fuente_sha256` | SHA-256 del PDF original. |
| `texto_linea_raw` | Token monetario original de `texto_linea`. |

### Identidades aritméticas

- Gastos, control principal: saldo por comprometer = presupuesto vigente al mes − obligación. Controles adicionales: vigente = inicial + modificación; exigible = devengado − pago; saldo por devengar = obligación − devengado; saldo por pagar = obligación − pago.
- Ingresos, control principal: saldo por percibir = presupuesto vigente al mes − percibido. Controles adicionales: vigente = inicial + modificación; por percibir = devengado − percibido; saldo por devengar = vigente al mes − devengado. Estos controles se conservan en el parseo de trabajo, incluso para documentos en cuarentena.

## 3. Cobertura, evidencias y versionado

- `ESP_2023-2025_documentos_v1.csv`: 70 PDF, métricas, título literal con página/línea/SHA-256, totales y cuarentenas.
- `ESP_2023-2025_cobertura_v1.csv`: 72 combinaciones período–tipo; julio de 2025 declarado sin datos.
- `INVENTARIO_FUENTES_v1.csv`: 141 PDF físicos con ruta, bytes y SHA-256.
- `COTEJO_VERSIONADO_CODIGOS_v1.csv` y `COTEJO_VERSIONADO_CODIGOS_ESP_v1.csv`: códigos históricos ausentes del clasificador vigente, sin remapeo.
- `ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv`: anexo permanente de diferencias jerárquicas BEP.

## 4. D-13: totales y series mensuales ESP de ingresos

- `ESP_2023-2025_controles_D13_v1.csv`: una fila por cada uno de los 35 ESP de ingresos, con las tres condiciones aritméticas, residuos, estatus y trazabilidad del total y de la cuenta 15.
- `ESP_2023-2025_totales_ingresos_v1.csv`: una fila por documento aceptado. `total_saldo_por_percibir_oficial_clp` es el total impreso DEUDORES PRESUPUESTARIOS; `saldo_por_percibir_suma_detalle_clp` es la suma de subtítulos de nivel 1. La diferencia se conserva junto al vigente/percibido de la cuenta 15 y sus ubicaciones.
- `ESP_2023-2025_serie_mensual_ingresos_v1.csv`: deltas período–cuenta–métrica para las nueve métricas CLP. Enero usa base cero explícita; los demás meses exigen corte mensual inmediatamente anterior aceptado y presencia de la cuenta en ambos. Las cuentas ausentes no se imputan como cero.
- `ESP_2023-2025_serie_totales_ingresos_v1.csv`: deltas documentales en formato largo. Mantiene series separadas para los nueve totales oficiales y la suma del detalle de saldo por percibir; nunca mezcla ambos conceptos.
- `ESP_2023-2025_hallazgos_delta_ingresos_v1.csv`: cuentas sin delta por ausencia en uno de los dos cortes, sin imputación.

**Nota metodológica D-13:** El total oficial de saldo por percibir incorpora la cuenta 15 por vigente al mes menos percibido; la suma del detalle conserva los saldos impresos, incluidos sus ceros. Ambos totales son legítimos, tienen nombres distintos y deben mostrarse con su diferencia explicada, nunca oculta ni sustituida. Los deltas son diferencias aritméticas entre acumulados y no necesariamente flujos mensuales, especialmente en métricas de saldo.

Resultado: 35 rehabilitados, 0 en cuarentena; 57636 deltas de cuentas y 340 de totales. Julio de 2025 es ausencia declarada y agosto no salta ese corte.
