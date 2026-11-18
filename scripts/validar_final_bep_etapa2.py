from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import re

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria"
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "bep_etapa2"
OUT = ROOT / "datos procesados" / "07_Información_Presupuestaria"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
METRICS = {
    "gastos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp", "saldo_presupuestario_miles_clp", "deuda_exigible_miles_clp"],
    "ingresos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "ingresos_percibidos_miles_clp", "saldo_presupuestario_miles_clp", "ingresos_por_percibir_miles_clp"],
}
ALL_METRICS = ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp", "deuda_exigible_miles_clp", "ingresos_percibidos_miles_clp", "ingresos_por_percibir_miles_clp", "saldo_presupuestario_miles_clp"]
THRESHOLDS = {"totales": 1.0, "jerarquia": 0.95, "aritmetica": 0.99}


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


canonical = read_csv(OUT / "BEP_2023-2025_canonico_v1.csv")
doc_rows = read_csv(OUT / "BEP_2023-2025_documentos_v1.csv")
coverage = read_csv(OUT / "BEP_2023-2025_cobertura_v1.csv")
deltas = read_csv(OUT / "BEP_2023-2025_serie_mensual_v1.csv")
inventory = read_csv(DOCS / "INVENTARIO_FUENTES_v1.csv")
versioning = read_csv(DOCS / "COTEJO_VERSIONADO_CODIGOS_v1.csv")
all_work_docs = []
all_work_records = []
all_work_totals = []
for year in [2023, 2024, 2025]:
    all_work_docs.extend(json.loads((WORK / str(year) / f"documentos_bep_{year}.json").read_text(encoding="utf-8")))
    all_work_records.extend(read_csv(WORK / str(year) / f"bep_{year}_parseado.csv"))
    all_work_totals.extend(read_csv(WORK / str(year) / f"bep_{year}_validacion_totales.csv"))
work_doc_by_id = {d["documento_id"]: d for d in all_work_docs}
accepted_ids = {d["documento_id"] for d in all_work_docs if d["estado"] == "aceptado"}
canon_doc_ids = {r["documento_id"] for r in canonical}
by_doc = defaultdict(list)
by_record_id = {}
for r in canonical:
    by_doc[r["documento_id"]].append(r)
    by_record_id[r["registro_id"]] = r
work_by_registro = {r["registro_id"]: r for r in all_work_records}

checks = []
def check(name, ok, observed, expected=""):
    checks.append({"control": name, "resultado": "calza" if ok else "no_calza", "observado": observed, "esperado": expected})

check("inventario_cantidad_fisica", len(inventory) == len(list(RAW.rglob("*.pdf"))), len(inventory), len(list(RAW.rglob("*.pdf"))))
check("inventario_familias", (sum(i["familia"] == "BEP" for i in inventory), sum(i["familia"] == "ESP" for i in inventory)) == (71, 70), f"BEP={sum(i['familia'] == 'BEP' for i in inventory)}; ESP={sum(i['familia'] == 'ESP' for i in inventory)}", "BEP=71; ESP=70")
hash_failures = []
for i in inventory:
    path = ROOT / i["ruta_relativa"]
    if not path.exists() or sha256(path) != i["sha256"]:
        hash_failures.append(i["ruta_relativa"])
check("hashes_inventario_completo", not hash_failures, f"{len(inventory) - len(hash_failures)}/{len(inventory)}", f"{len(inventory)}/{len(inventory)}")
check("canonico_solo_documentos_aceptados", canon_doc_ids == accepted_ids, len(canon_doc_ids), len(accepted_ids))
check("cuarentenas_excluidas", not (canon_doc_ids & {d["documento_id"] for d in all_work_docs if d["estado"] != "aceptado"}), 0, 0)
check("unicidad_registro_id", len({r["registro_id"] for r in canonical}) == len(canonical), len({r["registro_id"] for r in canonical}), len(canonical))
check("unicidad_documento_cuenta", len({(r["documento_id"], r["codigo_cuenta_pdf"]) for r in canonical}) == len(canonical), len({(r["documento_id"], r["codigo_cuenta_pdf"]) for r in canonical}), len(canonical))

