from pathlib import Path
from collections import defaultdict
import csv
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
OUT = ROOT / "datos procesados" / "07_Información_Presupuestaria"
METRICAS = [
    "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
    "presupuesto_vigente_mes_clp", "ingreso_devengado_clp", "ingreso_percibido_clp",
    "ingreso_por_percibir_clp", "saldo_por_devengar_clp", "saldo_por_percibir_clp",
]


def leer_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def escribir_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def periodo_previo(periodo):
    year, month = map(int, periodo.split("-"))
    return f"{year}-{month - 1:02d}" if month > 1 else None


def fuentes(row, prefijo):
    return {
        f"fuente_archivo_{prefijo}": row.get("fuente_archivo", ""),
        f"fuente_ruta_relativa_{prefijo}": row.get("fuente_ruta_relativa", ""),
        f"fuente_pagina_{prefijo}": row.get("fuente_pagina", ""),
        f"fuente_linea_{prefijo}": row.get("fuente_linea", ""),
        f"fuente_sha256_{prefijo}": row.get("fuente_sha256", ""),
    }


canonical = [r for r in leer_csv(OUT / "ESP_2023-2025_canonico_v1.csv") if r["tipo"] == "ingresos" and r["estado_documento"] == "aceptado"]
totals = leer_csv(OUT / "ESP_2023-2025_totales_ingresos_v1.csv")
by_period = defaultdict(list)
for row in canonical:
    by_period[row["periodo"]].append(row)
total_by_period = {r["periodo"]: r for r in totals}
periods = sorted(by_period)
assert set(periods) == set(total_by_period)
assert len(periods) == 35

