from pathlib import Path
from collections import defaultdict
import csv
import json
import shutil

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "factibilidad"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
DOCS.mkdir(parents=True, exist_ok=True)

summary = json.loads((WORK / "resumen_factibilidad.json").read_text(encoding="utf-8"))
verification = json.loads((WORK / "verificacion_independiente.json").read_text(encoding="utf-8"))
with (WORK / "hallazgos_factibilidad.csv").open(encoding="utf-8-sig", newline="") as f:
    findings = list(csv.DictReader(f))

docs = {d["muestra_id"]: d for d in summary["documentos"]}
short = {
    "BEP_GASTOS_2023_12": "Gastos 2023",
    "BEP_INGRESOS_2023_12": "Ingresos 2023",
    "BEP_GASTOS_2025_12": "Gastos 2025",
    "BEP_INGRESOS_2025_12": "Ingresos 2025",
}
metric_label = {
    "presupuesto_inicial_miles_clp": "Inicial",
    "presupuesto_vigente_miles_clp": "Vigente",
    "obligacion_devengada_miles_clp": "Devengado",
    "ingresos_percibidos_miles_clp": "Percibidos",
    "saldo_presupuestario_miles_clp": "Saldo",
    "deuda_exigible_miles_clp": "Exigible",
    "ingresos_por_percibir_miles_clp": "Por percibir",
}

def num(value):
    return f"{int(value):,}".replace(",", ".")

def signed(value):
    value = int(value)
    return ("+" if value > 0 else "") + num(value)

def pct(a, b):
    return f"{100 * a / b:.1f} %".replace(".", ",")

def md(value):
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()

def ref(row):
    return f"{short[row['muestra_id']]}, p. {row['fuente_pagina']}, l. {row['fuente_linea']}"

# Copia íntegra del registro de 350 hallazgos a documentación.
shutil.copyfile(WORK / "hallazgos_factibilidad.csv", DOCS / "REGISTRO_HALLAZGOS_ETAPA1_v1.csv")

# Informe principal.
L = []
a = L.append
a("# INFORME DE FACTIBILIDAD — ETAPA 1")
a("")
a("**Proyecto:** Portal de Transparencia Trazable — Municipalidad de Coronel  ")
a("**Ámbito:** Información Presupuestaria 2023–2025  ")
a("**Fecha de cierre de la prueba:** 14 de noviembre de 2026  ")
a("**Estado:** Etapa 1 finalizada; Etapa 2 no iniciada.")
a("")
a("## 1. Conclusión")
a("")
a("**La extracción es técnicamente factible, con condiciones.** Los cuatro BEP de diciembre se parsearon mediante coordenadas y reglas del formulario, con trazabilidad completa. Los 20 controles de totales impresos calzan exactamente; la jerarquía calza en 96,0 % de los controles y la aritmética de saldo en 99,7 % de las líneas.")
a("")
a("La principal condición es normativa: el catálogo vigente representa subtítulo, ítem y asignación, pero no los niveles 4 y 5 presentes en los PDF. Además, hay 66 ocurrencias (33 códigos únicos) de niveles 1–3 ausentes del catálogo, registradas como hallazgos de cobertura/versionado normativo. No se remapeó ni corrigió ningún código o monto.")
a("")
a("Esta conclusión se limita a los cuatro BEP analizados. No demuestra todavía la factibilidad de los ESP, de otros meses ni del procesamiento masivo. La autoevaluación no constituye aprobación del usuario ni autorización para iniciar la Etapa 2.")
a("")
a("## 2. Muestras e identidad de las fuentes")
a("")
a("Se eligieron los cortes acumulados al 31 de diciembre de 2023 y 2025 para maximizar la cobertura de cuentas. Los montos se expresan en miles de pesos (M$), tal como están impresos.")
a("")
a("| Muestra | Formulario detectado | Corte declarado | Archivo | SHA-256 |")
a("|---|---|---|---|---|")
for d in summary["documentos"]:
    a(f"| {short[d['muestra_id']]} | {', '.join(d['formularios'])} | {', '.join(d['fechas_corte_contenido'])} | {md(d['archivo'])} | `{d['sha256']}` |")
