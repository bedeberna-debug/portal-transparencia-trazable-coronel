import hashlib,json,re
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
import pandas as pd
import requests
from bs4 import BeautifulSoup
from utilidades_personal import ROOT,TMP

m=pd.read_excel(ROOT/'datos procesados'/'04_Personal_y_Remuneraciones'/'informes_honorarios'/'MANIFIESTO_DESCARGAS_v1.xlsx',sheet_name='Manifiesto')
samples=m[m['estado']=='no_pdf'].drop_duplicates('url_original').head(3).to_dict('records')

def variants(url):
    p=urlsplit(url); q=dict(parse_qsl(p.query,keep_blank_values=True))
    q1=dict(q); q1['dl']='1'; q1.pop('raw',None)
    q2=dict(q); q2.pop('dl',None); q2['raw']='1'
    q3=dict(q); q3.pop('dl',None); q3.pop('raw',None)
    return {
      'dl_1':urlunsplit((p.scheme,p.netloc,p.path,urlencode(q1),'')),
      'raw_1':urlunsplit((p.scheme,p.netloc,p.path,urlencode(q2),'')),
      'host_directo':urlunsplit(('https','dl.dropboxusercontent.com',p.path,urlencode(q3),''))}

results=[]
s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36'
for row in samples:
    for name,url in variants(row['url_original']).items():
        try:
            r=s.get(url,timeout=(20,45),allow_redirects=True)
            content=r.content; ispdf=b'%PDF-' in content[:1024]
            item={'url_original':row['url_original'],'variante':name,'url_solicitada':url,'http':r.status_code,
                  'url_final':r.url,'content_type':r.headers.get('Content-Type',''),'bytes':len(content),
                  'es_pdf':ispdf,'sha256_respuesta':hashlib.sha256(content).hexdigest()}
            if not ispdf:
                soup=BeautifulSoup(content[:2000000],'html.parser')
                item['titulo']=soup.title.get_text(' ',strip=True) if soup.title else ''
                text=re.sub(r'\s+',' ',soup.get_text(' ',strip=True))[:1200]
                item['texto_visible']=text
                item['inicio_html']=content[:300].decode('utf-8','replace')
            results.append(item)
            print(name,r.status_code,r.headers.get('Content-Type',''),len(content),'PDF',ispdf,'final',r.url,'titulo',item.get('titulo',''),flush=True)
        except Exception as e:
            results.append({'url_original':row['url_original'],'variante':name,'url_solicitada':url,'error':repr(e)})
            print(name,'ERROR',repr(e),flush=True)
(TMP/'diagnostico_dropbox.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
