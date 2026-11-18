# Bitácora de construcción — Módulo Personal y Remuneraciones

**Versión documental:** 1.5.0  
**Fecha de cierre:** 2026-11-18  
**Canónico de entrada:** `canonico_v1.0.0`  
**Pipeline:** `modulo_personal_v1.4.0`  
**Estado:** construcción estática verificada; SC-01 a SC-07 implementados, asignaciones especiales decodificadas en ficha y explorador, atribución D-18 y licencias D-16 sincronizadas, y pestañas estamentales reforzadas sin alterar la paleta funcional D-20.

## 1. Alcance y resultado

Se construyó el módulo desde los cuatro maestros canónicos de Planta, Contrata, Código del Trabajo y Honorarios, sin modificar maestros ni CSV originales. La distribución contiene portada, panel general, explorador transversal, vistas estamentales, ficha individual y metodología.

El resultado es un sitio React + TypeScript compilado con Vite como archivos estáticos. No utiliza backend, base de datos, API de aplicación, autenticación ni recursos tipográficos externos. La navegación usa `HashRouter` y el paquete incluye `.nojekyll`, por lo que puede publicarse como contenido estático en GitHub Pages. No se ejecutó un despliegue público.

**Resultado de controles de esta iteración:**

- **77/77** controles de agregados, estadísticas, proyección D-15, segmentos, cobertura D-17, normalización de cargos, glosario y asignaciones aprobados.
- **132/132** controles automatizados de navegador, interacción, contraste AA, accesibilidad básica, asignaciones, licencias y documentos aprobados.
- Verificación del paquete **APROBADA**: 19 JSON raíz y 1.068 fichas JSON, **1.087 JSON** en total, con hashes válidos; 144 CSV originales y copias con SHA-256 coincidente.
- Cero errores de consola, errores de ejecución, solicitudes fallidas y respuestas HTTP fallidas durante la prueba final.
- 35 capturas de la verificación vigente: diez rutas a 1440 px y 375 px, detalles de versión alterna y glosario, y capturas específicas de navegación superior, accesos, pestañas, indicadores, comparativas y asignaciones decodificadas. Las diez rutas también se midieron a 768 px y 1024 px. Se revisaron visualmente las asignaciones normales y anómalas, la ficha y las pestañas a 1440 y 375 px.
- Se publican 1.068 trayectorias individuales. La proyección contiene 22.938 registros seleccionados y dos versiones alternas, con cero colisiones persona-período sin resolver.

La evidencia se conserva en `documentación/plataforma/evidencia/`, en particular `verificacion_navegador.json`, `verificacion_paquete.json` y las capturas PNG.

## 2. Insumos vinculantes y decisiones aplicadas

Se aplicaron la especificación del módulo, el diccionario de datos, la validación final, la bitácora de transformaciones, el registro de hallazgos, el mapeo aprobado v1.1, el índice CPLT de asignaciones y las decisiones D-05, D-07, D-11, D-14, D-15, D-16, D-17, D-18 y D-20.

| Decisión | Aplicación en la construcción |
|---|---|
| D-05, datos abiertos | JSON agregado, detalle anual JSON, fichas JSON, exportación CSV del subconjunto y copia de los 144 CSV fuente. |
| D-07, esquema canónico | Los agregados se calculan desde las 22.940 filas de los maestros `MAESTRO_*_canonico_v1.xlsx`; las versiones alternas se conservan y no se deduplican en los agregados. |
| D-11, orden de módulos | Alcance limitado a Personal y Remuneraciones; no se incorporan presupuesto ni autoridades electas. |
| D-14, género agregado | Solo agregados por período, categoría y estamento; nunca en filas, filtros, exportación individual ni ficha. |
| D-15, proyección de trayectoria | Selección por coincidencia período-contenido/archivo nominal; `version_alterna` visible; sin desempate por monto, orden ni posterioridad; agregados intactos y no reconciliación declarada. |
| D-16, licencias | Código de plataforma bajo MIT; JSON y CSV derivados bajo CC BY 4.0 con atribución al proyecto. No se atribuyen esas licencias al municipio ni a los datos originales. |
| D-17, estamento estimado | Dimensión separada basada en `universo_cargos_d17.csv` v1.1; nunca sobrescribe `estamento` ni `estamento_raw`; «No clasificable» permanece visible. |
| D-18, identidad y fuente | El producto se cita como Portal de Transparencia Trazable; la fuente se describe como datos de transparencia activa del portal municipal, organismo MU068. |
| D-20, paleta funcional | Se conservaron los colores base de `Charts.tsx`; solo aumentó la mezcla de las pestañas para hacerlos más visibles. |

Las licencias de reutilización están **declaradas conforme a D-16** en Metodología, `meta.licencias` y la entrada `licencia_reutilizacion` de `ausencias.json`. Los datos originales siguen identificados como datos públicos obtenidos por transparencia activa conforme a la Ley 20.285.

## 3. Arquitectura y comando reproducible

Desde la raíz del proyecto:

```bash
python "scripts/build_modulo_personal.py"
```

