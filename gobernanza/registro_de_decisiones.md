# Registro de decisiones del proyecto

**Portal de Transparencia Trazable — Municipalidad de Coronel**
Memoria de decisiones tomadas en el chat de coordinación general. Cada entrada: fecha, decisión, fundamentación y estado.

---

## D-01 · 2026-11-14 — Gobernanza por chats especializados
**Decisión**: el proyecto se organiza en un chat de coordinación general (ideas, criterios, diseño de prompts, evaluación) y chats específicos por fase/tarea que ejecutan y reportan.
**Fundamentación**: mantener limpio el contexto de coordinación; entregables consolidados en un único workspace compartido.
**Estado**: vigente.

## D-02 · 2026-11-14 — Orden de fases
**Decisión**: secuencia de trabajo: (1) marco normativo → (2a) saneamiento y documentación del dataset de personal → (2) diagnóstico de brecha del portal de Coronel → (3) modelo de datos y categorías piloto → (4) pipeline de datos → (5) plataforma → (6) deploy en GitHub.
**Fundamentación**: la matriz normativa define la especificación de dato; el diagnóstico mide la brecha contra ella; el diseño se ancla en ambos.
**Estado**: vigente. Fase 1 entregada (14-11-2026); Fase 2a en ejecución.

## D-03 · 2026-11-14 — Alcance del universo institucional: solo municipalidad (beta)
**Decisión**: la beta cubre únicamente a la Municipalidad de Coronel como órgano. No se cubren corporaciones ni entidades satélites; se enlazan y se marcan como "cobertura pendiente".
**Fundamentación**: cubrirlas duplica el universo de datos y frena el piloto. Matiz jurisdiccional: educación en Coronel ya es **servicio traspasado (SLEP)**, por lo que no pertenece al universo de TA municipal (órgano distinto); una expansión futura consideraría **solo salud**, si sigue administrada por corporación municipal. Consecuencia: la desagregación presupuestaria del art. 78 IGTA aplica en Coronel solo para salud y cementerios.
**Estado**: vigente. Revisar al definir el alcance de la v2.

## D-04 · 2026-11-14 — Dataset "Personal y Remuneraciones" como implementación de referencia
**Decisión**: el dataset ya construido (maestros 2023-2025 con género curado, IDs y trazabilidad a CSV fuente) se adopta como implementación de referencia: su diccionario de datos y bitácora de transformaciones serán la plantilla replicable para futuras categorías.
**Fundamentación**: el trabajo manual ya realizado conoce los errores reales del portal (tipeo, duplicados, archivos corruptos); documentarlo como protocolo lo hace reproducible y auditable.
**Estado**: vigente. En ejecución vía Fase 2a.

## D-05 · 2026-11-14 — Datos abiertos estructurados como piso obligatorio interno
**Decisión**: el portal piloto adopta CSV/datos estructurados como requisito mínimo interno, aunque la IGTA (art. 115 g) lo califica solo como buena práctica.
**Fundamentación**: es la única vía para comparabilidad, trazabilidad automatizada y fiscalización por terceros (hallazgo H9 de la Fase 1).
**Estado**: vigente.

## D-06 · 2026-11-14 — Archivo preventivo de informes de funciones (honorarios)
**Decisión**: descargar y archivar con manifiesto (sha256, fecha, estado) los PDFs de funciones de trabajadores a honorarios enlazados en Dropbox desde los CSVs del portal.
**Fundamentación**: riesgo de pudrición de enlaces; los enlaces rotos detectados son además evidencia de brecha de disponibilidad.
**Estado**: vigente. En ejecución vía Fase 2a (tarea 7).

