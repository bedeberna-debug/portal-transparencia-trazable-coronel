# COBERTURA, CUARENTENAS Y AUSENCIAS — ETAPA 2

**Inventario físico:** 141 PDF (71 BEP y 70 ESP). **BEP:** 66 aceptados y 5 en cuarentena. **ESP:** 70 aceptados y 0 en cuarentena.

## 1. Cobertura BEP

| Año | Tipo | Aceptados | Cuarentena | Ausencias | Deltas computables |
|---|---|---|---|---|---|
| 2023 | gastos | 01, 02, 03, 04, 05, 06, 07, 10, 12 | 08, 09, 11 | — | 01, 02, 03, 04, 05, 06, 07 |
| 2023 | ingresos | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12 | — | — | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12 |
| 2024 | gastos | 01, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12 | 02 | — | 01, 04, 05, 06, 07, 08, 09, 10, 11, 12 |
| 2024 | ingresos | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12 | — | — | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12 |
| 2025 | gastos | 01, 02, 03, 04, 05, 06, 08, 09, 10, 11, 12 | — | 07 | 01, 02, 03, 04, 05, 06, 09, 10, 11, 12 |
| 2025 | ingresos | 01, 02, 03, 04, 05, 06, 08, 09, 10, 11, 12 | — | 07 | 01, 02, 03, 04, 05, 06, 09, 10, 11, 12 |

## 2. Cobertura ESP

| Año | Gastos aceptados | Ingresos aceptados | Ingresos en cuarentena | Ausencias por tipo |
|---|---|---|---|---|
| 2023 | 12 | 12 | 0 | — |
| 2024 | 12 | 12 | 0 | — |
| 2025 | 11 | 11 | 0 | julio |

Los 35 ESP de gastos cumplen los umbrales estrictos. Los 35 ESP de ingresos cumplen individualmente D-13 y quedan aceptados; 0 permanecen en cuarentena. La diferencia del saldo por percibir no se corrige: se conserva en los dos campos documentales y en `ESP_2023-2025_totales_ingresos_v1.csv`.

La serie ESP de ingresos tiene 57636 deltas de cuentas y 340 de totales en 34 cortes computables. Hay 53 cuentas sin delta por ausencia en el corte previo o actual. Julio de 2025 es ausencia declarada; agosto de 2025 no es computable.

## 3. Cuarentenas BEP permanentes

| Documento | Motivo |
|---|---|
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | republicacion_contenido_difiere_del_original |
| BEP_2023-08_GASTOS_ORIGINAL | jerarquia |
| BEP_2023-09_GASTOS_ORIGINAL | jerarquia |
| BEP_2023-11_GASTOS_ORIGINAL | jerarquia|aritmetica |
| BEP_2024-02_GASTOS_ORIGINAL | jerarquia|aritmetica |

## 4. Ausencias, versión republicada e inventario

- Julio de 2025: ausencia declarada en BEP y ESP, gastos e ingresos; sin interpolación.
- Enero de 2023 ingresos BEP: original aceptado y v2 parseada/cuarentenada; ambas versiones se conservan con SHA-256.
- La referencia inicial mencionó 143 PDF; se observaron 141. La malla teórica de 144 combinaciones menos cuatro ausencias de julio de 2025, más una republicación, explica 141 archivos físicos.
