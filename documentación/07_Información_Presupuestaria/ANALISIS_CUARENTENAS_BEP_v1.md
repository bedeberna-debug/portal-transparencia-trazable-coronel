# ANÁLISIS DE CUARENTENAS BEP Y POLÍTICA DE TOLERANCIA

**Universo:** 33 documentos inicialmente en cuarentena: 32 de gastos y la republicación v2 de ingresos. **Diferencias jerárquicas no calzantes:** 975. La tabla permanente `ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv` contiene cada diferencia con magnitud, cuenta, página, línea y SHA-256.

## 1. Distribución completa por magnitud

| Magnitud absoluta | Ocurrencias |
|---:|---:|
| 1 M$ | 921 |
| 2 M$ | 45 |
| 3 M$ | 4 |
| 25308 M$ | 1 |
| 881613 M$ | 1 |
| 906921 M$ | 2 |
| 2271862 M$ | 1 |

## 2. Política autorizada y resultado por documento

Criterio refinado para gastos: totales impresos 100 %, aritmética ≥99 % y todas las diferencias jerárquicas con magnitud ≤2 M$. No se corrigen valores ni se elimina el anexo. Un documento con cualquier diferencia >2 M$ permanece en cuarentena.

- Elegibles para incorporación: **28** documentos de gastos.
- Permanecen en cuarentena: **5** documentos: cuatro gastos y la v2 de ingresos.
- La v2 no es elegible por tipo y por diferencia de contenido respecto del original, independientemente de sus diferencias jerárquicas.

## 3. Diferencias superiores a 2 M$

| Documento | Cuenta | Métrica | Padre | Suma hijas | Diferencia | Página/línea |
|---|---|---|---:|---:|---:|---|
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | `12` | ingresos_percibidos_miles_clp | 25308 | 0 | 25308 | 4/5 |
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | `12` | ingresos_por_percibir_miles_clp | 2271862 | 0 | 2271862 | 4/5 |
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | `12` | presupuesto_inicial_miles_clp | 906922 | 1 | 906921 | 4/5 |
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | `12` | presupuesto_vigente_miles_clp | 906922 | 1 | 906921 | 4/5 |
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | `12` | saldo_presupuestario_miles_clp | 881614 | 1 | 881613 | 4/5 |
| BEP_2023-08_GASTOS_ORIGINAL | `21.01.001` | obligacion_devengada_miles_clp | 1918508 | 1918505 | 3 | 1/17 |
| BEP_2023-08_GASTOS_ORIGINAL | `21.01.001` | saldo_presupuestario_miles_clp | 926834 | 926837 | -3 | 1/17 |
| BEP_2023-09_GASTOS_ORIGINAL | `22` | obligacion_devengada_miles_clp | 10980668 | 10980671 | -3 | 4/13 |
| BEP_2023-09_GASTOS_ORIGINAL | `22` | saldo_presupuestario_miles_clp | 3400403 | 3400400 | 3 | 4/13 |

## 4. Documentos que permanecen en cuarentena

| Documento | Diferencias | Máximo absoluto | Otros motivos |
|---|---:|---:|---|
| BEP_2023-01_INGRESOS_REPUBLICACION_V2 | 5 | 2271862 M$ | republicacion_contenido_difiere_del_original |
| BEP_2023-08_GASTOS_ORIGINAL | 29 | 3 M$ | diferencia_jerarquica_mayor_2 |
| BEP_2023-09_GASTOS_ORIGINAL | 35 | 3 M$ | diferencia_jerarquica_mayor_2 |
| BEP_2023-11_GASTOS_ORIGINAL | 36 | 2 M$ | aritmetica |
| BEP_2024-02_GASTOS_ORIGINAL | 29 | 2 M$ | aritmetica |

## 5. Verificación visual

La muestra de 10 líneas confirmó 10/10 valores padre contra la imagen. El detalle y las coordenadas están en `VERIFICACION_VISUAL_CUARENTENAS_v1.md` y su CSV.
