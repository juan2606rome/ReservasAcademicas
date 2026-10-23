# Spec Delta

## Purpose

Esta capacidad proporciona la cancelación de reservas y el registro completo del historial de cambios de estado. Garantiza que cancelar libera el horario, que se registre toda la trazabilidad en la misma transacción que el cambio de estado y que las consultas de historial respeten los permisos de cada rol.

## ADDED Requirements

### Requirement: Cancelación de reservas
El sistema SHALL permitir al solicitante cancelar sus propias reservas en estado PENDIENTE o APROBADA. El sistema SHALL permitir al administrador cancelar cualquier reserva en estado PENDIENTE o APROBADA. El sistema SHALL NOT permitir cancelar reservas en estado RECHAZADA o CANCELADA. Al cancelar una reserva inexistente el sistema SHALL retornar 404. Al cancelar con éxito el sistema SHALL retornar 200 y la reserva SHALL quedar en estado CANCELADA. El comentario o motivo de la cancelación es opcional (máximo 500 caracteres).

#### Scenario: Orden de validaciones cuando hay varios errores
- **GIVEN** una solicitud de cancelación con múltiples errores posibles
- **WHEN** se realizan las validaciones
- **THEN** el orden de validaciones SHALL ser 401, 404, 403, 409

#### Scenario: Cancelar reserva inexistente
- **WHEN** se intenta cancelar una reserva que no existe
- **THEN** el sistema SHALL retornar 404

#### Scenario: Solicitante cancela su reserva PENDIENTE con éxito
- **GIVEN** un solicitante autenticado tiene una reserva en estado PENDIENTE que le pertenece
- **WHEN** cancela su propia reserva
- **THEN** el sistema SHALL retornar 200
- **AND** la reserva SHALL quedar en estado CANCELADA
- **AND** el horario SHALL quedar liberado

#### Scenario: Solicitante cancela su reserva APROBADA con éxito
- **GIVEN** un solicitante autenticado tiene una reserva en estado APROBADA que le pertenece
- **WHEN** cancela su propia reserva
- **THEN** el sistema SHALL retornar 200
- **AND** la reserva SHALL quedar en estado CANCELADA
- **AND** el horario SHALL quedar liberado

#### Scenario: Administrador cancela cualquier reserva
- **GIVEN** existe una reserva PENDIENTE o APROBADA de cualquier usuario
- **WHEN** un administrador cancela la reserva
- **THEN** el sistema SHALL retornar 200
- **AND** la reserva SHALL quedar en estado CANCELADA
- **AND** el horario SHALL quedar liberado

#### Scenario: No se cancela reserva RECHAZADA
- **GIVEN** existe una reserva en estado RECHAZADA
- **WHEN** se intenta cancelar
- **THEN** el sistema SHALL retornar 409

#### Scenario: No se cancela reserva ya CANCELADA
- **GIVEN** existe una reserva en estado CANCELADA
- **WHEN** se intenta cancelar
- **THEN** el sistema SHALL retornar 409

#### Scenario: Solicitante intenta cancelar reserva ajena
- **WHEN** un solicitante autenticado intenta cancelar una reserva que no le pertenece
- **THEN** el sistema SHALL retornar 403

#### Scenario: Cancelar libera el horario
- **GIVEN** una reserva APROBADA ocupa un horario
- **WHEN** se cancela la reserva
- **THEN** ese horario SHALL quedar disponible para nuevas reservas

### Requirement: Historial de cambios de estado
El sistema SHALL registrar cada cambio de estado de las reservas en la tabla HistorialReserva, incluyendo la creación de la solicitud. Cada registro SHALL contener estado anterior, estado nuevo, quién realizó el cambio, cuándo y un comentario. El cambio de estado y su registro en HistorialReserva SHALL ocurrir en la misma transacción; si falla el registro, el estado NO SHALL cambiar. Al crear la solicitud, estado_anterior SHALL ser NULL. Los comentarios por defecto SHALL ser: "Solicitud creada", "Aprobada" (o el motivo si se dio), el motivo del rechazo, y "Cancelada" (o el motivo si se dio).

