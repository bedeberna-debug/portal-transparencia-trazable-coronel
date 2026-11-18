from pathlib import Path
from collections import Counter
from datetime import datetime
import csv
import hashlib
import json
import re

import pdfplumber

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria" / "Estado de Situación Financiera"
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "esp_etapa2"
WORK.mkdir(parents=True, exist_ok=True)
YEARS = [2023, 2024, 2025]
MONTHS = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
THRESHOLDS = {"totales": 1.0, "jerarquia": 0.95, "aritmetica": 0.99}
CONFIG = {
    "gastos": {
        "metrics": [
            "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
            "presupuesto_vigente_mes_clp", "obligacion_clp", "obligacion_devengada_clp", "pago_clp",
            "deuda_exigible_clp", "saldo_por_comprometer_clp", "saldo_por_devengar_clp", "saldo_por_pagar_clp",
        ],
        "anchors": [286, 334, 388, 436, 484, 532, 580, 628, 676, 724, 772],
        "numeric_x0": 230, "code_x1": 90, "denom_x0": 140, "denom_x1": 240,
        "total_token": "ACREEDORES", "title": "ESTADO PRESUPUESTARIO DE GASTOS",
        "primary": "saldo_por_comprometer_clp",
    },
    "ingresos": {
        "metrics": [
            "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
            "presupuesto_vigente_mes_clp", "ingreso_devengado_clp", "ingreso_percibido_clp",
            "ingreso_por_percibir_clp", "saldo_por_devengar_clp", "saldo_por_percibir_clp",
        ],
        "anchors": [369, 423, 476, 525, 581, 639, 695, 755, 806],
        "numeric_x0": 300, "code_x1": 140, "denom_x0": 190, "denom_x1": 320,
        "total_token": "DEUDORES", "title": "ESTADO PRESUPUESTARIO DE INGRESOS",
        "primary": "saldo_por_percibir_clp",
    },
}
ALL_METRICS = list(dict.fromkeys(CONFIG["gastos"]["metrics"] + CONFIG["ingresos"]["metrics"]))
NUM_RE = re.compile(r"^-?(?:\d+|\d{1,3}(?:\.\d{3})+)$")
CODE_RE = re.compile(r"^\d{2}(?:\.\d{2,3})+$|^\d{2}$")


def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


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


def compact(text):
    return re.sub(r"\s+", "", text).upper()


def numeric_columns(line, cfg):
    values, raw = {}, {}
    for word in line:
        token = word["text"]
        if word["x0"] < cfg["numeric_x0"] or not NUM_RE.fullmatch(token):
            continue
        idx = min(range(len(cfg["anchors"])), key=lambda i: abs(word["x1"] - cfg["anchors"][i]))
        if abs(word["x1"] - cfg["anchors"][idx]) <= 5:
            if idx in values:
                raise ValueError(f"Columna numérica duplicada: {token}")
            values[idx] = money(token)
            raw[idx] = token
    return values, raw


def arithmetic_identities(rec, tipo):
    if tipo == "gastos":
        return {
            "vigente_igual_inicial_mas_modificacion": rec["presupuesto_vigente_clp"] - rec["presupuesto_inicial_clp"] - rec["modificacion_presupuestaria_clp"],
            "exigible_igual_devengado_menos_pago": rec["deuda_exigible_clp"] - rec["obligacion_devengada_clp"] + rec["pago_clp"],
            "saldo_comprometer": rec["saldo_por_comprometer_clp"] - rec["presupuesto_vigente_mes_clp"] + rec["obligacion_clp"],
            "saldo_devengar": rec["saldo_por_devengar_clp"] - rec["obligacion_clp"] + rec["obligacion_devengada_clp"],
            "saldo_por_pagar": rec["saldo_por_pagar_clp"] - rec["obligacion_clp"] + rec["pago_clp"],
        }
    return {
        "vigente_igual_inicial_mas_modificacion": rec["presupuesto_vigente_clp"] - rec["presupuesto_inicial_clp"] - rec["modificacion_presupuestaria_clp"],
        "por_percibir_igual_devengado_menos_percibido": rec["ingreso_por_percibir_clp"] - rec["ingreso_devengado_clp"] + rec["ingreso_percibido_clp"],
        "saldo_devengar": rec["saldo_por_devengar_clp"] - rec["presupuesto_vigente_mes_clp"] + rec["ingreso_devengado_clp"],
        "saldo_por_percibir": rec["saldo_por_percibir_clp"] - rec["presupuesto_vigente_mes_clp"] + rec["ingreso_percibido_clp"],
    }


