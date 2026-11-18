# Checklist de verificación — Módulo Personal y Remuneraciones

**Versión:** 1.5.0  
**Fecha:** 2026-11-18  
**Alcance:** criterios originales de aceptación, iteraciones SC-01 a SC-07 y encargo de asignaciones decodificadas, licencias D-16, atribución D-18 y refuerzo de selectores D-20.  
**Base verificada:** `plataforma/dist/`, servida como sitio estático.  
**Evidencia principal:** `evidencia/verificacion_navegador.json`, `evidencia/verificacion_paquete.json`, 35 capturas PNG de la verificación vigente y salidas del pipeline.

## Resultado ejecutivo

- **Agregados, estadísticas, proyección D-15, D-17, glosario y asignaciones:** 77/77 controles aprobados.
- **Navegador, interacción, contraste AA y documentos:** 132/132 controles aprobados en la ejecución final.
- **Integridad del paquete:** APROBADA; 1.087 JSON y 144 CSV verificados.
- **Compuerta 1:** APROBADA sobre la proyección D-15; 0 colisiones sin resolver y 1.068 fichas habilitadas.
- **SC-02:** CUMPLIDA con las 16 entradas aprobadas de `diseño/GLOSARIO_DEFINICIONES_v1.md` como fuente única, incluida «Asignaciones especiales». El antiguo `MICROTEXTOS_EXPLICATIVOS_v1.md` no alimenta la interfaz.
- **Asignaciones especiales:** CUMPLIDA; 394 conceptos oficiales, 13.476 registros con códigos, 13.475 completamente decodificados y una anomalía `-4` visible sin decodificar.
- **Licencia y atribución:** CUMPLIDA; código MIT y derivados CC BY 4.0 conforme a D-16; fuente municipal y producto Portal de Transparencia Trazable diferenciados conforme a D-18.
- **Aceptación completa de la beta:** **no declarada**. Persisten el cumplimiento parcial del enlace a PDF archivados de Honorarios, la prueba cronometrada con tercero no realizada, la revisión pendiente de dependencias y la ausencia de despliegue público.

## 1. Criterios de aceptación de la especificación, ítem por ítem

| Criterio literal | Estado | Evidencia verificada |
|---|---|---|
| «Las 5 vistas existen y cada cifra enlaza a su fuente.» | **Cumple** | Existen panel, explorador, vistas estamentales, ficha individual habilitada y metodología; además hay portada. Las diez rutas verificadas fueron abiertas y capturadas. Los gráficos tienen tabla y fuente; los registros y meses tienen fuente y `_raw`; las alternas muestran identificadores y trazabilidad. Capturas `01_` a `10_`; controles `vista_*`, `fuente_*`, `ficha_*`, `cifras_secundarias_*` y `totales_metodologicos_*`. |
| «Un tercero responde en menos de 5 minutos: gasto en horas extra por categoría y año; evolución de dotación; trayectoria de una persona dada; composición de género agregada.» | **Parcial: falta ensayo con tercero** | El selector de horas cambia 2025 → 2023; dotación y género están visibles con fuentes; las trayectorias PLT y COT se abren, muestran 36 meses y conservan ausencias. No se ejecutó una prueba cronometrada con un tercero. Controles `horas_extra_cambia_de_anio`, `leyenda_genero_panel`, `ficha_planta_*` y `ficha_codigo_*`. |
| «Todas las ausencias conocidas (sección 5) están rotuladas en la interfaz.» | **Cumple** | Portada y metodología declaran unidad organizacional ausente, Autoridades fuera de alcance, «No informa / No tiene» y no reconciliación D-15. Panel y vistas rotulan Honorarios sin horas y Código del Trabajo sin desagregación. Las fichas rotulan cada mes sin registro, sin imputar. Capturas `01_`, `02_`, `06_`, `07_`, `08_`, `09_`, `10_`; controles `honorarios_declara_horas_no_publicadas`, `ficha_planta_huecos_exactos_y_septiembre_presente` y `ficha_codigo_siete_periodos_y_ausencias`. |
| «Leyenda D-14 presente en toda vista con género; ninguna ficha individual muestra género.» | **Cumple** | La leyenda coincide literalmente con `meta.privacidad.leyenda`. El género no está en filtros, tabla, detalle individual, CSV ni ficha. El pipeline verifica su ausencia en los tres JSON del explorador y en las 1.068 fichas. Controles `genero_ausente_de_*`, `leyenda_genero_panel`, `ficha_planta_sin_genero_ni_derivados` y `ficha_codigo_sin_genero_ni_derivados`. |
| «Conteos de la interfaz calzan con VALIDACION_FINAL_v1 (22.940 registros, por categoría).» | **Cumple** | Planta 4.927; Contrata 7.616; Código del Trabajo 933; Honorarios 9.464; total 22.940. También calzan IDs, brutos, líquidos, horas, promedios, medianas y conteos de bruta informada. `plataforma/data/validacion_agregados.json`: 77/77, cero fallas. Captura `10_metodologia_1440.png`. |
| «Sitio estático desplegable en GitHub Pages sin backend; pipeline reproducible con un comando.» | **Cumple, sin despliegue ejecutado** | `python scripts/build_modulo_personal.py` regenera 22.940 registros, 19 JSON raíz y 1.068 fichas. `npm run build` produce `dist/` sin backend, copia 144 CSV, datos y documentos, y crea `.nojekyll`. Se usa `HashRouter`. Se verificó el build mediante un servidor estático local, no GitHub Pages público. |

