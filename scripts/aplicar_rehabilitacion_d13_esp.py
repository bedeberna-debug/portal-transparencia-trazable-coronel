from pathlib import Path
import csv
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "esp_etapa2"
OUT = ROOT / "datos procesados" / "07_Información_Presupuestaria"
YEARS = [2023, 2024, 2025]
METRICAS = [
    "presupuesto_inicial_clp", "modificacion_presupuestaria_clp", "presupuesto_vigente_clp",
    "presupuesto_vigente_mes_clp", "ingreso_devengado_clp", "ingreso_percibido_clp",
    "ingreso_por_percibir_clp", "saldo_por_devengar_clp", "saldo_por_percibir_clp",
]
OTRAS_OCHO = [m for m in METRICAS if m != "saldo_por_percibir_clp"]
POLITICA = "D-13_rehabilitacion_condicionada_cuenta_15"
NOTA = (
    "El total oficial de saldo por percibir incluye el saldo inicial de caja (cuenta 15) "
    "por su presupuesto vigente al mes menos ingreso percibido; la suma del detalle conserva "
    "el saldo por percibir impreso en las líneas, incluidos los ceros de la cuenta 15. "
    "Ambos valores se conservan por separado; no se corrige ninguna cifra impresa."
)


def leer_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


controles = []
resumen = {"documentos_ingresos": 0, "rehabilitados": 0, "permanecen_cuarentena": 0}
for year in YEARS:
    folder = WORK / str(year)
    docs_path = folder / f"documentos_esp_{year}.json"
    docs = json.loads(docs_path.read_text(encoding="utf-8"))
    records = leer_csv(folder / f"esp_{year}_parseado.csv")
    totals = leer_csv(folder / f"esp_{year}_validacion_totales.csv")
    by_doc = {}
    for record in records:
        by_doc.setdefault(record["documento_id"], []).append(record)
    for doc in docs:
        if doc["tipo"] != "ingresos":
            continue
        resumen["documentos_ingresos"] += 1
        did = doc["documento_id"]
        rows = by_doc[did]
        cuenta15 = [r for r in rows if r["codigo_cuenta_pdf"] == "15"]
        if len(cuenta15) != 1:
            raise RuntimeError(f"{did}: se esperaba una cuenta 15 y se encontraron {len(cuenta15)}")
        c15 = cuenta15[0]
        printed = {t["metrica"]: int(t["total_impreso"]) for t in totals if t["documento_id"] == did}
        sums = {t["metrica"]: int(t["suma_subtitulos"]) for t in totals if t["documento_id"] == did}
        total_trace = next(t for t in totals if t["documento_id"] == did and t["metrica"] == "saldo_por_percibir_clp")
        diferencias_otras = {m: printed[m] - sums[m] for m in OTRAS_OCHO}
        condicion_1 = all(value == 0 for value in diferencias_otras.values())
        oficial = printed["saldo_por_percibir_clp"]
        detalle = sums["saldo_por_percibir_clp"]
        vigente_total = printed["presupuesto_vigente_mes_clp"]
        percibido_total = printed["ingreso_percibido_clp"]
        residual_2 = oficial - (vigente_total - percibido_total)
        condicion_2 = residual_2 == 0
        vigente_15 = int(c15["presupuesto_vigente_mes_clp"])
        percibido_15 = int(c15["ingreso_percibido_clp"])
        residual_3 = (oficial - detalle) - (vigente_15 - percibido_15)
        condicion_3 = residual_3 == 0
        elegible = condicion_1 and condicion_2 and condicion_3
        previous_reasons = list(doc.get("motivos_cuarentena_previos", doc.get("motivos_cuarentena", [])))
        doc["motivos_cuarentena_previos"] = previous_reasons
        doc["control_d13"] = {
            "condicion_1_otras_ocho_metricas": condicion_1,
            "condicion_2_identidad_total": condicion_2,
            "condicion_3_reconciliacion_cuenta_15": condicion_3,
            "residual_condicion_2_clp": residual_2,
            "residual_condicion_3_clp": residual_3,
            "diferencias_otras_ocho_metricas_clp": diferencias_otras,
        }
        if elegible:
            doc["estado"] = "aceptado"
            doc["politica_aceptacion"] = POLITICA
            doc["nota_metodologica"] = NOTA
            doc["motivos_cuarentena"] = []
            resumen["rehabilitados"] += 1
        else:
            doc["estado"] = "cuarentena"
            doc["politica_aceptacion"] = ""
            doc["nota_metodologica"] = ""
            doc["motivos_cuarentena"] = sorted(set(previous_reasons + ["D-13_condiciones_no_reproducidas"]))
            resumen["permanecen_cuarentena"] += 1
        controles.append({
            "decision_id": "D-13", "documento_id": did, "periodo": doc["periodo"], "anio": year,
            "tipo": "ingresos", "version_fuente": doc["version_fuente"],
            "condicion_1_otras_ocho_metricas": "calza" if condicion_1 else "no_calza",
            "condicion_1_metricas_calzan": sum(value == 0 for value in diferencias_otras.values()),
            "condicion_1_metricas_totales": 8,
            "condicion_1_diferencias_clp": json.dumps(diferencias_otras, ensure_ascii=False, separators=(",", ":")),
            "condicion_2_identidad_total": "calza" if condicion_2 else "no_calza",
            "total_saldo_por_percibir_oficial_clp": oficial,
            "total_presupuesto_vigente_mes_clp": vigente_total,
            "total_ingreso_percibido_clp": percibido_total,
            "condicion_2_residual_clp": residual_2,
            "condicion_3_reconciliacion_cuenta_15": "calza" if condicion_3 else "no_calza",
            "saldo_por_percibir_suma_detalle_clp": detalle,
            "diferencia_oficial_menos_detalle_clp": oficial - detalle,
            "cuenta_15_presupuesto_vigente_mes_clp": vigente_15,
            "cuenta_15_ingreso_percibido_clp": percibido_15,
            "cuenta_15_vigente_menos_percibido_clp": vigente_15 - percibido_15,
            "condicion_3_residual_clp": residual_3,
            "cuenta_15_saldo_por_percibir_impreso_clp": int(c15["saldo_por_percibir_clp"]),
            "cuenta_15_saldo_por_percibir_raw": c15["saldo_por_percibir_clp_raw"],
            "resultado_control": "elegible" if elegible else "no_elegible",
            "estado_documento_posterior": doc["estado"],
            "politica_aceptacion": doc["politica_aceptacion"],
            "motivos_cuarentena_previos": "|".join(previous_reasons),
            "motivos_cuarentena_posteriores": "|".join(doc["motivos_cuarentena"]),
            "nota_metodologica": NOTA if elegible else "",
            "fuente_archivo": doc["archivo"], "fuente_ruta_relativa": doc["ruta_relativa"],
            "fuente_sha256": doc["sha256"],
            "total_fuente_pagina": total_trace["fuente_pagina_totales"],
            "total_fuente_linea": total_trace["fuente_linea_totales"],
            "cuenta_15_registro_id": c15["registro_id"],
            "cuenta_15_fuente_pagina": c15["fuente_pagina"], "cuenta_15_fuente_linea": c15["fuente_linea"],
        })
    docs_path.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")

controles.sort(key=lambda r: r["periodo"])
path = OUT / "ESP_2023-2025_controles_D13_v1.csv"
with path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(controles[0]))
    writer.writeheader()
    writer.writerows(controles)
resumen["archivo_controles"] = str(path.relative_to(ROOT))
resumen["resultado"] = "todos_elegibles" if resumen["permanecen_cuarentena"] == 0 else "cuarentena_residual"
(WORK / "resumen_rehabilitacion_d13.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(resumen, ensure_ascii=False, indent=2))
