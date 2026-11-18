# Especificación de módulo — Personal y Remuneraciones (v1)

**Proyecto:** Portal de Transparencia Trazable — Municipalidad de Coronel
**Fecha:** 15 de noviembre de 2026
**Estado:** propuesta para revisión en chat de coordinación; al aprobarse, es el encargo del chat de construcción.
**Datos base:** maestros canónicos `canonico_v1.0.0` — Planta, Contrata, Código del Trabajo y Honorarios 2023-2025 (22.940 registros, trazabilidad SHA-256 por fila).

---

## 0. Brújula del producto

> **Toda cifra mostrada se puede perseguir hasta su documento fuente, y toda ausencia se declara en vez de esconderse.**

Si una vista no puede sostener esa promesa, no entra a la beta. De ella se derivan cinco principios obligatorios:

1. **Trazabilidad clickeable.** Toda cifra agregada enlaza al detalle que la compone; todo registro individual muestra su fuente (archivo, período, fila, SHA-256).
2. **Ausencias declaradas.** Lo que no se publicó, no cuadró o no existe se muestra rotulado como ausencia. Nunca se interpola ni se promedia para disimular.
3. **Eje temporal por defecto.** Tenemos 36 meses estructurados; el portal oficial muestra fotos aisladas. Toda vista que pueda ser serie, es serie (2023-01 a 2025-12).
4. **Transversalidad.** Los filtros operan sobre el universo completo de personal; las subcategorías estamentales son puntos de entrada, no silos.
5. **Privacidad por diseño.** Los datos individuales mostrados son exclusivamente los que el municipio ya publica por obligación legal. Las variables derivadas propias (género inferido) solo se publican agregadas (D-14).

## 1. Arquitectura técnica de referencia

- Sitio **estático** (desplegable en GitHub Pages): HTML/JS sin backend.
- Los datos se sirven como **JSON agregados precalculados** por un pipeline reproducible desde los maestros canónicos (sección 5). La página nunca recalcula desde el detalle completo, salvo el explorador (ver 3.3).
- Todo agregado JSON incluye metadatos: `generado_desde` (versión de canónico), `fecha_generacion`, y conteos que permiten verificar contra la validación final.

## 2. Mapa de navegación

```
Inicio (portada del portal)
 └── Personal y Remuneraciones (portada de módulo)          [2.1]
      ├── Panel general de la institución                    [2.2]
      ├── Explorador transversal de personal                 [2.3]
      ├── Vistas estamentales (Planta | Contrata | Código del Trabajo | Honorarios)  [2.4]
      │    └── Ficha individual de trabajador                [2.5]
      └── Metodología y fuentes                              [2.6]
```

## 2.1 Portada del módulo

**Propósito:** orientar antes de mostrar números.

Contenido:
- Qué es esta información, qué obligación legal la exige (art. 34 y 36 Ley 18.575; IGTA Res. Ex. N°80/2026) y de dónde sale (portal de transparencia municipal, 168 archivos mensuales 2023-2025).
- Qué hicimos con ella: unificación en base relacional, saneamiento documentado, trazabilidad por fila.
- **Advertencias visibles desde el inicio** (no escondidas en un footer): género como variable inferida solo agregada; campos "No informa" de la fuente mostrados como tales; qué períodos o subcategorías tienen ausencias.
- Tres o cuatro cifras titulares del último período (dotación total, gasto bruto del mes, horas extra del mes) con enlace directo al panel.

**Pregunta que responde:** "¿qué estoy viendo y por qué puedo confiar en ello?"

## 2.2 Panel general de la institución

**Propósito:** radiografía de la dotación completa, sin distinción de estamento como barrera.

Vistas:
- **Dotación total por mes** (serie 36 meses, todas las categorías apiladas: Planta / Contrata / Código del Trabajo / Honorarios).
- **Gasto bruto mensual total** por categoría (serie).
- **Composición del último mes:** distribución por categoría y por estamento (barras).
- **Composición por género (agregada)** por categoría, con la leyenda D-14 (ver 4.2).
- **Horas extra del sistema:** horas y monto por mes, por categoría (solo donde la fuente las publica — ver 6).

**Preguntas que responde:** ¿cuánta gente trabaja para el municipio y cómo evoluciona? ¿Cuánto cuesta la dotación al mes? ¿Cómo se compone?

## 2.3 Explorador transversal de personal

**Propósito:** la vista que el portal oficial no puede dar: filtrar el universo completo.

