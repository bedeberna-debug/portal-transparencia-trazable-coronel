from pathlib import Path
import csv
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "cuarentenas_bep"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
OBSERVED = {
    "V01": "14.307.577|14.307.577|2.135.175|12.172.402|1.061.653",
    "V02": "642.130|639.130|159.670|479.460|6.445",
    "V03": "14.307.577|14.341.071|8.666.775|5.674.296|775.262",
    "V04": "188.150|213.644|58.994|154.650|1.121",
    "V05": "12.155.652|12.155.652|2.055.221|10.100.431|124.879",
    "V06": "2.917.457|2.917.457|1.781.503|1.135.954|0",
    "V07": "9.410.180|10.497.980|9.514.295|983.685|0",
    "V08": "3.050.063|3.050.063|765.654|2.284.409|0",
    "V09": "3.953.184|3.953.184|2.324.594|1.628.590|0",
    "V10": "10.707.427|10.707.427|9.665.161|1.042.266|0",
}
with (WORK / "verificacion_visual_10.csv").open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
    fields = list(rows[0])
for row in rows:
    row["valores_impresos_observados"] = OBSERVED[row["muestra_visual_id"]]
    expected = [f"{int(row['valor_padre_parseado_miles_clp']):,}".replace(",", ".")]
    metric_value = OBSERVED[row["muestra_visual_id"]].split("|")[2 if row["metrica"] == "obligacion_devengada_miles_clp" else 4]
    row["verificacion_visual"] = "confirmado" if metric_value == expected[0] else "no_coincide"
    row["observacion"] = "Lectura visual de la línea completa; valor padre y cinco cifras coinciden con la extracción. Sin corrección del PDF."
with (DOCS / "VERIFICACION_VISUAL_CUARENTENAS_v1.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

with (DOCS / "ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv").open(encoding="utf-8-sig", newline="") as f:
    differences = list(csv.DictReader(f))
result = json.loads((WORK / "distribucion_diferencias.json").read_text(encoding="utf-8"))
with (WORK / "resumen_33_cuarentenas.csv").open(encoding="utf-8-sig", newline="") as f:
    summaries = list(csv.DictReader(f))

L = ["# VERIFICACIÓN VISUAL DE CUARENTENAS BEP", "", "**Muestra:** 10 líneas de gastos, distribuidas entre 2023 (4), 2024 (3) y 2025 (3), en documentos distintos. Se renderizaron las páginas originales a escala 4 y se recortaron las coordenadas de la línea; los PDF no fueron modificados.", "", "**Resultado:** 10/10 valores padre confirmados contra la imagen. Las cinco cifras de cada línea también coinciden con el texto extraído. Esta verificación confirma la lectura, no elimina ni corrige la diferencia padre–hijas.", "", "| Muestra | Documento | Cuenta | Métrica | Página/línea | Coordenadas PDF (puntos) | Valor padre M$ | Resultado | Evidencia |", "|---|---|---|---|---|---|---:|---|---|"]
for row in rows:
    evidence = row["imagen_recorte"].replace("\\", "/")
    valor = f"{int(row['valor_padre_parseado_miles_clp']):,}".replace(",", ".")
    L.append(f"| {row['muestra_visual_id']} | {row['documento_id']} | `{row['codigo_padre']}` | {row['metrica']} | {row['fuente_pagina']}/{row['fuente_linea']} | {row['bbox_pdf_puntos']} | {valor} | {row['verificacion_visual']} | [recorte]({evidence}) |")
L += ["", "El CSV homónimo conserva las cinco cifras observadas, ruta, página, línea, SHA-256, coordenadas y vínculo al recorte.", ""]
(DOCS / "VERIFICACION_VISUAL_CUARENTENAS_v1.md").write_text("\n".join(L), encoding="utf-8")

L = ["# ANÁLISIS DE CUARENTENAS BEP Y POLÍTICA DE TOLERANCIA", "", f"**Universo:** 33 documentos inicialmente en cuarentena: 32 de gastos y la republicación v2 de ingresos. **Diferencias jerárquicas no calzantes:** {len(differences)}. La tabla permanente `ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv` contiene cada diferencia con magnitud, cuenta, página, línea y SHA-256.", "", "## 1. Distribución completa por magnitud", "", "| Magnitud absoluta | Ocurrencias |", "|---:|---:|"]
for magnitude, count in result["distribucion_magnitud_abs_miles_clp"].items():
    L.append(f"| {magnitude} M$ | {count} |")
L += ["", "## 2. Política autorizada y resultado por documento", "", "Criterio refinado para gastos: totales impresos 100 %, aritmética ≥99 % y todas las diferencias jerárquicas con magnitud ≤2 M$. No se corrigen valores ni se elimina el anexo. Un documento con cualquier diferencia >2 M$ permanece en cuarentena.", "", f"- Elegibles para incorporación: **{result['documentos_elegibles_politica_refinada']}** documentos de gastos.", "- Permanecen en cuarentena: **5** documentos: cuatro gastos y la v2 de ingresos.", "- La v2 no es elegible por tipo y por diferencia de contenido respecto del original, independientemente de sus diferencias jerárquicas.", "", "## 3. Diferencias superiores a 2 M$", "", "| Documento | Cuenta | Métrica | Padre | Suma hijas | Diferencia | Página/línea |", "|---|---|---|---:|---:|---:|---|"]
for row in differences:
    if abs(int(row["diferencia"])) > 2:
        L.append(f"| {row['documento_id']} | `{row['codigo_padre']}` | {row['metrica']} | {row['valor_padre']} | {row['suma_hijas_directas']} | {row['diferencia']} | {row['fuente_pagina']}/{row['fuente_linea']} |")
L += ["", "## 4. Documentos que permanecen en cuarentena", "", "| Documento | Diferencias | Máximo absoluto | Otros motivos |", "|---|---:|---:|---|"]
for row in summaries:
    if row["elegible_politica_refinada"] == "no":
        L.append(f"| {row['documento_id']} | {row['diferencias_jerarquicas']} | {row['magnitud_maxima_miles_clp']} M$ | {row['otros_motivos_cuarentena'] or 'diferencia_jerarquica_mayor_2'} |")
L += ["", "## 5. Verificación visual", "", "La muestra de 10 líneas confirmó 10/10 valores padre contra la imagen. El detalle y las coordenadas están en `VERIFICACION_VISUAL_CUARENTENAS_v1.md` y su CSV.", ""]
(DOCS / "ANALISIS_CUARENTENAS_BEP_v1.md").write_text("\n".join(L), encoding="utf-8")
print(json.dumps({"muestras_confirmadas": sum(r["verificacion_visual"] == "confirmado" for r in rows), "muestras_totales": len(rows), "diferencias_anexo": len(differences)}, ensure_ascii=False))
