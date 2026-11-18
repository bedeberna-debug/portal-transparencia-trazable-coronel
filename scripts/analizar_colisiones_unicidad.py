import json
from collections import Counter
from pathlib import Path
import pandas as pd
from utilidades_personal import ROOT,OUT,TMP,MESES,read_csv_robust,sha256,norm

OUTDIR=TMP
OUTDIR.mkdir(parents=True,exist_ok=True)
CASES=[
 {'caso':'COT-2023-0015 / 2025-05','categoria':'Código del Trabajo','id_trabajador':'COT-2023-0015','periodo':'2025-05','archivo':'05_CODTrabajo_Mayo_2025.csv','fila':9,'anio':2025,'mes':5},
 {'caso':'COT-2023-0015 / 2025-05','categoria':'Código del Trabajo','id_trabajador':'COT-2023-0015','periodo':'2025-05','archivo':'07_CODTrabajo_Julio_2025.csv','fila':29,'anio':2025,'mes':7},
 {'caso':'PLT-2023-0032 / 2024-11','categoria':'Planta','id_trabajador':'PLT-2023-0032','periodo':'2024-11','archivo':'11_Planta_Noviembre_2024.csv','fila':25,'anio':2024,'mes':11},
 {'caso':'PLT-2023-0032 / 2024-11','categoria':'Planta','id_trabajador':'PLT-2023-0032','periodo':'2024-11','archivo':'12_Planta_Diciembre_2024.csv','fila':132,'anio':2024,'mes':12},
]
MASTER={
 'Planta':'MAESTRO_Planta_Coronel_2023-2025_canonico_v1.xlsx',
 'Código del Trabajo':'MAESTRO_CODTrabajo_Coronel_2023-2025_canonico_v1.xlsx',
 'Contrata':'MAESTRO_Contrata_Coronel_2023-2025_canonico_v1.xlsx',
 'Honorarios':'MAESTRO_Honorarios_Coronel_2023-2025_canonico_v1.xlsx',
}
CANON={cat:pd.read_excel(OUT/file,sheet_name='Datos') for cat,file in MASTER.items()}
for cat,d in CANON.items():
    d['categoria']=cat

def clean(v):
    if pd.isna(v): return ''
    if isinstance(v,float) and v.is_integer(): return int(v)
    if hasattr(v,'item'):
        try: return clean(v.item())
        except Exception: pass
    return str(v) if not isinstance(v,(str,int,float,bool)) else v

def record(row): return {str(k):clean(v) for k,v in row.items()}
def period_raw(row):
    try: return f"{int(str(row['Año']).strip()):04d}-{MESES[norm(row['Mes'])]:02d}"
    except Exception: return f"{norm(row.get('Año',''))}|{norm(row.get('Mes',''))}"

def text(v): return norm(v).casefold()

raw_by_case={}
for c in CASES:
    matches=list((ROOT/'datos crudos'/'04_Personal_y_Remuneraciones').rglob(c['archivo']))
    assert len(matches)==1,(c['archivo'],matches)
    p=matches[0]
    d,encoding,sep=read_csv_robust(p)
    row=d.iloc[c['fila']-2]
    nominal=f"{c['anio']}-{c['mes']:02d}"
    periods=Counter(period_raw(r) for _,r in d.iterrows())
    off=[]
    for idx,r in d.iterrows():
        per=period_raw(r)
        if per!=nominal:
            off.append({'fila_csv':int(idx)+2,'nombre':clean(r.get('Nombre completo','')),'periodo':per,
                        'bruto_raw':clean(r.get('Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras)','')),
                        'liquido_raw':clean(r.get('Remuneración líquida del mes',''))})
    cat=CANON[c['categoria']]
    cx=cat[(cat['fuente_archivo']==c['archivo'])&(cat['fuente_fila_csv'].astype(int)==c['fila'])]
    assert len(cx)==1,(c['archivo'],c['fila'],len(cx))
    assert text(row['Nombre completo'])==text(cx.iloc[0]['nombre_original'])
    c.update({'ruta_relativa':str(p.relative_to(ROOT)),'sha256':sha256(p),'encoding':encoding,'separador':sep,
              'filas_datos':len(d),'columnas':list(map(str,d.columns)),'fila_cruda_completa':record(row),
              'fila_canonica_completa':record(cx.iloc[0]),'periodo_declarado':period_raw(row),'periodo_nominal_archivo':nominal,
              'distribucion_periodos':dict(sorted(periods.items())),'periodo_dominante':periods.most_common(1)[0][0],
              'filas_fuera_periodo_nominal':off})
    raw_by_case[c['archivo']]=c

