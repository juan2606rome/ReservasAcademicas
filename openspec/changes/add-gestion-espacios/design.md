# Design

## Context

Ver proposal.md - Why. Esta es la etapa E3 del plan de ingeniería, que depende de E1 (autenticación) y E2 (roles/permisos). Se necesita gestionar el catálogo de espacios académicos como base para las reservas (sección 2.3 módulo espacios, sección 3.3 entidad Espacio).

## Goals / Non-Goals

**Objetivos:**
- Implementar CRUD de espacios (crear, listar, consultar, editar, desactivar, activar)
- Restringir crear, editar, activar y desactivar a rol ADMINISTRADOR
- Permitir listar y consultar a cualquier usuario autenticado
- Validar tipo, nombre único sin distinguir mayúsculas ni espacios al inicio o al final, capacidad entera mayor que 0
- Implementar desactivación y activación en lugar de eliminación
- Listados por defecto solo muestran espacios activos; administrador puede usar ?incluir_inactivos=true
- Consultar por id un espacio inactivo: administrador recibe 200, solicitante recibe 404
- Retornar 404 al consultar, editar, activar o desactivar un espacio inexistente
- Retornar 422 para tipo inválido y para nombre vacío
- Desactivar espacio con reservas futuras PENDIENTE o APROBADA está permitido (no se modifican esas reservas, solo se impiden reservas nuevas)

**No objetivos:**
- Búsqueda avanzada o filtros complejos
- Gestión de equipamiento
- Disponibilidad de espacios (etapa posterior)
- Reservas

## Decisions

### Decisión: Control de acceso por operación
- **Elección**: Crear, editar, activar y desactivar requieren rol ADMINISTRADOR (403 para SOLICITANTE). Listar y consultar pueden hacerlo cualquier usuario autenticado.
- **Justificación**: Requerido explícitamente en la especificación
- **Alternativas consideradas**: Todas las operaciones solo para administrador - rechazada

### Decisión: Desactivación y activación en lugar de eliminación
- **Elección**: Usar campo `activo` booleano, desactivar mediante PATCH /espacios/{id}/desactivar y activar mediante PATCH /espacios/{id}/activar. Nunca usar DELETE.
- **Justificación**: Preservar integridad referencial con reservas futuras, mantener historial (sección 3.3)
- **Alternativas consideradas**: Eliminación física - rechazada

### Decisión: Tipos fijos
- **Elección**: Enum o validación para LABORATORIO, AUDITORIO, SALA_COMPUTO. Tipo inválido retorna 422.
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Tipos libres - rechazados

### Decisión: Nombre único
- **Elección**: Restricción a nivel de aplicación y base de datos considerando nombre normalizado (sin mayúsculas ni espacios al inicio o al final). Error 409 en caso de duplicado. Nombre vacío o solo espacios retorna 422.
- **Justificación**: Consistente con requerimientos
- **Alternativas consideradas**: Comparación exacta - rechazada

### Decisión: Validación de capacidad
- **Elección**: Debe ser entero mayor que 0. Error 422 si inválido
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Permitir 0 o negativos - rechazados

### Decisión: Listados y consulta por id
- **Elección**: Por defecto, listados solo muestran espacios activos. Administrador puede usar ?incluir_inactivos=true. Al consultar por id un espacio inactivo, administrador recibe 200, solicitante recibe 404.
- **Justificación**: Requerido explícitamente
- **Alternativas consideradas**: Mostrar todos en listado normal - no cumple con el requisito

### Decisión: Espacios inexistentes
- **Elección**: Consultar, editar, activar o desactivar un espacio inexistente retorna 404.
- **Justificación**: Requerido explícitamente

### Decisión: Desactivación con reservas futuras
- **Elección**: Desactivar un espacio con reservas futuras PENDIENTE o APROBADA está permitido. Esas reservas no se modifican y solo se impiden reservas nuevas.
- **Justificación**: Requerido explícitamente

### Decisión: Códigos de éxito
- **Elección**: 201 al crear (POST /espacios), 200 en las demás operaciones (GET /espacios, GET /espacios/{id}, PUT /espacios/{id}, PATCH /espacios/{id}/desactivar, PATCH /espacios/{id}/activar).
- **Justificación**: Requerido explícitamente

## Risks / Trade-offs

- **[Integridad] Reservas a espacios inactivos** → Mitigación: Espacios inactivos no aparecen en listados normales; validación en módulo de reservas para impedir reservas nuevas. Desactivación con reservas futuras PENDIENTE o APROBADA está permitida sin modificarlas.
- **[Integridad] Nombre duplicado** → Mitigación: Validación con normalización (sin mayúsculas ni espacios al inicio o al final) + constraint, retornar 409
- **[Validación] Tipo inválido o nombre vacío** → Mitigación: Validación estricta, retornar 422
- **[Validación] Capacidad inválida** → Mitigación: Validación estricta, retornar 422
- **[Autorización] Acceso no autorizado** → Mitigación: Crear, editar, activar y desactivar solo ADMINISTRADOR (403 para SOLICITANTE); listar y consultar para cualquier usuario autenticado
- **[Datos] Eliminación accidental** → Mitigación: Solo desactivación/activación, nunca DELETE
- **[Consulta] Espacio inactivo** → Mitigación: Administrador puede consultarlo (200), solicitante recibe 404
