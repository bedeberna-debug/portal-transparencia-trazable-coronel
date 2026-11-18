from pathlib import Path
from collections import Counter, defaultdict
import csv
import hashlib
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "factibilidad"
summary = json.loads((WORK / "resumen_factibilidad.json").read_text(encoding="utf-8"))
with (WORK / "bep_muestra_parseado.csv").open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
with (WORK / "validacion_jerarquia.csv").open(encoding="utf-8-sig", newline="") as f:
    hierarchy = list(csv.DictReader(f))
with (WORK / "validacion_lineas.csv").open(encoding="utf-8-sig", newline="") as f:
    line_checks = list(csv.DictReader(f))
catalog = {r["RUTA_JERARQUICA"] for r in json.loads((ROOT / "datos crudos" / "clasificadores_cgr" / "clasificador.json").read_text(encoding="utf-8"))}
assert len(rows) == len(line_checks) == summary["totales"]["lineas"] == 728
assert len({(r["muestra_id"], r["codigo_cuenta_pdf"]) for r in rows}) == len(rows)
assert all(r["fuente_archivo"] and r["fuente_ruta_relativa"] and r["fuente_pagina"] and r["fuente_linea"] and len(r["fuente_sha256"]) == 64 for r in rows)
assert all(hashlib.sha256((ROOT / r["fuente_ruta_relativa"]).read_bytes()).hexdigest() == r["fuente_sha256"] for r in rows)
assert all((r["codigo_cuenta_pdf"] in catalog) == (c["catalogo_estado"] == "encontrada") for r, c in zip(rows, line_checks))

by_doc = defaultdict(list)
for r in rows:
    by_doc[r["muestra_id"]].append(r)
for doc in summary["documentos"]:
    metrics = list(doc["totales_impresos"])
    top = [r for r in by_doc[doc["muestra_id"]] if int(r["nivel_jerarquico"]) == 1]
    for metric in metrics:
        recalculated = sum(int(r[metric]) for r in top)
        assert recalculated == doc["totales_impresos"][metric] == doc["sumas_subtitulos"][metric]

failed_h = [h for h in hierarchy if h["resultado"] == "no_calza"]
out_same = [r for r in rows if r["catalogo_estado"] == "fuera_catalogo_mismo_nivel"]
out_detail = [r for r in rows if r["catalogo_estado"] == "fuera_catalogo_nivel_detalle_no_representado"]
result = {
    "verificacion_independiente": "OK",
    "registros": len(rows),
    "trazabilidad_completa": len(rows),
    "sha256_fuentes_coinciden": len(rows),
    "catalogo_recalculado": "OK",
    "totales_recalculados": "20/20",
    "codigos_unicos_fuera_catalogo_mismo_nivel": len({r["codigo_cuenta_pdf"] for r in out_same}),
    "codigos_unicos_detalle_no_representado": len({r["codigo_cuenta_pdf"] for r in out_detail}),
    "padres_con_diferencias_jerarquia": len({(h["muestra_id"], h["codigo_padre"]) for h in failed_h}),
    "diferencias_jerarquia_por_magnitud_miles_clp": dict(Counter(str(abs(int(h["diferencia"]))) for h in failed_h)),
    "diferencia_maxima_absoluta_miles_clp": max(abs(int(h["diferencia"])) for h in failed_h),
}
(WORK / "verificacion_independiente.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
