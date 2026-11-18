# REGISTRO DE HALLAZGOS — ETAPA 2

**Tratamiento general:** preservación literal, sin remapeo, imputación ni interpolación. El CSV homónimo contiene cada ocurrencia y su trazabilidad.

## 1. Resumen

- BEP: 66 aceptados; 5 en cuarentena.
- ESP: 70 aceptados; 0 en cuarentena.
- Cotejo de versionado: 35 códigos BEP y 51 códigos ESP, sin remapeo.
- Serie BEP: 52200 deltas; ausencias y cuarentenas interrumpen el cálculo.

| Familia / tipo / subtipo | Ocurrencias |
|---|---:|
| BEP / aritmetica / saldo_no_igual_vigente_menos_ejecutado | 37 |
| BEP / ausencia / julio_2025_no_publicado | 2 |
| BEP / catalogo / fuera_catalogo_mismo_nivel | 1172 |
| BEP / catalogo / fuera_catalogo_nivel_detalle_no_representado | 4176 |
| BEP / cuarentena / documento_bajo_umbral_o_variante | 5 |
| BEP / delta / cuenta_ausente_en_corte_actual | 5 |
| BEP / delta / cuenta_ausente_en_corte_previo | 15 |
| BEP / jerarquia / padre_distinto_suma_hijas_directas | 1028 |
| BEP / versionado / metadatos_ausentes_periodo_asignado_desde_original | 1 |
| ESP / aritmetica / saldo_por_percibir_no_calza | 105 |
| ESP / aritmetica_adicional / saldo_devengar_no_calza | 105 |
| ESP / ausencia / julio_2025_no_publicado | 2 |
| ESP / catalogo / fuera_catalogo_mismo_nivel | 1571 |
| ESP / catalogo / fuera_catalogo_nivel_detalle_no_representado | 23161 |
| ESP / delta_no_computable_cuenta / cuenta_ausente_en_corte_actual | 6 |
| ESP / delta_no_computable_cuenta / cuenta_sin_corte_previo | 47 |
| ESP / jerarquia / padre_distinto_suma_hijas_directas | 153 |
| ESP / regla_agregacion / saldo_por_percibir_incluye_cuenta_15 | 35 |
| ESP / total_general / total_impreso_distinto_suma_subtitulos | 35 |
| ESP / variante_documental / esp_es_estado_presupuestario_no_financiero | 70 |
| todas / inventario / cantidad_observada_difiere_de_estimacion_inicial | 1 |

## 2. Hallazgo de tipo documental ESP

Los 70 archivos de la carpeta denominada “Estado de Situación Financiera” contienen el título “ESTADO PRESUPUESTARIO DE GASTOS” o “ESTADO PRESUPUESTARIO DE INGRESOS”, no “Estado de Situación Financiera”. Se procesan como tipo documental separado `estado_presupuestario`, contra el clasificador presupuestario y en CLP. Cada documento conserva el título literal, página, línea y SHA-256 en `ESP_2023-2025_documentos_v1.csv` y en el CSV de hallazgos.

## 3. Regla de agregación ESP de ingresos y D-13

Los 35 documentos fueron evaluados individualmente. 35 reprodujeron las tres condiciones y fueron rehabilitados; 0 permanecen en cuarentena. El total oficial de saldo por percibir incluye el saldo inicial de caja por vigente al mes menos percibido, mientras el detalle conserva los saldos impresos. No se modificaron ceros ni otras cifras. El control `ESP_2023-2025_controles_D13_v1.csv` conserva residuos, estatus y trazabilidad por documento. Los 53 casos de cuentas sin delta mensual se registran sin imputación. TP-18 queda descartada con causa documentada.

## 4. Política jerárquica BEP y verificación visual

La política refinada incorporó 28 documentos de gastos con diferencias exclusivamente ≤2 M$, totales 100 % y aritmética ≥99 %. El anexo permanente registra 975 diferencias de las 33 cuarentenas iniciales. La muestra visual confirmó 10/10 líneas y sus cinco cifras; no se modificó ningún valor. Permanen en cuarentena BEP_2023-08_GASTOS_ORIGINAL, BEP_2023-09_GASTOS_ORIGINAL, BEP_2023-11_GASTOS_ORIGINAL, BEP_2024-02_GASTOS_ORIGINAL y BEP_2023-01_INGRESOS_REPUBLICACION_V2.

## 5. Cotejo de versionado normativo

Los códigos históricos ausentes del clasificador vigente se conservan sin equivalencias forzadas. La presencia histórica no prueba por sí sola vigencia o invalidez normativa. Los 33 códigos de Etapa 1 siguen incluidos en el cotejo BEP; se añadieron `05.03.009` y `05.03.099`. Los detalles están en los dos CSV de cotejo.

## 6. Disposición

Las cuarentenas no entran a los canónicos. Las diferencias conservan los valores impresos. Julio de 2025 es ausencia declarada. La discrepancia de 141 PDF observados frente a 143 informados inicialmente queda documentada.
