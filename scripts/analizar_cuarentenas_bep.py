from pathlib import Path
from collections import Counter, defaultdict
import csv
import json
import pdfplumber
import pypdfium2
from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "bep_etapa2"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "cuarentenas_bep"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
IMG = OUT / "verificacion_visual"
OUT.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def group_lines(words):
    lines = []
    for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if not lines or abs(lines[-1][0]["top"] - word["top"]) > 2:
            lines.append([word])
        else:
            lines[-1].append(word)
    return [sorted(line, key=lambda w: w["x0"]) for line in lines]


docs = []
hierarchy = []
for year in [2023, 2024, 2025]:
    docs.extend(json.loads((WORK / str(year) / f"documentos_bep_{year}.json").read_text(encoding="utf-8")))
    hierarchy.extend(read_csv(WORK / str(year) / f"bep_{year}_validacion_jerarquia.csv"))
doc_by_id = {d["documento_id"]: d for d in docs}
quarantined = [d for d in docs if d["estado"] != "aceptado"]
failures = []
for row in hierarchy:
    if row["documento_id"] not in {d["documento_id"] for d in quarantined} or row["resultado"] != "no_calza":
        continue
    doc = doc_by_id[row["documento_id"]]
    item = dict(row)
    item["diferencia"] = int(row["diferencia"])
    item["magnitud_abs_miles_clp"] = abs(item["diferencia"])
    item["archivo"] = doc["archivo"]
    item["ruta_relativa"] = doc["ruta_relativa"]
    item["sobre_2_miles_clp"] = "si" if abs(item["diferencia"]) > 2 else "no"
    failures.append(item)
failures.sort(key=lambda r: (r["periodo"], r["tipo"], r["documento_id"], r["codigo_padre"], r["metrica"]))
write_csv(DOCS / "ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv", failures)

summaries = []
for d in sorted(quarantined, key=lambda x: (x.get("periodo", "9999"), x.get("tipo", ""), x.get("version_fuente", ""))):
    doc_failures = [r for r in failures if r["documento_id"] == d["documento_id"]]
    is_gastos = d.get("tipo") == "gastos"
    no_over_2 = all(abs(r["diferencia"]) <= 2 for r in doc_failures)
    other_reasons = [m for m in d.get("motivos_cuarentena", []) if m != "jerarquia"]
    eligible = is_gastos and d.get("tasa_totales") == 1.0 and d.get("tasa_aritmetica", 0) >= .99 and no_over_2 and not other_reasons
    summaries.append({
        "documento_id": d["documento_id"], "periodo": d.get("periodo", ""), "tipo": d.get("tipo", ""),
        "version_fuente": d.get("version_fuente", ""), "archivo": d["archivo"], "ruta_relativa": d["ruta_relativa"], "sha256": d["sha256"],
        "diferencias_jerarquicas": len(doc_failures), "magnitud_maxima_miles_clp": max([abs(r["diferencia"]) for r in doc_failures] or [0]),
        "diferencias_sobre_2_miles_clp": sum(abs(r["diferencia"]) > 2 for r in doc_failures),
        "tasa_totales": d.get("tasa_totales", ""), "tasa_aritmetica": d.get("tasa_aritmetica", ""),
        "otros_motivos_cuarentena": "|".join(other_reasons), "elegible_politica_refinada": "si" if eligible else "no",
    })
write_csv(OUT / "resumen_33_cuarentenas.csv", summaries)