trace_failures = []
raw_failures = []
export_failures = []
applicability_failures = []
for r in canonical:
    path = ROOT / r["fuente_ruta_relativa"]
    if not all([r["fuente_archivo"], r["fuente_ruta_relativa"], r["fuente_pagina"], r["fuente_linea"], re.fullmatch(r"[0-9a-f]{64}", r["fuente_sha256"])]):
        trace_failures.append(r["registro_id"])
    elif not path.exists() or path.name != r["fuente_archivo"] or sha256(path) != r["fuente_sha256"]:
        trace_failures.append(r["registro_id"])
    for metric in ALL_METRICS:
        value, raw = r[metric], r[metric + "_raw"]
        if (value == "") != (raw == ""):
            raw_failures.append(r["registro_id"] + "|" + metric)
        elif value != "" and money_raw(raw) != int(value):
            raw_failures.append(r["registro_id"] + "|" + metric)
    source = work_by_registro.get(r["registro_id"])
    if source is None:
        export_failures.append(r["registro_id"])
    else:
        for field in ["documento_id", "periodo", "tipo", "version_fuente", "codigo_cuenta_pdf", "denominacion_pdf", "fuente_archivo", "fuente_ruta_relativa", "fuente_pagina", "fuente_linea", "fuente_sha256", "texto_linea_raw"]:
            if r[field] != source[field]:
                export_failures.append(r["registro_id"] + "|" + field)
        for metric in METRICS[r["tipo"]]:
            if r[metric] != source[metric] or r[metric + "_raw"] != source[metric + "_raw"]:
                export_failures.append(r["registro_id"] + "|" + metric)
    expected_present = set(METRICS[r["tipo"]])
    actual_present = {m for m in ALL_METRICS if r[m] != ""}
    if actual_present != expected_present:
        applicability_failures.append(r["registro_id"])
check("trazabilidad_y_hash_por_registro", not trace_failures, f"{len(canonical) - len(trace_failures)}/{len(canonical)}", f"{len(canonical)}/{len(canonical)}")
check("valores_raw_coinciden_numericos", not raw_failures, len(raw_failures), 0)
check("exportacion_coincide_parseo", not export_failures, len(export_failures), 0)
check("metricas_no_aplicables_nulas", not applicability_failures, len(applicability_failures), 0)

