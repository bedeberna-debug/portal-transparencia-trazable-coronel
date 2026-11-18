import json
import pandas as pd
from utilidades_personal import *

CONFIG={
'Planta':{
 'folder':'01_Personal_Planta','master':'MAESTRO_Planta_Coronel_2023-2025.xlsx','name':'Nombre completo',
 'fields':{
  'diurnas':'Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta)',
  'nocturnas':'Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta)',
  'festivas':'Montos y horas extraordinarias festivas del mes (inc. en rem. bruta)'}},
'Contrata':{
 'folder':'02_Personal_Contrata','master':'MAESTRO_Contrata_Coronel_2023-2025.xlsx','name':'Nombre_completo',
 'fields':{'diurnas':'Horas_extra_diurnas','nocturnas':'Horas_extra_nocturnas','festivas':'Horas_extra_festivas'}}
}
RAW_EQUIV={
 'Horas_extra_diurnas':'Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta)',
 'Horas_extra_nocturnas':'Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta)',
 'Horas_extra_festivas':'Montos y horas extraordinarias festivas del mes (inc. en rem. bruta)'}
all_stats={}
for category,cfg in CONFIG.items():
    raw=load_raw_category(cfg['folder'])
    m=pd.read_excel(RAW/cfg['folder']/cfg['master'],sheet_name='Datos Completos',dtype=object).fillna('')
    raw['nombre_clave']=raw['Nombre completo'].map(keyname)
    m['nombre_clave']=m[cfg['name']].map(keyname)
    raw['archivo_clave']=raw['fuente_archivo'].map(norm)
    m['archivo_clave']=m['_archivo_origen'].map(norm)
    for df in (raw,m):
        df['clave']=df['archivo_clave']+'|'+df['nombre_clave']
        df['ocurrencia']=df.groupby('clave').cumcount()
    joined=m.merge(raw,on=['clave','ocurrencia'],how='left',suffixes=('_maestro','_csv'),indicator=True,validate='one_to_one')
    unmatched=int((joined['_merge']!='both').sum())
    assert unmatched==0, f'{category}: {unmatched} filas sin origen'
    result=m.drop(columns=['nombre_clave','archivo_clave','clave','ocurrencia']).copy()
    stats=[]; anomalies=[]
    for kind,mastercol in cfg['fields'].items():
        rawcol=RAW_EQUIV.get(mastercol,mastercol)
        masterref=mastercol+'_maestro' if mastercol+'_maestro' in joined.columns else mastercol
        master_raw=joined[masterref].map(norm)
        rawref=rawcol+'_csv' if rawcol+'_csv' in joined.columns else rawcol
        csv_raw=joined[rawref].map(norm)
        different=master_raw!=csv_raw
        parsed=csv_raw.map(hours)
        amount=csv_raw.map(money)
        legacy_amount=pd.to_numeric(joined[mastercol+'_maestro' if category=='Planta' else mastercol+'_num_maestro'],errors='coerce') if False else None
        newcol=f'Horas_extra_{kind}_cantidad'
        result[newcol]=parsed.values
        nonzero=parsed>0
        stats.append({'tipo':kind,'filas':len(result),'registros_con_horas':int(nonzero.sum()),
                      'horas_totales':float(parsed.sum()),'monto_total_clp':int(amount.sum()),
                      'diferencias_texto_maestro_vs_csv':int(different.sum()),
                      'monto_positivo_sin_horas_parseadas':int(((amount>0)&(parsed==0)).sum()),
                      'horas_positivas_con_monto_cero':int(((amount==0)&(parsed>0)).sum())})
        bad=(amount>0)&(parsed==0)
        for idx in joined.index[bad]:
            anomalies.append({'tipo':kind,'archivo':joined.loc[idx,'fuente_archivo'],
                              'fila_csv':joined.loc[idx,'fuente_fila_csv'],'nombre':joined.loc[idx,cfg['name']+'_maestro'],
                              'valor_raw':joined.loc[idx,rawcol+'_csv'],'monto_parseado':joined.loc[idx,rawcol+'_csv'] if False else amount.loc[idx],
                              'horas_parseadas':parsed.loc[idx]})
        assert int(different.sum())==0, f'{category}/{kind}: texto raw difiere del CSV'
    stats=pd.DataFrame(stats); anomalies=pd.DataFrame(anomalies)
    control=pd.DataFrame([
      {'indicador':'Filas maestro / CSV vinculadas','valor':f'{len(m)} / {len(joined)}'},
      {'indicador':'Filas sin origen','valor':unmatched},
      {'indicador':'Regla','valor':'Extraer número posterior a “:” y anterior a “hrs”; 0 cuando la fuente indica No tiene/No informa o no publica horas'},
      {'indicador':'Trazabilidad añadida','valor':'Las columnas fuente_archivo/fila/sha256 se incorporan en la versión canónica; esta versión conserva _archivo_origen'},
      {'indicador':'Hojas analíticas heredadas','valor':'No copiadas: sus agregaciones no se actualizaron con las nuevas columnas'},
      {'indicador':'Original modificado','valor':'No'}])
    sheets={'Datos Completos':result,'Control':control,'Resumen horas':stats}
    if len(anomalies): sheets['Anomalías horas']=anomalies
    outfile=OUT/f'MAESTRO_{category}_Coronel_2023-2025_v2_horas.xlsx'
    write_xlsx(outfile,sheets)
    result.to_pickle(TMP/f'{category.casefold()}_horas.pkl')
    all_stats[category]={'archivo':str(outfile.relative_to(ROOT)),'filas':len(result),'sha256':sha256(outfile),
                         'estadisticas':stats.to_dict('records'),'anomalias':anomalies.to_dict('records')}
    print('\n'+category+'\n'+stats.to_string(index=False))
    print('Archivo:',outfile)
(TMP/'horas_recuperacion_resumen.json').write_text(json.dumps(all_stats,ensure_ascii=False,indent=2),encoding='utf-8')