El comando lee los maestros y documentos de validación, normaliza el catálogo publicado, une el mapeo D-17 por `categoria + cargo_funcion`, proyecta las trayectorias conforme a D-15, valida unicidad, analiza cambios de cargo, calcula agregados y estadísticas, extrae el glosario canónico, genera fichas, contrasta los totales, copia los CSV fuente y replica la documentación pública en `plataforma/docs/`.

Para compilar la interfaz:

```bash
npm --prefix "plataforma" run build
```

El script `plataforma/scripts/copy-static.mjs` copia `data/`, `fuentes/` y `docs/` a `plataforma/dist/` y crea `.nojekyll`. El manifiesto `meta.json` contiene tamaño y SHA-256 de los otros **18 JSON raíz**; se excluye a sí mismo para evitar una autorreferencia inválida. `fichas_estado.json` contiene tamaño y SHA-256 de cada una de las 1.068 fichas. En total se distribuyen **1.087 artefactos JSON**.

### Artefactos raíz generados

- `meta.json`
- `panel_general_mensual.json`
- `composicion_estamento.json`
- `composicion_estamento_estimado.json`
- `composicion_genero_agregada.json`
- `horas_extra_mensual.json`
- `explorador_2023.json`, `explorador_2024.json`, `explorador_2025.json`
- `ausencias.json`
- `fuentes.json`
- `catalogo_estamentos.json`
- `validacion_unicidad.json`
- `fichas_estado.json`
- `resumen_estamental.json`
- `codigo_desvinculacion_mensual.json`
- `validacion_agregados.json`
- `glosario_definiciones.json`
- `asignaciones_indice.json`

Además se genera `plataforma/data/fichas/<id_trabajador>.json` para cada identificador de categoría. Cada ficha contiene los 36 meses, el registro seleccionado cuando existe, las ausencias explícitas, el análisis conservador de cargo, las asignaciones decodificadas y las versiones alternas íntegras.

Los tres archivos del explorador se serializan en JSON compacto. Sus tamaños en esta generación son 21.981.951, 24.091.720 y 25.041.228 bytes. Solo se descargan al entrar al explorador; la portada no los precarga. Las fichas se cargan individualmente bajo demanda.

## 4. Normalización previa del catálogo de estamento publicado

La normalización se ejecuta antes de cualquier agregado. La comparación usa Unicode normalizado, sin acentos y sin distinguir mayúsculas; el valor publicado se conserva en `estamento_raw`.

La lista cerrada resultante es: **Administrativo, Auxiliar, Profesional, Técnico, Directivo, Jefatura, Alcalde, Otro y Honorarios**.

Todos los valores observados correspondieron a una identidad canónica; no fue necesario sustituir variantes y no hubo correcciones silenciosas.

| Categoría | Valor observado → canónico | Registros |
|---|---|---:|
| Planta | Administrativo → Administrativo | 1.588 |
| Planta | Alcalde → Alcalde | 36 |
| Planta | Auxiliar → Auxiliar | 1.420 |
| Planta | Directivo → Directivo | 513 |
| Planta | Jefatura → Jefatura | 64 |
| Planta | Profesional → Profesional | 726 |
| Planta | Técnico → Técnico | 580 |
| Contrata | Administrativo → Administrativo | 3.197 |
| Contrata | Auxiliar → Auxiliar | 1.178 |
| Contrata | Profesional → Profesional | 1.773 |
| Contrata | Técnico → Técnico | 1.468 |
| Código del Trabajo | Administrativo → Administrativo | 858 |
| Código del Trabajo | Otro → Otro | 35 |
| Código del Trabajo | Profesional → Profesional | 6 |
| Código del Trabajo | Técnico → Técnico | 34 |
| Honorarios | Honorarios → Honorarios | 9.464 |

**Valores no mapeables:** 0. El detalle reutilizable está en `plataforma/data/catalogo_estamentos.json`.

## 5. Estamento estimado D-17, mapeo v1.1

**Insumo aprobado:** `trabajo/04_Personal_y_Remuneraciones/universo_cargos_d17.csv`  
**SHA-256:** `99a357539d830d1e83f1c89b8e12ee50ea1f57a0576d538e8a8284dc1a571548`  
**Filas:** 1.651; claves `categoria + cargo_funcion` duplicadas: 0.  
**Cobertura:** Código del Trabajo y Honorarios; no se clasifican Planta ni Contrata como «No clasificable».

La unión es exacta y `many_to_one`. Los campos `regla_estamento_estimado`, `origen_estamento_estimado` y `justificacion_estamento_estimado` se conservan en el detalle público. En las filas no clasificables, `estamento_estimado` permanece sin asignación y `estado_clasificacion_estimada = no_clasificable`; la etiqueta «No clasificable» se materializa al agregar y al rotular la interfaz.

| Categoría | Registros clasificados | No clasificables | Total | Cargos clasificados | Cargos no clasificables |
|---|---:|---:|---:|---:|---:|
| Código del Trabajo | 924 | 9 | 933 | 21 | 4 |
| Honorarios | 5.516 | 3.948 | 9.464 | 967 | 659 |
| **Total** | **6.440** | **3.957** | **10.397** | **988** | **663** |

