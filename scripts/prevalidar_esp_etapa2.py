from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re
import pdfplumber

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria" / "Estado de Situación Financiera"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "prevalidacion_etapa2"
OUT.mkdir(parents=True, exist_ok=True)
SAMPLES = [
    {"id": "ESP_GASTOS_2023_12_PREV", "anio": 2023, "path": RAW / "2023" / "Gastos 2023" / "esp dic municipalidad gastos.pdf"},
    {"id": "ESP_GASTOS_2025_12_PREV", "anio": 2025, "path": RAW / "2025" / "Gastos 2025" / "esp dic municipalidad gastos.pdf"},
]
METRICS = [
    "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
    "presupuesto_vigente_mes_clp", "obligacion_clp", "obligacion_devengada_clp", "pago_clp",
    "deuda_exigible_clp", "saldo_por_comprometer_clp", "saldo_por_devengar_clp", "saldo_por_pagar_clp",
]
ANCHORS = [286, 334, 388, 436, 484, 532, 580, 628, 676, 724, 772]
NUM_RE = re.compile(r"^-?(?:\d+|\d{1,3}(?:\.\d{3})+)$")
CODE_RE = re.compile(r"^\d{2}(?:\.\d{2,3})+$|^\d{2}$")

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

def numeric_columns(line):
    values, raw = {}, {}
    for word in line:
        token = word["text"]
        if word["x0"] < 230 or not NUM_RE.fullmatch(token):
            continue
        idx = min(range(len(ANCHORS)), key=lambda i: abs(word["x1"] - ANCHORS[i]))
        if abs(word["x1"] - ANCHORS[idx]) <= 5:
            if idx in values:
                raise ValueError(f"Columna numérica duplicada: {token}")
            values[idx] = money(token)
            raw[idx] = token
    return values, raw

def parse_document(sample):
    path = sample["path"]
    sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    records, totals, periods, titles = [], None, set(), set()
    last_record = None
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, 1):
            words = page.extract_words(x_tolerance=1, y_tolerance=2)
            lines = group_lines(words)
            text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
            for title_line in lines:
                title_raw = " ".join(w["text"] for w in title_line)
                if "E S T A D O" in title_raw and "G A S T O S" in title_raw:
                    periods.update(re.findall(r"\d{2}/\d{2}/\d{4}", title_raw))
            if "E S T A D O P R E S U P U E S T A R I O D E G A S T O S" in text:
                titles.add("ESTADO PRESUPUESTARIO DE GASTOS")
            header_lines = [i for i, line in enumerate(lines, 1) if any(w["text"] == "Cuenta" for w in line) and any(w["text"] == "Denominación" for w in line)]
            if len(header_lines) != 1:
                raise ValueError(f"Encabezado no único: {sample['id']} p.{page_no}")
            for line_no, line in enumerate(lines, 1):
                if line_no <= header_lines[0]:
                    continue
                values, raw_values = numeric_columns(line)
                raw_line = " ".join(w["text"] for w in line)
                if len(values) == len(METRICS):
                    if any(w["text"] == "ACREEDORES" for w in line):
                        if totals is not None:
                            raise ValueError(f"Total ACREEDORES duplicado: {sample['id']}")
                        totals = {
                            "pagina": page_no, "linea": line_no,
                            "valores": {METRICS[i]: values[i] for i in range(len(METRICS))},
                            "valores_raw": {METRICS[i]: raw_values[i] for i in range(len(METRICS))},
                            "texto_raw": raw_line,
                        }
                        continue
                    codes = [w["text"] for w in line if w["x0"] < 90 and CODE_RE.fullmatch(w["text"])]
                    if len(codes) != 1:
                        raise ValueError(f"Línea con once montos sin código único: {sample['id']} p.{page_no} l.{line_no}: {raw_line}")
                    code = codes[0]
                    rec = {
                        "muestra_id": sample["id"], "tipo": "gastos", "periodo": f"{sample['anio']}-12",
                        "codigo_cuenta_pdf": code, "nivel_jerarquico": len(code.split(".")),
                        "denominacion_pdf": " ".join(w["text"] for w in line if 140 <= w["x0"] < 240),
                        "fuente_archivo": path.name, "fuente_ruta_relativa": str(path.relative_to(ROOT)),
                        "fuente_pagina": page_no, "fuente_linea": line_no, "fuente_sha256": sha256,
                        "texto_linea_raw": raw_line,
                    }
                    for i, metric in enumerate(METRICS):
                        rec[metric] = values[i]
                        rec[metric + "_raw"] = raw_values[i]
                    records.append(rec)
                    last_record = rec
                elif values:
                    raise ValueError(f"Línea con columnas incompletas: {sample['id']} p.{page_no} l.{line_no}: {raw_line}")
                elif last_record is not None:
                    continuation = " ".join(w["text"] for w in line if 140 <= w["x0"] < 240)
                    if continuation and not any(k in continuation for k in ["PRESUPUESTO", "Vigente", "Saldo"]):
                        last_record["denominacion_pdf"] = (last_record["denominacion_pdf"] + " " + continuation).strip()
    if totals is None:
        raise ValueError(f"Sin total ACREEDORES: {sample['id']}")
    return records, totals, sorted(periods), sorted(titles), sha256

