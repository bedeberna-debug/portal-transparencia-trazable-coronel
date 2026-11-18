import json, re
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from utilidades_personal import *

NOW=datetime.now(ZoneInfo('America/Santiago'))
DATE=NOW.date().isoformat()
DOCS.mkdir(parents=True,exist_ok=True)
dictdf=pd.read_pickle(TMP/'diccionario_canonico.pkl')
quality=pd.read_pickle(TMP/'controles_canonicos.pkl')
cod=json.loads((TMP/'codigo_correccion_resumen.json').read_text(encoding='utf-8'))
hours=json.loads((TMP/'horas_recuperacion_resumen.json').read_text(encoding='utf-8'))
canon=json.loads((TMP/'maestros_canonicos_resumen.json').read_text(encoding='utf-8'))

# Diccionario de datos: una fila por maestro y columna, con mapeo y regla.
cat_order=['Planta','Contrata','Código del Trabajo','Honorarios']
dictdf['maestro']=pd.Categorical(dictdf['maestro'],cat_order,ordered=True)
dictdf=dictdf.sort_values(['maestro'],kind='stable')
dictdf['maestro']=dictdf['maestro'].astype(str)
catalogs=[]
filekeys={'Planta':'planta','Contrata':'contrata','Código del Trabajo':'código_del_trabajo','Honorarios':'honorarios'}
for cat in cat_order:
    d=pd.read_pickle(TMP/f'canonico_{filekeys[cat]}.pkl')
    for col in ['genero','estamento','mes_nombre','fecha_termino_tipo','derecho_horas_extra','tipo_pago','horas_extra_desagregacion']:
        if col in d:
            for value,n in d[col].fillna('(vacío)').replace('','(vacío)').value_counts().items():
                catalogs.append({'maestro':cat,'columna':col,'valor_observado':value,'registros':int(n)})
sheets={'Diccionario completo':dictdf,'Controles':quality,'Catálogos observados':pd.DataFrame(catalogs)}
for cat,sheet in zip(cat_order,['Planta','Contrata','COD Trabajo','Honorarios']):
    sheets[sheet]=dictdf[dictdf['maestro']==cat].copy()
write_xlsx(DOCS/'DICCIONARIO_DATOS_v1.xlsx',sheets)

def esc(x): return str(x).replace('|','\\|').replace('\n',' ')
md=['# Diccionario de datos — Personal y Remuneraciones','',
    '**Versión:** canonico_v1.0.0  ','**Fecha de generación:** '+DATE,'',
    'Cada tabla enumera todas las columnas del maestro canónico. `crudo` significa que el valor proviene del CSV; `derivado` indica una transformación o un campo conservado del maestro manual. Los importes `_clp` son pesos chilenos y las fechas ISO se acompañan siempre de su campo `_raw`.','']
for cat in cat_order:
    md += [f'## {cat}','', '| Columna | Tipo | Descripción | Valores posibles | Origen | Regla de transformación | Maestro original | CSV crudo |',
           '|---|---|---|---|---|---|---|---|']
    for _,r in dictdf[dictdf['maestro']==cat].iterrows():
        md.append('| '+' | '.join(esc(r[c]) for c in ['columna_canonica','tipo','descripcion','valores_posibles','origen','regla_transformacion','columna_maestro_original','columna_csv_crudo'])+' |')
    md.append('')
md += ['## Trazabilidad común','',
       'Todos los maestros incluyen `fuente_archivo`, `fuente_ruta_relativa`, `fuente_fila_csv` y `fuente_sha256`. La fila CSV considera el encabezado como fila 1. `registro_id` se deriva de categoría, período y una huella de ruta + fila; `id_trabajador` se conserva del maestro manual y no se reinterpreta como identificador global.',
       '', 'Los catálogos de valores efectivamente observados están en la hoja `Catálogos observados` del archivo Excel.']
