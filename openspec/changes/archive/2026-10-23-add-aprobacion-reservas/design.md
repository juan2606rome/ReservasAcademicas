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
- **Elección**: Campo motivo obligatorio al rechazar: no vacío ni solo espacios, máximo 500 caracteres, retornar 422 si falta o inválido. El motivo es opcional al aprobar y puede ser nulo.
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Motivo opcional al rechazar - rechazado

### Decisión: Trazabilidad obligatoria
- **Elección**: Registrar decidido_por (id usuario), decidido_en (timestamp UTC), motivo_decision. Las columnas decidido_por, decidido_en y motivo_decision se agregan a schema.sql en esta etapa (no "agregar si faltan").
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Registro parcial - insuficiente

### Decisión: Revalidación al aprobar
- **Elección**: Al aprobar, volver a verificar que no hay solapamientos con otras reservas PENDIENTE o APROBADA. La revalidación EXCLUYE la propia reserva (si no, siempre chocaría consigo misma). Por la decisión D6 del plan (PENDIENTE ocupa el espacio), un conflicto al aprobar solo puede darse por una inconsistencia de datos: es una validación defensiva. Por eso, la prueba de ese escenario inserta directamente en la base de datos una reserva solapada, en lugar de crearla por el flujo normal.
- **Justificación**: Protección contra condiciones de carrera o cambios entre creación y aprobación
- **Alternativas consideradas**: Confiar en validación inicial - arriesgado

### Decisión: Transición atómica
- **Elección**: Realizar validaciones y cambio de estado en transacción con BEGIN IMMEDIATE
- **Justificación**: Mantener integridad
- **Alternativas consideradas**: Sin transacción - vulnerable

### Decisión: Orden de validaciones
- **Elección**: Aplicar validaciones en el siguiente orden: 401, 403, 404, 422, 409. El orden se verifica con casos concretos: un solicitante que aprueba una reserva inexistente recibe 403 (no 404); un administrador que rechaza una reserva inexistente sin motivo recibe 404 (no 422); un administrador que rechaza una reserva ya APROBADA sin motivo recibe 422 (no 409). Cada caso tiene su propia prueba.
- **Justificación**: Definido explícitamente para evitar ambigüedad

### Decisión: No aprobar si inicio ya pasó
- **Elección**: No se puede aprobar una reserva cuyo inicio ya pasó: retornar 409. La reserva permanece en estado PENDIENTE sin cambios.
- **Justificación**: Requerido explícitamente

### Decisión: Endpoints
- **Elección**: POST /reservas/{id}/aprobar y POST /reservas/{id}/rechazar (con motivo en el cuerpo). Aprobar responde 200 y deja la reserva en APROBADA. Rechazar responde 200 y deja la reserva en RECHAZADA.
- **Justificación**: Requerido explícitamente

## Risks / Trade-offs

- **[Autorización] Acceso no autorizado** → Mitigación: Verificar rol ADMINISTRADOR, retornar 403
- **[Estados] Transiciones inválidas** → Mitigación: Validar estado, retornar 409
- **[Integridad] Solapamientos al aprobar** → Mitigación: Revalidar disponibilidad
- **[Trazabilidad] Datos faltantes** → Mitigación: Registrar obligatoriamente todos los campos
- **[Validación] Rechazo sin motivo** → Mitigación: Validar motivo, retornar 422
- **[Datos] Reserva inexistente** → Mitigación: Verificar existencia, retornar 404
