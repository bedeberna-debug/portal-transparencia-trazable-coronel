#!/usr/bin/env python3
"""Genera un candidato auditable de fusiones ortográficas de cargos.

No modifica maestros, agregados, fichas ni la normalización publicada. La integración
requiere revisión expresa del propietario del reporte generado.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
import csv
import re
import unicodedata

import pandas as pd

from build_modulo_personal import (
    ARCHIVOS,
    CATEGORIAS,
    DATOS,
    ROOT,
    VERSION_CANONICO,
    analizar_cargo,
    normalizar_cargo,
    proyectar_trayectoria,
    sha256,
    texto,
)

VERSION_CANDIDATO = "modulo_personal_v1.5.0-rc1_normalizacion_cargos"
SALIDA = ROOT / "documentación" / "plataforma"
REPORTE_MD = SALIDA / "REPORTE_FUSIONES_CARGOS_v0_1_1_CANDIDATO.md"
REPORTE_CSV = SALIDA / "REPORTE_FUSIONES_CARGOS_v0_1_1_CANDIDATO.csv"

ABREVIATURAS_NUEVAS = {
    "ENC": "ENCARGADO",
    "ENCG": "ENCARGADO",
    "ENCARG": "ENCARGADO",
    "DPTO": "DEPARTAMENTO",
    "JEF": "JEFE",
    "UNID": "UNIDAD",
    "AUX": "AUXILIAR",
}


def tokens_base(valor: str) -> list[str]:
    mayusculas = unicodedata.normalize("NFKD", texto(valor).upper())
    sin_acentos = "".join(c for c in mayusculas if not unicodedata.combining(c))
    return re.sub(r"[^A-ZÑ0-9]+", " ", sin_acentos).strip().split()


def normalizar_cargo_candidato(valor: str) -> str:
    """Versión candidata: amplía abreviaturas y ordena tokens sin corrección difusa."""
    vigente = normalizar_cargo(valor)
    tokens = [ABREVIATURAS_NUEVAS.get(token, token) for token in vigente.split()]
    return " ".join(sorted(tokens))


def razon_fusion(anterior: str, actual: str) -> str:
    razones = []
    base_anterior = tokens_base(anterior)
    base_actual = tokens_base(actual)
    nuevos_anterior = [ABREVIATURAS_NUEVAS.get(token, token) for token in normalizar_cargo(anterior).split()]
    nuevos_actual = [ABREVIATURAS_NUEVAS.get(token, token) for token in normalizar_cargo(actual).split()]
    if base_anterior != nuevos_anterior or base_actual != nuevos_actual:
        # La lista base conserva abreviaturas vigentes sin expandir; esta condición
        # complementa cualquier expansión nueva o ya aprobada.
        razones.append("expansión explícita de abreviaturas")
    normalizado_ampliado_anterior = " ".join(nuevos_anterior)
    normalizado_ampliado_actual = " ".join(nuevos_actual)
    if normalizado_ampliado_anterior != normalizado_ampliado_actual:
        razones.append("orden canónico de palabras")
    return " + ".join(razones) or "normalización Unicode y puntuación"


def trazabilidad(row: pd.Series, prefijo: str) -> dict:
    return {
        f"{prefijo}_registro_id": texto(row["registro_id"]),
        f"{prefijo}_periodo": texto(row["periodo"]),
        f"{prefijo}_cargo_publicado": texto(row["cargo_funcion"]),
        f"{prefijo}_normalizado_vigente": normalizar_cargo(row["cargo_funcion"]),
        f"{prefijo}_fuente_archivo": texto(row["fuente_archivo"]),
        f"{prefijo}_fuente_fila_csv": int(row["fuente_fila_csv"]),
        f"{prefijo}_fuente_sha256": texto(row["fuente_sha256"]),
    }


def main() -> None:
    generado = datetime.now().astimezone().isoformat(timespec="seconds")
    frames = []
    insumos = []
    columnas = [
        "registro_id", "categoria", "id_trabajador", "periodo", "cargo_funcion",
        "fuente_archivo", "fuente_fila_csv", "fuente_sha256", "version_esquema",
    ]
    for categoria in CATEGORIAS:
        ruta = DATOS / ARCHIVOS[categoria]
        df = pd.read_excel(ruta, sheet_name="Datos", usecols=columnas)
        if not df["version_esquema"].eq(VERSION_CANONICO).all():
            raise RuntimeError(f"Versión de esquema inesperada: {ruta}")
        insumos.append({"archivo": ruta.name, "sha256": sha256(ruta), "registros": len(df)})
        frames.append(df)
    todo = pd.concat(frames, ignore_index=True)
    proyeccion, _ = proyectar_trayectoria(todo)
    trayectoria = proyeccion[proyeccion["rol_trayectoria"].eq("canonica_trayectoria")].copy()

    fusiones = []
    comparaciones = 0
    for (categoria, id_trabajador), grupo in trayectoria.groupby(["categoria", "id_trabajador"], sort=True):
        grupo = grupo.sort_values("periodo")
        filas = list(grupo.itertuples(index=False))
        for anterior, actual in zip(filas, filas[1:]):
            comparaciones += 1
            cargo_anterior = texto(anterior.cargo_funcion)
            cargo_actual = texto(actual.cargo_funcion)
            if cargo_anterior == cargo_actual:
                continue
            candidato_anterior = normalizar_cargo_candidato(cargo_anterior)
            candidato_actual = normalizar_cargo_candidato(cargo_actual)
            vigente_anterior = normalizar_cargo(cargo_anterior)
            vigente_actual = normalizar_cargo(cargo_actual)
            if candidato_anterior != candidato_actual or vigente_anterior == vigente_actual:
                continue
            anterior_serie = pd.Series(anterior._asdict())
            actual_serie = pd.Series(actual._asdict())
            estado_vigente = analizar_cargo(cargo_actual, cargo_anterior, texto(anterior.periodo))["estado"]
            fusiones.append({
                "categoria": categoria,
                "id_trabajador": id_trabajador,
                "estado_vigente": estado_vigente,
                "estado_candidato": "variante_escritura",
                "normalizado_compartido_candidato": candidato_actual,
                "razon_fusion": razon_fusion(cargo_anterior, cargo_actual),
                **trazabilidad(anterior_serie, "anterior"),
                **trazabilidad(actual_serie, "actual"),
                "revision_propietario": "PENDIENTE",
            })

    # Comp Puerto de seguridad: los cambios sustantivos nunca colapsan.
    assert normalizar_cargo_candidato("ENC. DE OFICINA") != normalizar_cargo_candidato("JEFE DE OFICINA")
    assert normalizar_cargo_candidato("Profesional") != normalizar_cargo_candidato("Auxiliar")
    assert normalizar_cargo_candidato("ADM. DEPTO.") == normalizar_cargo_candidato("departamento administrativo")
    assert normalizar_cargo_candidato("ENC. DEPTO.") == normalizar_cargo_candidato("DEPARTAMENTO ENCARGADO")

    SALIDA.mkdir(parents=True, exist_ok=True)
    campos = list(fusiones[0].keys()) if fusiones else [
        "categoria", "id_trabajador", "estado_vigente", "estado_candidato",
        "normalizado_compartido_candidato", "razon_fusion", "revision_propietario",
    ]
    with REPORTE_CSV.open("w", encoding="utf-8-sig", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(fusiones)

    por_categoria = Counter(row["categoria"] for row in fusiones)
    por_estado = Counter(row["estado_vigente"] for row in fusiones)
    por_razon = Counter(row["razon_fusion"] for row in fusiones)
    lineas = [
        "# Reporte candidato de fusiones de cargos — v0.1.1",
        "",
        f"**Fecha:** {generado}  ",
        f"**Versión candidata de pipeline:** `{VERSION_CANDIDATO}`  ",
        f"**Canónico de entrada:** `{VERSION_CANONICO}`; {len(todo):,} registros  ",
        "**Estado:** **NO INTEGRADO — PENDIENTE DE REVISIÓN DEL PROPIETARIO**",
        "",
        "## 1. Alcance y compuerta",
        "",
        "Este reporte compara publicaciones consecutivas dentro de cada trayectoria D-15. "
        "Una fusión candidata ocurre solo cuando las grafías difieren, la normalización vigente también difiere "
        "y la normalización candidata produce exactamente la misma secuencia ordenada de tokens. "
        "No se usa similitud difusa, distancia de edición, inferencia semántica ni equivalencia entre cargos distintos.",
        "",
        "El candidato conserva `cargo_funcion`, los maestros, los agregados y las fichas publicadas sin cambios. "
        "Cada fila incluye ambos registros, períodos, archivos, filas CSV y SHA-256 para revisión. "
        "La columna `revision_propietario` permanece `PENDIENTE`; ninguna fusión se integra automáticamente.",
        "",
        "## 2. Reglas candidatas",
        "",
        "1. Unicode NFKD, mayúsculas, eliminación de acentos y puntuación, conservando Ñ.",
        "2. Expansiones vigentes y nuevas exclusivamente literales: `ENC./ENCG/ENCARG → ENCARGADO`, "
        "`DPTO → DEPARTAMENTO`, `JEF → JEFE`, `UNID → UNIDAD`, `AUX → AUXILIAR`; se mantienen las abreviaturas SC-04.",
        "3. Orden canónico alfabético de tokens después de expandir, conservando duplicados.",
        "4. `ENCARGADO` y `JEFE` no son equivalentes; tampoco `PROFESIONAL` y `AUXILIAR`. "
        "Las diferencias sustantivas permanecen como cambio de cargo o posible variante según la regla conservadora.",
        "",
        "## 3. Resultado",
        "",
        f"- Comparaciones consecutivas evaluadas: **{comparaciones:,}**.",
        f"- Fusiones nuevas candidatas: **{len(fusiones):,}**.",
        f"- Registros en la proyección D-15: **{len(trayectoria):,}**.",
        "- Integración en producción: **0; bloqueada hasta aprobación**.",
        "",
        "### Por categoría",
        "",
        "| Categoría | Fusiones candidatas |",
        "|---|---:|",
    ]
    lineas += [f"| {categoria} | {por_categoria.get(categoria, 0)} |" for categoria in CATEGORIAS]
    lineas += ["", "### Por estado que dejaría de marcarse como cambio/frontera", "", "| Estado vigente | Casos |", "|---|---:|"]
    lineas += [f"| {estado} | {conteo} |" for estado, conteo in sorted(por_estado.items())]
    lineas += ["", "### Por mecanismo", "", "| Mecanismo | Casos |", "|---|---:|"]
    lineas += [f"| {razon} | {conteo} |" for razon, conteo in sorted(por_razon.items())]
    lineas += [
        "",
        "## 4. Fusiones propuestas para revisión",
        "",
        "El CSV homónimo contiene la trazabilidad completa de ambos lados de cada par. "
        "La tabla siguiente resume las mismas candidaturas sin sustituir ese detalle.",
        "",
        "| Categoría | ID | Anterior | Actual | Normalizado candidato | Estado vigente | Motivo |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in fusiones:
        anterior = f"{row['anterior_periodo']}: {row['anterior_cargo_publicado']}".replace("|", "\\|")
        actual = f"{row['actual_periodo']}: {row['actual_cargo_publicado']}".replace("|", "\\|")
        lineas.append(
            f"| {row['categoria']} | `{row['id_trabajador']}` | {anterior} | {actual} | "
            f"`{row['normalizado_compartido_candidato']}` | {row['estado_vigente']} | {row['razon_fusion']} |"
        )
    if not fusiones:
        lineas.append("| — | — | — | — | — | — | Sin fusiones nuevas |")
    lineas += [
        "",
        "## 5. Insumos y decisión requerida",
        "",
        "| Maestro | Registros | SHA-256 |",
        "|---|---:|---|",
    ]
    lineas += [f"| `{row['archivo']}` | {row['registros']} | `{row['sha256']}` |" for row in insumos]
    lineas += [
        "",
        "**Decisión requerida:** revisar el CSV completo y aprobar, rechazar o enmendar las reglas y casos. "
        "Solo después de esa aprobación corresponde integrar el candidato al pipeline, regenerar fichas y "
        "declarar la mejora como aplicada. Hasta entonces, la interfaz debe rotularla como propuesta pendiente.",
        "",
    ]
    REPORTE_MD.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Reporte candidato generado: {REPORTE_MD.relative_to(ROOT)}")
    print(f"Detalle trazable: {REPORTE_CSV.relative_to(ROOT)}")
    print(f"Fusiones candidatas: {len(fusiones)}; integración: 0; revisión: PENDIENTE")


if __name__ == "__main__":
    main()
