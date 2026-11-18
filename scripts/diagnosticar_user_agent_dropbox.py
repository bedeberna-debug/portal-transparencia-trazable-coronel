import hashlib,json
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from utilidades_personal import ROOT,TMP

checkpoint=pd.read_csv(TMP/'reintentos_dropbox_checkpoint.csv',dtype=str).fillna('')
samples=checkpoint[checkpoint['estado']=='descargado_recuperado'].head(3)
uas={
 'v1_agente_archivo':'Mozilla/5.0 (compatible; PortalTransparenciaCoronel/1.0; archivo-documental)',
 'v2_agente_navegador':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36'
}
rows=[]
for _,item in samples.iterrows():
    for label,ua in uas.items():
        try:
            r=requests.get(item['url_reintento'],headers={'User-Agent':ua},timeout=(20,60),allow_redirects=True)
            content=r.content
            is_pdf=b'%PDF-' in content[:1024]
            soup=BeautifulSoup(content[:2000000],'html.parser') if not is_pdf else None
            rows.append({'clave_objeto':item['clave_objeto'],'agente':label,'url':item['url_reintento'],
                         'http':r.status_code,'content_type':r.headers.get('Content-Type',''),
                         'es_pdf':is_pdf,'titulo':soup.title.get_text(' ',strip=True) if soup is not None and soup.title else '',
                         'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'error':''})
        except Exception as e:
            rows.append({'clave_objeto':item['clave_objeto'],'agente':label,'url':item['url_reintento'],
                         'http':None,'content_type':'','es_pdf':False,'titulo':'','bytes':0,'sha256':'','error':repr(e)})
out=TMP/'diagnostico_user_agent_dropbox.json'
out.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
