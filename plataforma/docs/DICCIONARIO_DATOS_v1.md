# Diccionario de datos — Personal y Remuneraciones

**Versión:** canonico_v1.0.0  
**Fecha de generación:** 2026-11-14

Cada tabla enumera todas las columnas del maestro canónico. `crudo` significa que el valor proviene del CSV; `derivado` indica una transformación o un campo conservado del maestro manual. Los importes `_clp` son pesos chilenos y las fechas ISO se acompañan siempre de su campo `_raw`.

## Planta

| Columna | Tipo | Descripción | Valores posibles | Origen | Regla de transformación | Maestro original | CSV crudo |
|---|---|---|---|---|---|---|---|
| categoria | texto | Estamento o categoría de transparencia | Planta \| Contrata \| Código del Trabajo \| Honorarios | derivado | Constante asignada por categoría |  |  |
| registro_id | texto | Identificador único y estable del registro mensual | Un valor único por archivo y fila | derivado | Categoría + período + SHA-1 abreviado de ruta relativa y fila CSV |  |  |
| id_trabajador | texto | Identificador de trabajador del maestro manual | Valor heredado; no implica unicidad global validada | derivado | Conservado sin regenerar | ID_Trabajador |  |
| anio | entero | Año declarado en el contenido del CSV | 2023 \| 2024 \| 2025 | crudo | Conversión a entero; no se obtiene del nombre de archivo |  | Año |
| mes_numero | entero | Número de mes declarado en el contenido del CSV | 1-12 | derivado | Catálogo de nombres de mes en español |  | Mes |
| mes_nombre | texto | Nombre canónico del mes | Enero-Diciembre | derivado | Catálogo controlado a partir de Mes |  | Mes |
| periodo | texto (AAAA-MM) | Período mensual de la observación | AAAA-MM | derivado | Concatenación de anio y mes_numero |  |  |
| nombre_original | texto | Nombre tal como aparece en el CSV | Texto libre | crudo | Normalización Unicode y espacios; sin cambiar identidad |  | Nombre completo |
| nombre_normalizado | texto | Nombre depurado en el maestro manual | Texto libre | derivado | Conservado del maestro; no se recalcula | nombre_limpio |  |
| primer_nombre | texto | Primer nombre usado para revisión manual | Texto libre | derivado | Conservado del maestro | primer_nombre |  |
| genero | texto | Género registrado en el maestro tras inferencia y revisión manual | Femenino \| Masculino | derivado | Conservado; no se vuelve a inferir por nombre | genero |  |
| estamento | texto | Estamento o categoría funcional | Texto controlado según valores observados | crudo | Conservado del maestro/CSV | Estamento |  |
| cargo_funcion | texto | Cargo o descripción de la función | Texto libre | crudo | Normalización Unicode y espacios |  | Cargo o función |
| grado_eus_jornada | texto | Grado EUS o jornada informado | Texto libre; incluye No Asimilado a Grado | crudo | Texto conservado |  | Grado EUS o jornada |
| calificacion_profesional | texto | Calificación profesional o formación | Texto libre | crudo | Normalización Unicode y espacios |  | Calificación profesional o formación |
| region | texto | Región de desempeño | Texto libre; predominantemente Región del Biobío | crudo | Texto conservado |  | Región |
| fecha_inicio_raw | texto | Fecha de inicio tal como fue publicada | Texto libre | crudo | Conservada para auditoría |  | Fecha de inicio dd/mm/aa |
| fecha_inicio | fecha ISO 8601 (texto) | Fecha de inicio normalizada | AAAA-MM-DD o vacío si no es parseable | derivado | Interpretación día/mes/año; valor original preservado |  | Fecha de inicio dd/mm/aa |
| fecha_termino_raw | texto | Fecha de término o condición contractual publicada | Texto libre; incluye Indefinido | crudo | Conservada para auditoría |  | Fecha de término dd/mm/aa |
| fecha_termino | fecha ISO 8601 (texto) | Fecha de término normalizada | AAAA-MM-DD o vacío si no es una fecha | derivado | Interpretación día/mes/año; Indefinido queda vacío |  | Fecha de término dd/mm/aa |
| fecha_termino_tipo | texto | Clasificación del valor de término | fecha \| indefinido \| no_informa \| no_especificado \| otro | derivado | Clasificación de fecha_termino_raw y su parseo |  |  |
| observaciones | texto | Observaciones publicadas | Texto libre | crudo | Normalización Unicode y espacios |  | Observaciones |
| asignaciones_especiales_raw | texto | Códigos de asignaciones especiales incluidos en bruto | Texto con códigos entre paréntesis | crudo | Texto conservado |  | Asignaciones especiales del mes (inc. en rem. bruta) |
| remuneracion_bruta_raw | texto | Valor publicado de remuneracion bruta | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras) |
| remuneracion_bruta_clp | entero (CLP) | Remuneracion bruta en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras) |
| remuneracion_liquida_raw | texto | Valor publicado de remuneracion liquida | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración líquida del mes |
| remuneracion_liquida_clp | entero (CLP) | Remuneracion liquida en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración líquida del mes |
| viaticos_raw | texto | Valor publicado de viaticos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Viáticos del mes (no inc. en rem. bruta) |
| viaticos_clp | entero (CLP) | Viaticos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Viáticos del mes (no inc. en rem. bruta) |
| remuneracion_adicional_raw | texto | Valor publicado de remuneracion adicional | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Rem. adicionales del mes (no inc. en rem. bruta) |
| remuneracion_adicional_clp | entero (CLP) | Remuneracion adicional en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Rem. adicionales del mes (no inc. en rem. bruta) |
| bonos_incentivos_raw | texto | Valor publicado de bonos incentivos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración Bonos incentivos del mes (inc. en rem. bruta) |
| bonos_incentivos_clp | entero (CLP) | Bonos incentivos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración Bonos incentivos del mes (inc. en rem. bruta) |
| derecho_horas_extra | texto | Derecho a horas extraordinarias declarado | Sí \| No \| otros valores publicados | crudo | Texto conservado |  | Derecho a horas extraordinarias |
| horas_extra_diurnas_raw | texto | Monto y horas extra diurnas publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta) |
| horas_extra_diurnas_clp | entero (CLP) | Monto de horas extra diurnas en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta) |
| horas_extra_diurnas_horas | decimal (horas) | Cantidad de horas extra diurnas | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta) |
| horas_extra_nocturnas_raw | texto | Monto y horas extra nocturnas publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta) |
| horas_extra_nocturnas_clp | entero (CLP) | Monto de horas extra nocturnas en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta) |
| horas_extra_nocturnas_horas | decimal (horas) | Cantidad de horas extra nocturnas | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta) |
| horas_extra_festivas_raw | texto | Monto y horas extra festivas publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias festivas del mes (inc. en rem. bruta) |
| horas_extra_festivas_clp | entero (CLP) | Monto de horas extra festivas en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias festivas del mes (inc. en rem. bruta) |
| horas_extra_festivas_horas | decimal (horas) | Cantidad de horas extra festivas | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias festivas del mes (inc. en rem. bruta) |
| fuente_archivo | texto | Nombre del CSV de origen | Valor observado en archivos fuente | crudo | Nombre físico conservado |  | fuente_archivo |
| fuente_ruta_relativa | texto | Ruta relativa del CSV desde la raíz del proyecto | Valor observado en archivos fuente | derivado | Ruta relativa conservada |  | fuente_ruta_relativa |
| fuente_fila_csv | entero | Número de fila en el CSV, contando encabezado como fila 1 | Entero ≥ 2 | derivado | Índice original + 2 |  | fuente_fila_csv |
| fuente_sha256 | texto (SHA-256) | Huella digital del CSV fuente | 64 caracteres hexadecimales | derivado | SHA-256 de bytes originales |  | fuente_sha256 |
| fuente_encoding | texto | Codificación detectada del CSV | Valor observado en archivos fuente | derivado | Decodificación probada en orden UTF-8-SIG, CP1252, Latin-1 |  | fuente_encoding |
| fuente_separador | texto | Delimitador detectado del CSV | Valor observado en archivos fuente | derivado | Detección con csv.Sniffer |  | fuente_separador |
| version_esquema | texto | Versión del esquema canónico | canonico_v1.0.0 | derivado | Constante de versión |  |  |
| fecha_procesamiento | fecha-hora ISO 8601 | Marca temporal del procesamiento | ISO 8601 con zona America/Santiago | derivado | Marca de ejecución del proceso |  |  |

