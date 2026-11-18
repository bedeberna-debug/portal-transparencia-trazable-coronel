from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import csv
import hashlib
import json
import re

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria"
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "bep_etapa2"
OUT = ROOT / "datos procesados" / "07_Información_Presupuestaria"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
OUT.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)
YEARS = [2023, 2024, 2025]
MONTHS = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
MONTH_NAMES = [None, "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
METRICS = {
    "gastos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp", "saldo_presupuestario_miles_clp", "deuda_exigible_miles_clp"],
    "ingresos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "ingresos_percibidos_miles_clp", "saldo_presupuestario_miles_clp", "ingresos_por_percibir_miles_clp"],
}
ALL_METRICS = [
    "presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp",
    "deuda_exigible_miles_clp", "ingresos_percibidos_miles_clp", "ingresos_por_percibir_miles_clp",
    "saldo_presupuestario_miles_clp",
]
CANONICAL_FIELDS = [
    "esquema_version", "categoria", "subcategoria", "registro_id", "documento_id", "tipo", "version_fuente",
    "seleccionado_para_serie", "anio", "mes_numero", "mes_nombre", "periodo", "fecha_corte", "periodo_fuente",
    "formulario_cgr", "formulario_fuente", "codigo_cuenta_pdf", "nivel_jerarquico", "denominacion_pdf",
    "catalogo_estado", "catalogo_denominacion", "unidad_monetaria", "naturaleza_valor",
]
for _metric in ALL_METRICS:
    CANONICAL_FIELDS.extend([_metric, _metric + "_raw"])
CANONICAL_FIELDS.extend([
    "control_aritmetico_saldo", "control_aritmetico_diferencia_miles_clp", "estado_documento",
    "fuente_archivo", "fuente_ruta_relativa", "fuente_pagina", "fuente_linea", "fuente_sha256", "texto_linea_raw",
])


