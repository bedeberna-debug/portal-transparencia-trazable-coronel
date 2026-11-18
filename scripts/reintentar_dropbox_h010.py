import hashlib,html,json,os,re,threading,time,unicodedata
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
from zoneinfo import ZoneInfo
import pandas as pd
import requests
from bs4 import BeautifulSoup
from utilidades_personal import ROOT,OUT,TMP,write_xlsx,sha256

ARCHIVE=ROOT/'archivo externo'/'informes_funciones_honorarios'
OUTDIR=OUT/'informes_honorarios'
CHECKPOINT=TMP/'reintentos_dropbox_checkpoint.csv'
BATCH=50; WORKERS=8; MAX_ATTEMPTS=2
local=threading.local()

def now(): return datetime.now(ZoneInfo('America/Santiago')).isoformat(timespec='seconds')
def session():
    if not hasattr(local,'s'):
        s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36'
        local.s=s
    return local.s

def urls(url):
    p=urlsplit(url); q=dict(parse_qsl(p.query,keep_blank_values=True))
    q1=dict(q); q1['dl']='1'; q1.pop('raw',None)
    q2=dict(q); q2.pop('dl',None); q2['raw']='1'
    q3=dict(q); q3.pop('dl',None); q3.pop('raw',None)
    return [('dl=1',urlunsplit((p.scheme,p.netloc,p.path,urlencode(q1),''))),
            ('raw=1',urlunsplit((p.scheme,p.netloc,p.path,urlencode(q2),''))),
            ('host_directo',urlunsplit(('https','dl.dropboxusercontent.com',p.path,urlencode(q3),'')))]

def safe_name(url,key):
    base=Path(urlsplit(url).path).name or 'informe.pdf'
    base=unicodedata.normalize('NFKD',base).encode('ascii','ignore').decode('ascii')
    base=re.sub(r'[^A-Za-z0-9._-]+','_',base).strip('._') or 'informe.pdf'
    if not base.lower().endswith('.pdf'): base+='.pdf'
    return f'{Path(base).stem[-55:]}_{hashlib.sha1(key.encode()).hexdigest()[:10]}.pdf'

def response_info(resp,content):
    info={'http':resp.status_code,'url_final':resp.url,'content_type':resp.headers.get('Content-Type',''),
          'bytes_respuesta':len(content),'sha256_respuesta':hashlib.sha256(content).hexdigest(),
          'titulo':'','texto_visible':'','es_pdf':b'%PDF-' in content[:1024]}
    if info['es_pdf']:
        # Conservar el cuerpo validado evita que una segunda respuesta HTML anule una recuperación.
        info['_content']=content
    else:
        soup=BeautifulSoup(content[:2000000],'html.parser')
        info['titulo']=soup.title.get_text(' ',strip=True) if soup.title else ''
        info['texto_visible']=re.sub(r'\s+',' ',soup.get_text(' ',strip=True))[:600]
    return info

def request_variant(s,url):
    for attempt in range(1,MAX_ATTEMPTS+1):
        try:
            r=s.get(url,timeout=(20,60),allow_redirects=True)
            content=r.content
            if (r.status_code==429 or r.status_code>=500) and attempt<MAX_ATTEMPTS:
                retry=r.headers.get('Retry-After',''); time.sleep(min(int(retry) if retry.isdigit() else 3,60)); continue
            return response_info(r,content),'',attempt
        except Exception as e:
            if attempt==MAX_ATTEMPTS: return None,repr(e),attempt
            time.sleep(attempt*2)