## Contrata

| Columna | Tipo | Descripción | Valores posibles | Origen | Regla de transformación | Maestro original | CSV crudo |
|---|---|---|---|---|---|---|---|
| categoria | texto | Estamento o categoría de transparencia | Planta \| Contrata \| Código del Trabajo \| Honorarios | derivado | Constante asignada por categoría |  |  |
| registro_id | texto | Identificador único y estable del registro mensual | Un valor único por archivo y fila | derivado | Categoría + período + SHA-1 abreviado de ruta relativa y fila CSV |  |  |
| id_trabajador | texto | Identificador de trabajador del maestro manual | Valor heredado; no implica unicidad global validada | derivado | Conservado sin regenerar | ID_Trabajador |  |
| anio | entero | Año declarado en el contenido del CSV | 2023 \| 2024 \| 2025 | crudo | Conversión a entero; no se obtiene del nombre de archivo |  | Año |
| mes_numero | entero | Número de mes declarado en el contenido del CSV | 1-12 | derivado | Catálogo de nombres de mes en español |  | Mes |
| mes_nombre | texto | Nombre canónico del mes | Enero-Diciembre | derivado | Catálogo controlado a partir de Mes |  | Mes |
| periodo | texto (AAAA-MM) | Período mensual de la observación | AAAA-MM | derivado | Concatenación de anio y mes_numero |  |  |
| nombre_original | texto | Nombre tal como aparece en el CSV | Texto libre | crudo | Normalización Unicode y espacios; sin cambiar identidad |  | Nombre completo |
| nombre_normalizado | texto | Nombre depurado en el maestro manual | Texto libre | derivado | Conservado del maestro; no se recalcula | nombre_limpio |  |
| primer_nombre | texto | Primer nombre usado para revisión manual | Texto libre | derivado | Conservado del maestro | primer_nombre |  |
| genero | texto | Género registrado en el maestro tras inferencia y revisión manual | Femenino \| Masculino | derivado | Conservado; no se vuelve a inferir por nombre | genero |  |
| estamento | texto | Estamento o categoría funcional | Texto controlado según valores observados | crudo | Conservado del maestro/CSV | Estamento |  |
| cargo_funcion | texto | Cargo o descripción de la función | Texto libre | crudo | Normalización Unicode y espacios |  | Cargo o función |
| grado_eus_jornada | texto | Grado EUS o jornada informado | Texto libre; incluye No Asimilado a Grado | crudo | Texto conservado |  | Grado EUS o jornada |
| calificacion_profesional | texto | Calificación profesional o formación | Texto libre | crudo | Normalización Unicode y espacios |  | Calificación profesional o formación |
| region | texto | Región de desempeño | Texto libre; predominantemente Región del Biobío | crudo | Texto conservado |  | Región |
| fecha_inicio_raw | texto | Fecha de inicio tal como fue publicada | Texto libre | crudo | Conservada para auditoría |  | Fecha de inicio dd/mm/aa |
| fecha_inicio | fecha ISO 8601 (texto) | Fecha de inicio normalizada | AAAA-MM-DD o vacío si no es parseable | derivado | Interpretación día/mes/año; valor original preservado |  | Fecha de inicio dd/mm/aa |
| fecha_termino_raw | texto | Fecha de término o condición contractual publicada | Texto libre; incluye Indefinido | crudo | Conservada para auditoría |  | Fecha de término dd/mm/aa |
| fecha_termino | fecha ISO 8601 (texto) | Fecha de término normalizada | AAAA-MM-DD o vacío si no es una fecha | derivado | Interpretación día/mes/año; Indefinido queda vacío |  | Fecha de término dd/mm/aa |
| fecha_termino_tipo | texto | Clasificación del valor de término | fecha \| indefinido \| no_informa \| no_especificado \| otro | derivado | Clasificación de fecha_termino_raw y su parseo |  |  |
| observaciones | texto | Observaciones publicadas | Texto libre | crudo | Normalización Unicode y espacios |  | Observaciones |
| asignaciones_especiales_raw | texto | Códigos de asignaciones especiales incluidos en bruto | Texto con códigos entre paréntesis | crudo | Texto conservado |  | Asignaciones especiales del mes (inc. en rem. bruta) |
| remuneracion_bruta_raw | texto | Valor publicado de remuneracion bruta | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras) |
| remuneracion_bruta_clp | entero (CLP) | Remuneracion bruta en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras) |
| remuneracion_liquida_raw | texto | Valor publicado de remuneracion liquida | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración líquida del mes |
| remuneracion_liquida_clp | entero (CLP) | Remuneracion liquida en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración líquida del mes |
| viaticos_raw | texto | Valor publicado de viaticos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Viáticos del mes (no inc. en rem. bruta) |
| viaticos_clp | entero (CLP) | Viaticos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Viáticos del mes (no inc. en rem. bruta) |
| remuneracion_adicional_raw | texto | Valor publicado de remuneracion adicional | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Rem. adicionales del mes (no inc. en rem. bruta) |
| remuneracion_adicional_clp | entero (CLP) | Remuneracion adicional en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Rem. adicionales del mes (no inc. en rem. bruta) |
| bonos_incentivos_raw | texto | Valor publicado de bonos incentivos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración Bonos incentivos del mes (inc. en rem. bruta) |
| bonos_incentivos_clp | entero (CLP) | Bonos incentivos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración Bonos incentivos del mes (inc. en rem. bruta) |
| derecho_horas_extra | texto | Derecho a horas extraordinarias declarado | Sí \| No \| otros valores publicados | crudo | Texto conservado |  | Derecho a horas extraordinarias |
| horas_extra_diurnas_raw | texto | Monto y horas extra diurnas publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta) |
| horas_extra_diurnas_clp | entero (CLP) | Monto de horas extra diurnas en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta) |
| horas_extra_diurnas_horas | decimal (horas) | Cantidad de horas extra diurnas | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias diurnas del mes(inc. en rem. bruta) |
| horas_extra_nocturnas_raw | texto | Monto y horas extra nocturnas publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta) |
| horas_extra_nocturnas_clp | entero (CLP) | Monto de horas extra nocturnas en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta) |
| horas_extra_nocturnas_horas | decimal (horas) | Cantidad de horas extra nocturnas | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias nocturnas del mes(inc. en rem. bruta) |
| horas_extra_festivas_raw | texto | Monto y horas extra festivas publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias festivas del mes (inc. en rem. bruta) |
| horas_extra_festivas_clp | entero (CLP) | Monto de horas extra festivas en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias festivas del mes (inc. en rem. bruta) |
| horas_extra_festivas_horas | decimal (horas) | Cantidad de horas extra festivas | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias festivas del mes (inc. en rem. bruta) |
| fuente_archivo | texto | Nombre del CSV de origen | Valor observado en archivos fuente | crudo | Nombre físico conservado |  | fuente_archivo |
| fuente_ruta_relativa | texto | Ruta relativa del CSV desde la raíz del proyecto | Valor observado en archivos fuente | derivado | Ruta relativa conservada |  | fuente_ruta_relativa |
| fuente_fila_csv | entero | Número de fila en el CSV, contando encabezado como fila 1 | Entero ≥ 2 | derivado | Índice original + 2 |  | fuente_fila_csv |
| fuente_sha256 | texto (SHA-256) | Huella digital del CSV fuente | 64 caracteres hexadecimales | derivado | SHA-256 de bytes originales |  | fuente_sha256 |
| fuente_encoding | texto | Codificación detectada del CSV | Valor observado en archivos fuente | derivado | Decodificación probada en orden UTF-8-SIG, CP1252, Latin-1 |  | fuente_encoding |
| fuente_separador | texto | Delimitador detectado del CSV | Valor observado en archivos fuente | derivado | Detección con csv.Sniffer |  | fuente_separador |
| version_esquema | texto | Versión del esquema canónico | canonico_v1.0.0 | derivado | Constante de versión |  |  |
| fecha_procesamiento | fecha-hora ISO 8601 | Marca temporal del procesamiento | ISO 8601 con zona America/Santiago | derivado | Marca de ejecución del proceso |  |  |

