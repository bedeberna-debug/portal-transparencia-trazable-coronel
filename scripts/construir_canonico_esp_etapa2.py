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
MONTHS = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
MONTH_NAMES = [None, "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
ESP_METRICS = {
    "gastos": [
        "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
        "presupuesto_vigente_mes_clp", "obligacion_clp", "obligacion_devengada_clp", "pago_clp",
        "deuda_exigible_clp", "saldo_por_comprometer_clp", "saldo_por_devengar_clp", "saldo_por_pagar_clp",
    ],
    "ingresos": [
        "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
        "presupuesto_vigente_mes_clp", "ingreso_devengado_clp", "ingreso_percibido_clp",
        "ingreso_por_percibir_clp", "saldo_por_devengar_clp", "saldo_por_percibir_clp",
    ],
}
ALL_ESP_METRICS = list(dict.fromkeys(ESP_METRICS["gastos"] + ESP_METRICS["ingresos"]))
BEP_METRICS = {
    "gastos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "obligacion_devengada_miles_clp", "saldo_presupuestario_miles_clp", "deuda_exigible_miles_clp"],
    "ingresos": ["presupuesto_inicial_miles_clp", "presupuesto_vigente_miles_clp", "ingresos_percibidos_miles_clp", "saldo_presupuestario_miles_clp", "ingresos_por_percibir_miles_clp"],
}
ESP_BASE_FIELDS = [
    "esquema_version", "categoria", "subcategoria", "registro_id", "documento_id", "tipo_documental", "tipo",
    "version_fuente", "anio", "mes_numero", "mes_nombre", "periodo", "fecha_corte", "periodo_fuente",
    "formulario_cgr", "formulario_fuente", "codigo_cuenta_pdf", "nivel_jerarquico", "denominacion_pdf",
    "catalogo_estado", "catalogo_denominacion", "unidad_monetaria", "naturaleza_valor",
]
ESP_CANONICAL_FIELDS = list(ESP_BASE_FIELDS)
for metric in ALL_ESP_METRICS:
    ESP_CANONICAL_FIELDS.extend([metric, metric + "_raw"])
ESP_CANONICAL_FIELDS.extend([
    "identidad_aritmetica_principal", "control_aritmetico_principal", "control_aritmetico_diferencia_clp",
    "estado_documento", "politica_aceptacion", "nota_metodologica",
    "fuente_archivo", "fuente_ruta_relativa", "fuente_pagina", "fuente_linea",
    "fuente_sha256", "texto_linea_raw",
])


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def join(value):
    if isinstance(value, list):
        return "|".join(str(x) for x in value)
    return "" if value is None else str(value)


def month_from_name(name):
    lower = name.lower()
    return next((number for token, number in MONTHS.items() if re.search(rf"\b{token}\b", lower)), None)


def pct(value):
    return f"{100 * value:.2f} %".replace(".", ",")


def load_family(work, prefix, year):
    docs = json.loads((work / str(year) / f"documentos_{prefix}_{year}.json").read_text(encoding="utf-8"))
    records = read_csv(work / str(year) / f"{prefix}_{year}_parseado.csv")
    findings = read_csv(work / str(year) / f"{prefix}_{year}_hallazgos.csv")
    return docs, records, findings


bep_docs, bep_parsed, bep_findings = [], [], []
esp_docs, esp_parsed, esp_findings = [], [], []
for year in YEARS:
    d, r, f = load_family(BEP_WORK, "bep", year)
    bep_docs.extend(d); bep_parsed.extend(r); bep_findings.extend(f)
    d, r, f = load_family(ESP_WORK, "esp", year)
    esp_docs.extend(d); esp_parsed.extend(r); esp_findings.extend(f)
bep_by_id = {d["documento_id"]: d for d in bep_docs if d["documento_id"]}
esp_by_id = {d["documento_id"]: d for d in esp_docs if d["documento_id"]}
esp_accepted_ids = {d["documento_id"] for d in esp_docs if d["estado"] == "aceptado"}
bep_accepted_ids = {d["documento_id"] for d in bep_docs if d["estado"] == "aceptado"}

# Canónico ESP: gastos por umbrales estrictos e ingresos por control individual D-13.
esp_canonical = []
for rec in esp_parsed:
    did = rec["documento_id"]
    if did not in esp_accepted_ids:
        continue
    doc = esp_by_id[did]
    row = {
        "esquema_version": "canonico_v1.0.0", "categoria": "informacion_presupuestaria",
        "subcategoria": "estado_presupuestario", "registro_id": rec["registro_id"], "documento_id": did,
        "tipo_documental": doc["tipo_documental"], "tipo": rec["tipo"], "version_fuente": "original",
        "anio": rec["anio"], "mes_numero": rec["mes_numero"], "mes_nombre": MONTH_NAMES[int(rec["mes_numero"])],
        "periodo": rec["periodo"], "fecha_corte": rec["fecha_corte"], "periodo_fuente": "contenido",
        "formulario_cgr": "", "formulario_fuente": "no_identificado_en_contenido",
        "codigo_cuenta_pdf": rec["codigo_cuenta_pdf"], "nivel_jerarquico": rec["nivel_jerarquico"],
        "denominacion_pdf": rec["denominacion_pdf"], "catalogo_estado": rec["catalogo_estado"],
        "catalogo_denominacion": rec.get("catalogo_denominacion", ""), "unidad_monetaria": "CLP",
        "naturaleza_valor": "acumulado_al_corte", "identidad_aritmetica_principal": rec["identidad_aritmetica_principal"],
        "control_aritmetico_principal": rec["control_aritmetico_principal"],
        "control_aritmetico_diferencia_clp": rec["control_aritmetico_diferencia"],
        "estado_documento": doc["estado"],
        "politica_aceptacion": doc.get("politica_aceptacion") or "umbral_inicial_totales_100_jerarquia_95_aritmetica_99",
        "nota_metodologica": doc.get("nota_metodologica", ""), "fuente_archivo": rec["fuente_archivo"],
        "fuente_ruta_relativa": rec["fuente_ruta_relativa"], "fuente_pagina": rec["fuente_pagina"],
        "fuente_linea": rec["fuente_linea"], "fuente_sha256": rec["fuente_sha256"], "texto_linea_raw": rec["texto_linea_raw"],
    }
    for metric in ALL_ESP_METRICS:
        row[metric] = rec.get(metric, "")
        row[metric + "_raw"] = rec.get(metric + "_raw", "")
    esp_canonical.append(row)
esp_canonical.sort(key=lambda r: (r["periodo"], r["tipo"], r["codigo_cuenta_pdf"]))
write_csv(OUT / "ESP_2023-2025_canonico_v1.csv", esp_canonical, ESP_CANONICAL_FIELDS)

# Los dos valores legítimos del saldo por percibir se conservan sin sustituirse.
d13_controls = read_csv(OUT / "ESP_2023-2025_controles_D13_v1.csv")
d13_by_id = {r["documento_id"]: r for r in d13_controls}
esp_total_rows = []
for d in sorted(esp_docs, key=lambda x: x.get("periodo", "")):
    if d["tipo"] != "ingresos" or d["estado"] != "aceptado":
        continue
    c = d13_by_id[d["documento_id"]]
    row = {
        "esquema_version": "canonico_v1.0.0", "categoria": "informacion_presupuestaria",
        "subcategoria": "estado_presupuestario_totales", "documento_id": d["documento_id"],
        "tipo_documental": d["tipo_documental"], "tipo": "ingresos", "version_fuente": d["version_fuente"],
        "anio": d["anio"], "periodo": d["periodo"], "fecha_corte": d["fecha_corte"],
        "unidad_monetaria": "CLP", "naturaleza_valor": "acumulado_al_corte",
        "total_saldo_por_percibir_oficial_clp": c["total_saldo_por_percibir_oficial_clp"],
        "saldo_por_percibir_suma_detalle_clp": c["saldo_por_percibir_suma_detalle_clp"],
        "diferencia_oficial_menos_detalle_clp": c["diferencia_oficial_menos_detalle_clp"],
        "total_presupuesto_vigente_mes_clp": c["total_presupuesto_vigente_mes_clp"],
        "total_ingreso_percibido_clp": c["total_ingreso_percibido_clp"],
        "cuenta_15_presupuesto_vigente_mes_clp": c["cuenta_15_presupuesto_vigente_mes_clp"],
        "cuenta_15_ingreso_percibido_clp": c["cuenta_15_ingreso_percibido_clp"],
        "cuenta_15_vigente_menos_percibido_clp": c["cuenta_15_vigente_menos_percibido_clp"],
        "cuenta_15_saldo_por_percibir_impreso_clp": c["cuenta_15_saldo_por_percibir_impreso_clp"],
        "cuenta_15_saldo_por_percibir_raw": c["cuenta_15_saldo_por_percibir_raw"],
        "politica_aceptacion": d["politica_aceptacion"], "nota_metodologica": d["nota_metodologica"],
        "fuente_archivo": d["archivo"], "fuente_ruta_relativa": d["ruta_relativa"], "fuente_sha256": d["sha256"],
        "total_fuente_pagina": c["total_fuente_pagina"], "total_fuente_linea": c["total_fuente_linea"],
        "cuenta_15_registro_id": c["cuenta_15_registro_id"],
        "cuenta_15_fuente_pagina": c["cuenta_15_fuente_pagina"], "cuenta_15_fuente_linea": c["cuenta_15_fuente_linea"],
    }
    for metric in ESP_METRICS["ingresos"]:
        row["total_oficial_" + metric] = (d.get("totales_impresos") or {}).get(metric, "")
        row["suma_detalle_" + metric] = (d.get("sumas_subtitulos") or {}).get(metric, "")
    esp_total_rows.append(row)
write_csv(OUT / "ESP_2023-2025_totales_ingresos_v1.csv", esp_total_rows)

# Cobertura ESP completa; ingresos derivan deltas solo entre cortes consecutivos aceptados.
esp_coverage = []
for year in YEARS:
    for month in range(1, 13):
        period = f"{year}-{month:02d}"
        for tipo in ["gastos", "ingresos"]:
            period_docs = [d for d in esp_docs if d.get("periodo") == period and d.get("tipo") == tipo]
            accepted = [d for d in period_docs if d["estado"] == "aceptado"]
            quarantined = [d for d in period_docs if d["estado"] != "aceptado"]
            if not period_docs:
                state = "ausencia_declarada_no_publicado" if period == "2025-07" else "ausencia_detectada"
                reason = "julio_2025_no_publicado" if period == "2025-07" else "sin_pdf_en_fuente"
            elif accepted:
                state = "aceptado"
                reason = ""
            else:
                state = "cuarentena"
                reason = "|".join(sorted({m for d in quarantined for m in d.get("motivos_cuarentena", [])}))
            previous = f"{year}-{month-1:02d}" if month > 1 else None
            previous_accepted = previous and any(d.get("periodo") == previous and d.get("tipo") == tipo and d["estado"] == "aceptado" for d in esp_docs)
            derivada = "si" if accepted and tipo == "ingresos" else ("no_solicitada" if tipo == "gastos" else "no")
            if derivada == "si":
                delta_state = "computable_base_cero_convencion" if month == 1 else ("computable" if previous_accepted else "no_computable_corte_previo_ausente_o_cuarentena")
            else:
                delta_state = "no_computable"
            esp_coverage.append({
                "periodo": period, "anio": year, "mes_numero": month, "tipo": tipo, "estado_corte": state,
                "motivo_estado": reason, "documentos_inventariados": len(period_docs),
                "documentos_aceptados": len(accepted), "documentos_cuarentena": len(quarantined),
                "documento_canonico_id": accepted[0]["documento_id"] if accepted else "",
                "serie_mensual_derivada": derivada, "estado_delta_mensual": delta_state,
                "regla": "sin_interpolacion_sin_imputacion_sin_saltar_cortes",
            })
write_csv(OUT / "ESP_2023-2025_cobertura_v1.csv", esp_coverage)

# Tabla documental ESP con evidencia literal del título, política y ambos totales.
esp_doc_rows = []
for d in sorted(esp_docs, key=lambda x: (x.get("periodo", "9999"), x.get("tipo", ""), x["archivo"])):
    row = {k: join(v) for k, v in d.items() if k not in ["totales_impresos", "sumas_subtitulos", "titulo_evidencias", "diferencias_jerarquia_por_magnitud_clp", "control_d13"]}
    row["control_d13"] = json.dumps(d.get("control_d13", {}), ensure_ascii=False, separators=(",", ":")) if d["tipo"] == "ingresos" else ""
    row["en_canonico"] = "si" if d["documento_id"] in esp_accepted_ids else "no"
    row["diferencias_jerarquia_por_magnitud_clp"] = join(sorted(f"{k}:{v}" for k, v in (d.get("diferencias_jerarquia_por_magnitud_clp") or {}).items()))
    evidence = (d.get("titulo_evidencias") or [{}])[0]
    for field in ["tipo_documental_contenido", "titulo_literal_raw", "fuente_pagina", "fuente_linea"]:
        row["evidencia_titulo_" + field] = evidence.get(field, "")
    for metric in ALL_ESP_METRICS:
        row["total_impreso_" + metric] = (d.get("totales_impresos") or {}).get(metric, "")
        row["suma_subtitulos_" + metric] = (d.get("sumas_subtitulos") or {}).get(metric, "")
    c = d13_by_id.get(d["documento_id"], {})
    row["total_saldo_por_percibir_oficial_clp"] = c.get("total_saldo_por_percibir_oficial_clp", "")
    row["saldo_por_percibir_suma_detalle_clp"] = c.get("saldo_por_percibir_suma_detalle_clp", "")
    row["diferencia_oficial_menos_detalle_clp"] = c.get("diferencia_oficial_menos_detalle_clp", "")
    esp_doc_rows.append(row)
write_csv(OUT / "ESP_2023-2025_documentos_v1.csv", esp_doc_rows)

# Inventario físico completo y disposición actual de los 141 PDF.
bep_by_sha = {d["sha256"]: d for d in bep_docs}
esp_by_sha = {d["sha256"]: d for d in esp_docs}
inventory = []
for path in sorted(RAW.rglob("*.pdf"), key=lambda p: str(p.relative_to(ROOT)).lower()):
    rel = str(path.relative_to(ROOT))
    digest = sha256(path)
    family = "BEP" if "Balance de Ejecución Presupuestaria" in rel else "ESP"
    year = next((int(part) for part in path.parts if part in {"2023", "2024", "2025"}), "")
    month = month_from_name(path.stem)
    tipo = "gastos" if "gasto" in path.name.lower() else "ingresos"
    version = "republicacion_v2" if "v2" in path.stem.lower() else "original"
    doc = (bep_by_sha if family == "BEP" else esp_by_sha).get(digest)
    inventory.append({
        "familia": family, "anio_carpeta": year, "mes_nombre_archivo": month or "",
        "periodo_nombre_archivo": f"{year}-{month:02d}" if year and month else "", "tipo": tipo,
        "version_fuente": version, "archivo": path.name, "ruta_relativa": rel, "bytes": path.stat().st_size,
        "sha256": digest, "documento_id": doc["documento_id"] if doc else "",
        "periodo_contenido": doc.get("periodo", "") if doc else "",
        "tipo_documental_contenido": doc.get("tipo_documental", "BALANCE DE EJECUCION PRESUPUESTARIA") if doc else "",
        "estado_procesamiento": doc["estado"] if doc else "no_procesado",
        "motivo_estado": join(doc.get("motivos_cuarentena")) if doc else "",
    })
write_csv(DOCS / "INVENTARIO_FUENTES_v1.csv", inventory)

# Cotejo normativo ESP separado; no se remapea ningún código.
catalog_rows = json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))
catalog = {r["RUTA_JERARQUICA"]: r for r in catalog_rows}
outside_groups = defaultdict(list)
for r in esp_parsed:
    if r.get("catalogo_estado") == "fuera_catalogo_mismo_nivel":
        outside_groups[r["codigo_cuenta_pdf"]].append(r)