#### Scenario: Registro al crear solicitud
- **WHEN** se crea una solicitud de reserva
- **THEN** se SHALL registrar en HistorialReserva: estado_anterior NULL, estado_nuevo PENDIENTE, cambiado_por usuario creador, cambiado_en timestamp, comentario "Solicitud creada"

#### Scenario: Registro al aprobar
- **WHEN** un administrador aprueba una reserva
- **THEN** se SHALL registrar en HistorialReserva: estado_anterior PENDIENTE, estado_nuevo APROBADA, cambiado_por administrador, comentario "Aprobada" o el motivo si se dio

#### Scenario: Registro al rechazar
- **WHEN** un administrador rechaza una reserva
- **THEN** se SHALL registrar en HistorialReserva: estado_anterior PENDIENTE, estado_nuevo RECHAZADA, cambiado_por administrador, comentario con el motivo del rechazo

#### Scenario: Registro al cancelar
- **WHEN** se cancela una reserva
- **THEN** se SHALL registrar en HistorialReserva: estado_anterior (PENDIENTE o APROBADA), estado_nuevo CANCELADA, cambiado_por quien cancela, comentario "Cancelada" o el motivo si se dio

#### Scenario: Cambio de estado y registro en la misma transacción
- **GIVEN** una solicitud válida para cancelar una reserva
- **WHEN** ocurre un fallo al registrar en HistorialReserva
- **THEN** el estado de la reserva NO SHALL cambiar
- **AND** la operación SHALL fallar sin dejar cambios persistidos

### Requirement: Consulta de historial
El sistema SHALL permitir consultar el historial mediante GET /historial. El solicitante SHALL ver únicamente el historial de sus propias reservas. Un solicitante nunca SHALL ver historial de reservas ajenas, ni siquiera con filtros (recibe lista vacía con 200). El administrador SHALL ver todo el historial. La consulta SHALL soportar filtros opcionales reserva_id, espacio_id, estado (comparado con estado_nuevo), desde y hasta (fechas AAAA-MM-DD en hora de Bogotá, inclusivas, sobre cambiado_en). Valores inválidos SHALL retornar 422. Sin token el sistema SHALL retornar 401. Los resultados SHALL ordenarse del más reciente al más antiguo.

#### Scenario: Sin token al consultar historial
- **WHEN** se consulta GET /historial sin token
- **THEN** el sistema SHALL retornar 401

#### Scenario: Solicitante consulta su historial
- **WHEN** un solicitante consulta el historial
- **THEN** el sistema SHALL retornar únicamente los registros de sus propias reservas, ordenados del más reciente al más antiguo

#### Scenario: Solicitante con filtros no ve historial ajeno
- **GIVEN** existen reservas ajenas con historial
- **WHEN** un solicitante consulta GET /historial con filtros que podrían coincidir con reservas ajenas
- **THEN** el sistema SHALL retornar lista vacía con 200

#### Scenario: Administrador consulta todo el historial
- **WHEN** un administrador consulta el historial
- **THEN** el sistema SHALL retornar todos los registros sin restricción, ordenados del más reciente al más antiguo

#### Scenario: Filtrar por reserva_id
- **WHEN** se consulta historial filtrando por reserva_id
- **THEN** el sistema SHALL retornar solo registros relacionados con ese reserva_id

#### Scenario: Filtrar por espacio_id
- **WHEN** se consulta historial filtrando por espacio_id
- **THEN** el sistema SHALL retornar solo registros relacionados con ese espacio

#### Scenario: Filtrar por estado
- **WHEN** se consulta historial filtrando por estado
- **THEN** el sistema SHALL retornar solo registros con ese estado comparado con estado_nuevo

#### Scenario: Filtrar por rango de fechas en hora de Bogotá
- **WHEN** se consulta historial filtrando por desde y hasta con fechas AAAA-MM-DD en hora de Bogotá, inclusivas, sobre cambiado_en
- **THEN** el sistema SHALL retornar solo registros cuyo cambiado_en esté en ese rango

#### Scenario: Valores inválidos en filtros
- **WHEN** se envían valores inválidos en los filtros de GET /historial
- **THEN** el sistema SHALL retornar 422
