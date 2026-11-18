# PREVALIDACIÓN PREVIA A ESCALA — ETAPA 2

**Proyecto:** Portal de Transparencia Trazable — Municipalidad de Coronel  
**Fecha:** 14 de noviembre de 2026  
**Alcance:** dos archivos de la carpeta ESP y un BEP mensual de junio de 2024. No constituye procesamiento masivo.

## 1. Decisiones

- **ESP: no escalar sin nueva autorización expresa.** El contenido difiere sustantivamente de lo declarado: el título es “ESTADO PRESUPUESTARIO DE GASTOS”, presenta 11 columnas monetarias en CLP y utiliza códigos del clasificador presupuestario. No corresponde al Estado de Situación Financiera basado en el Plan de Cuentas Sector Municipal.
- **BEP junio de 2024: estructura estable, pero bajo umbral de jerarquía.** Mantiene Formulario 0102, cinco columnas en M$ y corte acumulado. Si el resultado se confirma durante la escala, el archivo quedará en cuarentena y no se incorporará al canónico ni a los deltas.
- El checkpoint BEP 2023 es independiente y continúa bajo la autorización otorgada.

## 2. Fuentes

| Muestra | Archivo | Corte de contenido | SHA-256 |
|---|---|---|---|
| ESP gastos 2023 | `esp dic municipalidad gastos.pdf` | 31/12/2023 | `4043c4a471ce07a3847780d9676092f845263286d8c7e22bbe9a573dfb23cc6c` |
| ESP gastos 2025 | `esp dic municipalidad gastos.pdf` | 31/12/2025 | `262d52dd2d66a33ac95ec85d5fc45724bce8fb5903914aebb27973145a5cf494` |
| BEP gastos junio 2024 | `bep jun municipalidad gastos.pdf` | 30/06/2024 | `6d26f697f1841f200a4758a39db335fd3bdb7c11fb2f79b9cd66812e59ff8e16` |

## 3. ESP: tres niveles de validación contra `plan_municipal.json`

El plan contiene 961 rutas jerárquicas únicas. Los totales impresos corresponden a la línea “ACREEDORES PRESUPUESTARIOS” de la primera página y se compararon contra la suma de subtítulos parseados para las 11 métricas.

| Muestra | Líneas | Catálogo plan municipal | Jerarquía | Totales | Aritmética de saldo |
|---|---:|---:|---:|---:|---:|
| ESP gastos 2023 | 833 | 0/833 — 0 % | 1.221/1.221 — 100 % | 11/11 — 100 % | 833/833 — 100 % |
| ESP gastos 2025 | 926 | 0/926 — 0 % | 1.243/1.243 — 100 % | 11/11 — 100 % | 926/926 — 100 % |
| **Total** | **1.759** | **0/1.759 — 0 %** | **2.464/2.464 — 100 %** | **22/22 — 100 %** | **1.759/1.759 — 100 %** |

Además, las cinco identidades aritméticas aplicables —vigente, exigible y tres saldos— calzan en 8.795/8.795 controles. Estos resultados confirman que el parseo interno es consistente, pero no resuelven la discrepancia de tipo documental y catálogo.

Las 11 columnas detectadas son: presupuesto inicial, modificación, vigente, vigente mes, obligación, devengado, pago, exigible, saldo por comprometer, saldo por devengar y saldo por pagar. No se seleccionó una columna `saldo` canónica ni se remapearon códigos.

## 4. BEP mensual junio de 2024

| Control | Resultado | Umbral | Evaluación |
|---|---:|---:|---|
| Totales impresos | 5/5 — 100 % | 100 % | Calza |
| Jerarquía | 383/410 — 93,4 % | ≥95 % | **Bajo umbral** |
| Aritmética | 261/262 — 99,6 % | ≥99 % | Calza |
| Catálogo, tasa bruta | 153/262 — 58,4 % | Informativo | 93 detalles no representados; 16 ausencias en niveles 1–3 |

Se detectaron 27 diferencias jerárquicas y una aritmética (`22.09.003`, +1 M$ en el saldo). No se corrigieron valores. El Formulario 0102 y el corte 30/06/2024 fueron identificados desde el contenido; no hay variante estructural respecto de los BEP de diciembre.

## 5. Evidencia y reproducción

- `scripts/prevalidar_entradas_etapa2.py`
- `scripts/prevalidar_esp_etapa2.py`
- `trabajo/07_Información_Presupuestaria/prevalidacion_etapa2/`

Los CSV de trabajo conservan archivo, ruta, página, línea y SHA-256. Los PDF originales permanecen intocados. La ausencia de julio de 2025 y la republicación v2 de enero de 2023 serán tratadas en sus respectivos lotes; no se interpolará ninguna ausencia.