- Tabla de registros persona-mes con filtros combinables: período (rango), categoría, **estamento** (la categorización funcional publicada: disponible en Planta y Contrata desde el CSV, en Código del Trabajo desde el maestro manual, constante en Honorarios), cargo (búsqueda de texto), rango de remuneración bruta, rango de horas extra, tipo de término (indefinido / fecha / no informa).
- Todo filtro actualiza también un mini-panel de agregados del subconjunto filtrado (conteo, gasto bruto, mediana, % género agregado con leyenda).
- Cada fila enlaza a la ficha individual [2.5] y a su fuente.
- Exportación del subconjunto filtrado a CSV, con las columnas de trazabilidad incluidas (coherente con D-05: datos abiertos estructurados).

**Preguntas que responde:** ¿quiénes ganan sobre X en la categoría Y? ¿Cuántas personas hicieron más de N horas extra en tal trimestre? ¿Cuántos contratos son a plazo fijo vs indefinidos?

**Nota de escala:** ~23.000 registros persona-mes es manejable en cliente como JSON particionado por año (≈ 3 archivos), sin backend.

## 2.4 Vistas estamentales

Cuatro entradas (Planta, Contrata, Código del Trabajo, Honorarios), misma plantilla, contenido adaptado a lo que cada fuente efectivamente publica:

- **Panel del estamento:** dotación por mes, gasto bruto por mes, composición por estamento y por género agregado, distribución de remuneraciones (histograma o rangos), antigüedad (fecha de inicio).
- **Horas extra (donde aplica):** Planta y Contrata traen desagregación diurna/nocturna/festiva en horas y monto; Código del Trabajo trae monto y horas sin desagregar; Honorarios no publica horas extra y la vista debe decirlo explícitamente.
- **Específicos de Honorarios:** tipo de pago, número de cuotas, y enlace al **informe de funciones archivado** cuando exista en nuestro respaldo (D-06); cuando el informe no exista o el enlace esté caído, se muestra su estado documentado ("eliminado en fuente", "suspendido en fuente", "sin URL publicada") — eso es fiscalización visible, no un error nuestro.
- **Específicos de Código del Trabajo:** monto de desvinculación cuando corresponda.
- Lista filtrable del estamento (misma mecánica del explorador, prefiltrada).

**Preguntas que responde:** ¿cómo evoluciona cada tipo de vínculo? ¿Cuánto del gasto de personal es honorarios vs planta? ¿Dónde se concentran las horas extra?

## 2.5 Ficha individual de trabajador

**La pieza distintiva del módulo.** Acceso desde cualquier lista.

- Encabezado: nombre (tal como lo publica la fuente), categoría(s) en que aparece, cargo(s), estamento.
- **Trayectoria mensual 2023-2025:** línea de tiempo con remuneración bruta por mes, marcadores de cambio de cargo, entradas y salidas, meses con horas extra.
- Detalle por mes expandible: todos los campos publicados (líquida, viáticos, bonos, adicionales, desglose de horas extra), cada uno con su `_raw` disponible y la referencia de fuente (archivo, fila, SHA-256).
- **No muestra género** (D-14). No muestra nada que la fuente no publique.

**Preguntas que responde:** ¿esta persona aparece y desaparece mes a mes (contratación intermitente)? ¿Cómo evolucionó su remuneración? ¿En qué meses hizo horas extra y cuántas?

**Requisito previo (bloqueante de datos):** `id_trabajador` se heredó del maestro manual y el propio diccionario advierte que "no implica unicidad global validada". Antes de construir esta vista, el pipeline debe ejecutar una **validación de unicidad persona-período** (una persona no puede tener dos fichas distintas ni una ficha que mezcle dos personas) y documentar colisiones. Sin esa validación aprobada, la ficha individual no se publica.

## 2.6 Metodología y fuentes

- Descripción del pipeline (12 pasos), versión del esquema, enlace a diccionario de datos y bitácora.
- Inventario de fuentes con estado; registro de hallazgos relevantes para el usuario (no el técnico completo).
- Ausencias declaradas del módulo (sección 6).
- Cómo citar/reutilizar los datos (licencia y formatos).

## 3. Reglas de visualización de datos

### 3.1 Montos y ceros
- CLP con separador de miles, sin decimales, en las vistas; el `_raw` siempre accesible.
- **Cero significa "la fuente no informa / no tiene", no necesariamente cero real** (regla del canónico: `0 si fuente no informa/no tiene`). Toda vista que sume o promedie montos debe indicar cuántos registros "no informan" quedaron dentro. Considerar mostrar mediana además de promedio por esta razón.

