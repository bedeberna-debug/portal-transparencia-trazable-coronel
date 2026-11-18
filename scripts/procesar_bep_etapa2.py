from pathlib import Path
from collections import Counter
from datetime import datetime
import argparse
import csv
import hashlib
import json
import re
import sys

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria" / "Balance de Ejecución Presupuestaria"
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "bep_etapa2"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
sys.path.insert(0, str(ROOT / "scripts"))
from factibilidad_bep_etapa1 import parse_document, CONFIG

MONTHS = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
THRESHOLDS = {"totales": 1.0, "jerarquia": 0.95, "aritmetica": 0.99}

def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def ratio(ok, total):
    return ok / total if total else 0.0

def pct(value):
    return f"{100 * value:.1f} %".replace(".", ",")

def process_file(path, year, catalog):
    name = path.name
    tipo = "gastos" if "gasto" in name.lower() else "ingresos"
    version = "republicacion_v2" if "v2" in path.stem.lower() else "original"
    expected_month = next((num for token, num in MONTHS.items() if re.search(rf"\b{token}\b", path.stem.lower())), None)
    sample = {"id": f"PRE_{year}_{tipo}_{version}_{path.stem}", "tipo": tipo, "anio": year, "path": path}
    cfg = CONFIG[tipo]
    records, totals, forms, periods, sha256 = parse_document(sample, allow_continuation_pages=version == "republicacion_v2")
    own_forms, own_periods = list(forms), list(periods)
    period_source = "contenido"
    companion_sha256 = ""
    companion_equal = None
    if version == "republicacion_v2" and not periods:
        companion_path = path.with_name(path.stem[:-2] + path.suffix)
        if not companion_path.exists():
            raise ValueError("Republicación sin metadatos de corte y sin original asociado")
        companion_sample = {"id": f"ORIGINAL_ASOCIADO_{path.stem}", "tipo": tipo, "anio": year, "path": companion_path}
        companion_records, companion_totals, companion_forms, companion_periods, companion_sha256 = parse_document(companion_sample)
        if len(companion_periods) != 1:
            raise ValueError(f"Corte del original asociado no único: {companion_periods}")
        periods = companion_periods
        if not forms:
            forms = companion_forms
        period_source = "documento_original_asociado"
        signature_fields = ["codigo_cuenta_pdf", "nivel_jerarquico", "denominacion_pdf"] + cfg["metrics"]
        companion_equal = (
            [{k: r[k] for k in signature_fields} for r in records]
            == [{k: r[k] for k in signature_fields} for r in companion_records]
            and totals["valores"] == companion_totals["valores"]
        )
    if len(periods) != 1:
        raise ValueError(f"Corte de contenido no único: {periods}")
    cutoff = datetime.strptime(periods[0], "%d/%m/%Y")
    if cutoff.year != year:
        raise ValueError(f"Año de contenido {cutoff.year} distinto de carpeta {year}")
    period = cutoff.strftime("%Y-%m")
    document_id = f"BEP_{period}_{tipo.upper()}_{version.upper()}"
    if expected_month is not None and cutoff.month != expected_month:
        period_mismatch = f"nombre_mes_{expected_month:02d}_contenido_{cutoff.month:02d}"
    else:
        period_mismatch = ""
    if len({r["codigo_cuenta_pdf"] for r in records}) != len(records):
        raise ValueError("Códigos duplicados dentro del documento")
    lines, hierarchy, total_checks, findings = [], [], [], []
    if period_source != "contenido":
        findings.append({
            "hallazgo_tipo": "versionado", "subtipo": "metadatos_ausentes_periodo_asignado_desde_original",
            "severidad": "pendiente_documental", "documento_id": document_id,
            "fuente_archivo": name, "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_sha256": sha256,
            "documento_original_sha256": companion_sha256,
            "contenido_tabular_identico_original": companion_equal,
            "decision": "conservar_version_separada_y_declarar_asociacion",
        })
    for rec in records:
        code = rec["codigo_cuenta_pdf"]
        level = rec["nivel_jerarquico"]
        rec["periodo"] = period
        rec["anio"] = cutoff.year
        rec["mes_numero"] = cutoff.month
        rec["fecha_corte"] = cutoff.strftime("%Y-%m-%d")
        rec["documento_id"] = document_id
        rec["version_fuente"] = version
        rec["registro_id"] = f"BEP|{sha256}|p{rec['fuente_pagina']}|l{rec['fuente_linea']}|{code}"
        if code in catalog:
            status = "encontrada"
        elif level > 3:
            status = "fuera_catalogo_nivel_detalle_no_representado"
        else:
            status = "fuera_catalogo_mismo_nivel"
        rec["catalogo_estado"] = status
        rec["catalogo_denominacion"] = catalog.get(code, {}).get("DENOMINACIÓN", "")
        diff = rec[cfg["metrics"][3]] - (rec[cfg["metrics"][1]] - rec[cfg["metrics"][2]])
        rec["control_aritmetico_saldo"] = "calza" if diff == 0 else "no_calza"
        rec["control_aritmetico_diferencia"] = diff
        line = {
            "documento_id": document_id, "periodo": period, "tipo": tipo, "version_fuente": version,
            "codigo_cuenta_pdf": code, "nivel_jerarquico": level, "denominacion_pdf": rec["denominacion_pdf"],
            "catalogo_estado": status, "control_aritmetico_saldo": rec["control_aritmetico_saldo"],
            "diferencia_aritmetica": diff, "fuente_archivo": name,
            "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_pagina": rec["fuente_pagina"],
            "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
        }
        lines.append(line)
        if status != "encontrada":
            findings.append({
                "hallazgo_tipo": "catalogo", "subtipo": status, "severidad": "informativo" if level > 3 else "pendiente_normativo",
                "documento_id": document_id, "codigo_cuenta_pdf": code, "denominacion_pdf": rec["denominacion_pdf"],
                "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
                "decision": "conservar_codigo_pdf_sin_remapear",
            })
        if diff != 0:
            findings.append({
                "hallazgo_tipo": "aritmetica", "subtipo": "saldo_no_igual_vigente_menos_ejecutado",
                "severidad": "control", "documento_id": document_id, "codigo_cuenta_pdf": code,
                "denominacion_pdf": rec["denominacion_pdf"], "diferencia": diff,
                "fuente_pagina": rec["fuente_pagina"], "fuente_linea": rec["fuente_linea"], "fuente_sha256": sha256,
                "decision": "conservar_valores_impresos",
            })
    for parent in records:
        code, level = parent["codigo_cuenta_pdf"], parent["nivel_jerarquico"]
        children = [r for r in records if r["nivel_jerarquico"] == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
        for metric in cfg["metrics"] if children else []:
            expected = sum(c[metric] for c in children)
            printed = parent[metric]
            diff = printed - expected
            check = {
                "documento_id": document_id, "periodo": period, "tipo": tipo, "version_fuente": version,
                "codigo_padre": code, "denominacion_padre": parent["denominacion_pdf"], "nivel_padre": level,
                "metrica": metric, "valor_padre": printed, "suma_hijas_directas": expected, "diferencia": diff,
                "resultado": "calza" if diff == 0 else "no_calza", "hijas_directas": len(children),
                "fuente_pagina": parent["fuente_pagina"], "fuente_linea": parent["fuente_linea"], "fuente_sha256": sha256,
            }
            hierarchy.append(check)
            if diff != 0:
                findings.append({
                    "hallazgo_tipo": "jerarquia", "subtipo": "padre_distinto_suma_hijas_directas",
                    "severidad": "control", "documento_id": document_id, "codigo_cuenta_pdf": code,
                    "denominacion_pdf": parent["denominacion_pdf"], "metrica": metric, "valor_padre": printed,
                    "suma_hijas": expected, "diferencia": diff, "fuente_pagina": parent["fuente_pagina"],
                    "fuente_linea": parent["fuente_linea"], "fuente_sha256": sha256,
                    "decision": "conservar_valores_impresos",
                })
    top = [r for r in records if r["nivel_jerarquico"] == 1]
    for metric in cfg["metrics"]:
        summed = sum(r[metric] for r in top)
        printed = totals["valores"][metric]
        check = {
            "documento_id": document_id, "periodo": period, "tipo": tipo, "version_fuente": version,
            "metrica": metric, "total_impreso": printed, "suma_subtitulos": summed,
            "diferencia": printed - summed, "resultado": "calza" if printed == summed else "no_calza",
            "fuente_pagina_totales": totals["pagina"], "fuente_linea_totales": totals["lineas"][0], "fuente_sha256": sha256,
        }
        total_checks.append(check)
        if printed != summed:
            findings.append({
                "hallazgo_tipo": "total_general", "subtipo": "total_impreso_distinto_suma_subtitulos",
                "severidad": "critico", "documento_id": document_id, "metrica": metric,
                "total_impreso": printed, "suma_subtitulos": summed, "diferencia": printed - summed,
                "fuente_pagina": totals["pagina"], "fuente_linea": totals["lineas"][0], "fuente_sha256": sha256,
                "decision": "cuarentena_documento",
            })
    if period_mismatch:
        findings.append({
            "hallazgo_tipo": "periodo", "subtipo": period_mismatch, "severidad": "control",
            "documento_id": document_id, "decision": "usar_periodo_del_contenido",
            "fuente_archivo": name, "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_sha256": sha256,
        })
    h_ok = sum(h["resultado"] == "calza" for h in hierarchy)
    t_ok = sum(t["resultado"] == "calza" for t in total_checks)
    a_ok = sum(r["control_aritmetico_saldo"] == "calza" for r in records)
    rates = {"totales": ratio(t_ok, len(total_checks)), "jerarquia": ratio(h_ok, len(hierarchy)), "aritmetica": ratio(a_ok, len(records))}
    reasons = [name for name, threshold in THRESHOLDS.items() if rates[name] < threshold]
    if companion_equal is False:
        reasons.append("republicacion_contenido_difiere_del_original")
    status = "cuarentena" if reasons else "aceptado"
    doc = {
        "documento_id": document_id, "anio": year, "periodo": period, "fecha_corte": cutoff.strftime("%Y-%m-%d"),
        "tipo": tipo, "version_fuente": version, "archivo": name, "ruta_relativa": str(path.relative_to(ROOT)),
        "sha256": sha256, "formularios": own_forms, "fechas_corte_contenido": own_periods,
        "formularios_asociados": forms, "periodo_fuente": period_source,
        "documento_original_asociado_sha256": companion_sha256,
        "contenido_tabular_identico_original": companion_equal,
        "estado": status, "motivos_cuarentena": reasons, "lineas": len(records),
        "catalogo_encontradas": sum(r["catalogo_estado"] == "encontrada" for r in records),
        "detalle_no_representado": sum(r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for r in records),
        "fuera_catalogo_mismo_nivel": sum(r["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for r in records),
        "jerarquia_calzan": h_ok, "controles_jerarquia": len(hierarchy), "tasa_jerarquia": rates["jerarquia"],
        "totales_calzan": t_ok, "controles_totales": len(total_checks), "tasa_totales": rates["totales"],
        "aritmetica_calza": a_ok, "tasa_aritmetica": rates["aritmetica"],
        "totales_impresos": totals["valores"], "sumas_subtitulos": {t["metrica"]: t["suma_subtitulos"] for t in total_checks},
    }
    for rec in records:
        rec["estado_documento"] = status
    for line in lines:
        line["estado_documento"] = status
    return {"doc": doc, "records": records, "lines": lines, "hierarchy": hierarchy, "totals": total_checks, "findings": findings}

def aggregate(docs, records, hierarchy, totals, accepted_only=False):
    selected = {d["documento_id"] for d in docs if d["estado"] == "aceptado"} if accepted_only else {d["documento_id"] for d in docs}
    r = [x for x in records if x["documento_id"] in selected]
    h = [x for x in hierarchy if x["documento_id"] in selected]
    t = [x for x in totals if x["documento_id"] in selected]
    h_ok = sum(x["resultado"] == "calza" for x in h)
    t_ok = sum(x["resultado"] == "calza" for x in t)
    a_ok = sum(x["control_aritmetico_saldo"] == "calza" for x in r)
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

def write_checkpoint(year, docs, summary):
    if year != 2023:
        return
    L = []
    a = L.append
    a("# CHECKPOINT BEP 2023 — ETAPA 2")
    a("")
    a("**Fecha:** 14 de noviembre de 2026  ")
    a("**Umbrales por archivo:** totales 100 %; jerarquía ≥95 %; aritmética ≥99 %.  ")
    a("**Regla:** archivo bajo umbral queda en cuarentena, se conserva en trabajo y no entra al canónico ni a deltas.")
    a("")
    accepted = summary["aceptados"]
    a(f"**Decisión del checkpoint:** {'continuar con BEP 2024–2025' if accepted['umbrales_calzan'] else 'detener la escala BEP'}. Los documentos aceptados cumplen los tres umbrales en agregado.")
    a("")
    a("| Cobertura | Documentos | Líneas | Totales | Jerarquía | Aritmética |")
    a("|---|---:|---:|---:|---:|---:|")
    for label, key in [("Todos los parseados", "todos"), ("Solo aceptados", "aceptados")]:
        s = summary[key]
        a(f"| {label} | {s['documentos']} | {s['lineas']} | {pct(s['tasa_totales'])} | {pct(s['tasa_jerarquia'])} | {pct(s['tasa_aritmetica'])} |")
    a("")
    a(f"Archivos inventariados: {summary['archivos_inventariados']}; aceptados: {summary['aceptados_conteo']}; cuarentena: {summary['cuarentenas_conteo']}. La versión original y la republicación v2 de enero de 2023 se conservan como documentos separados.")
    a("")
    a("| Documento | Líneas | Totales | Jerarquía | Aritmética | Estado / motivo |")
    a("|---|---:|---:|---:|---:|---|")
    for d in docs:
        if d["estado"] == "error_parseo":
            a(f"| {d['archivo']} | 0 | — | — | — | cuarentena: {d['error']} |")
        else:
            reason = ", ".join(d["motivos_cuarentena"]) or "—"
            a(f"| {d['documento_id']} | {d['lineas']} | {pct(d['tasa_totales'])} | {pct(d['tasa_jerarquia'])} | {pct(d['tasa_aritmetica'])} | {d['estado']} / {reason} |")
    a("")
    a("El catálogo se mantiene como control informativo: los códigos ausentes se registran sin remapear. Los detalles y totales por documento están en `trabajo/07_Información_Presupuestaria/bep_etapa2/2023/`.")
    (DOCS / "CHECKPOINT_BEP_2023_v1.md").write_text("\n".join(L) + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--anio", type=int, required=True, choices=[2023, 2024, 2025])
    args = parser.parse_args()
    year = args.anio
    out = WORK / str(year)
    out.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    catalog_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))
    catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
    paths = sorted((RAW / str(year)).glob("*.pdf"), key=lambda p: p.name.lower())
    docs, records, lines, hierarchy, totals, findings = [], [], [], [], [], []
    for path in paths:
        try:
            result = process_file(path, year, catalog)
            docs.append(result["doc"])
            records.extend(result["records"])
            lines.extend(result["lines"])
            hierarchy.extend(result["hierarchy"])
            totals.extend(result["totals"])
            findings.extend(result["findings"])
        except Exception as exc:
            docs.append({
                "documento_id": f"BEP_{year}_ERROR_{path.stem}", "anio": year, "archivo": path.name,
                "ruta_relativa": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "estado": "error_parseo", "error": str(exc), "motivos_cuarentena": ["error_parseo"],
            })
            findings.append({
                "hallazgo_tipo": "parseo", "subtipo": "error_parseo", "severidad": "critico",
                "documento_id": docs[-1]["documento_id"], "fuente_archivo": path.name,
                "fuente_ruta_relativa": str(path.relative_to(ROOT)), "fuente_sha256": docs[-1]["sha256"],
                "detalle": str(exc), "decision": "cuarentena_documento",
            })
    docs.sort(key=lambda d: (d.get("periodo", "9999"), d.get("tipo", ""), d.get("version_fuente", ""), d["archivo"]))
    all_summary = aggregate(docs, records, hierarchy, totals, accepted_only=False)
    accepted_summary = aggregate(docs, records, hierarchy, totals, accepted_only=True)
    summary = {
        "anio": year, "archivos_inventariados": len(paths),
        "aceptados_conteo": sum(d["estado"] == "aceptado" for d in docs),
        "cuarentenas_conteo": sum(d["estado"] != "aceptado" for d in docs),
        "todos": all_summary, "aceptados": accepted_summary,
        "continuar_siguiente_anio": accepted_summary["umbrales_calzan"] and accepted_summary["documentos"] > 0,
        "umbrales": THRESHOLDS, "hallazgos": len(findings),
    }
    write_csv(out / f"bep_{year}_parseado.csv", records)
    write_csv(out / f"bep_{year}_validacion_lineas.csv", lines)
    write_csv(out / f"bep_{year}_validacion_jerarquia.csv", hierarchy)
    write_csv(out / f"bep_{year}_validacion_totales.csv", totals)
    write_csv(out / f"bep_{year}_documentos.csv", docs)
    write_csv(out / f"bep_{year}_hallazgos.csv", findings)
    (out / f"resumen_bep_{year}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / f"documentos_bep_{year}.json").write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
    write_checkpoint(year, docs, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
