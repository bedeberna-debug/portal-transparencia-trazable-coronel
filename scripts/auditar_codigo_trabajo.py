from pathlib import Path
import sys, json, re, unicodedata
from collections import Counter, defaultdict
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from inspeccionar_fuentes import read_csv_robust
BASE = ROOT/'datos crudos'/'04_Personal_y_Remuneraciones'/'03_Personal_por_Código_del_Trabajo'
TMP = ROOT/'trabajo'/'04_Personal_y_Remuneraciones'
TMP.mkdir(parents=True, exist_ok=True)
MASTER = BASE/'MAESTRO_CODTrabajo_Coronel_2023-2025.xlsx'
NAME='Nombre completo'
COLS={
'bruta':'Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras)',
'liquida':'Remuneración líquida del mes',
'adicionales':'Rem. adicionales del mes (no inc. en rem. bruta)',
'bonos':'Remuneración Bonos incentivos del mes (inc. en rem. bruta)',
'desvinculacion':'Monto de desvinculación (no inc. en rem. bruta)',
'he':'Montos y horas extraordinarias del mes(inc. en rem. bruta)',
'viaticos':'Viáticos del mes (no inc. en rem. bruta)'}
NUM={'bruta':'rem_bruta_mes_num','liquida':'rem_liquida_mes_num','adicionales':'rem_adicionales_mes_num','bonos':'bonos_mes_num','desvinculacion':'desvinculacion_num','he':'he_monto_num','viaticos':'viaticos_num'}
MESES={m:i+1 for i,m in enumerate(['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'])}

def norm(x):
    if x is None or (isinstance(x,float) and np.isnan(x)): return ''
    x=unicodedata.normalize('NFKC',str(x)).strip()
    return re.sub(r'\s+',' ',x)

def keyname(x):
    x=norm(x).upper()
    return ''.join(c for c in unicodedata.normalize('NFD',x) if unicodedata.category(c)!='Mn')

def money(x):
    s=norm(x)
    if not s or s.lower() in {'no tiene','no informa','-','--','nan'}: return 0
    # Los montos publicados usan punto de miles y coma decimal; se conservan pesos enteros.
    left=s.split(':')[0]
    digits=re.sub(r'[^0-9,-]','',left)
    if not digits: return 0
    if ',' in digits: digits=digits.split(',')[0]
    digits=digits.replace('.','').replace('-','')
    try: return int(digits)
    except: return None

def hours(x):
    s=norm(x)
    m=re.search(r':\s*([0-9]+(?:[.,][0-9]+)?)\s*hrs?\b',s,re.I)
    if not m: return 0
    return float(m.group(1).replace(',','.'))

frames=[]
for p in sorted(BASE.glob('20*/*.csv')):
    df,enc,sep=read_csv_robust(p)
    df=df.loc[:,~df.columns.str.startswith('Unnamed:')].copy()
    df['_archivo_origen']=p.name
    df['_ruta_origen']=str(p.relative_to(ROOT))
    df['_fila_csv']=np.arange(2,len(df)+2)
    df['_encoding']=enc
    frames.append(df)
raw=pd.concat(frames,ignore_index=True)
raw['Año']=pd.to_numeric(raw['Año'],errors='coerce').astype('Int64')
raw['_mes_num']=raw['Mes'].map(MESES).astype('Int64')
raw['_nombre_clave']=raw[NAME].map(keyname)
raw['_clave']=raw['Año'].astype(str)+'-'+raw['_mes_num'].astype(str).str.zfill(2)+'|'+raw['_nombre_clave']
for k,c in COLS.items(): raw['_calc_'+k]=raw[c].map(money)
raw['_calc_he_horas']=raw[COLS['he']].map(hours)

m=pd.read_excel(MASTER,sheet_name='Datos Completos',dtype=object).fillna('')
m['Año']=pd.to_numeric(m['Año'],errors='coerce').astype('Int64')
m['_mes_num']=m['Mes'].map(MESES).astype('Int64')
m['_nombre_clave']=m['nombre_limpio'].map(keyname)
m['_clave']=m['Año'].astype(str)+'-'+m['_mes_num'].astype(str).str.zfill(2)+'|'+m['_nombre_clave']