### 3.2 Género (regla D-14)
- Solo agregado (porcentajes por categoría/estamento/período), **nunca** en ficha individual ni como filtro del explorador.
- Leyenda fija en toda vista que lo use: *"Composición por género inferida a partir del nombre con revisión manual; no corresponde a dato declarado por las personas ni publicado por el municipio. Se muestra solo de forma agregada."*

### 3.3 Ausencias
- Meses sin archivo publicado: se muestran como ausencia rotulada en las series (hueco visible con nota), nunca como cero ni interpolados.
- Documentos en cuarentena o información no recuperable: rotulados con su estado y causa.

### 3.4 Trazabilidad visible
- Cada panel lleva un enlace "¿De dónde sale este dato?" que abre la fuente: nombre de archivo, período, fila(s), SHA-256 y enlace al portal oficial de origen.

## 4. Contrato de datos (agregados a precalcular)

Pipeline Python desde los maestros canónicos hacia `plataforma/data/` (nombres tentativos):

| Artefacto | Contenido | Clave |
|---|---|---|
| `meta.json` | versión canónico, fecha de generación, conteos verificables | — |
| `panel_general_mensual.json` | dotación y gasto bruto por período × categoría | periodo, categoria |
| `composicion_estamento.json` | dotación por período × categoría × estamento | periodo, categoria, estamento |
| `composicion_genero_agregada.json` | % género por período × categoría (solo agregado) | periodo, categoria |
| `horas_extra_mensual.json` | horas y montos por período × categoría × tipo | periodo, categoria, tipo |
| `explorador_{2023,2024,2025}.json` | detalle persona-mes para el explorador (campos públicos + trazabilidad) | registro_id |
| `fichas/<id_trabajador>.json` | trayectoria mensual individual (generado tras validación de unicidad) | id_trabajador |
| `ausencias.json` | períodos/categorías sin dato, con causa | periodo, categoria |
| `fuentes.json` | inventario de archivos con estado y hash | fuente_sha256 |

Todo artefacto debe poder regenerarse con un solo comando y calzar con los conteos de `VALIDACION_FINAL_v1` de la categoría.

## 5. Ausencias y limitaciones conocidas del módulo

1. **No existe unidad/departamento organizacional en la fuente.** El portal municipal no publica a qué dirección o departamento pertenece cada persona. La categorización disponible y plenamente construible es por **estamento** (campo presente en las cuatro categorías). La dimensión departamental queda como ausencia declarada con tres salidas posibles: (a) esperar al módulo de estructura organizacional y cruzar por cargo (diferido); (b) derivación heurística desde `cargo_funcion` (frágil, requeriría leyenda de "clasificación derivada"); (c) solicitar la desagregación vía transparencia pasiva (candidato a la lista TP).
2. **Honorarios no publica horas extra** y Código del Trabajo no las desagrega: las vistas comparativas de horas extra deben rotular esa asimetría.
3. **Autoridades 2023 no publicadas** (categoría aparte, pendiente TP-05): el panel general cubre dotación funcionaria, no autoridades electas.
4. **"No informa / No tiene" de la fuente** se preserva como categoría visible, no se limpia.

## 6. Criterios de aceptación de la beta del módulo

- [ ] Las 5 vistas existen y cada cifra enlaza a su fuente.
- [ ] Un tercero responde en menos de 5 minutos: gasto en horas extra por categoría y año; evolución de dotación; trayectoria de una persona dada; composición de género agregada.
- [ ] Todas las ausencias conocidas (sección 5) están rotuladas en la interfaz.
- [ ] Leyenda D-14 presente en toda vista con género; ninguna ficha individual muestra género.
- [ ] Conteos de la interfaz calzan con `VALIDACION_FINAL_v1` (22.940 registros, por categoría).
- [ ] Sitio estático desplegable en GitHub Pages sin backend; pipeline reproducible con un comando.

## 7. Fuera de alcance (v1 del módulo)

- Cruce con presupuesto (partida de personal vs dotación): requiere el módulo presupuestario; se diseña en la integración, no aquí.
- Informes de funciones de honorarios como contenido legible (hoy solo se enlaza el respaldo con su estado).
- Actualización automática mensual (la beta es una fotografía 2023-2025; la cadencia de actualización es decisión posterior).
- Filtro por departamento/unidad organizacional (ver 5.1; la categorización por estamento sí está incluida).

## 8. Reutilización como plantilla

Esta especificación es la plantilla de todo módulo futuro: brújula → mapa de navegación → vistas con preguntas que responden → reglas de visualización → contrato de datos → ausencias declaradas → criterios de aceptación → fuera de alcance.