## 2. Compuertas y reglas duras

| Regla | Estado | Evidencia |
|---|---|---|
| Validación de unicidad antes de ficha | **Ejecutada y aprobada sobre la proyección D-15** | `VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md`: dos colisiones originales resueltas, cero colisiones en la proyección, cero IDs con varios nombres y 56 aliases entre categorías no unificados. |
| Selección conforme a D-15 | **Cumple** | Una coincidencia exacta período-contenido/archivo nominal por cada colisión; sin desempate por monto, orden ni posterioridad. `PLT-202411-8247F5515D` y `COT-202505-8DA800BA00` seleccionados. |
| Versiones alternas visibles | **Cumple** | `PLT-202411-3B54A1958D` y `COT-202505-9D0CE3F70A` aparecen en «Otra publicación del mismo período», con ID, rol, motivo, montos, campos y fuente. Captura `08_ficha_planta_alterna_1440.png`. |
| Colisiones incluidas sin corrección silenciosa | **Cumple** | Las 22.940 filas permanecen en agregados; 22.938 alimentan trayectorias y dos se preservan como alternas. No se sumaron, promediaron ni eliminaron duplicados de los agregados. |
| No reconciliación declarada | **Cumple** | Portada, ficha y metodología explican que la suma de fichas no reconcilia con los agregados. `meta.ficha_individual.nota_reconciliacion` y controles de interfaz. |
| Ausencias individuales sin imputación | **Cumple** | `PLT-2023-0032`: 22 publicados y 14 ausencias exactas, incluido 2024-12 y excluido 2024-09. `COT-2023-0015`: 7 publicados y 29 ausencias. El gráfico no conecta nulos. |
| Catálogo cerrado antes de agregados | **Cumple** | Nueve valores canónicos; 17 mapeos de identidad documentados; cero no mapeables. `catalogo_estamentos.json`. |
| Cero canónico no equivale a cero real | **Cumple** | Tres casos, todos en Código del Trabajo. Las sumas y cada segmento de monto muestran cuántos registros «No informa» incluyen; las filas dicen «No informa (0)»; la mediana excluye esos ceros. |
| Género solo agregado | **Cumple** | Sin género ni `primer_nombre`/`nombre_normalizado` en detalles anuales, fichas o exportación. Con filtros individuales se declara «No calculable». |
| Toda cifra con archivo, período, fila y SHA-256 | **Cumple para las visualizaciones de datos** | Diálogo con archivo, períodos, filas, ruta y SHA. Un CSV abrió con HTTP 200 y su SHA recalculado fue idéntico al declarado; las fuentes de ambas versiones alternas fueron verificadas. |
| Datos fuente de solo lectura | **Cumple** | El pipeline solo lee maestros y CSV originales; escribe en `plataforma/` y `documentación/plataforma/`. Los 144 pares original/copia tienen SHA-256 válido. |

## 3. Verificación de las iteraciones SC-01 a SC-07

### SC-01 — Métrica y barras apiladas por estamento

