## MODIFIED Requirements

### Requirement: Creación de solicitud de reserva
El sistema SHALL permitir crear una solicitud de reserva. El usuario de la solicitud sale del token, nunca del cuerpo de la petición (si el cuerpo trae un usuario, se ignora). La solicitud SHALL crearse en estado PENDIENTE. Las fechas inicio y fin SHALL devolverse en formato ISO 8601 con zona horaria UTC. Una sola reserva SHALL durar como máximo 4 horas; si dura más, el sistema SHALL retornar 422. Un usuario no SHALL acumular, en el mismo espacio, reservas contiguas en estado PENDIENTE o APROBADA que sumen más de 4 horas seguidas; si la nueva solicitud lo provoca, el sistema SHALL retornar 409. Las reservas CANCELADAS o RECHAZADAS no cuentan para la cadena.

#### Scenario: Creación exitosa de solicitud
- **GIVEN** existe un espacio activo
- **WHEN** un usuario autenticado crea una solicitud con datos válidos
- **THEN** la solicitud se crea en estado PENDIENTE
- **AND** el sistema retorna 201 con id, espacio_id, usuario_id, inicio, fin, motivo y estado=PENDIENTE
- **AND** inicio y fin se devuelven en formato ISO 8601 con zona horaria UTC

#### Scenario: Reserva de exactamente 4 horas permitida
- **GIVEN** existe un espacio activo
- **WHEN** un usuario autenticado crea una solicitud de 08:00 a 12:00 hora de Bogotá
- **THEN** el sistema retorna 201 y la solicitud queda en estado PENDIENTE

#### Scenario: Reserva de 4 horas y 1 minuto rechazada
- **WHEN** un usuario autenticado crea una solicitud de 08:00 a 12:01 hora de Bogotá
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Reservas contiguas del mismo usuario que superan 4 horas
- **GIVEN** un usuario tiene una reserva PENDIENTE de 08:00 a 10:00 en un espacio
- **WHEN** el mismo usuario solicita 10:00 a 13:00 en ese espacio
- **THEN** el sistema retorna error con código HTTP 409

#### Scenario: Reservas contiguas del mismo usuario que suman 4 horas permitidas
- **GIVEN** un usuario tiene una reserva APROBADA de 08:00 a 10:00 en un espacio
- **WHEN** el mismo usuario solicita 10:00 a 12:00 en ese espacio
- **THEN** el sistema retorna 201

#### Scenario: Mismas horas de otro usuario permitidas
- **GIVEN** un usuario tiene una reserva PENDIENTE de 08:00 a 10:00 en un espacio
- **WHEN** otro usuario solicita 10:00 a 13:00 en ese espacio
- **THEN** el sistema retorna 201

#### Scenario: Reservas del mismo usuario separadas por un hueco permitidas
- **GIVEN** un usuario tiene una reserva PENDIENTE de 08:00 a 10:00 en un espacio
- **WHEN** el mismo usuario solicita 11:00 a 14:00 en ese espacio
- **THEN** el sistema retorna 201

#### Scenario: Reserva CANCELADA o RECHAZADA no cuenta
- **GIVEN** un usuario tiene una reserva CANCELADA o RECHAZADA de 08:00 a 10:00 en un espacio
- **WHEN** el mismo usuario solicita 10:00 a 13:00 en ese espacio
- **THEN** el sistema retorna 201