a("")
a("Los documentos de gastos usan el Formulario 0102; los de ingresos, el Formulario 0101. En consecuencia, ingresos se valida con **Percibidos / Saldo / Por percibir**, no con Devengado / Exigible. Los cuatro ejemplares indican “TRIMESTRE CUARTO” y corte acumulado al 31/12.")
a("")
a("## 3. Método y trazabilidad")
a("")
a("1. Extracción de palabras y coordenadas con `pdfplumber`; no se utilizó el orden lineal del texto para asignar columnas.")
a("2. Detección del encabezado de cada página y de cinco columnas por anclas horizontales.")
a("3. Reconstrucción del código por posición y contexto jerárquico entre páginas, incluidas líneas que imprimen dos niveles a la vez.")
a("4. Conservación del código, denominación y cifras literales del PDF, junto con archivo, ruta relativa, página, línea textual y SHA-256.")
a("5. Controles independientes: catálogo, suma de hijas directas por cada padre y métrica, y comparación entre TOTALES impresos y suma de subtítulos parseados.")
a("6. Verificación independiente desde los CSV: unicidad, campos de trazabilidad, hashes de las fuentes, pertenencia al catálogo y totales.")
a("")
a(f"Resultado de la verificación independiente: **{verification['verificacion_independiente']}**; {verification['trazabilidad_completa']}/{verification['registros']} registros con trazabilidad completa y {verification['sha256_fuentes_coinciden']}/{verification['registros']} hashes coincidentes con los PDF originales.")
a("")
a("## 4. Nivel (a): existencia en el catálogo oficial")
a("")
a("El archivo `clasificador.json` contiene 451 rutas jerárquicas únicas y representa subtítulo/ítem/asignación. Se reportan dos tasas: la **bruta**, sobre todas las líneas, y la **comparable**, que excluye los niveles 4/5 no representados por ese catálogo.")
a("")
a("| Muestra | Líneas | En catálogo | Detalle 4/5 no representado | Fuera de catálogo, niveles 1–3 | Tasa bruta | Tasa comparable |")
a("|---|---:|---:|---:|---:|---:|---:|")
for d in summary["documentos"]:
    comparable = d["cuentas_en_catalogo"] + d["fuera_catalogo_mismo_nivel"]
    a(f"| {short[d['muestra_id']]} | {d['lineas_parseadas']} | {d['cuentas_en_catalogo']} | {d['detalle_no_representado']} | {d['fuera_catalogo_mismo_nivel']} | {pct(d['cuentas_en_catalogo'], d['lineas_parseadas'])} | {pct(d['cuentas_en_catalogo'], comparable)} |")
t = summary["totales"]
a(f"| **Total** | **{t['lineas']}** | **{t['catalogo_encontradas']}** | **{t['detalle_no_representado']}** | **{t['fuera_catalogo_mismo_nivel']}** | **{pct(t['catalogo_encontradas'], t['lineas'])}** | **{pct(t['catalogo_encontradas'], t['catalogo_encontradas'] + t['fuera_catalogo_mismo_nivel'])}** |")
a("")
a("Los 236 registros de niveles 4/5 no se interpretan automáticamente como códigos normativos inválidos: el catálogo entregado no contiene esos niveles. Las 66 ocurrencias restantes sí requieren cotejo de cobertura/versionado; corresponden a 33 códigos únicos, detallados en el registro de hallazgos.")
a("")
a("## 5. Nivel (b): suma de cuentas hijas al padre")
a("")
a("Cada control compara una métrica de un padre con la suma de sus hijas directas. La diferencia se define como `valor del padre − suma de hijas`.")
a("")
a("| Muestra | Controles padre–métrica | Calzan | No calzan | Tasa de éxito |")
a("|---|---:|---:|---:|---:|")
for d in summary["documentos"]:
    bad = d["controles_jerarquia"] - d["jerarquia_calzan"]
    a(f"| {short[d['muestra_id']]} | {d['controles_jerarquia']} | {d['jerarquia_calzan']} | {bad} | {pct(d['jerarquia_calzan'], d['controles_jerarquia'])} |")
