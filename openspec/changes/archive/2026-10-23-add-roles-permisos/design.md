# Design

## Context

Ver proposal.md - Why. Esta es la etapa E2 del plan de ingeniería, que depende de E1 (autenticación de usuarios). Se necesita implementar el control de acceso basado en roles para proteger los endpoints según lo definido en el plan (sección 1.3 actores, sección 2.3 módulo autorizacion).

## Goals / Non-Goals

**Objetivos:**
- Definir roles ADMINISTRADOR y SOLICITANTE
- Implementar matriz de permisos (GET /usuarios/yo para ambos; GET /usuarios, GET /usuarios/{id}, PATCH /usuarios/{id}/desactivar, PATCH /usuarios/{id}/activar solo para ADMINISTRADOR). Cada etapa posterior verifica los permisos de sus propios endpoints.
- Crear dependencias para autenticación con JWT desde el encabezado Authorization: Bearer <token>
- En cada petición protegida, consultar al usuario en la base de datos (no existe → 401, inactivo → 403). Un usuario desactivado por un administrador recibe 403 al intentar iniciar sesión.
- Crear verificadores de autorización por rol
- Exponer endpoints de administración de usuarios (solo ADMINISTRADOR): GET /usuarios, GET /usuarios/{id}, PATCH /usuarios/{id}/desactivar, PATCH /usuarios/{id}/activar; GET /usuarios/yo accesible a cualquier usuario autenticado (id, nombre, correo, rol, nunca hash). Activar un usuario ya activo responde 200 sin cambios.
- Impedir que un administrador se desactive a sí mismo (409)
- Ninguna respuesta de GET /usuarios, GET /usuarios/{id}, PATCH /usuarios/{id}/desactivar o PATCH /usuarios/{id}/activar incluye el hash de la contraseña
- Manejar errores con códigos HTTP correctos (401, 403, 404, 409)
- Crear script seed para primer administrador con variables de entorno ADMIN_NOMBRE, ADMIN_CORREO, ADMIN_PASSWORD (sin valores en código). El script SHALL NOT crear otro usuario ni SHALL NOT modificar el usuario existente si el correo ya existe. Si faltan variables, terminar con mensaje de error.

**No objetivos:**
- Gestión de roles dinámicos
- Permisos granulares por recurso
- Jerarquía de roles
- Cambio de roles por usuarios

## Decisions

### Decisión: Roles fijos
- **Elección**: Solo dos roles fijos: ADMINISTRADOR y SOLICITANTE. La columna rol solo acepta estos valores.
- **Justificación**: Suficiente para el alcance definido en el plan
- **Alternativas consideradas**: Roles más granulares - rechazados por complejidad innecesaria

### Decisión: Autenticación con JWT existente
- **Elección**: Reutilizar el sistema JWT de la etapa E1. El token se envía en el encabezado Authorization: Bearer <token>. Si falta o tiene formato incorrecto → 401.
- **Justificación**: Ya implementado, mantiene consistencia
- **Alternativas consideradas**: Nuevo sistema de autenticación - rechazado

### Decisión: Verificación de usuario en BD en cada petición protegida
- **Elección**: En cada petición protegida se consulta al usuario en la base de datos. Si no existe → 401; si está inactivo → 403 (aunque el token no haya vencido).
- **Justificación**: Garantiza estado actual del usuario (baja/desactivación)
- **Alternativas consideradas**: Confiar solo en claims del token - insuficiente

### Decisión: Implementación con dependencias de FastAPI
- **Elección**: Usar dependencias de FastAPI para autenticación y autorización
- **Justificación**: Integración limpia con el framework, reutilizable, testeable
- **Alternativas consideradas**: Middleware global - menos flexible por endpoint

### Decisión: Verificación de propiedad para SOLICITANTE
- **Elección**: Para acciones sobre recursos propios (según lo que aplique en etapas posteriores), además de verificar rol, verificar que el recurso pertenece al usuario. En esta etapa, los escenarios de propiedad sobre endpoints de otras etapas no se incluyen.
- **Justificación**: Requerido explícitamente cuando aplique
- **Alternativas consideradas**: Solo verificación por rol - insuficiente

### Decisión: Endpoints de administración de usuarios
- **Elección**: Solo ADMINISTRADOR puede acceder a GET /usuarios, GET /usuarios/{id}, PATCH /usuarios/{id}/desactivar, PATCH /usuarios/{id}/activar. GET /usuarios/yo accesible a cualquier usuario autenticado (devuelve id, nombre, correo, rol; nunca hash). Desactivar a sí mismo → 409. Usuario inexistente → 404. Activar un usuario ya activo responde 200 sin cambios. Ninguna respuesta de GET /usuarios, GET /usuarios/{id}, desactivar o activar incluye el hash de la contraseña.
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Permisos más amplios - rechazados por principio de menor privilegio

### Decisión: Script seed para primer administrador
- **Elección**: Crear script independiente (seed.py o similar) para inicializar el primer administrador. Nombre/correo/contraseña desde ADMIN_NOMBRE, ADMIN_CORREO, ADMIN_PASSWORD. Si el correo ya existe, el script SHALL NOT crear otro usuario ni SHALL NOT modificar el usuario existente. Si faltan variables, terminar con mensaje de error.
- **Justificación**: Requerido explícitamente, permite configurar el sistema sin depender de registro público
- **Alternativas consideradas**: Crear vía endpoint - rechazado por seguridad

### Decisión: Códigos de error
- **Elección**: Sin token/token inválido/token vencido/formato incorrecto → 401. Usuario no existe → 401. Usuario inactivo → 403. Rol insuficiente → 403. Usuario inexistente en operaciones admin → 404. Administrador intenta desactivarse a sí mismo → 409.
- **Justificación**: Requerido explícitamente en la especificación
- **Alternativas consideradas**: Códigos diferentes - no cumplen con los requisitos

## Risks / Trade-offs

- **[Seguridad] Bypass de autorización** → Mitigación: Aplicar verificaciones en todas las rutas protegidas, pruebas exhaustivas
- **[Seguridad] Token robado** → Mitigación: Expiración de 60 minutos (ya definida), validación correcta
- **[Seguridad] Escalación de privilegios** → Mitigación: Solo seed puede crear ADMINISTRADOR, rol ignorado en registro público
- **[Integridad] Verificación de propiedad** → Mitigación: Siempre verificar pertenencia del recurso para acciones de SOLICITANTE cuando aplique
- **[Operación] Seed mal usado** → Mitigación: Documentar uso, considerar protección o uso controlado
- **[Operación] Configuración incompleta** → Mitigación: El script debe fallar con mensaje claro si faltan variables de entorno
