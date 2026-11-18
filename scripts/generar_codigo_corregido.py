from pathlib import Path
import json
import pandas as pd
from utilidades_personal import *

FOLDER='03_Personal_por_Código_del_Trabajo'
MASTER=RAW/FOLDER/'MAESTRO_CODTrabajo_Coronel_2023-2025.xlsx'
OUTFILE=OUT/'MAESTRO_CODTrabajo_Coronel_2023-2025_v2_corregido.xlsx'
NAME='Nombre completo'
NUMS={
'rem_bruta_mes_num':'Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras)',
'rem_liquida_mes_num':'Remuneración líquida del mes',
'rem_adicionales_mes_num':'Rem. adicionales del mes (no inc. en rem. bruta)',
'bonos_mes_num':'Remuneración Bonos incentivos del mes (inc. en rem. bruta)',
'desvinculacion_num':'Monto de desvinculación (no inc. en rem. bruta)',
'he_monto_num':'Montos y horas extraordinarias del mes(inc. en rem. bruta)',
'viaticos_num':'Viáticos del mes (no inc. en rem. bruta)'}
raw=load_raw_category(FOLDER)
m=pd.read_excel(MASTER,sheet_name='Datos Completos',dtype=object).fillna('')
for df,namecol in ((raw,NAME),(m,'nombre_limpio')):
    df['anio_i']=pd.to_numeric(df['Año'],errors='raise').astype(int)
    df['mes_i']=df['Mes'].map(MESES).astype(int)
    df['nombre_clave']=df[namecol].map(keyname)
    df['clave']=df['anio_i'].astype(str)+'-'+df['mes_i'].astype(str).str.zfill(2)+'|'+df['nombre_clave']
    df['ocurrencia']=df.groupby('clave').cumcount()
joined=m.merge(raw,on=['clave','ocurrencia'],how='left',suffixes=('_maestro','_csv'),indicator=True,validate='one_to_one')
assert (joined['_merge']=='both').all(), 'Existen filas del maestro sin CSV fuente'
assert len(joined)==len(m)==len(raw)==933

# Las columnas crudas completamente vacías se restauran; las derivadas manuales se preservan.
restore=[c for c in raw.columns if c in m.columns and c not in ('Año','Mes','Región','Observaciones') and (m[c].map(norm)=='').all()]
corrected=m.copy()
for c in restore:
    corrected[c]=joined[c+'_csv'].values
corrected['_archivo_origen']=joined['fuente_archivo'].values
for c in ('fuente_ruta_relativa','fuente_fila_csv','fuente_sha256'):
    corrected[c]=joined[c].values
corrected['verificacion_estado']='CSV localizado; clave e importes numéricos coincidentes; campos crudos restaurados'

# Diferencias por columna y año, antes de la corrección.
diffs=[]
for c in restore+['_archivo_origen']:
    rawvals=joined['fuente_archivo'] if c=='_archivo_origen' else joined[c+'_csv']
    masterblank=m[c].map(norm)==''
    changed=(m[c].map(norm)!=rawvals.map(norm))
    for year in (2023,2024,2025):
        mask=m['anio_i']==year
        diffs.append({'columna':c,'anio':year,'celdas_diferentes':int((changed&mask).sum()),
                      'celdas_vacias_en_original':int((masterblank&mask).sum()),
                      'accion':'Restaurada desde CSV' if c!='_archivo_origen' else 'Nombre de CSV incorporado'})
diffs=pd.DataFrame(diffs)

# Control independiente de columnas numéricas preexistentes.
numchecks=[]
for num,rawcol in NUMS.items():
    expected=joined[rawcol+'_csv'].map(money).astype('int64')
    actual=pd.to_numeric(m[num],errors='coerce').astype('int64')
    numchecks.append({'columna_numerica':num,'campo_csv':rawcol,'filas_comparadas':len(m),
                      'diferencias':int((expected!=actual).sum()),'resultado':'Coincide' if (expected==actual).all() else 'Difiere'})
expected_hours=joined[NUMS['he_monto_num']+'_csv'].map(hours)
actual_hours=pd.to_numeric(m['he_horas_num'],errors='coerce')
numchecks.append({'columna_numerica':'he_horas_num','campo_csv':NUMS['he_monto_num'],'filas_comparadas':len(m),
                  'diferencias':int((expected_hours!=actual_hours).sum()),'resultado':'Coincide' if (expected_hours==actual_hours).all() else 'Difiere'})