## Código del Trabajo

| Columna | Tipo | Descripción | Valores posibles | Origen | Regla de transformación | Maestro original | CSV crudo |
|---|---|---|---|---|---|---|---|
| categoria | texto | Estamento o categoría de transparencia | Planta \| Contrata \| Código del Trabajo \| Honorarios | derivado | Constante asignada por categoría |  |  |
| registro_id | texto | Identificador único y estable del registro mensual | Un valor único por archivo y fila | derivado | Categoría + período + SHA-1 abreviado de ruta relativa y fila CSV |  |  |
| id_trabajador | texto | Identificador de trabajador del maestro manual | Valor heredado; no implica unicidad global validada | derivado | Conservado sin regenerar | ID_Trabajador |  |
| anio | entero | Año declarado en el contenido del CSV | 2023 \| 2024 \| 2025 | crudo | Conversión a entero; no se obtiene del nombre de archivo |  | Año |
| mes_numero | entero | Número de mes declarado en el contenido del CSV | 1-12 | derivado | Catálogo de nombres de mes en español |  | Mes |
| mes_nombre | texto | Nombre canónico del mes | Enero-Diciembre | derivado | Catálogo controlado a partir de Mes |  | Mes |
| periodo | texto (AAAA-MM) | Período mensual de la observación | AAAA-MM | derivado | Concatenación de anio y mes_numero |  |  |
| nombre_original | texto | Nombre tal como aparece en el CSV | Texto libre | crudo | Normalización Unicode y espacios; sin cambiar identidad |  | Nombre completo |
| nombre_normalizado | texto | Nombre depurado en el maestro manual | Texto libre | derivado | Conservado del maestro; no se recalcula | nombre_limpio |  |
| primer_nombre | texto | Primer nombre usado para revisión manual | Texto libre | derivado | Conservado del maestro | primer_nombre |  |
| genero | texto | Género registrado en el maestro tras inferencia y revisión manual | Femenino \| Masculino | derivado | Conservado; no se vuelve a inferir por nombre | genero |  |
| estamento | texto | Estamento o categoría funcional | Texto controlado según valores observados | derivado | Conservado del maestro manual; no existe en el CSV | Estamento |  |
| cargo_funcion | texto | Cargo o descripción de la función | Texto libre | crudo | Normalización Unicode y espacios |  | Cargo o función |
| grado_eus_jornada | texto | Grado EUS o jornada informado | Texto libre; incluye No Asimilado a Grado | crudo | Texto conservado |  | Grado EUS o jornada |
| calificacion_profesional | texto | Calificación profesional o formación | Texto libre | crudo | Normalización Unicode y espacios |  | Calificación profesional o formación |
| region | texto | Región de desempeño | Texto libre; predominantemente Región del Biobío | crudo | Texto conservado |  | Región |
| fecha_inicio_raw | texto | Fecha de inicio tal como fue publicada | Texto libre | crudo | Conservada para auditoría |  | Fecha de inicio dd/mm/aaaa |
| fecha_inicio | fecha ISO 8601 (texto) | Fecha de inicio normalizada | AAAA-MM-DD o vacío si no es parseable | derivado | Interpretación día/mes/año; valor original preservado |  | Fecha de inicio dd/mm/aaaa |
| fecha_termino_raw | texto | Fecha de término o condición contractual publicada | Texto libre; incluye Indefinido | crudo | Conservada para auditoría |  | Fecha de término dd/mm/aaaa |
| fecha_termino | fecha ISO 8601 (texto) | Fecha de término normalizada | AAAA-MM-DD o vacío si no es una fecha | derivado | Interpretación día/mes/año; Indefinido queda vacío |  | Fecha de término dd/mm/aaaa |
| fecha_termino_tipo | texto | Clasificación del valor de término | fecha \| indefinido \| no_informa \| no_especificado \| otro | derivado | Clasificación de fecha_termino_raw y su parseo |  |  |
| observaciones | texto | Observaciones publicadas | Texto libre | crudo | Normalización Unicode y espacios |  | Observaciones |
| asignaciones_especiales_raw | texto | Códigos de asignaciones especiales incluidos en bruto | Texto con códigos entre paréntesis | crudo | Texto conservado |  | Asignaciones especiales del mes (inc. en rem. bruta) |
| remuneracion_bruta_raw | texto | Valor publicado de remuneracion bruta | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras) |
| remuneracion_bruta_clp | entero (CLP) | Remuneracion bruta en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración bruta del mes (incluye bonos e incentivos, asig. especiales, horas extras) |
| remuneracion_liquida_raw | texto | Valor publicado de remuneracion liquida | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración líquida del mes |
| remuneracion_liquida_clp | entero (CLP) | Remuneracion liquida en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración líquida del mes |
| viaticos_raw | texto | Valor publicado de viaticos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Viáticos del mes (no inc. en rem. bruta) |
| viaticos_clp | entero (CLP) | Viaticos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Viáticos del mes (no inc. en rem. bruta) |
| remuneracion_adicional_raw | texto | Valor publicado de remuneracion adicional | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Rem. adicionales del mes (no inc. en rem. bruta) |
| remuneracion_adicional_clp | entero (CLP) | Remuneracion adicional en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Rem. adicionales del mes (no inc. en rem. bruta) |
| bonos_incentivos_raw | texto | Valor publicado de bonos incentivos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Remuneración Bonos incentivos del mes (inc. en rem. bruta) |
| bonos_incentivos_clp | entero (CLP) | Bonos incentivos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Remuneración Bonos incentivos del mes (inc. en rem. bruta) |
| monto_desvinculacion_raw | texto | Valor publicado de monto desvinculacion | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Monto de desvinculación (no inc. en rem. bruta) |
| monto_desvinculacion_clp | entero (CLP) | Monto desvinculacion en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Monto de desvinculación (no inc. en rem. bruta) |
| derecho_horas_extra | texto | Derecho a horas extraordinarias declarado | Sí \| No \| otros valores publicados | crudo | Texto conservado |  | Derecho a horas extraordinarias |
| horas_extra_raw | texto | Monto y horas extra generico publicados | Texto “monto : horas hrs”, No tiene o No informa | crudo | Texto conservado |  | Montos y horas extraordinarias del mes(inc. en rem. bruta) |
| horas_extra_clp | entero (CLP) | Monto de horas extra generico en pesos | Entero ≥ 0 | derivado | Parseo de segmento anterior a “:” |  | Montos y horas extraordinarias del mes(inc. en rem. bruta) |
| horas_extra_horas | decimal (horas) | Cantidad de horas extra generico | Decimal ≥ 0; 0 si no publica horas | derivado | Extraer número posterior a “:” y anterior a “hrs”; coma decimal a punto |  | Montos y horas extraordinarias del mes(inc. en rem. bruta) |
| horas_extra_desagregacion | texto | Nivel de desagregación de horas extra | sin_desagregacion | derivado | La fuente no distingue diurnas, nocturnas o festivas |  |  |
| fuente_archivo | texto | Nombre del CSV de origen | Valor observado en archivos fuente | crudo | Nombre físico conservado |  | fuente_archivo |
| fuente_ruta_relativa | texto | Ruta relativa del CSV desde la raíz del proyecto | Valor observado en archivos fuente | derivado | Ruta relativa conservada |  | fuente_ruta_relativa |
| fuente_fila_csv | entero | Número de fila en el CSV, contando encabezado como fila 1 | Entero ≥ 2 | derivado | Índice original + 2 |  | fuente_fila_csv |
| fuente_sha256 | texto (SHA-256) | Huella digital del CSV fuente | 64 caracteres hexadecimales | derivado | SHA-256 de bytes originales |  | fuente_sha256 |
| fuente_encoding | texto | Codificación detectada del CSV | Valor observado en archivos fuente | derivado | Decodificación probada en orden UTF-8-SIG, CP1252, Latin-1 |  | fuente_encoding |
| fuente_separador | texto | Delimitador detectado del CSV | Valor observado en archivos fuente | derivado | Detección con csv.Sniffer |  | fuente_separador |
| version_esquema | texto | Versión del esquema canónico | canonico_v1.0.0 | derivado | Constante de versión |  |  |
| fecha_procesamiento | fecha-hora ISO 8601 | Marca temporal del procesamiento | ISO 8601 con zona America/Santiago | derivado | Marca de ejecución del proceso |  |  |