summary={'raw_filas':len(raw),'maestro_filas':len(m),'por_año':{},'duplicados_raw':[],'duplicados_maestro':[],'diferencias':{},'muestras_diferencias':{},'contenido_archivos':[]}
for p in sorted(BASE.glob('20*/*.csv')):
    d=raw[raw['_archivo_origen']==p.name]
    summary['contenido_archivos'].append({'archivo':p.name,'filas':len(d),'años':sorted(set(d['Año'].dropna().astype(int))),'meses':sorted(set(d['Mes']))})
for y in (2023,2024,2025):
    r=raw[raw['Año']==y]; q=m[m['Año']==y]
    summary['por_año'][str(y)]={
        'raw':len(r),'maestro':len(q),
        'origen_vacio_maestro':int((q['_archivo_origen'].map(norm)=='').sum()),
        'raw_por_mes':{str(k):int(v) for k,v in r.groupby('_mes_num').size().items()},
        'maestro_por_mes':{str(k):int(v) for k,v in q.groupby('_mes_num').size().items()},
        'claves_solo_raw':int((Counter(r['_clave'])-Counter(q['_clave'])).total()),
        'claves_solo_maestro':int((Counter(q['_clave'])-Counter(r['_clave'])).total()),
    }
summary['duplicados_raw']=[{'clave':k,'n':v} for k,v in Counter(raw['_clave']).items() if v>1]
summary['duplicados_maestro']=[{'clave':k,'n':v} for k,v in Counter(m['_clave']).items() if v>1]

# Comparación uno-a-uno por clave y ocurrencia, preservando el orden original.
r=raw.copy(); q=m.copy()
r['_oc']=r.groupby('_clave').cumcount(); q['_oc']=q.groupby('_clave').cumcount()
a=r.merge(q,on=['_clave','_oc'],how='inner',suffixes=('_raw','_maestro'))
compare_cols=[c for c in raw.columns if not c.startswith('_') and c not in ('Año','Mes') and c in m.columns]
for c in compare_cols:
    neq=a[c+'_raw'].map(norm)!=a[c+'_maestro'].map(norm)
    summary['diferencias'][c]=int(neq.sum())
    if neq.any():
        summary['muestras_diferencias'][c]=a.loc[neq,['_clave',c+'_raw',c+'_maestro','_archivo_origen_raw']].head(10).to_dict('records')
for k,mc in NUM.items():
    calc=a['_calc_'+k]
    got=pd.to_numeric(a[mc],errors='coerce')
    neq=(calc.fillna(-999999)!=got.fillna(-999999))
    summary['diferencias'][mc]=int(neq.sum())
    if neq.any():
        summary['muestras_diferencias'][mc]=a.loc[neq,['_clave',COLS[k]+'_raw',mc,'_calc_'+k,'_archivo_origen_raw']].head(10).to_dict('records')
neq=a['_calc_he_horas']!=pd.to_numeric(a['he_horas_num'],errors='coerce').fillna(-999999)
summary['diferencias']['he_horas_num']=int(neq.sum())
summary['muestras_diferencias']['he_horas_num']=a.loc[neq,['_clave',COLS['he']+'_raw','he_horas_num','_calc_he_horas','_archivo_origen_raw']].head(10).to_dict('records')

# Control de archivos ya identificados en 2023.
a23=a[a['Año_raw']==2023]
summary['origen_2023_incorrecto']=int((a23['_archivo_origen_raw']!=a23['_archivo_origen_maestro']).sum())

(TMP/'auditoria_codigo_trabajo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
raw.to_pickle(TMP/'codigo_trabajo_raw.pkl')
m.to_pickle(TMP/'codigo_trabajo_maestro.pkl')

print(json.dumps({k:v for k,v in summary.items() if k not in ('contenido_archivos','muestras_diferencias','duplicados_raw','duplicados_maestro')},ensure_ascii=False,indent=2))
print('Duplicados raw:',len(summary['duplicados_raw']),'maestro:',len(summary['duplicados_maestro']))
print('Origen 2023 incorrecto:',summary['origen_2023_incorrecto'])