(DOCS/'DICCIONARIO_DATOS_v1.md').write_text('\n'.join(md),encoding='utf-8')

# Inventario inmutable de fuentes y maestros manuales.
source_rows=[]
for p in sorted(RAW.rglob('*.csv')):
    d,enc,sep=read_csv_robust(p)
    unnamed=[c for c in d if c.startswith('Unnamed:')]
    source_rows.append({'categoria':p.parent.parent.name,'archivo':p.name,'ruta_relativa':str(p.relative_to(ROOT)),
                        'filas':len(d),'columnas':len(d.columns),'encoding':enc,'separador':sep,
                        'columnas_unnamed':len(unnamed),'celdas_unnamed_no_vacias':sum(int((d[c].map(norm)!='').sum()) for c in unnamed),
                        'anios_contenido':'|'.join(sorted(set(d['Año'].map(norm)))) if 'Año' in d else '',
                        'meses_contenido':'|'.join(sorted(set(d['Mes'].map(norm)))) if 'Mes' in d else '',
                        'sha256':sha256(p)})
sources=pd.DataFrame(source_rows)
master_rows=[]
for p in sorted(RAW.rglob('MAESTRO_*.xlsx')):
    xf=pd.ExcelFile(p)
    master_rows.append({'archivo':p.name,'ruta_relativa':str(p.relative_to(ROOT)),'sha256':sha256(p),
                        'hojas':'|'.join(xf.sheet_names),'filas_datos_completos':len(pd.read_excel(p,sheet_name='Datos Completos'))})
masters=pd.DataFrame(master_rows)
write_xlsx(DOCS/'INVENTARIO_FUENTES_v1.xlsx',{'CSV fuente':sources,'Maestros originales':masters})