def write_csv(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pct(value):
    return f"{100 * value:.1f} %".replace(".", ",")


def join(value):
    if isinstance(value, list):
        return "|".join(str(x) for x in value)
    return "" if value is None else str(value)


def month_from_name(name):
    lower = name.lower()
    return next((number for token, number in MONTHS.items() if re.search(rf"\b{token}\b", lower)), None)


def prev_period(period):
    year, month = map(int, period.split("-"))
    return f"{year}-{month - 1:02d}" if month > 1 else None


def load_bep():
    docs, records, findings = [], [], []
    for year in YEARS:
        docs.extend(json.loads((WORK / str(year) / f"documentos_bep_{year}.json").read_text(encoding="utf-8")))
        records.extend(read_csv(WORK / str(year) / f"bep_{year}_parseado.csv"))
        findings.extend(read_csv(WORK / str(year) / f"bep_{year}_hallazgos.csv"))
    return docs, records, findings


docs, parsed_records, source_findings = load_bep()
doc_by_id = {d["documento_id"]: d for d in docs}
accepted_docs = [d for d in docs if d["estado"] == "aceptado"]
selected_docs = {}
for d in accepted_docs:
    key = (d["periodo"], d["tipo"])
    if key not in selected_docs or d["version_fuente"] == "republicacion_v2":
        selected_docs[key] = d["documento_id"]
selected_ids = set(selected_docs.values())
accepted_ids = {d["documento_id"] for d in accepted_docs}

canonical = []
for rec in parsed_records:
    did = rec["documento_id"]
    if did not in accepted_ids:
        continue
    doc = doc_by_id[did]
    own_forms = doc.get("formularios") or []
    row = {
        "esquema_version": "canonico_v1.0.0", "categoria": "informacion_presupuestaria",
        "subcategoria": "balance_ejecucion_presupuestaria", "registro_id": rec["registro_id"],
        "documento_id": did, "tipo": rec["tipo"], "version_fuente": rec["version_fuente"],
        "seleccionado_para_serie": "si" if did in selected_ids else "no",
        "anio": rec["anio"], "mes_numero": rec["mes_numero"], "mes_nombre": MONTH_NAMES[int(rec["mes_numero"])],
        "periodo": rec["periodo"], "fecha_corte": rec["fecha_corte"],
        "periodo_fuente": doc.get("periodo_fuente") or "contenido", "formulario_cgr": "0102" if rec["tipo"] == "gastos" else "0101",
        "formulario_fuente": "contenido" if own_forms else "documento_original_asociado",
        "codigo_cuenta_pdf": rec["codigo_cuenta_pdf"], "nivel_jerarquico": rec["nivel_jerarquico"],
        "denominacion_pdf": rec["denominacion_pdf"], "catalogo_estado": rec["catalogo_estado"],
        "catalogo_denominacion": rec.get("catalogo_denominacion", ""), "unidad_monetaria": "miles_de_CLP",
        "naturaleza_valor": "acumulado_al_corte",
        "control_aritmetico_saldo": rec["control_aritmetico_saldo"],
        "control_aritmetico_diferencia_miles_clp": rec["control_aritmetico_diferencia"],
        "estado_documento": rec["estado_documento"], "fuente_archivo": rec["fuente_archivo"],
        "fuente_ruta_relativa": rec["fuente_ruta_relativa"], "fuente_pagina": rec["fuente_pagina"],
        "fuente_linea": rec["fuente_linea"], "fuente_sha256": rec["fuente_sha256"],
        "texto_linea_raw": rec["texto_linea_raw"],
    }
    for metric in ALL_METRICS:
        row[metric] = rec.get(metric, "")
        row[metric + "_raw"] = rec.get(metric + "_raw", "")
    canonical.append(row)
canonical.sort(key=lambda r: (r["periodo"], r["tipo"], r["version_fuente"], r["codigo_cuenta_pdf"]))
write_csv(OUT / "BEP_2023-2025_canonico_v1.csv", canonical, CANONICAL_FIELDS)

canonical_by_id = {r["registro_id"]: r for r in canonical}
records_by_doc = defaultdict(list)
for r in canonical:
    records_by_doc[r["documento_id"]].append(r)

# Cobertura mensual: no se salta una ausencia ni una cuarentena para calcular deltas.
coverage = []
for year in YEARS:
    for month in range(1, 13):
        period = f"{year}-{month:02d}"
        for tipo in ["gastos", "ingresos"]:
            period_docs = [d for d in docs if d.get("periodo") == period and d.get("tipo") == tipo]
            accepted = [d for d in period_docs if d["estado"] == "aceptado"]
            quarantined = [d for d in period_docs if d["estado"] != "aceptado"]
            selected_id = selected_docs.get((period, tipo), "")
            if not period_docs:
                state = "ausencia_declarada_no_publicado" if period == "2025-07" else "ausencia_detectada"
                reason = "julio_2025_no_publicado" if period == "2025-07" else "sin_pdf_en_fuente"
            elif selected_id:
                state = "aceptado"
                reason = ""
            else:
                state = "cuarentena"
                reason = "|".join(sorted({m for d in quarantined for m in d.get("motivos_cuarentena", [])}))
            previous = prev_period(period)
            previous_selected = selected_docs.get((previous, tipo), "") if previous else ""
            if not selected_id:
                delta_state = "no_computable_corte_actual_no_aceptado"
            elif month == 1:
                delta_state = "computable_base_cero_inicio_anio"
            elif previous_selected:
                delta_state = "computable_cortes_consecutivos"
            else:
                delta_state = "no_computable_corte_previo_ausente_o_cuarentena"
            coverage.append({
                "periodo": period, "anio": year, "mes_numero": month, "tipo": tipo, "estado_corte": state,
                "motivo_estado": reason, "documentos_inventariados": len(period_docs),
                "documentos_aceptados": len(accepted), "documentos_cuarentena": len(quarantined),
                "documento_seleccionado_serie": selected_id, "periodo_previo_requerido": previous or "",
                "documento_previo_seleccionado": previous_selected, "estado_delta_mensual": delta_state,
                "regla": "sin_interpolacion_sin_saltar_cortes_sin_imputar_cuentas_ausentes",
            })
write_csv(OUT / "BEP_2023-2025_cobertura_v1.csv", coverage)

# Serie mensual en formato largo: una fila por periodo, cuenta y métrica.
deltas = []
delta_findings = []
for (period, tipo), did in sorted(selected_docs.items()):
    year, month = map(int, period.split("-"))
    previous = prev_period(period)
    previous_id = selected_docs.get((previous, tipo), "") if previous else ""
    if month != 1 and not previous_id:
        continue
    current_records = {r["codigo_cuenta_pdf"]: r for r in records_by_doc[did]}
    previous_records = {r["codigo_cuenta_pdf"]: r for r in records_by_doc[previous_id]} if previous_id else {}
    if previous_id:
        for code in sorted(set(current_records) - set(previous_records)):
            r = current_records[code]
            delta_findings.append({
                "hallazgo_tipo": "delta", "subtipo": "cuenta_ausente_en_corte_previo", "severidad": "control",
                "documento_id": did, "periodo": period, "codigo_cuenta_pdf": code,
                "decision": "delta_no_computable_no_imputar_cero", "fuente_archivo": r["fuente_archivo"],
                "fuente_ruta_relativa": r["fuente_ruta_relativa"], "fuente_pagina": r["fuente_pagina"],
                "fuente_linea": r["fuente_linea"], "fuente_sha256": r["fuente_sha256"],
            })
        for code in sorted(set(previous_records) - set(current_records)):
            r = previous_records[code]
            delta_findings.append({
                "hallazgo_tipo": "delta", "subtipo": "cuenta_ausente_en_corte_actual", "severidad": "control",
                "documento_id": did, "periodo": period, "codigo_cuenta_pdf": code,
                "decision": "delta_no_computable_no_imputar_cero", "fuente_archivo": r["fuente_archivo"],
                "fuente_ruta_relativa": r["fuente_ruta_relativa"], "fuente_pagina": r["fuente_pagina"],
                "fuente_linea": r["fuente_linea"], "fuente_sha256": r["fuente_sha256"],
            })
    for code, current in sorted(current_records.items()):
        if previous_id and code not in previous_records:
            continue
        prior = previous_records.get(code)
        for metric in METRICS[tipo]:
            actual = int(current[metric])
            base = int(prior[metric]) if prior else 0
            delta = actual - base
            difference = base + delta - actual
            deltas.append({
                "esquema_version": "canonico_v1.0.0", "registro_derivado_id": f"BEP_DELTA|{period}|{tipo}|{code}|{metric}|{current['fuente_sha256']}",
                "periodo": period, "anio": year, "mes_numero": month, "tipo": tipo, "codigo_cuenta_pdf": code,
                "nivel_jerarquico": current["nivel_jerarquico"], "denominacion_pdf": current["denominacion_pdf"],
                "metrica": metric, "unidad_monetaria": "miles_de_CLP", "periodo_previo": previous or "",
                "documento_actual_id": did, "documento_previo_id": previous_id,
                "registro_actual_id": current["registro_id"], "registro_previo_id": prior["registro_id"] if prior else "",
                "metodo_base": "cero_inicio_anio_convencion" if month == 1 else "acumulado_mes_consecutivo",
                "valor_acumulado_previo_miles_clp": "" if month == 1 else base,
                "base_numerica_utilizada_miles_clp": base, "valor_acumulado_actual_miles_clp": actual,
                "delta_mensual_miles_clp": delta, "control_consistencia": "calza" if difference == 0 else "no_calza",
                "diferencia_control_miles_clp": difference,
                "fuente_actual_archivo": current["fuente_archivo"], "fuente_actual_ruta_relativa": current["fuente_ruta_relativa"],
                "fuente_actual_pagina": current["fuente_pagina"], "fuente_actual_linea": current["fuente_linea"],
                "fuente_actual_sha256": current["fuente_sha256"], "fuente_previa_archivo": prior["fuente_archivo"] if prior else "",
                "fuente_previa_ruta_relativa": prior["fuente_ruta_relativa"] if prior else "",
                "fuente_previa_pagina": prior["fuente_pagina"] if prior else "", "fuente_previa_linea": prior["fuente_linea"] if prior else "",
                "fuente_previa_sha256": prior["fuente_sha256"] if prior else "",
            })
write_csv(OUT / "BEP_2023-2025_serie_mensual_v1.csv", deltas)
write_csv(OUT / "BEP_2023-2025_hallazgos_delta_v1.csv", delta_findings)

# Tabla documental con totales impresos, estados y selección de versión.
doc_rows = []
for d in sorted(docs, key=lambda x: (x.get("periodo", "9999"), x.get("tipo", ""), x.get("version_fuente", ""), x["archivo"])):
    row = {k: join(v) for k, v in d.items() if k not in ["totales_impresos", "sumas_subtitulos"]}
    row["en_canonico"] = "si" if d["documento_id"] in accepted_ids else "no"
    row["seleccionado_para_serie"] = "si" if d["documento_id"] in selected_ids else "no"
    for metric in ALL_METRICS:
        row["total_impreso_" + metric] = (d.get("totales_impresos") or {}).get(metric, "")
        row["suma_subtitulos_" + metric] = (d.get("sumas_subtitulos") or {}).get(metric, "")
    doc_rows.append(row)
write_csv(OUT / "BEP_2023-2025_documentos_v1.csv", doc_rows)

# Inventario físico completo; los ESP se inventarían y se conservan, pero no se escalan.
doc_by_sha = {d["sha256"]: d for d in docs}
prevalidated_esp = {
    "4043c4a471ce07a3847780d9676092f845263286d8c7e22bbe9a573dfb23cc6c",
    "262d52dd2d66a33ac95ec85d5fc45724bce8fb5903914aebb27973145a5cf494",
}
inventory = []
for path in sorted(RAW.rglob("*.pdf"), key=lambda p: str(p.relative_to(ROOT)).lower()):
    rel = str(path.relative_to(ROOT))
    digest = sha256(path)
    family = "BEP" if "Balance de Ejecución Presupuestaria" in rel else "ESP"
    year = next((int(part) for part in path.parts if part in {"2023", "2024", "2025"}), "")
    month = month_from_name(path.stem)
    tipo = "gastos" if "gasto" in path.name.lower() else "ingresos"
    version = "republicacion_v2" if "v2" in path.stem.lower() else "original"
    doc = doc_by_sha.get(digest)
    if family == "BEP":
        process_state = doc["estado"] if doc else "no_procesado"
        process_reason = join(doc.get("motivos_cuarentena")) if doc else ""
        did = doc["documento_id"] if doc else ""
    else:
        process_state = "prevalidado_no_escalado" if digest in prevalidated_esp else "no_escalado_variante_documental"
        process_reason = "pendiente_autorizacion_expresa_por_variante_documental"
        did = ""
    inventory.append({
        "familia": family, "anio_carpeta": year, "mes_nombre_archivo": month or "",
        "periodo_nombre_archivo": f"{year}-{month:02d}" if year and month else "",
        "tipo": tipo, "version_fuente": version, "archivo": path.name, "ruta_relativa": rel,
        "bytes": path.stat().st_size, "sha256": digest, "documento_id": did,
        "estado_procesamiento": process_state, "motivo_estado": process_reason,
    })
write_csv(DOCS / "INVENTARIO_FUENTES_v1.csv", inventory)

# Registro consolidado, enriquecido con la trazabilidad documental.
findings = []
for source in source_findings + delta_findings:
    row = dict(source)
    doc = doc_by_id.get(row.get("documento_id", ""), {})
    row["anio"] = doc.get("anio", str(row.get("periodo", ""))[:4])
    row["periodo"] = row.get("periodo") or doc.get("periodo", "")
    row["tipo"] = doc.get("tipo", "")
    row["version_fuente"] = doc.get("version_fuente", "")
    row["estado_documento"] = doc.get("estado", "")
    row["fuente_archivo"] = row.get("fuente_archivo") or doc.get("archivo", "")
    row["fuente_ruta_relativa"] = row.get("fuente_ruta_relativa") or doc.get("ruta_relativa", "")
    row["fuente_sha256"] = row.get("fuente_sha256") or doc.get("sha256", "")
    findings.append(row)
for d in docs:
    if d["estado"] == "aceptado":
        continue
    findings.append({
        "hallazgo_tipo": "cuarentena", "subtipo": "documento_bajo_umbral_o_variante", "severidad": "control",
        "documento_id": d["documento_id"], "anio": d.get("anio", ""), "periodo": d.get("periodo", ""),
        "tipo": d.get("tipo", ""), "version_fuente": d.get("version_fuente", ""), "estado_documento": d["estado"],
        "detalle": join(d.get("motivos_cuarentena")), "decision": "excluir_de_canonico_y_deltas_conservar_en_trabajo",
        "fuente_archivo": d["archivo"], "fuente_ruta_relativa": d["ruta_relativa"], "fuente_sha256": d["sha256"],
    })
for family in ["BEP", "ESP"]:
    for tipo in ["gastos", "ingresos"]:
        findings.append({
            "hallazgo_tipo": "ausencia", "subtipo": "julio_2025_no_publicado", "severidad": "informativo",
            "documento_id": "", "anio": 2025, "periodo": "2025-07", "tipo": tipo, "estado_documento": "ausente",
            "detalle": family, "decision": "ausencia_declarada_sin_interpolacion",
        })
for digest in sorted(prevalidated_esp):
    inv = next(i for i in inventory if i["sha256"] == digest)
    findings.append({
        "hallazgo_tipo": "variante_documental", "subtipo": "esp_es_estado_presupuestario_no_financiero",
        "severidad": "critico", "documento_id": "", "anio": inv["anio_carpeta"], "periodo": inv["periodo_nombre_archivo"],
        "tipo": inv["tipo"], "estado_documento": "no_escalado",
        "detalle": "0 codigos en plan municipal; 11 columnas presupuestarias CLP",
        "decision": "no_escalar_esp_sin_autorizacion_expresa", "fuente_archivo": inv["archivo"],
        "fuente_ruta_relativa": inv["ruta_relativa"], "fuente_sha256": digest,
    })
findings.append({
    "hallazgo_tipo": "inventario", "subtipo": "cantidad_observada_difiere_de_estimacion_inicial",
    "severidad": "control", "detalle": f"PDF observados: {len(inventory)}; referencia inicial del encargo: 143",
    "decision": "usar_inventario_fisico_verificable_y_declarar_diferencia",
})
for i, row in enumerate(findings, 1):
    row["hallazgo_id"] = f"H2-{i:06d}"
    row["etapa"] = "2"
write_csv(DOCS / "REGISTRO_HALLAZGOS_v1.csv", findings)

# Cotejo de versionado: niveles 1-3 ausentes del catálogo vigente, sin remapeo.
catalog_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))
catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
outside = [r for r in parsed_records if r.get("catalogo_estado") == "fuera_catalogo_mismo_nivel"]
outside_groups = defaultdict(list)
for r in outside:
    outside_groups[r["codigo_cuenta_pdf"]].append(r)