esp_versioning = []
for code, rows in sorted(outside_groups.items()):
    first = rows[0]
    periods = sorted({r["periodo"] for r in rows})
    esp_versioning.append({
        "familia": "ESP", "codigo_cuenta_pdf": code, "nivel_jerarquico": first["nivel_jerarquico"],
        "denominaciones_pdf": " | ".join(sorted({r["denominacion_pdf"] for r in rows})),
        "anios_observados": "|".join(sorted({r["anio"] for r in rows})), "periodos_observados": "|".join(periods),
        "cantidad_periodos": len(periods), "tipos": "|".join(sorted({r["tipo"] for r in rows})),
        "ocurrencias": len(rows), "documentos": len({r["documento_id"] for r in rows}),
        "estado_catalogo_vigente": "ausente" if code not in catalog else "presente_revisar",
        "cotejo_versionado": "presente_en_fuentes_historicas_y_ausente_en_clasificador_vigente",
        "decision": "conservar_codigo_original_sin_remapear", "fuente_ejemplo_archivo": first["fuente_archivo"],
        "fuente_ejemplo_ruta_relativa": first["fuente_ruta_relativa"], "fuente_ejemplo_pagina": first["fuente_pagina"],
        "fuente_ejemplo_linea": first["fuente_linea"], "fuente_ejemplo_sha256": first["fuente_sha256"],
    })
