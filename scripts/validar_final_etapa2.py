from pathlib import Path
from collections import Counter, defaultdict
import csv
import hashlib
import json
import re

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria"
BEP_WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "bep_etapa2"
ESP_WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "esp_etapa2"
OUT = ROOT / "datos procesados" / "07_Información_Presupuestaria"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
YEARS = [2023, 2024, 2025]
BEP_METRICS = {
    "gastos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp", "saldo_presupuestario_miles_clp", "deuda_exigible_miles_clp"],
    "ingresos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "ingresos_percibidos_miles_clp", "saldo_presupuestario_miles_clp", "ingresos_por_percibir_miles_clp"],
}
BEP_ALL_METRICS = list(dict.fromkeys(BEP_METRICS["gastos"] + BEP_METRICS["ingresos"]))
ESP_METRICS = {
    "gastos": [
        "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp", "presupuesto_vigente_mes_clp",
        "obligacion_clp", "obligacion_devengada_clp", "pago_clp", "deuda_exigible_clp", "saldo_por_comprometer_clp",
        "saldo_por_devengar_clp", "saldo_por_pagar_clp",
    ],
    "ingresos": [
        "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp", "presupuesto_vigente_mes_clp",
        "ingreso_devengado_clp", "ingreso_percibido_clp", "ingreso_por_percibir_clp", "saldo_por_devengar_clp", "saldo_por_percibir_clp",
    ],
}
ESP_ALL_METRICS = list(dict.fromkeys(ESP_METRICS["gastos"] + ESP_METRICS["ingresos"]))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def money_raw(value):
    return int(value.replace(".", "")) if value != "" else None


def pct(value):
    return f"{100 * value:.2f} %".replace(".", ",")


def prev_period(period):
    year, month = map(int, period.split("-"))
    return f"{year}-{month - 1:02d}" if month > 1 else None


def compact(text):
    return re.sub(r"\s+", "", text).upper()


hash_cache = {}
def verified_hash(path):
    key = str(path)
    if key not in hash_cache:
        hash_cache[key] = sha256(path) if path.exists() else ""
    return hash_cache[key]


checks = []
def check(name, ok, observed, expected=""):
    checks.append({"control": name, "resultado": "calza" if ok else "no_calza", "observado": observed, "esperado": expected})


# Fuentes y evidencias de trabajo.
bep_docs, bep_work_records, bep_work_totals = [], [], []
esp_docs, esp_work_records, esp_work_totals = [], [], []
for year in YEARS:
    bep_docs.extend(json.loads((BEP_WORK / str(year) / f"documentos_bep_{year}.json").read_text(encoding="utf-8")))
    bep_work_records.extend(read_csv(BEP_WORK / str(year) / f"bep_{year}_parseado.csv"))
    bep_work_totals.extend(read_csv(BEP_WORK / str(year) / f"bep_{year}_validacion_totales.csv"))
    esp_docs.extend(json.loads((ESP_WORK / str(year) / f"documentos_esp_{year}.json").read_text(encoding="utf-8")))
    esp_work_records.extend(read_csv(ESP_WORK / str(year) / f"esp_{year}_parseado.csv"))
    esp_work_totals.extend(read_csv(ESP_WORK / str(year) / f"esp_{year}_validacion_totales.csv"))
bep_doc_by_id = {d["documento_id"]: d for d in bep_docs if d["documento_id"]}
esp_doc_by_id = {d["documento_id"]: d for d in esp_docs if d["documento_id"]}
bep_accepted_ids = {d["documento_id"] for d in bep_docs if d["estado"] == "aceptado"}
esp_accepted_ids = {d["documento_id"] for d in esp_docs if d["estado"] == "aceptado"}
bep_work_by_record = {r["registro_id"]: r for r in bep_work_records}
esp_work_by_record = {r["registro_id"]: r for r in esp_work_records}

bep = read_csv(OUT / "BEP_2023-2025_canonico_v1.csv")
bep_doc_rows = read_csv(OUT / "BEP_2023-2025_documentos_v1.csv")
bep_coverage = read_csv(OUT / "BEP_2023-2025_cobertura_v1.csv")
deltas = read_csv(OUT / "BEP_2023-2025_serie_mensual_v1.csv")
esp = read_csv(OUT / "ESP_2023-2025_canonico_v1.csv")
esp_doc_rows = read_csv(OUT / "ESP_2023-2025_documentos_v1.csv")
esp_coverage = read_csv(OUT / "ESP_2023-2025_cobertura_v1.csv")
esp_d13 = read_csv(OUT / "ESP_2023-2025_controles_D13_v1.csv")
esp_totals = read_csv(OUT / "ESP_2023-2025_totales_ingresos_v1.csv")
esp_deltas = read_csv(OUT / "ESP_2023-2025_serie_mensual_ingresos_v1.csv")
esp_total_deltas = read_csv(OUT / "ESP_2023-2025_serie_totales_ingresos_v1.csv")
esp_delta_findings = read_csv(OUT / "ESP_2023-2025_hallazgos_delta_ingresos_v1.csv")
inventory = read_csv(DOCS / "INVENTARIO_FUENTES_v1.csv")
versioning = read_csv(DOCS / "COTEJO_VERSIONADO_CODIGOS_v1.csv")
esp_versioning = read_csv(DOCS / "COTEJO_VERSIONADO_CODIGOS_ESP_v1.csv")
findings = read_csv(DOCS / "REGISTRO_HALLAZGOS_v1.csv")
visual = read_csv(DOCS / "VERIFICACION_VISUAL_CUARENTENAS_v1.csv")
annex = read_csv(DOCS / "ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv")

bep_by_doc = defaultdict(list); esp_by_doc = defaultdict(list)
bep_by_record = {}; esp_by_record = {}
for r in bep:
    bep_by_doc[r["documento_id"]].append(r); bep_by_record[r["registro_id"]] = r
for r in esp:
    esp_by_doc[r["documento_id"]].append(r); esp_by_record[r["registro_id"]] = r

# Inventario físico, hashes y familias.
physical = list(RAW.rglob("*.pdf"))
check("inventario_cantidad_fisica", len(inventory) == len(physical) == 141, f"inventario={len(inventory)}; fisico={len(physical)}", 141)
check("inventario_familias", (sum(i["familia"] == "BEP" for i in inventory), sum(i["familia"] == "ESP" for i in inventory)) == (71, 70), f"BEP={sum(i['familia']=='BEP' for i in inventory)}; ESP={sum(i['familia']=='ESP' for i in inventory)}", "BEP=71; ESP=70")
hash_failures = [i["ruta_relativa"] for i in inventory if verified_hash(ROOT / i["ruta_relativa"]) != i["sha256"]]
check("hashes_inventario_completo", not hash_failures, f"{len(inventory)-len(hash_failures)}/{len(inventory)}", "141/141")
check("tablas_documentales_completas", len(bep_doc_rows) == 71 and len(esp_doc_rows) == 70, f"BEP={len(bep_doc_rows)}; ESP={len(esp_doc_rows)}", "BEP=71; ESP=70")

