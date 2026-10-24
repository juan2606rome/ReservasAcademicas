# Spec Delta

## Purpose

Esta capacidad proporciona la aprobación y rechazo de solicitudes de reserva por parte del administrador, garantizando el control de acceso, transiciones válidas, trazabilidad de las decisiones y validación de disponibilidad al aprobar.

## ADDED Requirements

### Requirement: Solo administrador puede aprobar o rechazar
El sistema SHALL permitir aprobar o rechazar reservas únicamente a usuarios con rol ADMINISTRADOR. Si un solicitante intenta realizar estas acciones, el sistema SHALL retornar error con código HTTP 403.

#### Scenario: Administrador aprueba reserva
- **WHEN** un usuario con rol ADMINISTRADOR aprueba una reserva en estado PENDIENTE
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado APROBADA

#### Scenario: Administrador rechaza reserva
- **WHEN** un usuario con rol ADMINISTRADOR rechaza una reserva en estado PENDIENTE
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado RECHAZADA

#### Scenario: Solicitante intenta aprobar
- **WHEN** un usuario con rol SOLICITANTE intenta aprobar una reserva
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: Solicitante intenta rechazar
- **WHEN** un usuario con rol SOLICITANTE intenta rechazar una reserva
- **THEN** el sistema retorna error con código HTTP 403

### Requirement: Solo se puede actuar sobre reservas en estado PENDIENTE
El sistema SHALL permitir aprobar o rechazar únicamente reservas en estado PENDIENTE. Si la reserva está en otro estado, el sistema SHALL retornar error con código HTTP 409.

#### Scenario: Aprobar reserva ya aprobada
- **GIVEN** existe una reserva en estado APROBADA
- **WHEN** un administrador intenta aprobarla nuevamente
- **THEN** el sistema retorna error con código HTTP 409

#### Scenario: Rechazar reserva ya rechazada
- **GIVEN** existe una reserva en estado RECHAZADA
- **WHEN** un administrador intenta rechazarla nuevamente
- **THEN** el sistema retorna error con código HTTP 409

#### Scenario: Aprobar reserva cancelada
- **GIVEN** existe una reserva en estado CANCELADA
- **WHEN** un administrador intenta aprobarla
- **THEN** el sistema retorna error con código HTTP 409

### Requirement: Rechazo exige motivo
El sistema SHALL exigir un motivo para rechazar una reserva. El motivo es obligatorio al rechazar: no vacío ni solo espacios, máximo 500 caracteres. Si no se proporciona motivo o es inválido, el sistema SHALL retornar error con código HTTP 422. El motivo es opcional al aprobar y puede ser nulo.

#### Scenario: Rechazo sin motivo
- **WHEN** un administrador intenta rechazar una reserva sin proporcionar motivo
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Rechazo con motivo vacío o solo espacios
- **WHEN** un administrador intenta rechazar una reserva con motivo vacío o solo espacios
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Rechazo con motivo excesivo
- **WHEN** un administrador intenta rechazar una reserva con un motivo de más de 500 caracteres
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Rechazo con motivo válido
- **WHEN** un administrador rechaza una reserva proporcionando un motivo válido
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado RECHAZADA

#### Scenario: Aprobar sin motivo
- **WHEN** un administrador aprueba una reserva sin proporcionar motivo
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado APROBADA

### Requirement: Trazabilidad de la decisión
El sistema SHALL registrar quién decidió, cuándo y el motivo de la decisión para toda acción de aprobación o rechazo. Las columnas decidido_por, decidido_en y motivo_decision se agregan a schema.sql en esta etapa.

#### Scenario: Registro de aprobación
- **WHEN** un administrador aprueba una reserva
- **THEN** el sistema registra decidido_por (id del administrador), decidido_en (timestamp) y motivo_decision puede ser nulo

#### Scenario: Registro de rechazo
- **WHEN** un administrador rechaza una reserva
- **THEN** el sistema registra decidido_por (id del administrador), decidido_en (timestamp) y el motivo proporcionado (no vacío)

### Requirement: Revalidación al aprobar
El sistema SHALL volver a validar la disponibilidad al aprobar una reserva para evitar conflictos que puedan haberse generado. La revalidación EXCLUYE la propia reserva (de lo contrario siempre chocaría consigo misma). Por la decisión D6 del plan (PENDIENTE ocupa el espacio), un conflicto al aprobar solo puede darse por una inconsistencia de datos: es una validación defensiva.

#### Scenario: Aprobar sin conflictos
- **GIVEN** una reserva en estado PENDIENTE sin conflictos con otras reservas activas
- **WHEN** un administrador la aprueba
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado APROBADA

#### Scenario: Aprobar con conflicto
- **GIVEN** una reserva en estado PENDIENTE que ahora solapa con otra reserva APROBADA
- **WHEN** un administrador intenta aprobarla
- **THEN** el sistema retorna error con código HTTP 409
- **AND** la reserva permanece en estado PENDIENTE sin cambios

### Requirement: Reserva inexistente
El sistema SHALL retornar error con código HTTP 404 si la reserva no existe.

#### Scenario: Aprobar reserva inexistente
- **WHEN** un administrador intenta aprobar una reserva con id inexistente
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Rechazar reserva inexistente
- **WHEN** un administrador intenta rechazar una reserva con id inexistente
- **THEN** el sistema retorna error con código HTTP 404

### Requirement: No se puede aprobar una reserva cuyo inicio ya pasó
El sistema SHALL retornar error con código HTTP 409 si se intenta aprobar una reserva cuyo inicio ya pasó.

#### Scenario: Aprobar reserva con inicio ya pasado
- **GIVEN** una reserva en estado PENDIENTE cuyo inicio ya pasó
- **WHEN** un administrador intenta aprobarla
- **THEN** el sistema retorna error con código HTTP 409
- **AND** la reserva permanece en estado PENDIENTE sin cambios

### Requirement: Orden de validaciones
El sistema SHALL aplicar las validaciones en el siguiente orden: 401, 403, 404, 422, 409.

#### Scenario: Solicitante intenta aprobar una reserva inexistente
- **GIVEN** un usuario con rol SOLICITANTE y una reserva con id inexistente
- **WHEN** el solicitante intenta aprobarla
- **THEN** el sistema retorna error con código HTTP 403 (no 404)

#### Scenario: Administrador rechaza una reserva inexistente sin motivo
- **GIVEN** una reserva con id inexistente
- **WHEN** un administrador intenta rechazarla sin proporcionar motivo
- **THEN** el sistema retorna error con código HTTP 404 (no 422)

#### Scenario: Administrador rechaza una reserva ya APROBADA sin motivo
- **GIVEN** existe una reserva en estado APROBADA
- **WHEN** un administrador intenta rechazarla sin proporcionar motivo
- **THEN** el sistema retorna error con código HTTP 422 (no 409)

### Requirement: Endpoints y transacción
El sistema SHALL exponer los endpoints POST /reservas/{id}/aprobar y POST /reservas/{id}/rechazar (con motivo en el cuerpo). La validación y el cambio de estado ocurren en la misma transacción con BEGIN IMMEDIATE.

#### Scenario: Aprobar mediante endpoint
- **WHEN** un administrador envía POST /reservas/{id}/aprobar sin motivo o con motivo nulo
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado APROBADA

#### Scenario: Rechazar mediante endpoint
- **WHEN** un administrador envía POST /reservas/{id}/rechazar con motivo en el cuerpo
- **THEN** el sistema responde 200
- **AND** la reserva queda en estado RECHAZADA
