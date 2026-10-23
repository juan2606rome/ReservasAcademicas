# Design

## Context

Ver proposal.md - Why. Esta es la etapa E4 del plan de ingeniería, que depende de E1 (autenticación), E2 (roles/permisos) y E3 (gestión de espacios). Implementa el núcleo de reservas con validación de disponibilidad y prevención de solapamientos (sección 2.1, sección 3.3, decisión D5, D6).

## Goals / Non-Goals

**Objetivos:**
- Crear solicitudes en estado PENDIENTE
- Validar fechas, horarios y espacio
- Implementar prevención de solapamientos con intervalos [inicio, fin)
- Usar transacción BEGIN IMMEDIATE para atomicidad
- Implementar consulta de disponibilidad
- Manejar reservas simultáneas correctamente

**No objetivos:**
- Aprobación/rechazo (etapa E5)
- Cancelación (etapa E6)
- Historial de cambios (etapa E6)
- Reglas adicionales de negocio (etapa E7)

## Decisions

### Decisión: Estado inicial PENDIENTE
- **Elección**: Todas las solicitudes se crean en estado PENDIENTE
- **Justificación**: Según diagrama de estados en plan (sección 2.1), PENDIENTE es el estado inicial. Además D6 establece que PENDIENTE ocupa el espacio
- **Alternativas consideradas**: Crear directamente en APROBADA - rechazado

### Decisión: PENDIENTE y APROBADA ocupan espacio
- **Elección**: Solo PENDIENTE y APROBADA bloquean el horario. RECHAZADA y CANCELADA liberan el espacio
- **Justificación**: Decisión D6 del plan - evita duplicidad desde el momento de la solicitud
- **Alternativas consideradas**: Solo APROBADA ocupa - rechazado

### Decisión: Intervalos semiabiertos [inicio, fin)
- **Elección**: Usar intervalos [inicio, fin) donde fin no es inclusivo
- **Justificación**: Supuesto S3 del plan - permite reservas contiguas
- **Alternativas consideradas**: Intervalos cerrados - dificultaría reservas contiguas

### Decisión: Misma día obligatorio
- **Elección**: inicio y fin deben ser el mismo día
- **Justificación**: Supuesto S2 del plan
- **Alternativas consideradas**: Permitir reservas de varios días - fuera de alcance

### Decisión: Inicio no en el pasado
- **Elección**: Validar que inicio >= ahora
- **Justificación**: Previene reservas en el pasado
- **Alternativas consideradas**: Permitir reservas pasadas - poco práctico

### Decisión: Transacción con BEGIN IMMEDIATE
- **Elección**: Comprobar solapamientos y crear reserva en misma transacción con BEGIN IMMEDIATE
- **Justificación**: Decisión D5 del plan - previene condiciones de carrera en SQLite
- **Alternativas consideradas**: Solo validación sin transacción - vulnerable a concurrencia

### Decisión: Detección de solapamientos
- **Elección**: Dos intervalos [a1,a2) y [b1,b2) se solapan si a1 < b2 AND b1 < a2
- **Justificación**: Fórmula correcta para intervalos semiabiertos
- **Alternativas consideradas**: Otras fórmulas - incorrectas para este caso

### Decisión: Consulta de disponibilidad
- **Elección**: Endpoint para consultar franjas ocupadas por fecha y espacio
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Solo validación al crear - insuficiente

## Risks / Trade-offs

- **[Concurrencia] Condiciones de carrera** → Mitigación: Transacción BEGIN IMMEDIATE, prueba de concurrencia
- **[Integridad] Solapamientos** → Mitigación: Detección correcta con intervalos semiabiertos, validación en transacción
- **[Validación] Reservas en pasado** → Mitigación: Validar inicio >= tiempo actual
- **[Lógica] Reservas contiguas** → Mitigación: Usar intervalos semiabiertos [inicio, fin)
- **[Datos] Espacios inactivos** → Mitigación: Verificar estado activo antes de crear reserva, retornar 409
- **[Integridad] Espacios inexistentes** → Mitigación: Verificar existencia, retornar 404
- **[Rendimiento] Transacciones largas** → Mitigación: Mantener transacción lo más corta posible
