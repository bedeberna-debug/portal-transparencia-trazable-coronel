import json
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
import pandas as pd
from utilidades_personal import *

OUTDIR=OUT/'informes_honorarios'
OUTDIR.mkdir(parents=True,exist_ok=True)
d=pd.read_pickle(TMP/'canonico_honorarios.pkl')

def download_url(url):
    if not url: return ''
    parts=urlsplit(url); q=dict(parse_qsl(parts.query,keep_blank_values=True)); q['dl']='1'
    return urlunsplit((parts.scheme,parts.netloc,parts.path,urlencode(q),parts.fragment))

inv=pd.DataFrame({
 'registro_id':d['registro_id'],'id_trabajador':d['id_trabajador'],'trabajador':d['nombre_normalizado'],
 'anio':d['anio'].astype(int),'mes_numero':d['mes_numero'].astype(int),'mes_nombre':d['mes_nombre'],'periodo':d['periodo'],
 'url_original':d['enlace_funciones_desarrolladas_url'].fillna(''),
 'fuente_archivo':d['fuente_archivo'],'fuente_ruta_relativa':d['fuente_ruta_relativa'],
 'fuente_fila_csv':d['fuente_fila_csv'].astype(int),'fuente_sha256':d['fuente_sha256']})
inv['url_descarga']=inv['url_original'].map(download_url)
inv['tiene_url']=inv['url_original']!=''
inv['es_dropbox']=inv['url_original'].str.contains('dropbox.com',case=False,regex=False)
inv['inventario_id']=['INF-'+str(i).zfill(6) for i in range(1,len(inv)+1)]
inv=inv[['inventario_id','registro_id','id_trabajador','trabajador','anio','mes_numero','mes_nombre','periodo','url_original','url_descarga','tiene_url','es_dropbox','fuente_archivo','fuente_ruta_relativa','fuente_fila_csv','fuente_sha256']]
summary=pd.DataFrame([
 {'indicador':'Registros de honorarios','valor':len(inv)},
 {'indicador':'Registros con URL','valor':int(inv['tiene_url'].sum())},
 {'indicador':'Registros sin URL','valor':int((~inv['tiene_url']).sum())},
 {'indicador':'URLs únicas','valor':inv.loc[inv['tiene_url'],'url_original'].nunique()},
 {'indicador':'Objetos únicos año/mes/URL a descargar','valor':inv.loc[inv['tiene_url'], ['anio','mes_numero','url_original']].drop_duplicates().shape[0]},
 {'indicador':'URLs no Dropbox','valor':int((inv['tiene_url']&~inv['es_dropbox']).sum())},
 {'indicador':'Criterio de URL de descarga','valor':'Parámetro dl=1; URL original preservada'},
])
write_xlsx(OUTDIR/'INVENTARIO_INFORMES_HONORARIOS_v1.xlsx',{'Inventario':inv,'Resumen':summary})
inv.to_pickle(TMP/'inventario_honorarios.pkl')
inv.to_csv(OUTDIR/'INVENTARIO_INFORMES_HONORARIOS_v1.csv',index=False,encoding='utf-8-sig')
stats={'registros':len(inv),'con_url':int(inv['tiene_url'].sum()),'sin_url':int((~inv['tiene_url']).sum()),
       'urls_unicas':int(inv.loc[inv['tiene_url'],'url_original'].nunique()),
       'objetos_unicos':int(inv.loc[inv['tiene_url'],['anio','mes_numero','url_original']].drop_duplicates().shape[0]),
       'no_dropbox':int((inv['tiene_url']&~inv['es_dropbox']).sum())}
(TMP/'inventario_honorarios_resumen.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
print('Archivo:',OUTDIR/'INVENTARIO_INFORMES_HONORARIOS_v1.xlsx')
