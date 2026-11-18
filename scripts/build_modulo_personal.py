#!/usr/bin/env python3
"""Genera los artefactos estáticos del módulo Personal y Remuneraciones.

Uso único desde la raíz del proyecto:
    python scripts/build_modulo_personal.py

Los maestros canónicos, inventarios y manifiestos se abren solo en lectura.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
import hashlib
import json
import math
import re
import shutil
import unicodedata

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATOS = ROOT / "datos procesados" / "04_Personal_y_Remuneraciones"
DOCS = ROOT / "documentación" / "04_Personal_y_Remuneraciones"
SALIDA_DOCS = ROOT / "documentación" / "plataforma"
DATA = ROOT / "plataforma" / "data"
DOCS_PUBLICOS = ROOT / "plataforma" / "docs"
PORTAL_OFICIAL = "https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=MU068"
VERSION_CANONICO = "canonico_v1.0.0"
VERSION_PIPELINE = "modulo_personal_v1.4.0"
GLOSARIO = ROOT / "diseño" / "GLOSARIO_DEFINICIONES_v1.md"
ASIGNACIONES_INDICE = DOCS / "asignaciones_indice.json"
LEYENDA_GENERO = (
    "Composición por género inferida a partir del nombre con revisión manual; "
    "no corresponde a dato declarado por las personas ni publicado por el municipio. "
    "Se muestra solo de forma agregada."
)
LEYENDA_ESTAMENTO_ESTIMADO = (
    "Estamento estimado por el proyecto a partir del cargo publicado; "
    "no corresponde a clasificación oficial del municipio."
)
MAPEO_ESTAMENTO = ROOT / "trabajo" / "04_Personal_y_Remuneraciones" / "universo_cargos_d17.csv"
SHA_MAPEO_ESTAMENTO = "99a357539d830d1e83f1c89b8e12ee50ea1f57a0576d538e8a8284dc1a571548"
CATEGORIAS_ESTIMADAS = ["Código del Trabajo", "Honorarios"]
ESTAMENTOS_ESTIMADOS = ["Administrativo", "Auxiliar", "Profesional", "Técnico", "Directivo", "Jefatura"]
ABREVIATURAS_CARGO = {
    "ADM": "ADMINISTRATIVO",
    "ADMIN": "ADMINISTRATIVO",
    "DEPTO": "DEPARTAMENTO",
    "DEPT": "DEPARTAMENTO",
    "OF": "OFICINA",
    "OFIC": "OFICINA",
    "PROF": "PROFESIONAL",
    "COORD": "COORDINACION",
    "GAB": "GABINETE",
    "MUNIC": "MUNICIPAL",
    "MUN": "MUNICIPAL",
    "RRHH": "RECURSOS HUMANOS",
}
MARCADORES_UNIDAD_CARGO = {
    "DEPARTAMENTO", "OFICINA", "DIRECCION", "GABINETE", "MUNICIPAL",
    "CENTRO", "PROGRAMA", "CEMENTERIO", "ALBERGUE",
}
CATEGORIAS = ["Planta", "Contrata", "Código del Trabajo", "Honorarios"]
ARCHIVOS = {
    "Planta": "MAESTRO_Planta_Coronel_2023-2025_canonico_v1.xlsx",
    "Contrata": "MAESTRO_Contrata_Coronel_2023-2025_canonico_v1.xlsx",
    "Código del Trabajo": "MAESTRO_CODTrabajo_Coronel_2023-2025_canonico_v1.xlsx",
    "Honorarios": "MAESTRO_Honorarios_Coronel_2023-2025_canonico_v1.xlsx",
}
ESTAMENTOS = [
    "Administrativo", "Auxiliar", "Profesional", "Técnico", "Directivo",
    "Jefatura", "Alcalde", "Otro", "Honorarios",
]
PERIODOS = [f"{anio}-{mes:02d}" for anio in (2023, 2024, 2025) for mes in range(1, 13)]
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def texto(valor) -> str:
    if valor is None or (not isinstance(valor, str) and pd.isna(valor)):
        return ""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", str(valor))).strip()


def clave(valor) -> str:
    valor = unicodedata.normalize("NFKD", texto(valor).casefold())
    return "".join(c for c in valor if not unicodedata.combining(c) and c.isalnum())


def clave_nombre(valor) -> str:
    return clave(valor).upper()


def decodificar_asignaciones(raw, conceptos: dict[str, dict]) -> list[dict]:
    """Traduce cada ocurrencia sin deduplicar ni alterar el valor municipal original."""
    original = texto(raw)
    if not original:
        return []
    codigos = re.findall(r"\(([^()]*)\)", original)
    if not codigos or "".join(f"({codigo})" for codigo in codigos) != original:
        return [{
            "codigo": original, "codigo_raw": original, "nombre": None,
            "estado": "no_decodificado",
            "nota": "Código fuera del formato de secuencia entre paréntesis; se conserva literalmente y no se infiere su significado.",
        }]
    decodificadas = []
    for codigo in codigos:
        concepto = conceptos.get(codigo)
        decodificadas.append({
            "codigo": codigo,
            "codigo_raw": f"({codigo})",
            "nombre": concepto["nombre"] if concepto else None,
            "estado": "decodificado" if concepto else "no_decodificado",
            "nota": None if concepto else "Código sin correspondencia en el índice oficial; no se infiere su significado.",
        })
    return decodificadas


def normalizar_cargo(valor) -> str:
    """Normalización conservadora para comparar; jamás reemplaza cargo_funcion."""
    texto_mayuscula = unicodedata.normalize("NFKD", texto(valor).upper())
    sin_acentos = "".join(c for c in texto_mayuscula if not unicodedata.combining(c))
    tokens = re.sub(r"[^A-ZÑ0-9]+", " ", sin_acentos).strip().split()
    return " ".join(ABREVIATURAS_CARGO.get(token, token) for token in tokens)


def analizar_cargo(actual: str, anterior: str, periodo_anterior: str) -> dict:
    """Distingue cambio, variante exacta normalizada y frontera por unidad añadida."""
    normalizado_actual = normalizar_cargo(actual)
    normalizado_anterior = normalizar_cargo(anterior)
    resultado = {
        "periodo_anterior": periodo_anterior,
        "cargo_anterior": anterior,
        "cargo_normalizado_proyecto": normalizado_actual,
        "cargo_anterior_normalizado_proyecto": normalizado_anterior,
    }
    if normalizado_actual == normalizado_anterior:
        return resultado | {
            "estado": "sin_cambio" if texto(actual) == texto(anterior) else "variante_escritura",
            "explicacion": "El texto normalizado es idéntico; se conservan ambas grafías originales.",
        }
    tokens_actual = set(normalizado_actual.split())
    tokens_anterior = set(normalizado_anterior.split())
    if tokens_actual and tokens_anterior and (tokens_actual < tokens_anterior or tokens_anterior < tokens_actual):
        agregados = tokens_actual.symmetric_difference(tokens_anterior)
        if agregados & MARCADORES_UNIDAD_CARGO:
            return resultado | {
                "estado": "posible_variante",
                "explicacion": "Un texto contiene el otro y añade o retira una unidad; requiere verificación documental.",
            }
    return resultado | {
        "estado": "cambio_cargo",
        "explicacion": "Los textos normalizados difieren y no cumplen la regla conservadora de posible variante.",
    }


def nativo(valor):
    if valor is None:
        return None
    if isinstance(valor, (np.integer,)):
        return int(valor)
    if isinstance(valor, (np.floating,)):
        return None if math.isnan(valor) else float(valor)
    if isinstance(valor, float) and math.isnan(valor):
        return None
    if isinstance(valor, (pd.Timestamp, datetime)):
        return valor.isoformat()
    if isinstance(valor, np.bool_):
        return bool(valor)
    return valor


def registro_limpio(registro: dict) -> dict:
    return {k: nativo(v) for k, v in registro.items()}


def escribir_json(nombre: str, contenido: dict | list, compacto: bool = False) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    destino = DATA / nombre
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(
            contenido,
            ensure_ascii=False,
            indent=None if compacto else 2,
            separators=(",", ":") if compacto else None,
            default=nativo,
        ) + "\n",
        encoding="utf-8",
    )
    return destino


def base_artefacto(generado: str, clave_primaria: list[str], registros: list[dict]) -> dict:
    return {
        "generado_desde": VERSION_CANONICO,
        "version_pipeline": VERSION_PIPELINE,
        "fecha_generacion": generado,
        "clave": clave_primaria,
        "conteos": {"registros": len(registros)},
        "registros": registros,
    }


def respaldo_csv(ruta_relativa: str) -> str:
    """Ruta pública estable del CSV copiado dentro del sitio estático."""
    ruta = Path(ruta_relativa)
    try:
        relativa = ruta.relative_to(Path("datos crudos") / "04_Personal_y_Remuneraciones")
    except ValueError:
        relativa = Path(ruta.name)
    return (Path("fuentes") / relativa).as_posix()


def trazabilidad(df: pd.DataFrame) -> dict:
    """Compacta archivo/ruta/SHA y enumera todas las filas que componen un agregado."""
    fuentes = []
    if df.empty:
        return {"portal_oficial": PORTAL_OFICIAL, "fuentes": []}
    columnas = ["fuente_archivo", "fuente_ruta_relativa", "fuente_sha256"]
    for (archivo, ruta, huella), grupo in df.groupby(columnas, dropna=False, sort=True):
        filas = sorted(int(v) for v in grupo["fuente_fila_csv"].tolist())
        fuentes.append({
            "archivo": texto(archivo),
            "ruta_relativa": texto(ruta),
            "url_respaldo": respaldo_csv(texto(ruta)),
            "sha256": texto(huella),
            "filas_csv": filas,
            "registros": len(filas),
            "periodos": sorted(grupo["periodo"].astype(str).unique().tolist()),
        })
    return {"portal_oficial": PORTAL_OFICIAL, "fuentes": fuentes}


def agregar(df: pd.DataFrame, claves: list[str], metricas: dict[str, str]) -> list[dict]:
    salida = []
    if df.empty:
        return salida
    for valores, grupo in df.groupby(claves, dropna=False, sort=True):
        if not isinstance(valores, tuple):
            valores = (valores,)
        fila = dict(zip(claves, valores))
        bruta_informada = grupo.loc[grupo["remuneracion_bruta_clp"] > 0, "remuneracion_bruta_clp"]
        for nombre, operacion in metricas.items():
            if operacion == "registros":
                fila[nombre] = int(len(grupo))
            elif operacion == "bruta":
                fila[nombre] = int(grupo["remuneracion_bruta_clp"].sum())
            elif operacion == "liquida":
                fila[nombre] = int(grupo["remuneracion_liquida_clp"].sum())
            elif operacion == "bruta_no_informa":
                fila[nombre] = int((grupo["remuneracion_bruta_clp"] == 0).sum())
            elif operacion == "bruta_informada":
                fila[nombre] = int(len(bruta_informada))
            elif operacion == "bruta_promedio":
                fila[nombre] = float(bruta_informada.mean()) if len(bruta_informada) else None
            elif operacion == "bruta_mediana":
                fila[nombre] = float(bruta_informada.median()) if len(bruta_informada) else None
        fila["trazabilidad"] = trazabilidad(grupo)
        salida.append(registro_limpio(fila))
    return salida


def periodo_nominal_archivo(archivo: str) -> str | None:
    """Extrae procedencia nominal sin sustituir jamás el período del contenido (D-07/D-15)."""
    coincidencia = re.search(r"([^_]+)_((?:19|20)\d{2})$", Path(texto(archivo)).stem)
    if not coincidencia:
        return None
    mes_texto, anio = coincidencia.groups()
    meses = {clave(mes): indice + 1 for indice, mes in enumerate(MESES)}
    mes = meses.get(clave(mes_texto))
    return f"{anio}-{mes:02d}" if mes else None


def proyectar_trayectoria(todo: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """Aplica D-15 solo a la proyección individual; no altera montos ni agregados."""
    proyeccion = todo.copy()
    proyeccion["periodo_nominal_archivo"] = proyeccion["fuente_archivo"].map(periodo_nominal_archivo)
    proyeccion["rol_trayectoria"] = "canonica_trayectoria"
    proyeccion["regla_resolucion"] = None
    proyeccion["version_alterna_de"] = None
    proyeccion["motivo_version_alterna"] = None
    claves = ["categoria", "id_trabajador", "periodo"]
    colisiones = proyeccion[proyeccion["id_trabajador"].map(texto).ne("") & proyeccion.duplicated(claves, keep=False)]
    resoluciones = []
    for (categoria, id_trabajador, periodo), grupo in colisiones.groupby(claves, sort=True):
        coincidentes = grupo[grupo["periodo_nominal_archivo"] == periodo]
        resolucion = {
            "categoria": categoria,
            "id_trabajador": id_trabajador,
            "periodo": periodo,
            "registros": int(len(grupo)),
            "versiones_coincidentes": int(len(coincidentes)),
            "resuelta": len(coincidentes) == 1,
            "registro_seleccionado": None,
            "registros_alternos": [],
        }
        if len(coincidentes) == 1:
            seleccionado = texto(coincidentes.iloc[0]["registro_id"])
            resolucion["registro_seleccionado"] = seleccionado
            proyeccion.loc[coincidentes.index, "regla_resolucion"] = "D-15_coincidencia_periodo_nominal"
            alternas = grupo.drop(index=coincidentes.index)
            for indice, fila in alternas.iterrows():
                proyeccion.loc[indice, "rol_trayectoria"] = "version_alterna"
                proyeccion.loc[indice, "regla_resolucion"] = "D-15_coincidencia_periodo_nominal"
                proyeccion.loc[indice, "version_alterna_de"] = seleccionado
                proyeccion.loc[indice, "motivo_version_alterna"] = "periodo_contenido_distinto_de_periodo_nominal_archivo"
                resolucion["registros_alternos"].append(texto(fila["registro_id"]))
        resoluciones.append(resolucion)
    return proyeccion, resoluciones


def validar_unicidad(proyeccion: pd.DataFrame, resoluciones: list[dict], generado: str) -> tuple[dict, bool]:
    trabajo = proyeccion.copy()
    trabajo["id_trabajador"] = trabajo["id_trabajador"].map(texto)
    trabajo["periodo"] = trabajo["periodo"].map(texto)
    trabajo["clave_nombre"] = trabajo["nombre_normalizado"].map(clave_nombre)
    trayectoria = trabajo[trabajo["rol_trayectoria"] == "canonica_trayectoria"]
    claves = ["categoria", "id_trabajador", "periodo"]
    mascara = trayectoria["id_trabajador"].ne("") & trayectoria.duplicated(claves, keep=False)
    duplicados = trayectoria[mascara]
    grupos = []
    for (categoria, id_trabajador, periodo), grupo in duplicados.groupby(claves, sort=True):
        grupos.append({
            "categoria": categoria,
            "id_trabajador": id_trabajador,
            "periodo": periodo,
            "registros": [texto(valor) for valor in grupo["registro_id"]],
        })
    nombres_por_id = trabajo[trabajo["id_trabajador"].ne("")].groupby("id_trabajador")["clave_nombre"].nunique()
    ids_mezclados = sorted(nombres_por_id[nombres_por_id > 1].index.tolist())
    ids_por_nombre = trabajo[trabajo["clave_nombre"].ne("")].groupby("clave_nombre")["id_trabajador"].nunique()
    nombres_multi_id = sorted(ids_por_nombre[ids_por_nombre > 1].index.tolist())
    aliases = []
    for nombre in nombres_multi_id:
        grupo = trabajo[trabajo["clave_nombre"] == nombre]
        aliases.append({
            "nombre_normalizado": sorted(grupo["nombre_normalizado"].astype(str).unique().tolist())[0],
            "identificadores": sorted(grupo["id_trabajador"].unique().tolist()),
            "categorias": sorted(grupo["categoria"].unique().tolist()),
        })
    mascara_nombre_categoria = trabajo["clave_nombre"].ne("") & trabajo.duplicated(["clave_nombre", "categoria"], keep=False)
    nombre_categoria = trabajo[mascara_nombre_categoria].groupby(["clave_nombre", "categoria"])["id_trabajador"].nunique()
    mismo_nombre_varios_ids_categoria = int((nombre_categoria > 1).sum())
    no_resueltas = [r for r in resoluciones if not r["resuelta"]]
    resumen = {
        "fecha_generacion": generado,
        "registros_evaluados": int(len(trabajo)),
        "registros_en_proyeccion_trayectoria": int(len(trayectoria)),
        "versiones_alternas": int((trabajo["rol_trayectoria"] == "version_alterna").sum()),
        "registro_id_duplicados": int(trabajo["registro_id"].duplicated().sum()),
        "id_trabajador_vacios": int(trabajo["id_trabajador"].eq("").sum()),
        "colisiones_originales_id_periodo": len(resoluciones),
        "colisiones_resueltas_d15": len(resoluciones) - len(no_resueltas),
        "colisiones_no_resueltas_d15": len(no_resueltas),
        "colisiones_id_periodo": len(grupos),
        "registros_en_colisiones_id_periodo": int(len(duplicados)),
        "ids_con_varios_nombres_normalizados": len(ids_mezclados),
        "nombres_con_varios_ids_entre_categorias": len(nombres_multi_id),
        "nombres_con_varios_ids_dentro_de_una_categoria": mismo_nombre_varios_ids_categoria,
        "estado": "RECHAZADA" if grupos or no_resueltas or ids_mezclados or mismo_nombre_varios_ids_categoria else "APROBADA",
        "ficha_individual_habilitada": not (grupos or no_resueltas or ids_mezclados or mismo_nombre_varios_ids_categoria),
        "criterio": (
            "D-15 selecciona una única versión por categoria + id_trabajador + periodo cuando su período de "
            "contenido coincide con el nominal del archivo. La validación exige unicidad sobre esa proyección, "
            "sin desempate por monto, orden de fila o posterioridad presumida."
        ),
        "detalle_colisiones": grupos,
        "resoluciones_d15": resoluciones,
        "aliases_entre_categorias": aliases,
        "nota": (
            "Los IDs heredados tienen alcance por categoría y no constituyen una identidad global. Las 56 "
            "advertencias entre categorías no se unifican. La suma de fichas no reconcilia con los agregados: "
            "estos conservan las 22.940 filas y la trayectoria selecciona 22.938 conforme a D-15."
        ),
    }
    aprobada = resumen["ficha_individual_habilitada"]

    lineas = [
        "# Validación de unicidad persona-período — Personal y Remuneraciones",
        "",
        f"**Fecha de ejecución:** {generado}  ",
        "**Insumo:** maestros `canonico_v1.0.0`, 22.940 registros  ",
        "**Proyección:** trayectoria individual conforme a D-15  ",
        f"**Resultado:** **{resumen['estado']}**  ",
        f"**Ficha individual:** {'HABILITADA' if aprobada else 'DESHABILITADA'}",
        "",
        "## 1. Criterio y alcance",
        "",
        "La validación comprueba: (1) unicidad de `registro_id`; (2) ausencia de `id_trabajador` vacío; "
        "(3) unicidad de `categoria + id_trabajador + periodo` sobre la proyección `canonica_trayectoria`; "
        "(4) que un ID no se asocie a varios nombres normalizados; y (5) que un nombre normalizado no tenga "
        "varios IDs dentro de una misma categoría. D-15 selecciona únicamente cuando existe exactamente una "
        "versión cuyo período de contenido coincide con el período nominal del archivo. No se desempata por "
        "monto, orden de fila ni posterioridad presumida y no se altera el período de contenido conforme a D-07.",
        "",
        "Las versiones no seleccionadas permanecen íntegras como `version_alterna`. La comprobación transversal "
        "de nombres con IDs distintos es una advertencia separada: no prueba identidad ni duplicación entre categorías.",
        "",
        "## 2. Resultados",
        "",
        "| Control | Resultado |",
        "|---|---:|",
        f"| Registros canónicos evaluados | {len(trabajo):,} |".replace(",", "."),
        f"| Registros seleccionados para trayectoria | {len(trayectoria):,} |".replace(",", "."),
        f"| Versiones alternas preservadas | {resumen['versiones_alternas']} |",
        f"| `registro_id` duplicados | {resumen['registro_id_duplicados']} |",
        f"| `id_trabajador` vacíos | {resumen['id_trabajador_vacios']} |",
        f"| Colisiones originales | {len(resoluciones)} |",
        f"| Colisiones resueltas por D-15 | {resumen['colisiones_resueltas_d15']} |",
        f"| Colisiones sin resolver | {len(no_resueltas)} |",
        f"| Colisiones en la proyección validada | {len(grupos)} |",
        f"| IDs asociados a varios nombres normalizados | {len(ids_mezclados)} |",
        f"| Nombres con varios IDs dentro de una categoría | {mismo_nombre_varios_ids_categoria} |",
        f"| Advertencias: nombres con IDs distintos entre categorías | {len(nombres_multi_id)} |",
        "",
        "## 3. Resolución de las colisiones originales",
        "",
    ]
    for resolucion in resoluciones:
        lineas += [
            f"### {resolucion['id_trabajador']} — {resolucion['periodo']}",
            "",
            f"**Estado:** {'resuelta por D-15' if resolucion['resuelta'] else 'sin resolver'}; "
            f"{resolucion['versiones_coincidentes']} versión(es) con coincidencia contenido/archivo.",
            "",
            "| Rol | Registro | Período nominal del archivo | Bruto CLP | Líquido CLP | Archivo | Fila CSV | SHA-256 |",
            "|---|---|---|---:|---:|---|---:|---|",
        ]
        subset = trabajo[(trabajo["categoria"] == resolucion["categoria"]) & (trabajo["id_trabajador"] == resolucion["id_trabajador"]) & (trabajo["periodo"] == resolucion["periodo"])]
        for r in subset.to_dict("records"):
            lineas.append(
                f"| {r['rol_trayectoria']} | `{r['registro_id']}` | {r['periodo_nominal_archivo'] or 'No identificable'} | "
                f"{int(r['remuneracion_bruta_clp']):,} | {int(r['remuneracion_liquida_clp']):,} | "
                f"`{r['fuente_archivo']}` | {r['fuente_fila_csv']} | `{r['fuente_sha256']}` |".replace(",", ".")
            )
        lineas += [
            "",
            "La selección es una convención documental para visualizar trayectoria, no una declaración de cuál "
            "cifra es jurídicamente correcta. Las versiones alternas se muestran en «Otra publicación del mismo período».",
            "",
        ]
    lineas += [
        "## 4. Advertencias de identidad transversal",
        "",
        f"Se observaron **{len(aliases)} nombres normalizados con más de un ID entre categorías**. "
        "No se resuelven por semejanza de nombre. Las fichas se publican por ID dentro de su categoría; "
        "D-15 no crea ni autoriza una identidad global fusionada.",
        "",
        "| Nombre normalizado | Identificadores | Categorías |",
        "|---|---|---|",
    ]
    for alias in aliases:
        lineas.append(
            f"| {alias['nombre_normalizado']} | {', '.join('`'+x+'`' for x in alias['identificadores'])} | "
            f"{', '.join(alias['categorias'])} |"
        )
    lineas += [
        "",
        "## 5. Decisión de publicación",
        "",
        (f"**Validación aprobada.** Se generan `data/fichas/<id_trabajador>.json` con {len(trayectoria):,} "
         "registros seleccionados y las versiones alternas íntegras. Los meses sin registro se declaran como "
         "ausencias y no se interpolan. No se incluye género ni campos derivados de nombre." if aprobada else
         "**Validación no aprobada.** No se generan fichas individuales; la interfaz permanece deshabilitada."),
        "",
        "Los agregados continúan usando las 22.940 filas canónicas. **La suma de fichas no reconcilia con los "
        "agregados**, porque D-15 excluye dos versiones alternas solo de la proyección de trayectoria.",
        "",
        "**Trazabilidad de esta conclusión:** generada automáticamente por `scripts/build_modulo_personal.py` "
        "desde los cuatro maestros canónicos; aplica D-15 a H-005 y H-006 sin modificar las fuentes.",
        "",
    ]
    SALIDA_DOCS.mkdir(parents=True, exist_ok=True)
    (SALIDA_DOCS / "VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md").write_text("\n".join(lineas), encoding="utf-8")
    return resumen, aprobada


def rango_remuneracion(valor: float) -> str:
    if valor == 0:
        return "No informa / No tiene (0 canónico)"
    if valor < 500_000:
        return "$1–$499.999"
    if valor < 1_000_000:
        return "$500.000–$999.999"
    if valor < 2_000_000:
        return "$1.000.000–$1.999.999"
    if valor < 3_000_000:
        return "$2.000.000–$2.999.999"
    return "$3.000.000 o más"


def main() -> None:
    generado = datetime.now().astimezone().isoformat(timespec="seconds")
    DATA.mkdir(parents=True, exist_ok=True)
    SALIDA_DOCS.mkdir(parents=True, exist_ok=True)
    DOCS_PUBLICOS.mkdir(parents=True, exist_ok=True)

    frames = []
    insumos = []
    mapa_estamento = {clave(v): v for v in ESTAMENTOS}
    mapeos = []
    for categoria in CATEGORIAS:
        ruta = DATOS / ARCHIVOS[categoria]
        df = pd.read_excel(ruta, sheet_name="Datos")
        if len(df) == 0:
            raise RuntimeError(f"Maestro vacío: {ruta}")
        if not df["version_esquema"].eq(VERSION_CANONICO).all():
            raise RuntimeError(f"Versión de esquema inesperada en {ruta}")
        insumos.append({
            "categoria": categoria,
            "archivo": ruta.name,
            "ruta_relativa": str(ruta.relative_to(ROOT)),
            "sha256": sha256(ruta),
            "registros": int(len(df)),
        })
        for valor in sorted(df["estamento"].map(texto).unique()):
            normalizado = mapa_estamento.get(clave(valor))
            mapeos.append({
                "categoria": categoria,
                "valor_observado": valor,
                "valor_canonico": normalizado,
                "registros": int((df["estamento"].map(texto) == valor).sum()),
                "transformacion": "identidad; comparación Unicode sin acentos y sin distinguir mayúsculas",
            })
        df["estamento_raw"] = df["estamento"].map(texto)
        df["estamento"] = df["estamento_raw"].map(lambda v: mapa_estamento.get(clave(v)))
        frames.append(df)

    no_mapeables = [m for m in mapeos if not m["valor_canonico"]]
    escribir_json("catalogo_estamentos.json", {
        "generado_desde": VERSION_CANONICO,
        "fecha_generacion": generado,
        "lista_cerrada": ESTAMENTOS,
        "mapeos": mapeos,
        "valores_no_mapeables": no_mapeables,
    })
    if no_mapeables:
        raise RuntimeError(f"Hay {len(no_mapeables)} valores de estamento no mapeables; revisar catalogo_estamentos.json")

    todo = pd.concat(frames, ignore_index=True)
    columnas_numericas = [c for c in todo.columns if c.endswith("_clp") or c.endswith("_horas")]
    for columna in columnas_numericas:
        todo[columna] = pd.to_numeric(todo[columna], errors="coerce").fillna(0)
    todo["periodo"] = todo["periodo"].astype(str)
    if set(todo["periodo"]) != set(PERIODOS):
        raise RuntimeError("La cobertura de períodos no coincide con los 36 meses esperados")
    if todo["registro_id"].duplicated().any():
        raise RuntimeError("registro_id duplicado en los maestros canónicos")

    # D-17 v1.1: unión exacta por categoría + cargo publicado; nunca modifica estamento.
    if sha256(MAPEO_ESTAMENTO) != SHA_MAPEO_ESTAMENTO:
        raise RuntimeError("El SHA-256 del mapeo D-17 no coincide con v1.1 aprobada")
    mapeo_estimado = pd.read_csv(MAPEO_ESTAMENTO, dtype=str, keep_default_na=False)
    mapeo_estimado["frecuencia"] = pd.to_numeric(mapeo_estimado["frecuencia"], errors="raise").astype(int)
    if mapeo_estimado.duplicated(["categoria", "cargo_funcion"]).any():
        raise RuntimeError("Clave duplicada en mapeo D-17")
    if set(mapeo_estimado["propuesta_version"]) != {"D-17_v1.1"} or set(mapeo_estimado["estado_revision"]) != {"aprobado_con_enmienda"}:
        raise RuntimeError("El mapeo D-17 no tiene versión/revisión aprobada v1.1")
    columnas_mapeo = {
        "estamento_estimado": "estamento_estimado",
        "estado_clasificacion": "estado_clasificacion_estimada",
        "regla_id": "regla_estamento_estimado",
        "origen_clasificacion": "origen_estamento_estimado",
        "justificacion": "justificacion_estamento_estimado",
    }
    todo = todo.merge(
        mapeo_estimado[["categoria", "cargo_funcion", *columnas_mapeo]].rename(columns=columnas_mapeo),
        on=["categoria", "cargo_funcion"], how="left", validate="many_to_one", sort=False,
    )
    for columna in columnas_mapeo.values():
        todo[columna] = todo[columna].map(texto)
    todo.loc[todo["estado_clasificacion_estimada"] == "no_clasificable", "estamento_estimado"] = ""
    todo["cargo_normalizado_proyecto"] = todo["cargo_funcion"].map(normalizar_cargo)
    faltantes_estimado = todo[todo["categoria"].isin(CATEGORIAS_ESTIMADAS) & todo["estado_clasificacion_estimada"].eq("")]
    if not faltantes_estimado.empty:
        raise RuntimeError(f"Hay {len(faltantes_estimado)} registros sin cobertura D-17 v1.1")
    cobertura_estimado = {}
    for categoria in CATEGORIAS_ESTIMADAS:
        grupo = todo[todo["categoria"] == categoria]
        clasificados = int(grupo["estado_clasificacion_estimada"].eq("clasificado").sum())
        no_clasificables = int(grupo["estado_clasificacion_estimada"].eq("no_clasificable").sum())
        cobertura_estimado[categoria] = {
            "clasificados": clasificados,
            "no_clasificables": no_clasificables,
            "totales": int(len(grupo)),
            "porcentaje_clasificados": round(clasificados / len(grupo) * 100, 4),
            "cargos_clasificados": int(mapeo_estimado[(mapeo_estimado["categoria"] == categoria) & (mapeo_estimado["estado_clasificacion"] == "clasificado")].shape[0]),
            "cargos_no_clasificables": int(mapeo_estimado[(mapeo_estimado["categoria"] == categoria) & (mapeo_estimado["estado_clasificacion"] == "no_clasificable")].shape[0]),
        }

    # Nomenclátor CPLT: conserva cada código, orden, duplicados y anomalías de origen.
    indice_asignaciones = json.loads(ASIGNACIONES_INDICE.read_text(encoding="utf-8"))
    conceptos_asignaciones = indice_asignaciones.get("conceptos", [])
    if indice_asignaciones.get("schema_version") != "1.0.0" or indice_asignaciones.get("total_conceptos") != 394 or len(conceptos_asignaciones) != 394:
        raise RuntimeError("El índice de asignaciones no coincide con el esquema 1.0.0 y los 394 conceptos esperados")
    codigos_indice = [texto(concepto.get("codigo")) for concepto in conceptos_asignaciones]
    if len(set(codigos_indice)) != 394 or any(not codigo or not texto(concepto.get("nombre")) for codigo, concepto in zip(codigos_indice, conceptos_asignaciones)):
        raise RuntimeError("El índice de asignaciones contiene códigos duplicados o conceptos incompletos")
    mapa_asignaciones = {texto(concepto["codigo"]): concepto for concepto in conceptos_asignaciones}
    todo["asignaciones_decodificadas"] = todo["asignaciones_especiales_raw"].map(lambda raw: decodificar_asignaciones(raw, mapa_asignaciones))
    con_asignaciones = todo[todo["asignaciones_especiales_raw"].map(texto).ne("")]
    asignaciones_anomalas = con_asignaciones[con_asignaciones["asignaciones_decodificadas"].map(lambda items: any(item["estado"] == "no_decodificado" for item in items))]
    cobertura_asignaciones = {
        "registros_con_codigos": int(len(con_asignaciones)),
        "registros_sin_codigos": int(len(todo) - len(con_asignaciones)),
        "registros_completamente_decodificados": int(len(con_asignaciones) - len(asignaciones_anomalas)),
        "registros_con_anomalias": int(len(asignaciones_anomalas)),
        "ocurrencias_decodificadas": int(sum(item["estado"] == "decodificado" for items in todo["asignaciones_decodificadas"] for item in items)),
        "ocurrencias_no_decodificadas": int(sum(item["estado"] == "no_decodificado" for items in todo["asignaciones_decodificadas"] for item in items)),
    }
    anomalias_asignaciones = [{
        "registro_id": texto(fila.registro_id), "id_trabajador": texto(fila.id_trabajador),
        "periodo": texto(fila.periodo), "categoria": texto(fila.categoria),
        "asignaciones_especiales_raw": texto(fila.asignaciones_especiales_raw),
        "fuente_archivo": texto(fila.fuente_archivo), "fuente_fila_csv": int(fila.fuente_fila_csv),
        "fuente_sha256": texto(fila.fuente_sha256),
    } for fila in asignaciones_anomalas.itertuples()]
    escribir_json("asignaciones_indice.json", {
        **{k: v for k, v in indice_asignaciones.items() if k not in {"fecha_generacion", "trazabilidad_proyecto", "conceptos"}},
        "generado_desde": VERSION_CANONICO,
        "version_pipeline": VERSION_PIPELINE,
        "fecha_generacion": generado,
        "insumo_proyecto": {
            "ruta_relativa": str(ASIGNACIONES_INDICE.relative_to(ROOT)),
            "sha256": sha256(ASIGNACIONES_INDICE),
            "canonico_modificado": False,
        },
        "cobertura_modulo": cobertura_asignaciones,
        "anomalias_observadas": anomalias_asignaciones,
        "limitacion": "La fuente publica qué conceptos aplican, no el monto de cada uno; los montos van incluidos en la remuneración bruta.",
        "conceptos": conceptos_asignaciones,
    })

    # SC-02: el glosario canónico es la única fuente de definiciones publicadas.
    glosario_registros = []
    seccion_glosario = ""
    entrada_glosario = None
    for linea in GLOSARIO.read_text(encoding="utf-8").splitlines():
        if linea.startswith("## "):
            seccion_glosario = linea[3:].strip()
            entrada_glosario = None
        elif linea.startswith("### ") and "✅" in linea:
            termino = linea[4:].split("—", 1)[0].strip()
            entrada_glosario = {
                "termino": termino,
                "seccion": seccion_glosario,
                "definicion": "",
                "fuente": "",
                "estado": "aprobada",
                "modulo_normativo": seccion_glosario != "Conceptos de la plataforma (propios del proyecto)",
            }
            glosario_registros.append(entrada_glosario)
        elif entrada_glosario is not None and linea.startswith("**Fuente:**"):
            entrada_glosario["fuente"] = linea.split("**Fuente:**", 1)[1].strip()
        elif entrada_glosario is not None and linea and not linea.startswith("**") and not entrada_glosario["definicion"]:
            entrada_glosario["definicion"] = linea.strip()
    terminos_glosario = [r["termino"] for r in glosario_registros]
    terminos_esperados = [
        "Planta", "Contrata", "Código del Trabajo", "Honorarios", "Estamento",
        "Directivo", "Profesional", "Técnico", "Administrativo", "Auxiliar",
        "Persona-mes", "No informa / No tiene", "Estamento estimado", "Trayectoria (convención D-15)",
        "Asignaciones especiales", "Transparencia trazable",
    ]
    if terminos_glosario != terminos_esperados or any(not r["definicion"] or not r["fuente"] for r in glosario_registros):
        raise RuntimeError("El glosario canónico no contiene exactamente las 16 entradas aprobadas esperadas")
    escribir_json("glosario_definiciones.json", {
        **base_artefacto(generado, ["termino"], glosario_registros),
        "fuente_unica": str(GLOSARIO.relative_to(ROOT)),
        "sha256": sha256(GLOSARIO),
        "terminos_pendientes_sin_definicion": ["Jefatura", "Alcalde", "Otro", "Honorarios (estamento publicado)", "No clasificable"],
    })

    trayectoria, resoluciones_d15 = proyectar_trayectoria(todo)
    unicidad, ficha_aprobada = validar_unicidad(trayectoria, resoluciones_d15, generado)
    escribir_json("validacion_unicidad.json", {
        k: v for k, v in unicidad.items() if k not in {"detalle_colisiones", "aliases_entre_categorias"}
    })
    nota_reconciliacion = (
        "Las fichas seleccionan una versión por persona y período conforme a D-15. "
        "Los agregados conservan todas las filas canónicas, incluidas las versiones alternas; "
        "por tanto, la suma de fichas no reconcilia con los agregados."
    )
    fichas_estado = {
        "fecha_generacion": generado,
        "habilitada": ficha_aprobada,
        "estado_validacion": unicidad["estado"],
        "colisiones_originales_id_periodo": unicidad["colisiones_originales_id_periodo"],
        "colisiones_id_periodo": unicidad["colisiones_id_periodo"],
        "registros_en_proyeccion_trayectoria": unicidad["registros_en_proyeccion_trayectoria"],
        "versiones_alternas": unicidad["versiones_alternas"],
        "nombres_con_varios_ids_entre_categorias": unicidad["nombres_con_varios_ids_entre_categorias"],
        "documento": "docs/VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md",
        "aviso": nota_reconciliacion,
        "fichas": [],
    }
    escribir_json("fichas_estado.json", fichas_estado)

    panel = agregar(todo, ["periodo", "categoria"], {
        "dotacion_registros": "registros",
        "gasto_bruto_clp": "bruta",
        "gasto_liquido_clp": "liquida",
        "registros_bruta_no_informa": "bruta_no_informa",
        "registros_bruta_informada": "bruta_informada",
        "promedio_bruto_clp": "bruta_promedio",
        "mediana_bruta_clp": "bruta_mediana",
    })
    escribir_json("panel_general_mensual.json", base_artefacto(generado, ["periodo", "categoria"], panel))

    estamento = agregar(todo, ["periodo", "categoria", "estamento"], {
        "dotacion_registros": "registros",
        "gasto_bruto_clp": "bruta",
        "registros_bruta_no_informa": "bruta_no_informa",
        "registros_bruta_informada": "bruta_informada",
        "promedio_bruto_clp": "bruta_promedio",
        "mediana_bruta_clp": "bruta_mediana",
    })
    escribir_json("composicion_estamento.json", base_artefacto(generado, ["periodo", "categoria", "estamento"], estamento))

    # D-17: dimensión adicional; «No clasificable» se materializa solo al agregar.
    estimado_para_agregar = todo[todo["categoria"].isin(CATEGORIAS_ESTIMADAS)].copy()
    estimado_para_agregar["estamento_estimado"] = estimado_para_agregar.apply(
        lambda fila: (
            "No clasificable"
            if fila["estado_clasificacion_estimada"] == "no_clasificable"
            else texto(fila["estamento_estimado"])
        ),
        axis=1,
    )
    estamento_estimado = agregar(
        estimado_para_agregar,
        ["periodo", "categoria", "estamento_estimado"],
        {
            "dotacion_registros": "registros",
            "gasto_bruto_clp": "bruta",
            "registros_bruta_no_informa": "bruta_no_informa",
            "registros_bruta_informada": "bruta_informada",
            "promedio_bruto_clp": "bruta_promedio",
            "mediana_bruta_clp": "bruta_mediana",
        },
    )
    escribir_json("composicion_estamento_estimado.json", {
        **base_artefacto(
            generado,
            ["periodo", "categoria", "estamento_estimado"],
            estamento_estimado,
        ),
        "decision": "D-17",
        "version_mapeo": "D-17_v1.1",
        "leyenda_fija": LEYENDA_ESTAMENTO_ESTIMADO,
        "fuente_mapeo": {
            "ruta_relativa": str(MAPEO_ESTAMENTO.relative_to(ROOT)),
            "sha256": SHA_MAPEO_ESTAMENTO,
        },
        "cobertura": cobertura_estimado,
    })

    genero_registros = []
    for (periodo, categoria, estamento_valor), grupo in todo.groupby(["periodo", "categoria", "estamento"], sort=True):
        conteos = grupo["genero"].map(texto).value_counts()
        femenino = int(conteos.get("Femenino", 0))
        masculino = int(conteos.get("Masculino", 0))
        otro = int(len(grupo) - femenino - masculino)
        total = int(len(grupo))
        genero_registros.append({
            "periodo": periodo,
            "categoria": categoria,
            "estamento": estamento_valor,
            "registros": total,
            "femenino": femenino,
            "masculino": masculino,
            "no_clasificado": otro,
            "femenino_pct": round(femenino / total * 100, 4) if total else None,
            "masculino_pct": round(masculino / total * 100, 4) if total else None,
            "leyenda": LEYENDA_GENERO,
            "trazabilidad": trazabilidad(grupo),
        })
    escribir_json("composicion_genero_agregada.json", {
        **base_artefacto(generado, ["periodo", "categoria", "estamento"], genero_registros),
        "leyenda_fija": LEYENDA_GENERO,
        "nota_privacidad": "Artefacto exclusivamente agregado. El género no se incluye en explorador_*.json ni en fichas.",
    })

    configuracion_horas = {
        "Planta": [
            ("Diurnas", "horas_extra_diurnas_horas", "horas_extra_diurnas_clp", "horas_extra_diurnas_raw"),
            ("Nocturnas", "horas_extra_nocturnas_horas", "horas_extra_nocturnas_clp", "horas_extra_nocturnas_raw"),
            ("Festivas", "horas_extra_festivas_horas", "horas_extra_festivas_clp", "horas_extra_festivas_raw"),
        ],
        "Contrata": [
            ("Diurnas", "horas_extra_diurnas_horas", "horas_extra_diurnas_clp", "horas_extra_diurnas_raw"),
            ("Nocturnas", "horas_extra_nocturnas_horas", "horas_extra_nocturnas_clp", "horas_extra_nocturnas_raw"),
            ("Festivas", "horas_extra_festivas_horas", "horas_extra_festivas_clp", "horas_extra_festivas_raw"),
        ],
        "Código del Trabajo": [
            ("Sin desagregar", "horas_extra_horas", "horas_extra_clp", "horas_extra_raw"),
        ],
    }
    horas_registros = []
    for categoria in CATEGORIAS:
        for periodo in PERIODOS:
            grupo = todo[(todo["categoria"] == categoria) & (todo["periodo"] == periodo)]
            if categoria == "Honorarios":
                horas_registros.append({
                    "periodo": periodo, "categoria": categoria, "tipo": "No publicado",
                    "estado": "ausencia_fuente", "horas": None, "monto_clp": None,
                    "registros": int(len(grupo)), "registros_cero_canonico": None,
                    "causa": "La fuente de Honorarios no publica horas extra.",
                    "trazabilidad": trazabilidad(grupo),
                })
                continue
            for tipo, col_horas, col_monto, col_raw in configuracion_horas[categoria]:
                horas_registros.append({
                    "periodo": periodo,
                    "categoria": categoria,
                    "tipo": tipo,
                    "estado": "publicado",
                    "horas": float(grupo[col_horas].sum()),
                    "monto_clp": int(grupo[col_monto].sum()),
                    "registros": int(len(grupo)),
                    "registros_cero_canonico": int((grupo[col_monto] == 0).sum()),
                    "registros_no_informa_explicito": int(grupo[col_raw].map(texto).str.casefold().eq("no informa").sum()),
                    "registros_no_tiene_explicito": int(grupo[col_raw].map(texto).str.casefold().eq("no tiene").sum()),
                    "causa": "Código del Trabajo no desagrega el tipo de hora." if categoria == "Código del Trabajo" else None,
                    "trazabilidad": trazabilidad(grupo),
                })
    escribir_json("horas_extra_mensual.json", base_artefacto(generado, ["periodo", "categoria", "tipo"], horas_registros))

    desvinculacion = []
    cod = todo[todo["categoria"] == "Código del Trabajo"]
    for periodo, grupo in cod.groupby("periodo", sort=True):
        desvinculacion.append({
            "periodo": periodo,
            "categoria": "Código del Trabajo",
            "monto_desvinculacion_clp": int(grupo["monto_desvinculacion_clp"].sum()),
            "registros": int(len(grupo)),
            "registros_cero_canonico": int((grupo["monto_desvinculacion_clp"] == 0).sum()),
            "trazabilidad": trazabilidad(grupo),
        })
    escribir_json("codigo_desvinculacion_mensual.json", base_artefacto(generado, ["periodo", "categoria"], desvinculacion))

    # Manifiesto vigente de informes: el detalle se une por registro_id, sin inferir estados.
    manifiesto_path = DATOS / "informes_honorarios" / "MANIFIESTO_DESCARGAS_v2.xlsx"
    manifiesto = pd.read_excel(manifiesto_path, sheet_name="Manifiesto")
    manifiesto = manifiesto.set_index("registro_id", drop=False)
    estados_informes = Counter(manifiesto["estado"].map(texto))
    informes_mensual = []
    for (periodo, estado), grupo in manifiesto.groupby(["periodo", "estado"], sort=True):
        informes_mensual.append({"periodo": str(periodo), "estado": texto(estado), "registros": int(len(grupo))})

    columnas_publicas = [
        "registro_id", "id_trabajador", "anio", "mes_numero", "mes_nombre", "periodo",
        "categoria", "nombre_original", "estamento", "estamento_raw", "cargo_funcion",
        "grado_eus_jornada", "calificacion_profesional", "region", "fecha_inicio_raw",
        "fecha_inicio", "fecha_termino_raw", "fecha_termino", "fecha_termino_tipo",
        "observaciones", "asignaciones_especiales_raw", "asignaciones_decodificadas", "remuneracion_bruta_raw",
        "remuneracion_bruta_clp", "remuneracion_liquida_raw", "remuneracion_liquida_clp",
        "viaticos_raw", "viaticos_clp", "remuneracion_adicional_raw", "remuneracion_adicional_clp",
        "bonos_incentivos_raw", "bonos_incentivos_clp", "monto_desvinculacion_raw",
        "monto_desvinculacion_clp", "derecho_horas_extra", "horas_extra_diurnas_raw",
        "horas_extra_diurnas_clp", "horas_extra_diurnas_horas", "horas_extra_nocturnas_raw",
        "horas_extra_nocturnas_clp", "horas_extra_nocturnas_horas", "horas_extra_festivas_raw",
        "horas_extra_festivas_clp", "horas_extra_festivas_horas", "horas_extra_raw",
        "horas_extra_clp", "horas_extra_horas", "horas_extra_desagregacion", "tipo_pago",
        "descripcion_pago", "numero_cuotas_raw", "numero_cuotas", "enlace_funciones_desarrolladas_raw",
        "enlace_funciones_desarrolladas_url", "fuente_archivo", "fuente_ruta_relativa",
        "fuente_fila_csv", "fuente_sha256", "fuente_encoding", "fuente_separador", "version_esquema",
        "periodo_nominal_archivo", "rol_trayectoria", "regla_resolucion", "version_alterna_de",
        "motivo_version_alterna", "estamento_estimado", "estado_clasificacion_estimada",
        "regla_estamento_estimado", "origen_estamento_estimado", "justificacion_estamento_estimado",
        "cargo_normalizado_proyecto",
    ]

    def registro_publico(fila: dict) -> dict:
        publico = {c: nativo(fila.get(c)) for c in columnas_publicas if c in fila}
        if fila["categoria"] == "Honorarios":
            publico["horas_extra_horas_total"] = None
            publico["horas_extra_monto_total"] = None
            if fila["registro_id"] in manifiesto.index:
                informe = manifiesto.loc[fila["registro_id"]]
                if isinstance(informe, pd.DataFrame):
                    raise RuntimeError(f"registro_id duplicado en manifiesto: {fila['registro_id']}")
                respaldo = texto(informe.get("archivo_relativo"))
                publico["informe_estado"] = texto(informe.get("estado"))
                publico["informe_archivo_respaldo"] = respaldo or None
                publico["informe_sha256"] = texto(informe.get("sha256")) or None
                publico["informe_respaldo_disponible"] = bool(respaldo and (ROOT / respaldo).is_file())
                publico["informe_fecha_verificacion"] = texto(informe.get("fecha_verificacion")) or None
        elif fila["categoria"] == "Código del Trabajo":
            publico["horas_extra_horas_total"] = float(fila["horas_extra_horas"])
            publico["horas_extra_monto_total"] = int(fila["horas_extra_clp"])
        else:
            publico["horas_extra_horas_total"] = float(sum(fila[c] for c in [
                "horas_extra_diurnas_horas", "horas_extra_nocturnas_horas", "horas_extra_festivas_horas",
            ]))
            publico["horas_extra_monto_total"] = int(sum(fila[c] for c in [
                "horas_extra_diurnas_clp", "horas_extra_nocturnas_clp", "horas_extra_festivas_clp",
            ]))
        publico["remuneracion_bruta_no_informa"] = bool(fila["remuneracion_bruta_clp"] == 0)
        publico["ficha_habilitada"] = bool(ficha_aprobada)
        return publico

    for anio in (2023, 2024, 2025):
        subset = trayectoria[trayectoria["anio"].astype(int) == anio]
        registros = [registro_publico(fila) for fila in subset.to_dict("records")]
        escribir_json(f"explorador_{anio}.json", {
            **base_artefacto(generado, ["registro_id"], registros),
            "anio": anio,
            "privacidad": "No contiene genero, primer_nombre ni nombre_normalizado. Las fichas no contienen género.",
            "nota_reconciliacion": nota_reconciliacion,
        }, compacto=True)

    fichas_dir = DATA / "fichas"
    if fichas_dir.exists():
        shutil.rmtree(fichas_dir)
    if ficha_aprobada:
        for id_trabajador, grupo in trayectoria.groupby("id_trabajador", sort=True):
            if grupo["categoria"].nunique() != 1:
                raise RuntimeError(f"El ID heredado cruza categorías y no admite ficha por categoría: {id_trabajador}")
            seleccionadas = grupo[grupo["rol_trayectoria"] == "canonica_trayectoria"]
            ultimo_registro = seleccionadas.sort_values("periodo").iloc[-1]
            entradas = []
            anterior_publicado = None
            for periodo in PERIODOS:
                del_periodo = grupo[grupo["periodo"] == periodo]
                canonica = del_periodo[del_periodo["rol_trayectoria"] == "canonica_trayectoria"]
                alternas = del_periodo[del_periodo["rol_trayectoria"] == "version_alterna"]
                if len(canonica) > 1:
                    raise RuntimeError(f"Colisión no resuelta en ficha: {id_trabajador} / {periodo}")
                publicado = registro_publico(canonica.iloc[0].to_dict()) if len(canonica) == 1 else None
                if publicado:
                    actual = canonica.iloc[0].to_dict()
                    publicado["analisis_cargo"] = (
                        analizar_cargo(actual["cargo_funcion"], anterior_publicado["cargo_funcion"], anterior_publicado["periodo"])
                        if anterior_publicado is not None
                        else {
                            "estado": "primer_registro",
                            "periodo_anterior": None,
                            "cargo_anterior": None,
                            "cargo_normalizado_proyecto": normalizar_cargo(actual["cargo_funcion"]),
                            "cargo_anterior_normalizado_proyecto": None,
                            "explicacion": "Primer período publicado de esta trayectoria; no existe comparación anterior.",
                        }
                    )
                    anterior_publicado = actual
                entradas.append({
                    "periodo": periodo,
                    "estado": "publicado" if len(canonica) == 1 else "sin_registro_publicado",
                    "causa_ausencia": None if len(canonica) == 1 else "No hay un registro de este ID y categoría en el canónico para este período; no se imputa ni interpola.",
                    "registro": publicado,
                    "versiones_alternas": [registro_publico(fila) for fila in alternas.sort_values("registro_id").to_dict("records")],
                })
            periodos_publicados = [e["periodo"] for e in entradas if e["registro"]]
            ficha = {
                "generado_desde": VERSION_CANONICO,
                "version_pipeline": VERSION_PIPELINE,
                "fecha_generacion": generado,
                "id_trabajador": texto(id_trabajador),
                "categoria": texto(ultimo_registro["categoria"]),
                "nombre_original": texto(ultimo_registro["nombre_original"]),
                "nombres_publicados": sorted({texto(v) for v in grupo["nombre_original"] if texto(v)}),
                "cargos": sorted({texto(v) for v in grupo["cargo_funcion"] if texto(v)}),
                "estamentos": sorted({texto(v) for v in grupo["estamento"] if texto(v)}),
                "periodo_inicio": min(PERIODOS),
                "periodo_fin": max(PERIODOS),
                "conteos": {
                    "periodos_publicados": len(periodos_publicados),
                    "ausencias": len(PERIODOS) - len(periodos_publicados),
                    "versiones_alternas": int((grupo["rol_trayectoria"] == "version_alterna").sum()),
                    "registros_fuente_conservados": int(len(grupo)),
                },
                "regla_resolucion": "D-15_coincidencia_periodo_nominal",
                "nota_reconciliacion": nota_reconciliacion,
                "privacidad": "No contiene género, primer_nombre ni nombre_normalizado.",
                "trayectoria": entradas,
            }
            destino = escribir_json(f"fichas/{id_trabajador}.json", ficha, compacto=True)
            fichas_estado["fichas"].append({
                "id_trabajador": texto(id_trabajador),
                "categoria": texto(ultimo_registro["categoria"]),
                "nombre_original": texto(ultimo_registro["nombre_original"]),
                "archivo": f"fichas/{id_trabajador}.json",
                "periodos_publicados": len(periodos_publicados),
                "ausencias": len(PERIODOS) - len(periodos_publicados),
                "versiones_alternas": ficha["conteos"]["versiones_alternas"],
                "bytes": destino.stat().st_size,
                "sha256": sha256(destino),
            })
        fichas_estado["conteo_fichas"] = len(fichas_estado["fichas"])
        escribir_json("fichas_estado.json", fichas_estado)

    ultimo = max(PERIODOS)
    resumen_categorias = {}
    for categoria in CATEGORIAS:
        subset = todo[(todo["categoria"] == categoria) & (todo["periodo"] == ultimo)].copy()
        subset["rango_remuneracion"] = subset["remuneracion_bruta_clp"].map(rango_remuneracion)
        distribucion = []
        for rango, grupo in subset.groupby("rango_remuneracion", sort=True):
            distribucion.append({
                "rango": rango, "registros": int(len(grupo)), "trazabilidad": trazabilidad(grupo),
            })
        subset["anio_inicio"] = subset["fecha_inicio"].map(lambda v: texto(v)[:4] if texto(v) else "No informa / no parseable")
        antiguedad = []
        for anio_inicio, grupo in subset.groupby("anio_inicio", sort=True):
            antiguedad.append({
                "anio_inicio": anio_inicio, "registros": int(len(grupo)), "trazabilidad": trazabilidad(grupo),
            })
        especificos = {}
        if categoria == "Honorarios":
            especificos = {
                "tipo_pago": [{"valor": texto(k) or "No informa", "registros": int(v)} for k, v in subset["tipo_pago"].value_counts(dropna=False).items()],
                "numero_cuotas": [{"valor": texto(k) or "No informa / no aplica", "registros": int(v)} for k, v in subset["numero_cuotas"].value_counts(dropna=False).items()],
                "informes_estados": dict(estados_informes),
                "informes_por_mes": informes_mensual,
                "nota_respaldo": "Los enlaces apuntan al respaldo documental del proyecto; no se duplican 2,36 GB de PDF dentro de plataforma/.",
            }
        resumen_categorias[categoria] = {
            "periodo_referencia": ultimo,
            "distribucion_remuneraciones": distribucion,
            "antiguedad_por_anio_inicio": antiguedad,
            "especificos": especificos,
        }
    escribir_json("resumen_estamental.json", {
        "generado_desde": VERSION_CANONICO,
        "fecha_generacion": generado,
        "categorias": resumen_categorias,
    })

    inventario = pd.read_excel(DOCS / "INVENTARIO_FUENTES_v1.xlsx", sheet_name="CSV fuente")
    fuentes_registros = []
    rutas_modulo = set(todo["fuente_ruta_relativa"].map(texto))
    for ruta in sorted(rutas_modulo):
        origen_csv = ROOT / ruta
        destino_csv = ROOT / "plataforma" / respaldo_csv(ruta)
        destino_csv.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen_csv, destino_csv)
        if sha256(origen_csv) != sha256(destino_csv):
            raise RuntimeError(f"La copia pública no conserva el SHA-256: {ruta}")
    for fila in inventario.to_dict("records"):
        ruta = texto(fila["ruta_relativa"])
        subset = todo[todo["fuente_ruta_relativa"].map(texto) == ruta]
        fuentes_registros.append(registro_limpio({
            "categoria_inventario": fila["categoria"],
            "archivo": fila["archivo"],
            "ruta_relativa": ruta,
            "url_respaldo": respaldo_csv(ruta) if ruta in rutas_modulo else None,
            "filas": fila["filas"],
            "columnas": fila["columnas"],
            "encoding": fila["encoding"],
            "separador": fila["separador"],
            "anios_contenido": fila["anios_contenido"],
            "meses_contenido": fila["meses_contenido"],
            "fuente_sha256": fila["sha256"],
            "estado": "procesado_en_modulo" if ruta in rutas_modulo else "fuera_de_alcance_autoridades",
            "periodos_modulo": sorted(subset["periodo"].unique().tolist()),
            "registros_modulo": int(len(subset)),
            "portal_oficial": PORTAL_OFICIAL,
        }))
    escribir_json("fuentes.json", {
        "generado_desde": VERSION_CANONICO,
        "fecha_generacion": generado,
        "portal_oficial": PORTAL_OFICIAL,
        "conteos": {
            "archivos_inventariados": int(len(fuentes_registros)),
            "archivos_modulo": len(rutas_modulo),
            "archivos_fuera_alcance": int(len(fuentes_registros) - len(rutas_modulo)),
        },
        "maestros_canonicos": insumos,
        "manifiesto_informes": {
            "ruta_relativa": str(manifiesto_path.relative_to(ROOT)),
            "sha256": sha256(manifiesto_path),
            "estados": dict(estados_informes),
            "archivos_unicos_verificados": 5991,
            "bytes_unicos": 2360241736,
        },
        "registros": fuentes_registros,
    })

    ausencias = []
    for periodo in PERIODOS:
        ausencias.append({
            "periodo": periodo, "categoria": "Honorarios", "dimension": "horas_extra",
            "estado": "no_publicado_en_fuente", "causa": "Honorarios no publica horas extra; no se imputan ceros.",
        })
        ausencias.append({
            "periodo": periodo, "categoria": "Código del Trabajo", "dimension": "desagregacion_horas_extra",
            "estado": "no_desagregado_en_fuente", "causa": "La fuente publica horas y monto genéricos, sin diurnas/nocturnas/festivas.",
        })
    ausencias += [
        {
            "periodo": "2023-01/2025-12", "categoria": "Todas", "dimension": "unidad_organizacional",
            "estado": "ausencia_estructural", "causa": "La fuente no publica dirección o departamento; no se deriva desde el cargo.",
        },
        {
            "periodo": "2023-01/2023-12", "categoria": "Autoridades", "dimension": "cobertura",
            "estado": "fuera_de_los_cuatro_maestros", "causa": "Autoridades 2023 no publicadas; pendiente TP-05. El panel cubre dotación funcionaria, no autoridades electas.",
        },
        {
            "periodo": "2023-01/2025-12", "categoria": "Todas", "dimension": "reconciliacion_fichas_agregados",
            "estado": "no_reconcilia_por_proyeccion_D15", "causa": nota_reconciliacion,
        },
        {
            "periodo": "2023-01/2025-12", "categoria": "Todas", "dimension": "licencia_reutilizacion",
            "estado": "declarada_D16",
            "causa": "D-16: código de la plataforma bajo MIT; datos agregados y artefactos derivados del proyecto (JSON y CSV exportables) bajo CC BY 4.0 con atribución al Portal de Transparencia Trazable. Estas licencias no se atribuyen al municipio ni alteran la condición pública de los datos originales obtenidos por transparencia activa conforme a la Ley 20.285.",
        },
    ]
    escribir_json("ausencias.json", {
        **base_artefacto(generado, ["periodo", "categoria", "dimension"], ausencias),
        "periodos_sin_archivo_en_cuatro_categorias": [],
        "informes_honorarios": {
            "sin_url": int(estados_informes.get("sin_url", 0)),
            "dropbox_file_deleted": int(estados_informes.get("dropbox_file_deleted", 0)),
            "dropbox_link_temporarily_disabled": int(estados_informes.get("dropbox_link_temporarily_disabled", 0)),
            "nota": "Los estados se conservan por registro en explorador_*.json; no se reinterpretan como ceros ni descargas exitosas.",
        },
    })

    esperados = pd.read_excel(DOCS / "VALIDACION_FINAL_v1.xlsx", sheet_name="Totales canónicos").set_index("maestro")
    controles = []
    for categoria in CATEGORIAS:
        grupo = todo[todo["categoria"] == categoria]
        esperado = esperados.loc[categoria]
        valores = {
            "registros": int(len(grupo)),
            "trabajadores_id": int(grupo["id_trabajador"].nunique()),
            "bruta_clp": int(grupo["remuneracion_bruta_clp"].sum()),
            "liquida_clp": int(grupo["remuneracion_liquida_clp"].sum()),
        }
        if categoria in ("Planta", "Contrata"):
            valores.update({
                "horas_diurnas": float(grupo["horas_extra_diurnas_horas"].sum()),
                "horas_nocturnas": float(grupo["horas_extra_nocturnas_horas"].sum()),
                "horas_festivas": float(grupo["horas_extra_festivas_horas"].sum()),
            })
        if categoria == "Código del Trabajo":
            valores["horas_sin_desagregar"] = float(grupo["horas_extra_horas"].sum())
        for metrica, actual in valores.items():
            valor_esperado = esperado[metrica]
            if pd.isna(valor_esperado):
                continue
            esperado_num = float(valor_esperado)
            controles.append({
                "categoria": categoria, "control": metrica,
                "esperado": nativo(valor_esperado), "actual": actual,
                "resultado": "APROBADO" if float(actual) == esperado_num else "FALLA",
            })
    genero_ausente_de_explorador = all(
        "genero" not in r
        for anio in (2023, 2024, 2025)
        for r in json.loads((DATA / f"explorador_{anio}.json").read_text(encoding="utf-8"))["registros"]
    )

    def sin_campos_privados(valor) -> bool:
        if isinstance(valor, dict):
            return all(k not in {"genero", "primer_nombre", "nombre_normalizado"} and sin_campos_privados(v) for k, v in valor.items())
        if isinstance(valor, list):
            return all(sin_campos_privados(v) for v in valor)
        return True

    genero_ausente_de_fichas = all(
        sin_campos_privados(json.loads((DATA / f["archivo"]).read_text(encoding="utf-8")))
        for f in fichas_estado["fichas"]
    )
    ficha_plt = json.loads((DATA / "fichas" / "PLT-2023-0032.json").read_text(encoding="utf-8")) if ficha_aprobada else {}
    ficha_cot = json.loads((DATA / "fichas" / "COT-2023-0015.json").read_text(encoding="utf-8")) if ficha_aprobada else {}
    huecos_plt = [e["periodo"] for e in ficha_plt.get("trayectoria", []) if e["estado"] == "sin_registro_publicado"]
    esperados_huecos_plt = [p for p in PERIODOS if "2023-08" <= p <= "2024-08" or p == "2024-12"]
    seleccion_esperada = {
        "PLT-2023-0032": ("2024-11", "PLT-202411-8247F5515D", "PLT-202411-3B54A1958D"),
        "COT-2023-0015": ("2025-05", "COT-202505-8DA800BA00", "COT-202505-9D0CE3F70A"),
    }
    seleccion_actual = {}
    referencias_alternas_validas = True
    for id_trabajador, (periodo, seleccionado, alterno) in seleccion_esperada.items():
        ficha = ficha_plt if id_trabajador == "PLT-2023-0032" else ficha_cot
        entrada = next((e for e in ficha.get("trayectoria", []) if e["periodo"] == periodo), {})
        registro = entrada.get("registro") or {}
        alternas = entrada.get("versiones_alternas") or []
        seleccion_actual[id_trabajador] = {
            "seleccionado": registro.get("registro_id"),
            "alterno": alternas[0].get("registro_id") if len(alternas) == 1 else None,
        }
        referencias_alternas_validas = referencias_alternas_validas and len(alternas) == 1 and alternas[0].get("version_alterna_de") == seleccionado
        seleccion_actual[id_trabajador]["correcta"] = registro.get("registro_id") == seleccionado and seleccion_actual[id_trabajador]["alterno"] == alterno
    extras = [
        ("unicidad_en_proyeccion_d15", 0, unicidad["colisiones_id_periodo"]),
        ("registros_seleccionados_trayectoria", 22938, unicidad["registros_en_proyeccion_trayectoria"]),
        ("versiones_alternas_preservadas", 2, unicidad["versiones_alternas"]),
        ("fichas_individuales_generadas", 1068, len(fichas_estado["fichas"])),
        ("plt_2023_0032_periodos_publicados", 22, ficha_plt.get("conteos", {}).get("periodos_publicados")),
        ("plt_2023_0032_ausencias_exactas", esperados_huecos_plt, huecos_plt),
        ("cot_2023_0015_periodos_publicados", 7, ficha_cot.get("conteos", {}).get("periodos_publicados")),
        ("seleccion_nominal_d15_exacta", True, all(v["correcta"] for v in seleccion_actual.values())),
        ("referencias_version_alterna_validas", True, referencias_alternas_validas),
        ("genero_ausente_de_fichas", True, genero_ausente_de_fichas),
    ]
    for control, esperado, actual in extras:
        controles.append({
            "categoria": "Todas", "control": control, "esperado": esperado, "actual": actual,
            "resultado": "APROBADO" if actual == esperado else "FALLA",
        })
    controles += [
        {"categoria": "Todas", "control": "total_registros", "esperado": 22940, "actual": int(len(todo)), "resultado": "APROBADO" if len(todo) == 22940 else "FALLA"},
        {"categoria": "Todas", "control": "panel_suma_registros", "esperado": 22940, "actual": sum(r["dotacion_registros"] for r in panel), "resultado": "APROBADO" if sum(r["dotacion_registros"] for r in panel) == 22940 else "FALLA"},
        {"categoria": "Todas", "control": "estamento_suma_registros", "esperado": 22940, "actual": sum(r["dotacion_registros"] for r in estamento), "resultado": "APROBADO" if sum(r["dotacion_registros"] for r in estamento) == 22940 else "FALLA"},
        {"categoria": "Todas", "control": "genero_suma_registros", "esperado": 22940, "actual": sum(r["registros"] for r in genero_registros), "resultado": "APROBADO" if sum(r["registros"] for r in genero_registros) == 22940 else "FALLA"},
        {"categoria": "Todas", "control": "estamentos_no_mapeables", "esperado": 0, "actual": len(no_mapeables), "resultado": "APROBADO" if not no_mapeables else "FALLA"},
        {"categoria": "Todas", "control": "cobertura_36_meses", "esperado": 36, "actual": todo["periodo"].nunique(), "resultado": "APROBADO" if todo["periodo"].nunique() == 36 else "FALLA"},
        {"categoria": "Todas", "control": "genero_ausente_de_explorador", "esperado": True, "actual": genero_ausente_de_explorador, "resultado": "APROBADO" if genero_ausente_de_explorador else "FALLA"},
    ]

    # SC-01/SC-03: cada período × categoría debe reconciliar segmentos y barra.
    metricas_segmentos = ["dotacion_registros", "gasto_bruto_clp", "registros_bruta_no_informa"]
    for nombre, segmentos, campo, categorias in [
        ("publicado", estamento, "estamento", CATEGORIAS),
        ("estimado", estamento_estimado, "estamento_estimado", CATEGORIAS_ESTIMADAS),
    ]:
        for metrica in metricas_segmentos:
            discrepancias = []
            for barra in panel:
                if barra["categoria"] not in categorias:
                    continue
                total_segmentos = sum(
                    r[metrica]
                    for r in segmentos
                    if r["periodo"] == barra["periodo"] and r["categoria"] == barra["categoria"]
                )
                if total_segmentos != barra[metrica]:
                    discrepancias.append({
                        "periodo": barra["periodo"],
                        "categoria": barra["categoria"],
                        "barra": barra[metrica],
                        "segmentos": total_segmentos,
                    })
            controles.append({
                "categoria": "Todas",
                "control": f"segmentos_{nombre}_igual_barra_{metrica}",
                "esperado": 0,
                "actual": len(discrepancias),
                "detalle_discrepancias": discrepancias,
                "resultado": "APROBADO" if not discrepancias else "FALLA",
            })

    cobertura_esperada = {
        "Código del Trabajo": {
            "clasificados": 924, "no_clasificables": 9, "totales": 933,
            "cargos_clasificados": 21, "cargos_no_clasificables": 4,
        },
        "Honorarios": {
            "clasificados": 5516, "no_clasificables": 3948, "totales": 9464,
            "cargos_clasificados": 967, "cargos_no_clasificables": 659,
        },
    }
    for categoria, esperado in cobertura_esperada.items():
        actual = {k: v for k, v in cobertura_estimado[categoria].items() if k in esperado}
        controles.append({
            "categoria": categoria, "control": "cobertura_estamento_estimado_v1_1",
            "esperado": esperado, "actual": actual,
            "resultado": "APROBADO" if actual == esperado else "FALLA",
        })
    enmiendas_m01 = mapeo_estimado[
        mapeo_estimado["cargo_funcion"].isin(["INFORMATICO", "INFOMATICO"])
    ]
    m01_correcta = (
        len(enmiendas_m01) == 2
        and enmiendas_m01["estamento_estimado"].eq("Técnico").all()
        and enmiendas_m01["regla_id"].eq("M01").all()
        and enmiendas_m01["origen_clasificacion"].eq("revisión manual del propietario").all()
    )
    no_clasificable_agregado = sum(
        r["dotacion_registros"] for r in estamento_estimado
        if r["estamento_estimado"] == "No clasificable"
    )
    pruebas_cargo = {
        "normalizacion_acentos_puntuacion_variante": analizar_cargo(
            "Jefatura - Departamento", "JEFATURA DEPARTAMENTO", "2023-01"
        )["estado"] == "variante_escritura",
        "normalizacion_abreviaturas_variante": analizar_cargo(
            "ADM. de Personal", "ADMINISTRATIVO DE PERSONAL", "2023-01"
        )["estado"] == "variante_escritura",
        "normalizacion_unidad_posible_variante": analizar_cargo(
            "Funcionario Departamento", "Funcionario", "2023-01"
        )["estado"] == "posible_variante",
        "normalizacion_diferencia_real_cambio": analizar_cargo(
            "Profesional", "Auxiliar", "2023-01"
        )["estado"] == "cambio_cargo",
    }
    ocurrencias_asignaciones_conservadas = all(
        len(items) == (len(re.findall(r"\([^()]*\)", texto(raw))) if re.fullmatch(r"(?:\([^()]*\))+", texto(raw)) else 1)
        for raw, items in zip(todo["asignaciones_especiales_raw"], todo["asignaciones_decodificadas"])
        if texto(raw)
    )
    nombres_asignaciones_exactos = all(
        item["nombre"] == mapa_asignaciones[item["codigo"]]["nombre"]
        for items in todo["asignaciones_decodificadas"] for item in items
        if item["estado"] == "decodificado"
    )
    fila_duplicados = todo[(todo["id_trabajador"] == "PLT-2023-0032") & (todo["periodo"] == "2023-01")].iloc[0]
    duplicado_04_conservado = sum(item["codigo"] == "04" for item in fila_duplicados["asignaciones_decodificadas"]) == 2
    entrada_asignaciones = next(r for r in glosario_registros if r["termino"] == "Asignaciones especiales")
    limitacion_asignaciones = "la fuente publica qué conceptos aplican, no el monto de cada uno; los montos van incluidos en la remuneración bruta"
    controles_nuevos = [
        ("Todas", "mapeo_estimado_filas_v1_1", 1651, len(mapeo_estimado)),
        ("Todas", "mapeo_estimado_claves_duplicadas", 0, int(mapeo_estimado.duplicated(["categoria", "cargo_funcion"]).sum())),
        ("Todas", "mapeo_estimado_sha256_aprobado", SHA_MAPEO_ESTAMENTO, sha256(MAPEO_ESTAMENTO)),
        ("Todas", "registros_sin_cobertura_estimado", 0, len(faltantes_estimado)),
        ("Todas", "no_clasificable_visible_en_agregado", 3957, no_clasificable_agregado),
        ("Todas", "enmienda_m01_informatico_infomatico", True, m01_correcta),
        *[("Todas", nombre, True, actual) for nombre, actual in pruebas_cargo.items()],
        ("Todas", "asignaciones_indice_394_conceptos", 394, len(conceptos_asignaciones)),
        ("Todas", "asignaciones_registros_con_codigos", 13476, cobertura_asignaciones["registros_con_codigos"]),
        ("Todas", "asignaciones_registros_completamente_decodificados", 13475, cobertura_asignaciones["registros_completamente_decodificados"]),
        ("Todas", "asignaciones_anomalia_exacta", [("PLT-202301-95B4374AC0", "-4")], [(a["registro_id"], a["asignaciones_especiales_raw"]) for a in anomalias_asignaciones]),
        ("Todas", "asignaciones_ocurrencias_orden_y_duplicados_conservados", True, ocurrencias_asignaciones_conservadas),
        ("Todas", "asignaciones_nombres_oficiales_exactos", True, nombres_asignaciones_exactos),
        ("Todas", "asignaciones_duplicado_04_visible_en_ficha", True, duplicado_04_conservado),
        ("Todas", "asignaciones_glosario_limitacion_exacta", True, limitacion_asignaciones.casefold() in entrada_asignaciones["definicion"].casefold()),
    ]
    for categoria, control, esperado, actual in controles_nuevos:
        controles.append({
            "categoria": categoria, "control": control, "esperado": esperado, "actual": actual,
            "resultado": "APROBADO" if actual == esperado else "FALLA",
        })

    # SC-05: recalcular independientemente cada estadística desde el canónico.
    for nombre, registros_agregados, claves, fuente_datos in [
        ("panel", panel, ["periodo", "categoria"], todo),
        ("estamento_publicado", estamento, ["periodo", "categoria", "estamento"], todo),
        ("estamento_estimado", estamento_estimado, ["periodo", "categoria", "estamento_estimado"], estimado_para_agregar),
    ]:
        discrepancias = {"conteos_no_informa": [], "promedio": [], "mediana": []}
        for agregado in registros_agregados:
            mascara = pd.Series(True, index=fuente_datos.index)
            for clave_grupo in claves:
                mascara &= fuente_datos[clave_grupo].eq(agregado[clave_grupo])
            grupo = fuente_datos[mascara]
            valores_informados = grupo.loc[grupo["remuneracion_bruta_clp"] > 0, "remuneracion_bruta_clp"]
            esperado_conteos = {
                "registros_bruta_no_informa": int((grupo["remuneracion_bruta_clp"] == 0).sum()),
                "registros_bruta_informada": int(len(valores_informados)),
                "dotacion_registros": int(len(grupo)),
            }
            actual_conteos = {k: agregado[k] for k in esperado_conteos}
            if actual_conteos != esperado_conteos:
                discrepancias["conteos_no_informa"].append({"clave": {k: agregado[k] for k in claves}, "esperado": esperado_conteos, "actual": actual_conteos})
            esperado_promedio = float(valores_informados.mean()) if len(valores_informados) else None
            esperado_mediana = float(valores_informados.median()) if len(valores_informados) else None
            if agregado["promedio_bruto_clp"] != esperado_promedio:
                discrepancias["promedio"].append({"clave": {k: agregado[k] for k in claves}, "esperado": esperado_promedio, "actual": agregado["promedio_bruto_clp"]})
            if agregado["mediana_bruta_clp"] != esperado_mediana:
                discrepancias["mediana"].append({"clave": {k: agregado[k] for k in claves}, "esperado": esperado_mediana, "actual": agregado["mediana_bruta_clp"]})
        for metrica, diferencias in discrepancias.items():
            controles.append({
                "categoria": "Todas", "control": f"sc05_{nombre}_{metrica}",
                "esperado": 0, "actual": len(diferencias), "detalle_discrepancias": diferencias,
                "resultado": "APROBADO" if not diferencias else "FALLA",
            })
    for control, esperado, actual in [
        ("sc02_glosario_16_entradas_aprobadas", 16, len(glosario_registros)),
        ("sc02_glosario_terminos_canonicos_exactos", terminos_esperados, terminos_glosario),
    ]:
        controles.append({
            "categoria": "Todas", "control": control, "esperado": esperado, "actual": actual,
            "resultado": "APROBADO" if actual == esperado else "FALLA",
        })
    fallas = [c for c in controles if c["resultado"] != "APROBADO"]
    validacion = {
        "fecha_generacion": generado,
        "referencia": "documentación/04_Personal_y_Remuneraciones/VALIDACION_FINAL_v1.xlsx — Totales canónicos",
        "controles": controles,
        "resumen": {"controles": len(controles), "aprobadas": len(controles) - len(fallas), "fallas": len(fallas)},
        "resultado": "APROBADO" if not fallas else "FALLA",
    }
    escribir_json("validacion_agregados.json", validacion)
    if fallas:
        raise RuntimeError(f"Fallaron {len(fallas)} controles de agregados: {fallas}")

    meta = {
        "modulo": "Personal y Remuneraciones",
        "version": VERSION_PIPELINE,
        "generado_desde": VERSION_CANONICO,
        "fecha_generacion": generado,
        "periodo_inicio": min(PERIODOS),
        "periodo_fin": max(PERIODOS),
        "ultimo_periodo": ultimo,
        "portal_oficial": PORTAL_OFICIAL,
        "conteos": {
            "registros_totales": int(len(todo)),
            "registros_por_categoria": {c: int((todo["categoria"] == c).sum()) for c in CATEGORIAS},
            "trabajadores_id_por_categoria": {c: int(todo[todo["categoria"] == c]["id_trabajador"].nunique()) for c in CATEGORIAS},
            "archivos_fuente_modulo": len(rutas_modulo),
            "periodos": int(todo["periodo"].nunique()),
            "registros_bruta_no_informa": int((todo["remuneracion_bruta_clp"] == 0).sum()),
            "registros_en_proyeccion_trayectoria": unicidad["registros_en_proyeccion_trayectoria"],
            "versiones_alternas": unicidad["versiones_alternas"],
            "fichas_individuales": len(fichas_estado["fichas"]),
        },
        "totales_por_categoria": {
            c: {
                "gasto_bruto_clp": int(todo[todo["categoria"] == c]["remuneracion_bruta_clp"].sum()),
                "gasto_liquido_clp": int(todo[todo["categoria"] == c]["remuneracion_liquida_clp"].sum()),
                "registros_bruta_no_informa": int((todo[todo["categoria"] == c]["remuneracion_bruta_clp"] == 0).sum()),
            } for c in CATEGORIAS
        },
        "validacion_agregados": validacion["resumen"] | {"resultado": validacion["resultado"]},
        "ficha_individual": {
            "habilitada": ficha_aprobada,
            "estado_validacion": unicidad["estado"],
            "colisiones_originales_id_periodo": unicidad["colisiones_originales_id_periodo"],
            "colisiones_resueltas_d15": unicidad["colisiones_resueltas_d15"],
            "colisiones_id_periodo": unicidad["colisiones_id_periodo"],
            "regla_resolucion": "D-15_coincidencia_periodo_nominal",
            "nota_reconciliacion": nota_reconciliacion,
        },
        "estamento_estimado": {
            "decision": "D-17",
            "version_mapeo": "D-17_v1.1",
            "leyenda_fija": LEYENDA_ESTAMENTO_ESTIMADO,
            "fuente_mapeo": {
                "ruta_relativa": str(MAPEO_ESTAMENTO.relative_to(ROOT)),
                "sha256": SHA_MAPEO_ESTAMENTO,
            },
            "categorias_cubiertas": CATEGORIAS_ESTIMADAS,
            "cobertura": cobertura_estimado,
            "no_sobrescribe": "estamento",
        },
        "glosario": {
            "fuente_unica": str(GLOSARIO.relative_to(ROOT)),
            "sha256": sha256(GLOSARIO),
            "entradas_aprobadas": len(glosario_registros),
        },
        "asignaciones_especiales": {
            "indice": "asignaciones_indice.json",
            "conceptos": len(conceptos_asignaciones),
            "cobertura": cobertura_asignaciones,
            "limitacion": "La fuente publica qué conceptos aplican, no el monto de cada uno; los montos van incluidos en la remuneración bruta.",
        },
        "licencias": {
            "decision": "D-16",
            "codigo": "MIT",
            "datos_derivados": "CC BY 4.0",
            "atribucion": "Portal de Transparencia Trazable — Municipalidad de Coronel",
            "datos_originales": "Datos públicos de la Municipalidad de Coronel obtenidos por transparencia activa conforme a la Ley 20.285; las licencias del proyecto no se atribuyen al municipio.",
        },
        "privacidad": {"genero": "solo_agregado", "leyenda": LEYENDA_GENERO},
        "artefactos": {},
    }
    # El manifiesto se calcula antes de escribir meta para no autorreferenciar su hash.
    for ruta in sorted(DATA.glob("*.json")):
        if ruta.name == "meta.json":
            continue
        meta["artefactos"][ruta.name] = {"bytes": ruta.stat().st_size, "sha256": sha256(ruta)}
    escribir_json("meta.json", meta)

    # Copias documentales para que el sitio desplegado conserve sus enlaces metodológicos.
    for origen in [
        ROOT / "diseño" / "MODULO_PERSONAL_Y_REMUNERACIONES_v1.md",
        GLOSARIO,
        DOCS / "DICCIONARIO_DATOS_v1.md",
        DOCS / "VALIDACION_FINAL_v1.md",
        DOCS / "BITACORA_TRANSFORMACIONES_v1.md",
        DOCS / "REGISTRO_HALLAZGOS_v1.md",
        SALIDA_DOCS / "VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md",
        SALIDA_DOCS / "BITACORA_CONSTRUCCION_MODULO_PERSONAL_v1.md",
        SALIDA_DOCS / "CHECKLIST_VERIFICACION_MODULO_PERSONAL_v1.md",
    ]:
        if origen.is_file():
            shutil.copyfile(origen, DOCS_PUBLICOS / origen.name)

    print(json.dumps({
        "resultado": "APROBADO",
        "registros": len(todo),
        "por_categoria": meta["conteos"]["registros_por_categoria"],
        "controles_agregados": validacion["resumen"],
        "unicidad": unicidad["estado"],
        "colisiones_id_periodo": unicidad["colisiones_id_periodo"],
        "ficha_individual": "HABILITADA" if ficha_aprobada else "DESHABILITADA",
        "fichas_generadas": len(fichas_estado["fichas"]),
        "registros_en_proyeccion_trayectoria": unicidad["registros_en_proyeccion_trayectoria"],
        "versiones_alternas": unicidad["versiones_alternas"],
        "estamentos_no_mapeables": len(no_mapeables),
        "artefactos_json_raiz": len(meta["artefactos"]) + 1,
        "artefactos_json_totales": len(meta["artefactos"]) + 1 + len(fichas_estado["fichas"]),
        "salida": str(DATA.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
