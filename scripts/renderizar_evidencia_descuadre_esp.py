from pathlib import Path
import csv
import json
import pdfplumber
import pypdfium2 as pdfium

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
WORK = ROOT / "trabajo" / "07_Información_Presupuestaria" / "descuadre_esp_ingresos"
OUT = WORK / "evidencia_visual"
OUT.mkdir(parents=True, exist_ok=True)
summary = json.loads((WORK / "resumen_hipotesis_diciembre.json").read_text(encoding="utf-8"))
with (WORK / "anomalias_aritmeticas_diciembre.csv").open(encoding="utf-8-sig", newline="") as f:
    anomalies = list(csv.DictReader(f))


def group_lines(words):
    lines = []
    for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if not lines or abs(lines[-1][0]["top"] - word["top"]) > 2:
            lines.append([word])
        else:
            lines[-1].append(word)
    return [sorted(line, key=lambda w: w["x0"]) for line in lines]


rows = []
for doc in summary:
    path = ROOT / doc["ruta_relativa"]
    account = next(a for a in anomalies if a["documento_id"] == doc["documento_id"] and a["codigo_cuenta_pdf"] == "15")
    targets = [
        ("total", int(doc["paginas_totales"]), int(doc["linea_total"])),
        ("cuenta15", int(account["fuente_pagina"]), int(account["fuente_linea"])),
    ]
    pdfium_doc = pdfium.PdfDocument(str(path))
    with pdfplumber.open(path) as pdf:
        for label, page_no, line_no in targets:
            page = pdf.pages[page_no - 1]
            lines = group_lines(page.extract_words(x_tolerance=1, y_tolerance=2))
            line = lines[line_no - 1]
            raw = " ".join(w["text"] for w in line)
            if label == "total" and "DEUDORES" not in raw:
                raise ValueError(f"Total inesperado: {doc['documento_id']}: {raw}")
            if label == "cuenta15" and not any(w["text"] == "15" for w in line):
                raise ValueError(f"Cuenta 15 inesperada: {doc['documento_id']}: {raw}")
            scale = 4
            bbox = (55, max(0, min(w["top"] for w in line) - 4), min(page.width, 820), min(page.height, max(w["bottom"] for w in line) + 4))
            image = pdfium_doc[page_no - 1].render(scale=scale).to_pil()
            crop = image.crop(tuple(round(v * scale) for v in bbox))
            filename = f"{doc['documento_id']}_{label}_p{page_no}_l{line_no}.png"
            crop.save(OUT / filename, optimize=True)
            rows.append({
                "documento_id": doc["documento_id"], "objeto": label, "archivo": path.name,
                "ruta_relativa": doc["ruta_relativa"], "pagina": page_no, "linea": line_no,
                "sha256": doc["sha256"], "bbox_pdf_puntos": ",".join(str(v) for v in bbox),
                "texto_linea_raw": raw, "imagen_recorte": str((OUT / filename).relative_to(ROOT)),
            })
    pdfium_doc.close()
with (WORK / "evidencia_visual_diciembre.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
print(json.dumps(rows, ensure_ascii=False, indent=2))
