# MEMO — DESCUADRE DE ESP DE INGRESOS

**Fecha:** 14 de noviembre de 2026  
**Muestra:** diciembre de 2023, 2024 y 2025; tres documentos, mismo mes calendario.  
**Unidad:** CLP, valores enteros impresos.  
**Compuerta aplicada:** el mecanismo quedó resuelto con tres documentos; no se procesó un cuarto ni un quinto.

## 1. Veredicto y recomendación

**Veredicto: (a). Se recomienda rehabilitar los 35 ESP de ingresos con nota metodológica, sujeto a que cada documento reproduzca el control específico descrito abajo. No se fundamenta TP-18 con esta evidencia.**

El descuadre es una regla de agregación del formulario, no un error de extracción. En los tres documentos:

- La cuenta `15 — SALDO INICIAL DE CAJA` está presente en el detalle, con saldo por devengar y saldo por percibir impresos en **0**.
- El total `DEUDORES PRESUPUESTARIOS` de saldo por percibir sí incorpora el vigente al mes menos percibido de esa cuenta.
- La diferencia entre el total impreso y la suma de subtítulos es exactamente `vigente_mes(15) − percibido(15)`.
- El total general cumple `saldo_por_percibir = vigente_mes − percibido`; las otras ocho métricas calzan contra la suma de subtítulos.

La rehabilitación no autoriza a cambiar los ceros impresos de la cuenta 15 ni a sustituir el total. Debe conservar simultáneamente el detalle, el total y la diferencia explicada.

## 2. Fuentes y localización

| Documento | Archivo | SHA-256 | Detalle | Total DEUDORES | Cuenta 15 |
|---|---|---|---:|---|---|
| ESP_2023-12_INGRESOS_ORIGINAL | `2023-12esp dic municipalidad ingresos.pdf` | `5b9f2257edf20b21d277cb3c7de5dd5fe5bfe85988ac86e2ec0d5517492e5b96` | 195 líneas | p. 1, l. 13 | p. 10, l. 37 |
| ESP_2024-12_INGRESOS_ORIGINAL | `esp dic municipalidad ingresos.pdf` | `2fd3c635ee378b971563fc7649c1144109c04b20340b40dc5080735282e07eb3` | 205 líneas | p. 1, l. 13 | p. 11, l. 20 |
| ESP_2025-12_INGRESOS_ORIGINAL | `esp dic municipalidad ingresos.pdf` | `7cba71d66e52378db18fd3d9988816b92c6a85a677c2ff65fdd058d35379de5c` | 191 líneas | p. 1, l. 13 | p. 10, l. 30 |

Las rutas completas están en `evidencia_visual_diciembre.csv` y en los parseos de trabajo. Los PDF originales no fueron modificados.

## 3. Reconstrucción métrica por métrica

La suma usa los diez subtítulos de nivel 1 de cada documento. “Diferencia” es total impreso menos suma del detalle.

### Diciembre de 2023

| Métrica | Suma detalle | Total impreso | Diferencia |
|---|---:|---:|---:|
| Presupuesto inicial | 37.938.207.000 | 37.938.207.000 | 0 |
| Modificación presupuestaria | 13.676.452.416 | 13.676.452.416 | 0 |
| Presupuesto vigente | 51.614.659.416 | 51.614.659.416 | 0 |
| Presupuesto vigente al mes | 51.614.659.416 | 51.614.659.416 | 0 |
| Ingreso devengado | 46.640.788.589 | 46.640.788.589 | 0 |
| Ingreso percibido | 43.594.896.390 | 43.594.896.390 | 0 |
| Ingreso por percibir | 3.045.892.199 | 3.045.892.199 | 0 |
| Saldo por devengar | -1.867.714.055 | -1.867.714.055 | 0 |
| **Saldo por percibir** | **1.178.178.144** | **8.019.763.026** | **6.841.584.882** |

### Diciembre de 2024

| Métrica | Suma detalle | Total impreso | Diferencia |
|---|---:|---:|---:|
| Presupuesto inicial | 55.608.648.000 | 55.608.648.000 | 0 |
| Modificación presupuestaria | 4.377.504.000 | 4.377.504.000 | 0 |
| Presupuesto vigente | 59.986.152.000 | 59.986.152.000 | 0 |
| Presupuesto vigente al mes | 59.986.152.000 | 59.986.152.000 | 0 |
| Ingreso devengado | 53.288.878.458 | 53.288.878.458 | 0 |
| Ingreso percibido | 49.228.785.129 | 49.228.785.129 | 0 |
| Ingreso por percibir | 4.060.093.329 | 4.060.093.329 | 0 |
| Saldo por devengar | -2.168.501.458 | -2.168.501.458 | 0 |
| **Saldo por percibir** | **1.891.591.871** | **10.757.366.871** | **8.865.775.000** |

### Diciembre de 2025