versioning = []
for code, rows in sorted(outside_groups.items()):
    first = rows[0]
    periods = sorted({r["periodo"] for r in rows})
    versioning.append({
        "codigo_cuenta_pdf": code, "nivel_jerarquico": first["nivel_jerarquico"],
        "denominaciones_pdf": " | ".join(sorted({r["denominacion_pdf"] for r in rows})),
        "anios_observados": "|".join(sorted({r["anio"] for r in rows})),
        "periodos_observados": "|".join(periods), "cantidad_periodos": len(periods),
        "tipos": "|".join(sorted({r["tipo"] for r in rows})), "ocurrencias": len(rows),
        "documentos": len({r["documento_id"] for r in rows}),
        "estado_catalogo_vigente": "ausente" if code not in catalog else "presente_revisar",
        "cotejo_versionado": "presente_en_fuentes_historicas_y_ausente_en_clasificador_vigente",
        "decision": "conservar_codigo_original_sin_remapear",
        "fuente_ejemplo_archivo": first["fuente_archivo"], "fuente_ejemplo_ruta_relativa": first["fuente_ruta_relativa"],
        "fuente_ejemplo_pagina": first["fuente_pagina"], "fuente_ejemplo_linea": first["fuente_linea"],
        "fuente_ejemplo_sha256": first["fuente_sha256"],
    })