write_csv(DOCS / "COTEJO_VERSIONADO_CODIGOS_ESP_v1.csv", esp_versioning)

# Registro consolidado reconstruido desde los parseos; no reutiliza textos de la versión anterior.
findings = []
bep_delta_findings = read_csv(OUT / "BEP_2023-2025_hallazgos_delta_v1.csv")
esp_delta_findings = read_csv(OUT / "ESP_2023-2025_hallazgos_delta_ingresos_v1.csv")
for family, source in [("BEP", bep_findings + bep_delta_findings), ("ESP", esp_findings + esp_delta_findings)]:
    for source_row in source:
        row = dict(source_row)
        row["familia"] = family
        doc = (bep_by_id if family == "BEP" else esp_by_id).get(row.get("documento_id", ""), {})
        row["anio"] = doc.get("anio", str(row.get("periodo", ""))[:4])
        row["periodo"] = row.get("periodo") or doc.get("periodo", "")
        row["tipo"] = row.get("tipo") or doc.get("tipo", "")
        row["version_fuente"] = row.get("version_fuente") or doc.get("version_fuente", "")
        row["estado_documento"] = doc.get("estado", row.get("estado_documento", ""))
        row["fuente_archivo"] = row.get("fuente_archivo") or row.get("fuente_archivo_actual") or doc.get("archivo", "")
        row["fuente_ruta_relativa"] = row.get("fuente_ruta_relativa") or row.get("fuente_ruta_relativa_actual") or doc.get("ruta_relativa", "")
        row["fuente_sha256"] = row.get("fuente_sha256") or row.get("fuente_sha256_actual") or doc.get("sha256", "")
        findings.append(row)