distribution = Counter(r["magnitud_abs_miles_clp"] for r in failures)
signed = Counter(r["diferencia"] for r in failures)
by_year = Counter(r["periodo"][:4] for r in failures)
by_metric = Counter(r["metrica"] for r in failures)
result = {
    "documentos_cuarentena": len(quarantined),
    "documentos_gastos_cuarentena": sum(d.get("tipo") == "gastos" for d in quarantined),
    "diferencias_no_calzantes": len(failures),
    "distribucion_magnitud_abs_miles_clp": {str(k): distribution[k] for k in sorted(distribution)},
    "distribucion_diferencia_con_signo_miles_clp": {str(k): signed[k] for k in sorted(signed)},
    "por_anio": dict(sorted(by_year.items())), "por_metrica": dict(sorted(by_metric.items())),
    "diferencias_sobre_2_miles_clp": sum(abs(r["diferencia"]) > 2 for r in failures),
    "documentos_elegibles_politica_refinada": sum(s["elegible_politica_refinada"] == "si" for s in summaries),
    "documentos_no_elegibles": [s["documento_id"] for s in summaries if s["elegible_politica_refinada"] == "no"],
}
(OUT / "distribucion_diferencias.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

# Diez líneas de gastos, distribuidas por año y por documentos distintos.
gastos = [r for r in failures if r["tipo"] == "gastos"]
selected = []
for year, count in [("2023", 4), ("2024", 3), ("2025", 3)]:
    year_rows = [r for r in gastos if r["periodo"].startswith(year)]
    by_doc = defaultdict(list)
    for r in year_rows:
        by_doc[r["documento_id"]].append(r)
    doc_ids = sorted(by_doc)
    indexes = []
    for i in range(count):
        idx = int((i + .5) * len(doc_ids) / count)
        while idx in indexes:
            idx = (idx + 1) % len(doc_ids)
        indexes.append(idx)
    for idx in indexes:
        did = doc_ids[idx]
        candidates = sorted(by_doc[did], key=lambda r: (-abs(r["diferencia"]), r["codigo_padre"], r["metrica"]))
        selected.append(candidates[0])

visual_rows = []
for number, row in enumerate(selected, 1):
    sample_id = f"V{number:02d}"
    path = ROOT / row["ruta_relativa"]
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[int(row["fuente_pagina"]) - 1]
        words = page.extract_words(x_tolerance=1, y_tolerance=2)
        lines = group_lines(words)
        target = lines[int(row["fuente_linea"]) - 1]
        x0 = min(w["x0"] for w in target)
        x1 = max(w["x1"] for w in target)
        top = min(w["top"] for w in target)
        bottom = max(w["bottom"] for w in target)
        raw = " ".join(w["text"] for w in target)
    pdfium = pypdfium2.PdfDocument(str(path))
    scale = 4
    image = pdfium[int(row["fuente_pagina"]) - 1].render(scale=scale).to_pil().convert("RGB")
    crop_left = max(0, int(25 * scale))
    crop_right = min(image.width, int((page.width - 15) * scale))
    crop_top = max(0, int((top - 18) * scale))
    crop_bottom = min(image.height, int((bottom + 18) * scale))
    crop = image.crop((crop_left, crop_top, crop_right, crop_bottom))
    draw = ImageDraw.Draw(crop)
    draw.rectangle((int(x0 * scale) - crop_left - 4, int(top * scale) - crop_top - 3, int(x1 * scale) - crop_left + 4, int(bottom * scale) - crop_top + 3), outline="red", width=3)
    image_path = IMG / f"{sample_id}_{row['documento_id']}_p{row['fuente_pagina']}_l{row['fuente_linea']}.png"
    crop.save(image_path, optimize=True)
    visual_rows.append({
        "muestra_visual_id": sample_id, "documento_id": row["documento_id"], "periodo": row["periodo"],
        "codigo_padre": row["codigo_padre"], "denominacion_padre": row["denominacion_padre"], "metrica": row["metrica"],
        "valor_padre_parseado_miles_clp": row["valor_padre"], "suma_hijas_directas_miles_clp": row["suma_hijas_directas"],
        "diferencia_miles_clp": row["diferencia"], "fuente_archivo": row["archivo"], "fuente_ruta_relativa": row["ruta_relativa"],
        "fuente_pagina": row["fuente_pagina"], "fuente_linea": row["fuente_linea"], "fuente_sha256": row["fuente_sha256"],
        "bbox_pdf_puntos": f"{x0:.2f},{top:.2f},{x1:.2f},{bottom:.2f}", "texto_linea_extraida": raw,
        "imagen_recorte": str(image_path.relative_to(ROOT)), "valores_impresos_observados": "",
        "verificacion_visual": "pendiente", "observacion": "",
    })
write_csv(OUT / "verificacion_visual_10.csv", visual_rows)
result["muestra_visual"] = [r["muestra_visual_id"] for r in visual_rows]
(OUT / "distribucion_diferencias.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
