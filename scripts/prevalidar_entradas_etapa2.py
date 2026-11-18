from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import sys
import pdfplumber

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "prevalidacion_etapa2"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "scripts"))
from factibilidad_bep_etapa1 import parse_document, CONFIG

BEP = {
    "id": "BEP_GASTOS_2024_06_PREV",
    "tipo": "gastos",
    "anio": 2024,
    "path": RAW / "Balance de Ejecución Presupuestaria" / "2024" / "bep jun municipalidad gastos.pdf",
}
ESP = [
    ("ESP_GASTOS_2023_12_PREV", RAW / "Estado de Situación Financiera" / "2023" / "Gastos 2023" / "esp dic municipalidad gastos.pdf"),
    ("ESP_GASTOS_2025_12_PREV", RAW / "Estado de Situación Financiera" / "2025" / "Gastos 2025" / "esp dic municipalidad gastos.pdf"),
]

def write_csv(name, rows):
    if not rows:
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def validate_bep():
    records, totals, forms, periods, sha256 = parse_document(BEP)
    cfg = CONFIG[BEP["tipo"]]
    catalog = {r["RUTA_JERARQUICA"] for r in json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))}
    line_rows = []
    hierarchy = []
    total_rows = []
    for rec in records:
        code = rec["codigo_cuenta_pdf"]
        level = rec["nivel_jerarquico"]
        if code in catalog:
            status = "encontrada"
        elif level > 3:
            status = "nivel_detalle_no_representado"
        else:
            status = "fuera_catalogo_mismo_nivel"
        diff = rec[cfg["metrics"][3]] - (rec[cfg["metrics"][1]] - rec[cfg["metrics"][2]])
        line_rows.append({
            "muestra_id": BEP["id"], "codigo_cuenta_pdf": code, "nivel_jerarquico": level,
            "denominacion_pdf": rec["denominacion_pdf"], "catalogo_estado": status,
            "control_aritmetico": "calza" if diff == 0 else "no_calza", "diferencia_aritmetica": diff,
            "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
        })
    for parent in records:
        code = parent["codigo_cuenta_pdf"]
        level = parent["nivel_jerarquico"]
        children = [r for r in records if r["nivel_jerarquico"] == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
        for metric in cfg["metrics"] if children else []:
            expected = sum(c[metric] for c in children)
            diff = parent[metric] - expected
            hierarchy.append({
                "muestra_id": BEP["id"], "codigo_padre": code, "denominacion_padre": parent["denominacion_pdf"],
                "metrica": metric, "valor_padre": parent[metric], "suma_hijas_directas": expected,
                "diferencia": diff, "resultado": "calza" if diff == 0 else "no_calza",
                "fuente_pagina": parent["fuente_pagina"], "fuente_linea": parent["fuente_linea"], "fuente_sha256": sha256,
            })
    top = [r for r in records if r["nivel_jerarquico"] == 1]
    for metric in cfg["metrics"]:
        summed = sum(r[metric] for r in top)
        printed = totals["valores"][metric]
        total_rows.append({
            "muestra_id": BEP["id"], "metrica": metric, "total_impreso": printed,
            "suma_subtitulos": summed, "diferencia": printed - summed,
            "resultado": "calza" if printed == summed else "no_calza",
            "fuente_pagina_totales": totals["pagina"], "fuente_sha256": sha256,
        })
    write_csv("bep_2024_06_parseado.csv", records)
    write_csv("bep_2024_06_lineas.csv", line_rows)
    write_csv("bep_2024_06_jerarquia.csv", hierarchy)
    write_csv("bep_2024_06_totales.csv", total_rows)
    counts = Counter(r["catalogo_estado"] for r in line_rows)
    result = {
        "muestra_id": BEP["id"], "archivo": BEP["path"].name,
        "ruta_relativa": str(BEP["path"].relative_to(ROOT)), "sha256": sha256,
        "formularios": forms, "fechas_corte_contenido": periods,
        "lineas": len(records), "catalogo": dict(counts),
        "jerarquia_calzan": sum(r["resultado"] == "calza" for r in hierarchy),
        "controles_jerarquia": len(hierarchy),
        "totales_calzan": sum(r["resultado"] == "calza" for r in total_rows),
        "controles_totales": len(total_rows),
        "aritmetica_calza": sum(r["control_aritmetico"] == "calza" for r in line_rows),
        "diferencias_jerarquia": [r for r in hierarchy if r["resultado"] == "no_calza"],
        "diferencias_aritmetica": [r for r in line_rows if r["control_aritmetico"] == "no_calza"],
        "totales_impresos": totals["valores"],
    }
    return result

def inspect_esp():
    summaries = []
    for sample_id, path in ESP:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        chunks_text = []
        chunks_layout = []
        chunks_coords = []
        with pdfplumber.open(path) as pdf:
            for page_no, page in enumerate(pdf.pages, 1):
                text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
                layout = page.extract_text(layout=True, x_tolerance=2, y_tolerance=3) or ""
                words = page.extract_words(x_tolerance=1, y_tolerance=2)
                lines = []
                for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
                    if not lines or abs(lines[-1][0]["top"] - word["top"]) > 2:
                        lines.append([word])
                    else:
                        lines[-1].append(word)
                chunks_text.append(f"===== PÁGINA {page_no} =====\n{text}")
                chunks_layout.append(f"===== PÁGINA {page_no} =====\n{layout}")
                chunks_coords.append(f"===== PÁGINA {page_no} =====")
                for line in lines:
                    top = sum(w["top"] for w in line) / len(line)
                    chunks_coords.append(f"top={top:7.2f} | " + " | ".join(f"{w['text']}@{w['x0']:.1f}-{w['x1']:.1f}" for w in line))
            summaries.append({
                "muestra_id": sample_id, "archivo": path.name, "ruta_relativa": str(path.relative_to(ROOT)),
                "sha256": digest, "paginas": len(pdf.pages),
                "dimensiones": sorted({(p.width, p.height) for p in pdf.pages}),
            })
        (OUT / f"{sample_id}_texto.txt").write_text("\n\n".join(chunks_text), encoding="utf-8")
        (OUT / f"{sample_id}_layout.txt").write_text("\n\n".join(chunks_layout), encoding="utf-8")
        (OUT / f"{sample_id}_coordenadas.txt").write_text("\n".join(chunks_coords), encoding="utf-8")
    return summaries

result = {"bep": validate_bep(), "esp": inspect_esp()}
(OUT / "resumen_prevalidacion.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
