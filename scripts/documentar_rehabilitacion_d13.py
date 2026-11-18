from pathlib import Path
import csv
import json

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
OUT = ROOT / "datos procesados" / "07_Información_Presupuestaria"
DOCS = ROOT / "documentación" / "07_Información_Presupuestaria"
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "esp_etapa2"


def leer_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def reemplazar(texto, anterior, nuevo):
    if anterior not in texto:
        raise RuntimeError(f"No se encontró el párrafo esperado: {anterior[:100]}")
    return texto.replace(anterior, nuevo)


esp = leer_csv(OUT / "ESP_2023-2025_canonico_v1.csv")
controles = leer_csv(OUT / "ESP_2023-2025_controles_D13_v1.csv")
totales = leer_csv(OUT / "ESP_2023-2025_totales_ingresos_v1.csv")
deltas = leer_csv(OUT / "ESP_2023-2025_serie_mensual_ingresos_v1.csv")
deltas_totales = leer_csv(OUT / "ESP_2023-2025_serie_totales_ingresos_v1.csv")
hallazgos_delta = leer_csv(OUT / "ESP_2023-2025_hallazgos_delta_ingresos_v1.csv")
cobertura = leer_csv(OUT / "ESP_2023-2025_cobertura_v1.csv")
rehabilitados = sum(r["estado_documento_posterior"] == "aceptado" for r in controles)
cuarentena = len(controles) - rehabilitados
nota = (
    "El total oficial de saldo por percibir incorpora la cuenta 15 por vigente al mes menos percibido; "
    "la suma del detalle conserva los saldos impresos, incluidos sus ceros. Ambos totales son legítimos, "
    "tienen nombres distintos y deben mostrarse con su diferencia explicada, nunca oculta ni sustituida."
)

# Diccionario: conservar la descripción completa previa y actualizar únicamente D-13 y las nuevas series.
p = DOCS / "DICCIONARIO_DATOS_v1.md"
t = p.read_text(encoding="utf-8")
t = reemplazar(t, "| `estado_documento` | Solo aceptado en el canónico. |",
    "| `estado_documento` | Estado vigente del documento; solo aceptado en el canónico. |\n| `politica_aceptacion` | Umbral estricto en gastos o `D-13_rehabilitacion_condicionada_cuenta_15` en ingresos. |\n| `nota_metodologica` | Regla de agregación y preservación de cifras para documentos rehabilitados por D-13. |")
t = reemplazar(t, "No se creó una serie mensual ESP porque no fue solicitada en la autorización de escala.",
    "## 4. D-13: totales y series mensuales ESP de ingresos\n\n"
    "- `ESP_2023-2025_controles_D13_v1.csv`: una fila por cada uno de los 35 ESP de ingresos, con las tres condiciones aritméticas, residuos, estatus y trazabilidad del total y de la cuenta 15.\n"
    "- `ESP_2023-2025_totales_ingresos_v1.csv`: una fila por documento aceptado. `total_saldo_por_percibir_oficial_clp` es el total impreso DEUDORES PRESUPUESTARIOS; `saldo_por_percibir_suma_detalle_clp` es la suma de subtítulos de nivel 1. La diferencia se conserva junto al vigente/percibido de la cuenta 15 y sus ubicaciones.\n"
    "- `ESP_2023-2025_serie_mensual_ingresos_v1.csv`: deltas período–cuenta–métrica para las nueve métricas CLP. Enero usa base cero explícita; los demás meses exigen corte mensual inmediatamente anterior aceptado y presencia de la cuenta en ambos. Las cuentas ausentes no se imputan como cero.\n"
    "- `ESP_2023-2025_serie_totales_ingresos_v1.csv`: deltas documentales en formato largo. Mantiene series separadas para los nueve totales oficiales y la suma del detalle de saldo por percibir; nunca mezcla ambos conceptos.\n"
    "- `ESP_2023-2025_hallazgos_delta_ingresos_v1.csv`: cuentas sin delta por ausencia en uno de los dos cortes, sin imputación.\n\n"
    f"**Nota metodológica D-13:** {nota} Los deltas son diferencias aritméticas entre acumulados y no necesariamente flujos mensuales, especialmente en métricas de saldo.\n\n"
    f"Resultado: {rehabilitados} rehabilitados, {cuarentena} en cuarentena; {len(deltas)} deltas de cuentas y {len(deltas_totales)} de totales. Julio de 2025 es ausencia declarada y agosto no salta ese corte.")
