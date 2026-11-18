import json,re
from pathlib import Path
import pandas as pd
from utilidades_personal import *

controls=[]; totals=[]
def check(area,name,ok,detail):
    controls.append({'area':area,'control':name,'resultado':'OK' if ok else 'FALLA','detalle':str(detail)})
    if not ok: print('FALLA:',area,name,detail)

initial=json.loads((TMP/'inventario_csv.json').read_text(encoding='utf-8'))
changed=[]
for item in initial:
    p=ROOT/item['ruta']
    if not p.exists() or sha256(p)!=item['sha256']: changed.append(item['ruta'])
check('Originales','168 CSV conservan SHA-256 de inspección inicial',not changed,f'Modificados: {len(changed)}')
master_initial=json.loads((TMP/'esquemas_maestros.json').read_text(encoding='utf-8'))
changed=[]
for name,item in master_initial.items():
    p=ROOT/item['ruta']
    if not p.exists() or sha256(p)!=item['sha256']: changed.append(item['ruta'])
check('Originales','4 maestros manuales conservan SHA-256 inicial',not changed,f'Modificados: {len(changed)}')

filekeys={'Planta':'planta','Contrata':'contrata','Código del Trabajo':'código_del_trabajo','Honorarios':'honorarios'}
folders={'Planta':'01_Personal_Planta','Contrata':'02_Personal_Contrata','Código del Trabajo':'03_Personal_por_Código_del_Trabajo','Honorarios':'04_Personal_Honorarios'}
files={'Planta':'MAESTRO_Planta_Coronel_2023-2025_canonico_v1.xlsx','Contrata':'MAESTRO_Contrata_Coronel_2023-2025_canonico_v1.xlsx','Código del Trabajo':'MAESTRO_CODTrabajo_Coronel_2023-2025_canonico_v1.xlsx','Honorarios':'MAESTRO_Honorarios_Coronel_2023-2025_canonico_v1.xlsx'}
all_dictionary=pd.read_excel(DOCS/'DICCIONARIO_DATOS_v1.xlsx',sheet_name='Diccionario completo')
for cat,key in filekeys.items():
    d=pd.read_pickle(TMP/f'canonico_{key}.pkl')
    x=pd.read_excel(OUT/files[cat],sheet_name='Datos')
    raw=load_raw_category(folders[cat])
    check(cat,'Filas CSV = canónico',len(raw)==len(d)==len(x),f'CSV {len(raw)}; memoria {len(d)}; XLSX {len(x)}')
    check(cat,'ID de registro únicos y completos',d['registro_id'].is_unique and d['registro_id'].notna().all(),f'{d["registro_id"].nunique()} IDs para {len(d)} filas')
    check(cat,'Trazabilidad completa',all(d[c].notna().all() for c in ['fuente_archivo','fuente_ruta_relativa','fuente_fila_csv','fuente_sha256']),'Archivo/ruta/fila/hash sin nulos')
    check(cat,'Par archivo+fila único',not d.duplicated(['fuente_ruta_relativa','fuente_fila_csv']).any(),'0 duplicados')
    bad_hash=[]; bad_source=[]
    raw_index=raw.set_index(['fuente_ruta_relativa','fuente_fila_csv'],drop=False)
    for _,r in d.iterrows():
        p=ROOT/r['fuente_ruta_relativa']
        if not p.exists() or sha256(p)!=r['fuente_sha256']: bad_hash.append(r['registro_id'])
        k=(r['fuente_ruta_relativa'],int(r['fuente_fila_csv']))
        if k not in raw_index.index: bad_source.append(r['registro_id']); continue
        rr=raw_index.loc[k]
        if isinstance(rr,pd.DataFrame): rr=rr.iloc[0]
        if norm(rr['Nombre completo'])!=norm(r['nombre_original']) or norm(rr['Año'])!=str(r['anio']) or MESES[norm(rr['Mes'])]!=int(r['mes_numero']): bad_source.append(r['registro_id'])
    check(cat,'SHA-256 de cada fila coincide con CSV actual',not bad_hash,f'Fallos: {len(bad_hash)}')
    check(cat,'Nombre y período coinciden con fila CSV',not bad_source,f'Fallos: {len(bad_source)}')
    # Todo par _raw/_clp y _raw/_horas se recalcula independientemente.
    numeric_errors={}
    for col in d.columns:
        if col.endswith('_clp') and col[:-4]+'_raw' in d:
            expected=d[col[:-4]+'_raw'].map(money)
            n=int((pd.to_numeric(d[col],errors='coerce')!=expected).sum())
            if n: numeric_errors[col]=n
        if col.endswith('_horas') and col[:-6]+'_raw' in d:
            expected=d[col[:-6]+'_raw'].map(hours)
            n=int((pd.to_numeric(d[col],errors='coerce')!=expected).sum())
            if n: numeric_errors[col]=n
    check(cat,'Importes y horas derivados del raw',not numeric_errors,numeric_errors or '0 diferencias')
    expected_cols=set(d.columns); documented=set(all_dictionary.loc[all_dictionary['maestro']==cat,'columna_canonica'])
    check(cat,'Diccionario cubre todas las columnas',expected_cols==documented,f'Faltan {expected_cols-documented}; sobran {documented-expected_cols}')
    dup=d[d.duplicated(['periodo','nombre_normalizado'],keep=False)]
    check(cat,'Duplicados período-nombre acotados y registrados',len(dup)==(2 if cat in ('Planta','Código del Trabajo') else 0),f'{len(dup)} filas involucradas')
    sums={'maestro':cat,'registros':len(d),'trabajadores_id':d['id_trabajador'].nunique(),
          'bruta_clp':int(d['remuneracion_bruta_clp'].sum()),'liquida_clp':int(d['remuneracion_liquida_clp'].sum()),
          'horas_diurnas':float(d['horas_extra_diurnas_horas'].sum()) if 'horas_extra_diurnas_horas' in d else None,
          'horas_nocturnas':float(d['horas_extra_nocturnas_horas'].sum()) if 'horas_extra_nocturnas_horas' in d else None,
          'horas_festivas':float(d['horas_extra_festivas_horas'].sum()) if 'horas_extra_festivas_horas' in d else None,
          'horas_sin_desagregar':float(d['horas_extra_horas'].sum()) if 'horas_extra_horas' in d else None}
    totals.append(sums)

