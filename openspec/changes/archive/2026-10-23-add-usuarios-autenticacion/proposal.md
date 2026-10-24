# Proposal

## Why

Actualmente el sistema no cuenta con gestión de usuarios ni autenticación. Según el plan de ingeniería (sección 1.2, N4), se requiere autenticación, roles y permisos para controlar quién puede hacer qué en el sistema de reservas. Como primer bloque (etapa E1), es necesario establecer el registro y la autenticación de usuarios para que las funcionalidades posteriores (espacios, reservas, aprobaciones) puedan protegerse y auditarse correctamente.

## What Changes

- Añadir la capacidad de registro de usuarios con nombre, correo único y contraseña
- Añadir la capacidad de autenticación para iniciar sesión y obtener un token JWT
- Implementar almacenamiento seguro de contraseñas mediante hash
- Aplicar reglas de negocio: los usuarios inactivos no pueden iniciar sesión; el correo duplicado devuelve error con código 409

## Capabilities

### New Capabilities
- `usuarios-autenticacion`: Registro y autenticación de usuarios, incluyendo hash de contraseñas, emisión de tokens JWT y validaciones de unicidad, formato y estado de cuenta

### Modified Capabilities
- (ninguna)

## Impact

- **APIs**: Nuevos endpoints para registro de usuarios e inicio de sesión
- **Base de datos**: Nueva tabla `usuarios` con campos id, nombre, correo, hash_contraseña, rol, activo
- **Seguridad**: Implementación de hash de contraseñas, generación y validación de tokens JWT
- **Dependencias**: Biblioteca para JWT y biblioteca para hash de contraseñas (según stack tecnológico)
- **Módulos**: Módulo `usuarios` según lo definido en el plan (sección 2.3)
