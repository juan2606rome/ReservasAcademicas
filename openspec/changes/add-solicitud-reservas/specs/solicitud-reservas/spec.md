# Spec Delta

## Purpose

Esta capacidad proporciona la creación de solicitudes de reserva y la consulta de disponibilidad para el sistema de reservas de espacios académicos. Implementa validaciones de fechas, prevención de solapamientos con transacciones atómicas, y garantiza que las reservas PENDIENTE y APROBADA ocupen el espacio correctamente.

## ADDED Requirements

### Requirement: Creación de solicitud de reserva
El sistema SHALL permitir crear una solicitud de reserva. El usuario de la solicitud sale del token, nunca del cuerpo de la petición (si el cuerpo trae un usuario, se ignora). La solicitud SHALL crearse en estado PENDIENTE. Las fechas inicio y fin SHALL devolverse en formato ISO 8601 con zona horaria UTC.

#### Scenario: Creación exitosa de solicitud
- **GIVEN** existe un espacio activo
- **WHEN** un usuario autenticado crea una solicitud con datos válidos
- **THEN** la solicitud se crea en estado PENDIENTE
- **AND** el sistema retorna 201 con id, espacio_id, usuario_id, inicio, fin, motivo y estado=PENDIENTE
- **AND** inicio y fin se devuelven en formato ISO 8601 con zona horaria UTC

### Requirement: Validaciones de fecha y hora
El sistema SHALL validar que fin > inicio. Los campos inicio y fin llegan en formato ISO 8601 con zona horaria; si no traen zona horaria, el sistema SHALL retornar 422. Internamente se guardan en UTC. La regla "mismo día" y la consulta de disponibilidad por fecha se evalúan en hora de Bogotá (America/Bogota, UTC-5). El sistema SHALL validar que inicio no esté en el pasado. En caso de violación, SHALL retornar error con código HTTP 422.

#### Scenario: Fin menor o igual a inicio
- **WHEN** se intenta crear una reserva con fin <= inicio
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Reserva en días diferentes
- **WHEN** se intenta crear una reserva que comienza y termina en días diferentes según la hora de Bogotá (America/Bogota, UTC-5)
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Inicio en el pasado
- **WHEN** se intenta crear una reserva con fecha/hora de inicio en el pasado según la hora de Bogotá (America/Bogota, UTC-5)
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Fechas sin zona horaria
- **WHEN** se intenta crear una reserva con inicio o fin en formato ISO 8601 sin zona horaria
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Reserva válida de 19:00 a 21:00 hora de Bogotá
- **GIVEN** existe un espacio activo
- **WHEN** un usuario autenticado crea una solicitud para el mismo día con inicio 19:00 y fin 21:00 hora de Bogotá (America/Bogota, UTC-5)
- **THEN** la solicitud se crea exitosamente en estado PENDIENTE

### Requirement: Validación de motivo
El sistema SHALL validar que el motivo sea obligatorio, no vacío y de máximo 500 caracteres. Si faltan campos o el motivo es inválido, SHALL retornar error con código HTTP 422.

#### Scenario: Motivo vacío
- **WHEN** se intenta crear una reserva con motivo vacío
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Motivo excede 500 caracteres
- **WHEN** se intenta crear una reserva con motivo de más de 500 caracteres
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Motivo faltante
- **WHEN** se intenta crear una reserva sin motivo
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Campos faltantes
- **WHEN** se intenta crear una reserva sin espacio_id, inicio o fin
- **THEN** el sistema retorna error con código HTTP 422

### Requirement: Validación de espacio
El sistema SHALL validar que el espacio exista y esté activo. Si el espacio no existe, SHALL retornar error con código HTTP 404. Si el espacio está inactivo, SHALL retornar error con código HTTP 409.

#### Scenario: Espacio inexistente
- **WHEN** se intenta crear una reserva para un espacio_id que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Espacio inactivo
- **WHEN** se intenta crear una reserva para un espacio inactivo
- **THEN** el sistema retorna error con código HTTP 409

### Requirement: Prevención de solapamientos
El sistema SHALL tratar los intervalos como [inicio, fin) (semiabiertos). Las reservas en estado PENDIENTE o APROBADA SHALL ocupar el espacio. Dos reservas SHALL solaparse si a1 < b2 y b1 < a2. El solapamiento se compara solo con reservas del MISMO espacio. Las reservas contiguas (una termina cuando otra empieza) SHALL estar permitidas. Una solicitud PENDIENTE contra otra PENDIENTE se solapa. En caso de solapamiento, SHALL retornar error con código HTTP 409.

