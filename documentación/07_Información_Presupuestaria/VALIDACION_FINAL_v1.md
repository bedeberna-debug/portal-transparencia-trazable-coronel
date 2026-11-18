# VALIDACIÓN FINAL — INFORMACIÓN PRESUPUESTARIA

**Alcance:** canónico BEP 2023–2025, series mensuales BEP y ESP de ingresos, y ESP como Estado Presupuestario separado. La validación recalcula controles desde los canónicos y contrasta totales impresos, fuentes y hashes.

**Resultado general:** APROBADO; LA COBERTURA BEP PERMANECE LIMITADA POR CINCO CUARENTENAS. ESP queda aceptado en 70/70 documentos, sujeto a la regla documental D-13 para ingresos y a la ausencia declarada de julio de 2025.

## 1. BEP: tres niveles y política refinada

| Año | Documentos | Líneas | Catálogo, tasa bruta | Jerarquía informativa | Totales impresos | Aritmética |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 21 | 3595 | 2080/3595 — 57,86 % | 5352/5595 — 95,66 % | 105/105 — 100,00 % | 3586/3595 — 99,75 % |
| 2024 | 23 | 4077 | 2340/4077 — 57,40 % | 6115/6415 — 95,32 % | 115/115 — 100,00 % | 4068/4077 — 99,78 % |
| 2025 | 22 | 3944 | 2333/3944 — 59,15 % | 5979/6330 — 94,45 % | 110/110 — 100,00 % | 3933/3944 — 99,72 % |
| total | 66 | 11616 | 6753/11616 — 58,14 % | 17446/18340 — 95,13 % | 330/330 — 100,00 % | 11587/11616 — 99,75 % |

Los documentos con política inicial cumplen totales 100 %, jerarquía ≥95 % y aritmética ≥99 %. Los 28 con política refinada cumplen totales 100 %, aritmética ≥99 % y cada diferencia jerárquica ≤2 M$. La jerarquía agregada se informa sin ocultar las diferencias. El anexo permanente contiene 975 diferencias; la verificación visual confirmó 10/10 líneas.

Permanecen fuera del canónico: BEP_2023-08_GASTOS_ORIGINAL, BEP_2023-09_GASTOS_ORIGINAL, BEP_2023-11_GASTOS_ORIGINAL, BEP_2024-02_GASTOS_ORIGINAL y BEP_2023-01_INGRESOS_REPUBLICACION_V2.

## 2. ESP: gastos estrictos e ingresos D-13

### Controles clásicos informativos sobre todos los aceptados

Estas tasas describen los documentos, pero no son el criterio de aceptación de ingresos D-13. En particular, el total clásico de saldo por percibir no se fuerza a calzar.

| Año | Documentos | Líneas | Catálogo, tasa bruta | Jerarquía | Totales impresos | Aritmética principal | Identidades adicionales |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 24 | 11297 | 2554/11297 — 22,61 % | 20843/20988 — 99,31 % | 228/240 — 95,00 % | 11261/11297 — 99,68 % | 54137/54209 — 99,87 % |
| 2024 | 24 | 11946 | 2493/11946 — 20,87 % | 21657/21665 — 99,96 % | 228/240 — 95,00 % | 11910/11946 — 99,70 % | 57319/57391 — 99,87 % |
| 2025 | 22 | 8869 | 2333/8869 — 26,31 % | 19756/19756 — 100,00 % | 209/220 — 95,00 % | 8836/8869 — 99,63 % | 42253/42319 — 99,84 % |
| total | 70 | 32112 | 7380/32112 — 22,98 % | 62256/62409 — 99,75 % | 665/700 — 95,00 % | 32007/32112 — 99,67 % | 153709/153919 — 99,86 % |

### Criterio de aceptación

- Los 35 ESP de gastos cumplen individualmente totales 100 %, jerarquía ≥95 % y aritmética ≥99 %.
- Los 35 ESP de ingresos reprodujeron individualmente las tres condiciones D-13: 35/35 rehabilitados y 0 en cuarentena. Las ocho métricas distintas de saldo por percibir calzan 280/280; el total oficial y la reconciliación con la cuenta 15 tienen residual cero en todos los documentos.
- `ESP_2023-2025_totales_ingresos_v1.csv` conserva `total_saldo_por_percibir_oficial_clp` y `saldo_por_percibir_suma_detalle_clp` con nombres y series separados. La diferencia se explica por la cuenta 15 y no se oculta.
- Las 35 líneas de la cuenta 15 conservan saldo por percibir impreso en cero; la exportación canónica coincide con el parseo y ningún PDF fue modificado. Los 70 títulos confirman “Estado Presupuestario”, con evidencia literal y trazabilidad.

## 3. Controles independientes

