## Context

Las reglas de reserva viven en `reservas/politicas.py`. La creación de solicitudes ocurre en `reservas/service.py` dentro de una transacción (`BEGIN IMMEDIATE`).

## Decisions

- **Dos reglas distintas, dos códigos:** una reserva individual de más de 4 horas es un dato mal formado (422). Una cadena contigua que supera 4 horas choca con el estado actual de las reservas del usuario (409).
- **Exactamente 4 horas es válido:** se rechaza solo si la duración es estrictamente mayor que 4 horas.
- **Contigüidad:** dos reservas son contiguas si `fin_a == inicio_b` en el mismo espacio y del mismo usuario. Se recorre la cadena hacia atrás y hacia adelante sumando duraciones.
- **Estados que cuentan:** solo PENDIENTE y APROBADA (los mismos que ocupan el espacio). CANCELADA y RECHAZADA se ignoran.
- **Orden de validaciones:** 401, 422 (incluye duración individual), 404, 409 (espacio inactivo, solapamiento, cadena > 4 h).
- **Dónde va:** la lógica pura (sumar duraciones) en `politicas.py`; la consulta de reservas del usuario en el repositorio; el servicio solo la invoca dentro de la misma transacción.

## Risks / Trade-offs

- Una cadena larga requiere consultar reservas vecinas; se acepta por el bajo volumen del sistema.
- Cancelar una reserva intermedia rompe la cadena, lo cual es el comportamiento deseado.