# Comparación exhaustiva por campos crudos y por campos canónicos.
comparisons=[]
for case_name in dict.fromkeys(c['caso'] for c in CASES):
    pair=[c for c in CASES if c['caso']==case_name]
    a,b=pair
    fields=list(dict.fromkeys(list(a['fila_cruda_completa'])+list(b['fila_cruda_completa'])))
    raw_diff=[]
    for f in fields:
        va=a['fila_cruda_completa'].get(f,''); vb=b['fila_cruda_completa'].get(f,'')
        raw_diff.append({'campo':f,'archivo_nominal':va,'archivo_posterior':vb,
                         'igual_exacto':clean(va)==clean(vb),'igual':text(va)==text(vb)})
    cfields=list(dict.fromkeys(list(a['fila_canonica_completa'])+list(b['fila_canonica_completa'])))
    canonical_diff=[]
    for f in cfields:
        va=a['fila_canonica_completa'].get(f,''); vb=b['fila_canonica_completa'].get(f,'')
        canonical_diff.append({'campo':f,'archivo_nominal':va,'archivo_posterior':vb,
                               'igual_exacto':clean(va)==clean(vb),'igual':text(va)==text(vb)})
    comparisons.append({'caso':case_name,'campos_crudos':raw_diff,'campos_canonicos':canonical_diff,
                        'campos_crudos_distintos':[x['campo'] for x in raw_diff if not x['igual']],
                        'campos_crudos_distintos_exactos':[x['campo'] for x in raw_diff if not x['igual_exacto']],
                        'campos_canonicos_distintos':[x['campo'] for x in canonical_diff if not x['igual']]})

# Colisiones por nombre+período dentro de cada categoría y contraste con id_trabajador.
all_canon=pd.concat(CANON.values(),ignore_index=True)
name_period=[]
for (cat,name,period),g in all_canon.groupby(['categoria','nombre_normalizado','periodo'],dropna=False):
    if len(g)<2: continue
    ids=sorted(set(g['id_trabajador'].astype(str)))
    name_period.append({'categoria':cat,'nombre_normalizado':name,'periodo':period,'registros':len(g),
                        'ids':ids,'mismo_id':len(ids)==1,
                        'fuentes':[{'registro_id':r['registro_id'],'id_trabajador':r['id_trabajador'],
                                    'archivo':r['fuente_archivo'],'fila_csv':int(r['fuente_fila_csv']),
                                    'bruto_clp':int(r['remuneracion_bruta_clp']),'liquido_clp':int(r['remuneracion_liquida_clp'])}
                                   for _,r in g.iterrows()]})
# Colisiones transversales: se cuantifican, pero no son pares equivalentes dentro de un estamento.
cross=[]
for (name,period),g in all_canon.groupby(['nombre_normalizado','periodo'],dropna=False):
    cats=sorted(set(g['categoria'].astype(str))); ids=sorted(set(g['id_trabajador'].astype(str)))
    if len(cats)>1 and len(ids)>1:
        cross.append({'nombre_normalizado':name,'periodo':period,'registros':len(g),'categorias':cats,'ids':ids})

# Trayectoria completa de las dos personas y selección hipotética por coincidencia nominal.
trajectories={}
for case_name in dict.fromkeys(c['caso'] for c in CASES):
    pair=[c for c in CASES if c['caso']==case_name]
    cat=pair[0]['categoria']; worker=pair[0]['id_trabajador']
    d=CANON[cat][CANON[cat]['id_trabajador']==worker].copy().sort_values(['periodo','fuente_archivo','fuente_fila_csv'])
    rows=[]
    for _,r in d.iterrows():
        source=next((c for c in pair if c['archivo']==r['fuente_archivo'] and int(c['fila'])==int(r['fuente_fila_csv'])),None)
        selected=True
        if source: selected=source['periodo']==source['periodo_nominal_archivo']
        rows.append({'periodo':r['periodo'],'registro_id':r['registro_id'],'bruto_clp':int(r['remuneracion_bruta_clp']),
                     'liquido_clp':int(r['remuneracion_liquida_clp']),'archivo':r['fuente_archivo'],'fila_csv':int(r['fuente_fila_csv']),
                     'en_colision':source is not None,'seleccion_propuesta':'canonica_trayectoria' if selected else 'version_alterna'})
    trajectories[case_name]=rows

result={'maestros_sha256':{file:sha256(OUT/file) for file in MASTER.values()},
        'casos':CASES,'comparaciones':comparisons,
        'colisiones_nombre_periodo_misma_categoria':name_period,
        'resumen_misma_categoria':{'grupos':len(name_period),'mismo_id':sum(x['mismo_id'] for x in name_period),
                                   'ids_distintos':sum(not x['mismo_id'] for x in name_period)},
        'colisiones_nombre_periodo_transversal':cross,
        'resumen_transversal':{'grupos':len(cross),'registros_involucrados':sum(x['registros'] for x in cross),
                               'por_combinacion_categorias':dict(Counter('|'.join(x['categorias']) for x in cross))},
        'trayectorias_propuestas':trajectories,
        'nota_alcance':'El análisis transversal no prueba identidad ni duplicación: los IDs heredados tienen alcance por categoría.'}
path=OUTDIR/'analisis_colisiones_unicidad.json'
path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Evidencia:',path)
for c in CASES:
    print('\n',c['archivo'],'SHA-256',c['sha256'])
    print('Período declarado:',c['periodo_declarado'],'nominal:',c['periodo_nominal_archivo'],'distribución:',c['distribucion_periodos'])
    print('Fuera de período:',c['filas_fuera_periodo_nominal'])
for comp in comparisons:
    print('\nDiferencias',comp['caso'])
    print('Crudos:',comp['campos_crudos_distintos'])
    print('Canónicos:',comp['campos_canonicos_distintos'])
    for x in comp['campos_crudos']:
        if not x['igual']: print(x)
print('\nMisma categoría:',result['resumen_misma_categoria'])
print('Transversal:',result['resumen_transversal'])
print('Trayectorias:',{k:len(v) for k,v in trajectories.items()})
