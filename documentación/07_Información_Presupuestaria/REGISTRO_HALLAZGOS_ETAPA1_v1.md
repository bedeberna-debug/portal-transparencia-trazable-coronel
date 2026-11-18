# REGISTRO DE HALLAZGOS — ETAPA 1

**Alcance:** cuatro BEP de diciembre de 2023 y 2025. Unidades monetarias: M$.  
**Tratamiento:** preservación literal; sin remapeo, corrección, imputación ni interpolación.  
**Trazabilidad:** la muestra identifica el archivo y SHA-256 en el informe principal; cada ocurrencia incluye página y línea. El CSV asociado contiene los 350 hallazgos con SHA-256 completo por fila.

## 1. Resumen

| Tipo | Ocurrencias | Códigos o relaciones únicas |
|---|---:|---:|
| Código fuera de catálogo, niveles 1–3 | 66 | 33 códigos |
| Detalle nivel 4/5 no representado en catálogo | 236 | 125 códigos |
| Padre distinto de suma de hijas directas | 46 controles | 24 relaciones documento–padre |
| Saldo distinto de vigente menos ejecutado | 2 | 2 líneas |
| **Total** | **350** | — |

Convenciones: en jerarquía, `diferencia = padre − suma de hijas`; en aritmética, `diferencia = saldo impreso − (vigente − ejecutado)`.

## 2. Códigos de niveles 1–3 ausentes del catálogo

Hallazgo de cobertura/versionado normativo. La ausencia en el catálogo vigente no prueba por sí sola invalidez histórica; no se fuerza el calce.