## Honorarios

| Columna | Tipo | Descripción | Valores posibles | Origen | Regla de transformación | Maestro original | CSV crudo |
|---|---|---|---|---|---|---|---|
| categoria | texto | Estamento o categoría de transparencia | Planta \| Contrata \| Código del Trabajo \| Honorarios | derivado | Constante asignada por categoría |  |  |
| registro_id | texto | Identificador único y estable del registro mensual | Un valor único por archivo y fila | derivado | Categoría + período + SHA-1 abreviado de ruta relativa y fila CSV |  |  |
| id_trabajador | texto | Identificador de trabajador del maestro manual | Valor heredado; no implica unicidad global validada | derivado | Conservado sin regenerar | ID Trabajador |  |
| anio | entero | Año declarado en el contenido del CSV | 2023 \| 2024 \| 2025 | crudo | Conversión a entero; no se obtiene del nombre de archivo |  | Año |
| mes_numero | entero | Número de mes declarado en el contenido del CSV | 1-12 | derivado | Catálogo de nombres de mes en español |  | Mes |
| mes_nombre | texto | Nombre canónico del mes | Enero-Diciembre | derivado | Catálogo controlado a partir de Mes |  | Mes |
| periodo | texto (AAAA-MM) | Período mensual de la observación | AAAA-MM | derivado | Concatenación de anio y mes_numero |  |  |
| nombre_original | texto | Nombre tal como aparece en el CSV | Texto libre | crudo | Normalización Unicode y espacios; sin cambiar identidad |  | Nombre completo |
| nombre_normalizado | texto | Nombre depurado en el maestro manual | Texto libre | derivado | Conservado del maestro; no se recalcula | Nombre Limpio |  |
| primer_nombre | texto | Primer nombre usado para revisión manual | Texto libre | derivado | Conservado del maestro | Primer Nombre |  |
| genero | texto | Género registrado en el maestro tras inferencia y revisión manual | Femenino \| Masculino | derivado | Conservado; no se vuelve a inferir por nombre | Género |  |
| estamento | texto | Estamento o categoría funcional | Texto controlado según valores observados | derivado | Constante Honorarios |  |  |
| cargo_funcion | texto | Cargo o descripción de la función | Texto libre | crudo | Normalización Unicode y espacios |  | Descripción de la función |
| grado_eus_jornada | texto | Grado EUS o jornada informado | Texto libre; incluye No Asimilado a Grado | crudo | Texto conservado |  | Grado EUS  (si corresponde) |
| calificacion_profesional | texto | Calificación profesional o formación | Texto libre | crudo | Normalización Unicode y espacios |  | Calificación profesional o formación |
| region | texto | Región de desempeño | Texto libre; predominantemente Región del Biobío | crudo | Texto conservado |  | Región |
| fecha_inicio_raw | texto | Fecha de inicio tal como fue publicada | Texto libre | crudo | Conservada para auditoría |  | Fecha de inicio |
| fecha_inicio | fecha ISO 8601 (texto) | Fecha de inicio normalizada | AAAA-MM-DD o vacío si no es parseable | derivado | Interpretación día/mes/año; valor original preservado |  | Fecha de inicio |
| fecha_termino_raw | texto | Fecha de término o condición contractual publicada | Texto libre; incluye Indefinido | crudo | Conservada para auditoría |  | Fecha de término |
| fecha_termino | fecha ISO 8601 (texto) | Fecha de término normalizada | AAAA-MM-DD o vacío si no es una fecha | derivado | Interpretación día/mes/año; Indefinido queda vacío |  | Fecha de término |
| fecha_termino_tipo | texto | Clasificación del valor de término | fecha \| indefinido \| no_informa \| no_especificado \| otro | derivado | Clasificación de fecha_termino_raw y su parseo |  |  |
| observaciones | texto | Observaciones publicadas | Texto libre | crudo | Normalización Unicode y espacios |  | Observaciones |
| remuneracion_bruta_raw | texto | Valor publicado de remuneracion bruta | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Honorario Total Bruto del mes |
| remuneracion_bruta_clp | entero (CLP) | Remuneracion bruta en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Honorario Total Bruto del mes |
| remuneracion_liquida_raw | texto | Valor publicado de remuneracion liquida | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Honorario Total Líquido del mes |
| remuneracion_liquida_clp | entero (CLP) | Remuneracion liquida en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Honorario Total Líquido del mes |
| viaticos_raw | texto | Valor publicado de viaticos | Texto libre con formato monetario o No informa/No tiene | crudo | Texto conservado |  | Viáticos |
| viaticos_clp | entero (CLP) | Viaticos en pesos chilenos | Entero ≥ 0; 0 si fuente no informa/no tiene | derivado | Quitar moneda y separadores; punto=miles, coma=decimales; truncar a pesos |  | Viáticos |
| tipo_pago | texto | Tipo de pago | Texto libre | crudo | Texto conservado |  | Tipo de pago |
| descripcion_pago | texto | Descripción del pago | Texto libre | crudo | Texto conservado |  | Descripción pago |
| numero_cuotas_raw | texto | Número de cuotas publicado | Texto numérico o “-” | crudo | Texto conservado |  | Número de cuotas |
| numero_cuotas | entero nullable | Número de cuotas | Entero ≥ 0 o vacío si no aplica/no informa | derivado | Conversión numérica; “-” queda vacío |  | Número de cuotas |
| enlace_funciones_desarrolladas_raw | texto | HTML del enlace al informe de funciones | HTML o vacío | crudo | Texto conservado |  | Enlace funciones desarrolladas |
| enlace_funciones_desarrolladas_url | texto (URL) | URL extraída del informe de funciones | URL HTTP/HTTPS o vacío | derivado | Extraer primer URL del HTML y decodificar entidades HTML |  | Enlace funciones desarrolladas |
| fuente_archivo | texto | Nombre del CSV de origen | Valor observado en archivos fuente | crudo | Nombre físico conservado |  | fuente_archivo |
| fuente_ruta_relativa | texto | Ruta relativa del CSV desde la raíz del proyecto | Valor observado en archivos fuente | derivado | Ruta relativa conservada |  | fuente_ruta_relativa |
| fuente_fila_csv | entero | Número de fila en el CSV, contando encabezado como fila 1 | Entero ≥ 2 | derivado | Índice original + 2 |  | fuente_fila_csv |
| fuente_sha256 | texto (SHA-256) | Huella digital del CSV fuente | 64 caracteres hexadecimales | derivado | SHA-256 de bytes originales |  | fuente_sha256 |
| fuente_encoding | texto | Codificación detectada del CSV | Valor observado en archivos fuente | derivado | Decodificación probada en orden UTF-8-SIG, CP1252, Latin-1 |  | fuente_encoding |
| fuente_separador | texto | Delimitador detectado del CSV | Valor observado en archivos fuente | derivado | Detección con csv.Sniffer |  | fuente_separador |
| version_esquema | texto | Versión del esquema canónico | canonico_v1.0.0 | derivado | Constante de versión |  |  |
| fecha_procesamiento | fecha-hora ISO 8601 | Marca temporal del procesamiento | ISO 8601 con zona America/Santiago | derivado | Marca de ejecución del proceso |  |  |

## Trazabilidad común

Todos los maestros incluyen `fuente_archivo`, `fuente_ruta_relativa`, `fuente_fila_csv` y `fuente_sha256`. La fila CSV considera el encabezado como fila 1. `registro_id` se deriva de categoría, período y una huella de ruta + fila; `id_trabajador` se conserva del maestro manual y no se reinterpreta como identificador global.

Los catálogos de valores efectivamente observados están en la hoja `Catálogos observados` del archivo Excel.