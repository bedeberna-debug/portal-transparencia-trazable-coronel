from pathlib import Path
import json
import pdfplumber

ROOT = Path(r"C:\Users\bsilq\Documents\Kimi\Workspaces\Portal de Transparencia Trazable - Municipalidad de Coronel")
RAW = ROOT / "datos crudos" / "07_Información_Presupuestaria" / "Estado de Situación Financiera"
OUT = ROOT / "trabajo" / "07_Información_Presupuestaria" / "esp_ingresos_inspeccion"
OUT.mkdir(parents=True, exist_ok=True)
SAMPLES = [
    RAW / "2023" / "Ingresos 2023" / "2023-12esp dic municipalidad ingresos.pdf",
    RAW / "2025" / "Ingresos 2025" / "esp dic municipalidad ingresos.pdf",
]
for path in SAMPLES:
    chunks = []
    metadata = []
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, 1):
            words = page.extract_words(x_tolerance=1, y_tolerance=2)
            lines = []
            for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
                if not lines or abs(lines[-1][0]["top"] - word["top"]) > 2:
                    lines.append([word])
                else:
                    lines[-1].append(word)
            chunks.append(f"===== PÁGINA {page_no} =====")
            for number, line in enumerate(lines, 1):
                top = sum(w["top"] for w in line) / len(line)
                chunks.append(f"l.{number:03d} top={top:.2f} | " + " | ".join(f"{w['text']}@{w['x0']:.1f}-{w['x1']:.1f}" for w in line))
            metadata.append({"pagina": page_no, "ancho": page.width, "alto": page.height, "lineas": len(lines)})
    target = OUT / f"{path.parent.parent.name}_{path.stem}_coordenadas.txt"
    target.write_text("\n".join(chunks), encoding="utf-8")
    print(json.dumps({"archivo": path.name, "paginas": len(metadata), "salida": str(target.relative_to(ROOT))}, ensure_ascii=False))