| Control | Resultado | Observado | Esperado |
|---|---|---|---|
| inventario_cantidad_fisica | calza | inventario=141; fisico=141 | 141 |
| inventario_familias | calza | BEP=71; ESP=70 | BEP=71; ESP=70 |
| hashes_inventario_completo | calza | 141/141 | 141/141 |
| tablas_documentales_completas | calza | BEP=71; ESP=70 | BEP=71; ESP=70 |
| bep_canonico_solo_aceptados | calza | 66 | 66 |
| bep_unicidad_registro_id | calza | 11616 | 11616 |
| bep_unicidad_documento_cuenta | calza | 11616 | 11616 |
| bep_trazabilidad_y_hash_por_registro | calza | 11616/11616 | 11616/11616 |
| bep_valores_raw_coinciden_numericos | calza | 0 | 0 |
| bep_exportacion_coincide_parseo | calza | 0 | 0 |
| bep_metricas_no_aplicables_nulas | calza | 0 | 0 |
| esp_canonico_solo_aceptados | calza | 70 | 70 |
| esp_unicidad_registro_id | calza | 32112 | 32112 |
| esp_unicidad_documento_cuenta | calza | 32112 | 32112 |
| esp_trazabilidad_y_hash_por_registro | calza | 32112/32112 | 32112/32112 |
| esp_valores_raw_coinciden_numericos | calza | 0 | 0 |
| esp_exportacion_coincide_parseo | calza | 0 | 0 |
| esp_metricas_no_aplicables_nulas | calza | 0 | 0 |
| bep_cotejo_clasificador_presupuestario | calza | 0 | 0 |
| esp_cotejo_clasificador_presupuestario | calza | 0 | 0 |
| bep_politica_en_cada_documento | calza | 66 | 66 |
| bep_28_documentos_refinados | calza | 28 | 28 |
| bep_cinco_cuarentenas_exactas_y_excluidas | calza | BEP_2023-01_INGRESOS_REPUBLICACION_V2|BEP_2023-08_GASTOS_ORIGINAL|BEP_2023-09_GASTOS_ORIGINAL|BEP_2023-11_GASTOS_ORIGINAL|BEP_2024-02_GASTOS_ORIGINAL | 5 documentos esperados; 0 en canónico |
| bep_anexo_975_diferencias | calza | 975 | 975 |
| bep_anexo_distribucion_magnitudes | calza | {1: 921, 2: 45, 25308: 1, 2271862: 1, 906921: 2, 881613: 1, 3: 4} | 921x1;45x2;4x3;5 grandes v2 |
| bep_refinados_todas_diferencias_anexo_hasta_2 | calza | 2 | <=2 M$ |
| bep_verificacion_visual_10_sobre_10 | calza | 10/10 | 10/10 |
| bep_verificacion_visual_trazada | calza | 0 | 0 |
| bep_totales_y_aritmetica_agregados_2023 | calza | totales=100,00 %; aritmetica=99,75 %; jerarquia_informativa=95,66 % | totales=100 %; aritmetica>=99 % |
| bep_totales_y_aritmetica_agregados_2024 | calza | totales=100,00 %; aritmetica=99,78 %; jerarquia_informativa=95,32 % | totales=100 %; aritmetica>=99 % |
| bep_totales_y_aritmetica_agregados_2025 | calza | totales=100,00 %; aritmetica=99,72 %; jerarquia_informativa=94,45 % | totales=100 %; aritmetica>=99 % |
| bep_totales_y_aritmetica_agregados_total | calza | totales=100,00 %; aritmetica=99,75 %; jerarquia_informativa=95,13 % | totales=100 %; aritmetica>=99 % |
| esp_criterio_aceptacion_en_cada_documento | calza | 70 | 70 |
| esp_35_ingresos_rehabilitados_d13 | calza | 35/35 | 35/35 aceptados por D-13 |
| esp_controles_d13_coinciden_recalculo | calza | 0 | 0 |
| esp_ingresos_diferencia_clasica_exclusiva_saldo_por_percibir | calza | 35; metricas=['saldo_por_percibir_clp'] | 35 saldo_por_percibir_clp; control informativo |
| esp_ingresos_otras_ocho_metricas_calzan | calza | 35 documentos con 8/9 | 35 documentos con 8/9 |
| esp_doble_total_35_documentos | calza | filas=35; errores=0 | 35; ambos totales y diferencia exactos |
| esp_doble_total_trazado | calza | 0 | 0 |
| esp_cuenta_15_ceros_impresos_intactos | calza | 35 líneas; ceros=35 | 35 líneas; 35 ceros |
| esp_politica_y_nota_en_canonico | calza | 32112 | 32112 |
| esp_gastos_tres_niveles_agregados_2023 | calza | totales=100,00 %; jerarquia=100,00 %; aritmetica=100,00 % | 100 %; >=95 %; >=99 % |
| esp_gastos_tres_niveles_agregados_2024 | calza | totales=100,00 %; jerarquia=100,00 %; aritmetica=100,00 % | 100 %; >=95 %; >=99 % |
| esp_gastos_tres_niveles_agregados_2025 | calza | totales=100,00 %; jerarquia=100,00 %; aritmetica=100,00 % | 100 %; >=95 %; >=99 % |
| esp_gastos_tres_niveles_agregados_total | calza | totales=100,00 %; jerarquia=100,00 %; aritmetica=100,00 % | 100 %; >=95 %; >=99 % |
| esp_titulo_y_evidencia_70_documentos | calza | 70/70 | 70/70 |
| esp_hallazgo_tipo_documental_70 | calza | 70 | 70 |
| esp_11_columnas_gastos_9_ingresos | calza | gastos=11; ingresos=9; CLP | gastos=11; ingresos=9; CLP |
| cobertura_72_periodos_tipo_por_familia | calza | BEP=72; ESP=72 | 72+72 |
| bep_julio_2025_ausencia_declarada | calza | 2 | 2 |
| bep_julio_2025_sin_datos | calza | 0 | 0 |
| esp_julio_2025_ausencia_declarada | calza | 2 | 2 |
| esp_julio_2025_sin_datos | calza | 0 | 0 |
| agosto_2025_sin_delta_saltando_julio | calza | 0 | 0 |
| republicacion_ambas_versiones_inventariadas | calza | original+v2 | original+v2 |
| republicacion_v2_parseada_y_cuarentenada | calza | cuarentena | cuarentena; 95 líneas |
| enero_2023_usa_original | calza | BEP_2023-01_INGRESOS_ORIGINAL | BEP_2023-01_INGRESOS_ORIGINAL |
| unicidad_delta | calza | 52200 | 52200 |
| recalculo_delta_y_trazabilidad | calza | 52200/52200 | 52200/52200 |
| cobertura_exacta_deltas | calza | actual=52200; faltantes=0; inesperados=0 | esperado=52200 |
| cobertura_cortes_delta | calza | computables=61; no_computables=11 | 61;11 |
| esp_delta_cuentas_unicidad_y_cantidad | calza | 57636 | 57636 |
| esp_delta_cuentas_recalculo_y_trazabilidad | calza | 57636/57636 | 57636/57636 |
| esp_delta_cuentas_cobertura_exacta | calza | actual=57636; faltantes=0; inesperados=0 | esperado=57636 |
| esp_delta_hallazgos_ausencias_exactos | calza | actual=53; esperados=53 | 53; sin imputación |
| esp_delta_totales_unicidad_y_cantidad | calza | 340 | 340 |
| esp_delta_totales_recalculo_y_trazabilidad | calza | 340/340 | 340/340 |
| esp_delta_totales_cobertura_y_separacion | calza | actual=340; esperado=340 | 340; 9 oficiales + 1 suma detalle por corte |
| esp_cobertura_cortes_delta_ingresos | calza | computables=34; no_computables=2 | 34;2 |
| esp_julio_y_agosto_2025_sin_deltas | calza | 0 | 0 |
| cotejo_conserva_33_codigos_etapa1 | calza | etapa1=33; cotejo=35; faltantes=0 | 33 incluidos |
| cotejo_bep_sin_remapeo | calza | 35 | 35 |
| cotejo_esp_sin_remapeo | calza | 51 | 51 |
| registro_hallazgos_ids_unicos | calza | 31732 | 31732 |
| gobernanza_d13_registrada | calza | D-13 y resultado 35/35 | D-13 vigente |
| gobernanza_tp18_descartada | calza | TP-18 cerrada sin solicitar | descartada con causa documentada |

## 4. Cobertura, series y versionado

- Inventario: 141 PDF con SHA-256 verificado; 71 BEP y 70 ESP.
- BEP: 66 aceptados, 5 en cuarentena y 11616 registros canónicos.
- ESP: 70 aceptados, 0 en cuarentena y 32112 registros canónicos; 35 ingresos rehabilitados por D-13.
- Serie BEP: 52200 deltas recalculados; 61 cortes computables y 11 no computables.
- Serie ESP de ingresos: 57636 deltas de cuentas y 340 de totales recalculados en 34 cortes. Los 53 casos de cuentas ausentes en un corte quedan sin delta y sin imputación.
- Julio de 2025: ausencia declarada en ambas familias y tipos; sin filas ni interpolación. Agosto de 2025 no tiene delta que salte julio.
- Enero de 2023: original y v2 conservados; v2 en cuarentena y original usado para la serie BEP.
- Versionado: 35 códigos BEP y 51 ESP, sin remapeo; los 33 de Etapa 1 están incluidos.
- Gobernanza: D-13 vigente y TP-18 descartada con causa documentada.
