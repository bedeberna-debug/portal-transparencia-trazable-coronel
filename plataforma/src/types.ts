export const CATEGORIAS = ['Planta', 'Contrata', 'Código del Trabajo', 'Honorarios'] as const
export type Categoria = typeof CATEGORIAS[number]

export interface Fuente {
  archivo: string
  ruta_relativa: string
  url_respaldo?: string | null
  sha256: string
  filas_csv: number[]
  registros: number
  periodos: string[]
}
export interface Trazabilidad { portal_oficial: string; fuentes: Fuente[] }
export interface PanelRow {
  periodo: string
  categoria: Categoria
  dotacion_registros: number
  gasto_bruto_clp: number
  gasto_liquido_clp: number
  registros_bruta_no_informa: number
  registros_bruta_informada: number
  promedio_bruto_clp: number | null
  mediana_bruta_clp: number | null
  trazabilidad: Trazabilidad
}
export interface GlosarioEntry {
  termino: string
  seccion: string
  definicion: string
  fuente: string
  estado: 'aprobada'
  modulo_normativo: boolean
}
export interface EstamentoRow extends PanelRow { estamento: string }
export interface EstamentoEstimadoRow extends PanelRow { estamento_estimado: string }
export interface AnalisisCargo {
  estado: 'primer_registro' | 'sin_cambio' | 'variante_escritura' | 'posible_variante' | 'cambio_cargo'
  periodo_anterior: string | null
  cargo_anterior: string | null
  cargo_normalizado_proyecto: string
  cargo_anterior_normalizado_proyecto: string | null
  explicacion: string
}
export interface GeneroRow {
  periodo: string
  categoria: Categoria
  estamento: string
  registros: number
  femenino: number
  masculino: number
  no_clasificado: number
  femenino_pct: number
  masculino_pct: number
  leyenda: string
  trazabilidad: Trazabilidad
}
export interface HorasRow {
  periodo: string
  categoria: Categoria
  tipo: string
  estado: string
  horas: number | null
  monto_clp: number | null
  registros: number
  registros_cero_canonico: number | null
  registros_no_informa_explicito?: number
  registros_no_tiene_explicito?: number
  causa?: string | null
  trazabilidad: Trazabilidad
}
export interface Meta {
  modulo: string
  version: string
  generado_desde: string
  fecha_generacion: string
  periodo_inicio: string
  periodo_fin: string
  ultimo_periodo: string
  portal_oficial: string
  conteos: {
    registros_totales: number
    registros_por_categoria: Record<Categoria, number>
    trabajadores_id_por_categoria: Record<Categoria, number>
    archivos_fuente_modulo: number
    periodos: number
    registros_bruta_no_informa: number
  }
  totales_por_categoria: Record<Categoria, { gasto_bruto_clp: number; gasto_liquido_clp: number; registros_bruta_no_informa: number }>
  validacion_agregados: { controles: number; aprobadas: number; fallas: number; resultado: string }
  ficha_individual: { habilitada: boolean; estado_validacion: string; colisiones_id_periodo: number; colisiones_originales_id_periodo: number; colisiones_resueltas_d15: number; regla_resolucion: string; nota_reconciliacion: string }
  estamento_estimado: {
    decision: string
    version_mapeo: string
    leyenda_fija: string
    fuente_mapeo: { ruta_relativa: string; sha256: string }
    categorias_cubiertas: Categoria[]
    cobertura: Record<string, { clasificados: number; no_clasificables: number; totales: number; porcentaje_clasificados: number; cargos_clasificados: number; cargos_no_clasificables: number }>
    no_sobrescribe: string
  }
  glosario: { fuente_unica: string; sha256: string; entradas_aprobadas: number }
  licencias: {
    decision: string
    codigo: string
    datos_derivados: string
    atribucion: string
    datos_originales: string
  }
  privacidad: { genero: string; leyenda: string }
}
export interface ResumenCategoria {
  periodo_referencia: string
  distribucion_remuneraciones: { rango: string; registros: number; trazabilidad: Trazabilidad }[]
  antiguedad_por_anio_inicio: { anio_inicio: string; registros: number; trazabilidad: Trazabilidad }[]
  especificos: {
    tipo_pago?: { valor: string; registros: number }[]
    numero_cuotas?: { valor: string; registros: number }[]
    informes_estados?: Record<string, number>
    informes_por_mes?: { periodo: string; estado: string; registros: number }[]
    nota_respaldo?: string
  }
}
export interface DesvinculacionRow {
  periodo: string
  categoria: Categoria
  monto_desvinculacion_clp: number
  registros: number
  registros_cero_canonico: number
  trazabilidad: Trazabilidad
}
export interface Ausencia {
  periodo: string
  categoria: string
  dimension: string
  estado: string
  causa: string
}
export interface CommonData {
  meta: Meta
  panel: PanelRow[]
  estamentos: EstamentoRow[]
  estamentosEstimados: EstamentoEstimadoRow[]
  genero: GeneroRow[]
  horas: HorasRow[]
  resumen: Record<Categoria, ResumenCategoria>
  ausencias: { registros: Ausencia[]; periodos_sin_archivo_en_cuatro_categorias: string[]; informes_honorarios: Record<string, unknown> }
  fuentes: { registros: Array<Record<string, unknown>>; maestros_canonicos: Array<Record<string, unknown>>; manifiesto_informes: Record<string, unknown> }
  desvinculacion: DesvinculacionRow[]
  glosario: GlosarioEntry[]
}
export interface AsignacionDecodificada {
  codigo: string
  codigo_raw: string
  nombre: string | null
  estado: 'decodificado' | 'no_decodificado'
  nota: string | null
}
export interface ExplorerRow {
  registro_id: string
  id_trabajador: string
  anio: number
  mes_numero: number
  periodo: string
  categoria: Categoria
  nombre_original: string
  estamento: string
  estamento_raw: string
  cargo_funcion: string
  remuneracion_bruta_raw: string
  remuneracion_bruta_clp: number
  remuneracion_liquida_raw: string
  remuneracion_liquida_clp: number
  fecha_inicio_raw?: string
  fecha_inicio?: string
  fecha_termino_raw?: string
  fecha_termino?: string
  fecha_termino_tipo: string
  horas_extra_horas_total: number | null
  horas_extra_monto_total: number | null
  fuente_archivo: string
  fuente_ruta_relativa: string
  fuente_fila_csv: number
  fuente_sha256: string
  fuente_encoding: string
  fuente_separador: string
  informe_estado?: string
  informe_archivo_respaldo?: string | null
  informe_sha256?: string | null
  informe_respaldo_disponible?: boolean
  informe_fecha_verificacion?: string | null
  ficha_habilitada: boolean
  periodo_nominal_archivo?: string | null
  rol_trayectoria?: 'canonica_trayectoria' | 'version_alterna'
  regla_resolucion?: string | null
  version_alterna_de?: string | null
  motivo_version_alterna?: string | null
  estamento_estimado?: string | null
  estado_clasificacion_estimada?: 'clasificado' | 'no_clasificable' | null
  regla_estamento_estimado?: string | null
  origen_estamento_estimado?: string | null
  justificacion_estamento_estimado?: string | null
  cargo_normalizado_proyecto?: string
  asignaciones_especiales_raw?: string
  asignaciones_decodificadas?: AsignacionDecodificada[]
  analisis_cargo?: AnalisisCargo
  [key: string]: unknown
}
export interface TrayectoriaEntry {
  periodo: string
  estado: 'publicado' | 'sin_registro_publicado'
  causa_ausencia: string | null
  registro: ExplorerRow | null
  versiones_alternas: ExplorerRow[]
}
export interface FichaData {
  id_trabajador: string
  categoria: Categoria
  nombre_original: string
  nombres_publicados: string[]
  cargos: string[]
  estamentos: string[]
  periodo_inicio: string
  periodo_fin: string
  conteos: { periodos_publicados: number; ausencias: number; versiones_alternas: number; registros_fuente_conservados: number }
  regla_resolucion: string
  nota_reconciliacion: string
  privacidad: string
  trayectoria: TrayectoriaEntry[]
}
