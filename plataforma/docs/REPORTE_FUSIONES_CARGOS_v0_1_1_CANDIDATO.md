# Reporte candidato de fusiones de cargos — v0.1.1

**Fecha:** 2026-11-19T02:14:33-03:00  
**Versión candidata de pipeline:** `modulo_personal_v1.5.0-rc1_normalizacion_cargos`  
**Canónico de entrada:** `canonico_v1.0.0`; 22,940 registros  
**Estado:** **NO INTEGRADO — PENDIENTE DE REVISIÓN DEL PROPIETARIO**

## 1. Alcance y compuerta

Este reporte compara publicaciones consecutivas dentro de cada trayectoria D-15. Una fusión candidata ocurre solo cuando las grafías difieren, la normalización vigente también difiere y la normalización candidata produce exactamente la misma secuencia ordenada de tokens. No se usa similitud difusa, distancia de edición, inferencia semántica ni equivalencia entre cargos distintos.

El candidato conserva `cargo_funcion`, los maestros, los agregados y las fichas publicadas sin cambios. Cada fila incluye ambos registros, períodos, archivos, filas CSV y SHA-256 para revisión. La columna `revision_propietario` permanece `PENDIENTE`; ninguna fusión se integra automáticamente.

## 2. Reglas candidatas

1. Unicode NFKD, mayúsculas, eliminación de acentos y puntuación, conservando Ñ.
2. Expansiones vigentes y nuevas exclusivamente literales: `ENC./ENCG/ENCARG → ENCARGADO`, `DPTO → DEPARTAMENTO`, `JEF → JEFE`, `UNID → UNIDAD`, `AUX → AUXILIAR`; se mantienen las abreviaturas SC-04.
3. Orden canónico alfabético de tokens después de expandir, conservando duplicados.
4. `ENCARGADO` y `JEFE` no son equivalentes; tampoco `PROFESIONAL` y `AUXILIAR`. Las diferencias sustantivas permanecen como cambio de cargo o posible variante según la regla conservadora.

## 3. Resultado

- Comparaciones consecutivas evaluadas: **21,870**.
- Fusiones nuevas candidatas: **31**.
- Registros en la proyección D-15: **22,938**.
- Integración en producción: **0; bloqueada hasta aprobación**.

### Por categoría

| Categoría | Fusiones candidatas |
|---|---:|
| Planta | 6 |
| Contrata | 25 |
| Código del Trabajo | 0 |
| Honorarios | 0 |

### Por estado que dejaría de marcarse como cambio/frontera

| Estado vigente | Casos |
|---|---:|
| cambio_cargo | 31 |

### Por mecanismo

| Mecanismo | Casos |
|---|---:|
| expansión explícita de abreviaturas | 31 |

## 4. Fusiones propuestas para revisión

El CSV homónimo contiene la trazabilidad completa de ambos lados de cada par. La tabla siguiente resume las mismas candidaturas sin sustituir ese detalle.

