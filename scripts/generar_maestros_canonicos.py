import hashlib, html, json, re
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
from utilidades_personal import *

PROCESSED_AT=datetime.now(ZoneInfo('America/Santiago')).isoformat(timespec='seconds')
LONG={
 'cargo':'Cargo o función','grado':'Grado EUS o jornada','calif':'Calificación profesional o formación','region':'Región',
 'inicio_planta':'Fecha de inicio dd/mm/aa','inicio_cod':'Fecha de inicio dd/mm/aaaa',
 'termino_planta':'Fecha de término dd/mm/aa','termino_cod':'Fecha de término dd/mm/aaaa','obs':'Observaciones',
 'asig':'Asignaciones especiales del mes (inc. en rem. bruta)',
 'bruta':'Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras)',
 'liquida':'Remuneración líquida del mes','adicional':'Rem. adicionales del mes (no inc. en rem. bruta)',
 'bonos':'Remuneración Bonos incentivos del mes (inc. en rem. bruta)',
 'desvinc':'Monto de desvinculación (no inc. en rem. bruta)','derecho':'Derecho a horas extraordinarias',
 'viaticos':'Viáticos del mes (no inc. en rem. bruta)',
 'he_generico':'Montos y horas extraordinarias del mes(inc. en rem. bruta)',
 'he_diurnas':'Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta)',
 'he_nocturnas':'Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta)',
 'he_festivas':'Montos y horas extraordinarias festivas del mes (inc. en rem. bruta)'}
CONFIG={
 'Planta':{'folder':'01_Personal_Planta','master':TMP/'planta_horas.pkl','id':'ID_Trabajador','name':'Nombre completo','clean':'nombre_limpio','first':'primer_nombre','gender':'genero','estamento':'Estamento','file':'_archivo_origen','prefix':'PLT','inicio':LONG['inicio_planta'],'termino':LONG['termino_planta'],
   'legacy':{'remuneracion_bruta_clp':LONG['bruta']+'_num','remuneracion_liquida_clp':'Remuneración líquida del mes_num','remuneracion_adicional_clp':LONG['adicional']+'_num','bonos_incentivos_clp':LONG['bonos']+'_num','viaticos_clp':LONG['viaticos']+'_num','horas_extra_diurnas_clp':LONG['he_diurnas']+'_num','horas_extra_nocturnas_clp':LONG['he_nocturnas']+'_num','horas_extra_festivas_clp':LONG['he_festivas']+'_num'}},
 'Contrata':{'folder':'02_Personal_Contrata','master':TMP/'contrata_horas.pkl','id':'ID_Trabajador','name':'Nombre_completo','clean':'nombre_limpio','first':'primer_nombre','gender':'genero','estamento':'Estamento','file':'_archivo_origen','prefix':'CON','inicio':LONG['inicio_planta'],'termino':LONG['termino_planta'],
   'legacy':{'remuneracion_bruta_clp':'Remuneración_bruta_num','remuneracion_liquida_clp':'Remuneración_líquida_num','remuneracion_adicional_clp':'Remuneración_adicional_num','bonos_incentivos_clp':'Bonos_incentivos_num','viaticos_clp':'Viáticos_num','horas_extra_diurnas_clp':'Horas_extra_diurnas_num','horas_extra_nocturnas_clp':'Horas_extra_nocturnas_num','horas_extra_festivas_clp':'Horas_extra_festivas_num'}},
 'Código del Trabajo':{'folder':'03_Personal_por_Código_del_Trabajo','master':TMP/'codigo_corregido.pkl','id':'ID_Trabajador','name':'Nombre completo','clean':'nombre_limpio','first':'primer_nombre','gender':'genero','estamento':'Estamento','file':'_archivo_origen','prefix':'COT','inicio':LONG['inicio_cod'],'termino':LONG['termino_cod'],
   'legacy':{'remuneracion_bruta_clp':'rem_bruta_mes_num','remuneracion_liquida_clp':'rem_liquida_mes_num','remuneracion_adicional_clp':'rem_adicionales_mes_num','bonos_incentivos_clp':'bonos_mes_num','monto_desvinculacion_clp':'desvinculacion_num','horas_extra_clp':'he_monto_num','horas_extra_horas':'he_horas_num','viaticos_clp':'viaticos_num'}},
 'Honorarios':{'folder':'04_Personal_Honorarios','master':RAW/'04_Personal_Honorarios'/'MAESTRO_Honorarios_Coronel_2023-2025.xlsx','id':'ID Trabajador','name':'Nombre Original','clean':'Nombre Limpio','first':'Primer Nombre','gender':'Género','estamento':None,'file':'Archivo Origen','prefix':'HON','inicio':'Fecha de inicio','termino':'Fecha de término',
   'legacy':{'remuneracion_bruta_clp':'Honorario Bruto ($)','remuneracion_liquida_clp':'Honorario Líquido ($)','viaticos_clp':'Viáticos ($)'}}
}