# Exportación, unicidad, raw y trazabilidad para ambas familias.
for family, rows, accepted, work_by_record, metrics, all_metrics in [
    ("BEP", bep, bep_accepted_ids, bep_work_by_record, BEP_METRICS, BEP_ALL_METRICS),
    ("ESP", esp, esp_accepted_ids, esp_work_by_record, ESP_METRICS, ESP_ALL_METRICS),
]:
    prefix = family.lower()
    check(prefix + "_canonico_solo_aceptados", {r["documento_id"] for r in rows} == accepted, len({r["documento_id"] for r in rows}), len(accepted))
    check(prefix + "_unicidad_registro_id", len({r["registro_id"] for r in rows}) == len(rows), len({r["registro_id"] for r in rows}), len(rows))
    check(prefix + "_unicidad_documento_cuenta", len({(r["documento_id"], r["codigo_cuenta_pdf"]) for r in rows}) == len(rows), len({(r["documento_id"], r["codigo_cuenta_pdf"]) for r in rows}), len(rows))
    trace_failures, raw_failures, export_failures, applicability_failures = [], [], [], []
    for r in rows:
        path = ROOT / r["fuente_ruta_relativa"]
        if not all([r["fuente_archivo"], r["fuente_ruta_relativa"], r["fuente_pagina"], r["fuente_linea"], re.fullmatch(r"[0-9a-f]{64}", r["fuente_sha256"])]):
            trace_failures.append(r["registro_id"])
        elif path.name != r["fuente_archivo"] or verified_hash(path) != r["fuente_sha256"]:
            trace_failures.append(r["registro_id"])
        for metric in all_metrics:
            value, raw = r[metric], r[metric + "_raw"]
            if (value == "") != (raw == ""):
                raw_failures.append(r["registro_id"] + "|" + metric)
            elif value != "" and money_raw(raw) != int(value):
                raw_failures.append(r["registro_id"] + "|" + metric)
        source = work_by_record.get(r["registro_id"])
        if source is None:
            export_failures.append(r["registro_id"])
        else:
            for field in ["documento_id", "periodo", "tipo", "codigo_cuenta_pdf", "denominacion_pdf", "fuente_archivo", "fuente_ruta_relativa", "fuente_pagina", "fuente_linea", "fuente_sha256", "texto_linea_raw"]:
                if r[field] != source[field]:
                    export_failures.append(r["registro_id"] + "|" + field)
            for metric in metrics[r["tipo"]]:
                if r[metric] != source[metric] or r[metric + "_raw"] != source[metric + "_raw"]:
                    export_failures.append(r["registro_id"] + "|" + metric)
        if {m for m in all_metrics if r[m] != ""} != set(metrics[r["tipo"]]):
            applicability_failures.append(r["registro_id"])
    check(prefix + "_trazabilidad_y_hash_por_registro", not trace_failures, f"{len(rows)-len(trace_failures)}/{len(rows)}", f"{len(rows)}/{len(rows)}")
    check(prefix + "_valores_raw_coinciden_numericos", not raw_failures, len(raw_failures), 0)
    check(prefix + "_exportacion_coincide_parseo", not export_failures, len(export_failures), 0)
    check(prefix + "_metricas_no_aplicables_nulas", not applicability_failures, len(applicability_failures), 0)

# Catálogo presupuestario para ambas familias, sin plan municipal ni remapeo.
catalog_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))
catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
for prefix, rows in [("bep", bep), ("esp", esp)]:
    failures = []
    for r in rows:
        code, level = r["codigo_cuenta_pdf"], int(r["nivel_jerarquico"])
        expected = "encontrada" if code in catalog else ("fuera_catalogo_nivel_detalle_no_representado" if level > 3 else "fuera_catalogo_mismo_nivel")
        if r["catalogo_estado"] != expected or r["catalogo_denominacion"] != catalog.get(code, {}).get("DENOMINACIÓN", ""):
            failures.append(r["registro_id"])
    check(prefix + "_cotejo_clasificador_presupuestario", not failures, len(failures), 0)

