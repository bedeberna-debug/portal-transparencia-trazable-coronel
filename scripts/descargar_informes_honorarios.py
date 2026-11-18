import hashlib, json, os, re, threading, time, unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
import pandas as pd
import requests
from utilidades_personal import *

ARCHIVE=ROOT/'archivo externo'/'informes_funciones_honorarios'
OUTDIR=OUT/'informes_honorarios'
CHECKPOINT=TMP/'descargas_objetos_checkpoint.csv'
BATCH_SIZE=50
WORKERS=8
MAX_ATTEMPTS=3
thread_local=threading.local()

def now(): return datetime.now(ZoneInfo('America/Santiago')).isoformat(timespec='seconds')
def session():
    if not hasattr(thread_local,'s'):
        s=requests.Session(); s.headers.update({'User-Agent':'Mozilla/5.0 (compatible; PortalTransparenciaCoronel/1.0; archivo-documental)'})
        thread_local.s=s
    return thread_local.s

def safe_name(url,key):
    base=Path(urlsplit(url).path).name or 'informe.pdf'
    base=unicodedata.normalize('NFKD',base).encode('ascii','ignore').decode('ascii')
    base=re.sub(r'[^A-Za-z0-9._-]+','_',base).strip('._') or 'informe.pdf'
    if not base.lower().endswith('.pdf'): base+='.pdf'
    stem=Path(base).stem[-55:]; digest=hashlib.sha1(key.encode()).hexdigest()[:10]
    return f'{stem}_{digest}.pdf'

def valid_pdf(path):
    try:
        with Path(path).open('rb') as f: return b'%PDF-' in f.read(1024)
    except OSError: return False

def key_of(r): return f"{int(r['anio'])}|{int(r['mes_numero']):02d}|{r['url_original']}"

def fetch(item):
    key,year,month,url,dlurl=item
    dest=ARCHIVE/str(year)/f'{month:02d}'/safe_name(url,key)
    rel=str(dest.relative_to(ROOT))
    result={'clave_objeto':key,'anio':year,'mes_numero':month,'url_original':url,'url_descarga':dlurl,
            'archivo_relativo':rel,'fecha_descarga':'','codigo_http':pd.NA,'estado':'','bytes':0,'sha256':'','intentos':0,'error':''}
    if dest.exists() and valid_pdf(dest):
        h=hashlib.sha256()
        with dest.open('rb') as f:
            for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
        result.update({'fecha_descarga':now(),'estado':'descargado','bytes':dest.stat().st_size,'sha256':h.hexdigest(),'error':'Archivo local preexistente validado; no se repitió la solicitud HTTP'})
        return result
    dest.parent.mkdir(parents=True,exist_ok=True)
    last_error=''
    for attempt in range(1,MAX_ATTEMPTS+1):
        result['intentos']=attempt
        temp=dest.with_suffix('.pdf.part')
        try:
            with session().get(dlurl,stream=True,allow_redirects=True,timeout=(20,75)) as resp:
                result['codigo_http']=int(resp.status_code)
                if resp.status_code==429 or resp.status_code>=500:
                    last_error=f'HTTP {resp.status_code}'
                    if attempt<MAX_ATTEMPTS:
                        retry=resp.headers.get('Retry-After','')
                        delay=min(max(int(retry) if retry.isdigit() else attempt*3,1),60)
                        time.sleep(delay)
                        continue
                if resp.status_code!=200:
                    last_error=f'HTTP {resp.status_code}'
                    break
                h=hashlib.sha256(); size=0; first=b''
                with temp.open('wb') as f:
                    for chunk in resp.iter_content(1024*128):
                        if not chunk: continue
                        if len(first)<1024: first=(first+chunk)[:1024]
                        f.write(chunk); h.update(chunk); size+=len(chunk)
                result['bytes']=size
                if b'%PDF-' not in first:
                    temp.unlink(missing_ok=True)
                    last_error='HTTP 200 pero la respuesta no contiene firma PDF'
                    result['estado']='no_pdf'
                    break
                os.replace(temp,dest)
                result.update({'fecha_descarga':now(),'estado':'descargado','sha256':h.hexdigest(),'error':''})
                return result
        except Exception as e:
            temp.unlink(missing_ok=True)
            last_error=f'{type(e).__name__}: {e}'[:700]
            if attempt<MAX_ATTEMPTS: time.sleep(attempt*2)
    result['fecha_descarga']=now()
    if not result['estado']: result['estado']='http_error' if str(result['codigo_http']) not in ('<NA>','nan','') else 'error_red'
    result['error']=last_error
    result['archivo_relativo']=rel if dest.exists() and valid_pdf(dest) else ''
    result['bytes']=dest.stat().st_size if result['archivo_relativo'] else 0
    return result

inv=pd.read_pickle(TMP/'inventario_honorarios.pkl')
withurl=inv[inv['tiene_url']].copy()
targets=withurl[['anio','mes_numero','url_original','url_descarga']].drop_duplicates().reset_index(drop=True)
items=[(key_of(r),int(r['anio']),int(r['mes_numero']),r['url_original'],r['url_descarga']) for _,r in targets.iterrows()]
previous={}
if CHECKPOINT.exists():
    old=pd.read_csv(CHECKPOINT,dtype=str).fillna('')
    for _,r in old.iterrows():
        if r.get('estado')=='descargado':
            if r.get('archivo_relativo') and valid_pdf(ROOT/r['archivo_relativo']): previous[r['clave_objeto']]=r.to_dict()
        else:
            # Los fallos ya comprobados no se reintentan en una reanudación técnica.
            previous[r['clave_objeto']]=r.to_dict()