## D-07 · 2026-11-14 — Esquema canónico v1.0.0 y criterio de período por contenido
**Decisión**: se adopta el esquema canónico `canonico_v1.0.0` (snake_case en español, núcleo común + específicos por estamento, campos `_raw` preservados, trazabilidad archivo/ruta/fila/SHA-256 por registro). El período de cada registro se toma siempre de `Año`/`Mes` **del contenido**, nunca del nombre del archivo. No se deduplican pares persona-período con valores o fuentes distintos; se documentan. Las hojas analíticas heredadas no se reutilizan (H-007); los agregados se recalculan.
**Fundamentación**: resultados verificados de la Fase 2a — 22.940 registros vinculados 100 % a fuente, 0 diferencias numéricas contra CSV, 48 controles aprobados; las anomalías de nombres de archivo del publicador (H-002, H-003) demuestran que el nombre no es fuente confiable de período.
**Estado**: vigente. Plantilla replicable de 12 pasos documentada en la bitácora de la categoría.

## D-08 · 2026-11-14 — Protocolo de verificación de disponibilidad: ningún "no disponible" sin evidencia explícita
**Decisión**: antes de clasificar un enlace o documento publicado como "no disponible" (y usarlo como hallazgo de brecha), se exige: (a) campaña de reintentos con backoff (mínimo 3 intentos espaciados); (b) clasificación del fallo por señal explícita del servidor (p.ej. título "File Deleted" de Dropbox = eliminado; "Link Temporarily Disabled" = suspendido), nunca inferida de una respuesta HTML genérica HTTP 200; (c) conservación de la evidencia (URL original y efectiva, código, título, fecha, SHA-256 si aplica).
**Fundamentación**: en la Fase 2a, 4.853 de 5.166 enlaces clasificados inicialmente como no recuperables eran recuperables: Dropbox alterna respuestas PDF/HTML para la misma URL (con `dl=1` y con ambos agentes de usuario), y tratar el HTML transitorio como fallo definitivo infló el hallazgo. Confundir "no pudimos descargar" con "no está publicado" destruiría la credibilidad del proyecto — la brecha debe ser real y demostrable.
**Estado**: vigente. Aplica a toda descarga externa futura (contratos, actas, planillas de otras categorías).

## D-09 · 2026-11-14 — Estrategia de transparencia pasiva: solicitar solo con vacíos confirmados
**Decisión**: los requerimientos al municipio vía Ley 20.285 se difieren hasta tener el desarrollo más avanzado y los vacíos confirmados. Se mantiene lista viva en `gobernanza/solicitudes_tp_pendientes.md`, donde cada ítem acumula su hallazgo origen, evidencia y justificativo normativo desde ya. Las solicitudes mismas se documentarán como ejercicio (plazos, respuesta, calidad) — insumo para evaluar la transparencia pasiva municipal.
**Fundamentación**: solicitar prematuramente gasta capital político y puede alertar al publicador; además varios hallazgos requieren agotar verificaciones previas (Wayback Machine, re-verificación de enlaces, búsqueda interna del nomenclátor).
**Estado**: vigente. Lista iniciada con TP-01 a TP-06 el 14-11-2026.

## D-10 · 2026-11-14 — Política de tolerancia por redondeo de origen (BEP) y ESP como tipo documental separado
**Decisión**: (a) los BEP de gastos se aceptan al canónico si cumplen: totales impresos 100 % + aritmética ≥99 % + todas sus diferencias jerárquicas ≤2 M$, con anexo permanente de diferencias (`ANEXO_DIFERENCIAS_JERARQUICAS_BEP_v1.csv`); cualquier diferencia mayor mantiene el documento en cuarentena. (b) Los archivos "ESP" se procesan como tipo documental propio **Estado Presupuestario** (11 métricas CLP en gastos, 9 en ingresos), validados contra el clasificador presupuestario, nunca contra el plan de cuentas municipal; los ESP de ingresos permanecen en cuarentena por descuadre sistemático del total impreso de "saldo por percibir" en los 35 documentos — inconsistencia de origen, no tolerada ni corregida.
**Fundamentación**: la distribución completa de diferencias jerárquicas (921×1 M$, 45×2 M$, 4×3 M$, 5 masivas en la v2 republicada) y la verificación visual 10/10 confirmaron el redondeo de origen del sistema CGR como causa dominante; la tolerancia se aplica con evidencia previa, no por conveniencia. El descuadre de ESP-ingresos es sistemático (35/35) y de una sola métrica: patrón de inconsistencia del publicador que se documenta como hallazgo, no se normaliza.
**Estado**: vigente para la tolerancia BEP y el tipo documental ESP. La cuarentena automática de ESP de ingresos por el descuadre de saldo por percibir queda reemplazada por D-13; no es una licencia general para relajar umbrales.

