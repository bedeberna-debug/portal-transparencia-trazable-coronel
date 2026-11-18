# Propuesta de mapeo para `estamento_estimado` (D-17)

**Versión:** v1 — propuesta para revisión del propietario.  
**Fecha:** 2026-11-17.  
**Estado:** no aprobada ni aplicada.  
**Compuerta:** este trabajo no modifica maestros canónicos, pipelines ni plataforma.

## 1. Objetivo y alcance

Se propone una clasificación funcional estimada para los valores de `cargo_funcion` de Honorarios y Código del Trabajo. El único insumo de decisión es el texto del cargo. No se utilizaron nombres de personas, identificadores, montos, honorarios ni trayectorias individuales.

Los destinos posibles son **Administrativo, Auxiliar, Profesional, Técnico, Directivo y Jefatura**. `No clasificable` expresa falta de evidencia textual y no integra la lista cerrada de estamentos. `Alcalde`, `Otro` y `Honorarios` no se usan como destinos.

La variable propuesta debe coexistir con el estamento publicado; no lo reemplaza ni corrige. Toda visualización futura debe declarar: **“Estamento estimado por el proyecto a partir del texto del cargo; no corresponde a una clasificación oficial del municipio.”**

## 2. Insumos y trazabilidad

- Honorarios: 9.464 registros y 1.626 cargos distintos.
- Código del Trabajo: 933 registros y 25 cargos distintos.
- Universo de trabajo: `trabajo/04_Personal_y_Remuneraciones/universo_cargos_d17.csv`.
- Catálogo cerrado: `plataforma/data/catalogo_estamentos.json`.

| Maestro de origen | SHA-256 verificado antes y después |
|---|---|
| Honorarios | `860d1fc0d005be9a3722451cef15f56dc79ff21b5c00734c8801a04e676d3bde` |
| Código del Trabajo | `c843d1759055b68c281f9d88886b28d67f5e072905d759228002ff1d8a21f6ea` |

## 3. Metodología

1. Se conserva cada par `categoria + cargo_funcion` exactamente como aparece en el universo extraído; no se fusionan variantes ni se corrige el texto publicado.
2. Para reconocer términos se crea solo en memoria una versión en mayúsculas, sin acentos ni puntuación. El CSV conserva siempre el cargo original.
3. Se aplican reglas deterministas en el orden indicado abajo. La precedencia evita, por ejemplo, que una coordinación técnica se clasifique como Técnico en vez de Jefatura.
4. Las faltas de ortografía se reconocen únicamente cuando el término funcional sigue siendo inequívoco; no se infiere una profesión desde una palabra dudosa.
5. Los textos genéricos, mixtos o ambiguos quedan `No clasificable`. No se persigue cobertura total.

| Regla | Destino | Criterio y límite |
|---|---|---|
| R00 | No clasificable | Apoyo administrativo combinado con monitoreo: función mixta. |
| R01 | Directivo | Dirección explícita; no acredita condición formal de directivo municipal. |
| R02 | Jefatura | Jefatura de departamento explícita. |
| R03 | Jefatura | Coordinación, supervisión o encargo de equipo explícito; no acredita jefatura formal. |
| R04 | Jefatura | Administración o subadministración del cementerio municipal. |
| R05 | Profesional | Profesión universitaria o condición profesional explícita. |
| R06 | Técnico | Título técnico, TENS, dibujo/topografía u operación especializada declarada. |
| R07 | Administrativo | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| R08 | Auxiliar | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| R97–R99 | No clasificable | Unidad/prestación sin rol, rol genérico o nivel funcional ambiguo. |

### Decisiones conservadoras relevantes

- `Monitor/a` de deportes, talleres o programas sociales no implica por sí solo Profesional, Técnico ni Auxiliar.
- `Gestor/a`, `asesor/a`, `apoyo` y `taller` sin especialidad de nivel tampoco se fuerzan.
- Diseñador, informático, prevencionista y educador social no se equiparan automáticamente a una profesión universitaria o técnica.
- Coordinadores y supervisores se proponen como Jefatura **funcional estimada**, sin afirmar jerarquía formal.
- Las cámaras y la operación audiovisual se proponen como Técnico por la operación especializada declarada; oficios como mecánico, gasfíter o carpintero se proponen como Auxiliar operativo.

## 4. Cobertura de la propuesta

| Categoría | Registros clasificados | Registros totales | % registros | Cargos clasificados | Cargos distintos | % cargos |
|---|---|---|---|---|---|---|
| Código del Trabajo | 924 | 933 | 99.04% | 21 | 25 | 84.00% |
| Honorarios | 5490 | 9464 | 58.01% | 965 | 1626 | 59.35% |

La cobertura de registros usa como numerador la suma de frecuencias de cargos clasificados. La cobertura de cargos usa valores distintos, sin ponderar. Ambas se recalcularon desde el CSV final.

### Distribución de registros clasificados por destino

| Categoría | Destino propuesto | Registros | Cargos distintos |
|---|---|---:|---:|
| Honorarios | Administrativo | 1075 | 206 |
| Honorarios | Auxiliar | 542 | 79 |
| Honorarios | Profesional | 2519 | 406 |
| Honorarios | Técnico | 747 | 141 |
| Honorarios | Directivo | 20 | 6 |
| Honorarios | Jefatura | 587 | 127 |
| Código del Trabajo | Administrativo | 112 | 8 |
| Código del Trabajo | Auxiliar | 716 | 4 |
| Código del Trabajo | Profesional | 7 | 4 |
| Código del Trabajo | Jefatura | 89 | 5 |

## 5. Muestra para revisión manual del propietario

### 5.1 Treinta mapeos clasificados, cinco por destino

Selección determinista por frecuencia descendente, con categoría y cargo como desempates. La muestra no constituye aprobación.

| Categoría | Cargo | Frecuencia | Destino | Regla |
|---|---|---|---|---|
| Código del Trabajo | SECRETARIA OFIC. CEMENTERIO MU | 72 | Administrativo | R07 |
| Honorarios | ENCUESTADOR REGISTRO SOCIAL DE HOGARES | 58 | Administrativo | R07 |
| Honorarios | APOYO ADMINISTRATIVO | 42 | Administrativo | R07 |
| Honorarios | APOYO ADM. DIRECCION DE TRANSITO | 39 | Administrativo | R07 |
| Honorarios | APOYO ADM. OMIL | 31 | Administrativo | R07 |
| Código del Trabajo | AUXILIAR DE SERVICIO | 535 | Auxiliar | R08 |
| Código del Trabajo | SALVAVIDAS | 99 | Auxiliar | R08 |
| Honorarios | MONITORA ALBERGUE | 77 | Auxiliar | R08 |
| Código del Trabajo | AUXILIAR DE SERVICIO CEMENTERIO | 70 | Auxiliar | R08 |
| Honorarios | MONITOR ALBERGUE | 40 | Auxiliar | R08 |
| Honorarios | PSICOLOGA CENTRO ANUN | 137 | Profesional | R05 |
| Honorarios | TRABAJADOR SOCIAL CENTRO ANUN | 101 | Profesional | R05 |
| Honorarios | PSICOLOGO CENTRO ANUN | 58 | Profesional | R05 |
| Honorarios | TRABAJADORA SOCIAL CASA DE LA SEGURIDAD | 44 | Profesional | R05 |
| Honorarios | APOYO PROFESIONAL SECPLAN | 40 | Profesional | R05 |
| Honorarios | TÉCNICO EN REHABILITACION CENTRO ANUN | 72 | Técnico | R06 |
| Honorarios | OPERADOR DE CAMARAS | 59 | Técnico | R06 |
| Honorarios | TÉCNICO EN REHABILITACIÓN CENTRO ANUN | 46 | Técnico | R06 |
| Honorarios | TÉCNICO EN ENFERMERIA ALBERGUE MUNICIPAL | 29 | Técnico | R06 |
| Honorarios | TOPOGRAFO SECPLAN | 28 | Técnico | R06 |
| Honorarios | DIRECTOR DE PROYECTOS CULTURALES DIRECCION DE CULTURA | 7 | Directivo | R01 |
| Honorarios | DIRECTOR DE PROYECTOS CULTURALES | 4 | Directivo | R01 |
| Honorarios | DIRECTOR DE PROYECTOS CULTURALES DIRECCIÓN DE CULTURA | 4 | Directivo | R01 |
| Honorarios | DIRECTOR DE PREYECTOR CULTURALES | 2 | Directivo | R01 |
| Honorarios | DIRECTOR DE PROYECYOS CULTURALES DIRECCION DE CULTURA | 2 | Directivo | R01 |
| Honorarios | SUPERVISOR PROEMPLEO | 86 | Jefatura | R03 |
| Código del Trabajo | ADMINISTRADOR CEMENTERIO MUNIC | 36 | Jefatura | R04 |
| Código del Trabajo | JEFA DEPTO. GAB. PSICOTECNICO | 33 | Jefatura | R02 |
| Honorarios | COORD. CONTROL GESTION | 27 | Jefatura | R03 |
| Honorarios | COORD. HABITABILIDAD | 26 | Jefatura | R03 |

### 5.2 Veinte no clasificables más frecuentes

Estos casos deben revisarse primero por su impacto en cobertura. Se mantienen sin clasificar hasta contar con evidencia funcional adicional.

| Categoría | Cargo | Frecuencia | Regla | Motivo |
|---|---|---|---|---|
| Honorarios | APOYO FAMILIAR FAMILIAS INTEGRADAS | 267 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTES | 261 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE MANUALIDADES | 204 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL | 168 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DEPORTIVA OF. DEPORTES | 126 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESORA SENIOR | 101 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FAMILIAR PROG. FAMILIAS INTEGRADAS | 68 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO DEPARTAMENTO | 60 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA DE 4 A 7 | 55 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA VECINAL | 53 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL | 51 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA MANUALIDADES TALLERES DE MUJERES | 47 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESORIA PERSONALIZADA ADULTOS MAYORES | 45 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA DE CASOS OLN | 40 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA PIAM ADULTO MAYOR | 40 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FAMILIAR PROGRAMA FAMILIAS INTEGRADAS | 32 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | OPERADOR DE RELOJ PLAZA 21 DE MAYO | 32 | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MONITORA DE MANUALIDADES | 29 | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | INFORMATICO | 25 | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTOR DE FUTBOL | 25 | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |

## 6. No clasificables, ordenados por frecuencia

Se listan los 665 valores no clasificables de ambas categorías, sin omisiones.

