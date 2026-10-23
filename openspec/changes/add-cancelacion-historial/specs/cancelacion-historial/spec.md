# Spec Delta

## Purpose

Esta capacidad proporciona la cancelación de reservas y el registro completo del historial de cambios de estado. Garantiza que cancelar libera el horario, que se registre toda la trazabilidad y que las consultas de historial respeten los permisos de cada rol.

## ADDED Requirements

### Requirement: Cancelación de reservas
The system SHALL permitir al solicitante cancelar sus propias reservas en estado PENDIENTE o APROBADA. The system SHALL permitir al administrador cancelar cualquier reserva en estado PENDIENTE o APROBADA. No SHALL permitir cancelar reservas en estado RECHAZADA o CANCELADA.

#### Scenario: Solicitante cancela su reserva PENDIENTE
- **GIVEN** un solicitante tiene una reserva en estado PENDIENTE
- **WHEN** cancela su propia reserva
- **THEN** la reserva pasa a estado CANCELADA
- **AND** el horario queda liberado

#### Scenario: Solicitante cancela su reserva APROBADA
- **GIVEN** un solicitante tiene una reserva en estado APROBADA
- **WHEN** cancela su propia reserva
- **THEN** la reserva pasa a estado CANCELADA
- **AND** el horario queda liberado

#### Scenario: Administrador cancela cualquier reserva
- **GIVEN** existe una reserva PENDIENTE o APROBADA de cualquier usuario
- **WHEN** un administrador cancela la reserva
- **THEN** la reserva pasa a estado CANCELADA
- **AND** el horario queda liberado

#### Scenario: No se cancela reserva RECHAZADA
- **GIVEN** existe una reserva en estado RECHAZADA
- **WHEN** se intenta cancelar
- **THEN** el sistema retorna error con código HTTP 409

#### Scenario: No se cancela reserva ya CANCELADA
- **GIVEN** existe una reserva en estado CANCELADA
- **WHEN** se intenta cancelar
- **THEN** el sistema retorna error con código HTTP 409

#### Scenario: Solicitante intenta cancelar reserva ajena
- **WHEN** un solicitante intenta cancelar una reserva que no le pertenece
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: Cancelar libera el horario
- **GIVEN** una reserva APROBADA ocupa un horario
- **WHEN** se cancela la reserva
- **THEN** ese horario queda disponible para nuevas reservas

### Requirement: Historial de cambios de estado
The system SHALL registrar cada cambio de estado de las reservas en la tabla HistorialReserva, incluyendo la creación de la solicitud. Cada registro SHALL contener estado anterior, estado nuevo, quién realizó el cambio, cuándo y un comentario.

#### Scenario: Registro al crear solicitud
- **WHEN** se crea una solicitud de reserva
- **THEN** se registra en historial: estado anterior null/vacío, estado nuevo PENDIENTE, cambiado_por usuario creador, cambiado_en timestamp, comentario

#### Scenario: Registro al aprobar
- **WHEN** un administrador aprueba una reserva
- **THEN** se registra en historial: estado anterior PENDIENTE, estado nuevo APROBADA, cambiado_por administrador, con comentario

#### Scenario: Registro al rechazar
- **WHEN** un administrador rechaza una reserva
- **THEN** se registra en historial: estado anterior PENDIENTE, estado nuevo RECHAZADA, cambiado_por administrador, con motivo como comentario

#### Scenario: Registro al cancelar
- **WHEN** se cancela una reserva
- **THEN** se registra en historial: estado anterior (PENDIENTE o APROBADA), estado nuevo CANCELADA, cambiado_por quien cancela, con comentario

### Requirement: Consulta de historial
The system SHALL permitir consultar el historial de reservas. El solicitante SHALL ver únicamente el historial de sus propias reservas. El administrador SHALL ver todo el historial. La consulta SHALL soportar filtros por espacio, estado y fecha.

#### Scenario: Solicitante consulta su historial
- **WHEN** un solicitante consulta el historial
- **THEN** el sistema retorna únicamente los registros de sus propias reservas

#### Scenario: Administrador consulta todo el historial
- **WHEN** un administrador consulta el historial
- **THEN** el sistema retorna todos los registros sin restricción

#### Scenario: Filtrar por espacio
- **WHEN** se consulta historial filtrando por espacio_id
- **THEN** el sistema retorna solo registros relacionados con ese espacio

#### Scenario: Filtrar por estado
- **WHEN** se consulta historial filtrando por estado
- **THEN** el sistema retorna solo registros con ese estado

#### Scenario: Filtrar por fecha
- **WHEN** se consulta historial filtrando por fecha
- **THEN** el sistema retorna solo registros en ese rango de fechas
