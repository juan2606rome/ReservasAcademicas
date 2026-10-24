# Design

## Context

Ver proposal.md - Why. Esta es la etapa E6 del plan de ingeniería, que depende de E1-E5. Completa el ciclo de vida con cancelación e historial según diagrama de estados (sección 2.1) y trazabilidad (sección 1.2 N6).

## Goals / Non-Goals

**Objetivos:**
- Implementar cancelación con permisos correctos
- Registrar todo cambio de estado en HistorialReserva en la misma transacción que el cambio de estado
- Permitir consulta de historial con filtros y permisos
- Asegurar que cancelar libera el horario

**No objetivos:**
- Cambio de reglas de negocio (etapa E7)

## Decisions

### Decisión: Orden de validaciones en cancelación
- **Elección**: El orden de validaciones en cancelación SHALL ser 401 (sin token), 404 (reserva inexistente), 403 (propiedad/rol), 409 (estado cancelable). El sistema SHALL retornar el primer error según ese orden; si una reserva ajena está RECHAZADA, el error a retornar es 403 (no 409). Si la reserva no existe, el error es 404 (no 403).
- **Justificación**: Requerido explícitamente para evitar filtrar existencia o estado con validaciones de autorización.
- **Alternativas consideradas**: Otro orden - no especificado

### Decisión: Cancelación de reservas
- **Elección**: El solicitante solo puede cancelar sus propias reservas en estado PENDIENTE o APROBADA. El administrador puede cancelar cualquier reserva en estado PENDIENTE o APROBADA. Cancelar una reserva inexistente retorna 404. Cancelar con éxito retorna 200 y la reserva queda en estado CANCELADA. El comentario o motivo de la cancelación es opcional (máximo 500 caracteres). Las reservas en estado RECHAZADA o CANCELADA no se pueden cancelar (409).
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Otros permisos - no especificados

### Decisión: Historial completo
- **Elección**: Registrar creación, aprobación, rechazo y cancelación. Al crear la solicitud, estado_anterior es NULL. Comentarios por defecto: "Solicitud creada", "Aprobada" (o el motivo si se dio), el motivo del rechazo, y "Cancelada" (o el motivo si se dio).
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Solo cambios posteriores a creación - insuficiente

### Decisión: Transaccionalidad
- **Elección**: El cambio de estado y su registro en HistorialReserva ocurren en la misma transacción. Si falla el registro en HistorialReserva, el cambio de estado no debe aplicarse.
- **Justificación**: Requerido explícitamente para garantizar integridad
- **Alternativas consideradas**: Operaciones separadas - no garantiza atomicidad

### Decisión: Estructura de historial
- **Elección**: Tabla HistorialReserva con campos id, reserva_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario
- **Justificación**: Coincide con entidad definida en plan (sección 3.3)
- **Alternativas consideradas**: Estructura diferente - no especificada

### Decisión: Permisos de consulta de historial
- **Elección**: Solicitante ve solo lo suyo. Un solicitante nunca ve historial de reservas ajenas, ni siquiera con filtros (recibe lista vacía con 200). Administrador ve todo.
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Todos ven todo - violaría privacidad

### Decisión: Filtros de consulta
- **Elección**: GET /historial soporta filtros opcionales reserva_id, espacio_id, estado (se compara con estado_nuevo), desde y hasta (fechas AAAA-MM-DD en hora de Bogotá, inclusivas, sobre cambiado_en). Los valores de cambiado_en en la respuesta SHALL devolverse en formato ISO 8601 con zona horaria UTC. Valores inválidos retornan 422. Resultados del más reciente al más antiguo.
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Sin filtros o con otros filtros - no especificados

### Decisión: Estructura de módulos
- **Elección**: Crear los módulos cancelacion/ e historial/ con las capas repository, service, router según corresponda
- **Justificación**: Requerido explícitamente por las tareas
- **Alternativas consideradas**: Estructura distinta - no especificada

## Risks / Trade-offs

- **[Validación] Orden incorrecto** → Mitigación: Implementar validaciones en orden estricto 401, 404, 403, 409; asegurar precedencia (reserva ajena RECHAZADA → 403, no 409; reserva inexistente → 404, no 403)
- **[Transaccionalidad] Historial no registrado o registro falla** → Mitigación: Ejecutar cambio de estado y registro en la misma transacción; revertir si falla el registro
- **[Permisos] Cancelación no autorizada** → Mitigación: Verificar autenticación primero (401), existencia (404), propiedad/rol (403), estado cancelable (409)
- **[Estados] Cancelación inválida** → Mitigación: Validar estado, retornar 409
- **[Trazabilidad] Historial incompleto** → Mitigación: Registrar en todas las transiciones de estado con comentarios por defecto
- **[Integridad] Historial huérfano** → Mitigación: Foreign key a reservas
- **[Privacidad] Acceso a historial ajeno** → Mitigación: Filtrar por usuario para solicitantes, incluso con filtros; retornar lista vacía con 200
- **[Consulta] Filtros inválidos o zona horaria** → Mitigación: Validar valores de filtros, interpretar fechas en hora de Bogotá, inclusivas, filtrar sobre cambiado_en; devolver cambiado_en en formato ISO 8601 con zona horaria UTC; ordenar del más reciente al más antiguo
- **[Disponibilidad] Horario liberado** → Mitigación: Al cancelar, liberar espacio (CANCELADA no ocupa)