for c in d13_controls:
    findings.append({
        "familia": "ESP", "hallazgo_tipo": "regla_agregacion", "subtipo": "saldo_por_percibir_incluye_cuenta_15",
        "severidad": "metodologico", "documento_id": c["documento_id"], "anio": c["anio"], "periodo": c["periodo"],
        "tipo": "ingresos", "version_fuente": c["version_fuente"], "estado_documento": c["estado_documento_posterior"],
        "codigo_cuenta_pdf": "15", "detalle": f"Diferencia oficial menos detalle: {c['diferencia_oficial_menos_detalle_clp']} CLP; tres condiciones D-13: {c['resultado_control']}",
        "decision": c["politica_aceptacion"] or "permanece_en_cuarentena", "fuente_archivo": c["fuente_archivo"],
        "fuente_ruta_relativa": c["fuente_ruta_relativa"], "fuente_sha256": c["fuente_sha256"],
        "fuente_pagina": c["total_fuente_pagina"], "fuente_linea": c["total_fuente_linea"],
    })
for family, docs in [("BEP", bep_docs), ("ESP", esp_docs)]:
    for d in docs:
        if d["estado"] == "aceptado":
            continue
        findings.append({
            "familia": family, "hallazgo_tipo": "cuarentena", "subtipo": "documento_bajo_umbral_o_variante",
            "severidad": "control", "documento_id": d["documento_id"], "anio": d.get("anio", ""),
            "periodo": d.get("periodo", ""), "tipo": d.get("tipo", ""), "version_fuente": d.get("version_fuente", ""),
            "estado_documento": d["estado"], "detalle": join(d.get("motivos_cuarentena")),
            "decision": "excluir_de_canonico_conservar_en_trabajo", "fuente_archivo": d["archivo"],
            "fuente_ruta_relativa": d["ruta_relativa"], "fuente_sha256": d["sha256"],
        })
for family in ["BEP", "ESP"]:
    for tipo in ["gastos", "ingresos"]:
        findings.append({
            "familia": family, "hallazgo_tipo": "ausencia", "subtipo": "julio_2025_no_publicado",
            "severidad": "informativo", "documento_id": "", "anio": 2025, "periodo": "2025-07", "tipo": tipo,
            "estado_documento": "ausente", "detalle": family, "decision": "ausencia_declarada_sin_interpolacion",
        })
findings.append({
    "familia": "todas", "hallazgo_tipo": "inventario", "subtipo": "cantidad_observada_difiere_de_estimacion_inicial",
    "severidad": "control", "detalle": f"PDF observados: {len(inventory)}; referencia inicial del encargo: 143",
    "decision": "usar_inventario_fisico_verificable_y_declarar_diferencia",
})
for i, row in enumerate(findings, 1):
    row["hallazgo_id"] = f"H2-{i:06d}"
    row["etapa"] = "2"
write_csv(DOCS / "REGISTRO_HALLAZGOS_v1.csv", findings)

# Resúmenes de construcción (la validación independiente se ejecuta en otro script).
bep_canonical = read_csv(OUT / "BEP_2023-2025_canonico_v1.csv")
bep_deltas = read_csv(OUT / "BEP_2023-2025_serie_mensual_v1.csv")
bep_coverage = read_csv(OUT / "BEP_2023-2025_cobertura_v1.csv")
bep_versioning = read_csv(DOCS / "COTEJO_VERSIONADO_CODIGOS_v1.csv")