La enmienda M01 fue comprobada: `INFORMATICO` e `INFOMATICO` se asignan a **Técnico**, con origen `revisión manual del propietario`.

Toda vista que usa esta dimensión presenta la leyenda fija:

> Estamento estimado por el proyecto a partir del cargo publicado; no corresponde a clasificación oficial del municipio.

En el panel general, el selector publicado/estimado aparece solo al comparar Código del Trabajo u Honorarios; Planta y Contrata permanecen en la dimensión publicada. En Honorarios, la dimensión estimada es la opción inicial tanto en la vista estamental como en la comparativa del panel; el estamento publicado sigue disponible. En explorador y ficha se muestra a nivel individual con el rótulo **«Estimado»**, incluida la categoría «No clasificable». El estamento publicado permanece visible e intacto.

## 6. Compuerta 1 y proyección D-15

El análisis independiente actualizado está en `VALIDACION_UNICIDAD_PERSONA_PERIODO_v1.md`. Se evaluaron 22.940 registros. La validación final se ejecuta sobre `categoria + id_trabajador + periodo` para las filas con `rol_trayectoria = canonica_trayectoria`, además de comprobar IDs vacíos, duplicidad de `registro_id` y consistencia de identificadores y nombres dentro de cada categoría.

D-15 selecciona una fila solo cuando existe exactamente una versión cuyo período de contenido coincide con el período nominal del archivo. La otra publicación conserva todos sus campos con `rol_trayectoria = version_alterna`, `version_alterna_de` y `motivo_version_alterna`. No se desempata por monto, orden de fila ni posterioridad presumida.

| Control | Resultado |
|---|---:|
| `registro_id` duplicados | 0 |
| `id_trabajador` vacíos | 0 |
| Colisiones originales `(id_trabajador, periodo)` | 2 |
| Colisiones resueltas por D-15 | 2 |
| Colisiones sin resolver en la proyección | 0 |
| Registros seleccionados para trayectorias | 22.938 |
| Versiones alternas preservadas | 2 |
| IDs asociados a varios nombres normalizados | 0 |
| Nombres con varios IDs dentro de una categoría | 0 |
| Nombres con IDs distintos entre categorías | 56; advertencia, sin unificación |

| ID y período | Selección para trayectoria | Versión alterna |
|---|---|---|
| `PLT-2023-0032`, 2024-11 | `PLT-202411-8247F5515D`, archivo nominal 2024-11 | `PLT-202411-3B54A1958D`, archivo nominal 2024-12 |
| `COT-2023-0015`, 2025-05 | `COT-202505-8DA800BA00`, archivo nominal 2025-05 | `COT-202505-9D0CE3F70A`, archivo nominal 2025-07 |

**Estado: APROBADA.** Se habilitan 1.068 fichas. Las cuatro filas involucradas en las colisiones originales permanecen incluidas en los agregados; solo dos quedan fuera de la proyección de trayectoria y se muestran como alternas. Los 56 aliases entre categorías se reportan como advertencia y no se unificaron.

La selección es una convención documental de visualización, no una declaración de cuál publicación es jurídicamente correcta. La interfaz declara que **la suma de fichas no reconcilia con los agregados**, porque estos conservan las 22.940 filas.

## 7. Validación de agregados y segmentos

| Categoría | Registros | IDs heredados | Bruto CLP | Líquido CLP |
|---|---:|---:|---:|---:|
| Planta | 4.927 | 178 | 10.797.372.125 | 8.196.431.255 |
| Contrata | 7.616 | 244 | 13.334.434.092 | 10.017.381.767 |
| Código del Trabajo | 933 | 53 | 1.128.969.662 | 866.746.415 |
| Honorarios | 9.464 | 593 | 8.747.261.374 | 7.519.192.800 |
| **Total** | **22.940** | **No sumable globalmente** | **34.008.037.253** | **26.599.752.237** |

También calzaron las horas: Planta 35.754 diurnas, 70.601 nocturnas y 0 festivas; Contrata 72.946 diurnas, 116.920 nocturnas y 0 festivas; Código del Trabajo 15.046 sin desagregar.

Los **77 controles** conservan las comprobaciones anteriores y añaden verificaciones estadísticas, de glosario y de asignaciones:

- Para panel, estamento publicado y estamento estimado, en cada `periodo × categoria × estamento`: reconciliación de `registros_bruta_informada + registros_bruta_no_informa = dotacion_registros`, y recálculo independiente de promedio y mediana sobre brutas mayores que cero.
- Integridad del glosario: 16 entradas únicas y aprobadas, con SHA-256 exacto del documento canónico.
- Integridad del índice de asignaciones: 394 conceptos, decodificación conservadora, preservación de códigos raw, duplicados y anomalías, y ausencia de montos individuales inventados.
- Se mantienen `suma(segmentos) = total de barra` para dotación, bruto y registros «No informa»; cobertura exacta D-17 v1.1; 1.651 filas de mapeo sin claves duplicadas; «No clasificable» visible; enmienda M01 y pruebas de normalización de cargos.