def write_csv(name, rows):
    if not rows:
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def main():
    plan_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "plan_municipal.json").read_text(encoding="utf-8"))
    plan = {r["RUTA_JERARQUICA"]: r for r in plan_rows}
    all_records, all_lines, all_hierarchy, all_totals, findings, summaries = [], [], [], [], [], []
    for sample in SAMPLES:
        records, totals, periods, titles, sha256 = parse_document(sample)
        if len({r["codigo_cuenta_pdf"] for r in records}) != len(records):
            raise ValueError(f"Códigos duplicados: {sample['id']}")
        for rec in records:
            code = rec["codigo_cuenta_pdf"]
            found = code in plan
            rec["catalogo_estado"] = "encontrada" if found else "fuera_plan_municipal"
            rec["catalogo_denominacion"] = plan.get(code, {}).get("N1_DENOMINACION", "")
            diff = rec["saldo_por_comprometer_clp"] - (rec["presupuesto_vigente_mes_clp"] - rec["obligacion_clp"])
            rec["control_aritmetico_saldo"] = "calza" if diff == 0 else "no_calza"
            rec["control_aritmetico_diferencia"] = diff
            identities = {
                "vigente_igual_inicial_mas_modificacion": rec["presupuesto_vigente_clp"] - (rec["presupuesto_inicial_clp"] + rec["modificacion_presupuestaria_clp"]),
                "exigible_igual_devengado_menos_pago": rec["deuda_exigible_clp"] - (rec["obligacion_devengada_clp"] - rec["pago_clp"]),
                "saldo_comprometer": diff,
                "saldo_devengar": rec["saldo_por_devengar_clp"] - (rec["obligacion_clp"] - rec["obligacion_devengada_clp"]),
                "saldo_por_pagar": rec["saldo_por_pagar_clp"] - (rec["obligacion_clp"] - rec["pago_clp"]),
            }
            for name, difference in identities.items():
                rec[f"control_{name}"] = "calza" if difference == 0 else "no_calza"
                rec[f"diferencia_{name}"] = difference
            line = {
                "muestra_id": sample["id"], "codigo_cuenta_pdf": code, "nivel_jerarquico": rec["nivel_jerarquico"],
                "denominacion_pdf": rec["denominacion_pdf"], "catalogo_estado": rec["catalogo_estado"],
                "control_aritmetico_saldo": rec["control_aritmetico_saldo"], "diferencia_aritmetica": diff,
                "controles_aritmeticos_adicionales_calzan": sum(rec[f"control_{name}"] == "calza" for name in identities),
                "controles_aritmeticos_adicionales": len(identities),
                "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
            }
            all_lines.append(line)
            if not found:
                findings.append({"hallazgo_tipo": "catalogo", "subtipo": "fuera_plan_municipal", **line})
            if diff != 0:
                findings.append({"hallazgo_tipo": "aritmetica", "subtipo": "saldo_comprometer_no_calza", **line})
        for parent in records:
            code, level = parent["codigo_cuenta_pdf"], parent["nivel_jerarquico"]
            children = [r for r in records if r["nivel_jerarquico"] == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
            for metric in METRICS if children else []:
                expected = sum(c[metric] for c in children)
                diff = parent[metric] - expected
                check = {
                    "muestra_id": sample["id"], "codigo_padre": code, "denominacion_padre": parent["denominacion_pdf"],
                    "nivel_padre": level, "metrica": metric, "valor_padre": parent[metric], "suma_hijas_directas": expected,
                    "diferencia": diff, "resultado": "calza" if diff == 0 else "no_calza", "hijas_directas": len(children),
                    "fuente_pagina": parent["fuente_pagina"], "fuente_linea": parent["fuente_linea"], "fuente_sha256": sha256,
                }
                all_hierarchy.append(check)
                if diff != 0:
                    findings.append({"hallazgo_tipo": "jerarquia", "subtipo": "padre_distinto_suma_hijas", **check})
        top = [r for r in records if r["nivel_jerarquico"] == 1]
        for metric in METRICS:
            summed = sum(r[metric] for r in top)
            printed = totals["valores"][metric]
            check = {
                "muestra_id": sample["id"], "metrica": metric, "total_impreso": printed,
                "suma_subtitulos": summed, "diferencia": printed - summed,
                "resultado": "calza" if printed == summed else "no_calza",
                "fuente_pagina_totales": totals["pagina"], "fuente_linea_totales": totals["linea"], "fuente_sha256": sha256,
            }
            all_totals.append(check)
            if printed != summed:
                findings.append({"hallazgo_tipo": "total_general", "subtipo": "total_impreso_no_calza", **check})
        all_records.extend(records)
        doc_h = [h for h in all_hierarchy if h["muestra_id"] == sample["id"]]
        doc_t = [t for t in all_totals if t["muestra_id"] == sample["id"]]
        summaries.append({
            "muestra_id": sample["id"], "archivo": sample["path"].name,
            "ruta_relativa": str(sample["path"].relative_to(ROOT)), "sha256": sha256,
            "titulos_contenido": titles, "fechas_corte_contenido": periods, "columnas_numericas": len(METRICS),
            "unidad": "CLP", "lineas": len(records),
            "catalogo_encontradas": sum(r["catalogo_estado"] == "encontrada" for r in records),
            "fuera_plan_municipal": sum(r["catalogo_estado"] != "encontrada" for r in records),
            "jerarquia_calzan": sum(h["resultado"] == "calza" for h in doc_h), "controles_jerarquia": len(doc_h),
            "totales_calzan": sum(t["resultado"] == "calza" for t in doc_t), "controles_totales": len(doc_t),
            "aritmetica_calza": sum(r["control_aritmetico_saldo"] == "calza" for r in records),
            "controles_aritmeticos_adicionales_calzan": sum(r["controles_aritmeticos_adicionales_calzan"] for r in all_lines if r["muestra_id"] == sample["id"]),
            "controles_aritmeticos_adicionales": sum(r["controles_aritmeticos_adicionales"] for r in all_lines if r["muestra_id"] == sample["id"]),
            "diferencias_jerarquia_por_magnitud_clp": dict(Counter(str(abs(h["diferencia"])) for h in doc_h if h["resultado"] == "no_calza")),
            "totales_impresos": totals["valores"],
        })
    write_csv("esp_muestras_parseado.csv", all_records)
    write_csv("esp_validacion_lineas.csv", all_lines)
    write_csv("esp_validacion_jerarquia.csv", all_hierarchy)
    write_csv("esp_validacion_totales.csv", all_totals)
    write_csv("esp_hallazgos_prevalidacion.csv", findings)
    result = {
        "alcance": "Prevalidación de dos archivos carpeta ESP; no autoriza escala ESP",
        "catalogo": {"archivo": "plan_municipal.json", "cuentas": len(plan), "rutas_unicas": len(plan)},
        "documentos": summaries,
        "hallazgos": len(findings),
    }
    (OUT / "resumen_prevalidacion_esp.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