## D-13 · 2026-11-15 — Regla de agregación del saldo por percibir en ESP de ingresos (cuenta 15) y política de rehabilitación condicionada
**Decisión**: cada ESP de ingresos se rehabilita solo si reproduce individualmente tres condiciones: (1) las ocho métricas distintas de `saldo_por_percibir_clp` calzan entre total impreso y suma de subtítulos; (2) `total_saldo_por_percibir_oficial = total_vigente_mes − total_percibido`; (3) `total_saldo_por_percibir_oficial − saldo_por_percibir_suma_detalle = vigente_mes_cuenta_15 − percibido_cuenta_15`. El documento que no reproduzca las tres permanece en cuarentena. No se modifica ninguna cifra impresa, incluidos los ceros de la cuenta 15. El canónico conserva por separado `total_saldo_por_percibir_oficial_clp` y `saldo_por_percibir_suma_detalle_clp`, su diferencia y trazabilidad; las visualizaciones futuras deben explicar la diferencia, no ocultarla. Las series de deltas mantienen separados ambos totales, no interpolan julio de 2025 ni saltan ese corte en agosto.
**Fundamentación**: `MEMO_DESCUADRE_ESP_INGRESOS_v1.md` descartó partida ausente, signo, confusión subtotal/total y redondeo; la evidencia impresa y visual mostró que el total DEUDORES PRESUPUESTARIOS incorpora la cuenta 15 por vigente menos percibido aunque su saldo de detalle esté impreso en cero. El control `ESP_2023-2025_controles_D13_v1.csv` extendió la prueba a los 35 documentos: 35/35 reprodujeron las tres condiciones y fueron rehabilitados; 0 permanecen en cuarentena por esta causa.
**Estado**: vigente. TP-18 queda descartada porque el mecanismo está explicado con evidencia reproducible y no subsiste un vacío que requiera transparencia pasiva.

## D-11 · 2026-11-15 — Orden de módulos de la plataforma y placeholders activos
**Decisión**: el primer módulo de la plataforma es **Personal y Remuneraciones**, seguido por **Información Presupuestaria**. Los módulos futuros (potestades y marco normativo; estructura organizacional y atribuciones; transferencias de fondos; trámites ante el organismo; Juntas de Vecinos Ley 21.146) aparecen desde la beta con estado "en desarrollo", pero ningún placeholder es una lápida vacía: debe indicar qué preguntas responderá, qué fuente usará y qué falta. Cada módulo nuevo nace con su ficha de especificación (plantilla: `diseño/MODULO_PERSONAL_Y_REMUNERACIONES_v1.md`).
**Fundamentación**: personal y presupuesto son las dos categorías con canónico maduro (22.940 y 43.728 registros respectivamente); el resto requiere su propia fase de datos. La especificación del módulo de personal define además la brújula de producto: toda cifra perseguible hasta su fuente y toda ausencia declarada.
**Estado**: vigente, **modificada el 17-11-2026**: el orden pasa a ser Personal y Remuneraciones → **Potestades y marco normativo + Estructura organizacional, facultades, funciones y atribuciones** (módulos combinados o secuenciales, a definir en su especificación) → Información Presupuestaria. Fundamento de la modificación: el módulo de personal evidenció que la validación de cargos, la dimensión departamental y la conexión cargos-actividades dependen de insumos normativos y organizacionales (acto de planta, manuales de funciones — TP-19); esos módulos entregan el contexto que los demás necesitan. Además se incorpora un nuevo chat especializado de **desarrollo general** (portada del portal, presentación de módulos, ajustes estéticos globales y despliegue de betas), bajo D-01.

