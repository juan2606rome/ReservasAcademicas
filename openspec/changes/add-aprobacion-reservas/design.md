# Design

## Context

Ver proposal.md - Why. Esta es la etapa E5 del plan de ingeniería, que depende de E1, E2, E3 y E4. Implementa el flujo de aprobación/rechazo según el diagrama de estados (sección 2.1) y las reglas de trazabilidad (sección 1.2 N5).

## Goals / Non-Goals

**Objetivos:**
- Permitir solo a administradores aprobar/rechazar
- Solo actuar sobre reservas PENDIENTE
- Exigir motivo al rechazar
- Registrar trazabilidad (quién, cuándo, motivo)
- Revalidar disponibilidad al aprobar
- Validar existencia de reserva

**No objetivos:**
- Cancelación por solicitante o administrador (etapa E6)
- Historial de cambios (etapa E6)
- Notificaciones

## Decisions

### Decisión: Solo administrador
- **Elección**: Usar autorización por rol ADMINISTRADOR
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Otros roles - no permitidos

### Decisión: Solo desde estado PENDIENTE
- **Elección**: Validar estado actual, solo PENDIENTE permite transición a APROBADA o RECHAZADA
- **Justificación**: Requerido explícitamente, coincide con diagrama de estados
- **Alternativas consideradas**: Permitir desde otros estados - rechazado

### Decisión: Rechazo requiere motivo
- **Elección**: Campo motivo obligatorio al rechazar, retornar 422 si falta
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Motivo opcional - rechazado

### Decisión: Trazabilidad obligatoria
- **Elección**: Registrar decidido_por (id usuario), decidido_en (timestamp UTC), motivo_decision
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Registro parcial - insuficiente

### Decisión: Revalidación al aprobar
- **Elección**: Al aprobar, volver a verificar que no hay solapamientos con otras reservas PENDIENTE o APROBADA
- **Justificación**: Protección contra condiciones de carrera o cambios entre creación y aprobación
- **Alternativas consideradas**: Confiar en validación inicial - arriesgado

### Decisión: Transición atómica
- **Elección**: Realizar validaciones y cambio de estado en transacción
- **Justificación**: Mantener integridad
- **Alternativas consideradas**: Sin transacción - vulnerable

## Risks / Trade-offs

- **[Autorización] Acceso no autorizado** → Mitigación: Verificar rol ADMINISTRADOR, retornar 403
- **[Estados] Transiciones inválidas** → Mitigación: Validar estado, retornar 409
- **[Integridad] Solapamientos al aprobar** → Mitigación: Revalidar disponibilidad
- **[Trazabilidad] Datos faltantes** → Mitigación: Registrar obligatoriamente todos los campos
- **[Validación] Rechazo sin motivo** → Mitigación: Validar motivo, retornar 422
- **[Datos] Reserva inexistente** → Mitigación: Verificar existencia, retornar 404