# Recálculo jerárquico y de totales, reutilizable con métricas y unidades distintas.
def hierarchy(rows, metrics):
    ok = total = 0
    differences = []
    for parent in rows:
        code, level = parent["codigo_cuenta_pdf"], int(parent["nivel_jerarquico"])
        children = [r for r in rows if int(r["nivel_jerarquico"]) == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
        for metric in metrics if children else []:
            expected = sum(int(c[metric]) for c in children)
            diff = int(parent[metric]) - expected
            total += 1
            ok += diff == 0
            if diff:
                differences.append({"codigo": code, "metrica": metric, "diferencia": diff})
    return ok, total, differences


def printed_totals(work_totals, did):
    return {t["metrica"]: int(t["total_impreso"]) for t in work_totals if t["documento_id"] == did}


bep_per_doc, bep_summary_parts = {}, {}
for did, rows in bep_by_doc.items():
    tipo = rows[0]["tipo"]
    h_ok, h_n, h_diffs = hierarchy(rows, BEP_METRICS[tipo])
    printed = printed_totals(bep_work_totals, did)
    top = [r for r in rows if int(r["nivel_jerarquico"]) == 1]
    t_ok = sum(printed[m] == sum(int(r[m]) for r in top) for m in BEP_METRICS[tipo])
    t_n = len(BEP_METRICS[tipo])
    executed = "obligacion_devengada_miles_clp" if tipo == "gastos" else "ingresos_percibidos_miles_clp"
    a_ok = sum(int(r["saldo_presupuestario_miles_clp"]) == int(r["presupuesto_vigente_miles_clp"]) - int(r[executed]) for r in rows)
    policy = bep_doc_by_id[did].get("politica_aceptacion", "umbral_inicial_totales_100_jerarquia_95_aritmetica_99")
    base_ok = t_ok == t_n and a_ok / len(rows) >= .99
    if policy == "refinada_tolerancia_jerarquia_2_miles_clp":
        accepted_rule = base_ok and tipo == "gastos" and all(abs(x["diferencia"]) <= 2 for x in h_diffs)
    else:
        accepted_rule = base_ok and h_ok / h_n >= .95
    bep_per_doc[did] = {
        "politica": policy, "totales": f"{t_ok}/{t_n}", "jerarquia": f"{h_ok}/{h_n}", "aritmetica": f"{a_ok}/{len(rows)}",
        "diferencias_jerarquia": len(h_diffs), "maxima_diferencia_abs_miles_clp": max([abs(x["diferencia"]) for x in h_diffs] or [0]),
        "criterio_aceptacion_calza": accepted_rule,
    }
    bep_summary_parts[did] = {"rows": rows, "h_ok": h_ok, "h_n": h_n, "t_ok": t_ok, "t_n": t_n, "a_ok": a_ok}
check("bep_politica_en_cada_documento", all(v["criterio_aceptacion_calza"] for v in bep_per_doc.values()), sum(v["criterio_aceptacion_calza"] for v in bep_per_doc.values()), len(bep_per_doc))
refined_ids = {did for did, d in bep_doc_by_id.items() if d.get("politica_aceptacion") == "refinada_tolerancia_jerarquia_2_miles_clp"}
check("bep_28_documentos_refinados", len(refined_ids) == 28 and refined_ids <= set(bep_by_doc), len(refined_ids), 28)
expected_quarantine = {"BEP_2023-08_GASTOS_ORIGINAL", "BEP_2023-09_GASTOS_ORIGINAL", "BEP_2023-11_GASTOS_ORIGINAL", "BEP_2024-02_GASTOS_ORIGINAL", "BEP_2023-01_INGRESOS_REPUBLICACION_V2"}
actual_quarantine = {d["documento_id"] for d in bep_docs if d["estado"] != "aceptado"}
check("bep_cinco_cuarentenas_exactas_y_excluidas", actual_quarantine == expected_quarantine and not (actual_quarantine & set(bep_by_doc)), "|".join(sorted(actual_quarantine)), "5 documentos esperados; 0 en canónico")
check("bep_anexo_975_diferencias", len(annex) == 975 and all(r["resultado"] == "no_calza" for r in annex), len(annex), 975)
check("bep_anexo_distribucion_magnitudes", Counter(int(r["magnitud_abs_miles_clp"]) for r in annex) == Counter({1: 921, 2: 45, 3: 4, 25308: 1, 881613: 1, 906921: 2, 2271862: 1}), dict(Counter(int(r["magnitud_abs_miles_clp"]) for r in annex)), "921x1;45x2;4x3;5 grandes v2")
check("bep_refinados_todas_diferencias_anexo_hasta_2", all(int(r["magnitud_abs_miles_clp"]) <= 2 for r in annex if r["documento_id"] in refined_ids), max([int(r["magnitud_abs_miles_clp"]) for r in annex if r["documento_id"] in refined_ids] or [0]), "<=2 M$")
check("bep_verificacion_visual_10_sobre_10", len(visual) == 10 and len({r["documento_id"] for r in visual}) == 10 and all(r["verificacion_visual"] == "confirmado" for r in visual), f"{sum(r['verificacion_visual']=='confirmado' for r in visual)}/{len(visual)}", "10/10")
visual_trace_failures = [r["muestra_visual_id"] for r in visual if verified_hash(ROOT / r["fuente_ruta_relativa"]) != r["fuente_sha256"] or not (ROOT / r["imagen_recorte"]).exists()]
check("bep_verificacion_visual_trazada", not visual_trace_failures, len(visual_trace_failures), 0)


def aggregate_bep(ids):
    parts = [bep_summary_parts[did] for did in ids]
    rows = [r for p in parts for r in p["rows"]]
    h_ok = sum(p["h_ok"] for p in parts); h_n = sum(p["h_n"] for p in parts)
    t_ok = sum(p["t_ok"] for p in parts); t_n = sum(p["t_n"] for p in parts)
    a_ok = sum(p["a_ok"] for p in parts)
    return {"documentos": len(parts), "lineas": len(rows), "catalogo_encontradas": sum(r["codigo_cuenta_pdf"] in catalog for r in rows),
            "catalogo_tasa_bruta": sum(r["codigo_cuenta_pdf"] in catalog for r in rows)/len(rows), "jerarquia_calzan": h_ok,
            "controles_jerarquia": h_n, "tasa_jerarquia": h_ok/h_n, "totales_calzan": t_ok, "controles_totales": t_n,
            "tasa_totales": t_ok/t_n, "aritmetica_calza": a_ok, "tasa_aritmetica": a_ok/len(rows)}


bep_aggregates = {str(y): aggregate_bep([did for did, rows in bep_by_doc.items() if int(rows[0]["anio"]) == y]) for y in YEARS}
bep_aggregates["total"] = aggregate_bep(list(bep_by_doc))
for label, a in bep_aggregates.items():
    check(f"bep_totales_y_aritmetica_agregados_{label}", a["tasa_totales"] == 1 and a["tasa_aritmetica"] >= .99,
          f"totales={pct(a['tasa_totales'])}; aritmetica={pct(a['tasa_aritmetica'])}; jerarquia_informativa={pct(a['tasa_jerarquia'])}", "totales=100 %; aritmetica>=99 %")

# ESP: gastos por umbrales estrictos; ingresos por las tres condiciones D-13, recalculadas por documento.
esp_per_doc, esp_summary_parts = {}, {}
d13_control_by_id = {r["documento_id"]: r for r in esp_d13}
d13_mismatches = []
for did, rows in esp_by_doc.items():
    tipo = rows[0]["tipo"]
    h_ok, h_n, h_diffs = hierarchy(rows, ESP_METRICS[tipo])
    printed = printed_totals(esp_work_totals, did)
    top = [r for r in rows if int(r["nivel_jerarquico"]) == 1]
    top_sums = {m: sum(int(r[m]) for r in top) for m in ESP_METRICS[tipo]}
    t_ok = sum(printed[m] == top_sums[m] for m in ESP_METRICS[tipo])
    t_n = len(ESP_METRICS[tipo])
    d13_conditions = None
    if tipo == "gastos":
        a_ok = sum(int(r["saldo_por_comprometer_clp"]) == int(r["presupuesto_vigente_mes_clp"]) - int(r["obligacion_clp"]) for r in rows)
        additional = [
            sum(int(r["presupuesto_vigente_clp"]) == int(r["presupuesto_inicial_clp"]) + int(r["modificacion_presupuestaria_clp"]) for r in rows),
            sum(int(r["deuda_exigible_clp"]) == int(r["obligacion_devengada_clp"]) - int(r["pago_clp"]) for r in rows),
            sum(int(r["saldo_por_comprometer_clp"]) == int(r["presupuesto_vigente_mes_clp"]) - int(r["obligacion_clp"]) for r in rows),
            sum(int(r["saldo_por_devengar_clp"]) == int(r["obligacion_clp"]) - int(r["obligacion_devengada_clp"]) for r in rows),
            sum(int(r["saldo_por_pagar_clp"]) == int(r["obligacion_clp"]) - int(r["pago_clp"]) for r in rows),
        ]
    else:
        a_ok = sum(int(r["saldo_por_percibir_clp"]) == int(r["presupuesto_vigente_mes_clp"]) - int(r["ingreso_percibido_clp"]) for r in rows)
        additional = [
            sum(int(r["presupuesto_vigente_clp"]) == int(r["presupuesto_inicial_clp"]) + int(r["modificacion_presupuestaria_clp"]) for r in rows),
            sum(int(r["ingreso_por_percibir_clp"]) == int(r["ingreso_devengado_clp"]) - int(r["ingreso_percibido_clp"]) for r in rows),
            sum(int(r["saldo_por_devengar_clp"]) == int(r["presupuesto_vigente_mes_clp"]) - int(r["ingreso_devengado_clp"]) for r in rows),
            sum(int(r["saldo_por_percibir_clp"]) == int(r["presupuesto_vigente_mes_clp"]) - int(r["ingreso_percibido_clp"]) for r in rows),
        ]
        c15 = [r for r in rows if r["codigo_cuenta_pdf"] == "15"]
        condition_1 = all(printed[m] == top_sums[m] for m in ESP_METRICS["ingresos"] if m != "saldo_por_percibir_clp")
        condition_2 = printed["saldo_por_percibir_clp"] == printed["presupuesto_vigente_mes_clp"] - printed["ingreso_percibido_clp"]
        condition_3 = len(c15) == 1 and printed["saldo_por_percibir_clp"] - top_sums["saldo_por_percibir_clp"] == int(c15[0]["presupuesto_vigente_mes_clp"]) - int(c15[0]["ingreso_percibido_clp"])
        d13_conditions = (condition_1, condition_2, condition_3)
        control = d13_control_by_id.get(did)
        expected_values = {
            "total_saldo_por_percibir_oficial_clp": printed["saldo_por_percibir_clp"],
            "saldo_por_percibir_suma_detalle_clp": top_sums["saldo_por_percibir_clp"],
            "diferencia_oficial_menos_detalle_clp": printed["saldo_por_percibir_clp"] - top_sums["saldo_por_percibir_clp"],
            "condicion_2_residual_clp": 0, "condicion_3_residual_clp": 0,
        }
        if control is None or any(int(control[k]) != v for k, v in expected_values.items()) or [control["condicion_1_otras_ocho_metricas"], control["condicion_2_identidad_total"], control["condicion_3_reconciliacion_cuenta_15"]] != ["calza", "calza", "calza"]:
            d13_mismatches.append(did)
    rates = {"totales": t_ok/t_n, "jerarquia": h_ok/h_n, "aritmetica": a_ok/len(rows)}
    if tipo == "gastos":
        rule = rates["totales"] == 1 and rates["jerarquia"] >= .95 and rates["aritmetica"] >= .99
        policy = "umbrales_estrictos"
    else:
        rule = all(d13_conditions) and esp_doc_by_id[did].get("politica_aceptacion") == "D-13_rehabilitacion_condicionada_cuenta_15"
        policy = "D-13"
    esp_per_doc[did] = {"totales_informativos": f"{t_ok}/{t_n}", "jerarquia_informativa": f"{h_ok}/{h_n}", "aritmetica_informativa": f"{a_ok}/{len(rows)}",
                        "identidades_adicionales": f"{sum(additional)}/{len(rows)*len(additional)}", "politica": policy,
                        "condiciones_d13": d13_conditions, "criterio_aceptacion_calza": rule}
    esp_summary_parts[did] = {"rows": rows, "h_ok": h_ok, "h_n": h_n, "t_ok": t_ok, "t_n": t_n, "a_ok": a_ok, "additional_ok": sum(additional), "additional_n": len(rows)*len(additional)}
check("esp_criterio_aceptacion_en_cada_documento", len(esp_per_doc) == 70 and all(v["criterio_aceptacion_calza"] for v in esp_per_doc.values()), sum(v["criterio_aceptacion_calza"] for v in esp_per_doc.values()), 70)
esp_income_docs = [d for d in esp_docs if d["tipo"] == "ingresos"]
check("esp_35_ingresos_rehabilitados_d13", len(esp_income_docs) == 35 and len(d13_control_by_id) == 35 and all(d["estado"] == "aceptado" and d.get("politica_aceptacion") == "D-13_rehabilitacion_condicionada_cuenta_15" for d in esp_income_docs), f"{sum(d['estado']=='aceptado' for d in esp_income_docs)}/35", "35/35 aceptados por D-13")
check("esp_controles_d13_coinciden_recalculo", not d13_mismatches, len(d13_mismatches), 0)
income_total_failures = [t for t in esp_work_totals if t["tipo"] == "ingresos" and t["resultado"] == "no_calza"]
check("esp_ingresos_diferencia_clasica_exclusiva_saldo_por_percibir", len(income_total_failures) == 35 and all(t["metrica"] == "saldo_por_percibir_clp" for t in income_total_failures), f"{len(income_total_failures)}; metricas={sorted({t['metrica'] for t in income_total_failures})}", "35 saldo_por_percibir_clp; control informativo")
check("esp_ingresos_otras_ocho_metricas_calzan", all(sum(t["resultado"] == "calza" for t in esp_work_totals if t["documento_id"] == d["documento_id"]) == 8 for d in esp_income_docs), "35 documentos con 8/9", "35 documentos con 8/9")

# Doble total, trazabilidad y preservación literal de la cuenta 15.
esp_total_by_id = {r["documento_id"]: r for r in esp_totals}
total_failures, total_trace_failures = [], []
for d in esp_income_docs:
    did = d["documento_id"]
    row = esp_total_by_id.get(did)
    if row is None:
        total_failures.append(did)
        continue
    official = d["totales_impresos"]["saldo_por_percibir_clp"]
    detail = d["sumas_subtitulos"]["saldo_por_percibir_clp"]
    if int(row["total_saldo_por_percibir_oficial_clp"]) != official or int(row["saldo_por_percibir_suma_detalle_clp"]) != detail or int(row["diferencia_oficial_menos_detalle_clp"]) != official - detail:
        total_failures.append(did)
    if verified_hash(ROOT / row["fuente_ruta_relativa"]) != row["fuente_sha256"] or not row["total_fuente_pagina"] or not row["total_fuente_linea"] or not row["cuenta_15_registro_id"]:
        total_trace_failures.append(did)
check("esp_doble_total_35_documentos", len(esp_totals) == 35 and not total_failures, f"filas={len(esp_totals)}; errores={len(total_failures)}", "35; ambos totales y diferencia exactos")
check("esp_doble_total_trazado", not total_trace_failures, len(total_trace_failures), 0)
account15 = [r for r in esp if r["tipo"] == "ingresos" and r["codigo_cuenta_pdf"] == "15"]
check("esp_cuenta_15_ceros_impresos_intactos", len(account15) == 35 and all(r["saldo_por_percibir_clp"] == "0" and money_raw(r["saldo_por_percibir_clp_raw"]) == 0 for r in account15), f"{len(account15)} líneas; ceros={sum(r['saldo_por_percibir_clp']=='0' for r in account15)}", "35 líneas; 35 ceros")
check("esp_politica_y_nota_en_canonico", all(r["estado_documento"] == "aceptado" and (r["tipo"] != "ingresos" or (r["politica_aceptacion"] == "D-13_rehabilitacion_condicionada_cuenta_15" and r["nota_metodologica"])) for r in esp), len(esp), len(esp))


def aggregate_esp(ids):
    parts = [esp_summary_parts[did] for did in ids]
    rows = [r for p in parts for r in p["rows"]]
    h_ok = sum(p["h_ok"] for p in parts); h_n = sum(p["h_n"] for p in parts)
    t_ok = sum(p["t_ok"] for p in parts); t_n = sum(p["t_n"] for p in parts)
    a_ok = sum(p["a_ok"] for p in parts)
    add_ok = sum(p["additional_ok"] for p in parts); add_n = sum(p["additional_n"] for p in parts)
    return {"documentos": len(parts), "lineas": len(rows), "catalogo_encontradas": sum(r["codigo_cuenta_pdf"] in catalog for r in rows),
            "catalogo_tasa_bruta": sum(r["codigo_cuenta_pdf"] in catalog for r in rows)/len(rows), "jerarquia_calzan": h_ok,
            "controles_jerarquia": h_n, "tasa_jerarquia": h_ok/h_n, "totales_calzan": t_ok, "controles_totales": t_n,
            "tasa_totales": t_ok/t_n, "aritmetica_calza": a_ok, "tasa_aritmetica": a_ok/len(rows),
            "identidades_adicionales_calzan": add_ok, "controles_identidades_adicionales": add_n, "tasa_identidades_adicionales": add_ok/add_n}


esp_aggregates = {str(y): aggregate_esp([did for did, rows in esp_by_doc.items() if int(rows[0]["anio"]) == y]) for y in YEARS}
esp_aggregates["total"] = aggregate_esp(list(esp_by_doc))
esp_gastos_ids = [did for did, rows in esp_by_doc.items() if rows[0]["tipo"] == "gastos"]
esp_ingresos_ids = [did for did, rows in esp_by_doc.items() if rows[0]["tipo"] == "ingresos"]
esp_gastos_aggregates = {str(y): aggregate_esp([did for did in esp_gastos_ids if int(esp_by_doc[did][0]["anio"]) == y]) for y in YEARS}
esp_gastos_aggregates["total"] = aggregate_esp(esp_gastos_ids)
esp_ingresos_aggregates = {"total": aggregate_esp(esp_ingresos_ids)}
for label, a in esp_gastos_aggregates.items():
    check(f"esp_gastos_tres_niveles_agregados_{label}", a["tasa_totales"] == 1 and a["tasa_jerarquia"] >= .95 and a["tasa_aritmetica"] >= .99,
          f"totales={pct(a['tasa_totales'])}; jerarquia={pct(a['tasa_jerarquia'])}; aritmetica={pct(a['tasa_aritmetica'])}", "100 %; >=95 %; >=99 %")

# Evidencia del tipo documental para los 70 ESP, no solo los aceptados.
title_failures = []
for d in esp_docs:
    expected = "ESTADO PRESUPUESTARIO DE " + d["tipo"].upper()
    evidence = d.get("titulo_evidencias") or []
    if d.get("tipo_documental") != expected or not evidence:
        title_failures.append(d.get("documento_id") or d["archivo"])
        continue
    for e in evidence:
        if compact(expected) not in compact(e["titulo_literal_raw"]) or e["fuente_sha256"] != d["sha256"] or not e["fuente_pagina"] or not e["fuente_linea"]:
            title_failures.append(d["documento_id"])
            break
check("esp_titulo_y_evidencia_70_documentos", not title_failures, f"{len(esp_docs)-len(title_failures)}/{len(esp_docs)}", "70/70")
title_findings = [f for f in findings if f.get("familia") == "ESP" and f.get("subtipo") == "esp_es_estado_presupuestario_no_financiero"]
check("esp_hallazgo_tipo_documental_70", len(title_findings) == 70 and all(f.get("titulo_literal_raw") for f in title_findings), len(title_findings), 70)
check("esp_11_columnas_gastos_9_ingresos", all(d["columnas_numericas"] == (11 if d["tipo"] == "gastos" else 9) and d["unidad_monetaria"] == "CLP" for d in esp_docs), "gastos=11; ingresos=9; CLP", "gastos=11; ingresos=9; CLP")

# Cobertura, ausencias y republicación.
check("cobertura_72_periodos_tipo_por_familia", len(bep_coverage) == len(esp_coverage) == 72 and len({(c["periodo"], c["tipo"]) for c in bep_coverage}) == len({(c["periodo"], c["tipo"]) for c in esp_coverage}) == 72, f"BEP={len(bep_coverage)}; ESP={len(esp_coverage)}", "72+72")
for prefix, coverage, canonical in [("bep", bep_coverage, bep), ("esp", esp_coverage, esp)]:
    july = [c for c in coverage if c["periodo"] == "2025-07"]
    check(prefix + "_julio_2025_ausencia_declarada", len(july) == 2 and all(c["estado_corte"] == "ausencia_declarada_no_publicado" for c in july), len(july), 2)
    check(prefix + "_julio_2025_sin_datos", not any(r["periodo"] == "2025-07" for r in canonical), 0, 0)
check("agosto_2025_sin_delta_saltando_julio", not any(d["periodo"] == "2025-08" for d in deltas), 0, 0)
v2_id = "BEP_2023-01_INGRESOS_REPUBLICACION_V2"; original_id = "BEP_2023-01_INGRESOS_ORIGINAL"
check("republicacion_ambas_versiones_inventariadas", {i["version_fuente"] for i in inventory if i["periodo_nombre_archivo"] == "2023-01" and i["familia"] == "BEP" and i["tipo"] == "ingresos"} == {"original", "republicacion_v2"}, "original+v2", "original+v2")
check("republicacion_v2_parseada_y_cuarentenada", v2_id in bep_doc_by_id and bep_doc_by_id[v2_id]["estado"] == "cuarentena" and bep_doc_by_id[v2_id]["lineas"] == 95 and v2_id not in bep_by_doc, bep_doc_by_id.get(v2_id, {}).get("estado"), "cuarentena; 95 líneas")
check("enero_2023_usa_original", original_id in bep_by_doc and all(r["seleccionado_para_serie"] == "si" for r in bep_by_doc[original_id]), original_id, original_id)

# Recalcular cada delta y su universo esperado.
delta_failures, delta_ids, actual_keys = [], set(), set()
for d in deltas:
    delta_ids.add(d["registro_derivado_id"])
    key = (d["periodo"], d["tipo"], d["codigo_cuenta_pdf"], d["metrica"])
    actual_keys.add(key)
    current = bep_by_record.get(d["registro_actual_id"])
    if current is None or current["documento_id"] not in bep_accepted_ids:
        delta_failures.append(d["registro_derivado_id"] + "|actual")
        continue
    month = int(d["mes_numero"])
    if month == 1:
        prior = None
        if d["metodo_base"] != "cero_inicio_anio_convencion" or d["registro_previo_id"] or d["valor_acumulado_previo_miles_clp"] != "":
            delta_failures.append(d["registro_derivado_id"] + "|base_enero")
    else:
        prior = bep_by_record.get(d["registro_previo_id"])
        if prior is None or prior["periodo"] != prev_period(d["periodo"]) or prior["documento_id"] not in bep_accepted_ids:
            delta_failures.append(d["registro_derivado_id"] + "|previo")
            continue
    metric = d["metrica"]
    actual = int(current[metric]); base = int(prior[metric]) if prior else 0; delta = actual - base
    if int(d["base_numerica_utilizada_miles_clp"]) != base or int(d["valor_acumulado_actual_miles_clp"]) != actual or int(d["delta_mensual_miles_clp"]) != delta or int(d["diferencia_control_miles_clp"]) != base + delta - actual or d["control_consistencia"] != "calza":
        delta_failures.append(d["registro_derivado_id"] + "|aritmetica")
check("unicidad_delta", len(delta_ids) == len(deltas) == 52200, len(delta_ids), 52200)
check("recalculo_delta_y_trazabilidad", not delta_failures, f"{len(deltas)-len(delta_failures)}/{len(deltas)}", "52200/52200")
selected = defaultdict(list)
for r in bep:
    if r["seleccionado_para_serie"] == "si":
        selected[(r["periodo"], r["tipo"])].append(r)
expected_keys = set()
for (period, tipo), rows in selected.items():
    month = int(period.split("-")[1]); previous = prev_period(period)
    previous_rows = {r["codigo_cuenta_pdf"]: r for r in selected.get((previous, tipo), [])} if previous else {}
    if month != 1 and not previous_rows:
        continue
    for r in rows:
        if month != 1 and r["codigo_cuenta_pdf"] not in previous_rows:
            continue
        for metric in BEP_METRICS[tipo]:
            expected_keys.add((period, tipo, r["codigo_cuenta_pdf"], metric))
check("cobertura_exacta_deltas", actual_keys == expected_keys, f"actual={len(actual_keys)}; faltantes={len(expected_keys-actual_keys)}; inesperados={len(actual_keys-expected_keys)}", f"esperado={len(expected_keys)}")
computable = sum(c["estado_delta_mensual"].startswith("computable") for c in bep_coverage)
not_computable = sum(c["estado_delta_mensual"].startswith("no_computable") for c in bep_coverage)
check("cobertura_cortes_delta", (computable, not_computable) == (61, 11), f"computables={computable}; no_computables={not_computable}", "61;11")

# Recálculo independiente de las series ESP de ingresos: cuentas y ambos ámbitos de totales.
income_by_period = {period: rows for period, rows in ((p, [r for r in esp if r["periodo"] == p and r["tipo"] == "ingresos"]) for p in sorted({r["periodo"] for r in esp if r["tipo"] == "ingresos"}))}
esp_delta_failures, esp_delta_ids, esp_actual_keys = [], set(), set()
for d in esp_deltas:
    esp_delta_ids.add(d["registro_derivado_id"])
    esp_actual_keys.add((d["periodo"], d["codigo_cuenta_pdf"], d["metrica"]))
    current = esp_by_record.get(d["registro_actual_id"])
    if current is None or current["tipo"] != "ingresos" or current["documento_id"] not in esp_accepted_ids:
        esp_delta_failures.append(d["registro_derivado_id"] + "|actual")
        continue
    month = int(d["mes_numero"])
    if month == 1:
        prior = None
        if d["metodo_base"] != "cero_inicio_anio_convencion" or d["registro_previo_id"] or d["valor_acumulado_previo_clp"] != "":
            esp_delta_failures.append(d["registro_derivado_id"] + "|base_enero")
    else:
        prior = esp_by_record.get(d["registro_previo_id"])
        if prior is None or prior["periodo"] != prev_period(d["periodo"]) or prior["documento_id"] not in esp_accepted_ids:
            esp_delta_failures.append(d["registro_derivado_id"] + "|previo")
            continue
    metric = d["metrica"]
    actual = int(current[metric]); base = int(prior[metric]) if prior else 0; delta = actual - base
    if int(d["base_numerica_utilizada_clp"]) != base or int(d["valor_acumulado_actual_clp"]) != actual or int(d["delta_mensual_clp"]) != delta or int(d["diferencia_control_clp"]) != base + delta - actual or d["control_consistencia"] != "calza":
        esp_delta_failures.append(d["registro_derivado_id"] + "|aritmetica")
    for suffix, source in [("actual", current), ("previo", prior)]:
        for field in ["fuente_archivo", "fuente_ruta_relativa", "fuente_pagina", "fuente_linea", "fuente_sha256"]:
            expected_value = source[field] if source else ""
            if d[field + "_" + suffix] != expected_value:
                esp_delta_failures.append(d["registro_derivado_id"] + "|trazabilidad_" + suffix)
expected_esp_keys, expected_delta_findings = set(), set()
for period, rows in income_by_period.items():
    month = int(period.split("-")[1]); previous = prev_period(period)
    previous_rows = {r["codigo_cuenta_pdf"]: r for r in income_by_period.get(previous, [])} if previous else {}
    if month != 1 and not previous_rows:
        continue
    current_codes = {r["codigo_cuenta_pdf"] for r in rows}
    if previous:
        expected_delta_findings.update((period, code, "cuenta_sin_corte_previo") for code in current_codes - set(previous_rows))
        expected_delta_findings.update((period, code, "cuenta_ausente_en_corte_actual") for code in set(previous_rows) - current_codes)
    for r in rows:
        if month != 1 and r["codigo_cuenta_pdf"] not in previous_rows:
            continue
        for metric in ESP_METRICS["ingresos"]:
            expected_esp_keys.add((period, r["codigo_cuenta_pdf"], metric))
check("esp_delta_cuentas_unicidad_y_cantidad", len(esp_delta_ids) == len(esp_deltas) == 57636, len(esp_deltas), 57636)
check("esp_delta_cuentas_recalculo_y_trazabilidad", not esp_delta_failures, f"{len(esp_deltas)-len(esp_delta_failures)}/{len(esp_deltas)}", "57636/57636")
check("esp_delta_cuentas_cobertura_exacta", esp_actual_keys == expected_esp_keys, f"actual={len(esp_actual_keys)}; faltantes={len(expected_esp_keys-esp_actual_keys)}; inesperados={len(esp_actual_keys-expected_esp_keys)}", f"esperado={len(expected_esp_keys)}")
actual_delta_findings = {(r["periodo"], r["codigo_cuenta_pdf"], r["subtipo"]) for r in esp_delta_findings}
check("esp_delta_hallazgos_ausencias_exactos", actual_delta_findings == expected_delta_findings and len(esp_delta_findings) == 53, f"actual={len(actual_delta_findings)}; esperados={len(expected_delta_findings)}", "53; sin imputación")

esp_total_delta_failures, esp_total_delta_ids, esp_total_actual_keys = [], set(), set()
for d in esp_total_deltas:
    esp_total_delta_ids.add(d["registro_derivado_id"])
    esp_total_actual_keys.add((d["periodo"], d["ambito_total"], d["metrica"]))
    current = esp_total_by_id.get(d["documento_actual_id"])
    if current is None:
        esp_total_delta_failures.append(d["registro_derivado_id"] + "|actual")
        continue
    month = int(d["mes_numero"])
    if month == 1:
        prior = None
        if d["metodo_base"] != "cero_inicio_anio_convencion" or d["documento_previo_id"] or d["valor_acumulado_previo_clp"] != "":
            esp_total_delta_failures.append(d["registro_derivado_id"] + "|base_enero")
    else:
        prior = esp_total_by_id.get(d["documento_previo_id"])
        if prior is None or prior["periodo"] != prev_period(d["periodo"]):
            esp_total_delta_failures.append(d["registro_derivado_id"] + "|previo")
            continue
    field = "total_oficial_" + d["metrica"] if d["ambito_total"] == "oficial" else "saldo_por_percibir_suma_detalle_clp"
    actual = int(current[field]); base = int(prior[field]) if prior else 0; delta = actual - base
    if int(d["base_numerica_utilizada_clp"]) != base or int(d["valor_acumulado_actual_clp"]) != actual or int(d["delta_mensual_clp"]) != delta or int(d["diferencia_control_clp"]) != base + delta - actual:
        esp_total_delta_failures.append(d["registro_derivado_id"] + "|aritmetica")
    for suffix, source in [("actual", current), ("previo", prior)]:
        expected_values = {
            "fuente_archivo_" + suffix: source["fuente_archivo"] if source else "",
            "fuente_ruta_relativa_" + suffix: source["fuente_ruta_relativa"] if source else "",
            "fuente_pagina_" + suffix: source["total_fuente_pagina"] if source else "",
            "fuente_linea_" + suffix: source["total_fuente_linea"] if source else "",
            "fuente_sha256_" + suffix: source["fuente_sha256"] if source else "",
        }
        if any(d[k] != v for k, v in expected_values.items()):
            esp_total_delta_failures.append(d["registro_derivado_id"] + "|trazabilidad_" + suffix)
expected_total_keys = set()
for current in esp_totals:
    period = current["periodo"]
    month = int(period.split("-")[1]); previous = prev_period(period)
    if month != 1 and not any(r["periodo"] == previous for r in esp_totals):
        continue
    for scope, metric in [("oficial", m) for m in ESP_METRICS["ingresos"]] + [("suma_detalle", "saldo_por_percibir_clp")]:
        expected_total_keys.add((period, scope, metric))
check("esp_delta_totales_unicidad_y_cantidad", len(esp_total_delta_ids) == len(esp_total_deltas) == 340, len(esp_total_deltas), 340)
check("esp_delta_totales_recalculo_y_trazabilidad", not esp_total_delta_failures, f"{len(esp_total_deltas)-len(esp_total_delta_failures)}/{len(esp_total_deltas)}", "340/340")
check("esp_delta_totales_cobertura_y_separacion", esp_total_actual_keys == expected_total_keys, f"actual={len(esp_total_actual_keys)}; esperado={len(expected_total_keys)}", "340; 9 oficiales + 1 suma detalle por corte")
income_coverage = [c for c in esp_coverage if c["tipo"] == "ingresos"]
esp_computable = sum(c["estado_delta_mensual"].startswith("computable") for c in income_coverage)
esp_not_computable = sum(c["estado_delta_mensual"].startswith("no_computable") for c in income_coverage)
check("esp_cobertura_cortes_delta_ingresos", (esp_computable, esp_not_computable) == (34, 2), f"computables={esp_computable}; no_computables={esp_not_computable}", "34;2")
check("esp_julio_y_agosto_2025_sin_deltas", not any(d["periodo"] in {"2025-07", "2025-08"} for d in esp_deltas + esp_total_deltas), 0, 0)

# Cotejo de versionado, incluidos los 33 códigos de Etapa 1.
stage1 = read_csv(DOCS / "REGISTRO_HALLAZGOS_ETAPA1_v1.csv")
stage1_codes = {r["codigo_cuenta_pdf"] for r in stage1 if r.get("subtipo") == "fuera_catalogo_mismo_nivel"}
version_codes = {r["codigo_cuenta_pdf"] for r in versioning}
check("cotejo_conserva_33_codigos_etapa1", len(stage1_codes) == 33 and stage1_codes <= version_codes, f"etapa1={len(stage1_codes)}; cotejo={len(version_codes)}; faltantes={len(stage1_codes-version_codes)}", "33 incluidos")
check("cotejo_bep_sin_remapeo", len(versioning) == 35 and all(r["estado_catalogo_vigente"] == "ausente" and r["decision"] == "conservar_codigo_original_sin_remapear" for r in versioning), len(versioning), 35)
check("cotejo_esp_sin_remapeo", len(esp_versioning) == 51 and all(r["estado_catalogo_vigente"] == "ausente" and r["decision"] == "conservar_codigo_original_sin_remapear" for r in esp_versioning), len(esp_versioning), 51)
check("registro_hallazgos_ids_unicos", len({f["hallazgo_id"] for f in findings}) == len(findings), len(findings), len(findings))

governance = (ROOT / "gobernanza" / "registro_de_decisiones.md").read_text(encoding="utf-8")
tp_pending = (ROOT / "gobernanza" / "solicitudes_tp_pendientes.md").read_text(encoding="utf-8")
check("gobernanza_d13_registrada", "D-13 · 2026-11-15" in governance and "35/35 reprodujeron las tres condiciones" in governance, "D-13 y resultado 35/35", "D-13 vigente")
check("gobernanza_tp18_descartada", "TP-18" in tp_pending and "DESCARTADA" in tp_pending and "Causa documentada del descarte" in tp_pending, "TP-18 cerrada sin solicitar", "descartada con causa documentada")

all_ok = all(c["resultado"] == "calza" for c in checks)
result = {
    "alcance": "Validación independiente conjunta de BEP, series mensuales BEP/ESP y ESP como Estado Presupuestario separado",
    "resultado_general": "aprobado_con_cobertura_bep_limitada_por_cuarentenas" if all_ok else "no_aprobado",
    "resultado_bep": "aprobado_con_politica_refinada_y_cobertura_limitada" if all_ok else "no_aprobado",
    "resultado_esp": "aprobado_70_documentos_35_ingresos_rehabilitados_d13" if all_ok else "no_aprobado",
    "controles": checks, "agregados_bep": bep_aggregates, "agregados_esp_informativos": esp_aggregates,
    "agregados_esp_gastos": esp_gastos_aggregates, "agregados_esp_ingresos_informativos": esp_ingresos_aggregates,
    "por_documento_bep": bep_per_doc, "por_documento_esp": esp_per_doc,
    "bep_registros": len(bep), "esp_registros": len(esp), "delta_registros_bep": len(deltas),
    "delta_registros_esp_cuentas": len(esp_deltas), "delta_registros_esp_totales": len(esp_total_deltas),
    "inventario_pdf": len(inventory), "bep_aceptados": len(bep_accepted_ids), "bep_cuarentena": sorted(actual_quarantine),
    "esp_aceptados": len(esp_accepted_ids), "esp_cuarentena": len(esp_docs)-len(esp_accepted_ids),
    "esp_ingresos_rehabilitados_d13": sum(d["estado"] == "aceptado" for d in esp_income_docs),
    "esp_hallazgos_delta_cuentas": len(esp_delta_findings),
    "codigos_versionado": {"bep": len(version_codes), "esp": len(esp_versioning), "etapa1": len(stage1_codes), "adicionales_bep": sorted(version_codes-stage1_codes)},
}
(DOCS / "VALIDACION_FINAL_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

L = ["# VALIDACIÓN FINAL — INFORMACIÓN PRESUPUESTARIA", "", "**Alcance:** canónico BEP 2023–2025, series mensuales BEP y ESP de ingresos, y ESP como Estado Presupuestario separado. La validación recalcula controles desde los canónicos y contrasta totales impresos, fuentes y hashes.", "", f"**Resultado general:** {'APROBADO; LA COBERTURA BEP PERMANECE LIMITADA POR CINCO CUARENTENAS' if all_ok else 'NO APROBADO'}. ESP queda aceptado en 70/70 documentos, sujeto a la regla documental D-13 para ingresos y a la ausencia declarada de julio de 2025.", "", "## 1. BEP: tres niveles y política refinada", "", "| Año | Documentos | Líneas | Catálogo, tasa bruta | Jerarquía informativa | Totales impresos | Aritmética |", "|---|---:|---:|---:|---:|---:|---:|"]
for label in ["2023", "2024", "2025", "total"]:
    a = bep_aggregates[label]
    L.append(f"| {label} | {a['documentos']} | {a['lineas']} | {a['catalogo_encontradas']}/{a['lineas']} — {pct(a['catalogo_tasa_bruta'])} | {a['jerarquia_calzan']}/{a['controles_jerarquia']} — {pct(a['tasa_jerarquia'])} | {a['totales_calzan']}/{a['controles_totales']} — {pct(a['tasa_totales'])} | {a['aritmetica_calza']}/{a['lineas']} — {pct(a['tasa_aritmetica'])} |")
L += ["", "Los documentos con política inicial cumplen totales 100 %, jerarquía ≥95 % y aritmética ≥99 %. Los 28 con política refinada cumplen totales 100 %, aritmética ≥99 % y cada diferencia jerárquica ≤2 M$. La jerarquía agregada se informa sin ocultar las diferencias. El anexo permanente contiene 975 diferencias; la verificación visual confirmó 10/10 líneas.", "", "Permanecen fuera del canónico: BEP_2023-08_GASTOS_ORIGINAL, BEP_2023-09_GASTOS_ORIGINAL, BEP_2023-11_GASTOS_ORIGINAL, BEP_2024-02_GASTOS_ORIGINAL y BEP_2023-01_INGRESOS_REPUBLICACION_V2.", "", "## 2. ESP: gastos estrictos e ingresos D-13", "", "### Controles clásicos informativos sobre todos los aceptados", "", "Estas tasas describen los documentos, pero no son el criterio de aceptación de ingresos D-13. En particular, el total clásico de saldo por percibir no se fuerza a calzar.", "", "| Año | Documentos | Líneas | Catálogo, tasa bruta | Jerarquía | Totales impresos | Aritmética principal | Identidades adicionales |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for label in ["2023", "2024", "2025", "total"]:
    a = esp_aggregates[label]
    L.append(f"| {label} | {a['documentos']} | {a['lineas']} | {a['catalogo_encontradas']}/{a['lineas']} — {pct(a['catalogo_tasa_bruta'])} | {a['jerarquia_calzan']}/{a['controles_jerarquia']} — {pct(a['tasa_jerarquia'])} | {a['totales_calzan']}/{a['controles_totales']} — {pct(a['tasa_totales'])} | {a['aritmetica_calza']}/{a['lineas']} — {pct(a['tasa_aritmetica'])} | {a['identidades_adicionales_calzan']}/{a['controles_identidades_adicionales']} — {pct(a['tasa_identidades_adicionales'])} |")
L += ["", "### Criterio de aceptación", "", "- Los 35 ESP de gastos cumplen individualmente totales 100 %, jerarquía ≥95 % y aritmética ≥99 %.", "- Los 35 ESP de ingresos reprodujeron individualmente las tres condiciones D-13: 35/35 rehabilitados y 0 en cuarentena. Las ocho métricas distintas de saldo por percibir calzan 280/280; el total oficial y la reconciliación con la cuenta 15 tienen residual cero en todos los documentos.", "- `ESP_2023-2025_totales_ingresos_v1.csv` conserva `total_saldo_por_percibir_oficial_clp` y `saldo_por_percibir_suma_detalle_clp` con nombres y series separados. La diferencia se explica por la cuenta 15 y no se oculta.", "- Las 35 líneas de la cuenta 15 conservan saldo por percibir impreso en cero; la exportación canónica coincide con el parseo y ningún PDF fue modificado. Los 70 títulos confirman “Estado Presupuestario”, con evidencia literal y trazabilidad.", "", "## 3. Controles independientes", "", "| Control | Resultado | Observado | Esperado |", "|---|---|---|---|"]
for c in checks:
    L.append(f"| {c['control']} | {c['resultado']} | {c['observado']} | {c['esperado']} |")
L += ["", "## 4. Cobertura, series y versionado", "", f"- Inventario: {len(inventory)} PDF con SHA-256 verificado; 71 BEP y 70 ESP.", f"- BEP: 66 aceptados, 5 en cuarentena y {len(bep)} registros canónicos.", f"- ESP: 70 aceptados, 0 en cuarentena y {len(esp)} registros canónicos; 35 ingresos rehabilitados por D-13.", f"- Serie BEP: {len(deltas)} deltas recalculados; 61 cortes computables y 11 no computables.", f"- Serie ESP de ingresos: {len(esp_deltas)} deltas de cuentas y {len(esp_total_deltas)} de totales recalculados en 34 cortes. Los {len(esp_delta_findings)} casos de cuentas ausentes en un corte quedan sin delta y sin imputación.", "- Julio de 2025: ausencia declarada en ambas familias y tipos; sin filas ni interpolación. Agosto de 2025 no tiene delta que salte julio.", "- Enero de 2023: original y v2 conservados; v2 en cuarentena y original usado para la serie BEP.", f"- Versionado: {len(versioning)} códigos BEP y {len(esp_versioning)} ESP, sin remapeo; los 33 de Etapa 1 están incluidos.", "- Gobernanza: D-13 vigente y TP-18 descartada con causa documentada.", ""]
(DOCS / "VALIDACION_FINAL_v1.md").write_text("\n".join(L), encoding="utf-8")

manifest_files = [
    OUT / "BEP_2023-2025_canonico_v1.csv", OUT / "BEP_2023-2025_serie_mensual_v1.csv",
    OUT / "BEP_2023-2025_cobertura_v1.csv", OUT / "BEP_2023-2025_documentos_v1.csv", OUT / "BEP_2023-2025_hallazgos_delta_v1.csv",
    OUT / "ESP_2023-2025_canonico_v1.csv", OUT / "ESP_2023-2025_cobertura_v1.csv", OUT / "ESP_2023-2025_documentos_v1.csv",
    OUT / "ESP_2023-2025_controles_D13_v1.csv", OUT / "ESP_2023-2025_totales_ingresos_v1.csv",
    OUT / "ESP_2023-2025_serie_mensual_ingresos_v1.csv", OUT / "ESP_2023-2025_serie_totales_ingresos_v1.csv",
    OUT / "ESP_2023-2025_hallazgos_delta_ingresos_v1.csv", OUT / "ESP_2023-2025_resumen_series_ingresos_v1.json",
    DOCS / "INVENTARIO_FUENTES_v1.csv", DOCS / "REGISTRO_HALLAZGOS_v1.csv", DOCS / "REGISTRO_HALLAZGOS_v1.md",
    DOCS / "COTEJO_VERSIONADO_CODIGOS_v1.csv", DOCS / "COTEJO_VERSIONADO_CODIGOS_ESP_v1.csv",
    DOCS / "DICCIONARIO_DATOS_v1.md", DOCS / "BITACORA_TRANSFORMACIONES_v1.md", DOCS / "COBERTURA_Y_AUSENCIAS_v1.md",
    DOCS / "MEMO_DESCUADRE_ESP_INGRESOS_v1.md", ROOT / "gobernanza" / "registro_de_decisiones.md", ROOT / "gobernanza" / "solicitudes_tp_pendientes.md",
    DOCS / "ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv", DOCS / "ANALISIS_CUARENTENAS_BEP_v1.md",
    DOCS / "VERIFICACION_VISUAL_CUARENTENAS_v1.csv", DOCS / "VERIFICACION_VISUAL_CUARENTENAS_v1.md",
    DOCS / "VALIDACION_FINAL_v1.md", DOCS / "VALIDACION_FINAL_v1.json",
]
manifest = [{"archivo": p.name, "ruta_relativa": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in manifest_files]
with (DOCS / "MANIFIESTO_ENTREGABLES_v1.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["archivo", "ruta_relativa", "bytes", "sha256"])
    writer.writeheader(); writer.writerows(manifest)
print(json.dumps({"resultado": result["resultado_general"], "controles_calzan": sum(c["resultado"] == "calza" for c in checks), "controles_totales": len(checks),
                  "bep_registros": len(bep), "esp_registros": len(esp), "deltas_bep": len(deltas),
                  "deltas_esp_cuentas": len(esp_deltas), "deltas_esp_totales": len(esp_total_deltas),
                  "fallidos": [c for c in checks if c["resultado"] != "calza"]}, ensure_ascii=False, indent=2))
raise SystemExit(0 if all_ok else 1)
