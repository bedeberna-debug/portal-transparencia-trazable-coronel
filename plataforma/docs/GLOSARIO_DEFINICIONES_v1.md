# Glosario canónico de definiciones del proyecto

**Portal de Transparencia Trazable — Municipalidad de Coronel**
**Versión:** v1 · 17-11-2026
**Regla de uso:** toda definición que aparezca en la interfaz de cualquier módulo sale de este archivo. Los chats de construcción proponen borradores; el chat de coordinación aprueba. El futuro módulo de marco normativo expande estas entradas con fichas profundas y conexiones, sin contradecirlas.

**Formato de cada entrada:** término · definición ciudadana (máx. ~60 palabras) · fuente normativa · notas de verificación · estado (📝 borrador / ✅ aprobada) · usado en.

---

## Categorías de vínculo

### Planta — ✅
Funcionarios municipales con nombramiento en la planta de personal aprobada por acto administrativo. Rige el Estatuto Administrativo (Ley 18.883): escalafón, grado y carrera funcionaria. Es el vínculo más estable y con más garantías.
**Fuente:** Ley 18.883 (Estatuto Administrativo para Funcionarios Municipales).
**Notas:** verificar artículo exacto sobre planta y escalafón con el marco normativo de la Fase 1.
**Usado en:** módulo Personal (pendiente integración SC-02).

### Contrata — ✅
Funcionarios municipales contratados para desempeñar funciones en la planta a contrata, a plazo fijo renovable. También rige el Estatuto Administrativo (Ley 18.883), con menos estabilidad que la planta: el vínculo vence y depende de renovación.
**Fuente:** Ley 18.883.
**Notas:** verificar régimen de renovación y si la planta a contrata se aprueba por acto administrativo (conexión TP-19).
**Usado en:** módulo Personal (pendiente integración SC-02).

### Código del Trabajo — ✅
Personas contratadas bajo el Código del Trabajo común (como un empleador privado), no por el Estatuto municipal. La ley permite este vínculo para labores específicas, típicamente operativas (aseo, cementerio, servicios directos).
**Fuente:** Código del Trabajo; Ley 18.883 (norma que habilita este vínculo — verificar artículo).
**Notas:** verificar alcance exacto de la habilitación.
**Usado en:** módulo Personal (pendiente integración SC-02).

### Honorarios — ✅
Personas que prestan servicios por honorarios mediante contrato, sin vínculo de planta ni contrata: cobran por prestación, sin carrera funcionaria ni estabilidad, usualmente por programas o funciones específicas. La transparencia exige publicar el informe de funciones de cada mes pagado.
**Fuente:** Ley 18.883; IGTA (Res. Ex. N°80/2026 CPLT, párrafo 4: descripción de función e informe de funciones).
**Notas:** —.
**Usado en:** módulo Personal (pendiente integración SC-02).

---

## Estamentos (clasificación funcional)

### Estamento — ✅
Clasificación funcional del cargo dentro del escalafón municipal: Directivo, Profesional, Técnico, Administrativo o Auxiliar. Indica la naturaleza de la función, no el sueldo. En la plataforma puede mostrarse el publicado por el municipio o el estimado por el proyecto (con leyenda).
**Fuente:** Ley 18.883 (escalafón — verificar artículo).
**Notas:** en los datos de Coronel aparecen además "Jefatura", "Alcalde" y "Otro"; documentar su origen cuando se integren.
**Usado en:** módulo Personal (pendiente integración SC-02).

### Directivo — ✅
Personal que ejerce dirección superior de unidades o áreas municipales, con responsabilidad de gestión y decisiones institucionales.
**Fuente:** Ley 18.883 (escalafón).
**Usado en:** módulo Personal.

### Profesional — ✅
Personal que desempeña funciones que requieren título profesional universitario.
**Fuente:** Ley 18.883 (escalafón).
**Usado en:** módulo Personal.

### Técnico — ✅
Personal que desempeña funciones que requieren formación técnica de nivel superior o especializada.
**Fuente:** Ley 18.883 (escalafón).
**Usado en:** módulo Personal.

### Administrativo — ✅
Personal de apoyo administrativo: secretaría, digitación, gestión documental, atención y trámites internos.
**Fuente:** Ley 18.883 (escalafón).
**Usado en:** módulo Personal.

### Auxiliar — ✅
Personal de apoyo operativo y servicios: aseo, vigilancia, alimentación, oficios manuales y labores de cuidado.
**Fuente:** Ley 18.883 (escalafón).
**Usado en:** módulo Personal.

---

## Conceptos de la plataforma (propios del proyecto)

### Persona-mes — ✅
Unidad de conteo de la plataforma: una persona en un mes específico. Si alguien trabajó los 36 meses, cuenta 36 veces en la serie. Los totales de "dotación" son personas-mes, no personas únicas.
**Fuente:** decisión de diseño (especificación módulo Personal, regla 7.1).
**Usado en:** módulo Personal.

### No informa / No tiene — ✅
Valor publicado por el municipio cuando no declara un dato. La plataforma lo muestra como categoría visible y nunca lo convierte en cero silencioso: en los cálculos de promedios y medianas estos registros se excluyen y se cuenta cuántos son.
**Fuente:** dato de la fuente + regla de visualización 3.1.
**Usado en:** módulo Personal.

### Estamento estimado — ✅
Clasificación funcional calculada por el proyecto a partir del texto del cargo publicado, cuando el estamento publicado no describe la función (Honorarios y parte de Código del Trabajo). No es clasificación oficial del municipio. "No clasificable" se muestra cuando el texto no permite estimar.
**Fuente:** decisión D-17; metodología en MAPEO_ESTAMENTO_ESTIMADO_v1.1.
**Usado en:** módulo Personal.

### Trayectoria (convención D-15) — ✅
Serie mensual de una persona construida por la plataforma. Cuando el municipio publicó dos versiones distintas del mismo mes, la trayectoria muestra la versión del archivo de ese mes y conserva la otra como "otra publicación del mismo período". Las sumas de fichas pueden no calzar con los totales generales por esta convención.
**Fuente:** decisión D-15.
**Usado en:** módulo Personal (ficha individual).

### Asignaciones especiales — ✅
Conceptos de asignaciones especiales que el municipio declara aplicables a un registro de remuneraciones, identificados mediante los códigos del nomenclátor del CPLT. La fuente publica qué conceptos aplican, no el monto de cada uno; los montos van incluidos en la remuneración bruta.
**Fuente:** Consejo para la Transparencia (CPLT), Oficio N.° 22003/2025 y plantilla oficial «Tipologías y Asignaciones Especiales».
**Usado en:** módulo Personal (ficha individual y explorador).

---

### Cola de términos pendientes (agregar a medida que los módulos los necesiten)
- Remuneración bruta / líquida · horas extraordinarias · viáticos · desvinculación · cuotas de honorarios · informe de funciones · acto administrativo · transparencia activa / pasiva.

### Transparencia trazable — ✅
Nombre propio de esta plataforma y su estándar: toda cifra publicada puede perseguirse hasta su documento fuente (archivo, fila y huella digital), y toda ausencia se declara en vez de ocultarse. No es sinónimo de "transparencia activa": esa es la obligación legal que origina los datos; este portal es un producto distinto construido sobre ellos.
**Fuente:** decisión D-18 del proyecto.
**Usado en:** portada, encabezados y metadatos de toda la plataforma.