# Hallazgos estructurados. Los resultados de descarga se agregan al rerutear este script con su manifiesto.
findings=[
 {'id':'H-001','categoria':'Autoridades','tipo':'Cobertura','severidad':'Alta','estado':'Pendiente verificación externa','titulo':'Sin publicación 2023 en el portal oficial','evidencia':'No existe directorio 2023 en datos crudos/05_Autoridades_de_Eleccion_Popular; solo hay 2024 y 2025.','impacto':'Serie 2023-2025 incompleta para autoridades.','decision_accion':'Verificar disponibilidad histórica en Wayback Machine; no reconstruir ni imputar registros.','pendiente':'Revisión Wayback Machine y eventual captura con fecha/URL de archivo.'},
 {'id':'H-002','categoria':'Código del Trabajo','tipo':'Nombre de archivo','severidad':'Baja','estado':'Resuelto por contenido','titulo':'Prefijo 03 duplicado en 2025 y ausencia de prefijo 04','evidencia':'03_CODTrabajo_Marzo_2025.csv y 03_CODTrabajo_Abril_2025.csv; el segundo contiene 27 filas, todas Mes=Abril.','impacto':'Riesgo de asignar abril a marzo si se usa el prefijo.','decision_accion':'Usar Año/Mes del contenido y conservar nombre físico como fuente.','pendiente':'No renombrar el original; opcionalmente solicitar corrección al publicador.'},
 {'id':'H-003','categoria':'Código del Trabajo','tipo':'Nombre de archivo','severidad':'Baja','estado':'Resuelto por contenido','titulo':'Archivo de noviembre de 2024 con nombre contradictorio','evidencia':'2024/10_CODTrabajo_Enero_2024 Noviembre.csv contiene 23 filas, todas Mes=Noviembre.','impacto':'Riesgo de clasificación errónea como enero u octubre.','decision_accion':'Asignar 2024-11 por contenido y mantener trazabilidad al archivo real.','pendiente':'No renombrar el original.'},
 {'id':'H-004','categoria':'Código del Trabajo','tipo':'Maestro incompleto','severidad':'Alta','estado':'Corregido en v2 y canónico','titulo':'Campos crudos y origen vacíos en los tres años','evidencia':'Las 15 columnas textuales crudas estaban vacías en 933/933 filas; _archivo_origen también estaba vacío en 933/933, incluido 2023.','impacto':'Pérdida de contexto publicado y de trazabilidad directa en el maestro manual.','decision_accion':'Restaurar 14.928 celdas (incluido origen) desde CSV; conservar ID, nombre depurado, género, estamento y numéricos. Control numérico: 0 diferencias.','pendiente':'Ninguno para la restauración; el original permanece intacto.'},
 {'id':'H-005','categoria':'Código del Trabajo','tipo':'Período en contenido','severidad':'Media','estado':'Documentado y trazado','titulo':'Una fila de mayo de 2025 está en el CSV de julio','evidencia':'07_CODTrabajo_Julio_2025.csv, fila CSV 29: FERNANDEZ CIFUENTES, GAIL MIRASLAVA BERNARDA, Año=2025, Mes=Mayo. La fila de mayo en 05_CODTrabajo_Mayo_2025.csv, fila 9, tiene igual bruto pero líquido distinto ($1.394.922 vs $1.394.849).','impacto':'Dos registros para la misma persona y período; no son duplicados exactos.','decision_accion':'Conservar ambos, con período 2025-05 y archivos/filas distintos; no deduplicar sin respaldo.','pendiente':'Solicitar aclaración al publicador si se requiere una única cifra oficial para ese mes.'},
 {'id':'H-006','categoria':'Planta','tipo':'Período en contenido','severidad':'Media','estado':'Documentado y trazado','titulo':'Una fila de noviembre de 2024 está en el CSV de diciembre','evidencia':'12_Planta_Diciembre_2024.csv, fila CSV 132: CARO PARRA, CARMEN SALOME, Mes=Noviembre. También existe registro en 11_Planta_Noviembre_2024.csv, fila 25; brutos y líquidos difieren.','impacto':'Dos registros para la misma persona y período; no son duplicados exactos.','decision_accion':'Conservar ambos con período 2024-11 y trazabilidad separada; no deduplicar.','pendiente':'Solicitar aclaración al publicador si se requiere una única cifra oficial para ese mes.'},
 {'id':'H-007','categoria':'Planta','tipo':'Resumen heredado','severidad':'Alta','estado':'Excluido de salidas nuevas','titulo':'Resumen Trabajadores contiene repeticiones masivas de ID','evidencia':'La hoja Resumen Trabajadores tiene 757 filas pero solo 178 ID_Trabajador únicos; 579 filas repiten un ID. Datos Completos tiene 178 IDs y 178 nombres normalizados únicos.','impacto':'Los agregados de esa hoja no son una tabla única confiable por trabajador.','decision_accion':'No copiar hojas analíticas heredadas a v2/canónico; recalcular desde Datos cuando se necesiten.','pendiente':'Reconstruir resumen solo bajo una regla explícita de unicidad.'},
 {'id':'H-008','categoria':'Autoridades','tipo':'Período faltante en contenido','severidad':'Media','estado':'Pendiente aclaración','titulo':'Diciembre de 2025 tiene Año y Mes sin informar','evidencia':'12_ElectosyOtros_Diciembre_2025.csv contiene 8 registros con Año=- y Mes=-; renta bruta publicada como UTM 15,60.','impacto':'El período solo puede inferirse del nombre/ruta, no del contenido; la renta bruta está expresada en UTM.','decision_accion':'No incorporar a los cuatro maestros canónicos ni imputar Año/Mes; conservar evidencia.','pendiente':'Confirmar período y conversión UTM aplicable antes de integrar autoridades.'},
 {'id':'H-009','categoria':'Todas','tipo':'Estructura CSV','severidad':'Informativa','estado':'Verificado','titulo':'Columnas Unnamed vacías','evidencia':'Se detectaron 166 columnas Unnamed en los CSV y 0 celdas no vacías en ellas.','impacto':'Separadores finales generan columnas auxiliares sin información.','decision_accion':'Excluirlas tras verificar que están completamente vacías.','pendiente':'Repetir esta verificación en cada nueva categoría/lote.'},
]
for f in findings: f['fecha_registro']=DATE
# Hallazgos de disponibilidad con verificación directa y reintento explícito.
manifest_path=OUT/'informes_honorarios'/'MANIFIESTO_DESCARGAS_v2.xlsx'
if manifest_path.exists():
    man=pd.read_excel(manifest_path,sheet_name='Manifiesto')
    retry=json.loads((TMP/'reintentos_h010_resumen.json').read_text(encoding='utf-8'))
    ok=int(man['estado'].eq('descargado').sum()); no_url=int(man['estado'].eq('sin_url').sum())
    failed=int((man['tiene_url']&man['estado'].ne('descargado')).sum())
    pdf_objects=man.loc[man['estado'].eq('descargado'),'archivo_relativo'].nunique()
    no_url_2023=int((man['estado'].eq('sin_url')&man['anio'].eq(2023)).sum())
    failed_states=man.loc[man['tiene_url']&man['estado'].ne('descargado'),'estado'].value_counts().to_dict()
    h010_title='Informes eliminados en Dropbox y ausencia histórica de enlaces' if retry['file_deleted'] else 'Disponibilidad de informes de funciones tras reintento directo'
    findings.append({'id':'H-010','fecha_registro':DATE,'categoria':'Honorarios','tipo':'Disponibilidad de enlaces','severidad':'Alta' if failed or no_url else 'Informativa','estado':'Verificado con reintento directo','titulo':h010_title,'evidencia':f'{len(man)} relaciones trabajador-mes-URL procesadas: {ok} registros tienen PDF confirmado ({pdf_objects} archivos únicos). La descarga v1 ya reescribía dl=0 a dl=1. Una prueba controlada sobre tres URL recuperadas mostró que la misma dirección con dl=1 puede alternar PDF y HTML con ambos agentes de usuario; por tanto, el artefacto se vincula a respuestas variables de Dropbox y no al parámetro dl=0 ni a un cliente específico. En v2 se reintentaron {retry["objetos_reintentados"]:,} objetos con dl=1: {retry["recuperados"]:,} PDF recuperados, {retry["file_deleted"]:,} con respuesta explícita File Deleted, {retry["link_temporarily_disabled"]:,} con Link Temporarily Disabled y {sum(retry["otros"].values()):,} con otros estados. El reintento redujo en {5166-failed:,} los registros inicialmente clasificados como no recuperables. Quedan {failed} registros con URL sin PDF ({failed_states}) y {no_url} registros sin URL: {no_url_2023} de 2023 y {no_url-no_url_2023} de 2024-2025. Evidencia en REINTENTOS_DROPBOX_H010_v1.xlsx y MANIFIESTO_DESCARGAS_v2.xlsx.','impacto':'La eliminación explícita de un archivo, otros errores de descarga y la ausencia de URL son condiciones distintas. No toda respuesta HTML HTTP 200 equivale a un archivo eliminado: la clasificación File Deleted se basa en el título explícito devuelto por Dropbox tras solicitar dl=1; las deshabilitaciones temporales y otros estados se mantienen separados.','decision_accion':'Conservar URL original, URL efectiva, variantes, códigos HTTP, títulos, fechas y SHA-256. Incorporar únicamente respuestas con firma PDF válida; mantener v1 como antecedente y v2 como manifiesto vigente.','pendiente':'Solicitar reposición o rehabilitación de los documentos eliminados o temporalmente deshabilitados y gestionar la ausencia histórica de enlaces de 2023. Revisar por separado cualquier otro estado residual.'})