El resultado íntegro está en `plataforma/data/validacion_agregados.json`.

## 8. Reglas de visualización implementadas

### 8.1 Unidad de dotación

Toda dotación se presenta como **registros persona-mes**, no como personas únicas ni nómina deduplicada. Los IDs son identificadores heredados por categoría y no identidad global validada.

### 8.2 Montos, ceros, segmentos y estadísticas

Los montos se muestran en CLP con separador de miles y sin decimales; los campos `_raw` están disponibles en el detalle del explorador y de cada mes de la ficha. Promedio y mediana usan solo remuneraciones brutas mayores que cero; cuando no hay valores informados, el campo agregado es nulo y la interfaz declara «Sin datos».

Hay **3** remuneraciones brutas con cero canónico, todas en Código del Trabajo. Toda suma muestra cuántos registros con cero canónico incluye y explica que equivalen a «No informa / No tiene», no a un cero real. En las filas se muestra «No informa (0)».

La jerarquía principal del panel es la categoría de vínculo: una dona del mes seleccionado y una serie histórica apilada de 36 meses comparten el selector **Dotación / Remuneración bruta**. Los tooltips corresponden al segmento bajo el cursor e informan categoría o estamento, período, valor y porcentaje; en montos declaran el número de registros «No informa». Cuatro tarjetas por categoría presentan dotación, gasto bruto, promedio, mediana, registros informados y no informados, con fuente.

La comparativa estamental del mes se calcula **dentro de una sola categoría seleccionada** y presenta gasto total, promedio, mediana, bruta informada y «No informa» por estamento. Nunca mezcla categorías en una barra general. Planta y Contrata usan estamento publicado; Código del Trabajo permite publicado/estimado; Honorarios abre con estimado y mantiene la leyenda D-17 y «No clasificable».

Las vistas estamentales conservan sus barras apiladas por estamento y tooltips por segmento. El apilado es absoluto. El toggle «ver proporciones» era opcional y **no se incorporó**; no hay control sin función ni cambio de escala no declarado.

### 8.3 Género y privacidad

La leyenda fija aparece en toda vista con género:

> Composición por género inferida a partir del nombre con revisión manual; no corresponde a dato declarado por las personas ni publicado por el municipio. Se muestra solo de forma agregada.

`explorador_*.json` y `data/fichas/*.json` no contienen `genero`, `primer_nombre` ni `nombre_normalizado`. La tabla, los filtros, el detalle, el CSV exportado y la ficha tampoco contienen género ni variables individuales derivadas del nombre.

Con filtros de período, categoría y estamento, los porcentajes se calculan desde agregados precalculados. Si se añade cargo, monto, horas o tipo de término, la interfaz muestra **«No calculable»**: cruzar ese subconjunto con género exigiría exponer el atributo individual y vulneraría D-14.

### 8.4 Ausencias y trayectoria individual

Se rotulan la ausencia de unidad organizacional, la falta de horas extra en Honorarios, la ausencia de desagregación en Código del Trabajo, la exclusión de Autoridades 2023 y los estados de informes. Las cuatro categorías incluidas tienen 36 meses; no se crearon huecos ni valores interpolados en los agregados.

Cada ficha presenta los 36 meses de enero de 2023 a diciembre de 2025. Los meses sin fila para el ID y categoría se muestran como ausencia, sin imputación ni interpolación. El gráfico usa `connectNulls={false}` y también interrumpe la línea cuando el bruto es 0 canónico.

- `PLT-2023-0032`: 22 períodos publicados y 14 ausencias: 2023-08 a 2024-08, más 2024-12. Septiembre de 2024 está publicado.
- `COT-2023-0015`: 7 períodos publicados y 29 ausencias.

Las versiones alternas aparecen en **«Otra publicación del mismo período»**, con ID alterno, ID seleccionado, rol, motivo, montos, campos `_raw` y fuente. El antiguo banner D-15 fue reemplazado por una línea desplegable: **«Convención de trayectoria D-15 — detalles»**, con la convención y la no reconciliación dentro.

### 8.5 Antigüedad

Las vistas estamentales muestran inicialmente los primeros **6 años** de la lista de antigüedad. Si existen más, un desplegable nativo muestra el resto. No se imputan fechas ausentes. La prueba en Planta comprobó 6 años iniciales y 34 años tras desplegar.

## 9. Normalización conservadora de cargos SC-04

La normalización se calcula en `cargo_normalizado_proyecto` **solo para comparar**. Nunca sobrescribe `cargo_funcion`, no corrige ortografía, no usa similitud difusa y no unifica género gramatical.

**Secuencia:** normalización Unicode NFKC mediante la lectura de texto; mayúsculas; NFKD y eliminación de acentos; puntuación reemplazada por espacios; separación por tokens; expansión exacta de abreviaturas.