def accepted_summary(docs):
    selected = [d for d in docs if d["estado"] == "aceptado"]
    h_ok = sum(d["jerarquia_calzan"] for d in selected); h_n = sum(d["controles_jerarquia"] for d in selected)
    t_ok = sum(d["totales_calzan"] for d in selected); t_n = sum(d["controles_totales"] for d in selected)
    a_ok = sum(d["aritmetica_calza"] for d in selected); a_n = sum(d["lineas"] for d in selected)
    return {
        "documentos": len(selected), "lineas": a_n, "jerarquia_calzan": h_ok, "controles_jerarquia": h_n,
        "tasa_jerarquia": h_ok / h_n if h_n else 0, "totales_calzan": t_ok, "controles_totales": t_n,
        "tasa_totales": t_ok / t_n if t_n else 0, "aritmetica_calza": a_ok, "tasa_aritmetica": a_ok / a_n if a_n else 0,
    }

bep_summaries = {str(y): accepted_summary([d for d in bep_docs if d.get("anio") == y]) for y in YEARS}
bep_summaries["total"] = accepted_summary(bep_docs)
esp_summaries = {str(y): accepted_summary([d for d in esp_docs if d.get("anio") == y]) for y in YEARS}
esp_summaries["total"] = accepted_summary(esp_docs)
construction = {
    "pdf_inventariados": len(inventory),
    "bep": {"inventariados": len(bep_docs), "aceptados": len(bep_accepted_ids), "cuarentena": len(bep_docs) - len(bep_accepted_ids),
            "registros_canonicos": len(bep_canonical), "registros_delta": len(bep_deltas), "controles": bep_summaries},
    "esp": {"inventariados": len(esp_docs), "aceptados": len(esp_accepted_ids), "cuarentena": len(esp_docs) - len(esp_accepted_ids),
            "registros_canonicos": len(esp_canonical), "controles": esp_summaries,
            "gastos_aceptados": sum(d["estado"] == "aceptado" and d["tipo"] == "gastos" for d in esp_docs),
            "ingresos_aceptados": sum(d["estado"] == "aceptado" and d["tipo"] == "ingresos" for d in esp_docs)},
    "hallazgos_consolidados": len(findings), "codigos_versionado_bep": len(bep_versioning), "codigos_versionado_esp": len(esp_versioning),
}
(ESP_WORK / "resumen_construccion_canonico.json").write_text(json.dumps(construction, ensure_ascii=False, indent=2), encoding="utf-8")

# Diccionario de datos conjunto.
metric_descriptions = {
    "presupuesto_inicial_clp": "Presupuesto inicial impreso, en CLP.",
    "modificacion_presupuestaria_clp": "Modificaciones presupuestarias impresas, en CLP.",
    "presupuesto_vigente_clp": "Presupuesto vigente impreso, en CLP.",
    "presupuesto_vigente_mes_clp": "Presupuesto vigente al mes de corte, en CLP.",
    "obligacion_clp": "Obligaciones de gastos, en CLP; no aplicable a ingresos.",
    "obligacion_devengada_clp": "Obligaciones devengadas de gastos, en CLP; no aplicable a ingresos.",
    "pago_clp": "Pagos de gastos, en CLP; no aplicable a ingresos.",
    "deuda_exigible_clp": "Deuda exigible de gastos, en CLP; no aplicable a ingresos.",
    "saldo_por_comprometer_clp": "Saldo por comprometer de gastos, en CLP; no aplicable a ingresos.",
    "saldo_por_devengar_clp": "Saldo por devengar, en CLP; presente en gastos e ingresos.",
    "saldo_por_pagar_clp": "Saldo por pagar de gastos, en CLP; no aplicable a ingresos.",
    "ingreso_devengado_clp": "Ingreso devengado, en CLP; no aplicable a gastos.",
    "ingreso_percibido_clp": "Ingreso percibido, en CLP; no aplicable a gastos.",
    "ingreso_por_percibir_clp": "Ingreso por percibir, en CLP; no aplicable a gastos.",
    "saldo_por_percibir_clp": "Saldo por percibir de ingresos, en CLP; no aplicable a gastos.",
}
field_descriptions = {
    "esquema_version": "Versión canonico_v1.0.0.", "categoria": "Categoría informacion_presupuestaria.",
    "subcategoria": "estado_presupuestario; separado del BEP.", "registro_id": "ID único con SHA-256, página, línea y código.",
    "documento_id": "ID ESP por período y tipo.", "tipo_documental": "Título normalizado del contenido: Estado Presupuestario de Gastos o Ingresos.",
    "tipo": "gastos o ingresos.", "version_fuente": "original.", "anio": "Año del corte de contenido.",
    "mes_numero": "Mes numérico del corte.", "mes_nombre": "Mes en español.", "periodo": "Período AAAA-MM.",
    "fecha_corte": "Fecha ISO impresa en el título.", "periodo_fuente": "contenido.",
    "formulario_cgr": "Vacío: número de formulario no identificado en el contenido ESP.",
    "formulario_fuente": "Declaración de no identificación; no se infiere el número.", "codigo_cuenta_pdf": "Código impreso, sin remapeo.",
    "nivel_jerarquico": "Nivel derivado de los componentes del código.", "denominacion_pdf": "Denominación impresa con continuaciones.",
    "catalogo_estado": "Cotejo con clasificador.json, nunca con plan_municipal.json.",
    "catalogo_denominacion": "Denominación oficial si la ruta existe.", "unidad_monetaria": "CLP; no convertir a M$.",
    "naturaleza_valor": "acumulado_al_corte.", "identidad_aritmetica_principal": "saldo_comprometer en gastos; saldo_por_percibir en ingresos.",
    "control_aritmetico_principal": "calza/no_calza de la identidad principal.",
    "control_aritmetico_diferencia_clp": "Diferencia de la identidad principal, en CLP, sin corrección.",
    "estado_documento": "Solo aceptado en el canónico.", "fuente_archivo": "Nombre físico original.",
    "fuente_ruta_relativa": "Ruta relativa al workspace.", "fuente_pagina": "Página PDF desde 1.",
    "fuente_linea": "Línea de extracción por coordenadas.", "fuente_sha256": "SHA-256 del PDF original.",
    "texto_linea_raw": "Texto extraído de la línea sin normalizar cifras.",
}
L = ["# DICCIONARIO DE DATOS — INFORMACIÓN PRESUPUESTARIA", "", "**Esquema:** canonico_v1.0.0  ", "**Alcance:** BEP aceptados, serie mensual BEP y ESP aceptados como Estado Presupuestario separado. Las cuarentenas no integran los canónicos.", "", "## 1. Tabla BEP canónica y serie mensual", "", "- `BEP_2023-2025_canonico_v1.csv`: una fila por documento–cuenta; siete métricas en M$, cada una con `_raw`.", "- `BEP_2023-2025_serie_mensual_v1.csv`: formato largo período–tipo–cuenta–métrica. Solo cortes consecutivos aceptados; enero usa base cero como convención explícita. No se imputan cuentas ausentes ni se saltan ausencias o cuarentenas.", "- `BEP_2023-2025_documentos_v1.csv`: disposición, política de aceptación, totales impresos y sumas por PDF.", "- `BEP_2023-2025_cobertura_v1.csv`: 72 combinaciones período–tipo y computabilidad del delta.", "", "## 2. Tabla ESP canónica", "", "Archivo: `ESP_2023-2025_canonico_v1.csv`. Una fila por documento–cuenta, en CLP. Incluye la unión de 15 métricas: 11 de gastos y 9 de ingresos, con cinco comunes. Una métrica no aplicable queda vacía, tanto en valor como en `_raw`; nunca se rellena con cero.", "", "| Campo | Definición |", "|---|---|"]
for field in ESP_CANONICAL_FIELDS:
    description = "Token monetario original de `" + field[:-4] + "`." if field.endswith("_raw") else field_descriptions.get(field, metric_descriptions.get(field, field))
    L.append(f"| `{field}` | {description} |")