findings=pd.DataFrame(findings)
# Detalle de anomalías por contenido/nombre y duplicados de período.
file_anomalies=[]
for folder in ['01_Personal_Planta','02_Personal_Contrata','03_Personal_por_Código_del_Trabajo','04_Personal_Honorarios','05_Autoridades_de_Eleccion_Popular']:
    r=load_raw_category(folder)
    for file,g in r.groupby('fuente_archivo'):
        expected=next((n for n in MESES if n.casefold() in file.casefold()),None)
        actual=sorted(set(g['Mes']),key=lambda x:MESES.get(x,99))
        if expected and (len(actual)>1 or actual[0]!=expected):
            file_anomalies.append({'categoria':folder,'archivo':file,'mes_esperado_nombre':expected,'meses_contenido':'|'.join(actual),'filas':len(g),'ruta':g['fuente_ruta_relativa'].iloc[0]})
duplicates=[]
for cat,key in filekeys.items():
    d=pd.read_pickle(TMP/f'canonico_{key}.pkl')
    x=d[d.duplicated(['periodo','nombre_normalizado'],keep=False)]
    for _,r in x.iterrows():
        duplicates.append({'maestro':cat,'periodo':r['periodo'],'nombre':r['nombre_normalizado'],'registro_id':r['registro_id'],'bruto_clp':r['remuneracion_bruta_clp'],'liquido_clp':r['remuneracion_liquida_clp'],'archivo':r['fuente_archivo'],'fila_csv':r['fuente_fila_csv']})