# Recálculo independiente de los tres niveles, por documento y agregado.
catalog_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))
catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
catalog_failures = []
summary = {}
per_document = {}
for did, rows in by_doc.items():
    tipo = rows[0]["tipo"]
    h_ok = h_total = 0
    for parent in rows:
        code, level = parent["codigo_cuenta_pdf"], int(parent["nivel_jerarquico"])
        children = [r for r in rows if int(r["nivel_jerarquico"]) == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
        for metric in METRICS[tipo] if children else []:
            h_total += 1
            h_ok += int(parent[metric]) == sum(int(c[metric]) for c in children)
    printed = {(t["documento_id"], t["metrica"]): int(t["total_impreso"]) for t in all_work_totals if t["documento_id"] == did}
    top = [r for r in rows if int(r["nivel_jerarquico"]) == 1]
    t_ok = t_total = 0
    for metric in METRICS[tipo]:
        t_total += 1
        t_ok += printed[(did, metric)] == sum(int(r[metric]) for r in top)
    executed = "obligacion_devengada_miles_clp" if tipo == "gastos" else "ingresos_percibidos_miles_clp"
    a_ok = sum(int(r["saldo_presupuestario_miles_clp"]) == int(r["presupuesto_vigente_miles_clp"]) - int(r[executed]) for r in rows)
    rates = {"totales": t_ok / t_total, "jerarquia": h_ok / h_total, "aritmetica": a_ok / len(rows)}
    per_document[did] = {"totales": f"{t_ok}/{t_total}", "jerarquia": f"{h_ok}/{h_total}", "aritmetica": f"{a_ok}/{len(rows)}", "umbrales_calzan": all(rates[k] >= v for k, v in THRESHOLDS.items())}
    summary[did] = {"rows": rows, "h_ok": h_ok, "h_total": h_total, "t_ok": t_ok, "t_total": t_total, "a_ok": a_ok}
check("umbrales_en_cada_documento_canonico", all(v["umbrales_calzan"] for v in per_document.values()), sum(v["umbrales_calzan"] for v in per_document.values()), len(per_document))

for r in canonical:
    code, level = r["codigo_cuenta_pdf"], int(r["nivel_jerarquico"])
    expected = "encontrada" if code in catalog else ("fuera_catalogo_nivel_detalle_no_representado" if level > 3 else "fuera_catalogo_mismo_nivel")
    if r["catalogo_estado"] != expected or r["catalogo_denominacion"] != catalog.get(code, {}).get("DENOMINACIÓN", ""):
        catalog_failures.append(r["registro_id"])
check("cotejo_catalogo_sin_remapeo", not catalog_failures, len(catalog_failures), 0)

def aggregate(ids):
    selected = [summary[did] for did in ids]
    rows = [r for item in selected for r in item["rows"]]
    h_ok = sum(x["h_ok"] for x in selected)
    h_total = sum(x["h_total"] for x in selected)
    t_ok = sum(x["t_ok"] for x in selected)
    t_total = sum(x["t_total"] for x in selected)
    a_ok = sum(x["a_ok"] for x in selected)
    return {
        "documentos": len(selected), "lineas": len(rows),
        "catalogo_encontradas": sum(r["codigo_cuenta_pdf"] in catalog for r in rows),
        "catalogo_tasa_bruta": sum(r["codigo_cuenta_pdf"] in catalog for r in rows) / len(rows),
        "jerarquia_calzan": h_ok, "controles_jerarquia": h_total, "tasa_jerarquia": h_ok / h_total,
        "totales_calzan": t_ok, "controles_totales": t_total, "tasa_totales": t_ok / t_total,
        "aritmetica_calza": a_ok, "tasa_aritmetica": a_ok / len(rows),
    }
aggregates = {str(year): aggregate([did for did, rows in by_doc.items() if int(rows[0]["anio"]) == year]) for year in [2023, 2024, 2025]}
aggregates["total"] = aggregate(list(by_doc))
for label, values in aggregates.items():
    check(f"umbrales_agregados_{label}", values["tasa_totales"] == 1 and values["tasa_jerarquia"] >= .95 and values["tasa_aritmetica"] >= .99, f"totales={pct(values['tasa_totales'])}; jerarquia={pct(values['tasa_jerarquia'])}; aritmetica={pct(values['tasa_aritmetica'])}", "100 %; >=95 %; >=99 %")
check("totales_independientes", aggregates["total"]["totales_calzan"] == aggregates["total"]["controles_totales"], f"{aggregates['total']['totales_calzan']}/{aggregates['total']['controles_totales']}", "190/190")

# Cobertura y ausencia declarada.
check("cobertura_72_periodos_tipo", len(coverage) == 72 and len({(c["periodo"], c["tipo"]) for c in coverage}) == 72, len(coverage), 72)
july = [c for c in coverage if c["periodo"] == "2025-07"]
check("julio_2025_ausencia_declarada", len(july) == 2 and all(c["estado_corte"] == "ausencia_declarada_no_publicado" for c in july), len(july), 2)
check("julio_2025_sin_datos", not any(r["periodo"] == "2025-07" for r in canonical) and not any(d["periodo"] == "2025-07" for d in deltas), 0, 0)
check("agosto_2025_sin_delta_saltando_julio", not any(d["periodo"] == "2025-08" for d in deltas), 0, 0)
v2_id = "BEP_2023-01_INGRESOS_REPUBLICACION_V2"
original_id = "BEP_2023-01_INGRESOS_ORIGINAL"
check("republicacion_ambas_versiones_inventariadas", {i["version_fuente"] for i in inventory if i["periodo_nombre_archivo"] == "2023-01" and i["familia"] == "BEP" and i["tipo"] == "ingresos"} == {"original", "republicacion_v2"}, "original+v2", "original+v2")
check("republicacion_v2_parseada_y_cuarentenada", v2_id in work_doc_by_id and work_doc_by_id[v2_id]["estado"] == "cuarentena" and work_doc_by_id[v2_id]["lineas"] == 95 and v2_id not in canon_doc_ids, work_doc_by_id.get(v2_id, {}).get("estado"), "cuarentena; 95 líneas")
check("enero_2023_usa_original", original_id in canon_doc_ids and all(r["seleccionado_para_serie"] == "si" for r in by_doc[original_id]), original_id, original_id)

# Recalcular cada delta y el universo esperado sin usar la lógica del constructor.
delta_failures = []
delta_ids = set()
actual_keys = set()
for d in deltas:
    delta_ids.add(d["registro_derivado_id"])
    key = (d["periodo"], d["tipo"], d["codigo_cuenta_pdf"], d["metrica"])
    actual_keys.add(key)
    current = by_record_id.get(d["registro_actual_id"])
    if current is None or current["documento_id"] not in accepted_ids:
        delta_failures.append(d["registro_derivado_id"] + "|actual")
        continue
    month = int(d["mes_numero"])
    if month == 1:
        prior = None
        if d["metodo_base"] != "cero_inicio_anio_convencion" or d["registro_previo_id"] or d["valor_acumulado_previo_miles_clp"] != "":
            delta_failures.append(d["registro_derivado_id"] + "|base_enero")
    else:
        prior = by_record_id.get(d["registro_previo_id"])
        if prior is None or prior["periodo"] != prev_period(d["periodo"]) or prior["documento_id"] not in accepted_ids:
            delta_failures.append(d["registro_derivado_id"] + "|previo")
            continue
    metric = d["metrica"]
    actual = int(current[metric])
    base = int(prior[metric]) if prior else 0
    delta = actual - base
    if int(d["base_numerica_utilizada_miles_clp"]) != base or int(d["valor_acumulado_actual_miles_clp"]) != actual or int(d["delta_mensual_miles_clp"]) != delta or int(d["diferencia_control_miles_clp"]) != base + delta - actual or d["control_consistencia"] != "calza":
        delta_failures.append(d["registro_derivado_id"] + "|aritmetica")
check("unicidad_delta", len(delta_ids) == len(deltas), len(delta_ids), len(deltas))
check("recalculo_delta_y_trazabilidad", not delta_failures, f"{len(deltas) - len(delta_failures)}/{len(deltas)}", f"{len(deltas)}/{len(deltas)}")

selected = defaultdict(list)
for r in canonical:
    if r["seleccionado_para_serie"] == "si":
        selected[(r["periodo"], r["tipo"])].append(r)
expected_keys = set()
for (period, tipo), rows in selected.items():
    month = int(period.split("-")[1])
    previous = prev_period(period)
    previous_rows = {r["codigo_cuenta_pdf"]: r for r in selected.get((previous, tipo), [])} if previous else {}
    if month != 1 and not previous_rows:
        continue
    for r in rows:
        if month != 1 and r["codigo_cuenta_pdf"] not in previous_rows:
            continue
        for metric in METRICS[tipo]:
            expected_keys.add((period, tipo, r["codigo_cuenta_pdf"], metric))
check("cobertura_exacta_deltas", actual_keys == expected_keys, f"actual={len(actual_keys)}; faltantes={len(expected_keys - actual_keys)}; inesperados={len(actual_keys - expected_keys)}", f"esperado={len(expected_keys)}")

stage1 = read_csv(DOCS / "REGISTRO_HALLAZGOS_ETAPA1_v1.csv")
stage1_codes = {r["codigo_cuenta_pdf"] for r in stage1 if r.get("subtipo") == "fuera_catalogo_mismo_nivel"}
version_codes = {r["codigo_cuenta_pdf"] for r in versioning}
check("cotejo_conserva_33_codigos_etapa1", len(stage1_codes) == 33 and stage1_codes <= version_codes, f"etapa1={len(stage1_codes)}; cotejo={len(version_codes)}; faltantes={len(stage1_codes - version_codes)}", "33 incluidos")
check("cotejo_sin_remapeo", all(r["estado_catalogo_vigente"] == "ausente" and r["decision"] == "conservar_codigo_original_sin_remapear" for r in versioning), len(versioning), len(versioning))

all_ok = all(c["resultado"] == "calza" for c in checks)
result = {
    "alcance": "Validación independiente del canónico BEP y deltas; ESP pendiente por variante documental y autorización",
    "resultado_bep": "aprobado_con_cobertura_limitada_por_cuarentenas" if all_ok else "no_aprobado",
    "esp_estado": "no_escalado_pendiente_autorizacion_expresa",
    "controles": checks, "agregados": aggregates, "por_documento": per_document,
    "delta_registros": len(deltas), "inventario_pdf": len(inventory),
    "codigos_versionado": {"etapa1": len(stage1_codes), "cotejo_total": len(version_codes), "adicionales_etapa2": sorted(version_codes - stage1_codes)},
}
(DOCS / "VALIDACION_FINAL_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

L = ["# VALIDACIÓN FINAL — INFORMACIÓN PRESUPUESTARIA", "", "**Alcance:** canónico BEP 2023–2025 y serie mensual derivada. Los ESP no fueron escalados: la variante documental sigue pendiente de autorización expresa.", "", f"**Resultado BEP:** {'APROBADO CON COBERTURA LIMITADA POR CUARENTENAS' if all_ok else 'NO APROBADO'}. Esto no equivale a cobertura completa de los 71 BEP ni a finalización del componente ESP.", "", "## 1. Tres niveles de control", "", "| Alcance | Documentos | Líneas | Catálogo, tasa bruta | Jerarquía | Totales impresos | Aritmética |", "|---|---:|---:|---:|---:|---:|---:|"]
for label in ["2023", "2024", "2025", "total"]:
    a = aggregates[label]
    L.append(f"| {label} | {a['documentos']} | {a['lineas']} | {a['catalogo_encontradas']}/{a['lineas']} — {pct(a['catalogo_tasa_bruta'])} | {a['jerarquia_calzan']}/{a['controles_jerarquia']} — {pct(a['tasa_jerarquia'])} | {a['totales_calzan']}/{a['controles_totales']} — {pct(a['tasa_totales'])} | {a['aritmetica_calza']}/{a['lineas']} — {pct(a['tasa_aritmetica'])} |")
L += ["", "Catálogo es informativo, sin umbral de aceptación. Jerarquía, totales y aritmética fueron recalculados desde el canónico; los totales impresos se tomaron de las evidencias de parseo. Todos los documentos canónicos cumplen individualmente los umbrales.", "", "## 2. Controles independientes", "", "| Control | Resultado | Observado | Esperado |", "|---|---|---|---|"]
for c in checks:
    L.append(f"| {c['control']} | {c['resultado']} | {c['observado']} | {c['esperado']} |")
L += ["", "## 3. Cobertura y disposición", "", f"- Inventario: {len(inventory)} PDF, con SHA-256 verificado; 71 BEP y 70 ESP.", f"- BEP: 38 aceptados en canónico y 33 en cuarentena; {len(canonical)} registros.", f"- Serie mensual: {len(deltas)} filas, recalculadas y con cobertura exacta frente a cortes elegibles.", "- Julio de 2025: ausencia declarada; no hay datos ni delta de agosto que salte julio.", "- Enero de 2023: original y v2 inventariados y parseados; v2 en cuarentena por diferencia de contenido, original aceptado para la serie.", f"- Versionado: {len(stage1_codes)} códigos de Etapa 1 incluidos en un cotejo total de {len(version_codes)}; adicionales de Etapa 2: {', '.join(sorted(version_codes - stage1_codes)) or 'ninguno'}.", "", "## 4. Límite pendiente", "", "Los 70 archivos de la carpeta ESP permanecen fuera del canónico. Las dos muestras prevalidadas son estados presupuestarios de gastos con códigos presupuestarios, no estados financieros del plan municipal. Se requiere autorización expresa para tratar esa variante.", ""]
(DOCS / "VALIDACION_FINAL_v1.md").write_text("\n".join(L), encoding="utf-8")

manifest_files = [
    OUT / "BEP_2023-2025_canonico_v1.csv", OUT / "BEP_2023-2025_serie_mensual_v1.csv",
    OUT / "BEP_2023-2025_cobertura_v1.csv", OUT / "BEP_2023-2025_documentos_v1.csv",
    OUT / "BEP_2023-2025_hallazgos_delta_v1.csv", DOCS / "INVENTARIO_FUENTES_v1.csv",
    DOCS / "REGISTRO_HALLAZGOS_v1.csv", DOCS / "COTEJO_VERSIONADO_CODIGOS_v1.csv",
    DOCS / "DICCIONARIO_DATOS_v1.md", DOCS / "BITACORA_TRANSFORMACIONES_v1.md",
    DOCS / "COBERTURA_Y_AUSENCIAS_v1.md", DOCS / "REGISTRO_HALLAZGOS_v1.md",
    DOCS / "VALIDACION_FINAL_v1.md", DOCS / "VALIDACION_FINAL_v1.json",
]
manifest = [{"archivo": p.name, "ruta_relativa": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in manifest_files]
with (DOCS / "MANIFIESTO_ENTREGABLES_v1.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["archivo", "ruta_relativa", "bytes", "sha256"])
    writer.writeheader()
    writer.writerows(manifest)
print(json.dumps({"resultado": result["resultado_bep"], "controles_calzan": sum(c["resultado"] == "calza" for c in checks), "controles_totales": len(checks), "registros": len(canonical), "deltas": len(deltas), "codigos_adicionales": sorted(version_codes - stage1_codes)}, ensure_ascii=False, indent=2))
raise SystemExit(0 if all_ok else 1)
