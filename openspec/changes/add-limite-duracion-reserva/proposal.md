## Why

La institución definió una nueva regla de negocio: ningún usuario podrá reservar un espacio académico durante más de cuatro horas consecutivas. Sin esta regla, un usuario puede acaparar un espacio durante toda la jornada.

## What Changes

- Una sola reserva no puede durar más de 4 horas (exactamente 4 horas es válido). Si excede: 422.
- Un usuario no puede encadenar reservas contiguas en el mismo espacio, en estado PENDIENTE o APROBADA, que sumen más de 4 horas seguidas. Si la cadena excede: 409.
- Las reservas CANCELADAS o RECHAZADAS no cuentan en la cadena.
- La regla se implementa en `reservas/politicas.py`.

## Impacto

- **Requisito afectado:** "Creación de solicitud de reserva" (capacidad `solicitud-reservas`), modificado con `## MODIFIED Requirements`.
- **Módulos afectados:** `reservas/politicas.py` (regla), `reservas/service.py` (llamar la regla en el orden de validaciones) y `reservas/repository.py` (consultar reservas contiguas del mismo usuario).
- **Plan de ingeniería:** no cambia. El plan ya concentraba las reglas de reserva en `politicas`.
- **Riesgo:** romper pruebas existentes; por eso la última tarea ejecuta toda la suite.

## Capabilities

### Modified Capabilities
- `solicitud-reservas`: se modifica el requisito de creación de solicitud con el límite de duración.