| Requisito | Estado | Evidencia |
|---|---|---|
| Selector dotación / remuneración bruta en vistas estamentales y panel general | **Cumple** | Ambos selectores fueron ejercitados en navegador; panel y vistas estamentales cambian de métrica sin alterar los totales canónicos. |
| Barras apiladas por la lista cerrada de estamento | **Cumple** | El pipeline genera composición por período × categoría × estamento. La interfaz dibuja barras absolutas por segmento. |
| Tooltip por segmento bajo el cursor | **Cumple** | Muestra estamento o categoría, valor y porcentaje de la barra correspondiente; no sustituye el segmento por un total con segmentos en cero. |
| Control suma(segmentos) = total de barra | **Cumple** | Controles de reconciliación por período y categoría para dotación, bruto y registros «No informa», sin diferencias. |
| Declaración de «No informa» por segmento de monto | **Cumple** | Cada segmento de remuneración bruta expone el conteo de registros sin monto informado incluido en ese segmento. |
| Apilado absoluto por defecto | **Cumple** | Es la representación implementada. El toggle opcional «ver proporciones» no se incorporó. |

### SC-02 — Tarjetas definitorias desde el glosario canónico

| Requisito | Estado | Evidencia |
|---|---|---|
| Fuente única aprobada | **Cumple** | `diseño/GLOSARIO_DEFINICIONES_v1.md` aporta las 16 entradas; el pipeline las copia sin reescritura a `glosario_definiciones.json` y valida su SHA-256. |
| Definiciones y fuentes exactas | **Cumple** | Las tarjetas junto a categorías, estamentos y conceptos muestran el texto y la fuente canónicos. Controles `glosario_definicion_y_fuente_exactas` y `ficha_glosario_asignaciones_limitacion_y_fuente_exactas`; capturas `02b_` y `08b_`. |
| Conceptos propios | **Cumple** | Persona-mes, «No informa / No tiene», estamento estimado, trayectoria D-15 y asignaciones especiales tienen tarjetas donde la interfaz los utiliza. |
| Conexión normativa futura | **Cumple** | Las entradas conectadas muestran el placeholder no interactivo «Marco normativo · módulo en desarrollo». |
| Términos sin entrada canónica | **Declarados, sin definición inventada** | Jefatura, Alcalde, Otro, Honorarios como estamento publicado y No clasificable quedan sin tarjeta propia y se listan como pendientes en el artefacto del glosario. |
| Microtextos anteriores | **No son fuente pública** | `MICROTEXTOS_EXPLICATIVOS_v1.md` no alimenta la interfaz ni se copia al paquete; fue reemplazado como ruta de contenido por el glosario aprobado. |

### SC-03 — `estamento_estimado` conforme a D-17 y mapeo v1.1

| Requisito | Estado | Evidencia |
|---|---|---|
| Nueva dimensión sin sobrescribir el estamento publicado | **Cumple** | Coexisten `estamento_estimado`, `estamento` y `estamento_raw`; el selector permite alternar entre publicado y estimado donde aplica. |
| Leyenda fija | **Cumple** | Toda vista que usa la dimensión muestra: «Estamento estimado por el proyecto a partir del cargo publicado; no corresponde a clasificación oficial del municipio.» |
| «No clasificable» visible | **Cumple** | Es una categoría visible en agregados y visualizaciones; no se oculta ni se convierte en cero. En detalle individual, el campo permanece vacío y `estado_clasificacion_estimada = no_clasificable`. |
| Uso individual permitido por D-17 | **Cumple** | Ficha y explorador pueden mostrar el valor con rótulo «estimado», sin incorporar género. |
| Honorarios con composición estimada | **Cumple** | Honorarios abre con estamento estimado y conserva disponible el publicado; las barras usan la dimensión estimada con su leyenda. |
| Cobertura Código del Trabajo | **Cumple** | 924 registros clasificados + 9 no clasificables = 933; 21 cargos clasificados + 4 no clasificables = 25. |
| Cobertura Honorarios | **Cumple** | 5.516 registros clasificados + 3.948 no clasificables = 9.464; 967 cargos clasificados + 659 no clasificables = 1.626. |
| Cobertura total del mapeo | **Cumple** | 6.440 registros clasificados + 3.957 no clasificables = 10.397. Planta y Contrata no se clasifican como «No clasificable». |
| Insumo v1.1 íntegro | **Cumple** | SHA-256 `99a357539d830d1e83f1c89b8e12ee50ea1f57a0576d538e8a8284dc1a571548`; cobertura y ausencia de duplicados controladas por el pipeline. |
| Nuevo artefacto | **Cumple** | `plataforma/data/composicion_estamento_estimado.json`, incluido en el paquete y en los controles de integridad. |

