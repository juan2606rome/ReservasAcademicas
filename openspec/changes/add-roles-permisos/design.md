# Design

## Context

Ver proposal.md - Why. Esta es la etapa E2 del plan de ingeniería, que depende de E1 (autenticación de usuarios). Se necesita implementar el control de acceso basado en roles para proteger los endpoints según lo definido en el plan (sección 1.3 actores, sección 2.3 módulo autorizacion).

## Goals / Non-Goals

**Objetivos:**
- Definir roles ADMINISTRADOR y SOLICITANTE
- Implementar matriz de permisos
- Crear dependencias/middleware para autenticación con JWT
- Crear verificadores de autorización por rol
- Manejar errores con códigos HTTP correctos (401, 403)
- Crear script seed para primer administrador

**No objetivos:**
- Gestión de roles dinámicos
- Permisos granulares por recurso
- Jerarquía de roles
- Cambio de roles por usuarios

## Decisions

### Decisión: Roles fijos
- **Elección**: Solo dos roles fijos: ADMINISTRADOR y SOLICITANTE
- **Justificación**: Suficiente para el alcance definido en el plan
- **Alternativas consideradas**: Roles más granulares - rechazados por complejidad innecesaria

### Decisión: Autenticación con JWT existente
- **Elección**: Reutilizar el sistema JWT de la etapa E1, validando token en cada petición protegida
- **Justificación**: Ya implementado, mantiene consistencia
- **Alternativas consideradas**: Nuevo sistema de autenticación - rechazado

### Decisión: Implementación con dependencias de FastAPI
- **Elección**: Usar dependencias de FastAPI para autenticación y autorización
- **Justificación**: Integración limpia con el framework, reutilizable, testeable
- **Alternativas consideradas**: Middleware global - menos flexible por endpoint

### Decisión: Verificación de propiedad para SOLICITANTE
- **Elección**: Para acciones sobre recursos propios (cancelar sus propias reservas), además de verificar rol, verificar que el recurso pertenece al usuario
- **Justificación**: Requerido explícitamente en la especificación
- **Alternativas consideradas**: Solo verificación por rol - insuficiente

### Decisión: Script seed para primer administrador
- **Elección**: Crear script independiente (seed.py o similar) para inicializar el primer administrador
- **Justificación**: Requerido explícitamente, permite configurar el sistema sin depender de registro público
- **Alternativas consideradas**: Crear vía endpoint - rechazado por seguridad

### Decisión: Códigos de error
- **Elección**: Sin token/token inválido/token vencido → 401; rol insuficiente o sin permiso sobre recurso ajeno → 403
- **Justificación**: Requerido explícitamente en la especificación
- **Alternativas consideradas**: Códigos diferentes - no cumplen con los requisitos

## Risks / Trade-offs

- **[Seguridad] Bypass de autorización** → Mitigación: Aplicar verificaciones en todas las rutas protegidas, pruebas exhaustivas
- **[Seguridad] Token robado** → Mitigación: Expiración de 60 minutos (ya definida), validación correcta
- **[Seguridad] Escalación de privilegios** → Mitigación: Solo seed puede crear ADMINISTRADOR, rol ignorado en registro público
- **[Integridad] Verificación de propiedad** → Mitigación: Siempre verificar pertenencia del recurso para acciones de SOLICITANTE
- **[Operación] Seed mal usado** → Mitigación: Documentar uso, considerar protección o uso controlado