p.write_text(t, encoding="utf-8")

# Bitácora de 12 pasos.
p = DOCS / "BITACORA_TRANSFORMACIONES_v1.md"
t = p.read_text(encoding="utf-8").replace("**Fecha:** 2026-11-14", "**Fecha:** 2026-11-15")
inicio = "## 5. Contrastar filas y totales"
fin = "## 6. Restaurar campos sin sobrescribir"
a = t.index(inicio); b = t.index(fin)
t = t[:a] + (
    f"{inicio}\n\nBEP aceptado: 330/330 totales. ESP de gastos: 385/385 totales con umbrales estrictos. "
    "En ingresos, las ocho métricas distintas de saldo por percibir calzan 280/280; el noveno total se rige por D-13. "
    f"Cada uno de los {len(controles)} documentos reprodujo individualmente las tres condiciones: ocho totales, identidad del total oficial y reconciliación exacta con la cuenta 15. "
    f"Se rehabilitaron {rehabilitados} y permanecen {cuarentena} en cuarentena. Los controles clásicos agregados se reportan como informativos, no como criterio D-13.\n\n"
) + t[b:]
t = reemplazar(t, "No hubo correcciones manuales. Los códigos fuera del catálogo se conservan como hallazgo de cobertura/versionado. Los ESP se tratan como tipo documental nuevo y separado, conforme a la autorización expresa. No se derivó serie ESP.",
    "No hubo correcciones manuales. Los códigos fuera del catálogo se conservan como hallazgo de cobertura/versionado. Los ESP son tipo documental separado. D-13 documenta la regla de agregación del saldo por percibir en ingresos y la rehabilitación condicionada por documento; no altera cifras ni remapea cuentas. TP-18 queda descartada porque el mecanismo está explicado y no hay vacío que requiera solicitud.")
inicio = "## 10. Ejecutar controles, tolerancia BEP y cuarentenas"
fin = "## 11. Registrar hallazgos y derivar deltas"
a = t.index(inicio); b = t.index(fin)
t = t[:a] + (
    f"{inicio}\n\nBEP: 66 aceptados y 5 en cuarentena. La política refinada incorporó 28 gastos con diferencias jerárquicas ≤2 M$, anexo permanente y verificación visual 10/10.\n\n"
    f"ESP: 35 gastos aceptados por umbrales estrictos y {rehabilitados} ingresos aceptados por D-13; {cuarentena} ESP en cuarentena. "
    "La tolerancia BEP de 2 M$ no se aplicó a ESP. D-13 no cambia los ceros de la cuenta 15 ni ningún otro dato impreso. "
    "El canónico y la tabla de totales conservan `total_saldo_por_percibir_oficial_clp` y `saldo_por_percibir_suma_detalle_clp` como campos distintos.\n\n"
) + t[b:]
inicio = "## 11. Registrar hallazgos y derivar deltas"
fin = "## 12. Versionar entregables y reproducción"
a = t.index(inicio); b = t.index(fin)
t = t[:a] + (
    f"{inicio}\n\nSe generaron 52.200 deltas BEP, {len(deltas)} deltas ESP de cuentas y {len(deltas_totales)} deltas ESP de totales. "
    f"Se registraron {len(hallazgos_delta)} cuentas sin delta por ausencia en un corte; no se imputaron ceros. "
    "Solo se unen meses consecutivos aceptados. Julio de 2025 no genera datos y agosto no salta julio. La serie oficial y la suma del detalle permanecen separadas.\n\n"
) + t[b:]
inicio = "## 12. Versionar entregables y reproducción"
a = t.index(inicio)
t = t[:a] + (
    f"{inicio}\n\nEntregables v1 actualizados: canónicos BEP/ESP, controles D-13, tabla de ambos totales, series BEP y ESP de ingresos, coberturas, hallazgos, diccionario, bitácora, gobernanza D-13/TP-18 y validación final. "
    "Reproducción desde la raíz: `python scripts/aplicar_rehabilitacion_d13_esp.py`; `python scripts/construir_canonico_esp_etapa2.py`; `python scripts/construir_series_d13_esp.py`; repetir la construcción del canónico para consolidar hallazgos de deltas; `python scripts/documentar_rehabilitacion_d13.py`; `python scripts/validar_final_etapa2.py`. Los PDF originales permanecen intocables.\n"
)
p.write_text(t, encoding="utf-8")