| Abreviatura o token | Expansión |
|---|---|
| ADM., ADM, ADMIN | ADMINISTRATIVO |
| DEPTO., DEPTO, DEPT | DEPARTAMENTO |
| OF., OF, OFIC | OFICINA |
| PROF., PROF | PROFESIONAL |
| COORD | COORDINACION |
| GAB | GABINETE |
| MUNIC, MUN | MUNICIPAL |
| RRHH | RECURSOS HUMANOS |

La comparación se hace contra el **período publicado anterior**, no contra un mes ausente. El primer registro queda como `primer_registro`.

| Estado | Regla | Presentación |
|---|---|---|
| `sin_cambio` | Texto original y normalizado idénticos | Sin marcador de cambio |
| `variante_escritura` | Normalizados idénticos, grafías distintas | Detalle colapsado con ambas grafías y normalización |
| `posible_variante` | Inclusión estricta de tokens y al menos un marcador de unidad añadido o retirado | «Posible variante, requiere verificación»; sin fusión |
| `cambio_cargo` | Normalizados distintos sin cumplir la frontera anterior | Marcador fuerte de cambio de cargo |

Marcadores de unidad usados en la frontera: `DEPARTAMENTO`, `OFICINA`, `DIRECCION`, `GABINETE`, `MUNICIPAL`, `CENTRO`, `PROGRAMA`, `CEMENTERIO` y `ALBERGUE`. La inclusión de tokens por sí sola no basta para declarar posible variante.

Conteos sobre los 22.938 registros seleccionados:

| Estado | Registros |
|---|---:|
| Primer registro | 1.068 |
| Sin cambio | 16.839 |
| Variante de escritura | 551 |
| Posible variante | 578 |
| Cambio de cargo | 3.902 |

Casos ejercitados en navegador:

- `COT-2023-0008`, 2023-06: variante por acento, con grafías originales conservadas.
- `COT-2023-0001`, 2025-08: `AUXILIAR DE SERVICIO CEMENTERIO` frente a `AUXILIAR DE SERVICIO`, posible variante que requiere verificación.
- `COT-2023-0005`, 2025-02: `MEDICO DIRECCIÓN DE TRANSITO` frente a `MEDICO PSICOTECNICO`, cambio de cargo.

## 10. SC-02 — tarjetas desde el glosario canónico

La fuente única es `diseño/GLOSARIO_DEFINICIONES_v1.md`, con **16 entradas aprobadas** y SHA-256 `dc75083029790500855baa7a1bebd6a4fde4bb304d77a4eec53c7582e85f44fc`. El pipeline extrae término, sección, definición, fuente, estado y conexión normativa sin reescribir el contenido, y genera `plataforma/data/glosario_definiciones.json`. El documento canónico se copia además a `plataforma/docs/GLOSARIO_DEFINICIONES_v1.md` y se enlaza desde Metodología.

Las tarjetas desplegables aparecen junto a categorías de vínculo, estamentos con entrada disponible y los conceptos persona-mes, «No informa / No tiene», estamento estimado y trayectoria D-15. Reproducen la definición y fuente exactas. Cuando existe conexión con el futuro módulo normativo, muestran el placeholder no interactivo **«Marco normativo · módulo en desarrollo»**.

No se redactaron definiciones normativas propias. **Jefatura, Alcalde, Otro, Honorarios como estamento publicado y No clasificable** no tienen entrada canónica individual: permanecen visibles como valores, pero sin tarjeta definitoria propia, y se declaran en `terminos_pendientes_sin_definicion`. La definición general de «Estamento» y de «Estamento estimado» sigue disponible donde corresponde.

El borrador anterior `documentación/plataforma/MICROTEXTOS_EXPLICATIVOS_v1.md` **no es fuente de la interfaz ni se copia al paquete público**. SC-02 queda implementada por la vía del glosario aprobado, no por aquel borrador.

### 10.1 SC-06 — diferenciación de las tarjetas de acceso

Las cuatro tarjetas usan fondos OKLCH con igual luminosidad (`0,90`) y croma (`0,09`), dentro del rango solicitado. Cada una incorpora una franja superior de 7 px y un chip de icono con el acento pleno correspondiente, de modo que la identificación no depende solo del fondo pastel.

| Acceso | Familia | Fondo | Acento | Contraste de texto medido |
|---|---|---|---|---:|
| Panel general | Azul-verde | `oklch(0.90 0.09 190)` | `oklch(0.52 0.18 190)` | 11,83:1 |
| Explorador transversal | Verde | `oklch(0.90 0.09 145)` | `oklch(0.52 0.18 145)` | 11,72:1 |
| Vistas estamentales | Ámbar | `oklch(0.90 0.09 75)` | `oklch(0.52 0.18 75)` | 11,24:1 |
| Metodología | Violeta | `oklch(0.90 0.09 305)` | `oklch(0.52 0.18 305)` | 10,94:1 |

Todos superan el mínimo AA de 4,5:1 para texto normal. Las capturas `01b_portada_accesos_1440.png` y `01c_portada_accesos_375.png` fueron revisadas visualmente.

### 10.2 SC-07 — pestañas, selectores e identidad del glosario