write_xlsx(DOCS/'REGISTRO_HALLAZGOS_v1.xlsx',{'Hallazgos':findings,'Anomalías archivos':pd.DataFrame(file_anomalies),'Duplicados período-nombre':pd.DataFrame(duplicates),'Controles canónicos':quality})

md=['# Registro de hallazgos — Personal y Remuneraciones','',f'**Fecha de corte:** {DATE}','',
    'Los estados “resuelto” se refieren al saneamiento en archivos nuevos; ningún CSV o maestro original fue modificado.','']
for _,r in findings.iterrows():
    md += [f"## {r['id']} — {r['titulo']}",'',f"- **Categoría:** {r['categoria']}",f"- **Tipo / severidad:** {r['tipo']} / {r['severidad']}",f"- **Estado:** {r['estado']}",f"- **Evidencia:** {r['evidencia']}",f"- **Impacto:** {r['impacto']}",f"- **Decisión / acción:** {r['decision_accion']}",f"- **Pendiente:** {r['pendiente']}",'']
md += ['## Duplicados período–nombre conservados','',
       'Las dos situaciones de Código del Trabajo y Planta descritas en H-005 y H-006 permanecen porque difieren en valores y/o archivo fuente. La hoja `Duplicados período-nombre` del registro Excel contiene los identificadores y cifras.']
(DOCS/'REGISTRO_HALLAZGOS_v1.md').write_text('\n'.join(md),encoding='utf-8')