## D-14 · 2026-11-15 — Género inferido: solo agregado, nunca individual
**Decisión**: la variable `genero` (inferida por nombre con revisión manual, no publicada por el municipio) se muestra exclusivamente como indicador agregado (porcentajes por categoría/estamento/período). Nunca aparece en la ficha individual del trabajador ni como filtro del explorador. Toda vista que la use lleva leyenda fija aclaratoria de su carácter inferido y agregado.
**Fundamentación**: es un dato derivado propio con margen de error, sobre personas identificables; publicarlo individualizado agregaría un dato personal que la fuente no publica. Con la Ley 21.719 vigente desde 01-12-2026, la privacidad por diseño es un argumento del proyecto, no una limitación.
**Estado**: vigente.

## D-15 · 2026-11-17 — Regla de selección para trayectoria individual ante colisiones persona-período
**Decisión**: dentro de una colisión `categoria + id_trabajador + periodo`, si existe exactamente una versión cuyo período declarado (contenido, conforme a D-07) coincide con el período nominal de su archivo, esa versión alimenta la trayectoria individual; las demás se rotulan `version_alterna` con motivo `periodo_contenido_distinto_de_periodo_nominal_archivo` y permanecen íntegramente disponibles y visibles en la ficha ("Otra publicación del mismo período"). Si hay cero o más de una versión coincidente, la colisión no se resuelve automáticamente (sin desempate por monto, orden de fila ni posterioridad presumida); solo cabe excepción con evidencia formal de rectificación, justificada registro por registro. La regla opera solo sobre la proyección de trayectoria: no modifica maestros, agregados ni totales; la interfaz declara que la suma de fichas no reconcilia con los agregados. La identidad transversal entre categorías (56 advertencias, 24 grupos nombre+período) queda fuera de alcance.
**Fundamentación**: `documentación/04_Personal_y_Remuneraciones/ANALISIS_COLISIONES_UNICIDAD_v1.md` demostró que las dos colisiones (COT-2023-0015/2025-05 y PLT-2023-0032/2024-11) comparten un patrón estructural objetivo: una fila nativa del período y una única fila fuera de período anexada al final del archivo del mes siguiente. El barrido completo confirmó que no existen más casos análogos dentro de categoría. La alternativa "la publicación posterior es corrección oficial" se descartó como regla automática por carecer de evidencia formal.
**Estado**: vigente. Autoriza al chat de construcción a implementar la proyección de trayectoria y repetir la validación de unicidad para habilitar la ficha individual.

## D-17 · 2026-11-17 — Clasificación estamental inferida como variable derivada condicionada
**Decisión**: se crea una variable derivada `estamento_estimado` para los registros cuyo estamento publicado no describe la naturaleza funcional del cargo (Honorarios, constante; Código del Trabajo, desagregación poco fiel). Condiciones obligatorias: (a) nunca sobrescribe el `estamento` publicado — ambas dimensiones coexisten con selector en la interfaz; (b) tabla de mapeo explícita cargo → estamento estimado, documentada y revisable, con "No clasificable" como resultado legítimo y visible (prohibido forzar cobertura); (c) reporte de cobertura y revisión manual de muestra antes de aprobar el mapeo; (d) leyenda fija en toda vista que lo use: clasificación estimada por el proyecto a partir del cargo publicado, no declarada por el municipio; (e) a diferencia del género (D-14), puede mostrarse a nivel individual con rótulo "estimado", porque clasifica un texto público del cargo y no un atributo personal. La implementación en la plataforma solo procede tras la aprobación del mapeo en este chat.
**Fundamentación**: habilita la comparación funcional transversal (p.ej. profesionales por honorarios vs planta), una de las preguntas fiscalizadoras centrales; sin ella, 9.464 registros de honorarios son un agregado indiferenciado. Las condiciones replican el estándar probado con el género inferido (revisión manual, transparencia del método, leyenda).
**Estado**: vigente. Mapeo **aprobado por el propietario el 17-11-2026 con una enmienda única**: `INFORMATICO` (y variantes de tipeo, p.ej. `INFOMATICO`) se reclasifica de "No clasificable" a **Técnico** por revisión manual del propietario. Se mantiene la metodología sin relajar; no se crea pseudo-estamento para roles de programa (monitores, talleristas, gestores) — su eventual tratamiento sería una dimensión ortogonal ("grupo funcional") a evaluar después de la normalización de cargos.