| Código PDF | Nivel | Denominación impresa | Ocurrencias y localización |
|---|---:|---|---|
| `05.03.002` | 3 | De la Subsecretaría de Desarrollo Regional y Administrativo | 2: Ingresos 2023, p. 1, l. 43; Ingresos 2025, p. 1, l. 41 |
| `05.03.007` | 3 | Del Tesoro Público | 2: Ingresos 2023, p. 1, l. 47; Ingresos 2025, p. 1, l. 46 |
| `08.02.001` | 3 | Multas - De Beneficio Municipal | 2: Ingresos 2023, p. 2, l. 25; Ingresos 2025, p. 2, l. 24 |
| `08.02.002` | 3 | Multas Art. 14, N° 6, Ley N° 18.695 – De Beneficio Fondo Común Municipal | 2: Ingresos 2023, p. 2, l. 28; Ingresos 2025, p. 2, l. 27 |
| `08.02.003` | 3 | Multas Ley de Alcoholes – De Beneficio Municipal | 2: Ingresos 2023, p. 2, l. 36; Ingresos 2025, p. 2, l. 33 |
| `08.02.004` | 3 | Multas Ley de Alcoholes – De Beneficio Servicios de Salud | 2: Ingresos 2023, p. 2, l. 38; Ingresos 2025, p. 2, l. 35 |
| `08.02.005` | 3 | Registro de Multas de Tránsito No Pagadas – De Beneficio Municipal | 2: Ingresos 2023, p. 2, l. 40; Ingresos 2025, p. 2, l. 37 |
| `08.02.006` | 3 | Registro de Multas de Tránsito No Pagadas – De Beneficio Otras Municipalidades | 2: Ingresos 2023, p. 2, l. 42; Ingresos 2025, p. 2, l. 39 |
| `08.02.007` | 3 | Multas Juzgado de Policía Local – De Beneficio Otras Municipalidades | 2: Ingresos 2023, p. 2, l. 45; Ingresos 2025, p. 2, l. 42 |
| `08.02.008` | 3 | Multas e Intereses | 2: Ingresos 2023, p. 2, l. 47; Ingresos 2025, p. 2, l. 44 |
| `08.04.001` | 3 | Arancel al Registro de Multas de Tránsito No Pagadas | 2: Ingresos 2023, p. 2, l. 52; Ingresos 2025, p. 2, l. 57 |
| `08.04.999` | 3 | Otros Fondos de Terceros | 2: Ingresos 2023, p. 2, l. 54; Ingresos 2025, p. 2, l. 59 |
| `08.99.999` | 3 | Otros | 2: Ingresos 2023, p. 2, l. 58; Ingresos 2025, p. 3, l. 16 |
| `13.01.001` | 3 | De la Comunidad - Programa Pavimentos Participativos | 2: Ingresos 2023, p. 3, l. 33; Ingresos 2025, p. 3, l. 37 |
| `13.01.999` | 3 | Otras | 2: Ingresos 2023, p. 3, l. 35; Ingresos 2025, p. 3, l. 39 |
| `13.03.002` | 3 | De la Subsecretaría de Desarrollo Regional y Administrativo | 2: Ingresos 2023, p. 3, l. 37; Ingresos 2025, p. 3, l. 41 |
| `13.03.005` | 3 | Del Tesoro Público | 2: Ingresos 2023, p. 3, l. 44; Ingresos 2025, p. 3, l. 45 |
| `24.01.001` | 3 | Fondos de Emergencia | 2: Gastos 2023, p. 6, l. 29; Gastos 2025, p. 6, l. 31 |
| `24.01.004` | 3 | Organizaciones Comunitarias | 2: Gastos 2023, p. 6, l. 30; Gastos 2025, p. 6, l. 32 |
| `24.01.005` | 3 | Otras Personas Jurídicas Privadas | 2: Gastos 2023, p. 6, l. 31; Gastos 2025, p. 6, l. 33 |
| `24.01.006` | 3 | Voluntariado | 2: Gastos 2023, p. 6, l. 32; Gastos 2025, p. 6, l. 34 |
| `24.01.007` | 3 | Asistencia Social a Personas Naturales | 2: Gastos 2023, p. 6, l. 33; Gastos 2025, p. 6, l. 35 |
| `24.01.008` | 3 | Premios y Otros | 2: Gastos 2023, p. 6, l. 34; Gastos 2025, p. 6, l. 36 |
| `24.01.999` | 3 | Otras Transferencias al Sector Privado | 2: Gastos 2023, p. 6, l. 35; Gastos 2025, p. 6, l. 37 |
| `24.03.002` | 3 | A los Servicios de Salud | 2: Gastos 2023, p. 6, l. 37; Gastos 2025, p. 6, l. 39 |
| `24.03.080` | 3 | A las Asociaciones | 2: Gastos 2023, p. 6, l. 39; Gastos 2025, p. 6, l. 41 |
| `24.03.090` | 3 | Al Fondo Común Municipal - Permisos de Circulación | 2: Gastos 2023, p. 6, l. 43; Gastos 2025, p. 6, l. 45 |
| `24.03.092` | 3 | Al Fondo Común Municipal - Multas | 2: Gastos 2023, p. 6, l. 46; Gastos 2025, p. 6, l. 48 |
| `24.03.099` | 3 | A Otras Entidades Públicas | 2: Gastos 2023, p. 6, l. 49; Gastos 2025, p. 6, l. 51 |
| `24.03.100` | 3 | A Otras Municipalidades | 2: Gastos 2023, p. 6, l. 50; Gastos 2025, p. 6, l. 52 |
| `24.03.101` | 3 | A Servicios Incorporados a su Gestión | 2: Gastos 2023, p. 6, l. 51; Gastos 2025, p. 6, l. 53 |
| `26.04.999` | 3 | Aplicación Otros Fondos de Terceros | 2: Gastos 2023, p. 7, l. 13; Gastos 2025, p. 7, l. 17 |
| `33.03.001` | 3 | A los Servicios Regionales de Vivienda y Urbanización | 2: Gastos 2023, p. 7, l. 51; Gastos 2025, p. 7, l. 52 |

## 3. Subniveles no representados por el catálogo

Son 236 ocurrencias y 125 códigos únicos de niveles 4/5. Se separan del grupo anterior porque el catálogo de 451 rutas solo representa subtítulo/ítem/asignación. El detalle íntegro, con denominación, página, línea y SHA-256, está en `REGISTRO_HALLAZGOS_ETAPA1_v1.csv`, filtrando `subtipo = fuera_catalogo_nivel_detalle_no_representado`.