a(f"| **Total** | **{t['controles_jerarquia']}** | **{t['jerarquia_calzan']}** | **{t['controles_jerarquia'] - t['jerarquia_calzan']}** | **{pct(t['jerarquia_calzan'], t['controles_jerarquia'])}** |")
a("")
a("Hay 46 diferencias concentradas en 24 relaciones documento–padre, todas en gastos: 44 de magnitud 1 M$ y 2 de magnitud 2 M$; máximo absoluto 2 M$. Son compatibles con diferencias de redondeo de la fuente, pero su causa no se presume ni se corrige. El detalle completo está en `REGISTRO_HALLAZGOS_ETAPA1_v1.md` y en el CSV asociado.")
a("")
a("## 6. Nivel (c): totales impresos contra lo parseado")
a("")
a("Cada celda de la tabla representa `total impreso = suma de subtítulos parseados`. Los 20 controles calzan sin diferencia.")
a("")
a("| Muestra | Inicial | Vigente | Ejecutado | Saldo | Quinta columna | Resultado |")
a("|---|---:|---:|---:|---:|---:|---|")
for d in summary["documentos"]:
    v = d["totales_impresos"]
    if d["muestra_id"].startswith("BEP_GASTOS"):
        ejecutado, quinta = f"Devengado: {num(v['obligacion_devengada_miles_clp'])}", f"Exigible: {num(v['deuda_exigible_miles_clp'])}"
    else:
        ejecutado, quinta = f"Percibidos: {num(v['ingresos_percibidos_miles_clp'])}", f"Por percibir: {num(v['ingresos_por_percibir_miles_clp'])}"
    a(f"| {short[d['muestra_id']]} | {num(v['presupuesto_inicial_miles_clp'])} | {num(v['presupuesto_vigente_miles_clp'])} | {ejecutado} | {num(v['saldo_presupuestario_miles_clp'])} | {quinta} | 5/5 |")
a(f"| **Total** | — | — | — | — | — | **{t['totales_calzan']}/{t['controles_totales']} (100,0 %)** |")
a("")
a("## 7. Control aritmético complementario")
a("")
a("Se comprobó además `saldo = vigente − ejecutado` para cada línea. No reemplaza ninguno de los tres niveles solicitados.")
a("")
a("| Muestra | Líneas que calzan | Total de líneas | Tasa |")
a("|---|---:|---:|---:|")
for d in summary["documentos"]:
    a(f"| {short[d['muestra_id']]} | {d['aritmetica_calza']} | {d['lineas_parseadas']} | {pct(d['aritmetica_calza'], d['lineas_parseadas'])} |")
a(f"| **Total** | **{t['aritmetica_calza']}** | **{t['lineas']}** | **{pct(t['aritmetica_calza'], t['lineas'])}** |")
a("")
a("Las dos excepciones están en gastos 2025: `22.06` presenta saldo 784.425 frente a 784.424 calculado, y `22.06.004` presenta 73.303 frente a 73.302; ambas diferencias son +1 M$ y se conservaron como impresas.")
a("")
a("## 8. Condiciones para una eventual escala")
a("")
a("- Conservar el código literal del PDF y su nivel; no forzar correspondencias con el catálogo.")
a("- Separar la validación de niveles 1–3 de la de subniveles no representados, y someter los 33 códigos únicos a cotejo normativo.")
a("- Incorporar reglas específicas para Formulario 0101 y 0102; validar por separado cualquier variante mensual/trimestral y los ESP antes de extrapolar.")
a("- Mantener como compuertas los tres controles y registrar las diferencias de fuente sin ajustar montos.")
a("- Conservar archivo, página, línea y SHA-256 por registro, y verificar los hashes antes de procesar.")
a("")
a("## 9. Evidencias y reproducción")
a("")
a("- Parser: `scripts/factibilidad_bep_etapa1.py`.")
a("- Verificador independiente: `scripts/verificar_factibilidad_bep_etapa1.py`.")
a("- Datos parseados y controles: `trabajo/07_Información_Presupuestaria/factibilidad/`.")
a("- Registro íntegro: `documentación/07_Información_Presupuestaria/REGISTRO_HALLAZGOS_ETAPA1_v1.csv` (350 ocurrencias).")
a("- Detalle narrativo y tablas de fallidos: `documentación/07_Información_Presupuestaria/REGISTRO_HALLAZGOS_ETAPA1_v1.md`.")
a("")
a("Comandos ejecutados desde la raíz del workspace:")
a("")
a("```bash")
a('python "scripts/factibilidad_bep_etapa1.py"')
a('python "scripts/verificar_factibilidad_bep_etapa1.py"')
a("```")
a("")
a("**Parada obligatoria:** no se procesaron los 143 PDF, ni ESP, ni julio de 2025, ni la republicación v2; no se generaron datos canónicos ni series mensuales de Etapa 2.")
(DOCS / "INFORME_FACTIBILIDAD_ETAPA1_v1.md").write_text("\n".join(L) + "\n", encoding="utf-8")