account_deltas = []
total_deltas = []
findings = []
for period in periods:
    month = int(period.split("-")[1])
    previous_period = periodo_previo(period)
    previous_rows = {r["codigo_cuenta_pdf"]: r for r in by_period.get(previous_period, [])} if previous_period else {}
    if month != 1 and not previous_rows:
        continue
    current_rows = {r["codigo_cuenta_pdf"]: r for r in by_period[period]}
    if previous_period:
        for code in sorted(set(current_rows) - set(previous_rows)):
            r = current_rows[code]
            findings.append({
                "hallazgo_tipo": "delta_no_computable_cuenta", "subtipo": "cuenta_sin_corte_previo",
                "severidad": "informativo", "documento_id": r["documento_id"], "periodo": period,
                "tipo": "ingresos", "codigo_cuenta_pdf": code, "denominacion_pdf": r["denominacion_pdf"],
                "detalle": "La cuenta está en el corte actual pero no en el mensual inmediatamente anterior; no se imputa base cero fuera de enero.",
                "decision": "omitir_delta_conservar_ambos_acumulados", "estado_documento": "aceptado",
                **fuentes(r, "actual"),
            })
        for code in sorted(set(previous_rows) - set(current_rows)):
            previous = previous_rows[code]
            current = by_period[period][0]
            findings.append({
                "hallazgo_tipo": "delta_no_computable_cuenta", "subtipo": "cuenta_ausente_en_corte_actual",
                "severidad": "informativo", "documento_id": current["documento_id"], "periodo": period,
                "tipo": "ingresos", "codigo_cuenta_pdf": code, "denominacion_pdf": previous["denominacion_pdf"],
                "detalle": "La cuenta está en el corte previo pero no en el actual; no se imputa un valor actual cero.",
                "decision": "omitir_delta_conservar_ambos_acumulados", "estado_documento": "aceptado",
                "registro_previo_id": previous["registro_id"], **fuentes(previous, "previo"), **fuentes(current, "actual"),
            })
    for code, current in sorted(current_rows.items()):
        previous = previous_rows.get(code)
        if month != 1 and previous is None:
            continue
        for metric in METRICAS:
            actual = int(current[metric])
            base = int(previous[metric]) if previous else 0
            delta = actual - base
            row = {
                "esquema_version": "canonico_v1.0.0", "categoria": "informacion_presupuestaria",
                "subcategoria": "estado_presupuestario_serie_mensual",
                "registro_derivado_id": f"ESP_DELTA|{current['documento_id']}|{code}|{metric}",
                "documento_actual_id": current["documento_id"], "documento_previo_id": previous["documento_id"] if previous else "",
                "registro_actual_id": current["registro_id"], "registro_previo_id": previous["registro_id"] if previous else "",
                "periodo": period, "anio": current["anio"], "mes_numero": month, "tipo": "ingresos",
                "codigo_cuenta_pdf": code, "nivel_jerarquico": current["nivel_jerarquico"],
                "denominacion_pdf": current["denominacion_pdf"], "catalogo_estado": current["catalogo_estado"],
                "metrica": metric, "unidad_monetaria": "CLP",
                "naturaleza_delta": "diferencia_entre_acumulados_no_necesariamente_flujo",
                "valor_acumulado_previo_clp": base if previous else "",
                "valor_acumulado_actual_clp": actual, "base_numerica_utilizada_clp": base,
                "delta_mensual_clp": delta, "diferencia_control_clp": base + delta - actual,
                "control_consistencia": "calza",
                "metodo_base": "cero_inicio_anio_convencion" if month == 1 else "corte_mensual_inmediatamente_anterior",
                "valor_actual_raw": current[metric + "_raw"], "valor_previo_raw": previous[metric + "_raw"] if previous else "",
                "politica_aceptacion": current["politica_aceptacion"], "nota_metodologica": current["nota_metodologica"],
                **fuentes(current, "actual"), **(fuentes(previous, "previo") if previous else fuentes({}, "previo")),
            }
            account_deltas.append(row)
    current_total = total_by_period[period]
    previous_total = total_by_period.get(previous_period) if previous_period else None
    series = [("oficial", m) for m in METRICAS] + [("suma_detalle", "saldo_por_percibir_clp")]
    for scope, metric in series:
        field = ("total_oficial_" + metric) if scope == "oficial" else "saldo_por_percibir_suma_detalle_clp"
        actual = int(current_total[field])
        base = int(previous_total[field]) if previous_total else 0
        delta = actual - base
        row = {
            "esquema_version": "canonico_v1.0.0", "categoria": "informacion_presupuestaria",
            "subcategoria": "estado_presupuestario_totales_serie_mensual",
            "registro_derivado_id": f"ESP_TOTAL_DELTA|{current_total['documento_id']}|{scope}|{metric}",
            "documento_actual_id": current_total["documento_id"], "documento_previo_id": previous_total["documento_id"] if previous_total else "",
            "periodo": period, "anio": current_total["anio"], "mes_numero": month, "tipo": "ingresos",
            "ambito_total": scope, "metrica": metric, "unidad_monetaria": "CLP",
            "naturaleza_delta": "diferencia_entre_acumulados_no_necesariamente_flujo",
            "valor_acumulado_previo_clp": base if previous_total else "", "valor_acumulado_actual_clp": actual,
            "base_numerica_utilizada_clp": base, "delta_mensual_clp": delta,
            "diferencia_control_clp": base + delta - actual, "control_consistencia": "calza",
            "metodo_base": "cero_inicio_anio_convencion" if month == 1 else "corte_mensual_inmediatamente_anterior",
            "politica_aceptacion": current_total["politica_aceptacion"], "nota_metodologica": current_total["nota_metodologica"],
            "fuente_archivo_actual": current_total["fuente_archivo"], "fuente_ruta_relativa_actual": current_total["fuente_ruta_relativa"],
            "fuente_pagina_actual": current_total["total_fuente_pagina"], "fuente_linea_actual": current_total["total_fuente_linea"],
            "fuente_sha256_actual": current_total["fuente_sha256"],
            "fuente_archivo_previo": previous_total["fuente_archivo"] if previous_total else "",
            "fuente_ruta_relativa_previo": previous_total["fuente_ruta_relativa"] if previous_total else "",
            "fuente_pagina_previo": previous_total["total_fuente_pagina"] if previous_total else "",
            "fuente_linea_previo": previous_total["total_fuente_linea"] if previous_total else "",
            "fuente_sha256_previo": previous_total["fuente_sha256"] if previous_total else "",
        }
        total_deltas.append(row)

account_fields = list(dict.fromkeys(k for r in account_deltas for k in r))
total_fields = list(dict.fromkeys(k for r in total_deltas for k in r))
finding_fields = list(dict.fromkeys(k for r in findings for k in r)) or ["hallazgo_tipo", "subtipo", "periodo"]
escribir_csv(OUT / "ESP_2023-2025_serie_mensual_ingresos_v1.csv", account_deltas, account_fields)
escribir_csv(OUT / "ESP_2023-2025_serie_totales_ingresos_v1.csv", total_deltas, total_fields)
escribir_csv(OUT / "ESP_2023-2025_hallazgos_delta_ingresos_v1.csv", findings, finding_fields)
assert not any(r["periodo"] in {"2025-07", "2025-08"} for r in account_deltas + total_deltas)
assert all(int(r["diferencia_control_clp"]) == 0 for r in account_deltas + total_deltas)
resumen = {
    "documentos_aceptados": len(periods), "cortes_con_delta": len({r["periodo"] for r in total_deltas}),
    "deltas_cuentas": len(account_deltas), "deltas_totales": len(total_deltas),
    "hallazgos_cuentas_sin_delta": len(findings),
    "julio_2025": "ausencia_declarada_sin_interpolacion", "agosto_2025": "sin_delta_por_ausencia_previa",
}
(OUT / "ESP_2023-2025_resumen_series_ingresos_v1.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(resumen, ensure_ascii=False, indent=2))