### SC-04 — Ficha y normalización conservadora de cargos

| Requisito | Estado | Evidencia |
|---|---|---|
| Antigüedad colapsable | **Cumple** | Primeros 6 años visibles; el resto se muestra solo al abrir el desplegable. |
| Aviso D-15 como nota desplegable | **Cumple** | «Convención de trayectoria D-15 — detalles» aparece en una línea, cerrada inicialmente, con el texto completo en su interior. |
| Normalización solo comparativa | **Cumple** | Mayúsculas, eliminación de puntuación y acentos y expansión de abreviaturas estándar; `cargo_funcion` se conserva sin modificaciones. |
| Tres estados de cargo | **Cumple** | «Cambio de cargo», «variante de escritura» —colapsada— y «posible variante, requiere verificación». No se usa similitud difusa ni fusión silenciosa. |
| Casos ejercitados | **Cumple** | `COT-2023-0008`, 2023-06: variante de escritura; `COT-2023-0001`, 2025-08: posible variante; `COT-2023-0005`, 2025-02: cambio de cargo. |
| Cobertura del análisis | **Cumple** | Sobre 22.938 registros proyectados: 1.068 primeros registros, 16.839 sin cambio, 551 variantes de escritura, 578 posibles variantes y 3.902 cambios de cargo. |
| Abreviaturas documentadas | **Cumple** | Tabla completa incluida en `BITACORA_CONSTRUCCION_MODULO_PERSONAL_v1.md`; ninguna equivalencia se aplica fuera de la comparación. |

### SC-05 — Iteración visual y analítica

| Requisito | Estado | Evidencia |
|---|---|---|
| Cuatro accesos cromáticos en portada | **Cumple** | Panel, Explorador, Vistas estamentales y Metodología tienen título, descriptor y cuatro fondos armónicos claramente diferenciados. Control `portada_cuatro_accesos_cromaticos`; captura `01b_portada_accesos_1440.png`. |
| Composición por categoría como jerarquía principal | **Cumple** | Dona del mes seleccionado y serie apilada de 36 meses, ambas controladas por dotación/bruto. Control `panel_dona_serie_y_cuatro_indicadores`. |
| Indicadores mensuales por categoría | **Cumple** | Cuatro tarjetas con dotación, gasto, promedio, mediana, bruta informada y «No informa». Los valores visibles calzan con el JSON para diciembre de 2025. Captura `02c_panel_indicadores_1440.png`. |
| Comparativa dentro de una categoría | **Cumple** | Gasto, promedio y mediana por estamento para la categoría y mes elegidos, sin barra general que mezcle vínculos. Planta y Honorarios fueron contrastados fila por fila con sus JSON. Capturas `02d_` y `02e_`. |
| Honorarios con estamento estimado | **Cumple** | Honorarios abre con la dimensión estimada, leyenda D-17 y «No clasificable» visible. |
| Nuevos agregados y controles | **Cumple** | Promedio y mediana excluyen ceros «No informa»; se conserva su conteo y se añade `registros_bruta_informada`. Estos controles estadísticos forman parte de la validación vigente de 77/77, que también cubre glosario, D-17, D-15 y asignaciones. |
| Cambio de mes | **Cumple** | El selector cambia de diciembre de 2025 a enero de 2023 y actualiza dona, indicadores y comparativa. |

### SC-06 — Diferenciación real de las tarjetas de acceso

| Requisito | Estado | Evidencia |
|---|---|---|
| Croma pastel presente y armonía | **Cumple** | Los cuatro fondos usan OKLCH con luminosidad 0,90 y croma 0,09; las familias son azul-verde, verde, ámbar y violeta. |
| Refuerzo no cromático | **Cumple** | Cada tarjeta tiene franja superior de 7 px y chip de icono con acento pleno. Control `portada_tarjetas_contraste_aa_y_refuerzo_no_cromatico`. |
| Contraste AA de texto | **Cumple** | Panel 11,83:1; Explorador 11,72:1; Vistas estamentales 11,24:1; Metodología 10,94:1. Todos superan 4,5:1. |
| Capturas para revisión | **Cumple** | `01b_portada_accesos_1440.png` y `01c_portada_accesos_375.png`, revisadas visualmente. |

### SC-07 — Identidad visual de selectores y botón de definición