| Categoría | ID | Anterior | Actual | Normalizado candidato | Estado vigente | Motivo |
|---|---|---|---|---|---|---|
| Contrata | `CTR-0009` | 2023-04: ENCARGADO GABINETE ALCALDIA | 2023-05: ENCARG. GABINETE ALCALDIA | `ALCALDIA ENCARGADO GABINETE` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0010` | 2024-05: ENCARG. CASA DE LA JUVENTUD | 2024-06: ENCG. CASA DE LA JUVENTUD | `CASA DE ENCARGADO JUVENTUD LA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0010` | 2024-06: ENCG. CASA DE LA JUVENTUD | 2024-07: ENCARG. CASA DE LA JUVENTUD | `CASA DE ENCARGADO JUVENTUD LA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0049` | 2024-02: ENC. EGIS MUNICIPAL | 2024-03: ENCARG. EGIS MUNICIPAL | `EGIS ENCARGADO MUNICIPAL` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0063` | 2023-09: ENCARG.DIFUSION MUNICIPAL CULTURA | 2023-10: ENC. DIFUSIÓN MUNICIPAL CULTURA | `CULTURA DIFUSION ENCARGADO MUNICIPAL` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0074` | 2024-10: ENCARG. FONDEVE Y PROF. LICITA | 2024-11: ENC. FONDEVE Y PROF. LICITA | `ENCARGADO FONDEVE LICITA PROFESIONAL Y` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0093` | 2023-09: ENCARG. OF. BIENESTAR. | 2023-10: ENC. OF. BIENESTAR | `BIENESTAR ENCARGADO OFICINA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0093` | 2024-04: ENC. OF. BIENESTAR | 2024-05: ENCARG. OF. BIENESTAR | `BIENESTAR ENCARGADO OFICINA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0095` | 2023-09: ENCARG. DEPTO. EJECUCION DE OBRAS | 2023-10: ENC. DEPTO . EJECUCIÓN DE OBRAS | `DE DEPARTAMENTO EJECUCION ENCARGADO OBRAS` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0097` | 2023-09: ENCARG. PARTICIPACION CIUDADANA | 2023-10: ENC. PARTICIPACIÓN CIUDADANA | `CIUDADANA ENCARGADO PARTICIPACION` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0099` | 2023-09: ENCARG. DEPTO. INFORMATICA | 2023-10: ENC. DEPTO. INFORMATICA | `DEPARTAMENTO ENCARGADO INFORMATICA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0118` | 2023-09: ENCARG. DE VIVIENDA | 2023-10: ENC. DE VIVIENDA | `DE ENCARGADO VIVIENDA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0127` | 2023-09: ENCARG. DE BIBLIO REDES | 2023-10: ENC. DE BIBLIO REDES | `BIBLIO DE ENCARGADO REDES` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0127` | 2024-01: ENC. DE BIBLIOREDES | 2024-02: ENCARGADO DE BIBLIOREDES | `BIBLIOREDES DE ENCARGADO` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0152` | 2023-09: ENCARG. OF. DISCAPACIDAD | 2023-10: ENC. OFICINA DISCAPACIDAD | `DISCAPACIDAD ENCARGADO OFICINA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0157` | 2023-09: ENCARG. GIM. MUNICIPAL | 2023-10: ENC. GIM MUNICIPAL | `ENCARGADO GIM MUNICIPAL` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0161` | 2023-09: ENCARG. DEPTO MUJER | 2023-10: ENC. DEPTO MUJER | `DEPARTAMENTO ENCARGADO MUJER` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0174` | 2023-09: ENCARG. DEPORTES | 2023-10: ENC. DEPORTES | `DEPORTES ENCARGADO` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0179` | 2023-09: ENCARG. OF. GESTION INTERNA MUNICIPAL | 2023-10: ENC. OF. GESTIÓN INTERNA MUNICIPAL | `ENCARGADO GESTION INTERNA MUNICIPAL OFICINA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0179` | 2024-03: ENCG. OF. GESTIÓN INTERNA | 2024-04: ENC. OF. GESTIÓN INTERNA | `ENCARGADO GESTION INTERNA OFICINA` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0181` | 2023-09: ENCARG. RECINTOS DEPORTIVOS | 2023-10: ENC. RECINTOS DEPORTIVOS | `DEPORTIVOS ENCARGADO RECINTOS` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0209` | 2023-09: ENCARG. BORDE COSTERO | 2023-10: ENC. BORDE COSTERO | `BORDE COSTERO ENCARGADO` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0218` | 2023-09: ENCARG. GESTION VECINAL | 2023-10: ENC. GESTIÓN VECINAL | `ENCARGADO GESTION VECINAL` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0228` | 2023-09: ENCARG. DEPTO RR.HH | 2023-10: ENC. DEPTO RR.HH | `DEPARTAMENTO ENCARGADO HH RR` | cambio_cargo | expansión explícita de abreviaturas |
| Contrata | `CTR-0243` | 2023-09: ENCARG. TRANSPORTE | 2023-10: ENC. TRANSPORTE | `ENCARGADO TRANSPORTE` | cambio_cargo | expansión explícita de abreviaturas |
| Planta | `PLT-2023-0008` | 2023-09: ENCARG. OF. CONSTRUCCION | 2023-10: ENC. OF. CONSTRUCCIÓN | `CONSTRUCCION ENCARGADO OFICINA` | cambio_cargo | expansión explícita de abreviaturas |
| Planta | `PLT-2023-0064` | 2024-02: ENCARG SISTEMAS COMP. | 2024-03: ENCARGADO SISTEMAS COMP. | `COMP ENCARGADO SISTEMAS` | cambio_cargo | expansión explícita de abreviaturas |
| Planta | `PLT-2023-0087` | 2024-04: JEFE DPTO. REGIST. PERS. JURID | 2024-05: JEFE. DEPTO REGIST. PERS. JURID | `DEPARTAMENTO JEFE JURID PERS REGIST` | cambio_cargo | expansión explícita de abreviaturas |
| Planta | `PLT-2023-0112` | 2024-12: JEFA DPTO. REMUNERACIONES | 2025-01: JEFA DEPTO. REMUNERACIONES | `DEPARTAMENTO JEFA REMUNERACIONES` | cambio_cargo | expansión explícita de abreviaturas |
| Planta | `PLT-2023-0124` | 2024-02: ENCARG. BODEGA MUNICIPAL | 2024-03: ENC. BODEGA MUNICIPAL | `BODEGA ENCARGADO MUNICIPAL` | cambio_cargo | expansión explícita de abreviaturas |
| Planta | `PLT-2023-0124` | 2024-11: ENC. BODEGA MUNICIPAL | 2024-12: ENCARG. BODEGA MUNICIPAL | `BODEGA ENCARGADO MUNICIPAL` | cambio_cargo | expansión explícita de abreviaturas |

## 5. Insumos y decisión requerida

| Maestro | Registros | SHA-256 |
|---|---:|---|
| `MAESTRO_Planta_Coronel_2023-2025_canonico_v1.xlsx` | 4927 | `9fc5e4a1784a9b43284c1af1c47de117f3abd9576d61e9b206ecb1135bf45a8e` |
| `MAESTRO_Contrata_Coronel_2023-2025_canonico_v1.xlsx` | 7616 | `578061f907e8f584f01ae5220302037a1c3f1836dca154b279903036c2d57fda` |
| `MAESTRO_CODTrabajo_Coronel_2023-2025_canonico_v1.xlsx` | 933 | `c843d1759055b68c281f9d88886b28d67f5e072905d759228002ff1d8a21f6ea` |
| `MAESTRO_Honorarios_Coronel_2023-2025_canonico_v1.xlsx` | 9464 | `860d1fc0d005be9a3722451cef15f56dc79ff21b5c00734c8801a04e676d3bde` |

**Decisión requerida:** revisar el CSV completo y aprobar, rechazar o enmendar las reglas y casos. Solo después de esa aprobación corresponde integrar el candidato al pipeline, regenerar fichas y declarar la mejora como aplicada. Hasta entonces, la interfaz debe rotularla como propuesta pendiente.