| Métrica | Suma detalle | Total impreso | Diferencia |
|---|---:|---:|---:|
| Presupuesto inicial | 61.538.548.000 | 61.538.548.000 | 0 |
| Modificación presupuestaria | 1.880.954.043 | 1.880.954.043 | 0 |
| Presupuesto vigente | 63.419.502.043 | 63.419.502.043 | 0 |
| Presupuesto vigente al mes | 63.419.502.043 | 63.419.502.043 | 0 |
| Ingreso devengado | 52.067.365.781 | 52.067.365.781 | 0 |
| Ingreso percibido | 48.494.655.604 | 48.494.655.604 | 0 |
| Ingreso por percibir | 3.572.710.177 | 3.572.710.177 | 0 |
| Saldo por devengar | 3.592.118.262 | 3.592.118.262 | 0 |
| **Saldo por percibir** | **7.164.828.439** | **14.924.846.439** | **7.760.018.000** |

## 4. Reconciliación de la cuenta 15

| Año | Vigente al mes | Devengado | Percibido | Por percibir impreso | Saldo por devengar impreso | Saldo por percibir impreso | Vigente − percibido |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 6.841.584.882 | 0 | 0 | 0 | 0 | 0 | 6.841.584.882 |
| 2024 | 8.865.775.000 | 0 | 0 | 0 | 0 | 0 | 8.865.775.000 |
| 2025 | 7.760.018.000 | 0 | 0 | 0 | 0 | 0 | 7.760.018.000 |

Comprobaciones exactas:

- 2023: `1.178.178.144 + 6.841.584.882 = 8.019.763.026`.
- 2024: `1.891.591.871 + 8.865.775.000 = 10.757.366.871`.
- 2025: `7.164.828.439 + 7.760.018.000 = 14.924.846.439`.

En cada año, la misma diferencia se reproduce en las cuentas hijas `15.01` y `15.02` según sus propios importes; no se corrigieron sus saldos impresos.

## 5. Prueba ordenada de hipótesis

| Orden | Hipótesis | Resultado | Evidencia |
|---:|---|---|---|
| i | El total incluye una partida no presente en el detalle | **Descartada en su forma literal** | La cuenta 15 sí está presente. El total incorpora su vigente menos percibido aunque el saldo de la línea esté impreso en cero. |
| ii | Problema de signo | **Descartada** | Los campos de la cuenta 15 son ceros, no valores negativos. Ningún cambio de signo de una línea reproduce el total. Los recortes confirman los signos negativos de otras columnas del total. |
| iii | El parser tomó un subtotal por el total o viceversa | **Descartada** | La línea usada es `DEUDORES PRESUPUESTARIOS`, p. 1, l. 13 en los tres PDF. Ningún subtotal del detalle tiene el mismo saldo por percibir que el total; las otras ocho métricas calzan. |
| iv | Redondeo | **Descartado** | Las diferencias son 6.841.584.882, 8.865.775.000 y 7.760.018.000 CLP y coinciden exactamente con la cuenta 15; no son diferencias de redondeo. |

## 6. Política recomendada para rehabilitación

Para cada ESP de ingresos que se incorpore, documentar y exigir simultáneamente:

1. Las ocho métricas distintas de `saldo_por_percibir_clp` calzan entre total impreso y suma de subtítulos.
2. `total_saldo_por_percibir = total_vigente_mes − total_percibido`.
3. `total_saldo_por_percibir − suma_detalle_saldo_por_percibir = vigente_mes_cuenta_15 − percibido_cuenta_15`.
4. La cuenta 15 conserva sus saldos impresos, incluidos los ceros, y toda la trazabilidad original.
5. La nota metodológica debe indicar que el total general de saldo por percibir incluye el saldo inicial de caja por su vigente menos percibido, mientras la línea de detalle publica saldo cero.

Este memo no modifica el canónico ni rehabilita documentos por sí mismo. Si algún documento no reproduce estas condiciones, debe permanecer en cuarentena y analizarse separadamente.

## 7. Evidencia reproducible

Directorio: `trabajo/07_Información_Presupuestaria/descuadre_esp_ingresos/`.

- `reconstruccion_9_metricas_diciembre.csv`: 27 reconstrucciones métrica–documento.
- `anomalias_aritmeticas_diciembre.csv`: líneas 15, 15.01 y 15.02 con valores, diferencias y trazabilidad.
- `detalle_nivel_1_diciembre.csv`: subtítulos usados en las sumas.
- `coincidencias_exactas_diciembre.csv`: cotejo entre la diferencia y la cuenta 15.
- `resumen_hipotesis_diciembre.json`: resultados computados por documento.
- `evidencia_visual_diciembre.csv`: coordenadas, texto y rutas de seis recortes.
- `evidencia_visual/`: tres totales y tres líneas de cuenta 15 renderizados desde los PDF.

Reproducción desde la raíz del workspace:

```bash
python "scripts/analizar_descuadre_esp_ingresos.py"
python "scripts/renderizar_evidencia_descuadre_esp.py"
```