| Requisito | Estado | Evidencia |
|---|---|---|
| Pestañas con la paleta de `Charts.tsx` | **Cumple** | Cada enlace recibe `--category-color` desde `COLORS`; inactiva al 30 % con blanco, hover al 40 %, activa al 48 % y borde pleno. Control `pestanas_categoria_paleta_charts_y_contraste_aa`. |
| Contraste AA de pestañas | **Cumple** | Planta activa 5,39:1; Contrata inactiva/activa 9,89:1/7,40:1; Código del Trabajo inactivo/activo 10,71:1/8,48:1; Honorarios inactivo/activo 10,94:1/8,74:1. |
| Píldora neutra uniforme | **Cumple** | Mes, métrica, categoría, año y clasificación comparten fondo neutro, radio 999 px y selector interno transparente. Control `selectores_periodo_metrica_pildora_neutra_uniforme`. |
| Botón predeterminado solo «¡» | **Cumple** | Área mínima 44 × 44 px, `aria-label` conservado y sin la palabra «Definir». Control `glosario_simbolo_y_leyenda_global_unica`. |
| Leyenda global única | **Cumple** | Una sola nota en el pie: «El símbolo ¡ abre una tarjeta con la definición del término y su fuente normativa.». |
| Excepciones con texto | **Cumple** | «Sobre la estimación» conserva icono y etiqueta; también se mantienen las demás etiquetas descriptivas. Control `glosario_excepcion_conserva_icono_y_texto`. |
| Capturas para revisión | **Cumple** | `04b_pestanas_categorias_1440.png` y `04c_pestanas_categorias_375.png`, revisadas visualmente. |
| Navegación superior con la paleta de portada | **Cumple** | Los cuatro accesos reutilizan azul-verde, verde, ámbar y violeta, con fondo pastel, franja de 3 px, icono de acento y estado activo diferenciado. Control `navegacion_superior_paleta_portada_y_contraste_aa`. |
| Contraste AA de navegación | **Cumple** | Inactivos: Panel 11,83:1; Explorador 11,72:1; Vistas 11,24:1; Metodología 10,94:1. Activos: 9,55:1; 9,54:1; 9,03:1; 8,83:1, respectivamente. |
| Capturas de navegación | **Cumple** | `00b_navegacion_superior_1440.png` y `00c_navegacion_superior_375.png`, revisadas visualmente; fila en escritorio y apilado legible en móvil. |

## 4. Verificación funcional de las vistas

| Vista o función | Resultado | Evidencia |
|---|---|---|
| Portada | Aprobada | Titulares de diciembre 2025, advertencias, cuatro accesos cromáticos, tarjetas canónicas y explicación D-15. `01_portada_1440.png`, `01_portada_375.png` y `01b_portada_accesos_1440.png`. |
| Panel general | Aprobado | Dona mensual, serie por categoría de 36 meses, selector dotación/bruto, cuatro indicadores por vínculo, comparativa estamental acotada, género y horas. `02_panel_*.png` y `02b_` a `02e_`. |
| Explorador | Aprobado | 50 filas por página, 22.940 registros, paginación, filtros, limpieza, mediana, ausencias, exportación, estamento estimado rotulado y enlaces a fichas. `03_explorador_*.png`. |
| Planta | Aprobada | 4.927 registros acumulados, 126 en diciembre 2025, selectores de métrica y estamento, horas desagregadas y fuentes. `04_planta_*.png`. |
| Contrata | Aprobada | 7.616 registros acumulados, 223 en diciembre 2025, selectores de métrica y estamento, horas desagregadas y fuentes. `05_contrata_*.png`. |
| Código del Trabajo | Aprobada | 933 registros acumulados, 36 en diciembre 2025, composición publicada/estimada, horas sin desagregar y desvinculación. `06_codigo_trabajo_*.png`. |
| Honorarios | Aprobada con límite documental | 9.464 registros acumulados, 323 en diciembre 2025, composición por estamento estimado con leyenda, «No publica» horas; tipo de pago, cuotas y estados de informes. PDF no duplicado. `07_honorarios_*.png`. |
| Ficha de Planta | Aprobada | 36 meses, 22 publicados, 14 ausencias exactas, septiembre 2024 presente, antigüedad colapsable, nota D-15, tarjeta canónica, fuente y versión alterna de noviembre 2024 visible. `08_ficha_planta_*.png` y `08b_ficha_glosario_1440.png`. |
| Ficha de Código del Trabajo | Aprobada | 36 meses, 7 publicados, 29 ausencias, estamento estimado rotulado y versión alterna de mayo 2025 con ambos IDs visibles. `09_ficha_codigo_*.png`. |
| Metodología | Aprobada | Pipeline, 77/77 controles, ausencias, no reconciliación D-15, inventario, ocho documentos enlazados —incluido el glosario—, formatos, atribución D-18 y licencias D-16: código MIT y datos derivados CC BY 4.0. `10_metodologia_*.png`. |

