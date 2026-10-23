# Design

## Context

Ver proposal.md - Why. Esta es la etapa E6 del plan de ingeniería, que depende de E1-E5. Completa el ciclo de vida con cancelación e historial según diagrama de estados (sección 2.1) y trazabilidad (sección 1.2 N6).

## Goals / Non-Goals

**Objetivos:**
- Implementar cancelación con permisos correctos
- Registrar todo cambio de estado en HistorialReserva
- Permitir consulta de historial con filtros y permisos
- Asegurar que cancelar libera el horario

**No objetivos:**
- Cambio de reglas de negocio (etapa E7)

## Decisions

### Decisión: Permisos de cancelación
- **Elección**: Solicitante solo cancela las suyas (PENDIENTE o APROBADA). Administrador cancela cualquiera (PENDIENTE o APROBADA)
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Otros permisos - no especificados

### Decisión: Estados cancelables
- **Elección**: Solo PENDIENTE o APROBADA se pueden cancelar. RECHAZADA y CANCELADA retornan 409
- **Justificación**: Requerido explícitamente, CANCELADA ya no es cancelable
- **Alternativas consideradas**: Permitir recancelar - rechazado

### Decisión: Historial completo
- **Elección**: Registrar creación, aprobación, rechazo y cancelación
- **Justificación**: Requerido explícitamente "incluida la creación"
- **Alternativas consideradas**: Solo cambios posteriores a creación - insuficiente

### Decisión: Estructura de historial
- **Elección**: Tabla HistorialReserva con estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario
- **Justificación**: Coincide con entidad definida en plan (sección 3.3)
- **Alternativas consideradas**: Estructura diferente - no especificada

### Decisión: Permisos de consulta de historial
- **Elección**: Solicitante ve solo lo suyo, administrador ve todo
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Todos ven todo - violaría privacidad

### Decisión: Filtros
- **Elección**: Soportar filtros por espacio, estado y fecha
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Sin filtros - menos útil

## Risks / Trade-offs

- **[Permisos] Cancelación no autorizada** → Mitigación: Verificar propiedad para solicitantes, rol para administradores, retornar 403
- **[Estados] Cancelación inválida** → Mitigación: Validar estado, retornar 409
- **[Trazabilidad] Historial incompleto** → Mitigación: Registrar en todas las transiciones de estado
- **[Integridad] Historial huérfano** → Mitigación: Foreign key a reservas
- **[Privacidad] Acceso a historial ajeno** → Mitigación: Filtrar por usuario para solicitantes
- **[Disponibilidad] Horario liberado** → Mitigación: Al cancelar, liberar espacio (CANCELADA no ocupa)