## D-16 · 2026-11-17 — Licencias de publicación
**Decisión**: el código de la plataforma se publica bajo licencia **MIT**; los datos agregados y artefactos derivados (JSON, CSV exportables) bajo **CC-BY 4.0** con atribución al proyecto. Los datos de origen son públicos por ley (Ley 20.285); nuestra capa de valor es la estructuración y trazabilidad. La licencia se declara explícitamente en la interfaz (hoy figura "no declarada").
**Fundamentación**: coherente con D-05 (datos abiertos estructurados) y con la finalidad de bien público del proyecto; MIT y CC-BY son las licencias estándar de máxima reutilización con atribución.
**Estado**: vigente.

## D-18 · 2026-11-17 — "Transparencia Trazable" como autoconcepto; prohibido el rótulo ambiguo "Transparencia activa"
**Decisión**: el proyecto se autodenomina **"Portal de Transparencia Trazable"** en portada, encabezados y metadatos. Ninguna vista puede titularse solo "Transparencia activa 2023-2025" o similar: "transparencia activa" es el mecanismo legal de origen de los datos, no el nombre del producto, y usarlo como rótulo confunde fuente con producto. La fórmula obligatoria es: producto = Transparencia Trazable; fuente = declarada como "datos de transparencia activa del portal municipal" con su base legal. Se agrega el concepto al glosario canónico.
**Fundamentación**: diferenciación conceptual frente al portal oficial y frente al concepto jurídico; además es la marca del "cómo debería ser" que el proyecto demuestra.
**Estado**: vigente. Aplica a la portada del módulo de personal (corregir encabezado), al shell del chat de desarrollo general y a todo módulo futuro.

## D-19 · 2026-11-17 — Estrategia de despliegue por hitos
**Decisión**: el primer despliegue público (v0.1) es una **herramienta de revisión en círculo cerrado** (propietario y evaluadores directos): no requiere prueba cronometrada con terceros ni campaña de difusión; el acceso no se restringe técnicamente (probabilidad de descubrimiento baja sin propagación). Las betas posteriores incorporan, antes de cualquier versión con fines de propagación: prueba de usabilidad cronometrada (criterio de éxito D-12), revisión de vulnerabilidades npm y endurecimiento pendiente del checklist.
**Fundamentación**: el valor inmediato del despliegue es la revisión real sobre el entorno de producción (GitHub Pages), no la difusión; diferir los controles de propagación a betas posteriores no compromete nada porque el contenido ya es íntegro y trazable.
**Estado**: vigente.

## D-20 · 2026-11-17 — Tema Coronel (C ajustado) como sistema visual definitivo
**Decisión**: se adopta el **Tema C ajustado** evaluado en SC-08 para el shell global y los módulos presentes y futuros: superficie papel cálido `#fdfbf6`, tinta `#182634`, azul institucional profundo y apagado `#143d6d` en estructura y encabezados, y cobre `#c98a1e` reservado para trazabilidad (fuentes, hashes y orígenes documentales). El texto pequeño de trazabilidad sobre fondo claro usa el derivado accesible `#8a5a0b`; sobre azul no se usa cobre pequeño. El verde se reserva para verificación aprobada, sin alterar los colores funcionales ya existentes en categorías y gráficos. Se conservan Source Sans 3 y Source Serif 4. Se retiran el Tema B, el conmutador provisional y los atributos de muestra; los parámetros `tema=b|c` quedan inertes.