## 5. Pruebas de interacción y datos

| Prueba | Resultado medido |
|---|---|
| Fuente con botón Cerrar | Aprobada |
| Fuente con Escape | Aprobada |
| Fuente con backdrop | Aprobada |
| CSV fuente | HTTP 200; SHA-256 descargado idéntico al mostrado |
| Selector de métrica | Dotación ↔ remuneración bruta en panel y vistas estamentales |
| Selector de estamento | Publicado ↔ estimado donde existe mapeo; Honorarios abre con estimado |
| Tooltip apilado | Segmento bajo el cursor con estamento, valor y porcentaje de su barra |
| Antigüedad | 6 años iniciales y resto en desplegable |
| Nota D-15 | Cerrada inicialmente; texto completo disponible al desplegar |
| Normalización de cargo | Los tres estados y sus casos de ejemplo verificados; cargo publicado intacto |
| Paginación | Página 1 → 2 → 1 |
| Filtros combinados | 2025 + Planta + Administrativo + cargo «a»: 453 resultados, igual al cálculo independiente sobre `explorador_2025.json` |
| Exportación del filtro | 453 filas; nombre `personal_coronel_filtrado_2025-01_2025-12.csv`; sin género ni derivados de nombre; incluye campos D-15 |
| Limpiar filtros | Conserva Planta y recupera 4.927 registros; restaura género agregado |
| Privacidad con filtro individual | «No calculable» y explicación visible |
| Rango invertido | Aviso explícito y estado vacío, sin datos ficticios |
| Honorarios | «No publica» en horas extra |
| Enlace a ficha | Href válido con `HashRouter`; ficha habilitada y cargada bajo demanda |
| Ficha PLT-2023-0032 | 22 períodos, 14 ausencias exactas, 1 alterna; JSON HTTP 200 y campos D-15 presentes |
| Ficha COT-2023-0015 | 7 períodos, 29 ausencias, 1 alterna; ID seleccionado y alterno visibles |
| Fuentes secundarias | Cuatro accesos de Honorarios; identificadores con 36 archivos; cinco fuentes en tabla metodológica |
| Tarjetas del glosario | Definición y fuente canónicas exactas; enlace al glosario y placeholder «módulo en desarrollo» verificados |
| Documentos enlazados | Ocho documentos con HTTP 200 y contenido no vacío, incluido el glosario canónico; el borrador de microtextos no se publica |

## 6. Accesibilidad, adaptación y ejecución

- Se conservaron y revisaron 35 capturas de la verificación vigente: diez rutas a **1440 × 1000** y **375 × 812** píxeles, más detalles de navegación superior, versión alterna, glosario, accesos, pestañas, indicadores, comparativas y asignaciones decodificadas.
- Las diez rutas también se midieron a **768 × 900** y **1024 × 900** píxeles.
- En los 40 cruces ruta/ancho no hubo desplazamiento horizontal del documento; solo las tablas pueden desplazarse internamente. Las pestañas se envuelven en varias filas cuando el ancho lo requiere.
- El menú móvil abre y navega correctamente.
- El foco de teclado es visible: contorno sólido de 3 px en el control ejercitado.
- El diálogo de fuente es operable con teclado y tiene tres mecanismos de cierre.
- Los contrastes de texto medidos en navegación, tarjetas y pestañas cumplen AA; los botones «¡» tienen área mínima de 44 × 44 px y nombre accesible.
- Resultado final: **0 errores de consola, 0 errores de ejecución, 0 solicitudes fallidas y 0 respuestas HTTP fallidas**.

## 7. Paquete y rendimiento

