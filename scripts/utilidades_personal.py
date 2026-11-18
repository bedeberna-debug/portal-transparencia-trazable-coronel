from pathlib import Path
import csv, hashlib, re, unicodedata
from io import StringIO
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'datos crudos' / '04_Personal_y_Remuneraciones'
OUT = ROOT / 'datos procesados' / '04_Personal_y_Remuneraciones'
DOCS = ROOT / 'documentación' / '04_Personal_y_Remuneraciones'
TMP = ROOT / 'trabajo' / '04_Personal_y_Remuneraciones'
MESES = {m:i+1 for i,m in enumerate(['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'])}
MES_NOMBRE = {v:k for k,v in MESES.items()}

def norm(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ''
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(x))).strip()

def keyname(x):
    x = norm(x).upper()
    return ''.join(c for c in unicodedata.normalize('NFD', x) if unicodedata.category(c) != 'Mn')

def read_csv_robust(path):
    data = Path(path).read_bytes()
    for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    try:
        sep = csv.Sniffer().sniff(text[:8192], delimiters=';,\t|').delimiter
    except csv.Error:
        sep = ';'
    df = pd.read_csv(StringIO(text), sep=sep, dtype=str, keep_default_na=False, engine='python')
    return df, enc, sep

def money(x):
    s = norm(x)
    if not s or s.casefold() in {'no tiene', 'no informa', '-', '--', 'nan', 'none'}:
        return 0
    left = s.split(':')[0]
    digits = re.sub(r'[^0-9,.-]', '', left)
    if not digits or not re.search(r'\d', digits):
        return 0
    if ',' in digits:
        digits = digits.split(',')[0]
    digits = digits.replace('.', '').replace('-', '')
    try:
        return int(digits)
    except ValueError:
        return None

def hours(x):
    s = norm(x)
    m = re.search(r':\s*([0-9]+(?:[.,][0-9]+)?)\s*hrs?\b', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else 0.0

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def load_raw_category(folder):
    frames = []
    for p in sorted((RAW/folder).glob('20*/*.csv')):
        df, enc, sep = read_csv_robust(p)
        df = df.loc[:, ~df.columns.str.startswith('Unnamed:')].copy()
        df['fuente_archivo'] = p.name
        df['fuente_ruta_relativa'] = str(p.relative_to(ROOT))
        df['fuente_fila_csv'] = np.arange(2, len(df)+2)
        df['fuente_sha256'] = sha256(p)
        df['fuente_encoding'] = enc
        df['fuente_separador'] = sep
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

def style_workbook(wb, freeze='A2'):
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        if ws.max_row >= 1 and ws.max_column >= 1:
            ws.freeze_panes = freeze
            ws.auto_filter.ref = ws.dimensions
            for cell in ws[1]:
                cell.font = Font(bold=True, color='FFFFFF')
                cell.fill = PatternFill('solid', fgColor='1F4E78')
                cell.alignment = Alignment(vertical='center', wrap_text=True)
            ws.row_dimensions[1].height = 32
            for i, col in enumerate(ws.iter_cols(min_row=1, max_row=min(ws.max_row, 250)), 1):
                values = [norm(c.value) for c in col]
                width = min(max([len(v) for v in values] + [8]) + 2, 45)
                ws.column_dimensions[get_column_letter(i)].width = width

def write_xlsx(path, sheets):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
        style_workbook(writer.book)
    return path