def parse_document(path, year, tipo, catalog):
    cfg = CONFIG[tipo]
    metrics = cfg["metrics"]
    digest = sha256(path)
    expected_month = next((num for token, num in MONTHS.items() if re.search(rf"\b{token}\b", path.stem.lower())), None)
    records, totals, periods, titles, title_evidence = [], None, set(), set(), []
    last_record = None
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, 1):
            words = page.extract_words(x_tolerance=1, y_tolerance=2)
            lines = group_lines(words)
            for line_no, line in enumerate(lines, 1):
                raw_line = " ".join(w["text"] for w in line)
                normalized = compact(raw_line)
                if compact(cfg["title"]) in normalized:
                    titles.add(cfg["title"])
                    found_dates = re.findall(r"\d{2}/\d{2}/\d{4}", raw_line)
                    periods.update(found_dates)
                    title_evidence.append({
                        "tipo_documental_contenido": cfg["title"], "titulo_literal_raw": raw_line,
                        "fuente_archivo": path.name, "fuente_ruta_relativa": str(path.relative_to(ROOT)),
                        "fuente_pagina": page_no, "fuente_linea": line_no, "fuente_sha256": digest,
                    })
            header_lines = [i for i, line in enumerate(lines, 1) if any(w["text"] == "Cuenta" for w in line) and any(w["text"] == "Denominación" for w in line)]
            if len(header_lines) != 1:
                raise ValueError(f"Encabezado no único: {path.name} p.{page_no}; encontrados={len(header_lines)}")
            for line_no, line in enumerate(lines, 1):
                if line_no <= header_lines[0]:
                    continue
                values, raw_values = numeric_columns(line, cfg)
                raw_line = " ".join(w["text"] for w in line)
                if len(values) == len(metrics):
                    if any(w["text"] == cfg["total_token"] for w in line):
                        if totals is not None:
                            raise ValueError(f"Total {cfg['total_token']} duplicado: {path.name}")
                        totals = {
                            "pagina": page_no, "linea": line_no,
                            "valores": {metrics[i]: values[i] for i in range(len(metrics))},
                            "valores_raw": {metrics[i]: raw_values[i] for i in range(len(metrics))},
                            "texto_raw": raw_line,
                        }
                        last_record = None
                        continue
                    codes = [w["text"] for w in line if w["x0"] < cfg["code_x1"] and CODE_RE.fullmatch(w["text"])]
                    if len(codes) != 1:
                        raise ValueError(f"Línea con {len(metrics)} montos sin código único: {path.name} p.{page_no} l.{line_no}: {raw_line}")
                    code = codes[0]
                    rec = {
                        "tipo": tipo, "codigo_cuenta_pdf": code, "nivel_jerarquico": len(code.split(".")),
                        "denominacion_pdf": " ".join(w["text"] for w in line if cfg["denom_x0"] <= w["x0"] < cfg["denom_x1"]),
                        "fuente_archivo": path.name, "fuente_ruta_relativa": str(path.relative_to(ROOT)),
                        "fuente_pagina": page_no, "fuente_linea": line_no, "fuente_sha256": digest,
                        "texto_linea_raw": raw_line,
                    }
                    for i, metric in enumerate(metrics):
                        rec[metric] = values[i]
                        rec[metric + "_raw"] = raw_values[i]
                    records.append(rec)
                    last_record = rec
                elif values:
                    raise ValueError(f"Línea con columnas incompletas: {path.name} p.{page_no} l.{line_no}: {raw_line}; columnas={sorted(values)}")
                elif last_record is not None:
                    continuation = " ".join(w["text"] for w in line if cfg["denom_x0"] <= w["x0"] < cfg["denom_x1"])
                    if continuation and not any(k in continuation for k in ["PRESUPUESTO", "Vigente", "Saldo"]):
                        last_record["denominacion_pdf"] = (last_record["denominacion_pdf"] + " " + continuation).strip()
    if totals is None:
        raise ValueError(f"Sin total {cfg['total_token']}: {path.name}")
    if len(periods) != 1:
        raise ValueError(f"Corte de contenido no único: {path.name}; {sorted(periods)}")
    if titles != {cfg["title"]}:
        raise ValueError(f"Título documental inesperado: {path.name}; {sorted(titles)}")
    cutoff = datetime.strptime(next(iter(periods)), "%d/%m/%Y")
    if cutoff.year != year:
        raise ValueError(f"Año de contenido {cutoff.year} distinto de carpeta {year}: {path.name}")
    period = cutoff.strftime("%Y-%m")
    document_id = f"ESP_{period}_{tipo.upper()}_ORIGINAL"
    if len({r["codigo_cuenta_pdf"] for r in records}) != len(records):
        raise ValueError(f"Códigos duplicados: {path.name}")

    lines_out, hierarchy, total_checks, findings = [], [], [], []
    period_mismatch = ""
    if expected_month is not None and cutoff.month != expected_month:
        period_mismatch = f"nombre_mes_{expected_month:02d}_contenido_{cutoff.month:02d}"
        findings.append({
            "hallazgo_tipo": "periodo", "subtipo": period_mismatch, "severidad": "control",
            "documento_id": document_id, "decision": "usar_periodo_del_contenido",
            "fuente_archivo": path.name, "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_sha256": digest,
        })
    findings.append({
        "hallazgo_tipo": "variante_documental", "subtipo": "esp_es_estado_presupuestario_no_financiero",
        "severidad": "informativo", "documento_id": document_id, "tipo": tipo, "periodo": period,
        "detalle": cfg["title"], "decision": "conservar_como_tipo_documental_separado_estado_presupuestario",
        **title_evidence[0],
    })
    for rec in records:
        code, level = rec["codigo_cuenta_pdf"], rec["nivel_jerarquico"]
        rec.update({
            "periodo": period, "anio": cutoff.year, "mes_numero": cutoff.month, "fecha_corte": cutoff.strftime("%Y-%m-%d"),
            "documento_id": document_id, "version_fuente": "original",
            "registro_id": f"ESP|{digest}|p{rec['fuente_pagina']}|l{rec['fuente_linea']}|{code}",
        })
        if code in catalog:
            status = "encontrada"
        elif level > 3:
            status = "fuera_catalogo_nivel_detalle_no_representado"
        else:
            status = "fuera_catalogo_mismo_nivel"
        rec["catalogo_estado"] = status
        rec["catalogo_denominacion"] = catalog.get(code, {}).get("DENOMINACIÓN", "")
        identities = arithmetic_identities(rec, tipo)
        primary_name = "saldo_comprometer" if tipo == "gastos" else "saldo_por_percibir"
        diff = identities[primary_name]
        rec["control_aritmetico_principal"] = "calza" if diff == 0 else "no_calza"
        rec["control_aritmetico_diferencia"] = diff
        rec["identidad_aritmetica_principal"] = primary_name
        for name, difference in identities.items():
            rec[f"control_{name}"] = "calza" if difference == 0 else "no_calza"
            rec[f"diferencia_{name}"] = difference
        line = {
            "documento_id": document_id, "periodo": period, "tipo": tipo,
            "codigo_cuenta_pdf": code, "nivel_jerarquico": level, "denominacion_pdf": rec["denominacion_pdf"],
            "catalogo_estado": status, "control_aritmetico_principal": rec["control_aritmetico_principal"],
            "diferencia_aritmetica": diff, "controles_aritmeticos_adicionales_calzan": sum(v == 0 for v in identities.values()),
            "controles_aritmeticos_adicionales": len(identities), "fuente_archivo": path.name,
            "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_pagina": rec["fuente_pagina"],
            "fuente_linea": rec["fuente_linea"], "fuente_sha256": digest,
        }
        lines_out.append(line)
        if status != "encontrada":
            findings.append({
                "hallazgo_tipo": "catalogo", "subtipo": status,
                "severidad": "informativo" if level > 3 else "pendiente_normativo",
                "documento_id": document_id, "periodo": period, "tipo": tipo,
                "codigo_cuenta_pdf": code, "denominacion_pdf": rec["denominacion_pdf"],
                "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": digest,
                "decision": "conservar_codigo_pdf_sin_remapear",
            })
        if diff != 0:
            findings.append({
                "hallazgo_tipo": "aritmetica", "subtipo": primary_name + "_no_calza", "severidad": "control",
                "documento_id": document_id, "periodo": period, "tipo": tipo, "codigo_cuenta_pdf": code,
                "denominacion_pdf": rec["denominacion_pdf"], "diferencia": diff,
                "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": digest,
                "decision": "conservar_valores_impresos",
            })
        for name, difference in identities.items():
            if name != primary_name and difference != 0:
                findings.append({
                    "hallazgo_tipo": "aritmetica_adicional", "subtipo": name + "_no_calza", "severidad": "informativo",
                    "documento_id": document_id, "periodo": period, "tipo": tipo, "codigo_cuenta_pdf": code,
                    "denominacion_pdf": rec["denominacion_pdf"], "diferencia": difference,
                    "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": digest,
                    "decision": "conservar_valores_impresos_y_documentar_identidad",
                })
    for parent in records:
        code, level = parent["codigo_cuenta_pdf"], parent["nivel_jerarquico"]
        children = [r for r in records if r["nivel_jerarquico"] == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
        for metric in metrics if children else []:
            expected = sum(c[metric] for c in children)
            printed = parent[metric]
            diff = printed - expected
            check = {
                "documento_id": document_id, "periodo": period, "tipo": tipo,
                "codigo_padre": code, "denominacion_padre": parent["denominacion_pdf"], "nivel_padre": level,
                "metrica": metric, "valor_padre": printed, "suma_hijas_directas": expected, "diferencia": diff,
                "resultado": "calza" if diff == 0 else "no_calza", "hijas_directas": len(children),
                "fuente_pagina": parent["fuente_pagina"], "fuente_linea": parent["fuente_linea"], "fuente_sha256": digest,
            }
            hierarchy.append(check)
            if diff != 0:
                findings.append({
                    "hallazgo_tipo": "jerarquia", "subtipo": "padre_distinto_suma_hijas_directas", "severidad": "control",
                    "documento_id": document_id, "periodo": period, "tipo": tipo, "codigo_cuenta_pdf": code,
                    "denominacion_pdf": parent["denominacion_pdf"], "metrica": metric, "valor_padre": printed,
                    "suma_hijas": expected, "diferencia": diff, "fuente_pagina": parent["fuente_pagina"],
                    "fuente_linea": parent["fuente_linea"], "fuente_sha256": digest, "decision": "conservar_valores_impresos",
                })
    top = [r for r in records if r["nivel_jerarquico"] == 1]
    for metric in metrics:
        summed = sum(r[metric] for r in top)
        printed = totals["valores"][metric]
        check = {
            "documento_id": document_id, "periodo": period, "tipo": tipo, "metrica": metric,
            "total_impreso": printed, "suma_subtitulos": summed, "diferencia": printed - summed,
            "resultado": "calza" if printed == summed else "no_calza",
            "fuente_pagina_totales": totals["pagina"], "fuente_linea_totales": totals["linea"], "fuente_sha256": digest,
        }
        total_checks.append(check)
        if printed != summed:
            findings.append({
                "hallazgo_tipo": "total_general", "subtipo": "total_impreso_distinto_suma_subtitulos", "severidad": "critico",
                "documento_id": document_id, "periodo": period, "tipo": tipo, "metrica": metric,
                "total_impreso": printed, "suma_subtitulos": summed, "diferencia": printed - summed,
                "fuente_pagina": totals["pagina"], "fuente_linea": totals["linea"], "fuente_sha256": digest,
                "decision": "cuarentena_documento",
            })
    h_ok = sum(h["resultado"] == "calza" for h in hierarchy)
    t_ok = sum(t["resultado"] == "calza" for t in total_checks)
    a_ok = sum(r["control_aritmetico_principal"] == "calza" for r in records)
    rates = {
        "totales": t_ok / len(total_checks) if total_checks else 0,
        "jerarquia": h_ok / len(hierarchy) if hierarchy else 0,
        "aritmetica": a_ok / len(records) if records else 0,
    }
    reasons = [name for name, threshold in THRESHOLDS.items() if rates[name] < threshold]
    status = "cuarentena" if reasons else "aceptado"
    doc = {
        "documento_id": document_id, "anio": year, "periodo": period, "fecha_corte": cutoff.strftime("%Y-%m-%d"),
        "tipo": tipo, "version_fuente": "original", "archivo": path.name, "ruta_relativa": str(path.relative_to(ROOT)),
        "sha256": digest, "tipo_documental": cfg["title"], "titulo_evidencias": title_evidence,
        "periodo_fuente": "contenido", "columnas_numericas": len(metrics), "unidad_monetaria": "CLP",
        "estado": status, "motivos_cuarentena": reasons, "lineas": len(records),
        "catalogo_encontradas": sum(r["catalogo_estado"] == "encontrada" for r in records),
        "detalle_no_representado": sum(r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for r in records),
        "fuera_catalogo_mismo_nivel": sum(r["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for r in records),
        "jerarquia_calzan": h_ok, "controles_jerarquia": len(hierarchy), "tasa_jerarquia": rates["jerarquia"],
        "totales_calzan": t_ok, "controles_totales": len(total_checks), "tasa_totales": rates["totales"],
        "aritmetica_calza": a_ok, "tasa_aritmetica": rates["aritmetica"],
        "controles_aritmeticos_adicionales_calzan": sum(r[f"control_{name}"] == "calza" for r in records for name in arithmetic_identities(r, tipo)),
        "controles_aritmeticos_adicionales": len(records) * len(arithmetic_identities(records[0], tipo)) if records else 0,
        "diferencias_jerarquia_por_magnitud_clp": dict(Counter(str(abs(h["diferencia"])) for h in hierarchy if h["resultado"] == "no_calza")),
        "totales_impresos": totals["valores"], "sumas_subtitulos": {t["metrica"]: t["suma_subtitulos"] for t in total_checks},
    }
    for rec in records:
        rec["estado_documento"] = status
    for line in lines_out:
        line["estado_documento"] = status
    return {"doc": doc, "records": records, "lines": lines_out, "hierarchy": hierarchy, "totals": total_checks, "findings": findings}


def ratio(ok, total):
    return ok / total if total else 0.0


def aggregate(docs, records, hierarchy, totals, accepted_only=False):
    selected = {d["documento_id"] for d in docs if d["estado"] == "aceptado"} if accepted_only else {d["documento_id"] for d in docs if d["estado"] != "error_parseo"}
    r = [x for x in records if x["documento_id"] in selected]
    h = [x for x in hierarchy if x["documento_id"] in selected]
    t = [x for x in totals if x["documento_id"] in selected]
    h_ok = sum(x["resultado"] == "calza" for x in h)
    t_ok = sum(x["resultado"] == "calza" for x in t)
    a_ok = sum(x["control_aritmetico_principal"] == "calza" for x in r)
    rates = {"totales": ratio(t_ok, len(t)), "jerarquia": ratio(h_ok, len(h)), "aritmetica": ratio(a_ok, len(r))}
    return {
        "documentos": len(selected), "lineas": len(r),
        "catalogo_encontradas": sum(x["catalogo_estado"] == "encontrada" for x in r),
        "detalle_no_representado": sum(x["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for x in r),
        "fuera_catalogo_mismo_nivel": sum(x["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for x in r),
        "jerarquia_calzan": h_ok, "controles_jerarquia": len(h), "tasa_jerarquia": rates["jerarquia"],
        "totales_calzan": t_ok, "controles_totales": len(t), "tasa_totales": rates["totales"],
        "aritmetica_calza": a_ok, "tasa_aritmetica": rates["aritmetica"],
        "umbrales_calzan": all(rates[k] >= v for k, v in THRESHOLDS.items()),
    }


def main():
    catalog_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))
    catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
    all_summaries = {}
    for year in YEARS:
        paths = sorted((RAW / str(year)).rglob("*.pdf"), key=lambda p: str(p.relative_to(ROOT)).lower())
        out = WORK / str(year)
        out.mkdir(parents=True, exist_ok=True)
        docs, records, lines, hierarchy, totals, findings = [], [], [], [], [], []
        for path in paths:
            tipo = "gastos" if "gasto" in path.name.lower() else "ingresos"
            print(f"Procesando {path.relative_to(ROOT)}", flush=True)
            try:
                result = parse_document(path, year, tipo, catalog)
                docs.append(result["doc"])
                for key, target in [("records", records), ("lines", lines), ("hierarchy", hierarchy), ("totals", totals), ("findings", findings)]:
                    target.extend(result[key])
            except Exception as exc:
                docs.append({
                    "documento_id": "", "anio": year, "periodo": "", "tipo": tipo, "version_fuente": "original",
                    "archivo": path.name, "ruta_relativa": str(path.relative_to(ROOT)), "sha256": sha256(path),
                    "estado": "error_parseo", "motivos_cuarentena": ["error_parseo"], "error": str(exc), "lineas": 0,
                })
                findings.append({
                    "hallazgo_tipo": "parseo", "subtipo": "error_estructural", "severidad": "critico",
                    "tipo": tipo, "detalle": str(exc), "decision": "cuarentena_documento",
                    "fuente_archivo": path.name, "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_sha256": sha256(path),
                })
        docs.sort(key=lambda d: (d.get("periodo", ""), d["tipo"], d["archivo"]))
        (out / f"documentos_esp_{year}.json").write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
        for name, rows in [("parseado", records), ("validacion_lineas", lines), ("validacion_jerarquia", hierarchy), ("validacion_totales", totals), ("hallazgos", findings)]:
            write_csv(out / f"esp_{year}_{name}.csv", rows)
        summary = {
            "archivos_inventariados": len(paths), "aceptados_conteo": sum(d["estado"] == "aceptado" for d in docs),
            "cuarentenas_conteo": sum(d["estado"] != "aceptado" for d in docs),
            "todos": aggregate(docs, records, hierarchy, totals),
            "aceptados": aggregate(docs, records, hierarchy, totals, accepted_only=True),
        }
        (out / f"resumen_esp_{year}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        all_summaries[str(year)] = summary
        print(json.dumps({str(year): summary}, ensure_ascii=False, indent=2), flush=True)
    all_docs = [json.loads((WORK / str(y) / f"documentos_esp_{y}.json").read_text(encoding="utf-8")) for y in YEARS]
    flat_docs = [d for year_docs in all_docs for d in year_docs]
    all_summaries["total"] = {
        "archivos_inventariados": len(flat_docs), "aceptados_conteo": sum(d["estado"] == "aceptado" for d in flat_docs),
        "cuarentenas_conteo": sum(d["estado"] != "aceptado" for d in flat_docs),
    }
    (WORK / "resumen_procesamiento_esp.json").write_text(json.dumps(all_summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(all_summaries["total"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