**Cierre y ajuste del 18-11-2026**: el azul `#143d6d` reemplaza al `#155bb5` de la muestra. El chrome de familia adopta encabezado sticky de 64 px, marca compacta, navegación en píldoras con mínimo táctil de 44 px, héroe de portada como banda baja y pie marino de dos líneas lógicas con licencias D-16. Se incorporan texturas SVG en línea, monocromas y no interactivas: mar, peces y pesca en el encabezado; carbón, minería e industria en el pie. Opacidad 8 % en escritorio y 6 % en móvil, con detalle simplificado en pantallas pequeñas.
**Fundamentación**: la comparativa SC-08 dejó ocho evidencias en dos vistas y dos anchos, con 59/59 controles en desarrollo y 7/7 en producción. El propietario comparó ambas direcciones, eligió C y posteriormente aprobó su ajuste como identidad Coronel y chrome compartido para futuros portales. El cobre como señal específica de procedencia refuerza la brújula del proyecto sin convertir el acento visual en decoración indiscriminada.
**Estado**: vigente; implementación final verificada el 18-11-2026. La aplicación global se realiza mediante variables y reglas del shell, sin modificar datos, lógica ni componentes internos de Personal. Esta decisión no autoriza despliegue, remoto ni commits.

---

### Pendientes de decisión
- [ ] Definición del criterio de éxito del piloto ("qué sería que funcione") — D-12; borrador de preguntas fiscalizadoras planteado en coordinación 14-11-2026, parcialmente incorporado a la especificación del módulo de personal.
- [x] ~~Categorías piloto~~ → resuelto como orden de módulos en D-11 (15-11-2026).
- [ ] Solicitud vía Ley de Transparencia de la categoría autoridades 2023 (ejercicio documentado) — pendiente tras verificación en Wayback Machine (Fase 2a).

### Backlog técnico (no requiere decisión, requiere ejecución oportuna)
- [ ] **Fuentes locales del módulo Normativa y Estructura Organizacional** (copiar al workspace al abrir su fase de datos; no re-descargar lo ya obtenido por el chat del marco normativo): `C:\Users\bsilq\Documents\04Proytectos Varios\Datos Municipio de Coronel\Dasboard_Coronel\02_Potestades_y_Marco_Normativo` · `...\03_Estructura_Organica_y_Facultades_Funciones_y_Atribuciones\Facultades, funciones y atribuciones de sus unidades u órganos internos` · `...\01_Actos_y_Documentos_Publicados_en_el_Diario_Oficial`. Idea de diseño registrada: módulo combinado con subcategorías (Marco Normativo; Potestades/competencias/facultades/atribuciones/tareas; Actos DO; Organigrama; Facultades de unidades) y portada con **grafo de nodos** (unidades, normas-articulado, cargos) con visibilidad conmutable de grupos y aristas — a definir en su especificación.
- [ ] **Saneamiento del plan de cuentas municipal** (`datos crudos/clasificadores_cgr/Plan_de_Cuentas_Sector_Municipal.xlsx` y `plan_municipal.json`): reparar filas Excel 145-148 (N3 que no anida en N2) y 506-514 (N2_COD no numérico "2152103001_des"); tipar todos los códigos como texto (hoy algunos se leen como flotante, p.ej. `1.151304e+06`); regenerar `plan_municipal.json` limpio. **Bloqueante para**: la futura capa de estado financiero (balance de comprobación). No afecta al pipeline BEP/ESP actual, que usa el clasificador presupuestario (verificado íntegro: 451 rutas, 0 anomalías, 14-11-2026). Detectado por el propietario, verificado en coordinación.