def process(item):
    key,year,month,url=item; variants=urls(url); history=[]; attempts=0
    dest=ARCHIVE/str(year)/f'{month:02d}'/safe_name(url,key)
    base={'clave_objeto':key,'anio':year,'mes_numero':month,'url_original':url,'url_reintento':variants[0][1],
          'fecha_verificacion':now(),'estado':'','codigo_http':pd.NA,'http_dl1':pd.NA,'content_type':'','url_final':'',
          'titulo_respuesta':'','texto_visible':'','sha256_respuesta':'','bytes_respuesta':0,'variantes_utilizadas':'',
          'archivo_relativo':'','fecha_descarga':'','sha256':'','bytes':0,'error':''}
    # Primero se reintenta dl=1 en TODOS los casos; las variantes solo se aplican si no hay eliminación explícita.
    for vi,(method,request_url) in enumerate(variants):
        info,error,nattempt=request_variant(session(),request_url); attempts+=nattempt
        if info is None:
            history.append({'variante':method,'error':error}); base['error']=error
            continue
        history.append({'variante':method,**{k:v for k,v in info.items() if k not in ('texto_visible','_content')}})
        base.update({'codigo_http':info['http'],'content_type':info['content_type'],'url_final':info['url_final'],
                     'titulo_respuesta':info['titulo'],'texto_visible':info['texto_visible'],
                     'sha256_respuesta':info['sha256_respuesta'],'bytes_respuesta':info['bytes_respuesta']})
        if vi==0: base['http_dl1']=info['http']
        if info['es_pdf']:
            content=info['_content']
            dest.parent.mkdir(parents=True,exist_ok=True); temp=dest.with_suffix('.pdf.part')
            temp.write_bytes(content); os.replace(temp,dest)
            base.update({'estado':'descargado_recuperado','archivo_relativo':str(dest.relative_to(ROOT)),
                         'fecha_descarga':now(),'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content),
                         'metodo_recuperacion':method,'error':''})
            break
        title=info['titulo'].casefold()
        if vi==0 and 'file deleted' in title:
            base['estado']='dropbox_file_deleted'; base['error']='Dropbox informa File Deleted con dl=1'; break
        if vi==1 and 'file deleted' in title:
            base['estado']='dropbox_file_deleted'; base['error']='Dropbox informa File Deleted con dl=1 y raw=1'; break
        if 'link temporarily disabled' in title:
            base['estado']='dropbox_link_temporarily_disabled'; base['error']=f'Dropbox informa Link Temporarily Disabled con {method}'; break
        if vi==2:
            base['estado']='no_pdf' if info['http']==200 else 'http_error'
            if not base['error']: base['error']='Sin PDF tras dl=1, raw=1 y host directo'
    base['variantes_utilizadas']='|'.join(h['variante'] for h in history)
    base['historial_json']=json.dumps(history,ensure_ascii=False)
    base['intentos']=attempts
    if not base['estado']: base['estado']='error_red'
    return base

m=pd.read_excel(OUTDIR/'MANIFIESTO_DESCARGAS_v1.xlsx',sheet_name='Manifiesto')
f=m[m['estado']=='no_pdf'][['anio','mes_numero','url_original']].drop_duplicates().reset_index(drop=True)
items=[(f"{int(r['anio'])}|{int(r['mes_numero']):02d}|{r['url_original']}",int(r['anio']),int(r['mes_numero']),r['url_original']) for _,r in f.iterrows()]
previous={}
if CHECKPOINT.exists():
    old=pd.read_csv(CHECKPOINT,dtype=str).fillna('')
    for _,r in old.iterrows():
        # Solo se reutilizan resultados terminales. Dropbox puede alternar HTML y PDF
        # para una misma URL; los demás estados se vuelven a intentar al reanudar.
        if r.get('estado') not in ('descargado_recuperado','dropbox_file_deleted','dropbox_link_temporarily_disabled'): continue
        if r.get('estado')=='descargado_recuperado':
            p=ROOT/r.get('archivo_relativo','')
            if not p.exists() or sha256(p)!=r.get('sha256'): continue
        previous[r['clave_objeto']]=r.to_dict()
results=list(previous.values()); pending=[x for x in items if x[0] not in previous]
print(f'Reintentos: {len(items)}; reutilizados: {len(previous)}; pendientes: {len(pending)}',flush=True)
for start in range(0,len(pending),BATCH):
    batch=pending[start:start+BATCH]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures={pool.submit(process,x):x for x in batch}
        for fut in as_completed(futures):
            try: results.append(fut.result())
            except Exception as e:
                x=futures[fut]; results.append({'clave_objeto':x[0],'anio':x[1],'mes_numero':x[2],'url_original':x[3],
                    'fecha_verificacion':now(),'estado':'error_interno','error':repr(e),'variantes_utilizadas':'','intentos':0})
    pd.DataFrame(results).to_csv(CHECKPOINT,index=False,encoding='utf-8-sig')
    states=pd.Series([r['estado'] for r in results]).value_counts().to_dict()
    print(f'Lote {start//BATCH+1}: {len(results)}/{len(items)}; {states}',flush=True)

res=pd.DataFrame(results)
# Al reanudar, el checkpoint entrega números como texto; normalizar antes de actualizar el manifiesto.
for c in ['anio','mes_numero','codigo_http','http_dl1','bytes_respuesta','bytes','intentos']:
    if c in res: res[c]=pd.to_numeric(res[c],errors='coerce')
res.to_csv(CHECKPOINT,index=False,encoding='utf-8-sig')
# Selección de columnas para libro de evidencia; historial_json conserva el detalle por variante.
retry_sheets={'Objetos':res,'Resumen estados':res.groupby('estado').size().rename('objetos').reset_index(),
              'Títulos':res.groupby(['estado','titulo_respuesta'],dropna=False).size().rename('objetos').reset_index()}
ua_diagnostic=TMP/'diagnostico_user_agent_dropbox.json'
if ua_diagnostic.exists(): retry_sheets['Diagnóstico cliente']=pd.DataFrame(json.loads(ua_diagnostic.read_text(encoding='utf-8')))
write_xlsx(OUTDIR/'REINTENTOS_DROPBOX_H010_v1.xlsx',retry_sheets)

