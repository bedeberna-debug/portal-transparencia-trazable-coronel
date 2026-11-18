from pathlib import Path
import csv
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "bep_etapa2"
ANALYSIS = ROOT / "trabajo" / "07_Información_Presupuestaria" / "cuarentenas_bep"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
POLICY = "refinada_tolerancia_jerarquia_2_miles_clp"
INITIAL = "umbral_inicial_totales_100_jerarquia_95_aritmetica_99"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


with (ANALYSIS / "resumen_33_cuarentenas.csv").open(encoding="utf-8-sig", newline="") as f:
    analysis = list(csv.DictReader(f))
eligibility = {r["documento_id"]: r["elegible_politica_refinada"] == "si" for r in analysis}
visual = read_csv(DOCS / "VERIFICACION_VISUAL_CUARENTENAS_v1.csv")
if len(visual) != 10 or any(r["verificacion_visual"] != "confirmado" for r in visual):
    raise ValueError("La política exige 10/10 verificaciones visuales confirmadas")
if sum(eligibility.values()) != 28:
    raise ValueError("El universo elegible esperado es 28 documentos")

result = {"politica": POLICY, "verificacion_visual": "10/10", "anios": {}}
for year in [2023, 2024, 2025]:
    folder = WORK / str(year)
    docs = json.loads((folder / f"documentos_bep_{year}.json").read_text(encoding="utf-8"))
    records = read_csv(folder / f"bep_{year}_parseado.csv")
    lines = read_csv(folder / f"bep_{year}_validacion_lineas.csv")
    hierarchy = read_csv(folder / f"bep_{year}_validacion_jerarquia.csv")
    totals = read_csv(folder / f"bep_{year}_validacion_totales.csv")
    for doc in docs:
        did = doc["documento_id"]
        if doc["estado"] == "aceptado":
            doc["politica_aceptacion"] = INITIAL
        elif eligibility.get(did, False):
            doc["estado_previo_politica_refinada"] = "cuarentena"
            doc["motivos_cuarentena_previos"] = doc.get("motivos_cuarentena", [])
            doc["estado"] = "aceptado"
            doc["motivos_cuarentena"] = []
            doc["politica_aceptacion"] = POLICY
            doc_failures = [h for h in hierarchy if h["documento_id"] == did and h["resultado"] == "no_calza"]
            doc["diferencias_jerarquicas_documentadas"] = len(doc_failures)
            doc["magnitud_maxima_diferencia_miles_clp"] = max([abs(int(h["diferencia"])) for h in doc_failures] or [0])
            doc["anexo_diferencias"] = "documentación/07_Información_Presupuestaria/ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv"
        else:
            doc["politica_aceptacion"] = "no_aceptado"
    accepted = {d["documento_id"] for d in docs if d["estado"] == "aceptado"}
    for row in records + lines:
        if row["documento_id"] in accepted:
            row["estado_documento"] = "aceptado"
            row["politica_aceptacion"] = next(d["politica_aceptacion"] for d in docs if d["documento_id"] == row["documento_id"])
    accepted_records = [r for r in records if r["documento_id"] in accepted]
    accepted_hierarchy = [h for h in hierarchy if h["documento_id"] in accepted]
    accepted_totals = [t for t in totals if t["documento_id"] in accepted]
    h_ok = sum(h["resultado"] == "calza" for h in accepted_hierarchy)
    t_ok = sum(t["resultado"] == "calza" for t in accepted_totals)
    a_ok = sum(r["control_aritmetico_saldo"] == "calza" for r in accepted_records)
    summary = json.loads((folder / f"resumen_bep_{year}.json").read_text(encoding="utf-8"))
    summary["aceptados_conteo_previo_politica_refinada"] = summary["aceptados_conteo"]
    summary["cuarentenas_conteo_previo_politica_refinada"] = summary["cuarentenas_conteo"]
    summary["aceptados_conteo"] = len(accepted)
    summary["cuarentenas_conteo"] = len(docs) - len(accepted)
    summary["aceptados"] = {
        "documentos": len(accepted), "lineas": len(accepted_records),
        "catalogo_encontradas": sum(r["catalogo_estado"] == "encontrada" for r in accepted_records),
        "detalle_no_representado": sum(r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado" for r in accepted_records),
        "fuera_catalogo_mismo_nivel": sum(r["catalogo_estado"] == "fuera_catalogo_mismo_nivel" for r in accepted_records),
        "jerarquia_calzan": h_ok, "controles_jerarquia": len(accepted_hierarchy),
        "tasa_jerarquia": h_ok / len(accepted_hierarchy), "totales_calzan": t_ok, "controles_totales": len(accepted_totals),
        "tasa_totales": t_ok / len(accepted_totals), "aritmetica_calza": a_ok, "tasa_aritmetica": a_ok / len(accepted_records),
    }
    summary["politica_refinada"] = {
        "decision": POLICY, "incorporados": sum(eligibility.get(d["documento_id"], False) for d in docs),
        "criterios": "totales=100%; aritmetica>=99%; toda diferencia jerarquica abs<=2 M$; anexo permanente",
        "verificacion_visual": "10/10 lineas confirmadas",
    }
    write_csv(folder / f"bep_{year}_parseado.csv", records)
    write_csv(folder / f"bep_{year}_validacion_lineas.csv", lines)
    write_csv(folder / f"bep_{year}_documentos.csv", docs)
    (folder / f"documentos_bep_{year}.json").write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / f"resumen_bep_{year}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    result["anios"][str(year)] = {"aceptados": len(accepted), "cuarentena": len(docs) - len(accepted), "lineas": len(accepted_records), "tasa_jerarquia_informativa": h_ok / len(accepted_hierarchy), "tasa_totales": t_ok / len(accepted_totals), "tasa_aritmetica": a_ok / len(accepted_records)}
result["aceptados_total"] = sum(x["aceptados"] for x in result["anios"].values())
result["cuarentena_total"] = sum(x["cuarentena"] for x in result["anios"].values())
(ANALYSIS / "resultado_politica_refinada.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