Las pestañas de categoría toman exactamente `COLORS` de `Charts.tsx`: Planta `#123c4a`, Contrata `#16756f`, Código del Trabajo `#bd6b2e` y Honorarios `#7c8794`. Tras el refuerzo cromático del encargo vigente, el estado inactivo mezcla 30 % del color con blanco; hover, 40 %; activo, 48 %, con borde del color pleno. Se mantuvo texto oscuro para garantizar contraste, en vez de imponer texto blanco sobre colores que no siempre lo permitirían.

Se midieron las cuatro pestañas activas, una por ruta, y las tres inactivas de Planta. Las razones fueron: Planta activa 5,39:1; Contrata inactiva/activa 9,89:1/7,40:1; Código del Trabajo inactivo/activo 10,71:1/8,48:1; Honorarios inactivo/activo 10,94:1/8,74:1. Todas cumplen AA. Las capturas `04b_pestanas_categorias_1440.png` y `04c_pestanas_categorias_375.png` muestran la distribución en una y dos filas, respectivamente.

Los selectores de mes, métrica, categoría, año y clasificación comparten una píldora neutra con fondo de superficie, radio `999px` y selector interno transparente. El color se reserva a las categorías. El foco visible se conserva en el grupo.

`GlossaryCard` muestra por defecto solo **«¡»**, en un área mínima de 44 × 44 px y con `aria-label="Definición de …"`. Las excepciones descriptivas conservan icono y texto, como «Sobre la estimación», «Unidad de conteo» y «Cómo contamos la dotación». Existe una única leyenda global en el pie: «El símbolo ¡ abre una tarjeta con la definición del término y su fuente normativa.». No se modificó el contenido canónico de las definiciones.

SC-07 fue exclusivamente visual. Los controles y metadatos se ampliaron después con las asignaciones y licencias descritas en la sección 15; la validación vigente es 77/77 con pipeline `modulo_personal_v1.4.0`.

### 10.3 Extensión de la paleta a la navegación superior

Los cuatro accesos de la navegación superior reutilizan los mismos tonos de las tarjetas de portada: azul-verde para Panel general, verde para Explorador, ámbar para Vistas estamentales y violeta para Metodología y fuentes. Cada enlace presenta fondo pastel, borde, franja superior de 3 px e icono con el acento pleno; el estado activo intensifica el fondo y el borde sin alterar la paleta.

| Acceso | Contraste inactivo | Contraste activo |
|---|---:|---:|
| Panel general | 11,83:1 | 9,55:1 |
| Explorador | 11,72:1 | 9,54:1 |
| Vistas estamentales | 11,24:1 | 9,03:1 |
| Metodología y fuentes | 10,94:1 | 8,83:1 |

Los ocho estados superan AA para texto normal. El control `navegacion_superior_paleta_portada_y_contraste_aa` verifica correspondencia cromática, diferenciación, franja y contraste. Las capturas `00b_navegacion_superior_1440.png` y `00c_navegacion_superior_375.png` fueron revisadas visualmente: en escritorio los accesos se muestran en una fila y en móvil se apilan sin pérdida de legibilidad.

Este ajuste es exclusivamente visual: no se modificaron datos, agregados, fuentes ni las reglas D-14, D-15 o D-17.

## 11. Trazabilidad y respaldo documental

Cada visualización de datos tiene acceso a su fuente directa o mediante su tabla desplegable. El diálogo informa archivo, período o períodos del contenido, filas CSV, número de registros, ruta original y SHA-256, con enlaces al CSV y al portal oficial MU068. Las filas del explorador y de las fichas incluyen además los valores `_raw`.

El artefacto estimado incluye la ruta y SHA-256 del mapeo D-17, su versión, leyenda y cobertura; sus segmentos conservan además la trazabilidad de las filas municipales que agregan. `meta.json` replica esos metadatos.

Se copiaron **144 CSV** a `plataforma/fuentes/`. El pipeline verifica que cada copia conserve exactamente el SHA-256 del original. La prueba de navegador descargó un CSV desde el diálogo y obtuvo HTTP 200 con coincidencia exacta entre el hash declarado y el recalculado. La verificación del paquete repitió el contraste de los 144 originales y copias.

Para Honorarios se conservaron los estados del manifiesto vigente:

| Estado | Registros |
|---|---:|
| Descargado y verificado en el respaldo del proyecto | 6.057 |
| Sin URL publicada | 3.094 |
| Enlace temporalmente deshabilitado | 186 |
| Archivo eliminado en fuente | 127 |

El respaldo tiene 5.991 PDF únicos y 2.360.241.736 bytes. **Esos 2,36 GB no se duplicaron dentro del sitio.** La interfaz muestra estado, ruta y SHA-256 cuando existen, y la URL publicada originalmente si está disponible, pero no presenta como activo un PDF local que no se distribuye.

## 12. Decisiones técnicas de interfaz