#### Scenario: Solapamiento detectado
- **GIVEN** existe una reserva PENDIENTE o APROBADA para un espacio
- **WHEN** se intenta crear otra reserva que se solapa con ella en el MISMO espacio
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se crea la nueva reserva

#### Scenario: Reservas contiguas permitidas
- **GIVEN** existe una reserva que termina a las 10:00
- **WHEN** se intenta crear otra reserva que empieza a las 10:00 en el mismo espacio
- **THEN** el sistema permite la creación
- **AND** ambas reservas son válidas

#### Scenario: Reserva RECHAZADA o CANCELADA no ocupa espacio
- **GIVEN** existe una reserva RECHAZADA o CANCELADA para un espacio
- **WHEN** se intenta crear otra reserva en el mismo horario en el MISMO espacio
- **THEN** el sistema permite la creación (no hay solapamiento)

#### Scenario: Mismo horario en otro espacio es permitido
- **GIVEN** existe una reserva PENDIENTE o APROBADA para un espacio A
- **WHEN** se intenta crear otra reserva en el mismo horario para un espacio B diferente
- **THEN** el sistema permite la creación
- **AND** ambas reservas son válidas

#### Scenario: Una solicitud PENDIENTE contra otra PENDIENTE se solapa
- **GIVEN** existe una solicitud PENDIENTE para un espacio
- **WHEN** se intenta crear otra solicitud PENDIENTE que se solapa con ella en el MISMO espacio
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se crea la nueva solicitud

### Requirement: Transacción atómica para prevención de solapamientos
El sistema SHALL realizar la comprobación de disponibilidad y el guardado de la reserva en una misma transacción iniciada con BEGIN IMMEDIATE. Esto SHALL prevenir condiciones de carrera entre solicitudes simultáneas.

#### Scenario: Dos solicitudes simultáneas
- **GIVEN** dos usuarios intentan crear reservas solapadas para el mismo espacio al mismo tiempo
- **WHEN** ambas solicitudes se procesan concurrentemente
- **THEN** solo una de las reservas se crea exitosamente
- **AND** la otra retorna error con código HTTP 409 por solapamiento

### Requirement: Consulta de disponibilidad
El sistema SHALL permitir consultar la disponibilidad de un espacio por fecha mediante GET /reservas/disponibilidad?espacio_id=...&fecha=AAAA-MM-DD, para cualquier usuario autenticado. La fecha se evalúa en hora de Bogotá (America/Bogota, UTC-5). El sistema SHALL mostrar las franjas ocupadas ordenadas por inicio, cada una con inicio, fin y estado, sin datos de usuarios. Las reservas en estado PENDIENTE o APROBADA SHALL ocupar el espacio. Las reservas RECHAZADA o CANCELADA no aparecen como ocupadas. Sin reservas, SHALL devolver lista vacía con 200. Espacio inexistente: 404. Fecha inválida o faltante: 422. Las fechas inicio y fin SHALL devolverse en formato ISO 8601 con zona horaria UTC.

#### Scenario: Consultar disponibilidad con franjas ocupadas
- **GIVEN** existen reservas PENDIENTE o APROBADA para un espacio en una fecha
- **WHEN** se consulta GET /reservas/disponibilidad?espacio_id=...&fecha=AAAA-MM-DD
- **THEN** el sistema retorna las franjas ocupadas ordenadas por inicio, cada una con inicio, fin y estado
- **AND** cada franja devuelve inicio y fin en formato ISO 8601 con zona horaria UTC
- **AND** las reservas RECHAZADA o CANCELADA no aparecen como ocupadas
- **AND** no se incluyen datos de usuarios

#### Scenario: Sin reservas devuelve lista vacía
- **GIVEN** no existen reservas PENDIENTE o APROBADA para un espacio en una fecha
- **WHEN** se consulta GET /reservas/disponibilidad?espacio_id=...&fecha=AAAA-MM-DD
- **THEN** el sistema retorna lista vacía con código HTTP 200

