# Proposal

## Why

Tras tener autenticación, roles/permisos y gestión de espacios, es necesario implementar el núcleo del sistema: las solicitudes de reserva. Según el plan de ingeniería (sección 1.2, N1, N2 y sección 2.1), se requiere crear solicitudes con validación de disponibilidad, prevención de solapamientos y el ciclo de vida de reservas. Esta es la funcionalidad central que resuelve el problema identificado.

## What Changes

- Crear capacidad de solicitud de reservas
- Permitir crear solicitudes con espacio_id, inicio, fin, motivo en estado PENDIENTE
- Implementar validaciones: fin > inicio, mismo día, inicio no en el pasado
- Validar existencia y estado del espacio
- Implementar prevención de solapamientos usando intervalos [inicio, fin)
- Las reservas PENDIENTE y APROBADA ocupan el espacio
- Reservas contiguas están permitidas (termina a 10:00, otra empieza a 10:00 no chocan)
- Implementar consulta de disponibilidad por espacio y fecha
- Usar transacción con BEGIN IMMEDIATE para comprobación y guardado atómicos
- Incluir prueba de dos solicitudes simultáneas

## Capabilities

### New Capabilities
- `solicitud-reservas`: Creación de solicitudes de reserva con validación de disponibilidad, prevención de solapamientos y consulta de disponibilidad

### Modified Capabilities
- (ninguna)

## Impact

- **APIs**: Endpoints para crear solicitud, consultar disponibilidad
- **Base de datos**: Tabla `reservas` con campos id, espacio_id, usuario_id, inicio, fin, motivo, estado, creada_en
- **Lógica de negocio**: Módulo de políticas para validaciones, detección de solapamientos
- **Seguridad**: Solo usuarios autenticados pueden crear solicitudes
- **Módulos**: Módulo `reservas` y `disponibilidad` según lo definido en el plan (sección 2.3)
