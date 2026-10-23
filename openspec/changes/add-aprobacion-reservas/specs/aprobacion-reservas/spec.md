# Spec Delta

## Purpose

Esta capacidad proporciona la aprobación y rechazo de solicitudes de reserva por parte del administrador, garantizando el control de acceso, transiciones válidas, trazabilidad de las decisiones y validación de disponibilidad al aprobar.

## ADDED Requirements

### Requirement: Solo administrador puede aprobar o rechazar
The system SHALL permitir aprobar o rechazar reservas únicamente a usuarios con rol ADMINISTRADOR. Si un solicitante intenta realizar estas acciones, SHALL retornar error con código HTTP 403.

#### Scenario: Administrador aprueba reserva
- **WHEN** un usuario con rol ADMINISTRADOR aprueba una reserva en estado PENDIENTE
- **THEN** el sistema permite la operación

#### Scenario: Solicitante intenta aprobar
- **WHEN** un usuario con rol SOLICITANTE intenta aprobar una reserva
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: Solicitante intenta rechazar
- **WHEN** un usuario con rol SOLICITANTE intenta rechazar una reserva
- **THEN** el sistema retorna error con código HTTP 403

### Requirement: Solo se puede actuar sobre reservas en estado PENDIENTE
The system SHALL permitir aprobar o rechazar únicamente reservas en estado PENDIENTE. Si la reserva está en otro estado, SHALL retornar error con código HTTP 409.

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
The system SHALL exigir un motivo para rechazar una reserva. Si no se proporciona motivo, SHALL retornar error con código HTTP 422.

#### Scenario: Rechazo sin motivo
- **WHEN** un administrador intenta rechazar una reserva sin proporcionar motivo
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Rechazo con motivo
- **WHEN** un administrador rechaza una reserva proporcionando un motivo
- **THEN** el sistema acepta la operación

### Requirement: Trazabilidad de la decisión
The system SHALL registrar quién decidió, cuándo y el motivo de la decisión para toda acción de aprobación o rechazo.

#### Scenario: Registro de aprobación
- **WHEN** un administrador aprueba una reserva
- **THEN** el sistema registra decidido_por (id del administrador), decidido_en (timestamp) y motivo_decision

#### Scenario: Registro de rechazo
- **WHEN** un administrador rechaza una reserva
- **THEN** el sistema registra decidido_por (id del administrador), decidido_en (timestamp) y el motivo proporcionado

### Requirement: Revalidación al aprobar
The system SHALL volver a validar la disponibilidad al aprobar una reserva para evitar conflictos que puedan haberse generado.

#### Scenario: Aprobar sin conflictos
- **GIVEN** una reserva en estado PENDIENTE sin conflictos con otras reservas activas
- **WHEN** un administrador la aprueba
- **THEN** el sistema la aprueba exitosamente

#### Scenario: Aprobar con conflicto
- **GIVEN** una reserva en estado PENDIENTE que ahora solapa con otra reserva APROBADA
- **WHEN** un administrador intenta aprobarla
- **THEN** el sistema rechaza la aprobación por conflicto de disponibilidad
- **AND** la reserva permanece en estado PENDIENTE o se maneja según la lógica definida

### Requirement: Reserva inexistente
The system SHALL retornar error con código HTTP 404 si la reserva no existe.

#### Scenario: Aprobar reserva inexistente
- **WHEN** un administrador intenta aprobar una reserva con id inexistente
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Rechazar reserva inexistente
- **WHEN** un administrador intenta rechazar una reserva con id inexistente
- **THEN** el sistema retorna error con código HTTP 404
