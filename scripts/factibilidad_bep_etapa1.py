from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import re
import pdfplumber

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria"
CATALOG = ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "factibilidad"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLES = [
    {"id": "BEP_GASTOS_2023_12", "tipo": "gastos", "anio": 2023, "path": RAW / "Balance de Ejecución Presupuestaria" / "2023" / "2023bep dic municipalidad gastos.pdf"},
    {"id": "BEP_INGRESOS_2023_12", "tipo": "ingresos", "anio": 2023, "path": RAW / "Balance de Ejecución Presupuestaria" / "2023" / "2023bep dic municipalidad ingreso.pdf"},
    {"id": "BEP_GASTOS_2025_12", "tipo": "gastos", "anio": 2025, "path": RAW / "Balance de Ejecución Presupuestaria" / "2025" / "bep dic municipalidad gastos.pdf"},
    {"id": "BEP_INGRESOS_2025_12", "tipo": "ingresos", "anio": 2025, "path": RAW / "Balance de Ejecución Presupuestaria" / "2025" / "bep dic municipalidad ingresos.pdf"},
]

CONFIG = {
    "gastos": {
        "formulario": "0102",
        "anchors": [333, 390, 446, 503, 565],
        "metrics": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp", "saldo_presupuestario_miles_clp", "deuda_exigible_miles_clp"],
        "code_bands": [(60, 72, 2, 1), (76, 91, 2, 2), (92, 108, 3, 3), (109, 125, 3, 4), (125, 144, 3, 5)],
        "denom_min": 140,
    },
    "ingresos": {
        "formulario": "0101",
        "anchors": [313, 370, 429, 489, 550],
        "metrics": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "ingresos_percibidos_miles_clp", "saldo_presupuestario_miles_clp", "ingresos_por_percibir_miles_clp"],
        "code_bands": [(39, 53, 2, 1), (54, 71, 2, 2), (72, 86, 3, 3), (86, 104, 3, 4)],
        "denom_min": 105,
    },
}
NUM_RE = re.compile(r"^-?(?:\d+|\d{1,3}(?:\.\d{3})+)$")


def money(token):
    return int(token.replace(".", ""))


def group_lines(words):
    lines = []
    for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if not lines or abs(lines[-1][0]["top"] - word["top"]) > 2:
            lines.append([word])
        else:
            lines[-1].append(word)
    return [sorted(line, key=lambda w: w["x0"]) for line in lines]


def numeric_columns(line, anchors):
    values = {}
    raw = {}
    for word in line:
        token = word["text"]
        if word["x0"] < 270 or not NUM_RE.fullmatch(token):
            continue
        idx = min(range(5), key=lambda i: abs(word["x1"] - anchors[i]))
        if abs(word["x1"] - anchors[idx]) <= 16 and idx not in values:
            values[idx] = money(token)
            raw[idx] = token
    return values, raw


def locate_codes(line, bands):
    candidates = []
    for word in line:
        token = word["text"]
        if not token.isdigit():
            continue
        for lo, hi, length, level in bands:
            if lo <= word["x0"] < hi and len(token) == length:
                candidates.append((word["x0"], level, token))
    candidates.sort()
    # Una línea puede imprimir simultáneamente asignación y subasignación.
    return [(level, token) for _, level, token in candidates]


