# Validación de unicidad persona-período — Personal y Remuneraciones

**Fecha de ejecución:** 2026-11-18T02:35:08-03:00  
**Insumo:** maestros `canonico_v1.0.0`, 22.940 registros  
**Proyección:** trayectoria individual conforme a D-15  
**Resultado:** **APROBADA**  
**Ficha individual:** HABILITADA

## 1. Criterio y alcance

La validación comprueba: (1) unicidad de `registro_id`; (2) ausencia de `id_trabajador` vacío; (3) unicidad de `categoria + id_trabajador + periodo` sobre la proyección `canonica_trayectoria`; (4) que un ID no se asocie a varios nombres normalizados; y (5) que un nombre normalizado no tenga varios IDs dentro de una misma categoría. D-15 selecciona únicamente cuando existe exactamente una versión cuyo período de contenido coincide con el período nominal del archivo. No se desempata por monto, orden de fila ni posterioridad presumida y no se altera el período de contenido conforme a D-07.

Las versiones no seleccionadas permanecen íntegras como `version_alterna`. La comprobación transversal de nombres con IDs distintos es una advertencia separada: no prueba identidad ni duplicación entre categorías.

## 2. Resultados

| Control | Resultado |
|---|---:|
| Registros canónicos evaluados | 22.940 |
| Registros seleccionados para trayectoria | 22.938 |
| Versiones alternas preservadas | 2 |
| `registro_id` duplicados | 0 |
| `id_trabajador` vacíos | 0 |
| Colisiones originales | 2 |
| Colisiones resueltas por D-15 | 2 |
| Colisiones sin resolver | 0 |
| Colisiones en la proyección validada | 0 |
| IDs asociados a varios nombres normalizados | 0 |
| Nombres con varios IDs dentro de una categoría | 0 |
| Advertencias: nombres con IDs distintos entre categorías | 56 |

## 3. Resolución de las colisiones originales

### COT-2023-0015 — 2025-05

**Estado:** resuelta por D-15; 1 versión(es) con coincidencia contenido/archivo.

| Rol | Registro | Período nominal del archivo | Bruto CLP | Líquido CLP | Archivo | Fila CSV | SHA-256 |
|---|---|---|---:|---:|---|---:|---|
| canonica_trayectoria | `COT-202505-8DA800BA00` | 2025-05 | 1.541.381 | 1.394.922 | `05_CODTrabajo_Mayo_2025.csv` | 9 | `9643364813d70e193efa40eaf7739fccbb04eafa3fc250b3ed50b385ef0880d8` |
| version_alterna | `COT-202505-9D0CE3F70A` | 2025-07 | 1.541.381 | 1.394.849 | `07_CODTrabajo_Julio_2025.csv` | 29 | `5dd2c396042e17cd6c1a45955cfa6c22c65e2d37d87f161447c77f77d5fbd4b7` |

La selección es una convención documental para visualizar trayectoria, no una declaración de cuál cifra es jurídicamente correcta. Las versiones alternas se muestran en «Otra publicación del mismo período».

### PLT-2023-0032 — 2024-11

**Estado:** resuelta por D-15; 1 versión(es) con coincidencia contenido/archivo.

| Rol | Registro | Período nominal del archivo | Bruto CLP | Líquido CLP | Archivo | Fila CSV | SHA-256 |
|---|---|---|---:|---:|---|---:|---|
| canonica_trayectoria | `PLT-202411-8247F5515D` | 2024-11 | 2.094.352 | 2.225.384 | `11_Planta_Noviembre_2024.csv` | 25 | `878d2cfa3b86c141a813724d00680c9de85686e403971d1518e464f5c73e84c1` |
| version_alterna | `PLT-202411-3B54A1958D` | 2024-12 | 2.796.012 | 2.225.573 | `12_Planta_Diciembre_2024.csv` | 132 | `bad153e30fec298ba714282e3c60048fc44137a74cd4d47161f48cd72da8144f` |

La selección es una convención documental para visualizar trayectoria, no una declaración de cuál cifra es jurídicamente correcta. Las versiones alternas se muestran en «Otra publicación del mismo período».

## 4. Advertencias de identidad transversal

Se observaron **56 nombres normalizados con más de un ID entre categorías**. No se resuelven por semejanza de nombre. Las fichas se publican por ID dentro de su categoría; D-15 no crea ni autoriza una identidad global fusionada.