# Bitácora replicable del proceso.
source_counts=sources.groupby('categoria').size().to_dict()
rows={cat:canon[cat]['filas'] for cat in cat_order}
hpl={x['tipo']:x for x in hours['Planta']['estadisticas']}; hco={x['tipo']:x for x in hours['Contrata']['estadisticas']}
bit=f'''# Bitácora de transformaciones — Personal y Remuneraciones

**Proyecto:** Portal de Transparencia Trazable – Municipalidad de Coronel  
**Versión del esquema:** canonico_v1.0.0  
**Fecha de corte:** {DATE}  
**Criterio rector:** trazabilidad total y fuentes originales intocables.

## 1. Alcance y fuentes

Se inspeccionaron **{len(sources)} CSV** y **4 maestros XLSX manuales**. Por categoría: Planta {source_counts.get('01_Personal_Planta',0)} CSV, Contrata {source_counts.get('02_Personal_Contrata',0)}, Código del Trabajo {source_counts.get('03_Personal_por_Código_del_Trabajo',0)}, Honorarios {source_counts.get('04_Personal_Honorarios',0)} y Autoridades {source_counts.get('05_Autoridades_de_Eleccion_Popular',0)}. Autoridades no tiene 2023; queda pendiente Wayback Machine (H-001).

Los archivos de `datos crudos` se abrieron en modo lectura. `INVENTARIO_FUENTES_v1.xlsx` registra ruta, filas, codificación, delimitador, contenido y SHA-256 de cada fuente y maestro original. Las salidas se escriben únicamente en `datos procesados` y `documentación`; los PDF se archivan en `archivo externo`.

## 2. Lectura y reglas comunes

1. Decodificación probada en orden UTF-8-SIG, CP1252 y Latin-1; separador detectado entre `;`, coma, tabulador y `|`. Los {len(sources)} CSV se leyeron sin errores.
2. Se verificó que las 166 columnas `Unnamed` estuvieran completamente vacías antes de excluirlas.
3. La vinculación usa nombre de archivo + nombre normalizado para cruce (mayúsculas, Unicode y espacios, sin acentos solo en la clave) + número de ocurrencia. El nombre original se conserva. Las ocurrencias múltiples no se eliminan automáticamente.
4. El período proviene de `Año` y `Mes` **dentro del contenido**, nunca del prefijo o nombre del archivo. El nombre físico queda en la trazabilidad.
5. Importes: se eliminan moneda y separadores; punto = miles y coma = decimales; se conservan pesos enteros. `No tiene`, `No informa`, `-` y vacío se transforman en 0 en columnas `_clp`; el texto original queda en `_raw`.
6. Horas: expresión sobre el segmento `monto : N,NN hrs`; la coma decimal se transforma en punto. Si no hay horas publicadas, el valor derivado es 0. Nunca se reparten horas genéricas entre diurnas/nocturnas/festivas.
7. Fechas: interpretación día/mes/año a ISO `AAAA-MM-DD`; el original y la clasificación de término se preservan. `Indefinido` no se convierte en una fecha ficticia.
8. Toda fila canónica incorpora archivo, ruta, fila CSV (encabezado = 1), SHA-256, codificación y separador. `registro_id` es único por ruta + fila; `id_trabajador` se conserva del maestro manual.

## 3. Correcciones manuales conocidas y su tratamiento

El encargo antecedente informa **deduplicación manual** e **inferencia de género por nombre con revisión manual de ambiguos**. No existen en la carpeta tablas separadas que permitan reejecutar esas decisiones; por ello se documentan como antecedentes conocidos, no como transformaciones independientemente reproducidas en este lote. Los IDs, nombres depurados, primeros nombres y géneros se conservaron. No se volvió a inferir género ni se aplicó una nueva deduplicación. Las repeticiones H-005 y H-006 se conservaron por tener valores o fuentes distintos.

## 4. Tarea 1 — Integridad de Código del Trabajo

- Los 36 CSV suman **933 filas**, exactamente las 933 del maestro; la cobertura mensual coincide en 36/36 meses.
- El cruce por período + nombre + ocurrencia vinculó 933/933 filas, sin registros huérfanos.
- Se detectó que **15 columnas crudas** estaban vacías en los tres años y `_archivo_origen` también, no solo en 2024-2025. Se restauraron **14.928 celdas** (13.995 de campos crudos + 933 de origen) en una versión nueva.
- Los siete importes numéricos y `he_horas_num` coinciden con el recálculo desde CSV en todas las filas: **0 diferencias**.
- La v2 conserva ID, nombre depurado, primer nombre, género, estamento, observaciones y numéricos del maestro; incorpora ruta, fila y SHA-256.
- Las anomalías de nombres 2024/2025 se resolvieron por contenido. Además se encontró una fila de mayo dentro del CSV de julio de 2025 (H-005); no se deduplicó.

**Salida:** `MAESTRO_CODTrabajo_Coronel_2023-2025_v2_corregido.xlsx`, con hojas de control, diferencias, cobertura y anomalías.

## 5. Tarea 2 — Recuperación de horas extra

Se comprobó que el texto raw de Planta y Contrata coincide con el CSV en las tres clases de horas. Resultados:

| Maestro | Tipo | Registros con horas | Horas totales | Monto total CLP | Monto positivo sin horas |
|---|---:|---:|---:|---:|---:|
| Planta | Diurnas | {hpl['diurnas']['registros_con_horas']:,} | {hpl['diurnas']['horas_totales']:,.0f} | {hpl['diurnas']['monto_total_clp']:,} | 0 |
| Planta | Nocturnas | {hpl['nocturnas']['registros_con_horas']:,} | {hpl['nocturnas']['horas_totales']:,.0f} | {hpl['nocturnas']['monto_total_clp']:,} | 0 |
| Planta | Festivas | 0 | 0 | 0 | 0 |
| Contrata | Diurnas | {hco['diurnas']['registros_con_horas']:,} | {hco['diurnas']['horas_totales']:,.0f} | {hco['diurnas']['monto_total_clp']:,} | 0 |
| Contrata | Nocturnas | {hco['nocturnas']['registros_con_horas']:,} | {hco['nocturnas']['horas_totales']:,.0f} | {hco['nocturnas']['monto_total_clp']:,} | 0 |
| Contrata | Festivas | 0 | 0 | 0 | 0 |

Código del Trabajo ya tenía `he_horas_num`; se validó contra el raw con 0 diferencias. Su fuente no distingue tipo, por lo que el canónico usa `horas_extra_horas` y `horas_extra_desagregacion=sin_desagregacion`.

**Salidas:** versiones nuevas `v2_horas` de Planta y Contrata. No se copiaron resúmenes heredados que pudieran quedar desactualizados.

## 6. Tarea 3 — Esquema canónico

Se adoptó `snake_case` en español, sin acentos en nombres técnicos. Núcleo común: `categoria`, `registro_id`, `id_trabajador`, `anio`, `mes_numero`, `mes_nombre`, `periodo`, identidad, estamento, cargo, fechas raw/ISO, importes raw/CLP y trazabilidad. Los conceptos específicos conservan sufijos por tipo de hora y los campos de pago/enlace de Honorarios.

| Maestro | Filas | Columnas canónicas | Vinculación CSV | Diferencias numéricas heredadas |
|---|---:|---:|---:|---:|
| Planta | {rows['Planta']:,} | {canon['Planta']['columnas']} | 100 % | 0 |
| Contrata | {rows['Contrata']:,} | {canon['Contrata']['columnas']} | 100 % | 0 |
| Código del Trabajo | {rows['Código del Trabajo']:,} | {canon['Código del Trabajo']['columnas']} | 100 % | 0 |
| Honorarios | {rows['Honorarios']:,} | {canon['Honorarios']['columnas']} | 100 % | 0 |
| **Total** | **{sum(rows.values()):,}** | — | **100 %** | **0** |

`MAPEO_ESQUEMA_CANONICO_v1.xlsx` documenta columna original del maestro, columna CSV, nombre canónico y regla. Las hojas analíticas antiguas no se copiaron. En particular, el resumen de Planta tiene 757 filas para 178 IDs y no se consideró confiable (H-007).

## 7. Informes de funciones de Honorarios

El inventario se extrae directamente de `Enlace funciones desarrolladas`, conservando trabajador, período, URL, archivo y fila. La descarga se realiza por lotes a `archivo externo/informes_funciones_honorarios/AAAA/MM/`. El manifiesto registra fecha, URL de descarga, HTTP, estado, bytes, SHA-256 y ruta local; solo se declara `descargado` con HTTP 200 y firma PDF válida.

La ejecución v1 **ya reescribió los parámetros `dl=0` a `dl=1`**. Una prueba controlada con tres URL recuperadas mostró respuestas variables de Dropbox: la misma URL con `dl=1` entregó PDF o HTML en distintas solicitudes, con ambos agentes de usuario. En consecuencia, el artefacto no se atribuye al parámetro `dl=0` ni a un cliente específico, y los estados no terminales se reintentan nuevamente al reanudar. Para descartar un artefacto técnico en H-010, v2 reintentó los {retry['objetos_reintentados']:,} objetos sin PDF nuevamente con `dl=1`, registrando URL final, HTTP, tipo de contenido, título HTML y SHA-256 de la respuesta. Solo cuando no existía una eliminación explícita se probaron además `raw=1` y el host directo. Resultado: {retry['recuperados']:,} PDF recuperados, {retry['file_deleted']:,} objetos con `File Deleted`, {retry['link_temporarily_disabled']:,} con `Link Temporarily Disabled` y {sum(retry['otros'].values()):,} con otros estados. Las respuestas `File Deleted` se clasifican como eliminación explícita, no como previsualizaciones ni como una inferencia genérica de enlaces rotos.

Los {retry['sin_url']:,} registros sin URL se mantienen separados: no son fallos de Dropbox. `MANIFIESTO_DESCARGAS_v1.xlsx` se conserva como antecedente de auditoría; `REINTENTOS_DROPBOX_H010_v1.xlsx` y `MANIFIESTO_DESCARGAS_v2.xlsx` constituyen la evidencia vigente, junto con `INVENTARIO_INFORMES_HONORARIOS_v1.xlsx` y H-010.

## 8. Validación y límites

- {sum(rows.values()):,} registros canónicos vinculados a fuente; 0 IDs de registro duplicados.
- Todos los importes y horas heredados comparados contra CSV: 0 diferencias.
- Fechas de inicio no vacías no parseadas: 0 en los cuatro maestros.
- Las cifras de personas, períodos repetidos o resúmenes no deben interpretarse como nómina única sin reglas adicionales; hay dos pares período-nombre conservados y documentados.
- Autoridades no forma parte de los cuatro maestros canónicos solicitados. Su ausencia de 2023 y el período no informado de diciembre de 2025 quedan pendientes.

## 9. Plantilla replicable para futuras categorías

1. Congelar fuentes; inventariar ruta, filas, esquema, codificación y SHA-256.
2. Comparar nombre de archivo contra período del contenido; registrar anomalías sin renombrar originales.
3. Perfil de columnas: vacíos, `Unnamed`, tipos, catálogos y formatos monetarios/horarios.
4. Definir clave de cruce y ocurrencia; no deduplicar solo por persona-período.
5. Contrastar filas por mes y totales por columna contra el maestro anterior.
6. Restaurar campos en archivo nuevo; nunca sobrescribir el manual ni el CSV.
7. Aplicar esquema canónico, conservar `_raw` y agregar derivados con reglas explícitas.
8. Añadir trazabilidad archivo/ruta/fila/SHA-256 a cada registro.
9. Documentar correcciones manuales conocidas y separar las que no son reproducibles.
10. Ejecutar controles de filas, huérfanos, duplicados, importes, horas, fechas y apertura/verificación XLSX.
11. Registrar hallazgos con severidad, evidencia, impacto, decisión y pendiente.
12. Versionar entregables y conservar manifiestos de descargas externas.

## 10. Scripts de reproducción

Los scripts quedan en `scripts/`: inspección, auditoría de Código del Trabajo, corrección, recuperación de horas, normalización, inventario/descargas y validación. Su ejecución utiliza únicamente las fuentes del espacio de trabajo y vuelve a crear archivos procesados, nunca los originales.
'''
(DOCS/'BITACORA_TRANSFORMACIONES_v1.md').write_text(bit,encoding='utf-8')
print('Diccionario:',len(dictdf),'filas; fuentes:',len(sources),'; hallazgos:',len(findings))
print('Documentos generados en',DOCS)