def parse_document(sample, allow_continuation_pages=False):
    cfg = CONFIG[sample["tipo"]]
    path = sample["path"]
    sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    records = []
    totals = None
    context = []
    last_record = None
    form_seen = set()
    period_seen = set()
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, 1):
            words = page.extract_words(x_tolerance=1, y_tolerance=2)
            lines = group_lines(words)
            page_text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
            form_seen.update(re.findall(r"Formulario\s+(\d{4})", page_text))
            period_seen.update(re.findall(r"(?:GASTOS|INGRESOS)\s+AL\s+(\d{2}/\d{2}/\d{4})", page_text))
            header_lines = [i for i, line in enumerate(lines, 1) if any(w["text"] == "Denominación" for w in line) and any(w["text"] == "(M$)" for w in line)]
            if len(header_lines) != 1:
                if allow_continuation_pages and not header_lines and page_no > 1:
                    data_start_line = 0
                else:
                    raise ValueError(f"Encabezado de formulario no único: {sample['id']} p.{page_no}")
            else:
                data_start_line = header_lines[0]
            for line_no, line in enumerate(lines, 1):
                if line_no <= data_start_line:
                    continue
                values, raw_values = numeric_columns(line, cfg["anchors"])
                raw_line = " ".join(w["text"] for w in line)
                if any(w["text"] == "TOTALES" for w in line):
                    combined = dict(values)
                    combined_raw = dict(raw_values)
                    if len(combined) < 5 and line_no < len(lines):
                        next_values, next_raw = numeric_columns(lines[line_no], cfg["anchors"])
                        combined.update(next_values)
                        combined_raw.update(next_raw)
                    if len(combined) == 5:
                        totals = {
                            "pagina": page_no,
                            "lineas": [line_no, line_no + 1] if line_no < len(lines) and numeric_columns(lines[line_no], cfg["anchors"])[0] else [line_no],
                            "valores": {cfg["metrics"][i]: combined[i] for i in range(5)},
                            "valores_raw": {cfg["metrics"][i]: combined_raw[i] for i in range(5)},
                            "texto_raw": raw_line + (" " + " ".join(w["text"] for w in lines[line_no]) if line_no < len(lines) else ""),
                        }
                    continue
                if len(values) != 5:
                    # Continuación de denominación: sin cifras y dentro de la zona de texto.
                    if last_record is not None:
                        continuation = " ".join(w["text"] for w in line if cfg["denom_min"] <= w["x0"] < 270)
                        if continuation and not any(k in continuation for k in ["MUNICIPALIDAD", "Formulario", "BALANCE", "PRESUPUESTARIA", "Clasificador"]):
                            last_record["denominacion_pdf"] = (last_record["denominacion_pdf"] + " " + continuation).strip()
                    continue
                codes = locate_codes(line, cfg["code_bands"])
                if not codes:
                    raise ValueError(f"Línea con cinco montos sin clasificador: {sample['id']} p.{page_no} l.{line_no}: {raw_line}")
                for level, code_part in codes:
                    context = context[: level - 1] + [code_part]
                level = codes[-1][0]
                code = ".".join(context)
                denomination = " ".join(w["text"] for w in line if cfg["denom_min"] <= w["x0"] < 270)
                rec = {
                    "muestra_id": sample["id"],
                    "tipo": sample["tipo"],
                    "periodo": f"{sample['anio']}-12",
                    "codigo_cuenta_pdf": code,
                    "nivel_jerarquico": level,
                    "denominacion_pdf": denomination,
                    "fuente_archivo": path.name,
                    "fuente_ruta_relativa": str(path.relative_to(ROOT)),
                    "fuente_pagina": page_no,
                    "fuente_linea": line_no,
                    "fuente_sha256": sha256,
                    "texto_linea_raw": raw_line,
                }
                for i, metric in enumerate(cfg["metrics"]):
                    rec[metric] = values[i]
                    rec[metric + "_raw"] = raw_values[i]
                records.append(rec)
                last_record = rec
    if totals is None:
        raise ValueError(f"Sin TOTALES: {sample['id']}")
    return records, totals, sorted(form_seen), sorted(period_seen), sha256