# Registro narrativo de hallazgos.
R = []
a = R.append
a("# REGISTRO DE HALLAZGOS — ETAPA 1")
a("")
a("**Alcance:** cuatro BEP de diciembre de 2023 y 2025. Unidades monetarias: M$.  ")
a("**Tratamiento:** preservación literal; sin remapeo, corrección, imputación ni interpolación.  ")
a("**Trazabilidad:** la muestra identifica el archivo y SHA-256 en el informe principal; cada ocurrencia incluye página y línea. El CSV asociado contiene los 350 hallazgos con SHA-256 completo por fila.")
a("")
a("## 1. Resumen")
a("")
a("| Tipo | Ocurrencias | Códigos o relaciones únicas |")
a("|---|---:|---:|")
a("| Código fuera de catálogo, niveles 1–3 | 66 | 33 códigos |")
a("| Detalle nivel 4/5 no representado en catálogo | 236 | 125 códigos |")
a("| Padre distinto de suma de hijas directas | 46 controles | 24 relaciones documento–padre |")
a("| Saldo distinto de vigente menos ejecutado | 2 | 2 líneas |")
a("| **Total** | **350** | — |")
a("")
a("Convenciones: en jerarquía, `diferencia = padre − suma de hijas`; en aritmética, `diferencia = saldo impreso − (vigente − ejecutado)`.")
a("")
a("## 2. Códigos de niveles 1–3 ausentes del catálogo")
a("")
a("Hallazgo de cobertura/versionado normativo. La ausencia en el catálogo vigente no prueba por sí sola invalidez histórica; no se fuerza el calce.")
a("")
outside = [f for f in findings if f["subtipo"] == "fuera_catalogo_mismo_nivel"]
groups = defaultdict(list)
for f in outside:
    groups[f["codigo_cuenta_pdf"]].append(f)
a("| Código PDF | Nivel | Denominación impresa | Ocurrencias y localización |")
a("|---|---:|---|---|")
for code in sorted(groups, key=lambda c: [int(x) for x in c.split(".")]):
    rows = groups[code]
    denoms = list(dict.fromkeys(md(r["denominacion_pdf"]) for r in rows))
    refs = "; ".join(ref(r) for r in rows)
    a(f"| `{code}` | {len(code.split('.'))} | {' / '.join(denoms)} | {len(rows)}: {refs} |")
a("")
a("## 3. Subniveles no representados por el catálogo")
a("")
a("Son 236 ocurrencias y 125 códigos únicos de niveles 4/5. Se separan del grupo anterior porque el catálogo de 451 rutas solo representa subtítulo/ítem/asignación. El detalle íntegro, con denominación, página, línea y SHA-256, está en `REGISTRO_HALLAZGOS_ETAPA1_v1.csv`, filtrando `subtipo = fuera_catalogo_nivel_detalle_no_representado`.")
a("")
a("| Muestra | Ocurrencias | Códigos únicos |")
a("|---|---:|---:|")
detail = [f for f in findings if f["subtipo"] == "fuera_catalogo_nivel_detalle_no_representado"]
for sample_id in docs:
    rows = [f for f in detail if f["muestra_id"] == sample_id]
    a(f"| {short[sample_id]} | {len(rows)} | {len(set(r['codigo_cuenta_pdf'] for r in rows))} |")
