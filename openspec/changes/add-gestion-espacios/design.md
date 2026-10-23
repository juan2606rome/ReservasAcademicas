# Design

## Context

Ver proposal.md - Why. Esta es la etapa E3 del plan de ingeniería, que depende de E1 (autenticación) y E2 (roles/permisos). Se necesita gestionar el catálogo de espacios académicos como base para las reservas (sección 2.3 módulo espacios, sección 3.3 entidad Espacio).

## Goals / Non-Goals

**Objetivos:**
- Implementar CRUD de espacios (crear, listar, consultar, editar, desactivar)
- Restringir operaciones a rol ADMINISTRADOR
- Validar tipo, nombre único, capacidad
- Implementar desactivación en lugar de eliminación
- Asegurar que espacios desactivados no aparezcan en listados normales

**No objetivos:**
- Búsqueda avanzada o filtros complejos
- Gestión de equipamiento
- Disponibilidad de espacios (etapa posterior)
- Reservas

## Decisions

### Decisión: Solo administrador gestiona espacios
- **Elección**: Todas las operaciones de creación, edición, desactivación requieren rol ADMINISTRADOR. Listado/consulta puede requerir autenticación según diseño, pero gestión completa solo para administrador
- **Justificación**: Requerido explícitamente en la especificación
- **Alternativas consideradas**: Permitir a solicitantes consultar - se permite consultar/listar pero solo admin gestiona

### Decisión: Desactivación en lugar de eliminación
- **Elección**: Usar campo `activo` booleano, desactivar en lugar de DELETE
- **Justificación**: Preservar integridad referencial con reservas futuras, mantener historial (sección 3.3)
- **Alternativas consideradas**: Eliminación física - rechazada

### Decisión: Tipos fijos
- **Elección**: Enum o validación para LABORATORIO, AUDITORIO, SALA_COMPUTO
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Tipos libres - rechazados

### Decisión: Nombre único
- **Elección**: Restricción UNIQUE en base de datos y validación en aplicación. Error 409 en caso de duplicado
- **Justificación**: Consistente con manejo de duplicados en usuarios
- **Alternativas consideradas**: Solo validación en aplicación - insuficiente

### Decisión: Validación de capacidad
- **Elección**: Debe ser entero mayor que 0. Error 422 si inválido
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Permitir 0 o negativos - rechazados

### Decisión: Listados filtran inactivos
- **Elección**: Por defecto, listados normales solo muestran espacios activos. Espacios inactivos no deben aparecer
- **Justificación**: Requerido explícitamente, evita que se usen para reservas
- **Alternativas consideradas**: Mostrar todos con indicador - no cumple con el requisito

## Risks / Trade-offs

- **[Integridad] Reservas a espacios inactivos** → Mitigación: Espacios inactivos no aparecen en listados; validación adicional en módulo de reservas
- **[Integridad] Nombre duplicado** → Mitigación: UNIQUE constraint + validación, retornar 409
- **[Validación] Capacidad inválida** → Mitigación: Validación estricta, retornar 422
- **[Autorización] Acceso no autorizado** → Mitigación: Solo ADMINISTRADOR puede crear/editar/desactivar, retornar 403
- **[Datos] Eliminación accidental** → Mitigación: Solo desactivación, nunca DELETE