def load_master(cfg):
    if str(cfg['master']).endswith('.pkl'): return pd.read_pickle(cfg['master']).fillna('')
    return pd.read_excel(cfg['master'],sheet_name='Datos Completos',dtype=object).fillna('')

def iso_date_series(s):
    d=pd.to_datetime(s.map(norm),format='mixed',dayfirst=True,errors='coerce')
    return d.dt.strftime('%Y-%m-%d').fillna(''),d

def end_type(raw,dates):
    out=[]
    for value,date in zip(raw,dates):
        s=norm(value).casefold()
        if not pd.isna(date): out.append('fecha')
        elif not s: out.append('no_especificado')
        elif 'indefin' in s: out.append('indefinido')
        elif s in {'no informa','-','--'}: out.append('no_informa')
        else: out.append('otro')
    return out

def extract_url(x):
    m=re.search(r'https?://[^\s\'\"<>]+',html.unescape(norm(x)))
    return m.group(0) if m else ''

all_dictionary=[]; all_quality=[]; outputs={}; canonical_frames={}
for category,cfg in CONFIG.items():
    raw=load_raw_category(cfg['folder'])
    m=load_master(cfg)
    raw['nombre_clave']=raw['Nombre completo'].map(keyname)
    m['nombre_clave']=m[cfg['name']].map(keyname)
    raw['archivo_clave']=raw['fuente_archivo'].map(norm)
    m['archivo_clave']=m[cfg['file']].map(norm)
    for df in (raw,m):
        df['clave']=df['archivo_clave']+'|'+df['nombre_clave']
        df['ocurrencia']=df.groupby('clave').cumcount()
    j=m.merge(raw,on=['clave','ocurrencia'],how='left',suffixes=('_maestro','_csv'),indicator=True,validate='one_to_one')
    unmatched=int((j['_merge']!='both').sum())
    assert unmatched==0, f'{category}: {unmatched} filas sin fuente'
    assert len(j)==len(m)==len(raw)
    def mc(c): return c+'_maestro' if c+'_maestro' in j.columns else c
    def rc(c): return c+'_csv' if c+'_csv' in j.columns else c
    out=pd.DataFrame(index=j.index); dictionary=[]
    def put(col,values,tipo,descripcion,valores,origen,regla,maestro='',crudo=''):
        out[col]=list(values) if not isinstance(values,pd.Series) else values.values
        dictionary.append({'maestro':category,'columna_canonica':col,'tipo':tipo,'descripcion':descripcion,
                           'valores_posibles':valores,'origen':origen,'regla_transformacion':regla,
                           'columna_maestro_original':maestro,'columna_csv_crudo':crudo})
    put('categoria',pd.Series(category,index=j.index),'texto','Estamento o categoría de transparencia','Planta | Contrata | Código del Trabajo | Honorarios','derivado','Constante asignada por categoría')
    ids=[]
    for pos,(_,r) in enumerate(j.iterrows()):
        ruta=norm(j[rc('fuente_ruta_relativa')].iloc[pos]); fila=j[rc('fuente_fila_csv')].iloc[pos]
        digest=hashlib.sha1((ruta+'#'+str(fila)).encode('utf-8')).hexdigest()[:10].upper()
        ids.append(f"{cfg['prefix']}-{int(r['Año_csv'] if 'Año_csv' in j.columns else r['Año'])}{MESES[norm(r['Mes_csv'] if 'Mes_csv' in j.columns else r['Mes'])]:02d}-{digest}")
    put('registro_id',ids,'texto','Identificador único y estable del registro mensual','Un valor único por archivo y fila','derivado','Categoría + período + SHA-1 abreviado de ruta relativa y fila CSV')
    put('id_trabajador',j[mc(cfg['id'])].map(norm),'texto','Identificador de trabajador del maestro manual','Valor heredado; no implica unicidad global validada','derivado','Conservado sin regenerar',cfg['id'])
    years=pd.to_numeric(j[rc('Año')],errors='raise').astype(int)
    months=j[rc('Mes')].map(lambda x:MESES[norm(x)]).astype(int)
    put('anio',years,'entero','Año declarado en el contenido del CSV','2023 | 2024 | 2025','crudo','Conversión a entero; no se obtiene del nombre de archivo',crudo='Año')
    put('mes_numero',months,'entero','Número de mes declarado en el contenido del CSV','1-12','derivado','Catálogo de nombres de mes en español',crudo='Mes')
    put('mes_nombre',months.map(MES_NOMBRE),'texto','Nombre canónico del mes','Enero-Diciembre','derivado','Catálogo controlado a partir de Mes',crudo='Mes')
    put('periodo',years.astype(str)+'-'+months.astype(str).str.zfill(2),'texto (AAAA-MM)','Período mensual de la observación','AAAA-MM','derivado','Concatenación de anio y mes_numero')
    put('nombre_original',j[rc('Nombre completo')].map(norm),'texto','Nombre tal como aparece en el CSV','Texto libre','crudo','Normalización Unicode y espacios; sin cambiar identidad',crudo='Nombre completo')
    put('nombre_normalizado',j[mc(cfg['clean'])].map(norm),'texto','Nombre depurado en el maestro manual','Texto libre','derivado','Conservado del maestro; no se recalcula',cfg['clean'])
    put('primer_nombre',j[mc(cfg['first'])].map(norm),'texto','Primer nombre usado para revisión manual','Texto libre','derivado','Conservado del maestro',cfg['first'])
    put('genero',j[mc(cfg['gender'])].map(norm),'texto','Género registrado en el maestro tras inferencia y revisión manual',' | '.join(sorted(set(j[mc(cfg['gender'])].map(norm)))),'derivado','Conservado; no se vuelve a inferir por nombre',cfg['gender'])
    est=j[mc(cfg['estamento'])].map(norm) if cfg['estamento'] else pd.Series('Honorarios',index=j.index)
    put('estamento',est,'texto','Estamento o categoría funcional','Texto controlado según valores observados','derivado' if category=='Código del Trabajo' or not cfg['estamento'] else 'crudo','Conservado del maestro manual; no existe en el CSV' if category=='Código del Trabajo' else ('Conservado del maestro/CSV' if cfg['estamento'] else 'Constante Honorarios'),cfg['estamento'] or '',LONG.get('estamento',''))
    raw_special=category=='Honorarios'
    cargo='Descripción de la función' if raw_special else LONG['cargo']
    grado='Grado EUS  (si corresponde)' if raw_special else LONG['grado']
    calif=LONG['calif']; region=LONG['region']
    put('cargo_funcion',j[rc(cargo)].map(norm),'texto','Cargo o descripción de la función','Texto libre','crudo','Normalización Unicode y espacios',crudo=cargo)
    put('grado_eus_jornada',j[rc(grado)].map(norm),'texto','Grado EUS o jornada informado','Texto libre; incluye No Asimilado a Grado','crudo','Texto conservado',crudo=grado)
    put('calificacion_profesional',j[rc(calif)].map(norm),'texto','Calificación profesional o formación','Texto libre','crudo','Normalización Unicode y espacios',crudo=calif)
    put('region',j[rc(region)].map(norm),'texto','Región de desempeño','Texto libre; predominantemente Región del Biobío','crudo','Texto conservado',crudo=region)
    inicio_raw=j[rc(cfg['inicio'])].map(norm); inicio_iso,inicio_dates=iso_date_series(inicio_raw)
    termino_raw=j[rc(cfg['termino'])].map(norm); termino_iso,termino_dates=iso_date_series(termino_raw)
    put('fecha_inicio_raw',inicio_raw,'texto','Fecha de inicio tal como fue publicada','Texto libre','crudo','Conservada para auditoría',crudo=cfg['inicio'])
    put('fecha_inicio',inicio_iso,'fecha ISO 8601 (texto)','Fecha de inicio normalizada','AAAA-MM-DD o vacío si no es parseable','derivado','Interpretación día/mes/año; valor original preservado',crudo=cfg['inicio'])
    put('fecha_termino_raw',termino_raw,'texto','Fecha de término o condición contractual publicada','Texto libre; incluye Indefinido','crudo','Conservada para auditoría',crudo=cfg['termino'])
    put('fecha_termino',termino_iso,'fecha ISO 8601 (texto)','Fecha de término normalizada','AAAA-MM-DD o vacío si no es una fecha','derivado','Interpretación día/mes/año; Indefinido queda vacío',crudo=cfg['termino'])
    put('fecha_termino_tipo',end_type(termino_raw,termino_dates),'texto','Clasificación del valor de término','fecha | indefinido | no_informa | no_especificado | otro','derivado','Clasificación de fecha_termino_raw y su parseo')
    put('observaciones',j[rc(LONG['obs'])].map(norm),'texto','Observaciones publicadas','Texto libre','crudo','Normalización Unicode y espacios',crudo=LONG['obs'])
    quality=[]
    if not raw_special:
        put('asignaciones_especiales_raw',j[rc(LONG['asig'])].map(norm),'texto','Códigos de asignaciones especiales incluidos en bruto','Texto con códigos entre paréntesis','crudo','Texto conservado',crudo=LONG['asig'])
    money_fields=[('remuneracion_bruta','Honorario Total Bruto del mes' if raw_special else LONG['bruta']),
                  ('remuneracion_liquida','Honorario Total Líquido del mes' if raw_special else LONG['liquida']),
                  ('viaticos','Viáticos' if raw_special else LONG['viaticos'])]
    if not raw_special:
        money_fields += [('remuneracion_adicional',LONG['adicional']),('bonos_incentivos',LONG['bonos'])]
    if category=='Código del Trabajo': money_fields += [('monto_desvinculacion',LONG['desvinc'])]
    for base,rawcol in money_fields:
        rawvalues=j[rc(rawcol)].map(norm); values=rawvalues.map(money)
        put(base+'_raw',rawvalues,'texto',f'Valor publicado de {base.replace("_"," ")}','Texto libre con formato monetario o No informa/No tiene','crudo','Texto conservado',crudo=rawcol)
        put(base+'_clp',values.astype('int64'),'entero (CLP)',f'{base.replace("_"," ").capitalize()} en pesos chilenos','Entero ≥ 0; 0 si fuente no informa/no tiene','derivado','Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos',crudo=rawcol)
        legacy=cfg['legacy'].get(base+'_clp')
        if legacy:
            actual=pd.to_numeric(j[mc(legacy)],errors='coerce')
            diff=(actual.isna())|(actual!=values)
            quality.append({'maestro':category,'control':'Importe numérico heredado vs CSV','columna':base+'_clp','filas':len(j),'diferencias':int(diff.sum()),'columna_maestro':legacy,'columna_csv':rawcol})
    if not raw_special:
        put('derecho_horas_extra',j[rc(LONG['derecho'])].map(norm),'texto','Derecho a horas extraordinarias declarado','Sí | No | otros valores publicados','crudo','Texto conservado',crudo=LONG['derecho'])
    hour_kinds=['diurnas','nocturnas','festivas'] if category in ('Planta','Contrata') else (['generico'] if category=='Código del Trabajo' else [])
    for kind in hour_kinds:
        rawcol=LONG['he_generico' if kind=='generico' else 'he_'+kind]
        prefix='horas_extra' if kind=='generico' else 'horas_extra_'+kind
        rawvalues=j[rc(rawcol)].map(norm); amounts=rawvalues.map(money); hrs=rawvalues.map(hours)
        put(prefix+'_raw',rawvalues,'texto',f'Monto y horas extra {kind} publicados','Texto “monto : horas hrs”, No tiene o No informa','crudo','Texto conservado',crudo=rawcol)
        put(prefix+'_clp',amounts.astype('int64'),'entero (CLP)',f'Monto de horas extra {kind} en pesos','Entero ≥ 0','derivado','Parseo de segmento anterior a “:”',crudo=rawcol)
        put(prefix+'_horas',hrs.astype(float),'decimal (horas)',f'Cantidad de horas extra {kind}','Decimal ≥ 0; 0 si no publica horas','derivado','Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto',crudo=rawcol)
        for suffix,values in (('_clp',amounts),('_horas',hrs)):
            legacy=cfg['legacy'].get(prefix+suffix)
            if legacy:
                actual=pd.to_numeric(j[mc(legacy)],errors='coerce')
                diff=(actual.isna())|(actual!=values)
                quality.append({'maestro':category,'control':'Horas/monto heredado vs CSV','columna':prefix+suffix,'filas':len(j),'diferencias':int(diff.sum()),'columna_maestro':legacy,'columna_csv':rawcol})
        if kind=='generico':
            put('horas_extra_desagregacion',pd.Series('sin_desagregacion',index=j.index),'texto','Nivel de desagregación de horas extra','sin_desagregacion','derivado','La fuente no distingue diurnas, nocturnas o festivas')
    if raw_special:
        for canonical,rawcol,desc in [('tipo_pago','Tipo de pago','Tipo de pago'),('descripcion_pago','Descripción pago','Descripción del pago')]:
            put(canonical,j[rc(rawcol)].map(norm),'texto',desc,'Texto libre','crudo','Texto conservado',crudo=rawcol)
        cuotas_raw=j[rc('Número de cuotas')].map(norm)
        put('numero_cuotas_raw',cuotas_raw,'texto','Número de cuotas publicado','Texto numérico o “-”','crudo','Texto conservado',crudo='Número de cuotas')
        cuotas=pd.to_numeric(cuotas_raw.replace({'-':'','':''}),errors='coerce').astype('Int64')
        put('numero_cuotas',cuotas,'entero nullable','Número de cuotas','Entero ≥ 0 o vacío si no aplica/no informa','derivado','Conversión numérica; “-” queda vacío',crudo='Número de cuotas')
        links=j[rc('Enlace funciones desarrolladas')].map(norm)
        put('enlace_funciones_desarrolladas_raw',links,'texto','HTML del enlace al informe de funciones','HTML o vacío','crudo','Texto conservado',crudo='Enlace funciones desarrolladas')
        put('enlace_funciones_desarrolladas_url',links.map(extract_url),'texto (URL)','URL extraída del informe de funciones','URL HTTP/HTTPS o vacío','derivado','Extraer primer URL del HTML y decodificar entidades HTML',crudo='Enlace funciones desarrolladas')
    # Trazabilidad completa al archivo físico intocable.
    for col,tipo,desc,rule in [('fuente_archivo','texto','Nombre del CSV de origen','Nombre físico conservado'),('fuente_ruta_relativa','texto','Ruta relativa del CSV desde la raíz del proyecto','Ruta relativa conservada'),('fuente_fila_csv','entero','Número de fila en el CSV, contando encabezado como fila 1','Índice original + 2'),('fuente_sha256','texto (SHA-256)','Huella digital del CSV fuente','SHA-256 de bytes originales'),('fuente_encoding','texto','Codificación detectada del CSV','Decodificación probada en orden UTF-8-SIG, CP1252, Latin-1'),('fuente_separador','texto','Delimitador detectado del CSV','Detección con csv.Sniffer')]:
        values=j[rc(col)].astype(int) if col=='fuente_fila_csv' else j[rc(col)].map(norm)
        possible='64 caracteres hexadecimales' if col=='fuente_sha256' else ('Entero ≥ 2' if col=='fuente_fila_csv' else 'Valor observado en archivos fuente')
        put(col,values,tipo,desc,possible,'crudo' if col=='fuente_archivo' else 'derivado',rule,crudo=col)
    put('version_esquema',pd.Series('canonico_v1.0.0',index=j.index),'texto','Versión del esquema canónico','canonico_v1.0.0','derivado','Constante de versión')
    put('fecha_procesamiento',pd.Series(PROCESSED_AT,index=j.index),'fecha-hora ISO 8601','Marca temporal del procesamiento','ISO 8601 con zona America/Santiago','derivado','Marca de ejecución del proceso')
    # Controles de fechas e identificadores.
    quality += [
      {'maestro':category,'control':'Vinculación CSV','columna':'fuente_archivo','filas':len(j),'diferencias':unmatched,'columna_maestro':cfg['file'],'columna_csv':'archivo+fila'},
      {'maestro':category,'control':'Fechas de inicio no vacías no parseadas','columna':'fecha_inicio','filas':len(j),'diferencias':int(((inicio_raw!='')&inicio_dates.isna()).sum()),'columna_maestro':'','columna_csv':cfg['inicio']},
      {'maestro':category,'control':'Valores de término no clasificados como fecha/indefinido/no informa/vacío','columna':'fecha_termino_tipo','filas':len(j),'diferencias':int((pd.Series(end_type(termino_raw,termino_dates))=='otro').sum()),'columna_maestro':'','columna_csv':cfg['termino']}]
    qdf=pd.DataFrame(quality)
    all_quality.extend(quality); all_dictionary.extend(dictionary); canonical_frames[category]=out
    control=pd.DataFrame([
      {'indicador':'Filas maestro original / CSV / canónico','valor':f'{len(m)} / {len(raw)} / {len(out)}'},
      {'indicador':'Columnas canónicas','valor':len(out.columns)},
      {'indicador':'Registros sin CSV fuente','valor':unmatched},
      {'indicador':'Diferencias en importes/horas heredados','valor':int(qdf[qdf['control'].str.contains('heredado')]['diferencias'].sum())},
      {'indicador':'IDs de registro duplicados','valor':int(out['registro_id'].duplicated().sum())},
      {'indicador':'Esquema','valor':'canonico_v1.0.0'},
      {'indicador':'Procesado','valor':PROCESSED_AT},
      {'indicador':'Original modificado','valor':'No'}])
    mapping=pd.DataFrame(dictionary)
    filename='MAESTRO_'+('CODTrabajo' if category=='Código del Trabajo' else category)+'_Coronel_2023-2025_canonico_v1.xlsx'
    outfile=OUT/filename
    write_xlsx(outfile,{'Datos':out,'Control':control,'Mapeo columnas':mapping})
    outputs[category]={'archivo':str(outfile.relative_to(ROOT)),'filas':len(out),'columnas':len(out.columns),'sha256':sha256(outfile),'controles':quality}
    print(category,':',len(out),'filas,',len(out.columns),'columnas; diferencias numéricas',int(qdf[qdf['control'].str.contains('heredado')]['diferencias'].sum()))

# Un registro por maestro y columna satisface el diccionario completo y el mapeo columna a columna.
dictdf=pd.DataFrame(all_dictionary)
qualitydf=pd.DataFrame(all_quality)
write_xlsx(DOCS/'MAPEO_ESQUEMA_CANONICO_v1.xlsx',{'Mapeo completo':dictdf,'Controles':qualitydf})
(TMP/'diccionario_canonico_base.pkl').write_bytes(b'')
dictdf.to_pickle(TMP/'diccionario_canonico.pkl'); qualitydf.to_pickle(TMP/'controles_canonicos.pkl')
for cat,df in canonical_frames.items(): df.to_pickle(TMP/('canonico_'+re.sub(r'\W+','_',cat.casefold())+'.pkl'))
(TMP/'maestros_canonicos_resumen.json').write_text(json.dumps(outputs,ensure_ascii=False,indent=2),encoding='utf-8')
print('\nDiccionario:',len(dictdf),'filas. Controles:',len(qualitydf))
