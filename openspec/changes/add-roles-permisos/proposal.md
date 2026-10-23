# Proposal

## Why

Tras establecer el registro y la autenticación de usuarios (etapa E1), es necesario implementar el control de acceso basado en roles. Según el plan de ingeniería (sección 1.2, N4 y sección 2.3), se requieren roles y permisos para garantizar que solo usuarios autorizados puedan realizar ciertas acciones. Esta funcionalidad es fundamental para proteger la gestión de espacios, la aprobación de reservas y el acceso a información sensible.

## What Changes

- Definir los roles del sistema: ADMINISTRADOR y SOLICITANTE
- Crear matriz de permisos que especifique qué puede hacer cada rol
- Implementar verificación de autenticación (token JWT)
- Implementar verificación de autorización por rol
- Establecer manejo de errores de autorización con códigos HTTP correctos
- Crear mecanismo para inicializar el primer administrador mediante script seed

## Capabilities

### New Capabilities
- `roles-permisos`: Control de acceso basado en roles con matriz de permisos, validación de tokens JWT y manejo de errores de autorización

### Modified Capabilities
- (ninguna)

## Impact

- **APIs**: Todos los endpoints protegidos deberán validar token y rol
- **Seguridad**: Middleware/dependencias para autenticación y autorización
- **Base de datos**: Campo rol ya existe en tabla usuarios (se valida su uso)
- **Scripts**: Script de inicialización (seed) para crear primer administrador
- **Módulos**: Módulo `autorizacion` según lo definido en el plan (sección 2.3)