# Controles específicos de versiones intermedias entregables.
cod=pd.read_excel(OUT/'MAESTRO_CODTrabajo_Coronel_2023-2025_v2_corregido.xlsx',sheet_name='Datos Completos').fillna('')
check('Código corregido','Origen y trazabilidad no vacíos',(cod['_archivo_origen'].map(norm)!='').all() and (cod['fuente_ruta_relativa'].map(norm)!='').all(),f'{len(cod)} filas')
for cat,prefix in [('Planta','Planta'),('Contrata','Contrata')]:
    h=pd.read_excel(OUT/f'MAESTRO_{prefix}_Coronel_2023-2025_v2_horas.xlsx',sheet_name='Datos Completos')
    for kind in ['diurnas','nocturnas','festivas']:
        rawcol=h['Horas_extra_'+kind] if cat=='Contrata' else h[{'diurnas':'Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta)','nocturnas':'Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta)','festivas':'Montos y horas extraordinarias festivas del mes (inc. en rem. bruta)'}[kind]]
        expected=rawcol.map(hours)
        check(cat,f'Horas {kind} en v2',(pd.to_numeric(h['Horas_extra_'+kind+'_cantidad'],errors='coerce')==expected).all(),f'Suma {expected.sum()}')

# Validación de inventario, reintento H-010, manifiesto vigente y PDF locales.
manifest_path=OUT/'informes_honorarios'/'MANIFIESTO_DESCARGAS_v2.xlsx'
download_summary={}
if manifest_path.exists():
    man=pd.read_excel(manifest_path,sheet_name='Manifiesto')
    man_csv=pd.read_csv(OUT/'informes_honorarios'/'MANIFIESTO_DESCARGAS_v2.csv',dtype=str).fillna('')
    csv_states=man_csv.set_index('inventario_id')['estado'].sort_index()
    xlsx_states=man.assign(inventario_id=man['inventario_id'].astype(str)).set_index('inventario_id')['estado'].astype(str).sort_index()
    check('Honorarios','Manifiesto v2 XLSX y CSV reconciliados',len(man_csv)==len(man) and csv_states.equals(xlsx_states),f'XLSX {len(man)}; CSV {len(man_csv)}; estados idénticos {csv_states.equals(xlsx_states)}')
    inv=pd.read_excel(OUT/'informes_honorarios'/'INVENTARIO_INFORMES_HONORARIOS_v1.xlsx',sheet_name='Inventario')
    retry=pd.read_excel(OUT/'informes_honorarios'/'REINTENTOS_DROPBOX_H010_v1.xlsx',sheet_name='Objetos')
    old=pd.read_excel(OUT/'informes_honorarios'/'MANIFIESTO_DESCARGAS_v1.xlsx',sheet_name='Manifiesto')
    retry_stats=json.loads((TMP/'reintentos_h010_resumen.json').read_text(encoding='utf-8'))
    expected_keys=set((old.loc[old['estado']=='no_pdf','anio'].astype(int).astype(str)+'|'+old.loc[old['estado']=='no_pdf','mes_numero'].astype(int).astype(str).str.zfill(2)+'|'+old.loc[old['estado']=='no_pdf','url_original'].astype(str)))
    check('Honorarios','Inventario y manifiesto conservan todos los registros',len(man)==len(inv)==9464 and man['inventario_id'].is_unique,f'Inventario {len(inv)}; manifiesto {len(man)}')
    check('Honorarios','Reintento exhaustivo de los 5.099 objetos sin PDF',len(retry)==5099 and retry['clave_objeto'].is_unique and set(retry['clave_objeto'])==expected_keys and retry['http_dl1'].notna().all(),f'Objetos {len(retry)}; únicos {retry["clave_objeto"].nunique()}; cobertura exacta {set(retry["clave_objeto"])==expected_keys}; sin HTTP dl=1 {retry["http_dl1"].isna().sum()}')
    check('Honorarios','Todos los objetos fueron solicitados con dl=1',retry['url_reintento'].fillna('').str.contains(r'(?:[?&])dl=1(?:&|$)',regex=True).all(),f'Variantes: {retry["variantes_utilizadas"].value_counts().to_dict()}')
    check('Honorarios','Sin errores de red o internos pendientes',not retry['estado'].isin(['error_red','error_interno']).any(),f'Estados residuales: {retry.loc[retry["estado"].isin(["error_red","error_interno"]),"estado"].value_counts().to_dict()}')
    deleted=retry[retry['estado']=='dropbox_file_deleted']
    check('Honorarios','File Deleted confirmado por Dropbox con dl=1',deleted['titulo_respuesta'].fillna('').str.contains('file deleted',case=False).all(),f'Objetos eliminados explícitos: {len(deleted)}')
    disabled=retry[retry['estado']=='dropbox_link_temporarily_disabled']
    check('Honorarios','Link Temporarily Disabled confirmado por Dropbox',disabled['titulo_respuesta'].fillna('').str.contains('link temporarily disabled',case=False).all(),f'Objetos deshabilitados explícitos: {len(disabled)}')
    check('Honorarios','Resumen del reintento coincide con su detalle',retry_stats['objetos_reintentados']==len(retry) and retry_stats['file_deleted']==len(deleted) and retry_stats['link_temporarily_disabled']==len(disabled) and retry_stats['recuperados']==int(retry['estado'].eq('descargado_recuperado').sum()),f'Recuperados: {retry_stats["recuperados"]}; File Deleted: {len(deleted)}; deshabilitados: {len(disabled)}; otros: {retry_stats["otros"]}')
    ok=man[man['estado']=='descargado']; bad=[]; checked_files=set()
    for _,r in ok.iterrows():
        rel=r['archivo_relativo']
        if not isinstance(rel,str) or not rel: bad.append(r['inventario_id']+':ruta'); continue
        p=ROOT/rel
        if not p.exists(): bad.append(r['inventario_id']+':ausente'); continue
        if rel in checked_files: continue
        checked_files.add(rel)
        with p.open('rb') as f: signature=b'%PDF-' in f.read(1024)
        if not signature or sha256(p)!=r['sha256'] or p.stat().st_size!=int(r['bytes']): bad.append(r['inventario_id']+':hash/pdf/bytes')
    check('Honorarios','Cada PDF declarado existe y coincide en firma, bytes y SHA-256',not bad,f'Archivos únicos verificados: {len(checked_files)}; fallos: {len(bad)}')
    partials=list((ROOT/'archivo externo'/'informes_funciones_honorarios').rglob('*.part'))
    check('Honorarios','Sin descargas parciales en el archivo documental',not partials,f'Archivos .part: {len(partials)}')
    failed=man[man['tiene_url']&(man['estado']!='descargado')]
    check('Honorarios','Fallos y registros sin URL documentados',len(man[man['estado']=='sin_url'])==3094,f'Sin URL: {sum(man["estado"]=="sin_url")}; fallidos con URL: {len(failed)}')
    check('Honorarios','Estados finales reconciliados con el reintento',len(failed)+len(ok)+int(man['estado'].eq('sin_url').sum())==len(man),f'Estados: {man["estado"].value_counts().to_dict()}')
    download_summary={'estados_registros':man['estado'].value_counts().to_dict(),'archivos_unicos_verificados':len(checked_files),'bytes_unicos':sum((ROOT/r['archivo_relativo']).stat().st_size for _,r in ok.drop_duplicates('archivo_relativo').iterrows()),'reintento_h010':retry_stats}