| Medida | Resultado |
|---|---:|
| Registros canónicos en agregados | 22.940 |
| Registros seleccionados para trayectorias | 22.938 |
| Versiones alternas preservadas | 2 |
| Fichas habilitadas | 1.068; 0 colisiones |
| JSON raíz en `dist/data/`, incluido `meta.json` | 19 |
| Fichas JSON / total JSON | 1.068 / 1.087 |
| Entradas hash en `meta.json` | 18; excluye correctamente la autorreferencia |
| Hashes de fichas | 1.068 válidos mediante `fichas_estado.json` |
| CSV fuente en `dist/fuentes/` | 144; hashes de originales y copias válidos |
| Controles de agregados | 77/77 aprobados |
| Controles de navegador | 132/132 aprobados |
| Carga inicial codificada | 5.920.334 bytes |
| Solicitudes iniciales | 17 |
| Detalles anuales precargados en portada | 0 |
| Detalle anual bajo demanda | 71.114.899 bytes en tres JSON |
| Chunk principal | 811,22 kB; advertencia no bloqueante de Vite |
| `.nojekyll` | Presente |
| Verificación de paquete | APROBADO |

## 8. Pendientes que impiden declarar aceptación total

1. **Decidir una distribución viable para los informes archivados de Honorarios.** El paquete actual no duplica 2,36 GB de PDF; ofrece metadatos y URL original cuando existe, no un enlace local al respaldo.
2. **Realizar, si se exige evidencia de usabilidad, la prueba cronometrada con un tercero.** Las pruebas automatizadas no equivalen a ese ensayo.
3. **Revisar las 16 advertencias de vulnerabilidades npm antes del despliegue.** No se aplicó una actualización forzada.
4. **Publicar y probar expresamente en GitHub Pages cuando se autorice el despliegue.** Esta verificación es local y no afirma que el sitio esté en línea.

La Compuerta 1 ya no es un pendiente: la validación sobre la proyección D-15 fue aprobada y las fichas están habilitadas. SC-02 está cumplida con el glosario canónico; solo cinco términos sin entrada aprobada quedan declarados como pendientes de contenido, sin definiciones improvisadas.


## 9. Encargo 2026-11-18 — asignaciones, licencia y tonos

| Requisito | Estado | Evidencia |
|---|---|---|
| Decodificar conceptos en ficha y explorador | **Cumple** | Cada ocurrencia muestra código y nombre oficial; raw visible en fila separada. 13.475 registros completos y 61.548 ocurrencias decodificadas. Capturas `08c_` y `03b_`. |
| Conservar orden, duplicados y raw | **Cumple** | `(39)(11)(10)(08)(07)(06)(04)(04)` conserva dos «(04) Bono de subrogación». Controles de pipeline y navegador. |
| Declarar anomalías sin decodificar | **Cumple** | `PLT-202301-95B4374AC0`, raw `-4`, muestra «Código sin decodificar» y nota de formato; no se infiere significado. `03c_explorador_asignacion_anomala_1440.png`. |
| Publicar índice y trazabilidad | **Cumple** | `asignaciones_indice.json`: 394 conceptos, fuentes CPLT, SHA del insumo, cobertura y anomalía. Ruta real documentada: `documentación/04_Personal_y_Remuneraciones/asignaciones_indice.json`. |
| Glosario y limitación de montos | **Cumple** | 16 entradas aprobadas. La tarjeta reproduce definición y fuente exactas, incluida la imposibilidad de separar montos por concepto. |
| Exportación CSV | **Cumple** | Arreglo serializado como JSON con escape CSV; columna presente y ausencia de `[object Object]` verificada. |
| Corrección de atribución D-18 | **Cumple** | Fuente municipal MU068 y producto Portal de Transparencia Trazable diferenciados; no aparece la nomenclatura incorrecta anterior. |
| Licencias D-16 | **Cumple** | Código MIT; JSON/CSV derivados CC BY 4.0 con atribución al proyecto; datos originales públicos por Ley 20.285. `meta.licencias`, Metodología y `ausencias.json = declarada_D16` coinciden. |
| Selectores estamentales más vivos | **Cumple** | Mezclas 30/40/48 % sobre la paleta D-20. Activos: 5,39:1 a 8,74:1; todos AA. `04b_pestanas_categorias_1440.png` y `04c_pestanas_categorias_375.png`. |
| Regresión completa | **Cumple** | 77/77 agregados; 132/132 navegador; paquete APROBADO con 1.087 JSON y 144 CSV; cero errores y desbordes. |
| Despliegue | **No ejecutado** | Verificación local del paquete estático, sin publicación externa. |
