# gestion-espacios Specification

## Purpose
Esta capacidad proporciona la gestión del catálogo de espacios académicos para el sistema de reservas. Permite crear, listar, consultar, editar, desactivar y reactivar espacios con validaciones adecuadas, garantizando la integridad del catálogo y el control de acceso por rol.

## Requirements

### Requirement: Tipos de espacio
El sistema SHALL soportar únicamente tres tipos de espacio: LABORATORIO, AUDITORIO y SALA_COMPUTO.

#### Scenario: Tipos válidos
- **WHEN** se crea o edita un espacio con tipo LABORATORIO, AUDITORIO o SALA_COMPUTO
- **THEN** el sistema acepta la operación

#### Scenario: Tipo inválido
- **WHEN** un administrador intenta crear o editar un espacio con un tipo inválido
- **THEN** el sistema retorna error con código HTTP 422

### Requirement: Gestión de espacios por rol
El sistema SHALL permitir crear, editar, activar y desactivar espacios únicamente a usuarios con rol ADMINISTRADOR. El sistema SHALL permitir listar y consultar espacios a cualquier usuario autenticado.

#### Scenario: Administrador crea espacio
- **WHEN** un usuario con rol ADMINISTRADOR crea un espacio
- **THEN** el sistema permite la operación

#### Scenario: Solicitante intenta crear espacio
- **WHEN** un usuario con rol SOLICITANTE intenta crear un espacio
- **THEN** el sistema rechaza la operación con código HTTP 403

#### Scenario: Solicitante intenta editar espacio
- **WHEN** un usuario con rol SOLICITANTE intenta editar un espacio
- **THEN** el sistema rechaza la operación con código HTTP 403

#### Scenario: Solicitante intenta desactivar espacio
- **WHEN** un usuario con rol SOLICITANTE intenta desactivar un espacio
- **THEN** el sistema rechaza la operación con código HTTP 403

#### Scenario: Solicitante intenta activar espacio
- **WHEN** un usuario con rol SOLICITANTE intenta activar un espacio
- **THEN** el sistema rechaza la operación con código HTTP 403

#### Scenario: Usuario autenticado lista espacios
- **WHEN** cualquier usuario autenticado solicita listar espacios
- **THEN** el sistema permite la operación

#### Scenario: Usuario autenticado consulta espacio
- **WHEN** cualquier usuario autenticado consulta un espacio específico
- **THEN** el sistema permite la operación

### Requirement: Nombre único de espacio
El sistema SHALL garantizar que el nombre de cada espacio sea único sin distinguir mayúsculas ni espacios al inicio o al final. Si se intenta crear un espacio, o editar un espacio asignándole el nombre de otro espacio existente según esta regla, el sistema SHALL retornar error con código HTTP 409. Al editar un espacio conservando su propio nombre, incluido un cambio que solo altere mayúsculas o minúsculas, el sistema SHALL aceptar la operación.

#### Scenario: Creación con nombre duplicado
- **WHEN** un administrador intenta crear un espacio con un nombre que ya existe ignorando mayúsculas y espacios al inicio o al final
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se crea el espacio

#### Scenario: Edición con nombre duplicado
- **WHEN** un administrador intenta editar un espacio cambiando su nombre por uno ya existente ignorando mayúsculas y espacios al inicio o al final
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se actualiza el espacio

#### Scenario: Edición conservando el propio nombre
- **GIVEN** existe un espacio con nombre "Laboratorio A"
- **WHEN** un administrador edita ese mismo espacio sin cambiar su nombre, o cambiando solo las mayúsculas o minúsculas de ese nombre
- **THEN** el sistema acepta la operación con código HTTP 200
- **AND** el espacio no se considera duplicado de sí mismo

#### Scenario: Nombre vacío
- **WHEN** un administrador intenta crear o editar un espacio con nombre vacío o solo espacios
- **THEN** el sistema retorna error con código HTTP 422

### Requirement: Validación de capacidad
El sistema SHALL validar que la capacidad sea un número entero mayor que 0. Si no cumple esta condición, el sistema SHALL retornar error con código HTTP 422.

#### Scenario: Capacidad inválida
- **WHEN** un administrador intenta crear o editar un espacio con capacidad 0, negativa o no entera
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Capacidad válida
- **WHEN** un administrador crea o edita un espacio con capacidad entera mayor que 0
- **THEN** el sistema acepta la operación

