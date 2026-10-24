# Design

## Context

Ver proposal.md - Why. Esta es la etapa E4 del plan de ingeniería, que depende de E1 (autenticación), E2 (roles/permisos) y E3 (gestión de espacios). Implementa el núcleo de reservas con validación de disponibilidad y prevención de solapamientos (sección 2.1, sección 3.3, decisión D5, D6).

## Goals / Non-Goals

**Objetivos:**
- Crear solicitudes en estado PENDIENTE
- El usuario de la solicitud sale del token, nunca del cuerpo de la petición (si el cuerpo trae un usuario, se ignora)
- Validar fechas, horarios y espacio
- Los campos inicio y fin llegan en formato ISO 8601 con zona horaria; si no traen zona horaria, retornar 422. Internamente se guardan en UTC. Las fechas inicio y fin se devuelven en formato ISO 8601 con zona horaria UTC en la creación, en la disponibilidad y en la consulta de reservas
- La regla "mismo día" y la consulta de disponibilidad por fecha se evalúan en hora de Bogotá (America/Bogota, UTC-5)
- Validar motivo obligatorio, no vacío y de máximo 500 caracteres
- Implementar prevención de solapamientos con intervalos [inicio, fin)
- El solapamiento se compara solo con reservas del MISMO espacio
- Usar transacción BEGIN IMMEDIATE para atomicidad
- Implementar consulta de disponibilidad
- Implementar consulta de reservas (GET /reservas, GET /reservas/{id}) con control por rol; filtros inválidos (estado no válido o espacio_id no numérico) retornan 422
- Manejar reservas simultáneas correctamente
- Orden de validaciones: 401, 422, 404, 409 (aplicar en ese orden cuando hay múltiples errores)

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
- **Elección**: inicio y fin deben ser el mismo día según la hora de Bogotá (America/Bogota, UTC-5)
- **Justificación**: Supuesto S2 del plan
- **Alternativas consideradas**: Permitir reservas de varios días - fuera de alcance

### Decisión: Inicio no en el pasado
- **Elección**: Validar que inicio >= ahora según la hora de Bogotá (America/Bogota, UTC-5)
- **Justificación**: Previene reservas en el pasado
- **Alternativas consideradas**: Permitir reservas pasadas - poco práctico

### Decisión: Zona horaria
- **Elección**: Los campos inicio y fin llegan en formato ISO 8601 con zona horaria; si no traen zona horaria, retornar 422. Internamente se guardan en UTC. "Mismo día" y disponibilidad se evalúan en hora de Bogotá (America/Bogota, UTC-5). Las fechas inicio y fin se devuelven en formato ISO 8601 con zona horaria UTC en la creación, en la disponibilidad y en la consulta de reservas
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Asumir zona horaria - rechazado

### Decisión: Usuario desde token
- **Elección**: El usuario_id sale del token de autenticación, nunca del cuerpo de la petición. Si el cuerpo trae un usuario, se ignora
- **Justificación**: Requerido explícitamente por seguridad
- **Alternativas consideradas**: Tomar del cuerpo - rechazado

### Decisión: Motivo obligatorio
- **Elección**: Motivo obligatorio, no vacío y de máximo 500 caracteres. Si faltan campos o es inválido, retornar 422
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Motivo opcional - rechazado

### Decisión: Transacción con BEGIN IMMEDIATE
- **Elección**: Comprobar solapamientos y crear reserva en misma transacción con BEGIN IMMEDIATE
- **Justificación**: Decisión D5 del plan - previene condiciones de carrera en SQLite
- **Alternativas consideradas**: Solo validación sin transacción - vulnerable a concurrencia

### Decisión: Detección de solapamientos
- **Elección**: Dos intervalos [a1,a2) y [b1,b2) se solapan si a1 < b2 AND b1 < a2. El solapamiento se compara solo con reservas del MISMO espacio. Una solicitud PENDIENTE contra otra PENDIENTE se solapa
- **Justificación**: Fórmula correcta para intervalos semiabiertos, con alcance por espacio
- **Alternativas consideradas**: Otras fórmulas - incorrectas para este caso; solapamiento entre espacios - rechazado

### Decisión: Consulta de disponibilidad
- **Elección**: GET /reservas/disponibilidad?espacio_id=...&fecha=AAAA-MM-DD para cualquier usuario autenticado. Fecha evaluada en hora de Bogotá. Devuelve franjas ocupadas ordenadas por inicio, cada una con inicio, fin y estado, sin datos de usuarios. Inicio y fin en formato ISO 8601 con zona horaria UTC. Sin reservas: lista vacía 200. Espacio inexistente: 404. Fecha inválida o faltante: 422
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Solo validación al crear - insuficiente

### Decisión: Consulta de reservas
- **Elección**: GET /reservas (solicitante ve solo las suyas, administrador todas; filtros opcionales estado y espacio_id; más recientes primero; filtros inválidos estado no válido o espacio_id no numérico: 422; inicio/fin en UTC ISO 8601) y GET /reservas/{id} (dueño o administrador; ajena siendo solicitante: 403; inexistente: 404; inicio/fin en UTC ISO 8601)
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Sin listado - insuficiente

### Decisión: Orden de validaciones
- **Elección**: Cuando hay varios errores, el orden es 401, 422, 404, 409. Casos: sin token+datos inválidos -> 401; fechas inválidas + espacio_id inexistente -> 422; petición válida sobre espacio inexistente -> 404; petición válida sobre espacio inactivo que además se solaparía -> 409
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Otro orden - rechazado

## Risks / Trade-offs

- **[Concurrencia] Condiciones de carrera** → Mitigación: Transacción BEGIN IMMEDIATE, prueba de concurrencia
- **[Integridad] Solapamientos** → Mitigación: Detección correcta con intervalos semiabiertos, validación en transacción, solo mismo espacio
- **[Validación] Reservas en pasado** → Mitigación: Validar inicio >= tiempo actual en hora de Bogotá
- **[Lógica] Reservas contiguas** → Mitigación: Usar intervalos semiabiertos [inicio, fin)
- **[Datos] Espacios inactivos** → Mitigación: Verificar estado activo antes de crear reserva, retornar 409
- **[Integridad] Espacios inexistentes** → Mitigación: Verificar existencia, retornar 404
- **[Zona horaria] Errores de interpretación** → Mitigación: Requerir zona horaria en ISO 8601, evaluar "mismo día" y disponibilidad en hora de Bogotá (UTC-5), guardar en UTC
- **[Seguridad] Usuario desde cuerpo** → Mitigación: Siempre tomar usuario_id del token
- **[Validación] Motivo inválido** → Mitigación: Validar obligatorio, no vacío, máximo 500 caracteres
- **[Rendimiento] Transacciones largas** → Mitigación: Mantener transacción lo más corta posible