| Categoría | Cargo | Frecuencia | Regla |
|---|---|---|---|
| Honorarios | APOYO FAMILIAR FAMILIAS INTEGRADAS | 267 | R98 |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTES | 261 | R98 |
| Honorarios | TALLER DE MANUALIDADES | 204 | R98 |
| Honorarios | GESTOR VECINAL | 168 | R98 |
| Honorarios | MONITORA DEPORTIVA OF. DEPORTES | 126 | R98 |
| Honorarios | ASESORA SENIOR | 101 | R98 |
| Honorarios | APOYO FAMILIAR PROG. FAMILIAS INTEGRADAS | 68 | R98 |
| Honorarios | APOYO DEPARTAMENTO | 60 | R98 |
| Honorarios | MONITORA PROGRAMA DE 4 A 7 | 55 | R98 |
| Honorarios | GESTORA VECINAL | 53 | R98 |
| Honorarios | GESTOR CULTURAL | 51 | R98 |
| Honorarios | MONITORA MANUALIDADES TALLERES DE MUJERES | 47 | R98 |
| Honorarios | ASESORIA PERSONALIZADA ADULTOS MAYORES | 45 | R98 |
| Honorarios | GESTORA DE CASOS OLN | 40 | R98 |
| Honorarios | MONITORA PROGRAMA PIAM ADULTO MAYOR | 40 | R98 |
| Honorarios | APOYO FAMILIAR PROGRAMA FAMILIAS INTEGRADAS | 32 | R98 |
| Honorarios | OPERADOR DE RELOJ PLAZA 21 DE MAYO | 32 | R99 |
| Honorarios | MONITORA DE MANUALIDADES | 29 | R98 |
| Honorarios | INFORMATICO | 25 | R99 |
| Honorarios | INSTRUCTOR DE FUTBOL | 25 | R99 |
| Honorarios | PREVENCIONISTA DE RIESGO | 23 | R99 |
| Honorarios | COMUNICADOR AUDIOVISUAL OF. COMUNICACIONES | 21 | R99 |
| Honorarios | ENSEÑANZA MEDIA COMPLETA | 21 | R99 |
| Honorarios | MONITOR DE FUTBOL OF. DEPORTES | 21 | R98 |
| Honorarios | ASESOR SENIOR | 20 | R98 |
| Honorarios | EJECUTIVO DE EMPRESAS OMIL | 19 | R99 |
| Honorarios | TALLER DE DANZA TRIBAL | 19 | R98 |
| Honorarios | APOYO EDUCATIVO PROGRAMA DE 4 A 7 | 17 | R98 |
| Honorarios | DISEÑADOR GRAFICO DIDECO | 17 | R99 |
| Honorarios | GESTORA CULTURAL | 17 | R98 |
| Honorarios | GESTORA DE CASO OLN | 17 | R98 |
| Honorarios | PROFESOR DE PATINAJE | 17 | R99 |
| Honorarios | APOYO PROFESIONA SECPLAN | 16 | R98 |
| Honorarios | ARBITRO DE FUTBOL OF. DEPORTES | 16 | R99 |
| Honorarios | GESTORA TERRITORIAL OLN | 16 | R98 |
| Honorarios | DISEÑADOR DIDECO | 15 | R99 |
| Honorarios | MONITORA DE FUTBOL FEMENINO OF. DEPORTES | 15 | R98 |
| Honorarios | MONITORA TALLER DE MUJERES | 15 | R98 |
| Honorarios | APOYO CIERRE DEM | 14 | R98 |
| Honorarios | APOYO FAMILIAR PROG FAMILIAS INTEGRADAS | 14 | R98 |
| Honorarios | APOYO FAMILIAR, FAMILIAS INTEGRADAS | 14 | R98 |
| Honorarios | COMUNICADOR AUDIOVISUAL DIDECO | 14 | R99 |
| Honorarios | MONITOR DE ALTEROFILIA OF. DEPORTES | 14 | R98 |
| Honorarios | MONITORA DE ZUMBA OF. DEPORTES | 14 | R98 |
| Honorarios | FOTOGRAFO OF. COMUNICACIONES | 13 | R99 |
| Honorarios | GESTOR DE CASOS OLN | 13 | R98 |
| Honorarios | LOCUTOR DEPTO COMUNICACIONES | 13 | R99 |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTIVO | 13 | R98 |
| Honorarios | ENCARGADA COMUNAL PMJ CORONEL | 12 | R99 |
| Honorarios | GESTOR VECINAL DIRECCION DE TRANSITO | 12 | R98 |
| Honorarios | MONITOR DE FUTBOL | 12 | R98 |
| Honorarios | MONITOR DE HERTEROFILIA OF. DEPORTES | 12 | R98 |
| Honorarios | MONITORA SOCIAL CENTRO DE LA MUJER | 12 | R98 |
| Honorarios | ENCARGADA DEPTO DE LA MUJER Y E.G | 11 | R99 |
| Honorarios | MONITOR DEPORTES | 11 | R98 |
| Honorarios | APOYO EGIS MUNICIPAL | 10 | R98 |
| Honorarios | APOYO FEMILIAR PROG. FAMILIAS INTEGRADAS | 10 | R98 |
| Honorarios | APOYO OF. INFORMACIONES | 10 | R98 |
| Honorarios | COMUNICADOR AUDIOVISUAL CASA DE LA CULTURA | 10 | R99 |
| Honorarios | COORDINADOR PRO EMPLEOS ISLA SANTA MARIA | 10 | R99 |
| Honorarios | COORDINADORA ASUNTOS RELIGIOSOS | 10 | R99 |
| Honorarios | EJECUTIVO ATENCION DE EMPRESAS OMIL | 10 | R99 |
| Honorarios | ENC. CASA DEL ADULTO MAYOR | 10 | R99 |
| Honorarios | GESTORA PATRIMONIAL | 10 | R98 |
| Honorarios | MONITORA PROGRAMAS PIAM ADULTO MAYOR | 10 | R98 |
| Honorarios | TALLER DE RECICLAJE | 10 | R98 |
| Honorarios | APOYO JURIDICO ASESORIA JURIDICA | 9 | R98 |
| Honorarios | APOYO PERIODISTICO SENDA PREVIENE | 9 | R98 |
| Honorarios | ATENCION DE CASOS SOCIALES | 9 | R99 |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE TRANSITO | 9 | R98 |
| Honorarios | MONITORA ARTES TEATRALES | 9 | R98 |
| Honorarios | MONITORA DE DANZA OF. DISCAPACIDAD | 9 | R98 |
| Honorarios | MONITORA FUTBOL FEMENINO OF. DEPORTES | 9 | R98 |
| Honorarios | TALLER DE ORFERERIA | 9 | R98 |
| Honorarios | APOYO CASA DE LA SEGURIDAD | 8 | R98 |
| Honorarios | APOYO EN SEGURIDAD DIRECCION DE SEGURIDAD PUBLICA | 8 | R98 |
| Honorarios | APOYO PARTICIPACION CIUDADANA | 8 | R98 |
| Honorarios | APOYO SOCIAL OF. ADULTO MAYOR | 8 | R98 |
| Honorarios | ENTRENADOR DE FUTBOL | 8 | R99 |
| Honorarios | GESTOR VECINAL OF. PARTICIPACION CIUDADANA | 8 | R98 |
| Honorarios | MONITORA DEPORTES | 8 | R98 |
| Honorarios | MONITORA PROG. DE 4 A 7 | 8 | R98 |
| Honorarios | MONITORA PROGRAMA CRECER EN COMUNIDAD | 8 | R98 |
| Honorarios | OPERADOR SOCIAL | 8 | R99 |
| Honorarios | REHAB. CENTRO ANUN | 8 | R99 |
| Honorarios | TALLER DE MANUALIDADES PORCELANA EN FRIO | 8 | R98 |
| Honorarios | TALLER DE YOGA PARA MUJERES | 8 | R98 |
| Honorarios | TRABAJO EN ARTES VISUALES | 8 | R99 |
| Honorarios | ACOMPAÑAMIENTO FAMILIAR POR. PSICOSOCIAL | 7 | R99 |
| Honorarios | APOYO DEPORTIVO | 7 | R98 |
| Honorarios | APOYO EN P.C.V. | 7 | R98 |
| Honorarios | APOYO FAMILIAR PROG PSICOSOCIAL | 7 | R98 |
| Honorarios | COORDINADOR PROEMPLEO | 7 | R99 |
| Honorarios | COORDINADORA | 7 | R99 |
| Honorarios | GESTOR CULTURAL EN EJECUCION DE OBRAS | 7 | R98 |
| Honorarios | MONITOR DE PATINAJE OF. DEPORTES | 7 | R98 |
| Honorarios | MONITOR DE VOLEIBOL | 7 | R98 |
| Honorarios | MONITOR PROGRAMA DE 4 A 7 | 7 | R98 |
| Honorarios | MONITORA DANZA OF. DISCAPACIDAD | 7 | R98 |
| Honorarios | MONITORA DE DANZA | 7 | R98 |
| Honorarios | MONITORA DE FOLKLORE CASA DEL ADULTO MAYOR | 7 | R98 |
| Honorarios | MONITORA DE MANUALIDADES OF. DISCAPACIDAD | 7 | R98 |
| Honorarios | MONITORA DE YERBAS MEDICINALES | 7 | R98 |
| Honorarios | MONITORA DEPORTIVA OF. DE DEPORTES | 7 | R98 |
| Honorarios | MONITORA FITNES | 7 | R98 |
| Honorarios | MONITORA MODA TALLERES DE MUJERES | 7 | R98 |
| Honorarios | MONITORA PROGRAMA VINCULOS ADULTO MAYOR | 7 | R98 |
| Honorarios | MONITORA REPOSTERIA OF. ADULTO MAYOR | 7 | R98 |
| Honorarios | MONITORA TALLER DE FLAMENCO | 7 | R98 |
| Honorarios | MONITORA YERBAS MEDICINALES TALLERES DE MUJERES | 7 | R98 |
| Honorarios | APOYO ADM. OF. JOVENES Y MONITORA DE AUTODEFENSA DEPTO. DE LA MUJER | 6 | R00 |
| Honorarios | APOYO DIRECCION DE CONTROL | 6 | R98 |
| Honorarios | APOYO EN P.C.V | 6 | R98 |
| Honorarios | APOYO JURIDICO DIRECCION DE CONTROL | 6 | R98 |
| Honorarios | APOYO JURIDICO EN GABINETE | 6 | R98 |
| Honorarios | ASESOR EN PROGRAMA Y PLANIFICACION DE NUEVOS INGRESOS MUNICIPALES | 6 | R98 |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS MUNICIPALES TRANSITO | 6 | R98 |
| Honorarios | COORDINADOR ALBERGUE | 6 | R99 |
| Honorarios | COORDINADOR DE COMUNICACIONES CASA DEL ADULTO MAYOR | 6 | R99 |
| Honorarios | COORDINADOR HABITABILIDAD | 6 | R99 |
| Honorarios | COORDINADOR INFOCENTRO YOBILO | 6 | R99 |
| Honorarios | COORDINADORA CASA DEL ADULTO MAYOR | 6 | R99 |
| Honorarios | COORDINADORA PATRIMONIO | 6 | R99 |
| Honorarios | COORDINADORA PROG. PARENTALIDAD SENDA | 6 | R99 |
| Honorarios | COORDINADORA PUEBLOS INDIGENAS | 6 | R99 |
| Honorarios | COORDINADORA SENDA PREVIENE | 6 | R99 |
| Honorarios | COORDINADORA TURISMO | 6 | R99 |
| Honorarios | EDUCADORA SOCIAL OPD | 6 | R99 |
| Honorarios | ENCARGADA COMUNAL PJM CORONEL | 6 | R99 |
| Honorarios | ENCARGADA COMUNAL PMJ | 6 | R99 |
| Honorarios | GESTOR | 6 | R98 |
| Honorarios | GESTOR CULTURAL DIRECCION DE CULTURA ARTE Y PATRIMONIO | 6 | R98 |
| Honorarios | GESTOR VECINAL DIRECCION DE MEDIO AMBIENTE | 6 | R98 |
| Honorarios | INSTRUCTOR DEPORTIVO | 6 | R99 |
| Honorarios | INSTRUCTORA YOGA DEPTO. DE LA MUJER | 6 | R99 |
| Honorarios | LOCUTOR DEPT. COMUNICACIONES | 6 | R99 |
| Honorarios | LOCUTOR DEPTO. COMUNICACIONES | 6 | R99 |
| Honorarios | MONITOR ALFABETIZACION DIGITAL CASA DEL ADULTO MAYOR | 6 | R98 |
| Honorarios | MONITOR DE CICLISMO | 6 | R98 |
| Honorarios | MONITORA DEPORTES OF. DEPORTES | 6 | R98 |
| Honorarios | MONITORA DEPORTES OF. DEPORTES Y TALLERES DE MUJERES | 6 | R98 |
| Honorarios | MONITORA PROGRAMA 4 A 7 SERNAMEG | 6 | R98 |
| Honorarios | MONITORA TALLERES DEPORTIVO | 6 | R98 |
| Honorarios | MONITORA ZUMBA OF. DEPORTES | 6 | R98 |
| Honorarios | TALLER DE TELAR MAPUCHE | 6 | R98 |
| Honorarios | APOYO CULTURA | 5 | R98 |
| Honorarios | APOYO JURICO ASESORIA JURIDICA | 5 | R98 |
| Honorarios | APOYO JURIDICO DIRECCIÓN DE CONTROL | 5 | R98 |
| Honorarios | ARBITRO DE FUTBOOL OF. DEPORTE | 5 | R99 |
| Honorarios | ASESOR FINANCIERO Y PLANIFICACION DE NUEVOS INGRESOS | 5 | R98 |
| Honorarios | ATENCIÓN DE CASOS SOCIALES | 5 | R99 |
| Honorarios | COORDINADOR AREA ARTISTICA OF. JOVENES | 5 | R99 |
| Honorarios | COORDINADOR SISTEMA SEGURIDAD ELECTRONICA DIRECCION SEGURIDAD PUBLICA | 5 | R99 |
| Honorarios | COORDINADORA ASENTAMIENTOS PRECARIOS | 5 | R99 |
| Honorarios | COORDINADORA CENTRO DE LA MUJER | 5 | R99 |
| Honorarios | COORDINADORA CHILE CRECE CINTIGO | 5 | R99 |
| Honorarios | COORDINADORA O.P.D. INFANCIA | 5 | R99 |
| Honorarios | COORDINADORA OPD | 5 | R99 |
| Honorarios | COORDINADORA PROGRAMA DE 4 A 7 | 5 | R99 |
| Honorarios | DISEÑADOR PLAN DE ACCIÓN OPD | 5 | R99 |
| Honorarios | GESTOR CULTURAL DIRECCION CULTURA, ARTES Y PATRIMONIO | 5 | R98 |
| Honorarios | GESTOR CULTURAL, DIRECCION DE CULTURA, ARTE Y PATRIMONIO | 5 | R98 |
| Honorarios | GESTOR VECINAL DIRECCION DE ASEO Y ORNATO | 5 | R98 |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE MEDIO AMBIENTE | 5 | R98 |
| Honorarios | GESTORA VECINAL DIRECCION DE TRANSITO | 5 | R98 |
| Honorarios | INSTRUCTORA DEPORTIVA OF. DEPORTES | 5 | R99 |
| Honorarios | MONITOR DE BASQUETBOL, OF. DEPORTES | 5 | R98 |
| Honorarios | MONITOR DE PATINAJE EN POLIDEPORTIVO | 5 | R98 |
| Honorarios | MONITOR DEPORTIVO | 5 | R98 |
| Honorarios | MONITORA COMUNITARIA O.P.D. | 5 | R98 |
| Honorarios | MONITORA DANZA TRIVAL TALLERES DE MUJERES | 5 | R98 |
| Honorarios | MONITORA DE ALFABETIZACIÓN DIGUITAL | 5 | R98 |
| Honorarios | MONITORA DE ARTES TEATRALES | 5 | R98 |
| Honorarios | MONITORA DE BARTENER Y GARSONERIA | 5 | R98 |
| Honorarios | MONITORA DEPORTIVA OF. DEPORTIVA | 5 | R98 |
| Honorarios | MONITORA ORFEBRERIA TALLERES DE MUJERES | 5 | R98 |
| Honorarios | MONITORA PATIN OF. DEPORTES | 5 | R98 |
| Honorarios | MONITORA PORCELANA EN FRIO TALLERES DE MUJERES | 5 | R98 |
| Honorarios | MONITORA PROG. VINCULO ADULTO MAYOR | 5 | R98 |
| Honorarios | MONITORA RECICLAJE TALLERES DE MUJERS | 5 | R98 |
| Honorarios | MONITORA SOCIAL | 5 | R98 |
| Honorarios | MONITORA TALLERES DE MUJERES | 5 | R98 |
| Honorarios | MURALISTAS DIRECCIÓN DE CULTURA | 5 | R99 |
| Código del Trabajo | ENCARGADO DE ESTADISTICA | 4 | R99 |
| Honorarios | ADM. PROG. REG SOCIAL DE HOGARES | 4 | R99 |
| Honorarios | APOYO ASEO Y ORNATO | 4 | R98 |
| Honorarios | APOYO BIBLIOTECA | 4 | R98 |
| Honorarios | APOYO CASA ADULTO MAYOR | 4 | R98 |
| Honorarios | APOYO CENTRO DE LA MUJER | 4 | R98 |
| Honorarios | APOYO DIRECCION DE TRANSITO | 4 | R98 |
| Honorarios | APOYO EN COORD. Y COBRANZAS | 4 | R98 |
| Honorarios | APOYO EN PCV | 4 | R98 |
| Honorarios | APOYO EN SEGURIDAD CASA DE LA SEGURIDAD | 4 | R98 |
| Honorarios | APOYO FINANZAS MUNICIPAL | 4 | R98 |
| Honorarios | APOYO GABINETE MUNICIPAL | 4 | R98 |
| Honorarios | APOYO MEDIO AMBIENTE | 4 | R98 |
| Honorarios | APOYO MUJERES JEFA DE HOGAR | 4 | R98 |
| Honorarios | APOYO OF PREVENCION DE RIESGOS | 4 | R98 |
| Honorarios | APOYO OF. CULTURA | 4 | R98 |
| Honorarios | APOYO OF. DE CONCEJALES | 4 | R98 |
| Honorarios | APOYO OF. DEPORTES | 4 | R98 |
| Honorarios | APOYO OFICINA DE JOVENES | 4 | R98 |
| Honorarios | APOYO OPD | 4 | R98 |
| Honorarios | APOYO PROG.PROEMPLEO | 4 | R98 |
| Honorarios | APOYO REG SOCIAL DE HOGARES | 4 | R98 |
| Honorarios | ASESOR SENDA PREVIENE | 4 | R98 |
| Honorarios | COMUNICADOR AUDIVISUAL DIDECO | 4 | R99 |
| Honorarios | COORDINADOR ALBERGUE MUNICIPAL | 4 | R99 |
| Honorarios | COORDINADOR INFOCENTRO | 4 | R99 |
| Honorarios | COORDINADORA PUEBLOS ORIGINARIOS | 4 | R99 |
| Honorarios | Coordinador Infocentro OF. JOVENES | 4 | R99 |
| Honorarios | EDUCADOR O.P.D. CORONEL | 4 | R99 |
| Honorarios | EGIS MUNICIPAL | 4 | R97 |
| Honorarios | ENCARGADA PREVIENE | 4 | R99 |
| Honorarios | ENCARGADA PROGRAMA PMJ CORONEL | 4 | R99 |
| Honorarios | ENCARGADA PROGRAMA PREVENCION DE VIOLENCIA | 4 | R99 |
| Honorarios | ENCARGADA PROGRAMA RED LOCAL DE APOYO Y CUIDADO | 4 | R98 |
| Honorarios | ENCARGADA TURISMO | 4 | R99 |
| Honorarios | EXPERTO OFICINA GABINETE | 4 | R99 |
| Honorarios | FOTOGRAFO DE OF. COMUNICACIONES | 4 | R99 |
| Honorarios | GESTOR CULTUYRAL DIRECCIÓN DE CULTURA | 4 | R98 |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE ASEO | 4 | R98 |
| Honorarios | INSTRUCTORA KARATE OF. JOVENES | 4 | R99 |
| Honorarios | LOCUTOR DEPTO DE COMUNICACIONES | 4 | R99 |
| Honorarios | MONITOR ALFABETIZACION DIGITAL | 4 | R98 |
| Honorarios | MONITOR DE ALFABETIZACION DIGUITAL | 4 | R98 |
| Honorarios | MONITOR DE HALTEROFILIA OF. DEPORTES | 4 | R98 |
| Honorarios | MONITOR DE HALTEROFILIA OFICINA DE DEPORTES | 4 | R98 |
| Honorarios | MONITOR DEPORTIVO OF DEPORTES | 4 | R98 |
| Honorarios | MONITOR OTEC | 4 | R98 |
| Honorarios | MONITOR TENIS EF DEPORTES | 4 | R98 |
| Honorarios | MONITOR VESPERTINO | 4 | R98 |
| Honorarios | MONITORA COMUNITARIA OPD | 4 | R98 |
| Honorarios | MONITORA COMUNITARIA, PROGRAMA VINCULO | 4 | R98 |
| Honorarios | MONITORA DE DANZA FOLCKLORICA | 4 | R98 |
| Honorarios | MONITORA DE DANZA FOLKLORICA CASA DEL ADULTO MAYOR | 4 | R98 |
| Honorarios | MONITORA DE PROGRAMA ADULTO MAYOR | 4 | R98 |
| Honorarios | MONITORA DE SUBLIMACION OF. DISCAPACIDAD | 4 | R98 |
| Honorarios | MONITORA DEPORTIVO OF. DEPORTES | 4 | R98 |
| Honorarios | MONITORA EDUCACION FISICA | 4 | R98 |
| Honorarios | MONITORA PATINAJE OFICINA DE DEPORTES | 4 | R98 |
| Honorarios | MONITORA PROGRANAS PIAM ADULTO MAYOR | 4 | R98 |
| Honorarios | PERMISO CIRCULACION | 4 | R97 |
| Honorarios | PREPARADOR FISICO | 4 | R99 |
| Honorarios | PROG. MINISTERIO CULTURA Y ARTES | 4 | R97 |
| Honorarios | PROG.PREVENC ALCOHOL SENDAS | 4 | R97 |
| Honorarios | TALLER DE ARTESANIA Y MANUALIDADES | 4 | R98 |
| Honorarios | TALLER DE FUTBOL | 4 | R98 |
| Código del Trabajo | APOYO TRANSITO | 3 | R98 |
| Honorarios | APOYO DEPARTAMENTO DIDECO | 3 | R98 |
| Honorarios | APOYO DIDECO | 3 | R98 |
| Honorarios | APOYO FAMILIAR | 3 | R98 |
| Honorarios | APOYO JURIDICO GABINETE | 3 | R98 |
| Honorarios | ARBITRO DE FUTBOL OF. DE DEPORTES | 3 | R99 |
| Honorarios | ASESOR EMPRENDIMIENTO FOMENTO PRODUCTIVO | 3 | R98 |
| Honorarios | ASESORIA A MUJERES JEFAS DE HOGAR | 3 | R98 |
| Honorarios | ATENCION DE CASOS | 3 | R99 |
| Honorarios | AUDIOVISUAL DIDECO | 3 | R99 |
| Honorarios | COMUNICADOR AUDIO VISUAL, RELACIONES PUBLICAS | 3 | R99 |
| Honorarios | COORDINADOR CUADRILLA EJECUCION DE OBRAS | 3 | R99 |
| Honorarios | DISEÑADOR GRAFICO | 3 | R99 |
| Honorarios | ENC. OF. JOVENES | 3 | R99 |
| Honorarios | ENCARGADA PROGRAMA JEFAS DE HOGAR | 3 | R99 |
| Honorarios | ENCARGADA PROGRAMA MUJERES CORONEL | 3 | R99 |
| Honorarios | ENCARGADO DE PROGRAMAS | 3 | R99 |
| Honorarios | ENCUENTROS MURALISTAS | 3 | R97 |
| Honorarios | GESTOR CULTURAL EJECUCIÓN DE OBRAS | 3 | R98 |
| Honorarios | GESTOR TERRITORIAL | 3 | R98 |
| Honorarios | GESTOR VECINAL FOMENTO PRODUCTIVO | 3 | R98 |
| Honorarios | GESTORA TERRITORIA OLN | 3 | R98 |
| Honorarios | GESTORA VECINAL DIRECCIÓN DE TRANSITO | 3 | R98 |
| Honorarios | INSTALACIONES ELECTRICAS | 3 | R97 |
| Honorarios | INSTRUCOR DE FUTBOL | 3 | R99 |
| Honorarios | INSTRUCTORA DEPORTIVA | 3 | R99 |
| Honorarios | MAESTRO DIRECCION DE CULTURA, ARTE Y PATRIMONIO | 3 | R99 |
| Honorarios | MONITOR ALFABETIZACION DIGUITAL | 3 | R98 |
| Honorarios | MONITOR ARTES VISUALES PROGRAMA DE 4 A 7 | 3 | R98 |
| Honorarios | MONITOR DE BASQUETBOL OF. DEPORTES | 3 | R98 |
| Honorarios | MONITOR DE FÚTBOL OF. DEPORTES | 3 | R98 |
| Honorarios | MONITOR SOCIAL | 3 | R98 |
| Honorarios | MONITOR ZUMBA | 3 | R98 |
| Honorarios | MONITORA BATUCADA | 3 | R98 |
| Honorarios | MONITORA DE ARTES MARCIALES | 3 | R98 |
| Honorarios | MONITORA DE DEPORTE | 3 | R98 |
| Honorarios | MONITORA DE DEPORTES OF. DEPORTES | 3 | R98 |
| Honorarios | MONITORA DE GARZONERIA | 3 | R98 |
| Honorarios | MONITORA DE YERBAS MEDICINALES TALLER DE MUJERES | 3 | R98 |
| Honorarios | MONITORA LIDEREZAS | 3 | R98 |
| Honorarios | MONITORA MANUALIDADES | 3 | R98 |
| Honorarios | MONITORA PROGRAMA 4 A 7 | 3 | R98 |
| Honorarios | MONITORA PROGRAMA PIAM ADULTO MAYORES | 3 | R98 |
| Honorarios | MONITORA TALLERES DEPORTIVOS | 3 | R98 |
| Honorarios | MONITORA TELAR MAPUCHE TALLERES DE MUJERES | 3 | R98 |
| Honorarios | OF DE JOVENES | 3 | R97 |
| Honorarios | OF DEPORTES | 3 | R97 |
| Honorarios | REGISTRO SOCIAL DE HOGARES | 3 | R97 |
| Honorarios | TALLER MAPUCHE | 3 | R98 |
| Honorarios | APOYO ADMINISTRATIVO MONITORAS JEFAS DE HOGAR | 2 | R00 |
| Honorarios | APOYO EJECUCION DE OBRAS | 2 | R98 |
| Honorarios | APOYO JURIDICO ASEDORIA JURIDICA | 2 | R98 |
| Honorarios | APOYO JURIDO GABINETA | 2 | R98 |
| Honorarios | APOYO OF. HONORARIOS | 2 | R98 |
| Honorarios | APOYO PVC | 2 | R98 |
| Honorarios | ARBITRO DE FUTBOL OF DEPORTES | 2 | R99 |
| Honorarios | ARIBITRO DE FUTBOL OF. DEPORTES | 2 | R99 |
| Honorarios | ARTISTA EDUCADOR | 2 | R99 |
| Honorarios | ASESOR DE PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS | 2 | R98 |
| Honorarios | ASESOR DE PROGRAMACIÓN Y PLANIFICACION | 2 | R98 |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION | 2 | R98 |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION D | 2 | R98 |
| Honorarios | ASESOR EN PROGRAMACIÓN Y PLANIFICACIÓN | 2 | R98 |
| Honorarios | ASESOR FINANCIERO Y PLANIFICACION DE NUEVO INGRESOS | 2 | R98 |
| Honorarios | AUDIOVISUAL CASA DE LA CULTURA | 2 | R99 |
| Honorarios | AUDIVISUAL DIDECO | 2 | R99 |
| Honorarios | CANTANTE | 2 | R99 |
| Honorarios | COMUNICACIÓN OPD | 2 | R97 |
| Honorarios | COMUNICADOR AUDIVISUAL OF. COMUNICACIONES | 2 | R99 |
| Honorarios | COORDINADORA CASA DE ADULTO MAYOR | 2 | R99 |
| Honorarios | EJECUCION DE OBRAS | 2 | R97 |
| Honorarios | EJECUTIVO DE EMPRESA OMIL | 2 | R99 |
| Honorarios | ENC. DE ORIENTACION E INFORMACION DE VIOLENCIA DE GENERO | 2 | R99 |
| Honorarios | ENC. DE ORIENTECION E INFORMACION DE VIOLENCIA | 2 | R99 |
| Honorarios | ENC. OF. HABITABILIDAD | 2 | R99 |
| Honorarios | ENC. OF. PUEBLOS ORIGINARIOS | 2 | R99 |
| Honorarios | ENCARGADA CASA ADULTO MAYOR | 2 | R99 |
| Honorarios | ENCARGADA OF. ASUNTOS RELIGIOSOS | 2 | R99 |
| Honorarios | ENCARGADO DE PROGRAMA Y PLANIFICACION DE RECURSOS | 2 | R99 |
| Honorarios | ENCARGADO DE PROGRAMACION Y PLANIFICACION | 2 | R99 |
| Honorarios | ENCUENTRO MURALISTAS | 2 | R97 |
| Honorarios | FOMENTO PRODUCTIVO | 2 | R97 |
| Honorarios | FORM.PROY.SOC.PARTIC.CIUDADAN | 2 | R97 |
| Honorarios | FOTOGRAFO DEPTO. COMUNICACIONES | 2 | R99 |
| Honorarios | GESTIÓN VECINAL | 2 | R99 |
| Honorarios | GESTOR COMUNITARIO | 2 | R98 |
| Honorarios | GESTOR CULTURA DIRECCIÓN DE CULTURA | 2 | R98 |
| Honorarios | GESTOR CULTURAL CASA DE LA CULTURA | 2 | R98 |
| Honorarios | GESTOR CULTURAL DIRECCIÓN DE CULTURA | 2 | R98 |
| Honorarios | GESTOR CULTURAL EN EJECUCIÓN DE OBRAS | 2 | R98 |
| Honorarios | GESTOR EJECUCIÓN DE OBRAS | 2 | R98 |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE TRÁNSITO | 2 | R98 |
| Honorarios | GESTORA TERRITIORAL OLN | 2 | R98 |
| Honorarios | INSTRUCTORA DE FUTBOL FEMENINO OF. DEPORTES | 2 | R99 |
| Honorarios | LOCUTOR | 2 | R99 |
| Honorarios | MONITOR ALFABETIZACIÓN DIGITAL CASA DEL ADULTO MAYOR | 2 | R98 |
| Honorarios | MONITOR DE DANZA URBANA | 2 | R98 |
| Honorarios | MONITOR DE HERTEROFILIA | 2 | R98 |
| Honorarios | MONITOR DE MANUALIDADES | 2 | R98 |
| Honorarios | MONITOR DE MANUALIDADES TALLERES DE MUJERES | 2 | R98 |
| Honorarios | MONITOR DE PROGRAMA DE 4 A 7 | 2 | R98 |
| Honorarios | MONITOR DEPORTIVO FOMENTO PRODUCTIVO | 2 | R98 |
| Honorarios | MONITOR FUTBOL OF. DEPORTES | 2 | R98 |
| Honorarios | MONITOR FUTBOL. OF DEPORTES | 2 | R98 |
| Honorarios | MONITOR FUTBOLOF. DEPORTES | 2 | R98 |
| Honorarios | MONITOR PROGRAMA VINCULOS ADULTO MAYOR | 2 | R98 |
| Honorarios | MONITOR TALLER BMX | 2 | R98 |
| Honorarios | MONITOR TALLER CALISTENIA | 2 | R98 |
| Honorarios | MONITOR TALLER SKATE | 2 | R98 |
| Honorarios | MONITORA | 2 | R98 |
| Honorarios | MONITORA DE ALFABETIZACION DIGUITAL | 2 | R98 |
| Honorarios | MONITORA DE CAPORAL | 2 | R98 |
| Honorarios | MONITORA DE DANZA FOLCKORICA | 2 | R98 |
| Honorarios | MONITORA DE DISCAPACIDAD | 2 | R98 |
| Honorarios | MONITORA DE MANUALIDADES, OF. DISCAPACIDAD | 2 | R98 |
| Honorarios | MONITORA DE MANUEALIDADES | 2 | R98 |
| Honorarios | MONITORA DE PROGRAMA PIAM | 2 | R98 |
| Honorarios | MONITORA DE PROGRAMA PIAM ADULTO MAYOR | 2 | R98 |
| Honorarios | MONITORA DE PROGRAMA VINCULOS ADULTO MAYOR | 2 | R98 |
| Honorarios | MONITORA DE SUBLIMACION OF. TRANSPORTE | 2 | R98 |
| Honorarios | MONITORA DE TALLER DE TEATRO | 2 | R98 |
| Honorarios | MONITORA DE ZUMBA OF. DE DEPORTES | 2 | R98 |
| Honorarios | MONITORA PATINES OF. DEPORTES | 2 | R98 |
| Honorarios | MONITORA PORCELANA EN FRIO TALLER DE MUJERES | 2 | R98 |
| Honorarios | MONITORA PROG DE 4 A 7 | 2 | R98 |
| Honorarios | MONITORA PROGRANA PIAM ADULTO MAYOR | 2 | R98 |
| Honorarios | MONITORA SOCIAL A.MAYOR | 2 | R98 |
| Honorarios | MONITORA YOGA | 2 | R98 |
| Honorarios | MONITRA ALFABETIZACIÓN DIGITAL | 2 | R99 |
| Honorarios | OFICINA EGIS | 2 | R97 |
| Honorarios | OPERADOR RELOJ PLAZA 21 DE MAYO | 2 | R99 |
| Honorarios | PARTICIPACIÓN DE DIAGNOSTICOS Y PLANIFICACIÓN CDM | 2 | R97 |
| Honorarios | PREV. RIESGOS CASA DE LA SEG. | 2 | R99 |
| Honorarios | PREVENCIONISTA DE RIESGO OF. RIESGO | 2 | R99 |
| Honorarios | PREVENCIONISTA EJ. DE OBRAS | 2 | R99 |
| Honorarios | PROGRAMA PSICOSOCIAL | 2 | R97 |
| Honorarios | PUBLICIDAD CASA DE LA SEGURIDAD | 2 | R97 |
| Honorarios | PUBLICISTA | 2 | R99 |
| Honorarios | PUBLICISTA CASA DE LA CULTURA | 2 | R99 |
| Honorarios | RELATOR DE TALLER | 2 | R98 |
| Código del Trabajo | ENCARGADO DE ESTADISTICAS | 1 | R99 |
| Código del Trabajo | GABINETE PSICOTECNICO | 1 | R99 |
| Honorarios | ACTRIZ | 1 | R99 |
| Honorarios | ADMINISTRACIÓN GIMANSIO SCHWAGER | 1 | R99 |
| Honorarios | ADMINISTRADOR GIMANSIO SCHWAGER | 1 | R99 |
| Honorarios | AMPLIAR PATRIMONIO COMUNAL | 1 | R97 |
| Honorarios | APOERADOR DE RELOJ PLAZA 21 DE MAYO | 1 | R99 |
| Honorarios | APOYO ADM. OF. DE JOVENES Y MONITORA DE AUTODEFENSA DEPTO. DE LA MUJER | 1 | R00 |
| Honorarios | APOYO ADM. OFICINA DE JOVENES Y MONITORA DE AUTODEFENSA DEPTO DE LA MUJER | 1 | R00 |
| Honorarios | APOYO ADM. OFICNA DE JOVENES Y MONITORA DE AUTODENSA | 1 | R00 |
| Honorarios | APOYO AMPLIFICACION | 1 | R98 |
| Honorarios | APOYO AMPLIFICACIÓN | 1 | R98 |
| Honorarios | APOYO ANUN | 1 | R98 |
| Honorarios | APOYO COMUNICACIONES | 1 | R98 |
| Honorarios | APOYO COORDINADOR SENDA | 1 | R98 |
| Honorarios | APOYO DIRECCION DE CULTURA | 1 | R98 |
| Honorarios | APOYO EDUCATIVO DE 4 A 7 | 1 | R98 |
| Honorarios | APOYO EN AMPLIFICACIÓN | 1 | R98 |
| Honorarios | APOYO EN SEGURIDAD | 1 | R98 |
| Honorarios | APOYO EN SEGURIDAD DIRECCION DE SEGURIDAD | 1 | R98 |
| Honorarios | APOYO EN SEGURIDAD DIRECCIÓN DE SEGURIDAD | 1 | R98 |
| Honorarios | APOYO EN SEGURIDAD DIRECCIÓN DE SEGURIDAD PÚBLICA | 1 | R98 |
| Honorarios | APOYO EN SEGURIDAD, CASA DE LA SEGURIDAD | 1 | R98 |
| Honorarios | APOYO FAMILIAR PROGRAMA FAMILIA | 1 | R98 |
| Honorarios | APOYO JURIDCO GABINETE | 1 | R98 |
| Honorarios | APOYO JURIDICO ASESORRIA JURIDICA | 1 | R98 |
| Honorarios | APOYO JURIDICO ASESORÍA JURIDICA | 1 | R98 |
| Honorarios | APOYO JURIDICO ASESORÍA JURÍDICA | 1 | R98 |
| Honorarios | APOYO JURIDICO ASOSORIA JURIDICA | 1 | R98 |
| Honorarios | APOYO JURIDICO GABIENTE | 1 | R98 |
| Honorarios | APOYO JURIDICO GABINITE | 1 | R98 |
| Honorarios | APOYO JURIDO ASESORIA JURIDICA | 1 | R98 |
| Honorarios | APOYO JURIDO GABINETE | 1 | R98 |
| Honorarios | APOYO OF INFORMACIONES | 1 | R98 |
| Honorarios | APOYO PROEMPLEO | 1 | R98 |
| Honorarios | APOYO PROFE. SENDA PREVIENE | 1 | R98 |
| Honorarios | APOYO PROFESIONA DEPTO RRHH | 1 | R98 |
| Honorarios | APOYO REGISTRO SOCIAL DE HOGARES | 1 | R98 |
| Honorarios | ARBITRI DE FUTBOL. OF. DE DEPORTE | 1 | R99 |
| Honorarios | ARBITRO DE FUTBOL OF. DE DEPORTE | 1 | R99 |
| Honorarios | ARBITRO DE FUTBOL. OF. DEPORTES | 1 | R99 |
| Honorarios | ARBITRO DE FÚTBOL OF. DEPORTES | 1 | R99 |
| Honorarios | ARTISTA MURALISTA | 1 | R99 |
| Honorarios | ASESOR DE PROGRAMA Y PLANIFICACIÓN DE NUEVOS INGRESOS | 1 | R98 |
| Honorarios | ASESOR DIRECCION JURIDICA | 1 | R98 |
| Honorarios | ASESOR EN PROG. Y PLANIF. DE NUEVOS INGRESOS MUNICIPALES | 1 | R98 |
| Honorarios | ASESOR EN PROGRAMA Y PLANIFICACIÓN DE NUEVOS INGRESOS | 1 | R98 |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS MUNICIPALES (DIRECCION | 1 | R98 |
| Honorarios | ASESOSA SENIOR | 1 | R99 |
| Honorarios | ASISTENTE CASA DE LA SEGURIDAD | 1 | R99 |
| Honorarios | ASOSOR FINANCIERO Y PLANIFICACION DE NUEVO INGRESOS | 1 | R99 |
| Honorarios | ASOSOR GABINETE | 1 | R99 |
| Honorarios | ASOSORA SENIOR | 1 | R99 |
| Honorarios | ATENCION DE CASO SOCIALES | 1 | R99 |
| Honorarios | ATENCIÓN CASOS SOCIALES | 1 | R99 |
| Honorarios | ATENCIÓN DE CASO SOCIALES | 1 | R99 |
| Honorarios | ATENCIÓN DE CASOS | 1 | R99 |
| Honorarios | ATENCIÓN EN COSOS SOCIALES | 1 | R99 |
| Honorarios | CANTANTE ACTIVIDADES ARTISTICAS GABINETE | 1 | R99 |
| Honorarios | CASA DE LA CULTURA | 1 | R97 |
| Honorarios | CASA DE LA SEGURIDAD | 1 | R97 |
| Honorarios | CHILE CREACION CONTIGO | 1 | R97 |
| Honorarios | COMINCADOR AUDIOVISUAL | 1 | R99 |
| Honorarios | COMINCADOR AUDIOVISUAL OF. COMUNICACIONES | 1 | R99 |
| Honorarios | COMUNICACIÓN AUDIOVISUAL | 1 | R97 |
| Honorarios | COMUNICADOR AUDIO VISUAL MUNICIPAL | 1 | R99 |
| Honorarios | COMUNICADOR AUDIOVISUAL | 1 | R99 |
| Honorarios | COMUNICADOR AUDIOVISUAL RELACIONES PUBLICAS | 1 | R99 |
| Honorarios | COMUNICADOR AUDIOVISUAL. OF. COMUNICACIONES | 1 | R99 |
| Honorarios | COMUNICADORA AUDIOVISUAL CASA DE LA CULTURA | 1 | R99 |
| Honorarios | COMUNICARDOR AUDIOVISUAL OF. COMUNICACIONES | 1 | R99 |
| Honorarios | CONSERVADORA | 1 | R99 |
| Honorarios | COORDD. PROGRAMA DE 4 A 7 SERNAMEG | 1 | R99 |
| Honorarios | COORDINADOR CASA ADULTO MAYOR | 1 | R99 |
| Honorarios | COORDINADOR COMUNICACIONES | 1 | R99 |
| Honorarios | COORDINADOR OTEC MUNICIPAL | 1 | R99 |
| Honorarios | COORDINADORA ESCUELA DE VERANO | 1 | R99 |
| Honorarios | COORDINADORA PATRIMONIAL | 1 | R99 |
| Honorarios | COORDINADORA PROGRAMA 4 A 7 SERNAMEG | 1 | R99 |
| Honorarios | DIRECCION DE CULTURA | 1 | R97 |
| Honorarios | DISEÑADOR GRAFICO CASA DE LA CULTURA | 1 | R99 |
| Honorarios | DISEÑADOR PLAN DE ACCION OPD | 1 | R99 |
| Honorarios | DISEÑADORA VIOLE. CONTRA MUJER | 1 | R99 |
| Honorarios | DISEÑADPR GRAFICO DIDECO | 1 | R99 |
| Honorarios | EJECUTIVO ATENCION DE EMPRESAS | 1 | R99 |
| Honorarios | EJECUTIVO ATENCIÓN DE EMPRESAS OMIL | 1 | R99 |
| Honorarios | EJECUTIVO DE EMPRESAS | 1 | R99 |
| Honorarios | EJECUTIVO DE VENTAS OMIL | 1 | R99 |
| Honorarios | EN | 1 | R97 |
| Honorarios | ENC. AREA INDEPENDIENTE | 1 | R99 |
| Honorarios | ENC. PROYECTO RESCATANTO MEMORIA | 1 | R99 |
| Honorarios | ENCAR. CASA DEL ADULTO MAYOR | 1 | R99 |
| Honorarios | ENCARGADA COMUNAL PJM | 1 | R99 |
| Honorarios | ENCARGADA COMUNICAL P.M.J | 1 | R99 |
| Honorarios | ENCARGADA CREE DEPENDIENTE | 1 | R99 |
| Honorarios | ENCARGADA DE ASUNTOS RELIGIOSO | 1 | R99 |
| Honorarios | ENCARGADA DE ASUNTOS RELIGIOSOS | 1 | R99 |
| Honorarios | ENCARGADA DE PROGRAMA OF. DEPORTES | 1 | R99 |
| Honorarios | ENCARGADA DE PROGRAMA PMJ CORONEL | 1 | R99 |
| Honorarios | ENCARGADA DEPTO DE LA MUJER Y EG | 1 | R99 |
| Honorarios | ENCARGADA DEPTO DE MUJER Y E.G | 1 | R99 |
| Honorarios | ENCARGADA JEFAS DE HOGAR | 1 | R99 |
| Honorarios | ENCARGADA OF. ASUNTOS RELIGIOSO | 1 | R99 |
| Honorarios | ENCARGADA PROGRAMA PJM CORONEL | 1 | R99 |
| Honorarios | ENCARGADA PROGRAMAS MUJERES CORONEL | 1 | R99 |
| Honorarios | ENCARGADO DE PROGRAMA | 1 | R99 |
| Honorarios | ENCARGADO DE PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS | 1 | R99 |
| Honorarios | ENCARGADO DE PROGRAMACION Y PLANIFICACIÓN | 1 | R99 |
| Honorarios | ENCCARGADO DE PROGRAMAS | 1 | R99 |
| Honorarios | ENTRANADOR DE FUTBOL | 1 | R99 |
| Honorarios | ENTREGA TARJETA NAVIDEÑAS | 1 | R97 |
| Honorarios | ENTRENADOR DE BASQUETBOL | 1 | R99 |
| Honorarios | EXPOSITORA | 1 | R99 |
| Honorarios | FOTOGRAFO DEPTO OF. COMUNICACIONES | 1 | R99 |
| Honorarios | FOTOGRAFO. OF. COMUNICACIONES | 1 | R99 |
| Honorarios | FOTOGRAFOTO OF. COMUNCACIONES | 1 | R99 |
| Honorarios | FOTOGRAFOTO OF. COMUNICACIONES | 1 | R99 |
| Honorarios | GESTION VECINAL DIRECCION DE ASEO Y ORNATO | 1 | R99 |
| Honorarios | GESTION VECINAL DIRECCIÓN DE ASEO Y ORNATO | 1 | R99 |
| Honorarios | GESTOA DE CASOS OLN | 1 | R99 |
| Honorarios | GESTOR CULTURAL DIRECCIÓN CULTURA, ARTES Y PATRIMONIO | 1 | R98 |
| Honorarios | GESTOR CULTURAL. DIRECCIÓN DE CULTURA, ARTE Y PATRIMONIO | 1 | R98 |
| Honorarios | GESTOR OF. DE TRANSITO | 1 | R98 |
| Honorarios | GESTOR VECINAL DIRECCION DE MEDIOAMBIENTE | 1 | R98 |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE TRANSITP | 1 | R98 |
| Honorarios | GESTOR VECINAL OF. PARTICIPACIÓN CIUDADANA | 1 | R98 |
| Honorarios | GESTOR VECINALDIRECCIÓN DE ASEO Y ORNATO | 1 | R98 |
| Honorarios | GESTOR VECINALL | 1 | R98 |
| Honorarios | GESTOR VECINALL DIRECCIÓN DE MEDIO AMBIENTE | 1 | R98 |
| Honorarios | GESTORA VECINAL DIRECCIÒN DE TRANSITO | 1 | R98 |
| Honorarios | GESTORA VECINAL DIRECCIÓN DE MEDIO AMBIENTE | 1 | R98 |
| Honorarios | INFOMATICO | 1 | R99 |
| Honorarios | INSTRUCTOR KICKBOXING | 1 | R99 |
| Honorarios | INSTRUCTORA DE FUTBOL OF. DEPORTES | 1 | R99 |
| Honorarios | INSTRUCTORA DE YOGA | 1 | R99 |
| Honorarios | INSTRUCTORA YOGA DEPTO DE LA MUJER | 1 | R99 |
| Honorarios | INTERPRETE DE LENGUAJE DE SEÑAS CUENTA PUBLICA | 1 | R99 |
| Honorarios | INTERPRETE DE LENGUAS DE SEÑAS | 1 | R99 |
| Honorarios | INTERPRETE LENGUA DE SEÑAS CUENTA PUBLICA | 1 | R99 |
| Honorarios | LOCUTOR OF. COMUNICACIONES | 1 | R99 |
| Honorarios | MANTENIENTO CANCHA NUEVO AMANECER | 1 | R99 |
| Honorarios | MANTENIMIENTO Y CUIDADO RECIENTOS DEPORTIVOS | 1 | R97 |
| Honorarios | MONITA DE YERBAS MEDICINALES TALLER DE MUJERES | 1 | R98 |
| Honorarios | MONITA DEPORTIVA OF. DEPORTES | 1 | R98 |
| Honorarios | MONITA PROGRAMA PIAM ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITA TALLERES DEPORTIVO | 1 | R98 |
| Honorarios | MONITO DE ALFABETIZACIÓN DIGUITAL | 1 | R98 |
| Honorarios | MONITO DE FUTBOL OF. DE DEPORTE | 1 | R98 |
| Honorarios | MONITOA PROGRAMAS PIAM ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR ARTES TEATRALES | 1 | R98 |
| Honorarios | MONITOR CIRCENCE | 1 | R98 |
| Honorarios | MONITOR DE ALFABERIZACIÓN ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR DE ALFABETIZACION DIGITAL CASA DEL ADULTOO MAYOR | 1 | R98 |
| Honorarios | MONITOR DE ALFABETIZACIÓN ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR DE ALFABETIZACIÓN DIGUETAL | 1 | R98 |
| Honorarios | MONITOR DE ALFABETIZACIÓN DIGUITAL | 1 | R98 |
| Honorarios | MONITOR DE ALFABETIZACIÓON DIGUITAL | 1 | R98 |
| Honorarios | MONITOR DE ARTES | 1 | R98 |
| Honorarios | MONITOR DE COCINA ESCUELA DE VERANO | 1 | R98 |
| Honorarios | MONITOR DE DANZA OF. DISCAPACIDAD | 1 | R98 |
| Honorarios | MONITOR DE DEPORTE | 1 | R98 |
| Honorarios | MONITOR DE FUTBOL DEPTO DEPORTES | 1 | R98 |
| Honorarios | MONITOR DE FUTBOL OF. DE DEPORTES | 1 | R98 |
| Honorarios | MONITOR DE FUTBOL OF. DEPORTIVO | 1 | R98 |
| Honorarios | MONITOR DE HERTEROFILIA OF DEPORTE | 1 | R98 |
| Honorarios | MONITOR DE JIUTIITSU | 1 | R98 |
| Honorarios | MONITOR DE JIUTITSU | 1 | R98 |
| Honorarios | MONITOR DE JIUTUTSU | 1 | R98 |
| Honorarios | MONITOR DE PATINAJE OFICINA DE DEPORTES | 1 | R98 |
| Honorarios | MONITOR DE PROG. DE 4 A 7 | 1 | R98 |
| Honorarios | MONITOR DE PROGRAMA VINCULO ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR DE PROGRAMAN VINCULO ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR DE TALLER CIRCO-TEATRO | 1 | R98 |
| Honorarios | MONITOR DE TALLER DE BATUCADA | 1 | R98 |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTES Y TALLER DE MUJERES | 1 | R98 |
| Honorarios | MONITOR EDUCATIVO DE 4 A 7 | 1 | R98 |
| Honorarios | MONITOR FOTOGRAFIA | 1 | R98 |
| Honorarios | MONITOR PROG. VÍNCULO ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR PROGRAMA VINCULO ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITOR TALLER DANZA URBANA | 1 | R98 |
| Honorarios | MONITOR TALLER DE BATUCADA | 1 | R98 |
| Honorarios | MONITORA ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA ALFABETIZACIÓN DIGITAL | 1 | R98 |
| Honorarios | MONITORA ALFABETIZACIÓN DIGITAL CASA DEL ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA ALFABETIZACIÓN DIGUITAL | 1 | R98 |
| Honorarios | MONITORA ALFARERIA TALLERES DE MUJERES | 1 | R98 |
| Honorarios | MONITORA ARTES TREATRALES | 1 | R98 |
| Honorarios | MONITORA ARTISTICA | 1 | R98 |
| Honorarios | MONITORA BAIEL KPOP OF. JOVENES | 1 | R98 |
| Honorarios | MONITORA COMUNITARIA O.P.D | 1 | R98 |
| Honorarios | MONITORA DANZA ARABE | 1 | R98 |
| Honorarios | MONITORA DE ARTES MARCOAÑES | 1 | R98 |
| Honorarios | MONITORA DE BARTENER Y GARONERIA | 1 | R98 |
| Honorarios | MONITORA DE DANZA FLOKLORICA CASA DEL ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA DE DANZA OF. DE DISCAPACIDAD | 1 | R98 |
| Honorarios | MONITORA DE DANZA TALLERES DE MUJERES | 1 | R98 |
| Honorarios | MONITORA DE DANZA TRIVAL TALLERES DE MUJERES | 1 | R98 |
| Honorarios | MONITORA DE DAZNA FOLKLORICA CASA DEL ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA DE FOLCLOR CASA DEL ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA DE MANUALIDAD | 1 | R98 |
| Honorarios | MONITORA DE ORFEBRERÍA TALLERES DE MUJERES | 1 | R98 |
| Honorarios | MONITORA DE PINTURA ASFALTICA | 1 | R98 |
| Honorarios | MONITORA DE PROGRAMA 4A 7 | 1 | R98 |
| Honorarios | MONITORA DE PROGRAMA DE 4 A 7 | 1 | R98 |
| Honorarios | MONITORA DE REPOSTERIA | 1 | R98 |
| Honorarios | MONITORA DE RESPOSTERIA OF. ADULTO MAYO | 1 | R98 |
| Honorarios | MONITORA DE RESPOSTERIA OF. ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA DE SUBLIMACION | 1 | R98 |
| Honorarios | MONITORA DE SUBLIMACION OF. DISCAPCIDAD | 1 | R98 |
| Honorarios | MONITORA DE SUBLIMACIONES OF. DISCAPACIDAD | 1 | R98 |
| Honorarios | MONITORA DE TALLER DANZA FOLCKORICA | 1 | R98 |
| Honorarios | MONITORA DE TALLER DE BATUCADA | 1 | R98 |
| Honorarios | MONITORA DE TALLER DE BODYBOARD | 1 | R98 |
| Honorarios | MONITORA DE TALLER DE DANZA | 1 | R98 |
| Honorarios | MONITORA DE TALLER DE DANZA FOLCKORICA | 1 | R98 |
| Honorarios | MONITORA DE TALLER DE MUJERES | 1 | R98 |
| Honorarios | MONITORA DE ZUMBA. OF. DEPORTES | 1 | R98 |
| Honorarios | MONITORA DEPTO. DE LA MUJER | 1 | R98 |
| Honorarios | MONITORA DERPORTES OF. DEPORTES | 1 | R98 |
| Honorarios | MONITORA ESTIMULACION TEMPRANA CHILE CRECE CONTIGO | 1 | R98 |
| Honorarios | MONITORA FITNETSS | 1 | R98 |
| Honorarios | MONITORA JURIDICA CENTRO DE LA MUJER | 1 | R98 |
| Honorarios | MONITORA OF. DEPORTES | 1 | R98 |
| Honorarios | MONITORA OFICINA DE DEPORTES | 1 | R98 |
| Honorarios | MONITORA PATÍN OF. DEPORTES | 1 | R98 |
| Honorarios | MONITORA PORCELANA EN FRÍO TALLERES DE MUJERES | 1 | R98 |
| Honorarios | MONITORA PROGRAMA ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA REPOSTERÍA OF. ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA RESPOSTERIA | 1 | R98 |
| Honorarios | MONITORA TALLER DE BATUCADA | 1 | R98 |
| Honorarios | MONITORA TALLER DE DANZA | 1 | R98 |
| Honorarios | MONITORA TALLER DE DANZA FOLKLORICA ADULTO MAYOR | 1 | R98 |
| Honorarios | MONITORA TALLER DE DANZA FOLKLORICA PARA ADULTOS MAYORES | 1 | R98 |
| Honorarios | MONITORA TELAR MAPUCHE | 1 | R98 |
| Honorarios | MONITORA ZUMBA OF DEPORTES | 1 | R98 |
| Honorarios | MONITORA ZUMBA OF. JOVENES | 1 | R98 |
| Honorarios | MONITORA ZUMBA. OF. DEPORTES | 1 | R98 |
| Honorarios | MONITORCAMARA DIRECCION DE SEGURIDAD PUBILICA | 1 | R99 |
| Honorarios | MONUNICADOR AUDIOVISUAL OF. COMUNICACIONES | 1 | R99 |
| Honorarios | MURALISTA DEPTO DE LA MUJER Y E.G | 1 | R99 |
| Honorarios | MURALISTAS | 1 | R99 |
| Honorarios | OPERADOR DE RELOJ PLAZA 21 MAYO | 1 | R99 |
| Honorarios | ORADOR | 1 | R99 |
| Honorarios | PARTICIPACION DE DIAGNOSTICO Y PLANIFICACIÓN CDM | 1 | R97 |
| Honorarios | PARTICIPACIÓN DE DIAGNOSTICOS Y PLANIFICACION CDM | 1 | R97 |
| Honorarios | PREVENCIONISTA | 1 | R99 |
| Honorarios | PREVENCIONISTA DE RIEGO | 1 | R99 |
| Honorarios | PREVENCIONISTA DE RIEGOS OF. RIESGO | 1 | R99 |
| Honorarios | PREVENCIONISTA DE RIEGOS. OF. RIESGO | 1 | R99 |
| Honorarios | PREVENCIONISTA DE RIESGO OF. RIESGTO | 1 | R99 |
| Honorarios | PREVENCIONISTRA DE RIESGO | 1 | R99 |
| Honorarios | PREVENCIONITA DE RIESGO | 1 | R99 |
| Honorarios | PRODUCTORA AUDIVISUAL CONSERVADORA | 1 | R99 |
| Honorarios | PROFESOR DEE PATINAJE | 1 | R99 |
| Honorarios | PROG 4 A 7 | 1 | R97 |
| Honorarios | PROG SOCIALES | 1 | R97 |
| Honorarios | PROGRAMA INDAP | 1 | R97 |
| Honorarios | PROGRAMA JEFAS DE HOGAR | 1 | R97 |
| Honorarios | PSIQUIATRICA CENTRO ANUN | 1 | R99 |
| Honorarios | RELATADORA | 1 | R99 |
| Honorarios | RELATORA FUNDACION ANTONIA | 1 | R98 |
| Honorarios | RELATORA OF. BECAS | 1 | R98 |
| Honorarios | REMODELACION PLAZA SCHWAGER | 1 | R97 |
| Honorarios | TALLER DE ARTESANIA Y MANUELIDADES | 1 | R98 |
| Honorarios | TALLER DE DANZA | 1 | R98 |
| Honorarios | TALLER DE GARZONERIA | 1 | R98 |
| Honorarios | TALLER DE MANUALIDADES EN PORCELANA EN FRIO | 1 | R98 |
| Honorarios | TALLER DE NATACION | 1 | R98 |
| Honorarios | TALLER DE NATACIÓN | 1 | R98 |
| Honorarios | TALLER DE ORFARERIA | 1 | R98 |
| Honorarios | TALLER DE YOGA | 1 | R98 |
| Honorarios | TITIRITERO OF. JOVENES | 1 | R99 |
| Honorarios | TRABAJO EN ARTES VISUELES | 1 | R99 |
| Honorarios | TRABAJO SOCIAL ADULTO MAYOR | 1 | R99 |
| Honorarios | TRABAJO SOCIAL CASA ADULTO MAYOR | 1 | R99 |
| Honorarios | TRABAJO SOCIAL SEPLAN | 1 | R99 |

## 7. Tabla de mapeo completa

La tabla contiene 1.651 filas, una por categoría y cargo exacto.

| Categoría | Cargo original | Frecuencia | Estamento(s) publicado(s) | Estamento estimado | Regla | Justificación |
|---|---|---|---|---|---|---|
| Código del Trabajo | AUXILIAR DE SERVICIO | 535 | Administrativo: 535 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Código del Trabajo | SALVAVIDAS | 99 | Administrativo: 99 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Código del Trabajo | SECRETARIA OFIC. CEMENTERIO MU | 72 | Administrativo: 72 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | AUXILIAR DE SERVICIO CEMENTERIO | 70 | Administrativo: 70 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Código del Trabajo | ADMINISTRADOR CEMENTERIO MUNIC | 36 | Administrativo: 36 | Jefatura | R04 | Administración o subadministración de una unidad municipal específica. |
| Código del Trabajo | JEFA DEPTO. GAB. PSICOTECNICO | 33 | Técnico: 33 | Jefatura | R02 | Jefatura de departamento explícita en el cargo. |
| Código del Trabajo | SECRETARIA | 15 | Administrativo: 15 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | SECRETARIA DEPTO CONTABILIDAD | 13 | Administrativo: 13 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | GASFITER | 12 | Otro: 12 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Código del Trabajo | SUBADMINISTRADOR CEMENTERIO MU | 11 | Administrativo: 11 | Jefatura | R04 | Administración o subadministración de una unidad municipal específica. |
| Código del Trabajo | SUBADMINISTRADOR CEMENTERIO | 7 | Administrativo: 7 | Jefatura | R04 | Administración o subadministración de una unidad municipal específica. |
| Código del Trabajo | COMPRADOR MERCADO PUBLICO | 5 | Otro: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | APOYO ADM. CHILECOMPRA | 4 | Otro: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | ENCARGADO DE ESTADISTICA | 4 | Otro: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Código del Trabajo | APOYO TRANSITO | 3 | Otro: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Código del Trabajo | MEDICO DIRECCIÓN DE TRANSITO | 3 | Profesional: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Código del Trabajo | JEFA DEPTO. GAB. PSICOTÉCNICO | 2 | Otro: 2 | Jefatura | R02 | Jefatura de departamento explícita en el cargo. |
| Código del Trabajo | MEDICO PSICOTECNICO | 2 | Profesional: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Código del Trabajo | ADMINISTRATIVO DIRECCION DE FINANZAS | 1 | Otro: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | COMPRADOR | 1 | Otro: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Código del Trabajo | ENCARGADO DE ESTADISTICAS | 1 | Otro: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Código del Trabajo | GABINETE PSICOTECNICO | 1 | Técnico: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Código del Trabajo | MEDICO | 1 | Profesional: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Código del Trabajo | MÉDICO CIRUJANO TRÁNSITO | 1 | Otro: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Código del Trabajo | OF. ADM. COMPRADOR CHILECOMPRA | 1 | Otro: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO FAMILIAR FAMILIAS INTEGRADAS | 267 | Honorarios: 267 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTES | 261 | Honorarios: 261 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE MANUALIDADES | 204 | Honorarios: 204 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL | 168 | Honorarios: 168 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PSICOLOGA CENTRO ANUN | 137 | Honorarios: 137 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITORA DEPORTIVA OF. DEPORTES | 126 | Honorarios: 126 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESORA SENIOR | 101 | Honorarios: 101 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TRABAJADOR SOCIAL CENTRO ANUN | 101 | Honorarios: 101 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | SUPERVISOR PROEMPLEO | 86 | Honorarios: 86 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | MONITORA ALBERGUE | 77 | Honorarios: 77 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | TÉCNICO EN REHABILITACION CENTRO ANUN | 72 | Honorarios: 72 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO FAMILIAR PROG. FAMILIAS INTEGRADAS | 68 | Honorarios: 68 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO DEPARTAMENTO | 60 | Honorarios: 60 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | OPERADOR DE CAMARAS | 59 | Honorarios: 59 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ENCUESTADOR REGISTRO SOCIAL DE HOGARES | 58 | Honorarios: 58 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | PSICOLOGO CENTRO ANUN | 58 | Honorarios: 58 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITORA PROGRAMA DE 4 A 7 | 55 | Honorarios: 55 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA VECINAL | 53 | Honorarios: 53 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL | 51 | Honorarios: 51 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA MANUALIDADES TALLERES DE MUJERES | 47 | Honorarios: 47 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TÉCNICO EN REHABILITACIÓN CENTRO ANUN | 46 | Honorarios: 46 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ASESORIA PERSONALIZADA ADULTOS MAYORES | 45 | Honorarios: 45 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TRABAJADORA SOCIAL CASA DE LA SEGURIDAD | 44 | Honorarios: 44 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADMINISTRATIVO | 42 | Honorarios: 42 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROFESIONAL SECPLAN | 40 | Honorarios: 40 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | GESTORA DE CASOS OLN | 40 | Honorarios: 40 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR ALBERGUE | 40 | Honorarios: 40 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITORA PROGRAMA PIAM ADULTO MAYOR | 40 | Honorarios: 40 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO ADM. DIRECCION DE TRANSITO | 39 | Honorarios: 39 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | INGENIERO AGRONOMO PRODESAL | 38 | Honorarios: 38 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TERAPEUTA OCUPACIONAL OMIL | 38 | Honorarios: 38 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | AUXILIAR DE SERVICIO CENTRO ANUN | 37 | Honorarios: 37 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE SOCIAL CENTRO ANUN | 36 | Honorarios: 36 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TERAPEUTA OCUPACIONAL CENTRO ANUN | 34 | Honorarios: 34 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL OPD | 33 | Honorarios: 33 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO FAMILIAR PROGRAMA FAMILIAS INTEGRADAS | 32 | Honorarios: 32 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | INGENIERO CONSTRUCTOR DIDECO | 32 | Honorarios: 32 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | OPERADOR DE RELOJ PLAZA 21 DE MAYO | 32 | Honorarios: 32 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | APOYO ADM. OMIL | 31 | Honorarios: 31 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | TRABAJADOR SOCIAL | 30 | Honorarios: 30 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITORA DE MANUALIDADES | 29 | Honorarios: 29 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TÉCNICO EN ENFERMERIA ALBERGUE MUNICIPAL | 29 | Honorarios: 29 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | AUXILIAR DE SERVICIOS CENTRO ANUN | 28 | Honorarios: 28 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | TOPOGRAFO SECPLAN | 28 | Honorarios: 28 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | COORD. CONTROL GESTION | 27 | Honorarios: 27 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | MANIPULADORA DE ALIMENTOS ALBERGUE MUNICIPAL | 27 | Honorarios: 27 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | APOYO ADM. DIRECCION DE SEGURIDAD | 26 | Honorarios: 26 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ASISTENTE SOCIAL SENDA PREVIENE | 26 | Honorarios: 26 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COORD. HABITABILIDAD | 26 | Honorarios: 26 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | INGENIERO CIVIL SECPLAN | 26 | Honorarios: 26 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MECANICO OF. TRANSPORTE | 26 | Honorarios: 26 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ENCUESTADOR RSH | 25 | Honorarios: 25 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ENCUESTADORA RSH | 25 | Honorarios: 25 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | INFORMATICO | 25 | Honorarios: 25 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTOR DE FUTBOL | 25 | Honorarios: 25 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | RECEPCIONISTA | 25 | Honorarios: 25 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ABOGADA EGIS MUNICIPAL | 24 | Honorarios: 24 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL HABITABILIDAD | 24 | Honorarios: 24 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL OLN | 24 | Honorarios: 24 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO TÉCNICO DIRECCIÓN DE MEDIO AMBIENTE | 23 | Honorarios: 23 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | PREVENCIONISTA DE RIESGO | 23 | Honorarios: 23 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | APOYO ADM. EGIS MUNICIPAL | 22 | Honorarios: 22 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROF. SENDAPREVIENE | 22 | Honorarios: 22 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL SENDA PREVIENE | 22 | Honorarios: 22 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | GUARDIA DE SEGURIDAD CENTRO ANUN | 22 | Honorarios: 22 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | TRABAJADORA SOCIAL CENTRO ANUN | 22 | Honorarios: 22 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL EGIS MUNICIPAL | 22 | Honorarios: 22 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. OF. JOVENES | 21 | Honorarios: 21 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ASISTENTE SOCIAL QUIERO MI BARRIO | 21 | Honorarios: 21 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COMUNICADOR AUDIOVISUAL OF. COMUNICACIONES | 21 | Honorarios: 21 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENSEÑANZA MEDIA COMPLETA | 21 | Honorarios: 21 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MONITOR DE FUTBOL OF. DEPORTES | 21 | Honorarios: 21 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PSICOLOGO OMIL | 21 | Honorarios: 21 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL EGIS MUNICIPAL | 21 | Honorarios: 21 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO ASESORIA JURIDICA | 20 | Honorarios: 20 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. DIRECCION DE MEDIO AMBIENTE | 20 | Honorarios: 20 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ASESOR SENIOR | 20 | Honorarios: 20 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TRABAJADORA SOCIAL SECPLAN | 20 | Honorarios: 20 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO DEPORTIVO OF. DEPORTES | 20 | Honorarios: 20 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO ADM. DEPTO REMUNERACIONES | 19 | Honorarios: 19 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROFESIONAL PREPARA2 | 19 | Honorarios: 19 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO SECPLAN | 19 | Honorarios: 19 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COORD. COMUNICACIONAL CASA DEL ADULTO MAYOR | 19 | Honorarios: 19 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE TURISMO | 19 | Honorarios: 19 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. TÉCNICA CENTRO ANUN | 19 | Honorarios: 19 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | EJECUTIVO DE EMPRESAS OMIL | 19 | Honorarios: 19 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MANIPULADORA DE ALIMENTOS ALBERGUE | 19 | Honorarios: 19 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITOR DE CAMARAS CASA DE LA SEGURIDAD | 19 | Honorarios: 19 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA ALBERGUE MUNICIPAL | 19 | Honorarios: 19 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | SECRETARIA EGIS MUNICIPAL | 19 | Honorarios: 19 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | TALLER DE DANZA TRIBAL | 19 | Honorarios: 19 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | DIGITADORA PROG. REGISTRO SOCIAL DE HOGARES | 18 | Honorarios: 18 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | MEDICO CENTRO ANUN | 18 | Honorarios: 18 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITOR DE CAMARAS | 18 | Honorarios: 18 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR DE CAMARAS DIRECCION DE SEGURIDAD PUBLICA | 18 | Honorarios: 18 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | PERIODISTA SENDAPREVIENE | 18 | Honorarios: 18 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL SENDAPREVIENE | 18 | Honorarios: 18 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA DIDECO | 17 | Honorarios: 17 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. CASA DE LA CULTURA | 17 | Honorarios: 17 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO EDUCATIVO PROGRAMA DE 4 A 7 | 17 | Honorarios: 17 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROF. DIRECCION DE ADM. Y FINANZAS | 17 | Honorarios: 17 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL DEPTO RRHH | 17 | Honorarios: 17 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | AUXILIAR DE ASEO ALBERGUE MUNICIPAL | 17 | Honorarios: 17 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | COORD. FINANCIERO Y ANALISTA CONTABLE | 17 | Honorarios: 17 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | DISEÑADOR GRAFICO DIDECO | 17 | Honorarios: 17 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTORA CULTURAL | 17 | Honorarios: 17 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA DE CASO OLN | 17 | Honorarios: 17 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PROFESOR DE PATINAJE | 17 | Honorarios: 17 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | SECRETARIA OF. CONCEJALES | 17 | Honorarios: 17 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. HABITABILIDAD | 16 | Honorarios: 16 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROFESIONA SECPLAN | 16 | Honorarios: 16 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROFESIONAL ADM. MUNICIPAL | 16 | Honorarios: 16 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARBITRO DE FUTBOL OF. DEPORTES | 16 | Honorarios: 16 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTORA TERRITORIAL OLN | 16 | Honorarios: 16 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TRABAJADOR SOCIAL CASA DE LA SEGURIDAD | 16 | Honorarios: 16 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ADMINISTRADOR GIMNASIO SCHWAGER | 15 | Honorarios: 15 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE TRANSITO | 15 | Honorarios: 15 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROFESIONAL BIBLIOTECA MUNICIPAL | 15 | Honorarios: 15 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COORD. DE SISTEMA DE SEGURIDAD | 15 | Honorarios: 15 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | DISEÑADOR DIDECO | 15 | Honorarios: 15 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MONITORA DE FUTBOL FEMENINO OF. DEPORTES | 15 | Honorarios: 15 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLER DE MUJERES | 15 | Honorarios: 15 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TÉCNICO EN ENFERMERIA EDIFICIO CONSISTORIAL | 15 | Honorarios: 15 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO ADM. OF. SUBSIDIO Y PENSIONES | 14 | Honorarios: 14 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DEPTO RRHH | 14 | Honorarios: 14 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO HABITABILIDAD | 14 | Honorarios: 14 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO CIERRE DEM | 14 | Honorarios: 14 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FAMILIAR PROG FAMILIAS INTEGRADAS | 14 | Honorarios: 14 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FAMILIAR, FAMILIAS INTEGRADAS | 14 | Honorarios: 14 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | COMUNICADOR AUDIOVISUAL DIDECO | 14 | Honorarios: 14 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORD. PROGRAMA DE 4 A 7 | 14 | Honorarios: 14 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PUEBLOS ORIGINARIOS | 14 | Honorarios: 14 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | INGENIERO CONSTRUCTOR EGIS MUNICIPAL | 14 | Honorarios: 14 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MEDICO PSIQUIATRA CENTRO ANUN | 14 | Honorarios: 14 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITOR DE ALTEROFILIA OF. DEPORTES | 14 | Honorarios: 14 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ZUMBA OF. DEPORTES | 14 | Honorarios: 14 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | RECEPCION DIDECO | 14 | Honorarios: 14 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | TRABAJADOR SOCIAL ANUN | 14 | Honorarios: 14 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL CENTRO DE LA MUJER | 14 | Honorarios: 14 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO EN CONSTRUCCION EGIS MUNICIPAL | 14 | Honorarios: 14 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO ADM. ADULTO MAYOR | 13 | Honorarios: 13 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE FINANZAS | 13 | Honorarios: 13 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. DE SUBSIDIO Y PENSIONES | 13 | Honorarios: 13 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO EGIS | 13 | Honorarios: 13 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROFESIONAL SENDAPREVIENE | 13 | Honorarios: 13 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | FONOAUDIOLOGA OF. DISCAPACIDAD | 13 | Honorarios: 13 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | FOTOGRAFO OF. COMUNICACIONES | 13 | Honorarios: 13 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOR DE CASOS OLN | 13 | Honorarios: 13 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | LOCUTOR DEPTO COMUNICACIONES | 13 | Honorarios: 13 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTIVO | 13 | Honorarios: 13 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PSIQUIATRA CENTRO ANUN | 13 | Honorarios: 13 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TECNICO EN REHABILITACION CENTRO ANUN | 13 | Honorarios: 13 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ABOGADO OLN | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. CENTRO ANUN | 12 | Honorarios: 12 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE ASEO Y ORNATO | 12 | Honorarios: 12 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO PROF. BIBLIOTECA MUNICIPAL | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL DEPTO PERSONAL | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO DOM | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | AUXILIAR DE SERVICIOS | 12 | Honorarios: 12 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | COORD. INFOCENTRO | 12 | Honorarios: 12 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | DIBUJANTE EGIS SECPLAN | 12 | Honorarios: 12 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ENCARGADA COMUNAL PMJ CORONEL | 12 | Honorarios: 12 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCUESTADOR PROG. REGISTRO SOCIAL DE HOGARES | 12 | Honorarios: 12 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | GESTOR VECINAL DIRECCION DE TRANSITO | 12 | Honorarios: 12 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE FUTBOL | 12 | Honorarios: 12 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE HERTEROFILIA OF. DEPORTES | 12 | Honorarios: 12 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TELEVIGILANCIA | 12 | Honorarios: 12 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA SOCIAL CENTRO DE LA MUJER | 12 | Honorarios: 12 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PROFESIONAL DE APOYO SENDA PREVIENE | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO SENDAPREVIENE | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA CENTRO DE LA MUJER | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL PREPARA2 SENDA | 12 | Honorarios: 12 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO AGRONOMO PRODESAL | 12 | Honorarios: 12 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ABOGADA DEPTO DE LA MUJER Y E.G | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. CASA DEL ADULTO MAYOR | 11 | Honorarios: 11 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OBRAS MUNICIPALES | 11 | Honorarios: 11 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO TÉCNICO DIRECCION DE MEDIO AMBIENTE | 11 | Honorarios: 11 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | COORD. SENDA PREVIENE | 11 | Honorarios: 11 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | DIBUJANTE ARQUITECTONICO EGIS | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | DIBUJANTE Y PROYECTISTA DIGUITAL | 11 | Honorarios: 11 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ENCARGADA DEPTO DE LA MUJER Y E.G | 11 | Honorarios: 11 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GUARDIA DE SEGURIDAD ANUN | 11 | Honorarios: 11 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITOR DEPORTES | 11 | Honorarios: 11 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PSICOLOGA PROGRAMA LAZOS | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO LABORAL OMIL | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO OPD | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | SALVAVIDAS | 11 | Honorarios: 11 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | SECRETARIA OF. DERECHOS HUMANOS | 11 | Honorarios: 11 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SECRETARIA OPD | 11 | Honorarios: 11 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SUPERVISORA PROEMPLEO | 11 | Honorarios: 11 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | TRABAJADOR SOCIAL EGIS | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO EN ENFERMERIA DIDECO | 11 | Honorarios: 11 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | VETERINARIO MEDIO AMBIENTE | 11 | Honorarios: 11 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA CENTRO DE LA MUJER | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. DEPTO DE LA MUJER Y E.G | 10 | Honorarios: 10 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE CULTURA, ARTE Y PATRIMONIO | 10 | Honorarios: 10 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. SENDA PREVIENE | 10 | Honorarios: 10 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO EGIS MUNICIPAL | 10 | Honorarios: 10 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FEMILIAR PROG. FAMILIAS INTEGRADAS | 10 | Honorarios: 10 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OF. INFORMACIONES | 10 | Honorarios: 10 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROFESIONAL | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL EN ADM. MUNICIPAL | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL PROGRAMA PREPARA2 | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COMUNICADOR AUDIOVISUAL CASA DE LA CULTURA | 10 | Honorarios: 10 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORD. GENERAL SUPERVISOR PROEMPLEO | 10 | Honorarios: 10 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PROEMPLEO ISLA SANTA MARIA | 10 | Honorarios: 10 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. SENDAPREVIENE | 10 | Honorarios: 10 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR PRO EMPLEOS ISLA SANTA MARIA | 10 | Honorarios: 10 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA ASUNTOS RELIGIOSOS | 10 | Honorarios: 10 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EJECUTIVO ATENCION DE EMPRESAS OMIL | 10 | Honorarios: 10 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENC. CASA DEL ADULTO MAYOR | 10 | Honorarios: 10 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCUESTADORA REGISTRO SOCIAL DE HOGARES | 10 | Honorarios: 10 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | GESTORA PATRIMONIAL | 10 | Honorarios: 10 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ING. CIVIL SECPLAN | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MAESTRO CARPINTERO HABITABILIDAD | 10 | Honorarios: 10 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITORA PROGRAMAS PIAM ADULTO MAYOR | 10 | Honorarios: 10 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PERIODISTA DEPTO COMUNICACIONES | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA O.P.D. INFANCIA | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | SOCIOLOGO OF. PARTICIPACION CIUDADANA | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TALLER DE RECICLAJE | 10 | Honorarios: 10 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TRABAJADORA SOCIAL CDM | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO EN CONSTRUCCIÓN EGIS MUNICIPAL | 10 | Honorarios: 10 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | VETERINARIO DIRECCION DE MEDIO AMBIENTE | 10 | Honorarios: 10 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA EGIS | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO OPD | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. EGIS | 9 | Honorarios: 9 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO JURIDICO ASESORIA JURIDICA | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PERIODISTICO SENDA PREVIENE | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO TÉCNICO CASA DE LA SEGURIDAD | 9 | Honorarios: 9 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ASISTENTE SOCIAL | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ATENCION DE CASOS SOCIALES | 9 | Honorarios: 9 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | AUXILIAR DE ASEO ALBERGUE | 9 | Honorarios: 9 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | COORD. CASA DEL ADULTO MAYOR | 9 | Honorarios: 9 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | ENFERMERA VIVIENDAS TUTELADAS | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE TRANSITO | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ARTES TEATRALES | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA OF. DISCAPACIDAD | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA FUTBOL FEMENINO OF. DEPORTES | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | OPERADOR AUDIOVISUAL CASA DE LA CULTURA | 9 | Honorarios: 9 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | PSICOLOGA DEPTO DE LA MUJER Y E.G | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA PARENTALIDAD | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA SENDAPREVIENE | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO OPD INFANCIA | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TALLER DE ORFERERIA | 9 | Honorarios: 9 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TERAPEUTA OCUPACIONAL ANUN | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL HABITABILIDAD | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL DIRECCION DE SEGURIDAD PUBLICA | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO EN REHABILITACION ANUN | 9 | Honorarios: 9 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | VETERINARIO DIRECCIÓN DE MEDIO AMBIENTE | 9 | Honorarios: 9 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO DIRECCIÓN DE MEDIO AMBIENTE | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCION DE CULTURA | 8 | Honorarios: 8 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO CASA DE LA SEGURIDAD | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD DIRECCION DE SEGURIDAD PUBLICA | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PARTICIPACION CIUDADANA | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROF. PARTICIPACION CIUDADANA | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL EN ADMINISTRACION MUNICIPAL | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL OF. DISCAPACIDAD | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO SOCIAL OF. ADULTO MAYOR | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | COORD.FINAC Y ANALISTA CONTABLE PROEMPLEO | 8 | Honorarios: 8 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | ENTRENADOR DE FUTBOL | 8 | Honorarios: 8 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOR VECINAL OF. PARTICIPACION CIUDADANA | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | INGENIERO COMERCIAL DIRECCIÓN DE FINANZAS | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO OLN | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MECANICO DEPTO DE TRANSPORTE | 8 | Honorarios: 8 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MEDICO PSIQUIATRA ANUN | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITORA DEPORTES | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROG. DE 4 A 7 | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA CRECER EN COMUNIDAD | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | OPERADOR SOCIAL | 8 | Honorarios: 8 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PROFESIONAL OPD | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL PROG. PSICOSOCIAL | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA ANUN | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA CASA DE LA SEGURIDAD | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA OPD | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | REHAB. CENTRO ANUN | 8 | Honorarios: 8 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | SUPERVISORA EQUIPO DEM | 8 | Honorarios: 8 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | TALLER DE MANUALIDADES PORCELANA EN FRIO | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE YOGA PARA MUJERES | 8 | Honorarios: 8 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TRABAJADORA SOCIAL DIRECCIÓN DE SEGURIDAD | 8 | Honorarios: 8 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJO EN ARTES VISUALES | 8 | Honorarios: 8 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ABOGADO TRANSPARENCIA SECRETARIA MUNICIPAL | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ACOMPAÑAMIENTO FAMILIAR POR. PSICOSOCIAL | 7 | Honorarios: 7 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | APOYO ADM. DEPTO. REMUNERACIONES | 7 | Honorarios: 7 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE SEGURIDAD | 7 | Honorarios: 7 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. ISLA SANTA MARIA | 7 | Honorarios: 7 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DEPTO PERSONAL | 7 | Honorarios: 7 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO DEPORTIVO | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN P.C.V. | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FAMILIAR PROG PSICOSOCIAL | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROF. SECPLAN | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL PARTICIPACION CIUDADANA | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE DE APOYO PEDAGOGICO | 7 | Honorarios: 7 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE SOCIAL CASA DE LA SEGURIDAD | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL SECPLAN | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | CARPINTERO HABITABILIDAD | 7 | Honorarios: 7 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | COODINADOR COMUNICACIONES | 7 | Honorarios: 7 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ARTISTICO OF. JOVENES | 7 | Honorarios: 7 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. OPD INFANCIA | 7 | Honorarios: 7 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR PROEMPLEO | 7 | Honorarios: 7 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA | 7 | Honorarios: 7 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DIRECTOR DE PROYECTOS CULTURALES DIRECCION DE CULTURA | 7 | Honorarios: 7 | Directivo | R01 | Dirección explícita de proyectos o funciones; estimación funcional, no confirmación de directivo municipal formal. |
| Honorarios | GESTOR CULTURAL EN EJECUCION DE OBRAS | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | KINESIOLOGO CHILE CRECE CONTIGO | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO OF. DISCAPACIDAD | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITOR ALBERGUE MUNICIPAL | 7 | Honorarios: 7 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITOR DE PATINAJE OF. DEPORTES | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE VOLEIBOL | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR PROGRAMA DE 4 A 7 | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DANZA OF. DISCAPACIDAD | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE FOLKLORE CASA DEL ADULTO MAYOR | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE MANUALIDADES OF. DISCAPACIDAD | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE YERBAS MEDICINALES | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DEPORTIVA OF. DE DEPORTES | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA FITNES | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA MODA TALLERES DE MUJERES | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA VINCULOS ADULTO MAYOR | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA REPOSTERIA OF. ADULTO MAYOR | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLER DE FLAMENCO | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA YERBAS MEDICINALES TALLERES DE MUJERES | 7 | Honorarios: 7 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | PERIODISTA OF. COMUNICACIONES | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO PREPARA2 SENDA | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | SUPERVISOR CAMARAS DE SEGURIDAD | 7 | Honorarios: 7 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | SUPERVISOR PRO EMPLEOS | 7 | Honorarios: 7 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | TRABAJADOR SOCIAL OPD | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL SENDA PREVIENE | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL OF. VIVIENDA | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL PROGRAMA DE 4 A 7 | 7 | Honorarios: 7 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA ASESORIA JURIDICA | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA DEPTO DE LA MUJER Y EG | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ADM. GIMNASIO SCHWAGER | 6 | Honorarios: 6 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. CASA DE LA SEGURIDAD | 6 | Honorarios: 6 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEPTO EJECUCION DE OBRAS | 6 | Honorarios: 6 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. EN DIRECCION DE TRANSITO | 6 | Honorarios: 6 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. JOVENES Y MONITORA DE AUTODEFENSA DEPTO. DE LA MUJER | 6 | Honorarios: 6 | No clasificable | R00 | Combina apoyo administrativo y monitoreo; el texto no permite asignar un único estamento funcional. |
| Honorarios | APOYO ADM. OFICINA CONCEJALES | 6 | Honorarios: 6 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OF. CONCEJALES | 6 | Honorarios: 6 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO DIRECCION DE CONTROL | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN P.C.V | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO DIRECCION DE CONTROL | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO EN GABINETE | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROF. SENDA PREVIENE | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO TÉCNICO PROFESIONAL DIRECCIÓN DE SEGURIDAD PUBLICA | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO - DOM | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO DIRECCION DE OBRAS MUNICIPALES | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASESOR EN PROGRAMA Y PLANIFICACION DE NUEVOS INGRESOS MUNICIPALES | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS MUNICIPALES TRANSITO | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASISTENTE DE APOYO PEDAGOGICO PROG. DE 4 A 7 | 6 | Honorarios: 6 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE SOCIAL OPD | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COORD. INFOCENTRO YOBILO | 6 | Honorarios: 6 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR ALBERGUE | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR DE COMUNICACIONES CASA DEL ADULTO MAYOR | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR HABITABILIDAD | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR INFOCENTRO YOBILO | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA CASA DEL ADULTO MAYOR | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PATRIMONIO | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PROG. PARENTALIDAD SENDA | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PUEBLOS INDIGENAS | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA SENDA PREVIENE | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA TECNICA CENTRO ANUN | 6 | Honorarios: 6 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | COORDINADORA TURISMO | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EDUCADORA SOCIAL OPD | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA COMUNAL PJM CORONEL | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA COMUNAL PMJ | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOR | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL DIRECCION DE CULTURA ARTE Y PATRIMONIO | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCION DE MEDIO AMBIENTE | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GUARDIA DE SEGURIDAD ANUN CENTRO ANUN | 6 | Honorarios: 6 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | INGENIERA AGRONOMO PRODESAL | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INSTRUCTOR DEPORTIVO | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTORA YOGA DEPTO. DE LA MUJER | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | LOCUTOR DEPT. COMUNICACIONES | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | LOCUTOR DEPTO. COMUNICACIONES | 6 | Honorarios: 6 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MECANICO DEPT. TRANSPORTE | 6 | Honorarios: 6 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITOR ALFABETIZACION DIGITAL CASA DEL ADULTO MAYOR | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE CAMARAS DIRECCIÓN DE SEGURIDAD PÚBLICA | 6 | Honorarios: 6 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR DE CICLISMO | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TELEVIGILANCIA | 6 | Honorarios: 6 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA DEPORTES OF. DEPORTES | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DEPORTES OF. DEPORTES Y TALLERES DE MUJERES | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA 4 A 7 SERNAMEG | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLERES DEPORTIVO | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ZUMBA OF. DEPORTES | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCIÓN DE CULTURA | 6 | Honorarios: 6 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | PROF. CASA DE LA SEGURIDAD | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. DE APOYO SENDAPREVIENE | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. PROG. PSICOSOCIAL | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO EN SENDA PREVIENE | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL SECPLAN | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DEPTO DE LA MUJER Y EG | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DIRECCIÓN DE SEGURIDAD | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA PREPARA2 SENDA | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TALLER DE TELAR MAPUCHE | 6 | Honorarios: 6 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TERAPEUTA OCUPACIONAL OF. DISCAPACIDAD | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TERAPEUTA OCUPACIONAL RED LOCAL DE APOYO Y CUIDADO | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL OF. ADULTO MAYOR | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL RED LOCAL DE APOYO Y CUIDADO | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL CHILE CRECE CONTIGO | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL O.P.D. INFANCIA | 6 | Honorarios: 6 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA CDM | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO CDM | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO DIRECCION DE MEDIO AMBIENTE | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO DIRECCION MEDIO AMBIENTE | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO OFICINA O.P.D. INFANCIA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO OFICINA OPD | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. ADULTO MAYOR CENTSA ANUN | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE ADM Y FINANZAS | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE CULTURA | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. ADULTO MAYOR | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. SUBSIDIOS Y PENSIONES | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO CULTURA | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURICO ASESORIA JURIDICA | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO DIRECCIÓN DE CONTROL | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROFESIONAL ADMINISTRACION MUNICIPAL | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARBITRO DE FUTBOOL OF. DEPORTE | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASESOR FINANCIERO Y PLANIFICACION DE NUEVOS INGRESOS | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASISTENTE SOCIAL PROG. TRANSFORMANDO BARRIOS | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL SENDAPREVIENE | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ATENCIÓN DE CASOS SOCIALES | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | AUX. DE SERVICIOS ANUN | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | AUXILIAR DE SERVICIOS ALBERGUE MUNICIPAL | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | CONSTRUCTORA CIVIL SECPLAN | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COORD. ARTISTICO OF. DE JOVENES | 5 | Honorarios: 5 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL SUPERVISOR EN TERRENO | 5 | Honorarios: 5 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR AREA ARTISTICA OF. JOVENES | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR GENERAL DE SUPERVISION EN TERRENO Y ADMINISTRATIVO PRO EMPLEOS | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | COORDINADOR SISTEMA SEGURIDAD ELECTRONICA DIRECCION SEGURIDAD PUBLICA | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA ASENTAMIENTOS PRECARIOS | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA CENTRO DE LA MUJER | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA CHILE CRECE CINTIGO | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA O.P.D. INFANCIA | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA OPD | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PROGRAMA DE 4 A 7 | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | CORDINADORA PROGRAMA DE 4 A 7 | 5 | Honorarios: 5 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | DIBUJANTE SECPLAN | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | DISEÑADOR PLAN DE ACCIÓN OPD | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DE GESTORES TERRITORIALES OLN | 5 | Honorarios: 5 | Jefatura | R03 | Encargo explícito de equipo de gestores territoriales. |
| Honorarios | ENCUSTADORA PROG. REGISTRO SOCIAL DE HOGARES | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | GESTOR CULTURAL DIRECCION CULTURA, ARTES Y PATRIMONIO | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL, DIRECCION DE CULTURA, ARTE Y PATRIMONIO | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCION DE ASEO Y ORNATO | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE MEDIO AMBIENTE | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA VECINAL DIRECCION DE TRANSITO | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | INGENIERO COMERCIAL OF. PARTICIPACION CIUDADANA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO COMERCIAL PARTICIPACIÓN CIUDADANA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INSTRUCTORA DEPORTIVA OF. DEPORTES | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | KINESIOLOGO PROG. CHILE CRECE CONTYIGO | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MANIPULADORA DE ALIMENTOS | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MECANICO DEPTO. TRANSPORTE | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITOR DE BASQUETBOL, OF. DEPORTES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE PATINAJE EN POLIDEPORTIVO | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DEPORTIVO | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA COMUNITARIA O.P.D. | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DANZA TRIVAL TALLERES DE MUJERES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ALFABETIZACIÓN DIGUITAL | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ARTES TEATRALES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE BARTENER Y GARSONERIA | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE CAMARAS | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA DEPORTIVA OF. DEPORTIVA | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ORFEBRERIA TALLERES DE MUJERES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PATIN OF. DEPORTES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PORCELANA EN FRIO TALLERES DE MUJERES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROG. VINCULO ADULTO MAYOR | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA RECICLAJE TALLERES DE MUJERS | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA SOCIAL | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLERES DE MUJERES | 5 | Honorarios: 5 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TELEVIGILANCIA DIRECCION SEGURIDAD PUBLICA | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA VESPERTINO ALBERGUE | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MURALISTAS DIRECCIÓN DE CULTURA | 5 | Honorarios: 5 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCION CULTURA, ARTES Y PATRIMONIO | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE CAMARAS DIRECCION SEGURIDAD PUBLICA | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE MAQUINARIA | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | OPERADORA DE CAMARAS | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | PERIODISTA SENDA PREVIENE | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO ALBERGUE | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DIRECCION DE SEGURIDAD | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DIRECCION SEGURIDAD PUBLICA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO O.P.D. INFANCIA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO PREPARADOS | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO PROGRAMA LAZOS | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | SALVAVIDAS POLIDEPORTIVO | 5 | Honorarios: 5 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | SECRETARIA O.P.D. INFANCIA | 5 | Honorarios: 5 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SUPERVISOR DE CAMARAS DIRECCION SEGURIDAD PUBLICA | 5 | Honorarios: 5 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | T.E.N.S. EN EDIFICIO CONSISTORIAL | 5 | Honorarios: 5 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TRABADORA SOCIAL DIRECCION DE SEGURIDAD PUBLICA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL O.P.D. INFANCIA | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL OF. DISCAPACIDAD | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL PROG. 4 A 7 | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO CANIL MUNICIPAL | 5 | Honorarios: 5 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO A. MAYOR | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO CENTRO DE LA MUJER | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ADM. PROG. REG SOCIAL DE HOGARES | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ADMINISRATIVA EGIS | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. ADMINISTRACION MUNICIPAL | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEM | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE FINANZAS | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. GESTORES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF PROEMPLEOS | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OFICINA DE JOVENES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. SEGURIDAD PUBLICA | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. SENDA | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO CASA DEL ADULTO MAYOR | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCIÓN DE MEDIO AMBIENTE | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO EGIS MUNICIPAL | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OF. INFORMACIONES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OPD | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ASEO Y ORNATO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO BIBLIOTECA | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO CASA ADULTO MAYOR | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO CENTRO DE LA MUJER | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO DIRECCION DE TRANSITO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN COORD. Y COBRANZAS | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN PCV | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD CASA DE LA SEGURIDAD | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FINANZAS MUNICIPAL | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO GABINETE MUNICIPAL | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO MECANICO DEPTO TRANSPORTE | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | APOYO MEDIO AMBIENTE | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO MUJERES JEFA DE HOGAR | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OF PREVENCION DE RIESGOS | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OF. CULTURA | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OF. DE CONCEJALES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OF. DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OFICINA DE JOVENES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OPD | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROF. ADM. MUNICIPAL | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DIDECO | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DIRECCION DE ADM Y FINANZAS | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DIRECCIÓN DE ADM Y FINANZAS | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DISCAPACIDAD | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL INVENTARIO | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL PARTICIPACIÓN CIUDADANA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL RRHH | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROG.PROEMPLEO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO REG SOCIAL DE HOGARES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO TÉCNICO | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TÉCNICO EGIS MUNICIPAL | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ARQUITECTOR SECPLAN | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASESOR SENDA PREVIENE | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESORIA TECNICA PRODESAL | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ASISTENTE SOCIAL ANUN | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL SENDA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | AUXILIAR DE ASEO | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | AUXILIAR DE SERVICIO | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | COMUNICADOR AUDIVISUAL DIDECO | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COOR. PROEMPLEO ISLA SANTA MARIA | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD DE TURISMO | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ASUNTOS RELIGIOSO | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ASUNTOS RELIGIOSOS | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. OPD | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PROGRAMA DE 4 A 7 SERNAMEG | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PUEBLOS ORIGINARIOS CULTURA Y DEPORTES | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. SISTEMA DE SEGURIDAD | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. TÉCNICO CENTRO ANUN | 4 | Honorarios: 4 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR ALBERGUE MUNICIPAL | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR ALBERGUE- TEC. EN REHABILITACION CENTRO ANUN | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | COORDINADOR INFOCENTRO | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PUEBLOS ORIGINARIOS | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | Coordinador Infocentro OF. JOVENES | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DIGITADORA PROGRAMA REGISTRO SOCIAL DE HOGARES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | DIGITADORA REG. SOC. DE HOGARES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | DIGUITADORA PROG. REGISTR SOCIAL DE HOGARES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | DIRECTOR DE PROYECTOS CULTURALES | 4 | Honorarios: 4 | Directivo | R01 | Dirección explícita de proyectos o funciones; estimación funcional, no confirmación de directivo municipal formal. |
| Honorarios | DIRECTOR DE PROYECTOS CULTURALES DIRECCIÓN DE CULTURA | 4 | Honorarios: 4 | Directivo | R01 | Dirección explícita de proyectos o funciones; estimación funcional, no confirmación de directivo municipal formal. |
| Honorarios | EDUCADOR O.P.D. CORONEL | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EGIS MUNICIPAL | 4 | Honorarios: 4 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | ELECTRICO EGIS | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ENCARGADA PREVIENE | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMA PMJ CORONEL | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMA PREVENCION DE VIOLENCIA | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMA RED LOCAL DE APOYO Y CUIDADO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ENCARGADA TURISMO | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCUESTADOR REG SOCIAL DE HOGARES | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | EXPERTO OFICINA GABINETE | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | FONOAUDILOGA OF. DISCAPACIDAD | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | FOTOGRAFO DE OF. COMUNICACIONES | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOR CULTUYRAL DIRECCIÓN DE CULTURA | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE ASEO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | INSTRUCTORA KARATE OF. JOVENES | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | KINISIOLOGO OF. DISCAPACIDAD | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | LOCUTOR DEPTO DE COMUNICACIONES | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MAQUINISTA PRODESAL | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MECANICO DEPTO TRANSPORTE | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MECANICO OF. DEPORTES | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MEDICO ANUN | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITOR ALFABETIZACION DIGITAL | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR CAMARA CASA DE LA SEGURIDAD | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR CAMARAS CASA DE LA SEGURIDAD | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR DE ALFABETIZACION DIGUITAL | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE CÁMARAS DIRECCIÓN DE SEGURIDAD PÚBLICA | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR DE HALTEROFILIA OF. DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE HALTEROFILIA OFICINA DE DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DEPORTIVO OF DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR OTEC | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TENIS EF DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR VESPERTINO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA COMUNITARIA OPD | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA COMUNITARIA, PROGRAMA VINCULO | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA FOLCKLORICA | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA FOLKLORICA CASA DEL ADULTO MAYOR | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PROGRAMA ADULTO MAYOR | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE SUBLIMACION OF. DISCAPACIDAD | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DEPORTIVO OF. DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA EDUCACION FISICA | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PATINAJE OFICINA DE DEPORTES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRANAS PIAM ADULTO MAYOR | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TELEVIGILANCIA | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOREO DE CAMARAS | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE CAMARAS CASA DE LA SEGURIDAD | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | PERMISO CIRCULACION | 4 | Honorarios: 4 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PREPARADOR FISICO | 4 | Honorarios: 4 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PROF PARTICIPACION CIUDADANA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. ADMINISTRACION | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. MEDIO AMBIENTE | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. OF. VIVIENDA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. PROG PSICOSOCIAL | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. SENDA ACTUAR A TIEMPO | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. SENDA PREVIENE | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL PREVIENE | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFRSIONAL OF SEG. PUBLICA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROG. MINISTERIO CULTURA Y ARTES | 4 | Honorarios: 4 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PROG.PREVENC ALCOHOL SENDAS | 4 | Honorarios: 4 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PSICOLOGO SENDA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLÓGA OPD | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICÓLOGO OTEC | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | REPARTIDOR | 4 | Honorarios: 4 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | SECRETARIS EGIS MUNICIPAL | 4 | Honorarios: 4 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | TALLER DE ARTESANIA Y MANUALIDADES | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE FUTBOL | 4 | Honorarios: 4 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TEC. AGROP PRODESAL | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS ALBERGUE | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TRABAJADOR SOCIAL PARENTABILIDAD PREVIENE | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL ADULTO MAYOR | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL ANUN | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL BECAS | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL CHILECRECE CONTIGO | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL DE 4 A 7 | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL DIRECCIÓN DE SEGURIDAD PÚBLICA | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJOR SOCIAL SENDA PREPARA2 | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO EN EDIFICACION EGIS MUNICIPAL | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA ANUN | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN REHABILITACIÓN ANUN | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN REHABILITACIÓN, CENTRO ANUN | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO SECPLAN | 4 | Honorarios: 4 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | VETERINARIA DIRECCION DE MEDIO AMBIENTE | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIA MEDIO AMBIENTE | 4 | Honorarios: 4 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO EGIS MUNICIPAL | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ADMINISTRATIVO CASA DE LA CULTURA | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ANTROPOLOGO PROGRAMA QUIERO MI BARRIO | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO ADM. ANUN | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. CENTRO DE LA MUJER | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEPTO DE LA MUJER Y EG | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE CULTURA | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. EX DEM | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. BECAS | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. SECRETARIA MUNICIPAL | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO CASA DE LA CULTURA | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCION DE CULTURA ARTE Y PATRIMONIO | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCION DE SEGURIDAD PUBLICA | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCIÓN DE SEGURIDAD PUBLICA | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OIRS | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OMIL | 3 | Honorarios: 3 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO DEPARTAMENTO DIDECO | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO DIDECO | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO FAMILIAR | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO GABINETE | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROFESIONAL DEPTO TRANSPARENCIA | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL OF. COMUNICACIONES | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO TECNICO DIRECCION DE MEDIO AMBIENTE | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TECNICO EGIS MUNICIPAL | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TÉCNICO DIRECCIÓN DE SEGURIDAD | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TÉCNICO PROFESIONAL DIRECCION DE SEGURIDAD PUBLICA | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARBITRO DE FUTBOL OF. DE DEPORTES | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARQUITECTOR DOM | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASESOR EMPRENDIMIENTO FOMENTO PRODUCTIVO | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESORIA A MUJERES JEFAS DE HOGAR | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASISTENTE SOCIAL DIRECCION DE SEGURIDAD | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL DIRECCIÓN DE SEGURIDAD | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ATENCION DE CASOS | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | AUDIOVISUAL DIDECO | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICADOR AUDIO VISUAL, RELACIONES PUBLICAS | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COOR. TÉCNICA CENTRO ANUN | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ALBERGUE MUNICIPAL | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ARTISITICO OF. DE JOVENES | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. CHILE CRECE CONTIGO | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE ASENTAMIENTO PRECARIO | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE COMUNICACIONES | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE COMUNICACIONES CASA DEL ADULTO MAYOR | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE COMUNICACIÓN CASA DEL ADULTO MAYOR | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DEPTO DE LA MUJER Y EG | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PATRIMONIO | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PROGRAMA 4 A 7 | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PUEBLOS INDIGENAS | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. TURISMO | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR CUADRILLA EJECUCION DE OBRAS | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | CORDINADORA | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | DISEÑADOR GRAFICO | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENC. OF. JOVENES | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMA JEFAS DE HOGAR | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMA MUJERES CORONEL | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADO DE PROGRAMAS | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCUENTROS MURALISTAS | 3 | Honorarios: 3 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | ENFERMERA RED LOCAL DE APOYO Y CUIDADO | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | GESTOR CULTURAL EJECUCIÓN DE OBRAS | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR TERRITORIAL | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL FOMENTO PRODUCTIVO | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA TERRITORIA OLN | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA VECINAL DIRECCIÓN DE TRANSITO | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | INSTALACIONES ELECTRICAS | 3 | Honorarios: 3 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | INSTRUCOR DE FUTBOL | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTORA DEPORTIVA | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | KINESIOLOGA RED LOCAL DE APOYO Y CUIDADO | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO CHILECRECE CONTIGO | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO OF. DE DISCAPACIDAD | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO PRLAC | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MAESTRO CARPINTERO | 3 | Honorarios: 3 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MAESTRO DIRECCION DE CULTURA, ARTE Y PATRIMONIO | 3 | Honorarios: 3 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MANIPULADORA DE ALIEMENTO ALBERGUE MUNICIPAL | 3 | Honorarios: 3 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MANIPULADORA DE ALIMENTO ALBERGUE | 3 | Honorarios: 3 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITOR ALFABETIZACION DIGUITAL | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR ARTES VISUALES PROGRAMA DE 4 A 7 | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE BASQUETBOL OF. DEPORTES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE FÚTBOL OF. DEPORTES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR SOCIAL | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR ZUMBA | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA BATUCADA | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ARTES MARCIALES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DEPORTE | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DEPORTES OF. DEPORTES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE GARZONERIA | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE YERBAS MEDICINALES TALLER DE MUJERES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA LIDEREZAS | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA MANUALIDADES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA 4 A 7 | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA PIAM ADULTO MAYORES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLERES DEPORTIVOS | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TELAR MAPUCHE TALLERES DE MUJERES | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA VESPERTINA ALBERGUE | 3 | Honorarios: 3 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | OF DE JOVENES | 3 | Honorarios: 3 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | OF DEPORTES | 3 | Honorarios: 3 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | OPERADOR MAQUINISTA | 3 | Honorarios: 3 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | PERIODISTA SECPLAN | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PINTOR EJEC. OBRAS | 3 | Honorarios: 3 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | PROFESIONAL INDAP | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESOR DE EDUCACION FISICA CENTRO ANUN | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA PRLA | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | REGISTRO SOCIAL DE HOGARES | 3 | Honorarios: 3 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | SOCIOLOGO OF. PARTICIPACIÓN CIUDADANA | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | SUPERVISOR DE CAMARAS DIRECCION DE SEGURIDAD PUBLICA | 3 | Honorarios: 3 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | TALLER MAPUCHE | 3 | Honorarios: 3 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TECNICO AGRONOMO PRODESAL | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN CONSTRUCCION EGIS MUNICIPAL | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN REHABILITACION ANUN | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TERAPEUTA OCUPACIONAL | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL PROGRAMA LAZOS | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL PROGRAMA LAZOS | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL SENDA | 3 | Honorarios: 3 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÈCNICO EN ENFERMERIA ALBERGUE MUNICIPAL | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO AGRICOLA PRODESAL | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA CENTRO ANUN | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA EDIFICIO CONSITORIAL | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN REHABILITACION | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN REHABILITACION ANUN CENTRU ANUN | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN SIST. ELECTRICOS CASA DE LA SEGURIDAD | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN TREHABILITACION CENTRO ANUN | 3 | Honorarios: 3 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ABOGADA DEPTO DE LA MUJER | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA OFICINA JURIDICO | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO DIRECCIÓN MEDIO AMBIENTE | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO OFICINA OPD INFANCIA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO TRANSPARENCIA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO TRANSPARENCIA. SECRETARIA MUNICIPAL | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ADMINISTRACION GIMNASIO SCHWAGER | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRACIÓN GIMNASIO SCHWAGER | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRADOR PUBLICO DE CONTROL | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO AD. CASA DE LA CULTURA ARTE Y PATRIMONIO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AD. EN OFICNA DE SUBSIDIO Y PESNIONES | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AD. HABITABILIDAD | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM DIRECCION DE FINANZAS | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM HABITABILIDAD | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM OMIL | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. ASEO Y ORNATO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIIRECCION DE TRANSITO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE ADM Y FINANZAS | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE ASEO Y ORNATO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE CULTURA, ARTE Y PATRIMONIO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE TRÁNSITO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OFICINA DE TRANSITO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. SENDAPREVIENE | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. SENDRA PREVIENE | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCIÓN DE CULTURA | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO ISLA SANTA MARIA | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO MONITORAS JEFAS DE HOGAR | 2 | Honorarios: 2 | No clasificable | R00 | Combina apoyo administrativo y monitoreo; el texto no permite asignar un único estamento funcional. |
| Honorarios | APOYO DEPARTAMENTO ADMINISTRACIÓN MUNICIPAL | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO EDUCATIVO Y AUXILIAR DE 4 A 7 | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | APOYO EDUCATIVO Y AUXILIAR PROG DE 4 A 7 | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | APOYO EDUCATIVO Y AUXILIAR PROG. DE 4 A 7 | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | APOYO EJECUCION DE OBRAS | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EQUIPO TÉCNICO SECPLAN | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO JURIDICO ASEDORIA JURIDICA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDO GABINETA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO OF. HONORARIOS | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PREFESIONAL BIBLIOTECA MUNICIPAL | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL BIBLIOTÉCA MUNICIPAL | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL DEPTO DE TRANSPARENCIA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL OFICINA DE DISCAPACIDAD | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PVC | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO TECNICO PROFESIONAL DIRECCION DE SEGURIDAD PUBLICA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARBITRO DE FUTBOL OF DEPORTES | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARIBITRO DE FUTBOL OF. DEPORTES | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARQUITECTO BORDE COSTERO | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO DIRECCIÓN DE OBRAS MUNICIPALES | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTTO EN DIRECCIÓN DE OBRAS MUNICIPALES | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARTISTA EDUCADOR | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASESOR DE PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR DE PROGRAMACIÓN Y PLANIFICACION | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION D | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROGRAMACIÓN Y PLANIFICACIÓN | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR FINANCIERO Y PLANIFICACION DE NUEVO INGRESOS | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASISTENTE APOYO PEDAGOGICO | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE SOCIAL PROG. TRANSFORMANDO BARRIO | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL PROGRAMA TRANSFORMANDO BARRIOS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | AUDIOVISUAL CASA DE LA CULTURA | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | AUDIVISUAL DIDECO | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | CANTANTE | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICACIÓN OPD | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | COMUNICADOR AUDIVISUAL OF. COMUNICACIONES | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COOR. CASA DEL ADILTO MAYOR | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COOR. FINANCIERO Y ANALISTA CONTABLE | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COOR. INFOCENTRO YOBILO | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COOR. SENDAPREVIENE | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD DE SISTEMANDE SEGURIDAD | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. AREA ARTISTICA OF. DE JOVENES | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ARTISITICO CASA DE LA JUVENTUD | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ARTISTICO CASA DE LA JUVENTUD | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ASUSNTOS RELIGIOSOS | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE PROYECTOR Y GESTOR PATRIMONIAL | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. FINACIERO Y ANALISTA CONTABLE | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL PROGRAMA DE EMERGENCIAS | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL PROGRAMAS DE EMERGENCIA | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL SUPERVISOR EN TERRENO Y EDM. PROEMPLEO | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. INFORCENTRO | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PATRIMONIAL | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PRO EMPLEOS ISLA SANTA MARÍA | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PROEMPLEO | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PROGRAMA 4 A7 | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PUEBLO ORIGINARIOS | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. TECNICA CENTRO ANUN | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADORA CASA DE ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DIGUITADORA PROG. REGISTRO SOCIAL DE HOGARES | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | DIRECTOR DE PREYECTOR CULTURALES | 2 | Honorarios: 2 | Directivo | R01 | Dirección explícita de proyectos o funciones; estimación funcional, no confirmación de directivo municipal formal. |
| Honorarios | DIRECTOR DE PROYECYOS CULTURALES DIRECCION DE CULTURA | 2 | Honorarios: 2 | Directivo | R01 | Dirección explícita de proyectos o funciones; estimación funcional, no confirmación de directivo municipal formal. |
| Honorarios | EJECUCION DE OBRAS | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | EJECUTIVO DE EMPRESA OMIL | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ELECTRICISTA HABITABILIDAD | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ENC. DE ORIENTACION E INFORMACION DE VIOLENCIA DE GENERO | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENC. DE ORIENTECION E INFORMACION DE VIOLENCIA | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENC. OF. HABITABILIDAD | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENC. OF. PUEBLOS ORIGINARIOS | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA CASA ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA OF. ASUNTOS RELIGIOSOS | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADO DE PROGRAMA Y PLANIFICACION DE RECURSOS | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADO DE PROGRAMACION Y PLANIFICACION | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCUENTRO MURALISTAS | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | FOMENTO PRODUCTIVO | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | FORM.PROY.SOC.PARTIC.CIUDADAN | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | FOTOGRAFO DEPTO. COMUNICACIONES | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTIÓN VECINAL | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOR COMUNITARIO | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURA DIRECCIÓN DE CULTURA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL CASA DE LA CULTURA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL DIRECCIÓN DE CULTURA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL EN EJECUCIÓN DE OBRAS | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR EJECUCIÓN DE OBRAS | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE TRÁNSITO | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA TERRITIORAL OLN | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ING CIVIL INDUSTRIAL EJEC. DE OBRAS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO AGRONOMO PROFESAL | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO COMERCIAL PARTICIPACION CIUDADNA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO CONSTRUCCION OF. VIVIENDA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO CONSTRUCTOR EGIS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO CONTRUCTOR EGIS MUNICIPAL | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INSTRUCTORA DE FUTBOL FEMENINO OF. DEPORTES | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | LOCUTOR | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MAESTRO GASFITER HABITABILIDAD | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MECANICO DEPTO. TRANSPORTES | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MEDICO VETERINARIO | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITOR ALFABETIZACIÓN DIGITAL CASA DEL ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE DANZA URBANA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE HERTEROFILIA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE MANUALIDADES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE MANUALIDADES TALLERES DE MUJERES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE PROGRAMA DE 4 A 7 | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DEPORTIVO FOMENTO PRODUCTIVO | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR FUTBOL OF. DEPORTES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR FUTBOL. OF DEPORTES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR FUTBOLOF. DEPORTES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR PROGRAMA VINCULOS ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TALLER BMX | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TALLER CALISTENIA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TALLER SKATE | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ALFABETIZACION DIGUITAL | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE CAPORAL | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA FOLCKORICA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DISCAPACIDAD | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE MANUALIDADES, OF. DISCAPACIDAD | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE MANUEALIDADES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PROGRAMA PIAM | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PROGRAMA PIAM ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PROGRAMA VINCULOS ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE SUBLIMACION OF. TRANSPORTE | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DE TEATRO | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TELEVIGILANCIA DIRECCION DE CASA DE LA SEGURIDAD | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA DE ZUMBA OF. DE DEPORTES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PATINES OF. DEPORTES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PORCELANA EN FRIO TALLER DE MUJERES | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROG DE 4 A 7 | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRANA PIAM ADULTO MAYOR | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA SOCIAL A.MAYOR | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA YOGA | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITRA ALFABETIZACIÓN DIGITAL | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | OFICINA EGIS | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | OPERADOR AUDIVISUAL CASA DE LA CULTURA | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR CAMARAS TELEVIGILANCIA | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE MAQUINA | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | OPERADOR DE MAQUINARIA PRODESAL | 2 | Honorarios: 2 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | OPERADOR RELOJ PLAZA 21 DE MAYO | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PARTICIPACIÓN DE DIAGNOSTICOS Y PLANIFICACIÓN CDM | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PERIODISTA OF. DE COMUNICACIONES | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PREV. RIESGOS CASA DE LA SEG. | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTA DE RIESGO OF. RIESGO | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTA EJ. DE OBRAS | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PROF EJECUCION DE OBRAS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. APOYO SENDAPREVIENE | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROF. DIRECCION JURIDICA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO DENDAPREVIENE | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL LINEA ASISTENCIA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL OF.VIVIENDAS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROGRAMA PSICOSOCIAL | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PSICOLOGA CDM | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DE DIRECCION DE SEGURIDAD | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DE DIRECCIÓN DE SEGURIDAD | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO PRLA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICÓLOGA CENTRO DE LA MUJER | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PUBLICIDAD CASA DE LA SEGURIDAD | 2 | Honorarios: 2 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PUBLICISTA | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PUBLICISTA CASA DE LA CULTURA | 2 | Honorarios: 2 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | RECEPCIÓN DIDECO | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | RELATOR DE TALLER | 2 | Honorarios: 2 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | SECRETARIA | 2 | Honorarios: 2 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SUPERVISOR EQUIPO DEM | 2 | Honorarios: 2 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | TABAJADORA SOCIAL DIRECCION DE SEGURIDAD | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TECNICO AGRONOMO INDAP | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN ENFERMERIA CENTRO ANUN | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN REHABILITACION ANUN CENTRU ANUN | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN TREHABILITACION CENTRO ANUN | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS EN EDIFICIO CONSISTORIAL | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS. EDIFICIO CONSISTORIA | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS. EDIFICIO CONSITORIAL | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS. EDIFICIO COSISTORIAL | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TERAPEUTA OCUPACIONAL CENTRO ANNUN | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TERAPEUTA OCUPACIONAL RED LOCAL DE APOYO | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABADORA SOCIAL CASA DE LA SEGURIDAD | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL PREPARA2 | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL CASA DE LA MUJER | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL DIRECCION DE SEGURIDAD | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL DIRECCIÓN DE SEGURIDAD PUBLICA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL EGIS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL O.P.D INFANCIA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL SENDA PREVIENE | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJOR SOCIAL CENTRO ANUN | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJOR SOCIAL EGIS | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRBAJADORA SOCIAL PROG SENAMA | 2 | Honorarios: 2 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÉCNICO AGRONOMO | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMARIA ALBERGUE MUNICIPAL | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA ALBERGUE MUNICIAPAL | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA ALGERGUE MUNICIPAL | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA OLN | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN SEGURIDAD CASA DE LA SEGURIDAD | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉNICO EN REHABILITACIÓN CENTRO ANUN | 2 | Honorarios: 2 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | ABOGA CENTRO DE LA MUJER | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA ASESORIA JURIDICO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA ASOSORIA JURIDICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADA DEPTO DE LA MUJER E.G | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO DIRECCION DE MEDIOAMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO EGIS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO OFICINA O.P.D INFANCIA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO TRANSPARENCIA MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ABOGADO, JURIDICO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ACTRIZ | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ADM GIMNASIO SCHWAGER | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTADOR GIMNASIO SCHWAGER | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRACIÓN GIMANSIO SCHWAGER | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ADMINISTRADOR GIMANSIO SCHWAGER | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ADMINISTRADOR GIMNACIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRADOR GIMNASIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRADOR GIMNASIO ACHWAGER | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRADOR GIMNASIO CHWAGER | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMINISTRATIVA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ADMISTRACIÓN GIMNASIO SCHWAGER | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | AIXILIAR DE SERVICIOS | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | AIXILIAR DE SERVICIOS CENTRO ANUN | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | AMPLIAR PATRIMONIO COMUNAL | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | ANTROPOLOGA DIRECCION DE CULTURA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | AOYO ADM. CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APERADOR AUDIOVISUAL CASA DE LA CULTURA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOERADOR DE RELOJ PLAZA 21 DE MAYO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | APOY ADM. DIRECCION DE CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AD. DIRECCION DE CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AD. OF. BECAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADD. CASA DE LA CULTURA ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADD. DIRECCIÓN DE CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADD. OF. SUBSIDIO Y PENSIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM CASA DE LA CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM DEPTO DE LA MUJER Y EG | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM DIRECCION DE TRANSITO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM DIRECCIÓN DE CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM EGIS MUNICIPAL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM OF. SUBSIDIO Y PENSIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM OF. TRANSITO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM SENDAPREVIENE | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. CASA DE CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. CASA DE LA CULTURA ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEPTO DE LA MIJER Y EG | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEPTO DE LA MUJER Y EG, | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEPTO DE TRANSITO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DEPTO RRHH | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE CULTURA ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCION DE FINANZA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIONDE SEGURIDAD | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE ADM. Y FINANZAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DIRECCIÓN DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. DISCAPACIDAD | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. EC DEM | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. EN DIRECCIÓN DE TRÁNSITO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. EN OFICINA DE SUBSIDIO Y PENSIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. FINANZAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. JPL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. ADUNTO MAYOR | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. CONCEJALES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OF. DE JOVENES Y MONITORA DE AUTODEFENSA DEPTO. DE LA MUJER | 1 | Honorarios: 1 | No clasificable | R00 | Combina apoyo administrativo y monitoreo; el texto no permite asignar un único estamento funcional. |
| Honorarios | APOYO ADM. OF. TRANSPORTE | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OFICINA DE CONCEJALES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OFICINA DE JOVENES Y MONITORA DE AUTODEFENSA DEPTO DE LA MUJER | 1 | Honorarios: 1 | No clasificable | R00 | Combina apoyo administrativo y monitoreo; el texto no permite asignar un único estamento funcional. |
| Honorarios | APOYO ADM. OFICINA DE SUBSIDIO Y PENSIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM. OFICNA DE JOVENES Y MONITORA DE AUTODENSA | 1 | Honorarios: 1 | No clasificable | R00 | Combina apoyo administrativo y monitoreo; el texto no permite asignar un único estamento funcional. |
| Honorarios | APOYO ADM. SENDA PREVIEIEN | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM., OF. BECAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM.OF DE JOVENES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM.OF. BECAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADM.OMIL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISITRATIVO DIRECCION DE CULTURA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTATIVO ISLA SANTA MARIA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRACION | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVA EGIS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DEM | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DEPTO BECAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCION DE CULTURA ARTES Y PATRIMONIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCION DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DIRECCIÓN DE ASEO Y ORNATO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO DPTO DE LA MUJER | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO EN DIRECCÓN DE TRANSITO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO EN OFICINA DE SUBSIDIO Y PENSIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO FOMENTO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OF INFORMACIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OF. BECAS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OF. JOVENES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO OF. SUBSIDIO Y PENSIONES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO ORIS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMINISTRATIVO PERSONAL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMNINISTRATIVO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO ADMNISTRATIVO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AMD. CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AMD. DIRECCION DE TRANSITO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AMDINISTRATIVO EGIS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO AMPLIFICACION | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO AMPLIFICACIÓN | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO ANUN | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO COORDINADOR SENDA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO DIRECCION DE CULTURA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EDUCATIVO DE 4 A 7 | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN ADM EN DIRECCIÓN DE CULTURA ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO EN ADM. EN DIRECCION DE CULTURA DE ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO EN AMPLIFICACIÓN | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD DIRECCION DE SEGURIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD DIRECCIÓN DE SEGURIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD DIRECCIÓN DE SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EN SEGURIDAD, CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO EQUIPO TECNICO SECPLAN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO FAMILIAR PROGRAMA FAMILIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDCO GABINETE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO ASESORRIA JURIDICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO ASESORÍA JURIDICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO ASESORÍA JURÍDICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO ASOSORIA JURIDICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO GABIENTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDICO GABINITE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDO ASESORIA JURIDICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO JURIDO GABINETE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO LOGISTICO Y ADMINISTRATIVO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | APOYO OF INFORMACIONES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROEMPLEO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROF. ADM MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. BILBIOTECA MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DEPTO RRHH | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DIRECCION DE FINANZAS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. DIRECCIÓN DE FINANZAS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROF. PARTICIPACION CIUDANA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFE. SENDA PREVIENE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROFESIONA DEPTO RRHH | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO PROFESIONAL ADMINISTRACIÓN MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL DEPTO. TRANSPARENCIA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL DIRECCIÓN DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL EN ADMINISTRACIÓN MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL OFINA DE DISCAPACIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL PARTICIPACIÓN CIUDANA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO PROFESIONAL PERSONAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO REGISTRO SOCIAL DE HOGARES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | APOYO TECNICO CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TECNICO DIRECCION DE MEDIOAMBIENTE | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TECNICO PROFESIONAL DIRECCIÓN DE SEGURIDAD AD PUBLICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYO TÉCNICO DIRECCION DE SEGURIDAD | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TÉCNICO DIRECCIÓN DE MEDIOAMBIENTE | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | APOYO TÉCNICO PROFESIONAL DIRECCIÓN DE SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | APOYP ADM. DIRECCION DE ASEO Y ORNATO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ARBITRI DE FUTBOL. OF. DE DEPORTE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARBITRO DE FUTBOL OF. DE DEPORTE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARBITRO DE FUTBOL. OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARBITRO DE FÚTBOL OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ARQUICTOR SECPLAN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO DERECCION DE OBRAS MUNICIPALES | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTO RESTAURADOR | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTOR EN DIRECCIÓN DE OBRAS MUNICIPALES | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITECTTO DOM | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITÉCTOR EN DIRECCIÓN DE OBRAS MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARQUITÉCTOR EN DIRECCIÓN DE OBRAS MUNICIPALES | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ARTISTA MURALISTA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASESOR DE PROGRAMA Y PLANIFICACIÓN DE NUEVOS INGRESOS | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR DIRECCION JURIDICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROG. Y PLANIF. DE NUEVOS INGRESOS MUNICIPALES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROGRAMA Y PLANIFICACIÓN DE NUEVOS INGRESOS | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOR EN PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS MUNICIPALES (DIRECCION | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | ASESOSA SENIOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASISNTE SOCIAL SENDAPREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISNTENTE SOCIAL SENDAPREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISNTETE SOCIAL CENTRO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISNTETE SOCIAL DIRECCION DE SEGURIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISNTETE SOCIAL QUIERO MI BARRIO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISNTETE SOCIAL SENDAPREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENENTE SOCIAL DIRECCION DE SEGURIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASISTENTE DE APOYO PEDAGOGICO PROG 4 A 7 | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE DE APOYO PEDAGOGICO PROGRAMA 4 A 7 | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE DE APOYO PEDAGÓGICO | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ASISTENTE SOCIAL CASA DE CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL CENTO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL PROGRAMA PREVENCION | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL QUIERO MI BARIO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL QUIERO MI BARRIO SEPLAN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTENTE SOCIAL TRANSFORMANDO BARRIO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTNETE SOCIAL CENTRO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASISTNETE SOCIAL SENDAPREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASITENTE SOCIAL CENTRO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ASOSOR FINANCIERO Y PLANIFICACION DE NUEVO INGRESOS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASOSOR GABINETE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ASOSORA SENIOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ATENCION DE CASO SOCIALES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ATENCION EN OIRS | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ATENCIÓN CASOS SOCIALES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ATENCIÓN DE CASO SOCIALES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ATENCIÓN DE CASOS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ATENCIÓN EN COSOS SOCIALES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | AUXILIAR DE SERVICION CENTRO ANUN | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | AUXULIAR DE ASEO ALBERGUE MUNICIPAL | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | CANTANTE ACTIVIDADES ARTISTICAS GABINETE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | CARPINERO HABITABILIDAD | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | CASA DE LA CULTURA | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | CHILE CREACION CONTIGO | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | COMINCADOR AUDIOVISUAL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMINCADOR AUDIOVISUAL OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICACIÓN AUDIOVISUAL | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | COMUNICADOR AUDIO VISUAL MUNICIPAL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICADOR AUDIOVISUAL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICADOR AUDIOVISUAL RELACIONES PUBLICAS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICADOR AUDIOVISUAL. OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICADORA AUDIOVISUAL CASA DE LA CULTURA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COMUNICARDOR AUDIOVISUAL OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | CONSERVADORA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | CONTRUCTOR CIVIL DOM | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | COOD. ASUNTOS RELIGIOSOS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COOR. CHILE CRECE CONTIGO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COOR. FINACIERO Y ANALISTA CONTABLE PROEMPLEO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD ARTISTICO OF. DE JOVENES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD, PROGRAMA DE 4 A 7 | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. AREA ARTISTICA OFICINA DE JOVENES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ARTISITIVO OF. JOVENES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ARTISTICA OF. JOVENES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ASENTAMIENTOS PRECARIOS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ASUSNTOS RELIGIOSO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. CENTRI DE LA MUJER | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. CENTRO DE LA MUJER | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. COMUNICACICONES CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. COMUNICACIONES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. CONTORL GESTION | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. CONTROL GESTIÓN | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE ASENTAMIENTO PRECARIOS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE ASENTAMIENTOS PRECARIOS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE COMUNICACIÓN | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE PROYECTOS Y GESTOR PATRIMONIAL | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE SISTEMA DE SEGURIDAD ELECTRONICA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE SISTEMA DE SEGURIDAD ELECTRONICA DIRECCIÓN DE SEGURIDAD PÙBLICA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DE SISTEMAN DE SEGURIDAD | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DEPTO DE LA MUJER Y EG. | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. DEPTO DE LA MUNER Y EG | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. FINANC Y ANALISTA CONTABLE PRO EMPLEO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. FINANC Y ANALISTA CONTABLE PROEMPLEO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. FINANCIER Y ANALISTAS CONTABLE | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. FINANCIERO Y ANALIESTA CONTABLE | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. FINANCIERO Y ANALISTA CONTABLE PROEMPLEO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL DE SUPERVISIÓN EN TERRENO Y ADMINISTRATIVO PRO EMPLEOS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL PROEMPLEO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL PROGRAMAS DE EMERGENCIAS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL PROGRAMAS DE EMERGENVIAS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL PROGRAMAS DE EMERGIAS | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. GENERAL SUPERVISION EN TERRENO Y ADMINISTRATIVO PRO EMPLEP | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. O.P.D INFANCIA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PARENTALIDAD SENDA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. PARENTRALIDAD SENDA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. SISTEMA DE SEGURIDAD ELECTRONICA DIRECCION DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. SISTEMA DE SEGURIDAD ELECTRÓNICA DIRECCIÓN SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. SISTEMANDE SEGURIDAD | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. TÉCNICO CENTO ANUN | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD. ÁREA ARTÍSTICA OF. JÓVENES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORD.ARTISITICO OF. JOVENES | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDD. PROGRAMA DE 4 A 7 SERNAMEG | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDDINADOR ALBERGUE | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | COORDINADOR CASA ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADOR OTEC MUNICIPAL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA ESCUELA DE VERANO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PATRIMONIAL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | COORDINADORA PROGRAMA 4 A 7 SERNAMEG | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DIBUJANTE ARQUITECTONICO ESTRUCTURAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | DIBUJANTE TÉCNICO SECPLAN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | DIBUJANTE Y PROYECTISTA SECPLAN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | DIGUITADOR PROG. REGISTRO SOCIAL DE HOGARES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | DIRECCION DE CULTURA | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | DIRECTOR DE PROYECTOR CULTURALES | 1 | Honorarios: 1 | Directivo | R01 | Dirección explícita de proyectos o funciones; estimación funcional, no confirmación de directivo municipal formal. |
| Honorarios | DISEÑADOR GRAFICO CASA DE LA CULTURA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DISEÑADOR PLAN DE ACCION OPD | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DISEÑADORA VIOLE. CONTRA MUJER | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DISEÑADPR GRAFICO DIDECO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | DISTRIB. DE CORRESPONDENCIA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | EJECUTIVO ATENCION DE EMPRESAS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EJECUTIVO ATENCIÓN DE EMPRESAS OMIL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EJECUTIVO DE EMPRESAS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EJECUTIVO DE VENTAS OMIL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ELECTRICISTA | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ELECTRICO | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ELECTRICO HABITABILIDAD | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | EN | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | ENC. AREA INDEPENDIENTE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENC. PROYECTO RESCATANTO MEMORIA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCAR. CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA COMUNAL PJM | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA COMUNICAL P.M.J | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA CREE DEPENDIENTE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DE ASUNTOS RELIGIOSO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DE ASUNTOS RELIGIOSOS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DE GESTPRES TERRITORIALES OLN | 1 | Honorarios: 1 | Jefatura | R03 | Encargo explícito de equipo de gestores territoriales. |
| Honorarios | ENCARGADA DE PROGRAMA OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DE PROGRAMA PMJ CORONEL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DE SALVAVIDAS | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ENCARGADA DEPTO DE LA MUJER Y EG | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA DEPTO DE MUJER Y E.G | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA JEFAS DE HOGAR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA OF. ASUNTOS RELIGIOSO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMA PJM CORONEL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADA PROGRAMAS MUJERES CORONEL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADO DE PROGRAMA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADO DE PROGRAMACION Y PLANIFICACION DE NUEVOS INGRESOS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCARGADO DE PROGRAMACION Y PLANIFICACIÓN | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCCARGADO DE PROGRAMAS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENCUESTADOR | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ENCUESTADORA PROG. REGISTRO SOCIAL DE HOGARES | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | ENFEMERA RED LOCAL DE APOYO Y CUIDADO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ENFERMA VIVIENDAS TUTELADAS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ENFERMERA VIVIENDA TUTELADAS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ENTRANADOR DE FUTBOL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ENTREGA TARJETA NAVIDEÑAS | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | ENTRENADOR DE BASQUETBOL | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | EXPOSITORA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | FONOADIOLOGA OF. DISCAPACIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | FONOADIOLOGO OF. DISCAPACIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | FOTOGRAFO DEPTO OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | FOTOGRAFO. OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | FOTOGRAFOTO OF. COMUNCACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | FOTOGRAFOTO OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GASFITER DE HABITABILIDAD | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | GASFITER PROG. HABITABILIDAD | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | GESTION VECINAL DIRECCION DE ASEO Y ORNATO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTION VECINAL DIRECCIÓN DE ASEO Y ORNATO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOA DE CASOS OLN | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | GESTOR CULTURAL DIRECCIÓN CULTURA, ARTES Y PATRIMONIO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR CULTURAL. DIRECCIÓN DE CULTURA, ARTE Y PATRIMONIO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR OF. DE TRANSITO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCION DE MEDIOAMBIENTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL DIRECCIÓN DE TRANSITP | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINAL OF. PARTICIPACIÓN CIUDADANA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINALDIRECCIÓN DE ASEO Y ORNATO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINALL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTOR VECINALL DIRECCIÓN DE MEDIO AMBIENTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA VECINAL DIRECCIÒN DE TRANSITO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GESTORA VECINAL DIRECCIÓN DE MEDIO AMBIENTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | GUADIA DE SEGURIDAD CENTRO ANUN | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | GUARDA DE SEGURIDAD ANUN | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | GUARIA DE SEGURIDAD CENTRO ANUN | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | INFOMATICO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | ING. CIVIL BORDE COSTERO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | ING.CIVIL BORDE COSTERO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERA AGRICOLA PRODESAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERA AGRONOMA PRODEDAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERA AGRONOMA PRODESAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERA PRODESAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERIO AGRONOMO PRODESAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERIO CONSTRUCTOR EGIS MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO AGRONOMO OF. DEPORTES | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO AGRÓNOMO PRODESAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO CIVIL BORDE COSTERO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO COMERCIAL DIRECCIÓN DE FINANAZAS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO COMERCIAL OF. PARTICIPACIÓN CIUDADANA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO COMERCIAL PARTICIPACION CIUDADANA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO CONSTRUCTORA DIDECO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO CONTRUCTOR EGIS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO EN COMPUNTACION E INFORMATICA EGIS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO EN COMPUTACION E INFORMATICA SECPLAN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO EN COMPUTACION EGIS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INGENIERO EN CONSTRUCCION | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | INSTRUCTOR KICKBOXING | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTORA DE FUTBOL OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTORA DE YOGA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INSTRUCTORA YOGA DEPTO DE LA MUJER | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INTERPRETE DE LENGUAJE DE SEÑAS CUENTA PUBLICA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INTERPRETE DE LENGUAS DE SEÑAS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | INTERPRETE LENGUA DE SEÑAS CUENTA PUBLICA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | KINESIOLOEGO CHILECRECE CONTIGO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGA RED DE APOYO Y CUIDADO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO DIDECO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO OF. DE DISCAPACIDAAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | KINESIOLOGO PROG CHILE CRECE CONTIGO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | LOCUTOR OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MAESTRO CARPINTERO HABLITABILIDAD | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MAESTRO OBRAS CIVILES | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MANTENIENTO CANCHA NUEVO AMANECER | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MANTENIMIENTO Y CUIDADO RECIENTOS DEPORTIVOS | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | MEDICO PSIQUIATRA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MEDICO PSIQUIATRA MEDICO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MEDICO VETERINARIO DIRECCION DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | MONITA ALBERGUE MUNICIPAL | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITA DE YERBAS MEDICINALES TALLER DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITA DEPORTIVA OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITA PROGRAMA PIAM ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITA TALLERES DEPORTIVO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITO CAMARA DIRECCIÓN DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITO DE ALFABETIZACIÓN DIGUITAL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITO DE FUTBOL OF. DE DEPORTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOA PROGRAMAS PIAM ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR ARTES TEATRALES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR CAMARA DIRECCION DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR CIRCENCE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ALFABERIZACIÓN ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ALFABETIZACION DIGITAL CASA DEL ADULTOO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ALFABETIZACIÓN ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ALFABETIZACIÓN DIGUETAL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ALFABETIZACIÓN DIGUITAL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ALFABETIZACIÓON DIGUITAL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE ARTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE CAMARAAS | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR DE COCINA ESCUELA DE VERANO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE DANZA OF. DISCAPACIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE DEPORTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE FUTBOL DEPTO DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE FUTBOL OF. DE DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE FUTBOL OF. DEPORTIVO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE HERTEROFILIA OF DEPORTE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE JIUTIITSU | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE JIUTITSU | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE JIUTUTSU | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE PATINAJE OFICINA DE DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE PROG. DE 4 A 7 | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE PROGRAMA VINCULO ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE PROGRAMAN VINCULO ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE TALLER CIRCO-TEATRO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE TALLER DE BATUCADA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR DE TELEVIGILANCIA SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITOR DEPORTIVO OF. DEPORTES Y TALLER DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR EDUCATIVO DE 4 A 7 | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR FOTOGRAFIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR PROG. VÍNCULO ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR PROGRAMA VINCULO ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TALLER DANZA URBANA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR TALLER DE BATUCADA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITOR VESPERTINO ALBERGUE MUNICIPAL | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITORA ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ALFABETIZACIÓN DIGITAL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ALFABETIZACIÓN DIGITAL CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ALFABETIZACIÓN DIGUITAL | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ALFARERIA TALLERES DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ARTES TREATRALES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ARTISTICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA BAIEL KPOP OF. JOVENES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA COMUNITARIA O.P.D | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DANZA ARABE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ARTES MARCOAÑES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE BARTENER Y GARONERIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA FLOKLORICA CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA OF. DE DISCAPACIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA TALLERES DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DANZA TRIVAL TALLERES DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE DAZNA FOLKLORICA CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE FOLCLOR CASA DEL ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE MANUALIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE ORFEBRERÍA TALLERES DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PINTURA ASFALTICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PROGRAMA 4A 7 | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE PROGRAMA DE 4 A 7 | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE REPOSTERIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE RESPOSTERIA OF. ADULTO MAYO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE RESPOSTERIA OF. ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE SUBLIMACION | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE SUBLIMACION OF. DISCAPCIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE SUBLIMACIONES OF. DISCAPACIDAD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DANZA FOLCKORICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DE BATUCADA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DE BODYBOARD | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DE DANZA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DE DANZA FOLCKORICA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TALLER DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DE TELEVIGILANCIA DIRECCIÓN DE CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA DE TELEVIGILANCIA DIRECCIÓN DE LA CASA DE LA SEGURIDAD | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA DE TELIVIGILANCIA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA DE ZUMBA. OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DEPTO. DE LA MUJER | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA DERPORTES OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ESTIMULACION TEMPRANA CHILE CRECE CONTIGO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA FITNETSS | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA JURIDICA CENTRO DE LA MUJER | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA OFICINA DE DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PATÍN OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PORCELANA EN FRÍO TALLERES DE MUJERES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA PROGRAMA ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA REPOSTERÍA OF. ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA RESPOSTERIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLER DE BATUCADA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLER DE DANZA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLER DE DANZA FOLKLORICA ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TALLER DE DANZA FOLKLORICA PARA ADULTOS MAYORES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TELAR MAPUCHE | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA TELEVIGILACIA DIRECCION DE SEGURIDAD PIBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA TELEVIGILANCIA DIRECCION DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA TELEVIGILANCIA DIRECCIÓN SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA TENS | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONITORA VESPERTINI ALBERGUE | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITORA VESPERTINO ALBERGUE MUNICIPAL | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | MONITORA ZUMBA OF DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ZUMBA OF. JOVENES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORA ZUMBA. OF. DEPORTES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | MONITORCAMARA DIRECCION DE SEGURIDAD PUBILICA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MONITORES DE CAMARAS | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | MONUNICADOR AUDIOVISUAL OF. COMUNICACIONES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MURALISTA DEPTO DE LA MUJER Y E.G | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | MURALISTAS | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | NUTRICIONISTA PRODESAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCION DE CULTURA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCION DE CULTURA ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCION DE CULTURA ARTES Y PATRIMONIO | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCIÓN CULTURA, ARTES Y PATRIMONIO | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR AUDIOVISUAL DIRECCIÓN DE CULTURA ARTE Y PATRIMONIO | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR AUDIVISUAL DIRECCIÓN DE CULTURA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE CAMARAS DIRECCION DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE CAMARAS DIRECCION DE SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE CAMARAS DIRECCIÓN DE SEGUIRIDAD PUBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE CÁMARAS DIRECCIÓN SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | OPERADOR DE MAQUINARIA PESADA ISLA SANTA MARÌA | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | OPERADOR DE MAQUINARIAS | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | OPERADOR DE RELOJ PLAZA 21 MAYO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | OPERADOR MAQUINARIA PRODESAL | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | ORADOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PARTICIPACION DE DIAGNOSTICO Y PLANIFICACIÓN CDM | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PARTICIPACIÓN DE DIAGNOSTICOS Y PLANIFICACION CDM | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PELUQUERO | 1 | Honorarios: 1 | Auxiliar | R08 | Apoyo operativo, cuidado, vigilancia, alimentación u oficio manual explícito. |
| Honorarios | PERIODISTA DEPTO COMUNITARIO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PERIODISTA OF. DEDE COMUNICACIONES | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PERIODISTA RELACIONES PUBLICAS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PREVENCIONISTA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTA DE RIEGO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTA DE RIEGOS OF. RIESGO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTA DE RIEGOS. OF. RIESGO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTA DE RIESGO OF. RIESGTO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONISTRA DE RIESGO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PREVENCIONITA DE RIESGO | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PRFESIONAL DE APOYO SENDAPREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PRODUCTORA AUDIVISUAL CONSERVADORA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PROF. DE APYO SENDAPREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO ALBERGUES | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL DE APOYO PREPARA2 | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESIONAL OF. OTEC | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PROFESOR DEE PATINAJE | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | PROG 4 A 7 | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PROG SOCIALES | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PROGRAMA INDAP | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PROGRAMA JEFAS DE HOGAR | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | PSICOGA ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DE DIRECCION DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DE DIRECCION SE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DEPTO DE LA MUJER Y E,G | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DEPTO DE LA MUJER Y EG. | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DIRECCION DE SEGURIDAD PUBLICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA DIRECCIÓN SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA O.P.D INFANCIA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGA SENDA PREVIENE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO CENTRO DE LA MUJER | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO DEPTO DE LA MUJER Y EG | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO O.P.D INFANCIA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO PORG. LAZOS | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOGO PROGRAMA LAZOZ | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLOOGA OPD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSICOLÓGA O.P.D INFANCIA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSIQUIATRA ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | PSIQUIATRICA CENTRO ANUN | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | RECEPCIONISTRA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | RECEPECIONISTA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | RELATADORA | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | RELATORA FUNDACION ANTONIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | RELATORA OF. BECAS | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | REMODELACION PLAZA SCHWAGER | 1 | Honorarios: 1 | No clasificable | R97 | El texto denomina principalmente unidad, programa o prestación, no una función con nivel de estamento inequívoco. |
| Honorarios | SECRETARIA EGOS MUNICIPAL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SECRETARIA EJECUTIVA | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SECRETARIA OF. CONCEJAL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SECRETARIA OF. DERECHOS HUMANO | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SECRETARÍA EGIS MUNICIPAL | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SECRRETARIA OPD | 1 | Honorarios: 1 | Administrativo | R07 | Función administrativa, secretarial, recepción, digitación, encuestas o compras explícita. |
| Honorarios | SUPERVISOR DE CÁMARAS DIRECCIÓN DE SEGURIDAD PÚBLICA | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | SUPERVISOR PRO EMPLEO | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | SUPERVISORA EQUIPO EX DEM | 1 | Honorarios: 1 | Jefatura | R03 | Coordinación o supervisión explícita de programa, área o equipo; no acredita una jefatura formal. |
| Honorarios | T.E.N.S EN EDIFICIO CONSISTORIAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TALLER DE ARTESANIA Y MANUELIDADES | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE DANZA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE GARZONERIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE MANUALIDADES EN PORCELANA EN FRIO | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE NATACION | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE NATACIÓN | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE ORFARERIA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TALLER DE YOGA | 1 | Honorarios: 1 | No clasificable | R98 | Rol genérico o actividad sin evidencia textual suficiente para distinguir nivel profesional, técnico, administrativo o auxiliar. |
| Honorarios | TEC. TRABAJO SOCIAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO DEPORTIVO OF. DEPORTES | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN INFORMATICA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN REHABILITACIÓN CENTRO ANUN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TECNICO EN SIST. ELECTRICOS | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENCICO EN REHABILITACION ANUN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TENS EN ANUN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TEPAPEUTA OCUPACIONAL OF. DISCAPACIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TERAPEUTA OCUPACIONAL OF. DISCPACIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TITIRITERO OF. JOVENES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | TRAABAJADOR SOCIAL CENTRO DE LA MUJER | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL CASA ADULTO MAYOR | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADOR SOCIAL OLN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL CASA DE LA MUJER Y E.G | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL CENTRO DE LA MUUER | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL OF. ADULTO MAYOR | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL PREPARA2 SENDA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL PROGRAMA 4 A 7 | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL RED LOCA DE APOYO Y CUIDADO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL RED LOCAL DE APOYO Y CUIDADO | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORA SOCIAL. OF DE VIVIENDA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORASOCIAL HABITABILIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJADORS SOCIAL CENTRO ANUN | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJO EN ARTES VISUELES | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | TRABAJO SOCIAL ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | TRABAJO SOCIAL CASA ADULTO MAYOR | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | TRABAJO SOCIAL SEPLAN | 1 | Honorarios: 1 | No clasificable | R99 | Texto insuficiente o nivel funcional ambiguo; requiere contexto adicional y revisión manual. |
| Honorarios | TRABAJOR SOCIAL HABITABILIDAD | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TRABAJORA SOCIAL PREPARA2 SENDA | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | TÈCNICO AGRONOMO PRODESAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÈCNICO EN CONSTRUCCION EGIS MUNICIPAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÈCNICO EN ENFERMERIA EDIFICIO CONSISTORIAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO AGRONOMO INDAP | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO AGRONOMO. PRODESAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO AUDIOVISUAL, DIRECCION DE CULTURA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO CONSTRUCCION EGIS MUNICIPAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO CONSTRUCCIÓN EGIS MUNICIPAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN CONSTRUCCION EGIS MUNICIPA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA ALBERGUE | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA ALBERGUE MUNCIPAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA DIDECOO | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN ENFERMERIA ESCUALA DE VERANO | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN REH | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICO EN REHABILITACIÓN ANUN CENTRO ANUN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉCNICOEN CONSTRUCCIÓN EGIS MUNICIPAL | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | TÉNICO EN REHABILITACION CENTRO ANUN | 1 | Honorarios: 1 | Técnico | R06 | Título técnico, TENS, dibujo/topografía u operación especializada declarada en el texto. |
| Honorarios | VETERIANARIO DIRECCION DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERIANRIO DIRECCIÓN DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIA MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO DIRECCION DE MEDIO AMBIENTTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO DIRECCION DE MEDIOAMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO DIRECCION MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO DIRECCIOÓN DE MEDIO AMBIENTE | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |
| Honorarios | VETERINARIO MUNICIPAL | 1 | Honorarios: 1 | Profesional | R05 | Profesión o condición profesional explícita; las variantes ortográficas solo se usan para reconocer el mismo término. |

## 8. Validaciones y reproducción

Se comprobó automáticamente:

- una fila por `categoria + cargo_funcion`, sin duplicados;
- sumas de frecuencias: 9.464 en Honorarios y 933 en Código del Trabajo;
- 1.626 y 25 cargos distintos, respectivamente;
- destinos limitados a los seis valores permitidos o `No clasificable`;
- coherencia entre destino y estado de clasificación;
- exactamente 30 clasificados estratificados y 20 no clasificables en la muestra;
- SHA-256 de ambos maestros sin cambios antes y después de generar la propuesta.

Reproducción desde la raíz del workspace:

```bash
python "trabajo/04_Personal_y_Remuneraciones/construir_mapeo_estamento_estimado.py"
```

Archivos generados:

- `trabajo/04_Personal_y_Remuneraciones/MAPEO_ESTAMENTO_ESTIMADO_v1.csv`: tabla completa revisable.
- `trabajo/04_Personal_y_Remuneraciones/MUESTRA_REVISION_ESTAMENTO_ESTIMADO_v1.csv`: muestras de revisión.
- `trabajo/04_Personal_y_Remuneraciones/validacion_mapeo_estamento_estimado_v1.json`: comprobaciones y trazabilidad.
- `documentación/04_Personal_y_Remuneraciones/MAPEO_ESTAMENTO_ESTIMADO_v1.md`: este informe.

## 9. Decisión pendiente

El propietario debe revisar la tabla completa y, especialmente, las muestras y los no clasificables frecuentes. Solo después del registro/aprobación de la decisión corresponde diseñar su incorporación como variable derivada. Esta propuesta no habilita por sí misma cambios en datos ni en plataforma.