L += ["", "### Identidades aritméticas", "", "- Gastos, control principal: saldo por comprometer = presupuesto vigente al mes − obligación. Controles adicionales: vigente = inicial + modificación; exigible = devengado − pago; saldo por devengar = obligación − devengado; saldo por pagar = obligación − pago.", "- Ingresos, control principal: saldo por percibir = presupuesto vigente al mes − percibido. Controles adicionales: vigente = inicial + modificación; por percibir = devengado − percibido; saldo por devengar = vigente al mes − devengado. Estos controles se conservan en el parseo de trabajo, incluso para documentos en cuarentena.", "", "## 3. Cobertura, evidencias y versionado", "", "- `ESP_2023-2025_documentos_v1.csv`: 70 PDF, métricas, título literal con página/línea/SHA-256, totales y cuarentenas.", "- `ESP_2023-2025_cobertura_v1.csv`: 72 combinaciones período–tipo; julio de 2025 declarado sin datos.", "- `INVENTARIO_FUENTES_v1.csv`: 141 PDF físicos con ruta, bytes y SHA-256.", "- `COTEJO_VERSIONADO_CODIGOS_v1.csv` y `COTEJO_VERSIONADO_CODIGOS_ESP_v1.csv`: códigos históricos ausentes del clasificador vigente, sin remapeo.", "- `ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv`: anexo permanente de diferencias jerárquicas BEP.", "", "No se creó una serie mensual ESP porque no fue solicitada en la autorización de escala.", ""]
(DOCS / "DICCIONARIO_DATOS_v1.md").write_text("\n".join(L), encoding="utf-8")

