# Proposal

## Why

Tras implementar el flujo completo de solicitudes y aprobación, es necesario completar el ciclo de vida con cancelación e historial. Según el plan de ingeniería (sección 2.1 diagrama de estados, sección 1.2 N6), se requiere poder cancelar reservas y mantener trazabilidad completa de todos los cambios de estado. Esto permite auditar quién decidió qué y cuándo.

## What Changes

- Permitir al solicitante cancelar sus propias reservas PENDIENTE o APROBADA
- Permitir al administrador cancelar cualquier reserva PENDIENTE o APROBADA
- No permitir cancelar reservas RECHAZADA o CANCELADA
- Cancelar libera el horario (ya que CANCELADA no ocupa espacio)
- Registrar cada cambio de estado en HistorialReserva, incluida la creación
- Historial debe guardar estado anterior, estado nuevo, quién, cuándo, comentario
- Consulta de historial con permisos: solicitante ve lo suyo, administrador ve todo
- Filtros por espacio, estado y fecha

## Capabilities

### New Capabilities
- `cancelacion-historial`: Cancelación de reservas y registro completo de historial con consultas filtradas

### Modified Capabilities
- (ninguna)

## Impact

- **APIs**: Endpoint para cancelar, endpoint para consultar historial con filtros
- **Base de datos**: Tabla `HistorialReserva` con campos id, reserva_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario
- **Lógica de negocio**: Validaciones de cancelación, registro automático de historial
- **Seguridad**: Verificación de propiedad para solicitantes
- **Módulos**: Módulo `cancelacion`/`historial` según lo definido en el plan (sección 2.3)