- React + TypeScript + Vite, compilación completamente estática.
- `HashRouter` para evitar dependencia de reglas de reescritura en GitHub Pages.
- Recharts para series y Lucide para iconografía; Source Sans 3 y Source Serif 4 se sirven localmente.
- JSON agregado para portada, panel, vistas estamentales y metodología; detalle anual bajo demanda solo en el explorador y un JSON por ficha al abrirla.
- Tooltip por segmento mediante el evento de la barra señalada; sin animación en las barras estamentales.
- Tablas con desplazamiento interno, sin desplazamiento horizontal del documento.
- Diálogo nativo de fuente, cerrable con botón, Escape y backdrop.
- Exportación CSV en UTF-8 con BOM, delimitador `;` y columnas de trazabilidad, D-15 y D-17.
- Cada gráfico tiene una tabla desplegable con sus datos y fuentes.
- Selectores con nombres accesibles y foco visible; nombre accesible explícito añadido al selector de año.
- Los enlaces del explorador abren fichas habilitadas; la ficha se limita al ID dentro de su categoría.

## 13. Desviaciones, límites y advertencias

| Tema | Situación y justificación |
|---|---|
| Reconciliación de fichas | **Límite deliberado de D-15, declarado.** Las fichas seleccionan 22.938 filas; los agregados conservan 22.940. Las dos alternas permanecen visibles. |
| Enlace al informe archivado de Honorarios | **Cumplimiento parcial.** Se publican estado, ruta, hash y URL original cuando existe, pero no el enlace a un PDF archivado dentro del sitio, debido a 2,36 GB de respaldo. |
| Género con filtros individuales | **Limitación deliberada para proteger D-14.** El porcentaje es «No calculable» al agregar cargo, monto, horas o término. |
| Cobertura del glosario | **SC-02 cumplida para las 16 entradas aprobadas.** Jefatura, Alcalde, Otro, Honorarios como estamento publicado y No clasificable quedan sin definición propia hasta que el glosario canónico las incorpore; no se improvisaron textos. |
| Número de vistas | El checklist original dice «5 vistas» y la especificación define además la portada. Se entregaron seis superficies: portada + secciones 2.2–2.6. |
| Toggle de proporciones | No incorporado; SC-01 lo define como opcional. Las barras son absolutas. |
| Prueba con tercero | No se ejecutó una prueba cronometrada de usabilidad con un tercero; los 132 controles automatizados no sustituyen ese ensayo. |
| Despliegue | El paquete está preparado para GitHub Pages, pero no se desplegó públicamente. |
| Rendimiento | La carga inicial medida fue 5.920.334 bytes codificados en 17 solicitudes. Vite advierte que el chunk principal, de 811,22 kB, supera su umbral de 500 kB; no impide el funcionamiento. El explorador descarga bajo demanda 71.114.899 bytes de detalle anual. |
| Dependencias | La revisión de vulnerabilidades npm sigue pendiente antes del despliegue; no se ejecutó una actualización forzada en esta iteración. |
| Licencia | Declarada conforme a D-16: código MIT y derivados CC BY 4.0; datos originales públicos por Ley 20.285, sin atribuir las licencias del proyecto al municipio. |

No se alteró ninguna decisión vinculante ni se resolvió por cuenta propia una colisión, ausencia o clasificación no mapeable. No hay desviaciones nuevas respecto de D-15, D-16, D-17, D-18 o D-20.

## 14. Evidencia y reproducción de la verificación

Con el build servido como sitio estático en el puerto 7101:

```bash
npm --prefix "plataforma" run preview -- --host 127.0.0.1 --port 7101
```

En otra terminal, desde `plataforma/`:

```bash
CHECK_DOCS=1 node "scripts/verify-modulo.mjs"
```

Desde la raíz, para verificar integridad del paquete:

```bash
node "plataforma/scripts/verify-package.mjs"
```

La verificación final registra **132/132 controles aprobados**. Incluye la navegación superior con la paleta de portada y contraste AA en estados activos e inactivos, los cuatro accesos cromáticos con contraste y refuerzo no cromático, pestañas activas e inactivas con la paleta canónica y contraste AA, píldoras neutras de selección, símbolo y leyenda global del glosario, dona y serie por categoría, cambio de mes y métrica, indicadores y comparativas contrastados con JSON, glosario exacto y placeholder normativo, trazabilidad y hash de CSV, cierre accesible, tooltips por segmento, «No informa», leyenda D-17, «No clasificable», antigüedad colapsada, nota D-15, tres estados de cargo, filtros con conteo independiente, exportación de 453 filas sin género y con asignaciones serializadas, decodificación normal y anómala, licencias D-16/D-18, paginación, ausencias, fichas, ocho documentos enlazados, cuatro anchos, menú móvil, foco visible, peso inicial y errores de red/consola.

El checklist de aceptación, ítem por ítem, está en `CHECKLIST_VERIFICACION_MODULO_PERSONAL_v1.md`. La aceptación total de la beta sigue condicionada por los límites documentados de PDF, la prueba con tercero no realizada, la revisión de dependencias y la ausencia de despliegue público. SC-02 ya no es una compuerta pendiente.


## 15. Cierre 2026-11-18 — asignaciones, licencias y selectores