# Bitácora conforme a los 12 pasos.
bs, es = bep_summaries["total"], esp_summaries["total"]
refined = [d for d in bep_docs if d.get("politica_aceptacion") == "refinada_tolerancia_jerarquia_2_miles_clp"]
L = ["# BITÁCORA DE TRANSFORMACIONES — INFORMACIÓN PRESUPUESTARIA", "", "**Proyecto:** Portal de Transparencia Trazable – Municipalidad de Coronel  ", "**Versión del esquema:** canonico_v1.0.0  ", "**Fecha:** 2026-11-14  ", "**Criterio rector:** fuentes originales intocables, trazabilidad total y ausencias declaradas.", "", "## 1. Congelar fuentes e inventariar", "", f"Se inventariaron **{len(inventory)} PDF** con ruta, tamaño y SHA-256: 71 BEP y 70 ESP. La referencia inicial de 143 difiere del inventario físico; no se completaron registros. Julio de 2025 no está publicado en ninguna familia ni tipo.", "", "## 2. Comparar nombre y período del contenido", "", "El período se obtiene del encabezado impreso y se contrasta con el nombre. La v2 BEP de enero de 2023 carece de encabezado: se asoció documentalmente al original, se conservó por separado y quedó en cuarentena por contenido distinto (95 versus 97 líneas). Los 70 ESP tienen fecha de corte y título en el contenido.", "", "## 3. Perfilar formularios, columnas y catálogos", "", "Los BEP usan Formulario 0101/0102, cinco columnas en M$. Los ESP son Estados Presupuestarios: gastos tiene 11 columnas e ingresos 9, todas en CLP. Se validaron contra `clasificador.json`; nunca contra `plan_municipal.json`. No se infirió un número de formulario para ESP.", "", "## 4. Definir claves y versionado", "", "La clave canónica es documento–código; `registro_id` añade SHA-256, página y línea. Original y republicación se conservan separados. Para la serie BEP de enero de 2023 se usa el original aceptado, no la v2 cuarentenada.", "", "## 5. Contrastar filas y totales", "", f"BEP aceptado: {bs['totales_calzan']}/{bs['controles_totales']} totales; ESP aceptado: {es['totales_calzan']}/{es['controles_totales']}. Los totales impresos se comparan con la suma independiente de subtítulos. Los 35 ESP de ingresos quedaron en cuarentena por un descuadre del total impreso de saldo por percibir y por aritmética <99 % en cada documento; las otras ocho métricas de totales calzan.", "", "## 6. Restaurar campos sin sobrescribir", "", "No se corrigieron cifras ni se modificaron PDF. Las salidas son archivos nuevos; los parseos y controles de cuarentena permanecen en `trabajo`.", "", "## 7. Aplicar esquema canónico y conservar raw", "", "BEP conserva siete métricas en M$; ESP conserva la unión de 15 métricas en CLP. Cada métrica tiene `_raw`. Los campos no aplicables quedan vacíos. No se remapearon códigos ni se imputaron ausencias.", "", "## 8. Añadir trazabilidad", "", f"El canónico BEP contiene {len(bep_canonical)} registros y el ESP {len(esp_canonical)}. Cada registro incluye archivo, ruta, página, línea y SHA-256. Cada delta BEP enlaza IDs y trazabilidad de ambos cortes. Cada ESP documenta además el título literal y su ubicación.", "", "## 9. Separar decisiones no reproducibles o pendientes", "", "No hubo correcciones manuales. Los códigos fuera del catálogo se conservan como hallazgo de cobertura/versionado. Los ESP se tratan como tipo documental nuevo y separado, conforme a la autorización expresa. No se derivó serie ESP.", "", "## 10. Ejecutar controles, tolerancia BEP y cuarentenas", "", f"BEP: {len(bep_accepted_ids)} aceptados y {len(bep_docs)-len(bep_accepted_ids)} en cuarentena. Se aplicó la política refinada a {len(refined)} gastos: totales 100 %, aritmética ≥99 % y cada diferencia jerárquica ≤2 M$; el anexo permanente conserva todas las diferencias. La verificación visual confirmó 10/10 líneas. Permanecen cuatro gastos y la v2 de ingresos en cuarentena.", "", f"ESP: {len(esp_accepted_ids)} aceptados y {len(esp_docs)-len(esp_accepted_ids)} en cuarentena, con umbrales estrictos por archivo. La tolerancia de 2 M$ no se aplicó a ESP.", "", "## 11. Registrar hallazgos y derivar deltas", "", f"El registro consolidado contiene {len(findings)} ocurrencias. El cotejo BEP contiene {len(bep_versioning)} códigos únicos y el ESP {len(esp_versioning)}. Se generaron {len(bep_deltas)} deltas BEP; no se saltaron ausencias ni cuarentenas. Julio de 2025 no genera datos ni interpolación.", "", "## 12. Versionar entregables y reproducción", "", "Entregables v1: canónicos BEP/ESP, documentos, coberturas, serie mensual BEP, hallazgos, diccionario, bitácora, inventario, cotejos, anexo jerárquico, verificación visual y validación final. Scripts principales: `procesar_bep_etapa2.py`, `aplicar_politica_refinada_bep.py`, `construir_canonico_bep_etapa2.py`, `procesar_esp_etapa2.py`, `construir_canonico_esp_etapa2.py` y `validar_final_etapa2.py`.", ""]
(DOCS / "BITACORA_TRANSFORMACIONES_v1.md").write_text("\n".join(L), encoding="utf-8")

# Cobertura legible y detalle de las cuarentenas.
L = ["# COBERTURA, CUARENTENAS Y AUSENCIAS — ETAPA 2", "", f"**Inventario físico:** {len(inventory)} PDF (71 BEP y 70 ESP). **BEP:** {len(bep_accepted_ids)} aceptados y {len(bep_docs)-len(bep_accepted_ids)} en cuarentena. **ESP:** {len(esp_accepted_ids)} aceptados y {len(esp_docs)-len(esp_accepted_ids)} en cuarentena.", "", "## 1. Cobertura BEP", "", "| Año | Tipo | Aceptados | Cuarentena | Ausencias | Deltas computables |", "|---|---|---|---|---|---|"]
for year in YEARS:
    for tipo in ["gastos", "ingresos"]:
        rows = [c for c in bep_coverage if c["anio"] == str(year) and c["tipo"] == tipo]
        accepted_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_corte"] == "aceptado"]
        quarantined_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_corte"] == "cuarentena"]
        absent_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_corte"].startswith("ausencia")]
        delta_months = [f"{int(c['mes_numero']):02d}" for c in rows if c["estado_delta_mensual"].startswith("computable")]
        L.append(f"| {year} | {tipo} | {', '.join(accepted_months) or '—'} | {', '.join(quarantined_months) or '—'} | {', '.join(absent_months) or '—'} | {', '.join(delta_months) or '—'} |")