| Nombre normalizado | Identificadores | Categorías |
|---|---|---|
| AGUILERA BRAVO, DARWIN ANDRES | `CTR-0003`, `HON-0010` | Contrata, Honorarios |
| ALVAREZ TAPIA, JENNY JAZMIN | `CTR-0005`, `PLT-2023-0011` | Contrata, Planta |
| ALVIAL HENRIQUEZ, PEDRO ESTEBAN | `CTR-0006`, `PLT-2023-0012` | Contrata, Planta |
| ALVIAL RIOS, PEDRO ROMAN | `CTR-0007`, `PLT-2023-0014` | Contrata, Planta |
| ARELLANO ROJAS, BRYAN HUMBERTO | `CTR-0010`, `HON-0048` | Contrata, Honorarios |
| ARIAS AHUMADA, MARIOLY ANDREA | `CTR-0013`, `PLT-2023-0016` | Contrata, Planta |
| ARROS CRISOSTO, JAVIER ALEJANDRO | `CTR-0017`, `HON-0057` | Contrata, Honorarios |
| BERNALES HERNANDEZ, TATIANA COSNTANZA | `COT-2023-0005`, `PLT-2023-0172` | Código del Trabajo, Planta |
| BUSTOS MATUS, ROSA AMELIA | `CTR-0026`, `PLT-2023-0030` | Contrata, Planta |
| CARDENAS LEAL, NICOLAS SEBASTIAN | `COT-2023-0007`, `HON-0100` | Código del Trabajo, Honorarios |
| CARO PARRA, CARMEN SALOME | `COT-2023-0008`, `PLT-2023-0032` | Código del Trabajo, Planta |
| CARTES ALBORNOZ, JENNIFER JAZMIN | `CTR-0037`, `HON-0111`, `PLT-2023-0035` | Contrata, Honorarios, Planta |
| CASTILLO GARAI, NICOLAS BASTIAN | `CTR-0041`, `HON-0118` | Contrata, Honorarios |
| CISTERNAS OLGUIN, JORGE LUIS | `CTR-0054`, `HON-0132` | Contrata, Honorarios |
| CONCHA PENA, JOCELYN VERONICA | `CTR-0055`, `HON-0135`, `PLT-2023-0045` | Contrata, Honorarios, Planta |
| CUEVAS MENESES, JORGE ANDRES | `CTR-0061`, `HON-0150` | Contrata, Honorarios |
| DIAZ FERNANDEZ, FELIPE EDUARDO | `CTR-0062`, `HON-0161` | Contrata, Honorarios |
| ELGUETA HENRIQUEZ, JOCELYN PILAR | `CTR-0066`, `HON-0170` | Contrata, Honorarios |
| ESPINOZA ARANEDA, JORGE MAURICIO | `CTR-0069`, `HON-0180` | Contrata, Honorarios |
| ESPINOZA CRUCES, ARNOLDO RAIMUNDO | `CTR-0070`, `HON-0182`, `PLT-2023-0058` | Contrata, Honorarios, Planta |
| ESPINOZA VILLOUTA, JASER ABDON | `CTR-0072`, `HON-0189` | Contrata, Honorarios |
| FERNANDEZ SAEZ, IVONNE OLAYA | `CTR-0076`, `PLT-2023-0061` | Contrata, Planta |
| GATICA CATRIL, MACARENA DEL CARMEN | `CTR-0093`, `PLT-2023-0069` | Contrata, Planta |
| GONZALEZ DELGADO, CESAR ALEJANDRO | `CTR-0094`, `HON-0244`, `PLT-2023-0073` | Contrata, Honorarios, Planta |
| HENRIQUEZ ZUNIGA, STEPHANIE ARLETTE | `CTR-0101`, `HON-0263` | Contrata, Honorarios |
| IRRIBARRA CASTILLO, JORGE ABDON | `CTR-0105`, `PLT-2023-0081` | Contrata, Planta |
| JARA SAEZ, FELICITA DEL CARMEN | `CTR-0108`, `PLT-2023-0175` | Contrata, Planta |
| LEIVA PARRA, GONZALO ANDRES | `CTR-0113`, `HON-0298`, `PLT-2023-0090` | Contrata, Honorarios, Planta |
| LEPEZ GALLEGOS, LUIS MAURICIO | `CTR-0116`, `HON-0300` | Contrata, Honorarios |
| MEDINA OSSES, ADRIAN EDGARDO | `CTR-0124`, `HON-0332` | Contrata, Honorarios |
| MORALES INOSTROZA, LUIS LESTER | `CTR-0137`, `HON-0353` | Contrata, Honorarios |
| MUNOZ ALARCON, SANDRA DEL CARMEN | `CTR-0139`, `HON-0362` | Contrata, Honorarios |
| MUNOZ PENAILILLO, EDUARDO ANDRES | `CTR-0144`, `HON-0366` | Contrata, Honorarios |
| MUNOZ RIOS, SCARLETT NICOLETT | `COT-2023-0027`, `HON-0367` | Código del Trabajo, Honorarios |
| OCARES CANDIA, VICTOR MANUEL | `CTR-0150`, `HON-0380` | Contrata, Honorarios |
| OJEDA BARRALES, ROSA ALICIA | `CTR-0151`, `HON-0381`, `PLT-2023-0111` | Contrata, Honorarios, Planta |
| ORMENO PARRA, NATALIA BELEN | `COT-2023-0031`, `HON-0392` | Código del Trabajo, Honorarios |
| OSSES SOTO, CRISTIAN MARCELO | `CTR-0158`, `PLT-2023-0115` | Contrata, Planta |
| PACHECO PARADA, ALEXY RODRIGO | `CTR-0159`, `HON-0400` | Contrata, Honorarios |
| PARRA PARRA, MARIA ELENA | `CTR-0163`, `HON-0410` | Contrata, Honorarios |
| RETAMAL MANZANO, ALBERTO ADRIAN | `CTR-0178`, `HON-0436` | Contrata, Honorarios |
| ROA PENA, CARLOS PATRICIO | `CTR-0185`, `HON-0463` | Contrata, Honorarios |
| ROJAS DOMINGUEZ, CLAUDIA SOLANGE | `CTR-0189`, `HON-0474` | Contrata, Honorarios |
| ROMERO PARRA, MERYAN CICCIOLINA | `CTR-0190`, `HON-0479` | Contrata, Honorarios |
| SAAVEDRA CARRILLO, ALDO RENZO | `CTR-0193`, `PLT-2023-0137` | Contrata, Planta |
| SAEZ SANZANA, ERICK ENRIQUE | `COT-2023-0039`, `PLT-2023-0176` | Código del Trabajo, Planta |
| SALAS AGUILERA, JOHANNA CAROLINA | `CTR-0199`, `HON-0489` | Contrata, Honorarios |
| SANHUEZA GRANDON, GERSON ELIAS | `CTR-0204`, `HON-0505` | Contrata, Honorarios |
| SEGUEL ALLEN, JAIME RODRIGO | `CTR-0205`, `HON-0513` | Contrata, Honorarios |
| SEPULVEDA VALENZUELA, GUILLERMO IGNACIO | `CTR-0206`, `HON-0520` | Contrata, Honorarios |
| SILVA PARRAGA, FRANCIA ALEJANDRINA | `COT-2023-0042`, `PLT-2023-0152` | Código del Trabajo, Planta |
| SOTO PILCO, YESSENIA AMINADAB | `CTR-0208`, `HON-0527` | Contrata, Honorarios |
| SOTO VARELA, YINY DEL CARMEN | `CTR-0210`, `HON-0529` | Contrata, Honorarios |
| TORO GUAJARDO, FERNANDA | `CTR-0216`, `HON-0536` | Contrata, Honorarios |
| ULLOA VEGA, PAMELA ALEJANDRA | `CTR-0221`, `HON-0550`, `PLT-2023-0163` | Contrata, Honorarios, Planta |
| VIGUERAS ZANETTA, VIVIANNE ALEJANDRA | `CTR-0237`, `PLT-2023-0171` | Contrata, Planta |

## 5. Decisión de publicación

**Validación aprobada.** Se generan `data/fichas/<id_trabajador>.json` con 22,938 registros seleccionados y las versiones alternas íntegras. Los meses sin registro se declaran como ausencias y no se interpolan. No se incluye género ni campos derivados de nombre.

Los agregados continúan usando las 22.940 filas canónicas. **La suma de fichas no reconcilia con los agregados**, porque D-15 excluye dos versiones alternas solo de la proyección de trayectoria.

**Trazabilidad de esta conclusión:** generada automáticamente por `scripts/build_modulo_personal.py` desde los cuatro maestros canónicos; aplica D-15 a H-005 y H-006 sin modificar las fuentes.