# Manifest v2: conserva v1 y agrega diagnóstico/reintento sin alterar los éxitos anteriores.
man=m.copy()
for c in ['fecha_verificacion','content_type','url_final','titulo_respuesta','sha256_respuesta','variantes_utilizadas','metodo_recuperacion','historial_intentos']:
    man[c]=''
lookup={r['clave_objeto']:r for _,r in res.iterrows()}
for idx,row in man[man['estado']=='no_pdf'].iterrows():
    key=f"{int(row['anio'])}|{int(row['mes_numero']):02d}|{row['url_original']}"; r=lookup[key]
    old=f"v1: dl=1, HTTP {int(row['codigo_http'])}, no_pdf"
    man.at[idx,'historial_intentos']=old+f" | v2: {r.get('variantes_utilizadas','')}, {r['estado']}"
    for c in ['fecha_verificacion','content_type','url_final','titulo_respuesta','sha256_respuesta','variantes_utilizadas']:
        man.at[idx,c]=r.get(c,'')
    if r['estado']=='descargado_recuperado':
        man.at[idx,'estado']='descargado'
        for c in ['archivo_relativo','fecha_descarga','sha256','bytes']: man.at[idx,c]=r[c]
        man.at[idx,'codigo_http']=r['codigo_http']; man.at[idx,'metodo_recuperacion']=r.get('metodo_recuperacion','')
        man.at[idx,'error']='Recuperado en reintento H-010'
    else:
        man.at[idx,'estado']=r['estado']; man.at[idx,'codigo_http']=r.get('codigo_http',pd.NA)
        man.at[idx,'error']=r.get('error',''); man.at[idx,'archivo_relativo']=''; man.at[idx,'sha256']=''; man.at[idx,'bytes']=0
man.loc[man['historial_intentos']=='','historial_intentos']='v1: '+man['estado'].astype(str)
man['codigo_http']=pd.to_numeric(man['codigo_http'],errors='coerce').astype('Int64')
man['bytes']=pd.to_numeric(man['bytes'],errors='coerce').fillna(0).astype('int64')
status=man.groupby('estado').size().rename('registros').reset_index()
monthly=man.groupby(['anio','mes_numero','estado']).size().rename('registros').reset_index()
summary=pd.DataFrame([
 {'indicador':'Objetos reintentados con dl=1','valor':len(res)},
 {'indicador':'Objetos recuperados en reintento','valor':int((res['estado']=='descargado_recuperado').sum())},
 {'indicador':'Objetos File Deleted explícitos','valor':int((res['estado']=='dropbox_file_deleted').sum())},
 {'indicador':'Objetos Link Temporarily Disabled explícitos','valor':int((res['estado']=='dropbox_link_temporarily_disabled').sum())},
 {'indicador':'Objetos con otros estados','valor':int((~res['estado'].isin(['descargado_recuperado','dropbox_file_deleted','dropbox_link_temporarily_disabled'])).sum())},
 {'indicador':'PDF únicos totales confirmados','valor':man.loc[man['estado']=='descargado','archivo_relativo'].nunique()},
 {'indicador':'Registros totales con PDF','valor':int((man['estado']=='descargado').sum())},
 {'indicador':'Registros sin URL','valor':int((man['estado']=='sin_url').sum())},
 {'indicador':'Generado','valor':now()}])
write_xlsx(OUTDIR/'MANIFIESTO_DESCARGAS_v2.xlsx',{'Manifiesto':man,'Resumen':summary,'Estados':status,'Por mes':monthly,
    'Fallidos':man[man['tiene_url']&man['estado'].ne('descargado')]})
man.to_csv(OUTDIR/'MANIFIESTO_DESCARGAS_v2.csv',index=False,encoding='utf-8-sig')
stats={'objetos_reintentados':len(res),'recuperados':int((res['estado']=='descargado_recuperado').sum()),
       'file_deleted':int((res['estado']=='dropbox_file_deleted').sum()),
       'link_temporarily_disabled':int((res['estado']=='dropbox_link_temporarily_disabled').sum()),
       'otros':res.loc[~res['estado'].isin(['descargado_recuperado','dropbox_file_deleted','dropbox_link_temporarily_disabled']),'estado'].value_counts().to_dict(),
       'pdf_unicos_totales':int(man.loc[man['estado']=='descargado','archivo_relativo'].nunique()),
       'registros_pdf_totales':int((man['estado']=='descargado').sum()),'sin_url':int((man['estado']=='sin_url').sum()),
       'estados_registros':man['estado'].value_counts().to_dict(),'generado':now()}
(TMP/'reintentos_h010_resumen.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2),flush=True)