#### Scenario: Espacio inexistente en consulta de disponibilidad
- **WHEN** se consulta la disponibilidad para un espacio_id que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Fecha inválida o faltante en consulta de disponibilidad
- **WHEN** se consulta la disponibilidad sin fecha o con fecha inválida
- **THEN** el sistema retorna error con código HTTP 422

### Requirement: Consulta de reservas
El sistema SHALL exponer GET /reservas. El solicitante ve solo las suyas, el administrador todas. Filtros opcionales: estado y espacio_id. Más recientes primero. Las fechas inicio y fin SHALL devolverse en formato ISO 8601 con zona horaria UTC. El sistema SHALL exponer GET /reservas/{id}. La ve su dueño o un administrador; si es ajena siendo solicitante, SHALL retornar 403; si no existe, SHALL retornar 404. Las fechas inicio y fin SHALL devolverse en formato ISO 8601 con zona horaria UTC. Filtros inválidos de GET /reservas (estado distinto de PENDIENTE, APROBADA, RECHAZADA o CANCELADA, o espacio_id no numérico): 422.

#### Scenario: Solicitante ve solo sus reservas
- **GIVEN** un solicitante autenticado con reservas propias y existen reservas de otros usuarios
- **WHEN** consulta GET /reservas
- **THEN** el sistema retorna solo las reservas del solicitante
- **AND** las retorna más recientes primero

#### Scenario: Administrador ve todas las reservas
- **GIVEN** un administrador autenticado
- **WHEN** consulta GET /reservas
- **THEN** el sistema retorna todas las reservas
- **AND** las retorna más recientes primero

#### Scenario: Filtrar reservas por estado
- **GIVEN** un usuario autenticado con reservas en distintos estados
- **WHEN** consulta GET /reservas?estado=PENDIENTE
- **THEN** el sistema retorna solo las reservas que coincidan con el filtro según el rol del usuario

#### Scenario: Filtrar reservas por espacio_id
- **GIVEN** un usuario autenticado
- **WHEN** consulta GET /reservas?espacio_id=...
- **THEN** el sistema retorna solo las reservas que coincidan con el filtro según el rol del usuario

#### Scenario: Consultar reserva propia por id
- **GIVEN** un solicitante autenticado dueño de una reserva
- **WHEN** consulta GET /reservas/{id}
- **THEN** el sistema retorna la reserva
- **AND** inicio y fin se devuelven en formato ISO 8601 con zona horaria UTC

#### Scenario: Administrador consulta cualquier reserva por id
- **GIVEN** un administrador autenticado
- **WHEN** consulta GET /reservas/{id} de cualquier reserva
- **THEN** el sistema retorna la reserva
- **AND** inicio y fin se devuelven en formato ISO 8601 con zona horaria UTC

#### Scenario: Solicitante consulta reserva ajena
- **GIVEN** un solicitante autenticado
- **WHEN** consulta GET /reservas/{id} de una reserva que no le pertenece
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: Consultar reserva inexistente
- **WHEN** se consulta GET /reservas/{id} de una reserva que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Filtros inválidos de GET /reservas
- **WHEN** se consulta GET /reservas con estado distinto de PENDIENTE, APROBADA, RECHAZADA o CANCELADA
- **OR** se consulta GET /reservas con espacio_id no numérico
- **THEN** el sistema retorna error con código HTTP 422

### Requirement: Orden de validaciones
Cuando hay varios errores, el orden de validaciones SHALL ser: 401, 422, 404, 409.

#### Scenario: Petición sin token y con datos inválidos
- **WHEN** se realiza una petición sin token y con datos inválidos (fechas sin zona horaria o motivo inválido, entre otros)
- **THEN** el sistema retorna error con código HTTP 401 (no 422)

#### Scenario: Petición con fechas inválidas y espacio_id inexistente
- **WHEN** se realiza una petición con fechas inválidas (por ejemplo fin <= inicio) y espacio_id inexistente
- **THEN** el sistema retorna error con código HTTP 422 (no 404)

#### Scenario: Petición válida sobre espacio inexistente
- **WHEN** se realiza una petición válida (autenticada, datos válidos, fechas con zona horaria, motivo válido) sobre un espacio_id inexistente
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Petición válida sobre espacio inactivo que además se solaparía
- **WHEN** se realiza una petición válida (autenticada, datos válidos) sobre un espacio inactivo y además la reserva se solaparía con una reserva PENDIENTE o APROBADA
- **THEN** el sistema retorna error con código HTTP 409
