from pathlib import Path
from collections import defaultdict
import csv
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "esp_etapa2"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "descuadre_esp_ingresos"
OUT.mkdir(parents=True, exist_ok=True)
YEARS = [2023, 2024, 2025]
METRICS = [
    "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
    "presupuesto_vigente_mes_clp", "ingreso_devengado_clp", "ingreso_percibido_clp",
    "ingreso_por_percibir_clp", "saldo_por_devengar_clp", "saldo_por_percibir_clp",
]


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def integer_rows(rows):
    result = []
    for row in rows:
        item = dict(row)
        for metric in METRICS:
            item[metric] = int(item[metric])
        item["nivel_jerarquico"] = int(item["nivel_jerarquico"])
        result.append(item)
    return result


summaries, reconstruction, anomalies, exact_matches, top_detail = [], [], [], [], []
for year in YEARS:
    did = f"ESP_{year}-12_INGRESOS_ORIGINAL"
    records = integer_rows([r for r in read_csv(WORK / str(year) / f"esp_{year}_parseado.csv") if r["documento_id"] == did])
    totals_rows = [r for r in read_csv(WORK / str(year) / f"esp_{year}_validacion_totales.csv") if r["documento_id"] == did]
    printed = {r["metrica"]: int(r["total_impreso"]) for r in totals_rows}
    total_trace = next(r for r in totals_rows if r["metrica"] == "saldo_por_percibir_clp")
    top = [r for r in records if r["nivel_jerarquico"] == 1]
    top_detail.extend(top)
    sums = {m: sum(r[m] for r in top) for m in METRICS}
    discrepancy = printed["saldo_por_percibir_clp"] - sums["saldo_por_percibir_clp"]
    for metric in METRICS:
        reconstruction.append({
            "documento_id": did, "metrica": metric, "suma_subtitulos_nivel_1": sums[metric],
            "total_impreso_deudores": printed[metric], "diferencia_total_menos_suma": printed[metric] - sums[metric],
            "resultado": "calza" if printed[metric] == sums[metric] else "no_calza",
            "cantidad_subtitulos": len(top), "fuente_pagina_totales": total_trace["fuente_pagina_totales"],
            "fuente_linea_totales": total_trace["fuente_linea_totales"], "fuente_sha256": total_trace["fuente_sha256"],
        })
    doc_anomalies = []
    for r in records:
        expected_saldo_percibir = r["presupuesto_vigente_mes_clp"] - r["ingreso_percibido_clp"]
        diff_saldo = r["saldo_por_percibir_clp"] - expected_saldo_percibir
        expected_por_percibir = r["ingreso_devengado_clp"] - r["ingreso_percibido_clp"]
        diff_por_percibir = r["ingreso_por_percibir_clp"] - expected_por_percibir
        expected_saldo_devengar = r["presupuesto_vigente_mes_clp"] - r["ingreso_devengado_clp"]
        diff_devengar = r["saldo_por_devengar_clp"] - expected_saldo_devengar
        if diff_saldo or diff_por_percibir or diff_devengar:
            item = {
                "documento_id": did, "codigo_cuenta_pdf": r["codigo_cuenta_pdf"], "nivel_jerarquico": r["nivel_jerarquico"],
                "denominacion_pdf": r["denominacion_pdf"], "presupuesto_vigente_mes_clp": r["presupuesto_vigente_mes_clp"],
                "ingreso_devengado_clp": r["ingreso_devengado_clp"], "ingreso_percibido_clp": r["ingreso_percibido_clp"],
                "ingreso_por_percibir_clp": r["ingreso_por_percibir_clp"], "saldo_por_devengar_clp": r["saldo_por_devengar_clp"],
                "saldo_por_percibir_clp": r["saldo_por_percibir_clp"], "saldo_percibir_esperado": expected_saldo_percibir,
                "diferencia_saldo_percibir": diff_saldo, "diferencia_por_percibir": diff_por_percibir,
                "diferencia_saldo_devengar": diff_devengar, "texto_linea_raw": r["texto_linea_raw"],
                "fuente_archivo": r["fuente_archivo"], "fuente_ruta_relativa": r["fuente_ruta_relativa"],
                "fuente_pagina": r["fuente_pagina"], "fuente_linea": r["fuente_linea"], "fuente_sha256": r["fuente_sha256"],
            }
            anomalies.append(item)
            doc_anomalies.append(item)
    for r in records:
        for metric in METRICS:
            value = r[metric]
            if abs(value) == abs(discrepancy) or abs(r["presupuesto_vigente_mes_clp"] - r["ingreso_percibido_clp"]) == abs(discrepancy):
                exact_matches.append({
                    "documento_id": did, "diferencia_total_menos_suma": discrepancy, "codigo_cuenta_pdf": r["codigo_cuenta_pdf"],
                    "denominacion_pdf": r["denominacion_pdf"], "metrica_coincidente": metric, "valor": value,
                    "vigente_menos_percibido": r["presupuesto_vigente_mes_clp"] - r["ingreso_percibido_clp"],
                    "fuente_pagina": r["fuente_pagina"], "fuente_linea": r["fuente_linea"], "fuente_sha256": r["fuente_sha256"],
                })
    total_identity_diff = printed["saldo_por_percibir_clp"] - (printed["presupuesto_vigente_mes_clp"] - printed["ingreso_percibido_clp"])
    top_identity_diff_sum = sum(r["saldo_por_percibir_clp"] - (r["presupuesto_vigente_mes_clp"] - r["ingreso_percibido_clp"]) for r in top)
    # Prueba de signo: cambiar el signo de cada saldo impreso y medir si resuelve exactamente el descuadre.
    sign_candidates = []
    for r in records:
        value = r["saldo_por_percibir_clp"]
        for candidate in [value, -value]:
            if sums["saldo_por_percibir_clp"] - value + candidate == printed["saldo_por_percibir_clp"]:
                sign_candidates.append({"codigo": r["codigo_cuenta_pdf"], "valor_original": value, "valor_requerido": candidate})
    subtotal_candidates = [r["codigo_cuenta_pdf"] for r in records if r["saldo_por_percibir_clp"] == printed["saldo_por_percibir_clp"]]
    summaries.append({
        "documento_id": did, "archivo": records[0]["fuente_archivo"], "ruta_relativa": records[0]["fuente_ruta_relativa"],
        "sha256": records[0]["fuente_sha256"], "paginas_totales": total_trace["fuente_pagina_totales"],
        "linea_total": total_trace["fuente_linea_totales"], "lineas_detalle": len(records), "subtitulos_nivel_1": len(top),
        "diferencia_saldo_por_percibir": discrepancy, "totales_calzan": sum(printed[m] == sums[m] for m in METRICS),
        "total_identidad_diferencia": total_identity_diff, "suma_diferencias_identidad_nivel_1": top_identity_diff_sum,
        "anomalias_aritmeticas_todas_las_lineas": len(doc_anomalies),
        "anomalias_nivel_1": [a["codigo_cuenta_pdf"] for a in doc_anomalies if a["nivel_jerarquico"] == 1],
        "coincidencias_exactas_diferencia": len([m for m in exact_matches if m["documento_id"] == did]),
        "candidatos_cambio_signo": sign_candidates, "subtotales_iguales_al_total_saldo": subtotal_candidates,
        "totales_impresos": printed, "sumas_nivel_1": sums,
    })

write_csv(OUT / "reconstruccion_9_metricas_diciembre.csv", reconstruction)
write_csv(OUT / "anomalias_aritmeticas_diciembre.csv", anomalies)
write_csv(OUT / "coincidencias_exactas_diciembre.csv", exact_matches)
write_csv(OUT / "detalle_nivel_1_diciembre.csv", top_detail)
(OUT / "resumen_hipotesis_diciembre.json").write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summaries, ensure_ascii=False, indent=2))
