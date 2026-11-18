from pathlib import Path
import csv, json, hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'datos crudos' / '04_Personal_y_Remuneraciones'
TMP = ROOT / 'trabajo' / '04_Personal_y_Remuneraciones'
TMP.mkdir(parents=True, exist_ok=True)

def read_csv_robust(path):
    data = path.read_bytes()
    for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=';,\t|')
        sep = dialect.delimiter
    except csv.Error:
        sep = ';'
    from io import StringIO
    df = pd.read_csv(StringIO(text), sep=sep, dtype=str, keep_default_na=False, engine='python')
    return df, enc, sep

inventory = []
for p in sorted(RAW.rglob('*.csv')):
    try:
        df, enc, sep = read_csv_robust(p)
        inventory.append({
            'ruta': str(p.relative_to(ROOT)), 'filas': len(df), 'columnas': list(df.columns),
            'encoding': enc, 'separador': sep, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'error': ''
        })
    except Exception as e:
        inventory.append({'ruta': str(p.relative_to(ROOT)), 'error': repr(e)})

masters = {}
for p in sorted(RAW.rglob('MAESTRO_*.xlsx')):
    xf = pd.ExcelFile(p)
    info = {'ruta': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'hojas': {}}
    for sh in xf.sheet_names:
        df = pd.read_excel(p, sheet_name=sh, dtype=object)
        info['hojas'][sh] = {
            'filas': len(df), 'columnas': list(df.columns),
            'nulos': {str(c): int(df[c].isna().sum()) for c in df.columns},
            'muestra': df.head(3).fillna('').astype(str).to_dict('records')
        }
    masters[p.name] = info

(TMP/'inventario_csv.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
(TMP/'esquemas_maestros.json').write_text(json.dumps(masters, ensure_ascii=False, indent=2), encoding='utf-8')

samples = [
    RAW/'03_Personal_por_Código_del_Trabajo'/'2024'/'10_CODTrabajo_Enero_2024 Noviembre.csv',
    RAW/'03_Personal_por_Código_del_Trabajo'/'2025'/'03_CODTrabajo_Abril_2025.csv',
    RAW/'03_Personal_por_Código_del_Trabajo'/'2025'/'03_CODTrabajo_Marzo_2025.csv',
    RAW/'01_Personal_Planta'/'2024'/'01_Planta_Enero_2024.csv',
    RAW/'04_Personal_Honorarios'/'2024'/'01_Honorarios_Enero_2024.csv',
    RAW/'05_Autoridades_de_Eleccion_Popular'/'2024'/'01_ElectosyOtros_Enero_2024.csv',
]
out = []
for p in samples:
    df, enc, sep = read_csv_robust(p)
    out.append(f'\n=== {p.relative_to(ROOT)} ===\nencoding={enc}; sep={sep!r}; filas={len(df)}\ncolumnas={list(df.columns)}\n{df.head(3).to_string(index=False)}')
(TMP/'muestras.txt').write_text('\n'.join(out), encoding='utf-8')

print(f'CSV: {len(inventory)}; errores: {sum(bool(x.get("error")) for x in inventory)}')
print(f'Maestros: {len(masters)}')
for name, info in masters.items():
    for sh, s in info['hojas'].items():
        print(f'{name} | {sh}: {s["filas"]} filas, {len(s["columnas"])} columnas')
        print('  ' + ' | '.join(map(str, s['columnas'])))
print(f'Salidas: {TMP}')
