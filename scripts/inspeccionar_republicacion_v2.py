from pathlib import Path
import json
import pdfplumber

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
PDF = ROOT / "datos crudos" / "07_Información_Presupuestaria" / "Balance de Ejecución Presupuestaria" / "2023" / "2023bep ene municipalidad ingresov2.pdf"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "republicacion_v2"
OUT.mkdir(parents=True, exist_ok=True)

resultado = []
with pdfplumber.open(PDF) as pdf:
    for numero, pagina in enumerate(pdf.pages, 1):
        palabras = pagina.extract_words(x_tolerance=1, y_tolerance=2)
        lineas = []
        for palabra in sorted(palabras, key=lambda w: (w["top"], w["x0"])):
            if not lineas or abs(lineas[-1][0]["top"] - palabra["top"]) > 2:
                lineas.append([palabra])
            else:
                lineas[-1].append(palabra)
        detalle = []
        for numero_linea, linea in enumerate(lineas, 1):
            linea = sorted(linea, key=lambda w: w["x0"])
            detalle.append({
                "linea": numero_linea,
                "texto": " ".join(w["text"] for w in linea),
                "palabras": [{"texto": w["text"], "x0": round(w["x0"], 2), "x1": round(w["x1"], 2), "top": round(w["top"], 2)} for w in linea],
            })
        resultado.append({"pagina": numero, "ancho": pagina.width, "alto": pagina.height, "lineas": detalle})

(OUT / "republicacion_v2_coordenadas.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
with (OUT / "republicacion_v2_texto.txt").open("w", encoding="utf-8") as f:
    for pagina in resultado:
        f.write(f"=== PÁGINA {pagina['pagina']} ===\n")
        for linea in pagina["lineas"]:
            f.write(f"{linea['linea']:03d}: {linea['texto']}\n")
print(json.dumps({"pdf": PDF.name, "paginas": len(resultado), "salida": str(OUT.relative_to(ROOT))}, ensure_ascii=False))