| Muestra | Ocurrencias | Códigos únicos |
|---|---:|---:|
| Gastos 2023 | 95 | 95 |
| Ingresos 2023 | 26 | 26 |
| Gastos 2025 | 93 | 93 |
| Ingresos 2025 | 22 | 22 |
| **Total** | **236** | **125** |

## 4. Diferencias de jerarquía

Se listan las 46 diferencias padre–métrica. La denominación y los montos se mantienen como fueron extraídos.

| Muestra | Código padre | Denominación | Métrica | Padre | Suma hijas | Diferencia | Página/línea |
|---|---|---|---|---:|---:|---:|---|
| Gastos 2023 | `21` | C x P Gastos en Personal | Exigible | 3.628 | 3.629 | -1 | 1/15 |
| Gastos 2023 | `21.01.001.014` | Asignaciones Compensatorias | Devengado | 296.562 | 296.561 | +1 | 1/39 |
| Gastos 2023 | `21.01.001.014` | Asignaciones Compensatorias | Saldo | 2.170 | 2.171 | -1 | 1/39 |
| Gastos 2023 | `21.02.001` | Sueldos y Sobresueldos | Devengado | 3.039.131 | 3.039.132 | -1 | 2/37 |
| Gastos 2023 | `21.02.001` | Sueldos y Sobresueldos | Saldo | 334 | 333 | +1 | 2/37 |
| Gastos 2023 | `21.03` | Otras Remuneraciones | Devengado | 346.609 | 346.608 | +1 | 3/44 |
| Gastos 2023 | `21.03` | Otras Remuneraciones | Saldo | 6.746 | 6.747 | -1 | 3/44 |
| Gastos 2023 | `22` | C x P Bienes y Servicios de Consumo | Exigible | 880.900 | 880.899 | +1 | 4/13 |
| Gastos 2023 | `22` | C x P Bienes y Servicios de Consumo | Devengado | 16.267.772 | 16.267.771 | +1 | 4/13 |
| Gastos 2023 | `22` | C x P Bienes y Servicios de Consumo | Saldo | 356.559 | 356.560 | -1 | 4/13 |
| Gastos 2023 | `22.02` | Textiles, Vestuario y Calzado | Devengado | 78.191 | 78.192 | -1 | 4/17 |
| Gastos 2023 | `22.02` | Textiles, Vestuario y Calzado | Saldo | 12.814 | 12.813 | +1 | 4/17 |
| Gastos 2023 | `22.04` | Materiales de Uso o Consumo | Devengado | 449.202 | 449.201 | +1 | 4/27 |
| Gastos 2023 | `22.04` | Materiales de Uso o Consumo | Saldo | 108.104 | 108.105 | -1 | 4/27 |
| Gastos 2023 | `22.05` | Servicios Básicos | Devengado | 3.098.433 | 3.098.432 | +1 | 4/52 |
| Gastos 2023 | `22.05` | Servicios Básicos | Saldo | -142.519 | -142.518 | -1 | 4/52 |
| Gastos 2023 | `31` | C x P Iniciativas de Inversión | Exigible | 32.925 | 32.926 | -1 | 7/41 |
| Gastos 2023 | `31` | C x P Iniciativas de Inversión | Devengado | 4.368.920 | 4.368.921 | -1 | 7/41 |
| Gastos 2023 | `31` | C x P Iniciativas de Inversión | Saldo | 8.298.164 | 8.298.163 | +1 | 7/41 |
| Gastos 2025 | `21.01` | Personal de Planta | Devengado | 3.635.664 | 3.635.665 | -1 | 1/16 |
| Gastos 2025 | `21.01` | Personal de Planta | Saldo | 96.565 | 96.564 | +1 | 1/16 |
| Gastos 2025 | `21.01.001.014` | Asignaciones Compensatorias | Devengado | 290.332 | 290.331 | +1 | 1/39 |
| Gastos 2025 | `21.01.001.014` | Asignaciones Compensatorias | Saldo | 1.835 | 1.836 | -1 | 1/39 |
| Gastos 2025 | `21.01.004` | Remuneraciones Variables | Devengado | 182.862 | 182.861 | +1 | 2/24 |
| Gastos 2025 | `21.01.004` | Remuneraciones Variables | Saldo | 34.033 | 34.034 | -1 | 2/24 |
| Gastos 2025 | `21.02.003` | Asignaciones por Desempeño | Devengado | 501.316 | 501.315 | +1 | 3/19 |
| Gastos 2025 | `21.02.003` | Asignaciones por Desempeño | Saldo | -52.950 | -52.949 | -1 | 3/19 |
| Gastos 2025 | `21.02.004` | Remuneraciones Variables | Devengado | 350.890 | 350.891 | -1 | 3/32 |
| Gastos 2025 | `21.02.004` | Remuneraciones Variables | Saldo | 44.735 | 44.734 | +1 | 3/32 |
| Gastos 2025 | `22` | C x P Bienes y Servicios de Consumo | Devengado | 17.148.456 | 17.148.457 | -1 | 4/15 |
| Gastos 2025 | `22.02` | Textiles, Vestuario y Calzado | Devengado | 31.253 | 31.254 | -1 | 4/19 |
| Gastos 2025 | `22.02` | Textiles, Vestuario y Calzado | Saldo | 9.429 | 9.428 | +1 | 4/19 |
| Gastos 2025 | `22.04` | Materiales de Uso o Consumo | Exigible | 64.571 | 64.570 | +1 | 4/29 |
| Gastos 2025 | `22.05` | Servicios Básicos | Devengado | 3.512.919 | 3.512.921 | -2 | 4/54 |
| Gastos 2025 | `22.05` | Servicios Básicos | Saldo | 289.548 | 289.546 | +2 | 4/54 |
| Gastos 2025 | `22.07` | Publicidad Y Difusión | Exigible | 10.935 | 10.934 | +1 | 5/31 |
| Gastos 2025 | `22.08` | Servicios Generales | Exigible | 608.264 | 608.265 | -1 | 5/36 |
| Gastos 2025 | `22.08` | Servicios Generales | Devengado | 11.606.485 | 11.606.484 | +1 | 5/36 |
| Gastos 2025 | `22.08` | Servicios Generales | Saldo | 1.844.927 | 1.844.928 | -1 | 5/36 |
| Gastos 2025 | `22.09` | Arriendos | Devengado | 423.119 | 423.120 | -1 | 5/47 |
| Gastos 2025 | `22.09` | Arriendos | Saldo | 151.561 | 151.560 | +1 | 5/47 |
| Gastos 2025 | `23` | C x P Prestaciones de Seguridad Social | Devengado | 376.964 | 376.965 | -1 | 6/24 |
| Gastos 2025 | `23` | C x P Prestaciones de Seguridad Social | Saldo | 173.831 | 173.830 | +1 | 6/24 |
| Gastos 2025 | `29` | C x P Adquisición de Activos no Financieros | Exigible | 41.960 | 41.959 | +1 | 7/18 |
| Gastos 2025 | `29.05` | Máquinas y Equipos | Devengado | 17.114 | 17.113 | +1 | 7/24 |
| Gastos 2025 | `29.05` | Máquinas y Equipos | Saldo | 62.547 | 62.548 | -1 | 7/24 |

## 5. Diferencias aritméticas de línea

| Muestra | Código | Denominación | Saldo impreso | Vigente − devengado | Diferencia | Página/línea |
|---|---|---|---:|---:|---:|---|
| Gastos 2025 | `22.06` | Mantenimiento y Reparaciones | 784.425 | 784.424 | +1 | 5/15 |
| Gastos 2025 | `22.06.004` | Mantenimiento y Reparación de Máquinas y Equipos de Oficina | 73.303 | 73.302 | +1 | 5/22 |

## 6. Disposición

Todos los hallazgos quedan abiertos para revisión normativa o documental; ninguno fue resuelto alterando la fuente. La Etapa 2 permanece sin iniciar hasta autorización expresa del usuario.
