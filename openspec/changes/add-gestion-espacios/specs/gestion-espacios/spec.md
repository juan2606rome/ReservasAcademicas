# Spec Delta

## Purpose

Esta capacidad proporciona la gestión del catálogo de espacios académicos para el sistema de reservas. Permite crear, listar, consultar, editar y desactivar espacios con validaciones adecuadas, garantizando la integridad del catálogo y el control de acceso por rol.

## ADDED Requirements

### Requirement: Tipos de espacio
The system SHALL soportar únicamente tres tipos de espacio: LABORATORIO, AUDITORIO y SALA_COMPUTO.

#### Scenario: Tipos válidos
- **WHEN** se crea o edita un espacio
- **THEN** el sistema acepta únicamente LABORATORIO, AUDITORIO o SALA_COMPUTO

### Requirement: Gestión de espacios solo por administrador
The system SHALL permitir crear, listar, consultar, editar y desactivar espacios únicamente a usuarios con rol ADMINISTRADOR.

#### Scenario: Administrador crea espacio
- **WHEN** un usuario con rol ADMINISTRADOR crea un espacio
- **THEN** el sistema permite la operación

#### Scenario: Solicitante intenta crear espacio
- **WHEN** un usuario con rol SOLICITANTE intenta crear un espacio
- **THEN** el sistema rechaza la operación con código HTTP 403

### Requirement: Nombre único de espacio
The system SHALL garantizar que el nombre de cada espacio sea único. Si se intenta crear o editar un espacio con un nombre ya existente, el sistema SHALL retornar error con código HTTP 409.

#### Scenario: Creación con nombre duplicado
- **WHEN** un administrador intenta crear un espacio con un nombre que ya existe
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se crea el espacio

#### Scenario: Edición con nombre duplicado
- **WHEN** un administrador intenta editar un espacio cambiando su nombre por uno ya existente
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se actualiza el espacio

### Requirement: Validación de capacidad
The system SHALL validar que la capacidad sea un número entero mayor que 0. Si no cumple esta condición, el sistema SHALL retornar error con código HTTP 422.

#### Scenario: Capacidad inválida
- **WHEN** un administrador intenta crear o editar un espacio con capacidad 0, negativa o no entera
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Capacidad válida
- **WHEN** un administrador crea o edita un espacio con capacidad entera mayor que 0
- **THEN** el sistema acepta la operación

### Requirement: Desactivación de espacios
The system SHALL permitir desactivar espacios en lugar de eliminarlos. Los espacios desactivados SHALL no aparecer en los listados normales ni SHALL aceptar reservas.

#### Scenario: Desactivar espacio
- **WHEN** un administrador desactiva un espacio
- **THEN** el sistema marca el espacio como inactivo
- **AND** el espacio no se elimina de la base de datos

#### Scenario: Espacio desactivado no aparece en listado normal
- **GIVEN** existe un espacio desactivado
- **WHEN** se solicita el listado normal de espacios
- **THEN** el espacio desactivado no aparece en el resultado

#### Scenario: Espacio desactivado no acepta reservas
- **GIVEN** existe un espacio desactivado
- **WHEN** se intenta crear una reserva para ese espacio
- **THEN** el sistema rechaza la operación (la validación se aplicará en la etapa de reservas, pero el espacio no debe estar disponible)

### Requirement: Operaciones CRUD de espacios
The system SHALL permitir al administrador crear, listar, consultar, editar y desactivar espacios.

#### Scenario: Listar espacios
- **WHEN** un usuario autenticado solicita listar espacios
- **THEN** el sistema retorna la lista de espacios activos (en listado normal)

#### Scenario: Consultar espacio
- **WHEN** un usuario autenticado consulta un espacio específico
- **THEN** el sistema retorna la información del espacio

#### Scenario: Editar espacio
- **WHEN** un administrador edita los datos de un espacio
- **THEN** el sistema actualiza el espacio con los nuevos datos válidos
