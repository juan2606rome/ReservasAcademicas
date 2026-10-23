# Proposal

## Why

Tras implementar las solicitudes de reserva, es necesario formalizar el proceso de decisión. Según el plan de ingeniería (sección 1.2, N5 y sección 2.1), el administrador debe aprobar o rechazar las solicitudes con trazabilidad. Esta funcionalidad completa el flujo de aprobación definido en el diagrama de estados.

## What Changes

- Crear capacidad de aprobación y rechazo de reservas
- Solo el administrador puede aprobar o rechazar
- Solo se puede actuar sobre reservas en estado PENDIENTE
- El rechazo exige un motivo
- Se debe registrar quién decidió, cuándo y el motivo de la decisión
- Al aprobar, se vuelve a validar la disponibilidad para evitar conflictos
- Validar existencia de reserva

## Capabilities

### New Capabilities
- `aprobacion-reservas`: Aprobación y rechazo de solicitudes por parte del administrador con trazabilidad y validación

### Modified Capabilities
- (ninguna)

## Impact

- **APIs**: Endpoints para aprobar y rechazar reservas, solo para administradores
- **Base de datos**: Campos en tabla reservas: decidido_por, decidido_en, motivo_decision
- **Lógica de negocio**: Validación de transiciones de estado, revalidación de disponibilidad al aprobar
- **Seguridad**: Solo rol ADMINISTRADOR puede aprobar/rechazar
- **Módulos**: Módulo `aprobacion` según lo definido en el plan (sección 2.3)