numchecks=pd.DataFrame(numchecks)
assert (numchecks['diferencias']==0).all()

coverage=[]
for year in (2023,2024,2025):
    for month in range(1,13):
        coverage.append({'anio':year,'mes_numero':month,'mes_nombre':MES_NOMBRE[month],
                         'filas_csv':int(((raw['anio_i']==year)&(raw['mes_i']==month)).sum()),
                         'filas_maestro_original':int(((m['anio_i']==year)&(m['mes_i']==month)).sum()),
                         'filas_maestro_corregido':int(((corrected['anio_i']==year)&(corrected['mes_i']==month)).sum())})
coverage=pd.DataFrame(coverage)
coverage['coincide']=coverage['filas_csv']==coverage['filas_maestro_original']

files=raw.groupby(['fuente_archivo','fuente_ruta_relativa','fuente_sha256'],as_index=False).agg(
    filas=('Nombre completo','size'),anios_contenido=('Año',lambda s:'|'.join(sorted(set(s)))),
    meses_contenido=('Mes',lambda s:'|'.join(sorted(set(s),key=lambda x:MESES[x]))))
files['mes_distinto_al_anio_directorio']=files.apply(lambda r:any(str(y) not in Path(r['fuente_ruta_relativa']).parts for y in []),axis=1)
# Marca explícita de contenido que no corresponde al mes indicado por el nombre de archivo.
month_by_file=raw.groupby('fuente_archivo')['Mes'].agg(lambda s:'|'.join(sorted(set(s),key=lambda x:MESES[x]))).to_dict()
files['contenido_mes_multiple']=files['meses_contenido'].str.contains(r'\|')
files=files.drop(columns=['mes_distinto_al_anio_directorio'])

anomalies=[]
for file,g in raw.groupby('fuente_archivo'):
    expected_month=next((n for n in MESES if n.casefold() in file.casefold()),None)
    actual=sorted(set(g['Mes']),key=lambda x:MESES[x])
    if expected_month and (len(actual)>1 or actual[0]!=expected_month):
        for mes in actual:
            if mes!=expected_month:
                rows=g[g['Mes']==mes]
                anomalies.append({'archivo':file,'mes_esperado_por_nombre':expected_month,'mes_en_contenido':mes,
                                  'filas':len(rows),'filas_csv':','.join(map(str,rows['fuente_fila_csv'])),
                                  'decision':'Conservar Año/Mes del contenido y mantener trazabilidad al archivo real'})
anomalies=pd.DataFrame(anomalies)

control=pd.DataFrame([
    {'indicador':'Filas CSV / maestro / corregido','valor':f'{len(raw)} / {len(m)} / {len(corrected)}'},
    {'indicador':'Columnas crudas restauradas','valor':len(restore)},
    {'indicador':'Celdas crudas restauradas','valor':int(diffs['celdas_diferentes'].sum())},
    {'indicador':'Filas sin CSV fuente','valor':int((joined['_merge']!='both').sum())},
    {'indicador':'Diferencias en columnas numéricas','valor':int(numchecks['diferencias'].sum())},
    {'indicador':'Cobertura mensual coincidente','valor':f"{int(coverage['coincide'].sum())} de {len(coverage)}"},
    {'indicador':'Alcance ampliado','valor':'2023 también presentaba campos crudos y _archivo_origen vacíos; se corrigieron 2023-2025'},
    {'indicador':'Original modificado','valor':'No'},
])
write_xlsx(OUTFILE,{'Datos Completos':corrected,'Control':control,'Diferencias':diffs,
                    'Control numérico':numchecks,'Cobertura mensual':coverage,
                    'Archivos fuente':files,'Anomalías periodo':anomalies})

(TMP/'codigo_correccion_resumen.json').write_text(json.dumps({
    'archivo':str(OUTFILE.relative_to(ROOT)),'filas':len(corrected),'columnas_restauradas':restore,
    'celdas_restauradas':int(diffs['celdas_diferentes'].sum()),'diferencias_numericas':int(numchecks['diferencias'].sum()),
    'anomalias_periodo':anomalies.to_dict('records'),'sha256':sha256(OUTFILE)
},ensure_ascii=False,indent=2),encoding='utf-8')
corrected.to_pickle(TMP/'codigo_corregido.pkl')
print(control.to_string(index=False))
print('\nColumnas restauradas:',', '.join(restore))
print('\nAnomalías de periodo:\n',anomalies.to_string(index=False))
print('\nArchivo:',OUTFILE)