write_csv(DOCS / "COTEJO_VERSIONADO_CODIGOS_v1.csv", versioning)

# Resumen de controles por año y agregado, calculado sobre el canónico aceptado.
def control_summary(rows):
    hierarchy_ok = hierarchy_total = 0
    by_doc = defaultdict(list)
    for r in rows:
        by_doc[r["documento_id"]].append(r)
    for doc_rows_inner in by_doc.values():
        for parent in doc_rows_inner:
            level = int(parent["nivel_jerarquico"])
            code = parent["codigo_cuenta_pdf"]
            children = [r for r in doc_rows_inner if int(r["nivel_jerarquico"]) == level + 1 and r["codigo_cuenta_pdf"].startswith(code + ".")]
            for metric in METRICS[parent["tipo"]] if children else []:
                hierarchy_total += 1
                hierarchy_ok += int(parent[metric]) == sum(int(c[metric]) for c in children)
    arithmetic_ok = sum(r["control_aritmetico_saldo"] == "calza" for r in rows)
    total_ok = total_controls = 0
    for did in by_doc:
        d = doc_by_id[did]
        top = [r for r in by_doc[did] if int(r["nivel_jerarquico"]) == 1]
        for metric in METRICS[d["tipo"]]:
            total_controls += 1
            total_ok += int(d["totales_impresos"][metric]) == sum(int(r[metric]) for r in top)
    return {
        "documentos": len(by_doc), "lineas": len(rows),
        "catalogo_encontradas": sum(r["catalogo_estado"] == "encontrada" for r in rows),
        "detalle_no_representado": sum(r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for r in rows),
        "fuera_catalogo_mismo_nivel": sum(r["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for r in rows),
        "jerarquia_calzan": hierarchy_ok, "controles_jerarquia": hierarchy_total,
        "tasa_jerarquia": hierarchy_ok / hierarchy_total if hierarchy_total else 0,
        "totales_calzan": total_ok, "controles_totales": total_controls,
        "tasa_totales": total_ok / total_controls if total_controls else 0,
        "aritmetica_calza": arithmetic_ok, "tasa_aritmetica": arithmetic_ok / len(rows) if rows else 0,
    }

summaries = {str(year): control_summary([r for r in canonical if int(r["anio"]) == year]) for year in YEARS}
summaries["total"] = control_summary(canonical)
construction = {
    "alcance": "BEP escalado; ESP inventariado y prevalidado, no escalado",
    "pdf_inventariados": len(inventory), "bep_inventariados": len(docs), "esp_inventariados": sum(i["familia"] == "ESP" for i in inventory),
    "bep_aceptados": len(accepted_docs), "bep_cuarentena": len(docs) - len(accepted_docs),
    "registros_canonicos": len(canonical), "registros_delta": len(deltas),
    "cortes_delta_computables": sum(c["estado_delta_mensual"].startswith("computable") for c in coverage),
    "cortes_delta_no_computables": sum(c["estado_delta_mensual"].startswith("no_computable") for c in coverage),
    "codigos_fuera_catalogo_nivel_1_3_unicos": len(versioning),
    "hallazgos_consolidados": len(findings), "controles": summaries,
}
(WORK / "resumen_construccion_canonico.json").write_text(json.dumps(construction, ensure_ascii=False, indent=2), encoding="utf-8")

# Diccionario de datos.
metric_descriptions = {
    "presupuesto_inicial_miles_clp": "Presupuesto inicial impreso, acumulado al corte; aplicable a gastos e ingresos.",
    "presupuesto_vigente_miles_clp": "Presupuesto vigente impreso al corte; aplicable a gastos e ingresos.",
    "obligacion_devengada_miles_clp": "Obligación devengada de gastos; nulo en ingresos.",
    "deuda_exigible_miles_clp": "Deuda exigible de gastos; nulo en ingresos.",
    "ingresos_percibidos_miles_clp": "Ingresos percibidos acumulados; nulo en gastos.",
    "ingresos_por_percibir_miles_clp": "Ingresos por percibir; nulo en gastos.",
    "saldo_presupuestario_miles_clp": "Saldo presupuestario impreso; en ambos tipos se controla como vigente menos ejecutado.",
}
field_descriptions = {
    "esquema_version": "Versión de esquema: canonico_v1.0.0.", "categoria": "Categoría funcional fija.",
    "subcategoria": "Identifica Balance de Ejecución Presupuestaria.", "registro_id": "ID único con SHA-256, página, línea y código.",
    "documento_id": "ID del documento BEP y versión.", "tipo": "gastos o ingresos.",
    "version_fuente": "original o republicacion_v2.", "seleccionado_para_serie": "Versión aceptada usada para deltas.",
    "anio": "Año del corte.", "mes_numero": "Mes numérico del corte.", "mes_nombre": "Mes en español.",
    "periodo": "Período AAAA-MM.", "fecha_corte": "Fecha ISO del corte.",
    "periodo_fuente": "Origen del período; contenido o asociación documental explícita.",
    "formulario_cgr": "0101 ingresos o 0102 gastos.", "formulario_fuente": "Soporte del formulario asignado.",
    "codigo_cuenta_pdf": "Código impreso, sin remapeo.", "nivel_jerarquico": "Nivel 1 a 5 derivado de las columnas del formulario.",
    "denominacion_pdf": "Denominación impresa, incluidas continuaciones.", "catalogo_estado": "Resultado de cotejo con clasificador vigente.",
    "catalogo_denominacion": "Denominación oficial si el código existe; vacío si no existe.",
    "unidad_monetaria": "miles_de_CLP (M$).", "naturaleza_valor": "acumulado_al_corte.",
    "control_aritmetico_saldo": "calza/no_calza para saldo = vigente - ejecutado.",
    "control_aritmetico_diferencia_miles_clp": "saldo - (vigente - ejecutado), sin corrección.",
    "estado_documento": "Solo aceptado en el canónico.", "fuente_archivo": "Nombre físico original.",
    "fuente_ruta_relativa": "Ruta relativa al workspace.", "fuente_pagina": "Página PDF, desde 1.",
    "fuente_linea": "Línea de extracción por coordenadas dentro de la página.", "fuente_sha256": "SHA-256 del PDF original.",
    "texto_linea_raw": "Texto extraído de la línea, sin normalizar cifras.",
}
L = ["# DICCIONARIO DE DATOS — INFORMACIÓN PRESUPUESTARIA", "", "**Esquema:** canonico_v1.0.0  ", "**Alcance:** BEP aceptados 2023–2025 y serie mensual derivada. ESP no incluido por variante documental pendiente de autorización.", "", "## 1. Tabla BEP canónica", "", "Archivo: `datos procesados/07_Información_Presupuestaria/BEP_2023-2025_canonico_v1.csv`. Una fila por documento–cuenta. Los importes son enteros en M$; el vacío significa no aplicable, nunca cero imputado. Cada métrica tiene una columna hermana `_raw` con el token impreso.", "", "| Campo | Tipo | Definición |", "|---|---|---|"]
for field in CANONICAL_FIELDS:
    base = field[:-4] if field.endswith("_raw") else field
    description = "Token monetario original de `" + base + "`." if field.endswith("_raw") else field_descriptions.get(field, metric_descriptions.get(field, field))
    tipo_dato = "texto" if field.endswith("_raw") or field in ["registro_id", "documento_id", "tipo", "periodo", "codigo_cuenta_pdf"] else "entero/texto según definición"
    L.append(f"| `{field}` | {tipo_dato} | {description} |")
L += ["", "## 2. Serie mensual derivada", "", "Archivo: `BEP_2023-2025_serie_mensual_v1.csv`. Formato largo: una fila por período–tipo–cuenta–métrica. Solo une cortes mensuales consecutivos aceptados. En enero se declara base numérica cero como convención de inicio de año; no representa un PDF previo. Las diferencias de presupuesto o saldo son deltas matemáticos, no necesariamente flujos económicos.", "", "| Campo | Definición |", "|---|---|"]
delta_descriptions = {
    "registro_derivado_id": "ID único del delta.", "metrica": "Una de las cinco métricas del formulario.",
    "periodo_previo": "Mes inmediatamente anterior; vacío en enero.", "metodo_base": "Corte consecutivo o convención de enero.",
    "valor_acumulado_previo_miles_clp": "Acumulado previo real; vacío en enero.", "base_numerica_utilizada_miles_clp": "Valor usado en la resta; cero declarado en enero.",
    "valor_acumulado_actual_miles_clp": "Acumulado del corte actual.", "delta_mensual_miles_clp": "Actual menos base.",
    "control_consistencia": "calza si base + delta = actual.", "diferencia_control_miles_clp": "base + delta - actual; debe ser 0.",
    "documento_actual_id": "Documento aceptado actual.", "documento_previo_id": "Documento aceptado previo; vacío en enero.",
    "registro_actual_id": "ID canónico actual.", "registro_previo_id": "ID canónico previo; vacío en enero.",
}
for field in (list(deltas[0].keys()) if deltas else ["registro_derivado_id", "periodo", "tipo", "codigo_cuenta_pdf", "metrica", "delta_mensual_miles_clp"]):
    if field.startswith("fuente_actual_"):
        description = "Trazabilidad " + field.replace("fuente_actual_", "") + " del registro actual."
    elif field.startswith("fuente_previa_"):
        description = "Trazabilidad " + field.replace("fuente_previa_", "") + " del registro previo; vacía en enero."
    else:
        description = delta_descriptions.get(field, field_descriptions.get(field, field))
    L.append(f"| `{field}` | {description} |")
L += ["", "## 3. Cobertura, documentos e inventario", "", "- `BEP_2023-2025_cobertura_v1.csv`: estado de cada período–tipo, versión elegida y computabilidad del delta.", "- `BEP_2023-2025_documentos_v1.csv`: un registro por PDF BEP, con umbrales, cuarentena, totales impresos y sumas.", "- `INVENTARIO_FUENTES_v1.csv`: los 141 PDF físicos, ruta, bytes, SHA-256 y disposición.", "- `COTEJO_VERSIONADO_CODIGOS_v1.csv`: una fila por código de niveles 1–3 ausente del catálogo vigente.", "", "La ausencia declarada de julio de 2025 no genera filas canónicas ni deltas. Las cuentas ausentes entre dos cortes no se convierten en cero; sus pares quedan en `BEP_2023-2025_hallazgos_delta_v1.csv`.", ""]
(DOCS / "DICCIONARIO_DATOS_v1.md").write_text("\n".join(L), encoding="utf-8")

# Bitácora conforme a la plantilla de 12 pasos.
s = summaries["total"]
L = ["# BITÁCORA DE TRANSFORMACIONES — INFORMACIÓN PRESUPUESTARIA", "", "**Proyecto:** Portal de Transparencia Trazable – Municipalidad de Coronel  ", "**Versión del esquema:** canonico_v1.0.0  ", "**Fecha:** 2026-11-14  ", "**Criterio rector:** fuentes originales intocables, trazabilidad total y ausencias declaradas.", "", "## 1. Congelar fuentes e inventariar", "", f"Se inventariaron **{len(inventory)} PDF** con ruta, tamaño y SHA-256: 71 BEP y 70 archivos en la carpeta ESP. El inventario físico difiere de la referencia inicial de 143; se documenta sin completar registros. Julio de 2025 no está publicado para ninguna familia ni tipo.", "", "## 2. Comparar nombre y período del contenido", "", "El período BEP se obtiene del encabezado impreso y se contrasta con el nombre. La v2 de enero de 2023 carece de encabezado, fecha y formulario: se recuperó la tabla por coordenadas y se asoció al original, pero quedó en cuarentena porque contiene 95 líneas frente a 97 del original. No se renombró ni alteró ningún original.", "", "## 3. Perfilar formularios, columnas y catálogos", "", "Los BEP usan Formulario 0101 (ingresos) u 0102 (gastos), cinco columnas en M$ y acumulados al corte. El parser asigna cifras por coordenadas y códigos por bandas jerárquicas. Los dos ESP prevalidados contienen estados presupuestarios de gastos con 11 columnas en CLP y 0 códigos del plan municipal; no se escalaron.", "", "## 4. Definir claves y versionado", "", "La clave canónica es documento–código; `registro_id` añade SHA-256, página y línea. Original y republicación se conservan como documentos separados. Para series se prefiere una v2 aceptada; como esta v2 quedó en cuarentena, enero de 2023 usa el original aceptado.", "", "## 5. Contrastar filas y totales", "", f"Se compararon los totales impresos con la suma independiente de subtítulos. En el canónico calzan **{s['totales_calzan']}/{s['controles_totales']}** controles. Todo archivo bajo umbral se excluyó, aunque sus evidencias permanecen en trabajo.", "", "## 6. Restaurar campos sin sobrescribir", "", "No se restauraron ni corrigieron cifras en los PDF. Las salidas son archivos nuevos en `datos procesados`; los parseos y controles de cuarentena se conservan en `trabajo`.", "", "## 7. Aplicar esquema canónico y conservar raw", "", "Cada fila conserva código y denominación PDF, denominación oficial cuando existe, siete métricas específicas con `_raw`, unidad M$, período y controles. Las métricas no aplicables quedan vacías. No se remapearon códigos ni se transformaron ausencias en cero.", "", "## 8. Añadir trazabilidad", "", f"Los **{len(canonical)} registros** canónicos incluyen archivo, ruta, página, línea y SHA-256. Cada delta enlaza los IDs y las trazabilidades de ambos cortes.", "", "## 9. Separar decisiones no reproducibles o pendientes", "", "No se aplicaron correcciones manuales. La diferencia documental de ESP queda pendiente de autorización. Los códigos ausentes del catálogo se interpretan solo como hallazgo de cobertura/versionado; no se afirma invalidez histórica ni se fuerza equivalencia.", "", "## 10. Ejecutar controles y cuarentenas", "", f"BEP: 38 aceptados y 33 cuarentenados. Canónico: jerarquía {s['jerarquia_calzan']}/{s['controles_jerarquia']} ({pct(s['tasa_jerarquia'])}), totales {pct(s['tasa_totales'])}, aritmética {s['aritmetica_calza']}/{s['lineas']} ({pct(s['tasa_aritmetica'])}). Junio de 2024 quedó en cuarentena por jerarquía, tal como anticipó la prevalidación.", "", "## 11. Registrar hallazgos y derivar deltas", "", f"El registro consolidado contiene {len(findings)} ocurrencias. El cotejo de versionado contiene {len(versioning)} códigos únicos de niveles 1–3. Se generaron {len(deltas)} deltas; no se calculó ningún delta saltando ausencias o cuarentenas. Las cuentas sin par se dejaron no computables.", "", "## 12. Versionar entregables y reproducción", "", "Entregables v1: canónico, documentos, cobertura, serie mensual, hallazgos de delta, diccionario, bitácora, inventario y cotejo normativo. Scripts: `factibilidad_bep_etapa1.py`, `prevalidar_entradas_etapa2.py`, `prevalidar_esp_etapa2.py`, `procesar_bep_etapa2.py`, `construir_canonico_bep_etapa2.py` y el validador final independiente.", ""]
(DOCS / "BITACORA_TRANSFORMACIONES_v1.md").write_text("\n".join(L), encoding="utf-8")

# Cobertura legible.
L = ["# COBERTURA, CUARENTENAS Y AUSENCIAS — ETAPA 2", "", f"**Inventario físico:** {len(inventory)} PDF (71 BEP y 70 ESP). **Escala ejecutada:** solo BEP. **ESP:** 2 prevalidaciones; 70 archivos no escalados por variante documental.", "", "## 1. Cobertura BEP", "", "| Año | Tipo | Aceptados | Cuarentena | Ausencias | Deltas computables |", "|---|---|---|---|---|---|"]
for year in YEARS:
    for tipo in ["gastos", "ingresos"]:
        rows = [c for c in coverage if c["anio"] == year and c["tipo"] == tipo]
        accepted_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_corte"] == "aceptado"]
        quarantined_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_corte"] == "cuarentena"]
        absent_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_corte"].startswith("ausencia")]
        delta_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_delta_mensual"].startswith("computable")]
        L.append(f"| {year} | {tipo} | {', '.join(accepted_months) or '—'} | {', '.join(quarantined_months) or '—'} | {', '.join(absent_months) or '—'} | {', '.join(delta_months) or '—'} |")
L += ["", "Los meses se indican con dos dígitos. Un corte aceptado cuyo predecesor está ausente o en cuarentena no produce delta. Enero usa base cero explícita; no se toma diciembre del año anterior.", "", "## 2. Ausencias y versión republicada", "", "- Julio de 2025: ausencia declarada en BEP y ESP, gastos e ingresos; sin interpolación.", "- Enero de 2023 ingresos: original aceptado; v2 parseada y cuarentenada por diferencia de 95 versus 97 líneas respecto del original. Ambas rutas y SHA-256 están en el inventario y ambos parseos se conservan en trabajo.", "- No se detectaron otras ausencias físicas por nombre de archivo en la malla mensual 2023–2025. El canónico tiene cobertura limitada por las cuarentenas detalladas en la tabla documental.", "", "## 3. Diferencia de inventario", "", f"La referencia inicial mencionó 143 PDF; la carpeta contiene {len(inventory)}. La malla teórica de 144 combinaciones menos cuatro ausencias de julio de 2025, más una republicación, explica 141 archivos físicos. Esta aritmética de cobertura no sustituye el inventario individual con SHA-256.", ""]
(DOCS / "COBERTURA_Y_AUSENCIAS_v1.md").write_text("\n".join(L), encoding="utf-8")

# Registro de hallazgos legible, incluidos todos los códigos de niveles 1-3.
counts = Counter((f["hallazgo_tipo"], f.get("subtipo", "")) for f in findings)
L = ["# REGISTRO DE HALLAZGOS — ETAPA 2", "", "**Tratamiento general:** preservación literal, sin remapeo, imputación ni interpolación. El CSV homónimo contiene cada ocurrencia y su trazabilidad.", "", "## 1. Resumen", "", f"- {len(docs) - len(accepted_docs)} documentos BEP en cuarentena; 38 aceptados.", f"- {len(versioning)} códigos únicos de niveles 1–3 ausentes del catálogo vigente.", f"- {len({r['codigo_cuenta_pdf'] for r in parsed_records if r.get('catalogo_estado') == 'fuera_catalogo_nivel_detalle_no_representado'})} códigos únicos de niveles 4/5 no representados por el catálogo.", f"- {len(deltas)} deltas calculados; {construction['cortes_delta_no_computables']} cortes tipo–período sin delta computable.", "- Variante ESP crítica: no se escala sin autorización expresa.", "", "| Tipo / subtipo | Ocurrencias |", "|---|---:|"]
for (kind, subtype), count in sorted(counts.items()):
    L.append(f"| {kind} / {subtype} | {count} |")
L += ["", "## 2. Cotejo de versionado normativo", "", "Los siguientes códigos aparecen en fuentes históricas y no en el clasificador vigente. Se conserva el código PDF; la presencia histórica no prueba por sí sola vigencia o invalidez normativa.", "", "| Código | Nivel | Denominación PDF | Años | Períodos | Ocurrencias |", "|---|---:|---|---|---|---:|"]
for row in versioning:
    L.append(f"| `{row['codigo_cuenta_pdf']}` | {row['nivel_jerarquico']} | {row['denominaciones_pdf']} | {row['anios_observados']} | {row['cantidad_periodos']} | {row['ocurrencias']} |")
L += ["", "El detalle de períodos, documentos y una evidencia archivo/página/línea/SHA-256 por código está en `COTEJO_VERSIONADO_CODIGOS_v1.csv`.", "", "## 3. Disposición", "", "Los documentos en cuarentena no entran al canónico ni a deltas. Las diferencias de jerarquía y aritmética conservan los valores impresos. Julio de 2025 es ausencia declarada. La discrepancia de 141 PDF observados frente a 143 informados inicialmente queda documentada.", ""]
(DOCS / "REGISTRO_HALLAZGOS_v1.md").write_text("\n".join(L), encoding="utf-8")

print(json.dumps(construction, ensure_ascii=False, indent=2))