results=list(previous.values())
pending=[x for x in items if x[0] not in previous]
print(f'Objetos: {len(items)}; reutilizados: {len(previous)}; pendientes: {len(pending)}',flush=True)
for start in range(0,len(pending),BATCH_SIZE):
    batch=pending[start:start+BATCH_SIZE]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures={pool.submit(fetch,item):item for item in batch}
        for fut in as_completed(futures):
            try: results.append(fut.result())
            except Exception as e:
                item=futures[fut]
                results.append({'clave_objeto':item[0],'anio':item[1],'mes_numero':item[2],'url_original':item[3],'url_descarga':item[4],
                                'archivo_relativo':'','fecha_descarga':now(),'codigo_http':pd.NA,'estado':'error_interno','bytes':0,'sha256':'','intentos':0,'error':repr(e)})
    checkpoint=pd.DataFrame(results)
    checkpoint.to_csv(CHECKPOINT,index=False,encoding='utf-8-sig')
    done=len(results); ok=int((checkpoint['estado']=='descargado').sum())
    print(f'Lote {start//BATCH_SIZE+1}: procesados {done}/{len(items)}; PDF confirmados {ok}',flush=True)

res=pd.DataFrame(results)
res['anio']=pd.to_numeric(res['anio'],errors='raise').astype(int)
res['mes_numero']=pd.to_numeric(res['mes_numero'],errors='raise').astype(int)
res.to_csv(CHECKPOINT,index=False,encoding='utf-8-sig')
man=inv.merge(res[['clave_objeto','anio','mes_numero','url_original','archivo_relativo','fecha_descarga','codigo_http','estado','bytes','sha256','intentos','error']],
              left_on=['anio','mes_numero','url_original'],right_on=['anio','mes_numero','url_original'],how='left')
man=man.drop(columns=['clave_objeto'])
man.loc[~man['tiene_url'],'estado']='sin_url'
man['estado']=man['estado'].fillna('error_interno')
for c in ['archivo_relativo','fecha_descarga','sha256','error']: man[c]=man[c].fillna('')
man['bytes']=pd.to_numeric(man['bytes'],errors='coerce').fillna(0).astype('int64')
man['codigo_http']=pd.to_numeric(man['codigo_http'],errors='coerce').astype('Int64')
man['intentos']=pd.to_numeric(man['intentos'],errors='coerce').fillna(0).astype('int64')
# El manifiesto conserva una fila por relación trabajador-mes-URL del inventario.
cols=['inventario_id','registro_id','id_trabajador','trabajador','anio','mes_numero','mes_nombre','periodo','url_original','url_descarga','tiene_url',
      'fuente_archivo','fuente_fila_csv','estado','codigo_http','fecha_descarga','bytes','sha256','archivo_relativo','intentos','error']
man=man[cols]
status=man.groupby('estado',dropna=False).size().rename('registros').reset_index()
monthly=man.groupby(['anio','mes_numero','estado']).size().rename('registros').reset_index()
summary=pd.DataFrame([
 {'indicador':'Relaciones trabajador-mes-URL','valor':len(man)},
 {'indicador':'Objetos únicos solicitados','valor':len(items)},
 {'indicador':'Registros con PDF confirmado','valor':int((man['estado']=='descargado').sum())},
 {'indicador':'Objetos PDF únicos confirmados','valor':int((res['estado']=='descargado').sum())},
 {'indicador':'Registros sin URL','valor':int((man['estado']=='sin_url').sum())},
 {'indicador':'Registros fallidos con URL','valor':int((man['tiene_url']&(man['estado']!='descargado')).sum())},
 {'indicador':'Bytes PDF únicos','valor':int(pd.to_numeric(res.loc[res['estado']=='descargado','bytes'],errors='coerce').sum())},
 {'indicador':'Validación PDF','valor':'HTTP 200 y firma %PDF- en los primeros 1024 bytes; SHA-256 calculado sobre archivo final'},
 {'indicador':'Generado','valor':now()}])
write_xlsx(OUTDIR/'MANIFIESTO_DESCARGAS_v1.xlsx',{'Manifiesto':man,'Resumen':summary,'Estados':status,'Por mes':monthly,
                                                  'Fallidos':man[(man['tiene_url'])&(man['estado']!='descargado')]})
man.to_csv(OUTDIR/'MANIFIESTO_DESCARGAS_v1.csv',index=False,encoding='utf-8-sig')
stats={'relaciones':len(man),'objetos':len(items),'registros_pdf':int((man['estado']=='descargado').sum()),
       'objetos_pdf':int((res['estado']=='descargado').sum()),'sin_url':int((man['estado']=='sin_url').sum()),
       'fallidos_con_url':int((man['tiene_url']&(man['estado']!='descargado')).sum()),
       'estados_objetos':res['estado'].value_counts().to_dict(),'bytes_unicos':int(pd.to_numeric(res.loc[res['estado']=='descargado','bytes'],errors='coerce').sum()),
       'generado':now()}
(TMP/'descargas_resumen.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2),flush=True)
