# Proposal

## Why

Tras tener autenticación (E1) y control de acceso por roles (E2), es necesario gestionar el catálogo de espacios académicos. Según el plan de ingeniería (sección 1.2, N1 y sección 2.3), se requiere crear, consultar, editar y desactivar espacios para que los solicitantes puedan realizar reservas sobre ellos. Esta funcionalidad es fundamental para el núcleo del sistema.

## What Changes

- Crear capacidad de gestión de espacios académicos
- Permitir crear, listar, consultar, editar y desactivar espacios (solo administrador)
- Soportar tipos de espacio: LABORATORIO, AUDITORIO y SALA_COMPUTO
- Garantizar nombre único con error 409
- Validar capacidad entera mayor que 0 con error 422
- Implementar desactivación (no eliminación) de espacios
- Los espacios desactivados no aparecen en listados normales ni aceptan reservas

## Capabilities

### New Capabilities
- `gestion-espacios`: Gestión de espacios académicos con CRUD, tipos, validaciones, unicidad de nombre y desactivación

### Modified Capabilities
- (ninguna)

## Impact

- **APIs**: Endpoints para CRUD de espacios, solo accesibles por administradores
- **Base de datos**: Tabla `espacios` con campos id, nombre, tipo, capacidad, activo
- **Seguridad**: Endpoints protegidos con rol ADMINISTRADOR
- **Módulos**: Módulo `espacios` según lo definido en el plan (sección 2.3)
- **Integración**: Los espacios desactivados no aceptarán reservas en etapas futuras