else:
    check('Honorarios','Manifiesto de descargas disponible',False,'No existe el manifiesto v2')

# Inventario de entregables (excluye intermedios y archivos de trabajo).
deliverables=[]
for base in [OUT,DOCS]:
    for p in sorted(base.rglob('*')):
        if p.is_file() and not p.stem.endswith('_recalc_verify'):
            deliverables.append({'tipo':base.name,'archivo':p.name,'ruta_relativa':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha256(p)})
controls_df=pd.DataFrame(controls); totals_df=pd.DataFrame(totals); deliverables_df=pd.DataFrame(deliverables)
write_xlsx(DOCS/'VALIDACION_FINAL_v1.xlsx',{'Controles':controls_df,'Totales canónicos':totals_df,'Descargas':pd.DataFrame([download_summary]),'Entregables':deliverables_df})
failed=controls_df[controls_df['resultado']=='FALLA']
md=['# Validación final — Personal y Remuneraciones','',f'**Controles ejecutados:** {len(controls_df)}  ',f'**Resultado:** {"APROBADO" if failed.empty else "CON FALLAS"}','',
    '## Totales independientes','',totals_df.to_markdown(index=False),'',
    '## Descargas','',f'```json\n{json.dumps(download_summary,ensure_ascii=False,indent=2)}\n```','',
    '## Controles no aprobados','', 'Ninguno.' if failed.empty else failed.to_markdown(index=False),'',
    'La hoja `Entregables` del libro Excel registra ruta, tamaño y SHA-256 de los productos finales. Los CSV y XLSX originales conservaron sus huellas iniciales.']
(DOCS/'VALIDACION_FINAL_v1.md').write_text('\n'.join(md),encoding='utf-8')
(TMP/'validacion_trazabilidad.json').write_text(json.dumps({'controles':len(controls_df),'fallas':len(failed),'totales':totals,'descargas':download_summary},ensure_ascii=False,indent=2),encoding='utf-8')
print(controls_df.to_string(index=False))
print('RESULTADO:', 'APROBADO' if failed.empty else f'{len(failed)} FALLAS')
if not failed.empty: raise SystemExit(1)