def main():
    catalog_rows = json.loads(CATALOG.read_text(encoding="utf-8"))
    catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
    assert len(catalog_rows) == 451 and len(catalog) == 451
    all_records = []
    all_line_checks = []
    all_hierarchy = []
    doc_summaries = []
    findings = []

    for sample in SAMPLES:
        records, totals, forms, periods, sha256 = parse_document(sample)
        cfg = CONFIG[sample["tipo"]]
        by_code = {r["codigo_cuenta_pdf"]: r for r in records}
        if len(by_code) != len(records):
            seen = set()
            duplicates = []
            for rec in records:
                code = rec["codigo_cuenta_pdf"]
                if code in seen:
                    duplicates.append(f"{code} (p.{rec['fuente_pagina']} l.{rec['fuente_linea']})")
                seen.add(code)
            raise ValueError(f"Códigos duplicados en {sample['id']}: {duplicates}")
        for rec in records:
            code = rec["codigo_cuenta_pdf"]
            in_catalog = code in catalog
            level = rec["nivel_jerarquico"]
            if in_catalog:
                catalog_status = "encontrada"
            elif level > 3:
                catalog_status = "fuera_catalogo_nivel_detalle_no_representado"
            else:
                catalog_status = "fuera_catalogo_mismo_nivel"
            rec["catalogo_estado"] = catalog_status
            rec["catalogo_denominacion"] = catalog.get(code, {}).get("DENOMINACIÓN", "")
            arith_ok = rec[cfg["metrics"][3]] == rec[cfg["metrics"][1]] - rec[cfg["metrics"][2]]
            rec["control_aritmetico_saldo"] = "calza" if arith_ok else "no_calza"
            rec["control_aritmetico_diferencia"] = rec[cfg["metrics"][3]] - (rec[cfg["metrics"][1]] - rec[cfg["metrics"][2]])
            all_line_checks.append({
                "muestra_id": sample["id"], "codigo_cuenta_pdf": code, "nivel_jerarquico": level,
                "catalogo_estado": catalog_status, "control_aritmetico_saldo": rec["control_aritmetico_saldo"],
                "control_aritmetico_diferencia": rec["control_aritmetico_diferencia"],
                "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
            })
            if not in_catalog:
                findings.append({
                    "hallazgo_tipo": "codigo_fuera_catalogo",
                    "subtipo": catalog_status,
                    "muestra_id": sample["id"], "codigo_cuenta_pdf": code,
                    "denominacion_pdf": rec["denominacion_pdf"], "fuente_pagina": rec["fuente_pagina"],
                    "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
                })
            if not arith_ok:
                findings.append({
                    "hallazgo_tipo": "aritmetica_linea", "subtipo": "saldo_no_igual_vigente_menos_ejecutado",
                    "muestra_id": sample["id"], "codigo_cuenta_pdf": code,
                    "denominacion_pdf": rec["denominacion_pdf"], "diferencia": rec["control_aritmetico_diferencia"],
                    "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
                })

        for parent in records:
            pcode = parent["codigo_cuenta_pdf"]
            plevel = parent["nivel_jerarquico"]
            children = [r for r in records if r["nivel_jerarquico"] == plevel + 1 and r["codigo_cuenta_pdf"].startswith(pcode + ".")]
            if not children:
                continue
            for metric in cfg["metrics"]:
                expected = sum(c[metric] for c in children)
                printed = parent[metric]
                check = {
                    "muestra_id": sample["id"], "codigo_padre": pcode, "denominacion_padre": parent["denominacion_pdf"],
                    "nivel_padre": plevel, "metrica": metric, "valor_padre": printed, "suma_hijas_directas": expected,
                    "diferencia": printed - expected, "resultado": "calza" if printed == expected else "no_calza",
                    "hijas_directas": len(children), "fuente_pagina_padre": parent["fuente_pagina"],
                    "fuente_linea_padre": parent["fuente_linea"], "fuente_sha256": sha256,
                }
                all_hierarchy.append(check)
                if printed != expected:
                    findings.append({
                        "hallazgo_tipo": "jerarquia", "subtipo": "padre_distinto_suma_hijas_directas",
                        "muestra_id": sample["id"], "codigo_cuenta_pdf": pcode, "metrica": metric,
                        "valor_padre": printed, "suma_hijas": expected, "diferencia": printed - expected,
                        "fuente_pagina": parent["fuente_pagina"], "fuente_linea": parent["fuente_linea"], "fuente_sha256": sha256,
                    })

        top = [r for r in records if r["nivel_jerarquico"] == 1]
        total_checks = []
        for metric in cfg["metrics"]:
            parsed_sum = sum(r[metric] for r in top)
            printed = totals["valores"][metric]
            total_checks.append({
                "muestra_id": sample["id"], "metrica": metric, "total_impreso": printed,
                "suma_subtitulos_parseados": parsed_sum, "diferencia": printed - parsed_sum,
                "resultado": "calza" if printed == parsed_sum else "no_calza",
                "fuente_pagina_totales": totals["pagina"], "fuente_sha256": sha256,
            })
            if printed != parsed_sum:
                findings.append({
                    "hallazgo_tipo": "total_general", "subtipo": "total_impreso_distinto_suma_subtitulos",
                    "muestra_id": sample["id"], "metrica": metric, "total_impreso": printed,
                    "suma_subtitulos": parsed_sum, "diferencia": printed - parsed_sum,
                    "fuente_pagina": totals["pagina"], "fuente_sha256": sha256,
                })
        all_records.extend(records)
        doc_h = [h for h in all_hierarchy if h["muestra_id"] == sample["id"]]
        doc_summaries.append({
            "muestra_id": sample["id"], "archivo": sample["path"].name, "ruta_relativa": str(sample["path"].relative_to(ROOT)),
            "sha256": sha256, "formularios": forms, "fechas_corte_contenido": periods,
            "lineas_parseadas": len(records), "cuentas_en_catalogo": sum(r["catalogo_estado"] == "encontrada" for r in records),
            "detalle_no_representado": sum(r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for r in records),
            "fuera_catalogo_mismo_nivel": sum(r["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for r in records),
            "controles_jerarquia": len(doc_h), "jerarquia_calzan": sum(h["resultado"] == "calza" for h in doc_h),
            "totales_calzan": sum(t["resultado"] == "calza" for t in total_checks), "controles_totales": len(total_checks),
            "aritmetica_calza": sum(r["control_aritmetico_saldo"] == "calza" for r in records),
            "totales_impresos": totals["valores"], "sumas_subtitulos": {t["metrica"]: t["suma_subtitulos_parseados"] for t in total_checks},
        })

    def write_csv(name, rows):
        if not rows:
            return
        keys = list(dict.fromkeys(k for row in rows for k in row))
        with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    write_csv("bep_muestra_parseado.csv", all_records)
    write_csv("validacion_lineas.csv", all_line_checks)
    write_csv("validacion_jerarquia.csv", all_hierarchy)
    write_csv("hallazgos_factibilidad.csv", findings)

    summary = {
        "alcance": "Etapa 1; cuatro BEP de diciembre; no incluye ESP ni procesamiento masivo",
        "catalogo": {"archivo": CATALOG.name, "cuentas": len(catalog), "niveles_representados": "subtitulo/item/asignacion"},
        "totales": {
            "lineas": len(all_records),
            "catalogo_encontradas": sum(r["catalogo_estado"] == "encontrada" for r in all_records),
            "detalle_no_representado": sum(r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for r in all_records),
            "fuera_catalogo_mismo_nivel": sum(r["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for r in all_records),
            "controles_jerarquia": len(all_hierarchy),
            "jerarquia_calzan": sum(h["resultado"] == "calza" for h in all_hierarchy),
            "controles_totales": len(doc_summaries) * 5,
            "totales_calzan": sum(d["totales_calzan"] for d in doc_summaries),
            "aritmetica_calza": sum(r["control_aritmetico_saldo"] == "calza" for r in all_records),
        },
        "documentos": doc_summaries,
        "hallazgos": len(findings),
    }
    (OUT / "resumen_factibilidad.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