### Requirement: Desactivación y activación de espacios
El sistema SHALL permitir desactivar espacios en lugar de eliminarlos mediante PATCH /espacios/{id}/desactivar, y SHALL permitir reactivarlos mediante PATCH /espacios/{id}/activar, ambas operaciones únicamente para usuarios con rol ADMINISTRADOR. El sistema SHALL nunca eliminar espacios mediante DELETE.

#### Scenario: Desactivar espacio
- **WHEN** un administrador desactiva un espacio
- **THEN** el sistema marca el espacio como inactivo
- **AND** el sistema retorna código HTTP 200
- **AND** el espacio no se elimina de la base de datos

#### Scenario: Activar espacio
- **WHEN** un administrador activa un espacio
- **THEN** el sistema marca el espacio como activo
- **AND** el sistema retorna código HTTP 200
- **AND** el espacio no se elimina de la base de datos

#### Scenario: Desactivar espacio con reservas futuras PENDIENTE o APROBADA
- **GIVEN** existe un espacio con reservas futuras en estado PENDIENTE o APROBADA
- **WHEN** un administrador desactiva el espacio
- **THEN** el sistema marca el espacio como inactivo
- **AND** las reservas futuras PENDIENTE o APROBADA no se modifican
- **AND** solo se impiden reservas nuevas para ese espacio

### Requirement: Listados y consulta de espacios
El sistema SHALL mostrar por defecto solo espacios activos en los listados. El administrador SHALL poder usar el parámetro ?incluir_inactivos=true para incluir espacios inactivos en el listado. Al consultar un espacio por id, si el espacio está inactivo, el administrador SHALL recibir código HTTP 200 y el solicitante SHALL recibir código HTTP 404.

#### Scenario: Listar espacios por defecto
- **WHEN** cualquier usuario autenticado solicita listar espacios sin el parámetro incluir_inactivos
- **THEN** el sistema retorna únicamente los espacios activos con código HTTP 200

#### Scenario: Listar espacios incluyendo inactivos
- **WHEN** un administrador solicita listar espacios con ?incluir_inactivos=true
- **THEN** el sistema retorna todos los espacios incluyendo inactivos con código HTTP 200

#### Scenario: Consultar espacio activo
- **WHEN** cualquier usuario autenticado consulta un espacio activo por id
- **THEN** el sistema retorna la información del espacio con código HTTP 200

#### Scenario: Consultar espacio inactivo como administrador
- **WHEN** un administrador consulta un espacio inactivo por id
- **THEN** el sistema retorna la información del espacio con código HTTP 200

#### Scenario: Consultar espacio inactivo como solicitante
- **WHEN** un solicitante consulta un espacio inactivo por id
- **THEN** el sistema retorna error con código HTTP 404

### Requirement: Espacio inexistente
El sistema SHALL retornar código HTTP 404 al consultar, editar, activar o desactivar un espacio que no existe.

#### Scenario: Consultar espacio inexistente
- **WHEN** un usuario autenticado consulta un espacio que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Editar espacio inexistente
- **WHEN** un administrador intenta editar un espacio que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Desactivar espacio inexistente
- **WHEN** un administrador intenta desactivar un espacio que no existe
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Activar espacio inexistente
- **WHEN** un administrador intenta activar un espacio que no existe
- **THEN** el sistema retorna error con código HTTP 404

### Requirement: Operaciones CRUD de espacios
El sistema SHALL exponer los endpoints POST /espacios, GET /espacios, GET /espacios/{id}, PUT /espacios/{id}, PATCH /espacios/{id}/desactivar y PATCH /espacios/{id}/activar. El sistema SHALL retornar código HTTP 201 al crear un espacio y código HTTP 200 en las demás operaciones.

#### Scenario: Crear espacio
- **WHEN** un administrador crea un espacio con datos válidos
- **THEN** el sistema crea el espacio y retorna código HTTP 201

#### Scenario: Listar espacios
- **WHEN** cualquier usuario autenticado solicita listar espacios
- **THEN** el sistema retorna la lista con código HTTP 200

#### Scenario: Consultar espacio
- **WHEN** cualquier usuario autenticado consulta un espacio específico
- **THEN** el sistema retorna la información del espacio con código HTTP 200

#### Scenario: Editar espacio
- **WHEN** un administrador edita los datos de un espacio con datos válidos
- **THEN** el sistema actualiza el espacio y retorna código HTTP 200