### 15.1 Decodificación reproducible

El encargo indicó `datos/asignaciones_indice.json`, pero el insumo entregado se encuentra en `documentación/04_Personal_y_Remuneraciones/asignaciones_indice.json`. Se usó esa ruta real sin mover ni modificar el archivo; es una diferencia de ubicación documentada, no una compuerta de diseño.

El pipeline valida `schema_version = 1.0.0`, 394 conceptos, códigos únicos y nombres no vacíos. Publica `plataforma/data/asignaciones_indice.json` con metadatos y fuentes CPLT, SHA-256 del insumo, cobertura del módulo, limitación de montos y anomalías observadas. La plantilla oficial conserva SHA-256 `0e3ae33f0735a0f596741b639654cf73017e7dd9f61f08c11765b8491664ddd1`; el Oficio N.° 22003/2025, `2855abd88245a40f3092196c0f465f298b4575c1daddb4d3ff30c3c8bd977528`.

Cada registro público incorpora `asignaciones_decodificadas` sin alterar `asignaciones_especiales_raw`. Cada ocurrencia conserva `codigo`, `codigo_raw`, `nombre`, `estado` y `nota`. Se preservan orden y duplicados; no se corrigen grafías oficiales ni se infieren códigos desconocidos. Los conceptos se muestran como listas con código y nombre en explorador y ficha, incluidas las versiones alternas. El raw permanece en una fila separada.

| Cobertura | Resultado |
|---|---:|
| Conceptos oficiales publicados | 394 |
| Registros con algún código | 13.476 |
| Registros completamente decodificados | 13.475 |
| Ocurrencias decodificadas | 61.548 |
| Registros sin códigos | 9.464, todos Honorarios |
| Anomalías de origen | 1 registro / 1 ocurrencia |

La anomalía es `PLT-202301-95B4374AC0`, trabajador `PLT-2023-0010`, período 2023-01, Planta, raw `-4`, archivo `01_Planta_Enero_2023.csv`, fila CSV 11. La interfaz muestra «Código sin decodificar» y la nota de formato inválido; no inventa un nombre. En `PLT-2023-0032`, enero de 2023, el raw `(39)(11)(10)(08)(07)(06)(04)(04)` presenta dos veces «(04) Bono de subrogación».

El glosario canónico quedó con 16 entradas y SHA-256 `dc75083029790500855baa7a1bebd6a4fde4bb304d77a4eec53c7582e85f44fc`. La entrada «Asignaciones especiales» declara literalmente que la fuente publica los conceptos aplicables, no sus montos individuales, y que estos van incluidos en la remuneración bruta. La exportación CSV serializa el arreglo como JSON escapado; se comprobó que no produce `[object Object]`.

### 15.2 Atribución y licencias

Metodología diferencia fuente y producto según D-18. La fuente es la Municipalidad de Coronel, datos de transparencia activa del portal municipal, organismo MU068; el producto derivado es el Portal de Transparencia Trazable. Se eliminó la denominación incorrecta «Portal de Transparencia Activa MU068».

Según D-16, el código se ofrece bajo MIT y los datos agregados y artefactos derivados —JSON y CSV exportables— bajo CC BY 4.0 con atribución al proyecto. `ausencias.json` usa ahora `estado = declarada_D16`; ya no declara una ausencia de licencia. Ninguno de estos textos atribuye MIT o CC BY al municipio ni cambia la condición pública de los datos originales bajo la Ley 20.285.

### 15.3 Selectores y contraste

Las pestañas mantienen los colores base D-20 de `Charts.tsx`: Planta `#123c4a`, Contrata `#16756f`, Código del Trabajo `#bd6b2e` y Honorarios `#7c8794`. Las mezclas pasaron de 14/24/38 % a **30 % inactiva, 40 % hover y 48 % activa**; no fue necesario reducir el activo para cumplir AA. Contrastes activos medidos: Planta 5,39:1; Contrata 7,40:1; Código del Trabajo 8,48:1; Honorarios 8,74:1. Inactivos: 9,89:1 a 10,94:1.

Capturas revisadas: `08c_ficha_asignaciones_decodificadas_1440.png`, `03b_explorador_asignaciones_decodificadas_1440.png`, `03c_explorador_asignacion_anomala_1440.png`, `04b_pestanas_categorias_1440.png` y `04c_pestanas_categorias_375.png`.

### 15.4 Verificación final de la iteración

- Pipeline 1.4.0: **77/77 controles**, 22.940 registros y agregados canónicos intactos.
- Navegador: **132/132 controles**, incluidos ocho nuevos de índice, CSV, explorador, ficha, glosario y licencias.
- Paquete: **APROBADO**, 19 JSON raíz, 1.068 fichas, 1.087 JSON totales, 18 hashes raíz y 144 CSV válidos.
- Carga inicial: 5.920.334 bytes codificados en 17 solicitudes; detalle anual bajo demanda: 71.114.899 bytes en tres JSON.
- Cero errores de consola/ejecución/red y cero desbordes en los cuatro anchos.
- No se realizó despliegue público.