# Cobertura legible.
p = DOCS / "COBERTURA_Y_AUSENCIAS_v1.md"
t = p.read_text(encoding="utf-8")
inicio = "Los 35 ESP de gastos cumplen los umbrales."
a = t.index(inicio); b = t.index("## 3. Cuarentenas BEP permanentes")
t = t[:a] + (
    f"Los 35 ESP de gastos cumplen los umbrales estrictos. Los {rehabilitados} ESP de ingresos cumplen individualmente D-13 y quedan aceptados; {cuarentena} permanecen en cuarentena. "
    f"La diferencia del saldo por percibir no se corrige: se conserva en los dos campos documentales y en `ESP_2023-2025_totales_ingresos_v1.csv`.\n\n"
    f"La serie ESP de ingresos tiene {len(deltas)} deltas de cuentas y {len(deltas_totales)} de totales en 34 cortes computables. "
    f"Hay {len(hallazgos_delta)} cuentas sin delta por ausencia en el corte previo o actual. Julio de 2025 es ausencia declarada; agosto de 2025 no es computable.\n\n"
) + t[b:]
p.write_text(t, encoding="utf-8")

# Registro legible de hallazgos.
p = DOCS / "REGISTRO_HALLAZGOS_v1.md"
t = p.read_text(encoding="utf-8")
inicio = "## 3. Cuarentenas ESP de ingresos"
fin = "## 4. Política jerárquica BEP y verificación visual"
a = t.index(inicio); b = t.index(fin)
t = t[:a] + (
    "## 3. Regla de agregación ESP de ingresos y D-13\n\n"
    f"Los {len(controles)} documentos fueron evaluados individualmente. {rehabilitados} reprodujeron las tres condiciones y fueron rehabilitados; {cuarentena} permanecen en cuarentena. "
    "El total oficial de saldo por percibir incluye el saldo inicial de caja por vigente al mes menos percibido, mientras el detalle conserva los saldos impresos. "
    "No se modificaron ceros ni otras cifras. El control `ESP_2023-2025_controles_D13_v1.csv` conserva residuos, estatus y trazabilidad por documento. "
    f"Los {len(hallazgos_delta)} casos de cuentas sin delta mensual se registran sin imputación. TP-18 queda descartada con causa documentada.\n\n"
) + t[b:]
p.write_text(t, encoding="utf-8")

# Resumen de construcción actualizado con los nuevos productos.
p = WORK / "resumen_construccion_canonico.json"
resumen = json.loads(p.read_text(encoding="utf-8"))
resumen["esp"].update({
    "ingresos_rehabilitados_d13": rehabilitados, "ingresos_cuarentena_d13": cuarentena,
    "totales_documentales_ingresos": len(totales), "registros_delta_ingresos_cuentas": len(deltas),
    "registros_delta_ingresos_totales": len(deltas_totales), "hallazgos_delta_ingresos": len(hallazgos_delta),
})
p.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(resumen["esp"], ensure_ascii=False, indent=2))
