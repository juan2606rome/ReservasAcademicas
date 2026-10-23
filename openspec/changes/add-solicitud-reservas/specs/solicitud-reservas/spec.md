# Spec Delta

## Purpose

Esta capacidad proporciona la creación de solicitudes de reserva y la consulta de disponibilidad para el sistema de reservas de espacios académicos. Implementa validaciones de fechas, prevención de solapamientos con transacciones atómicas, y garantiza que las reservas PENDIENTE y APROBADA ocupen el espacio correctamente.

## ADDED Requirements

### Requirement: Creación de solicitud de reserva
The system SHALL permitir crear una solicitud de reserva proporcionando espacio_id, inicio, fin y motivo. La solicitud SHALL crearse en estado PENDIENTE.

#### Scenario: Creación exitosa de solicitud
- **GIVEN** existe un espacio activo
- **WHEN** un usuario autenticado crea una solicitud con datos válidos
- **THEN** la solicitud se crea en estado PENDIENTE
- **AND** el sistema retorna confirmación exitosa

### Requirement: Validaciones de fecha y hora
The system SHALL validar que fin > inicio, que la reserva sea el mismo día, y que inicio no esté en el pasado. En caso de violación, SHALL retornar error con código HTTP 422.

#### Scenario: Fin menor o igual a inicio
- **WHEN** se intenta crear una reserva con fin <= inicio
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Reserva en días diferentes
- **WHEN** se intenta crear una reserva que comienza y termina en días diferentes
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Inicio en el pasado
- **WHEN** se intenta crear una reserva con fecha/hora de inicio en el pasado
- **THEN** el sistema retorna error con código HTTP 422

### Requirement: Validación de espacio
The system SHALL validar que el espacio exista y esté activo. Si el espacio no existe, SHALL retornar error con código HTTP 404. Si el espacio está inactivo, SHALL retornar error con código HTTP 409.

#### Scenario: Espacio inexistente
- **WHEN** se intenta crear una reserva para un espacio_id que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Espacio inactivo
- **WHEN** se intenta crear una reserva para un espacio inactivo
- **THEN** el sistema retorna error con código HTTP 409

### Requirement: Prevención de solapamientos
The system SHALL tratar los intervalos como [inicio, fin) (semiabiertos). Las reservas en estado PENDIENTE o APROBADA SHALL ocupar el espacio. Dos reservas SHALL solaparse si a1 < b2 y b1 < a2. Las reservas contiguas (una termina cuando otra empieza) SHALL estar permitidas. En caso de solapamiento, SHALL retornar error con código HTTP 409.

#### Scenario: Solapamiento detectado
- **GIVEN** existe una reserva PENDIENTE o APROBADA para un espacio
- **WHEN** se intenta crear otra reserva que se solapa con ella
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se crea la nueva reserva

#### Scenario: Reservas contiguas permitidas
- **GIVEN** existe una reserva que termina a las 10:00
- **WHEN** se intenta crear otra reserva que empieza a las 10:00 en el mismo espacio
- **THEN** el sistema permite la creación
- **AND** ambas reservas son válidas

#### Scenario: Reserva RECHAZADA o CANCELADA no ocupa espacio
- **GIVEN** existe una reserva RECHAZADA o CANCELADA para un espacio
- **WHEN** se intenta crear otra reserva en el mismo horario
- **THEN** el sistema permite la creación (no hay solapamiento)

### Requirement: Transacción atómica para prevención de solapamientos
The system SHALL realizar la comprobación de disponibilidad y el guardado de la reserva en una misma transacción iniciada con BEGIN IMMEDIATE. Esto SHALL prevenir condiciones de carrera entre solicitudes simultáneas.

#### Scenario: Dos solicitudes simultáneas
- **GIVEN** dos usuarios intentan crear reservas solapadas para el mismo espacio al mismo tiempo
- **WHEN** ambas solicitudes se procesan concurrentemente
- **THEN** solo una de las reservas se crea exitosamente
- **AND** la otra retorna error con código HTTP 409 por solapamiento

### Requirement: Consulta de disponibilidad
The system SHALL permitir consultar la disponibilidad de un espacio por fecha, mostrando las franjas ocupadas por reservas PENDIENTE o APROBADA.

#### Scenario: Consultar disponibilidad con franjas ocupadas
- **GIVEN** existen reservas PENDIENTE o APROBADA para un espacio en una fecha
- **WHEN** se consulta la disponibilidad del espacio para esa fecha
- **THEN** el sistema retorna las franjas ocupadas
- **AND** las reservas RECHAZADA o CANCELADA no aparecen como ocupadas
