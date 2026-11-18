import json, subprocess, sys
from pathlib import Path
from utilidades_personal import ROOT,OUT,DOCS,sha256

TOOL=Path(r'C:\Users\bsilq\AppData\Roaming\kimi-desktop\daimon-share\daimon\runtime\kimi-code\home\plugins\managed\kimi-excel\skills\kimi-excel\scripts\xlsx_tools.py')
LOG=ROOT/'trabajo'/'04_Personal_y_Remuneraciones'/'validacion_xlsx.json'
records={}
if LOG.exists():
    for r in json.loads(LOG.read_text(encoding='utf-8')): records[r['archivo']]=r

def run(cmd):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=300)
    start=p.stdout.find('{'); end=p.stdout.rfind('}')
    if start<0 or end<start:
        raise RuntimeError(f'Sin salida JSON ({p.returncode}): {p.stdout[-1000:]} {p.stderr[-1000:]}')
    return json.loads(p.stdout[start:end+1]),p.stdout+p.stderr

files=sorted(list(OUT.rglob('*.xlsx'))+list(DOCS.rglob('*.xlsx')))
for path in files:
    if path.stem.endswith('_recalc_verify'): continue
    rel=str(path.relative_to(ROOT)); digest=sha256(path)
    old=records.get(rel)
    if old and old.get('sha256')==digest and old.get('verify',{}).get('status') in ('pass','pass_with_warnings'):
        print('Ya validado:',rel,flush=True); continue
    print('Recalculando:',rel,flush=True)
    recalc,_=run([sys.executable,str(TOOL),'recalc',str(path)])
    verification=recalc.get('verification_file')
    print('Verificando:',rel,flush=True)
    verify,_=run([sys.executable,str(TOOL),'verify',str(path)])
    # recalc puede ajustar calcPr en el original; la huella entregable se toma después de verify.
    records[rel]={'archivo':rel,'sha256':sha256(path),'recalc':recalc,'verify':verify}
    LOG.write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
    if verification:
        vp=Path(verification)
        if not vp.is_absolute(): vp=ROOT/vp
        if vp.is_file() and vp.name.endswith('_recalc_verify.xlsx'): vp.unlink()
    if verify.get('status') not in ('pass','pass_with_warnings'):
        raise RuntimeError(f'Validación no aprobada: {rel}: {verify}')
print(f'Libros aprobados: {len(records)}',flush=True)