L += ["", "## 2. Cobertura ESP", "", "| Año | Gastos aceptados | Ingresos aceptados | Ingresos en cuarentena | Ausencias por tipo |", "|---|---|---|---|---|"]
for year in YEARS:
    docs_y = [d for d in esp_docs if d.get("anio") == year]
    L.append(f"| {year} | {sum(d['estado']=='aceptado' and d['tipo']=='gastos' for d in docs_y)} | {sum(d['estado']=='aceptado' and d['tipo']=='ingresos' for d in docs_y)} | {sum(d['estado']!='aceptado' and d['tipo']=='ingresos' for d in docs_y)} | {'julio' if year == 2025 else '—'} |")
L += ["", "Los 35 ESP de gastos cumplen los umbrales. Cada ESP de ingresos tiene 8/9 totales calzantes; el total impreso de `saldo_por_percibir_clp` difiere de la suma de subtítulos y la aritmética queda bajo 99 %. Por ambos motivos, cada documento queda en cuarentena. No se corrigió ni toleró la diferencia.", "", "## 3. Cuarentenas BEP permanentes", "", "| Documento | Motivo |", "|---|---|"]
for d in bep_docs:
    if d["estado"] != "aceptado":
        L.append(f"| {d['documento_id']} | {join(d.get('motivos_cuarentena'))} |")
L += ["", "## 4. Ausencias, versión republicada e inventario", "", "- Julio de 2025: ausencia declarada en BEP y ESP, gastos e ingresos; sin interpolación.", "- Enero de 2023 ingresos BEP: original aceptado y v2 parseada/cuarentenada; ambas versiones se conservan con SHA-256.", f"- La referencia inicial mencionó 143 PDF; se observaron {len(inventory)}. La malla teórica de 144 combinaciones menos cuatro ausencias de julio de 2025, más una republicación, explica 141 archivos físicos.", ""]
(DOCS / "COBERTURA_Y_AUSENCIAS_v1.md").write_text("\n".join(L), encoding="utf-8")

# Registro legible; el CSV conserva todas las ocurrencias.
counts = Counter((f.get("familia", ""), f["hallazgo_tipo"], f.get("subtipo", "")) for f in findings)
L = ["# REGISTRO DE HALLAZGOS — ETAPA 2", "", "**Tratamiento general:** preservación literal, sin remapeo, imputación ni interpolación. El CSV homónimo contiene cada ocurrencia y su trazabilidad.", "", "## 1. Resumen", "", f"- BEP: {len(bep_accepted_ids)} aceptados; {len(bep_docs)-len(bep_accepted_ids)} en cuarentena.", f"- ESP: {len(esp_accepted_ids)} aceptados; {len(esp_docs)-len(esp_accepted_ids)} en cuarentena.", f"- Cotejo de versionado: {len(bep_versioning)} códigos BEP y {len(esp_versioning)} códigos ESP, sin remapeo.", f"- Serie BEP: {len(bep_deltas)} deltas; ausencias y cuarentenas interrumpen el cálculo.", "", "| Familia / tipo / subtipo | Ocurrencias |", "|---|---:|"]
for (family, kind, subtype), count in sorted(counts.items()):
    L.append(f"| {family} / {kind} / {subtype} | {count} |")
L += ["", "## 2. Hallazgo de tipo documental ESP", "", "Los 70 archivos de la carpeta denominada “Estado de Situación Financiera” contienen el título “ESTADO PRESUPUESTARIO DE GASTOS” o “ESTADO PRESUPUESTARIO DE INGRESOS”, no “Estado de Situación Financiera”. Se procesan como tipo documental separado `estado_presupuestario`, contra el clasificador presupuestario y en CLP. Cada documento conserva el título literal, página, línea y SHA-256 en `ESP_2023-2025_documentos_v1.csv` y en el CSV de hallazgos.", "", "## 3. Cuarentenas ESP de ingresos", "", "En los 35 documentos de ingresos, ocho de nueve totales calzan; `saldo_por_percibir_clp` presenta una diferencia entre el total impreso y la suma de subtítulos. Además, los 35 tienen aritmética <99 %. El detalle por documento, cifra y evidencia está en `ESP_2023-2025_documentos_v1.csv` y en los CSV de trabajo. Se excluyen del canónico por totales <100 % y aritmética <99 %.", "", "## 4. Política jerárquica BEP y verificación visual", "", f"La política refinada incorporó {len(refined)} documentos de gastos con diferencias exclusivamente ≤2 M$, totales 100 % y aritmética ≥99 %. El anexo permanente registra 975 diferencias de las 33 cuarentenas iniciales. La muestra visual confirmó 10/10 líneas y sus cinco cifras; no se modificó ningún valor. Permanen en cuarentena BEP_2023-08_GASTOS_ORIGINAL, BEP_2023-09_GASTOS_ORIGINAL, BEP_2023-11_GASTOS_ORIGINAL, BEP_2024-02_GASTOS_ORIGINAL y BEP_2023-01_INGRESOS_REPUBLICACION_V2.", "", "## 5. Cotejo de versionado normativo", "", "Los códigos históricos ausentes del clasificador vigente se conservan sin equivalencias forzadas. La presencia histórica no prueba por sí sola vigencia o invalidez normativa. Los 33 códigos de Etapa 1 siguen incluidos en el cotejo BEP; se añadieron `05.03.009` y `05.03.099`. Los detalles están en los dos CSV de cotejo.", "", "## 6. Disposición", "", "Las cuarentenas no entran a los canónicos. Las diferencias conservan los valores impresos. Julio de 2025 es ausencia declarada. La discrepancia de 141 PDF observados frente a 143 informados inicialmente queda documentada.", ""]
(DOCS / "REGISTRO_HALLAZGOS_v1.md").write_text("\n".join(L), encoding="utf-8")

print(json.dumps(construction, ensure_ascii=False, indent=2))