a(f"| **Total** | **{len(detail)}** | **{len(set(r['codigo_cuenta_pdf'] for r in detail))}** |")
a("")
a("## 4. Diferencias de jerarquía")
a("")
hierarchy = [f for f in findings if f["hallazgo_tipo"] == "jerarquia"]
with (WORK / "validacion_jerarquia.csv").open(encoding="utf-8-sig", newline="") as f:
    hierarchy_rows = list(csv.DictReader(f))
hierarchy_names = {(r["muestra_id"], r["codigo_padre"]): r["denominacion_padre"] for r in hierarchy_rows}
a(f"Se listan las {len(hierarchy)} diferencias padre–métrica. La denominación y los montos se mantienen como fueron extraídos.")
a("")
a("| Muestra | Código padre | Denominación | Métrica | Padre | Suma hijas | Diferencia | Página/línea |")
a("|---|---|---|---|---:|---:|---:|---|")
for f in sorted(hierarchy, key=lambda r: (r["muestra_id"], int(r["fuente_pagina"]), int(r["fuente_linea"]), r["metrica"])):
    denomination = f["denominacion_pdf"] or hierarchy_names[(f["muestra_id"], f["codigo_cuenta_pdf"])]
    a(f"| {short[f['muestra_id']]} | `{f['codigo_cuenta_pdf']}` | {md(denomination)} | {metric_label[f['metrica']]} | {num(f['valor_padre'])} | {num(f['suma_hijas'])} | {signed(f['diferencia'])} | {f['fuente_pagina']}/{f['fuente_linea']} |")
a("")
a("## 5. Diferencias aritméticas de línea")
a("")
a("| Muestra | Código | Denominación | Saldo impreso | Vigente − devengado | Diferencia | Página/línea |")
a("|---|---|---|---:|---:|---:|---|")
# Se recuperan los operandos desde el parseo para no reconstruirlos manualmente.
with (WORK / "bep_muestra_parseado.csv").open(encoding="utf-8-sig", newline="") as f:
    parsed = list(csv.DictReader(f))
parsed_key = {(r["muestra_id"], r["codigo_cuenta_pdf"]): r for r in parsed}
for f in [x for x in findings if x["hallazgo_tipo"] == "aritmetica_linea"]:
    p = parsed_key[(f["muestra_id"], f["codigo_cuenta_pdf"])]
    saldo = int(p["saldo_presupuestario_miles_clp"])
    calculado = int(p["presupuesto_vigente_miles_clp"]) - int(p["obligacion_devengada_miles_clp"])
    a(f"| {short[f['muestra_id']]} | `{f['codigo_cuenta_pdf']}` | {md(f['denominacion_pdf'])} | {num(saldo)} | {num(calculado)} | {signed(f['diferencia'])} | {f['fuente_pagina']}/{f['fuente_linea']} |")
a("")
a("## 6. Disposición")
a("")
a("Todos los hallazgos quedan abiertos para revisión normativa o documental; ninguno fue resuelto alterando la fuente. La Etapa 2 permanece sin iniciar hasta autorización expresa del usuario.")
(DOCS / "REGISTRO_HALLAZGOS_ETAPA1_v1.md").write_text("\n".join(R) + "\n", encoding="utf-8")

print(json.dumps({
    "informe": str(DOCS / "INFORME_FACTIBILIDAD_ETAPA1_v1.md"),
    "registro_md": str(DOCS / "REGISTRO_HALLAZGOS_ETAPA1_v1.md"),
    "registro_csv": str(DOCS / "REGISTRO_HALLAZGOS_ETAPA1_v1.csv"),
    "hallazgos_csv": len(findings),
    "codigos_nivel_1_3_unicos": len(groups),
    "diferencias_jerarquia": len(hierarchy),
}, ensure_ascii=False, indent=2))
