# Spec Delta

## Purpose

Esta capacidad proporciona el control de acceso basado en roles para el sistema de reservas de espacios académicos. Define los roles ADMINISTRADOR y SOLICITANTE, establece una matriz de permisos, implementa la validación de tokens JWT y garantiza el manejo correcto de errores de autorización.

## ADDED Requirements

### Requirement: Roles del sistema
The system SHALL definir dos roles: ADMINISTRADOR y SOLICITANTE.

#### Scenario: Roles disponibles
- **WHEN** se consulta la lista de roles del sistema
- **THEN** el sistema reconoce únicamente los roles ADMINISTRADOR y SOLICITANTE

### Requirement: Matriz de permisos
The system SHALL aplicar la siguiente matriz de permisos:
- El ADMINISTRADOR SHALL gestionar espacios, ver todas las reservas, aprobar, rechazar y cancelar cualquiera
- El SOLICITANTE SHALL consultar espacios y disponibilidad, crear reservas, y ver y cancelar las suyas

#### Scenario: Administrador gestiona espacios
- **WHEN** un usuario con rol ADMINISTRADOR solicita gestionar espacios
- **THEN** el sistema permite la operación

#### Scenario: Administrador ve todas las reservas
- **WHEN** un usuario con rol ADMINISTRADOR solicita ver todas las reservas
- **THEN** el sistema permite ver todas las reservas sin restricción

#### Scenario: Administrador aprueba, rechaza y cancela cualquiera
- **WHEN** un usuario con rol ADMINISTRADOR aprueba, rechaza o cancela cualquier reserva
- **THEN** el sistema permite la operación

#### Scenario: Solicitante consulta espacios y disponibilidad
- **WHEN** un usuario con rol SOLICITANTE consulta espacios y disponibilidad
- **THEN** el sistema permite la operación

#### Scenario: Solicitante crea reservas
- **WHEN** un usuario con rol SOLICITANTE crea una reserva
- **THEN** el sistema permite la operación

#### Scenario: Solicitante ve y cancela las suyas
- **WHEN** un usuario con rol SOLICITANTE solicita ver o cancelar sus propias reservas
- **THEN** el sistema permite la operación

#### Scenario: Solicitante intenta cancelar reserva ajena
- **WHEN** un usuario con rol SOLICITANTE intenta cancelar una reserva que no le pertenece
- **THEN** el sistema rechaza la operación con código HTTP 403

### Requirement: Autenticación obligatoria
The system SHALL requerir un token JWT válido para acceder a endpoints protegidos.

#### Scenario: Sin token
- **WHEN** se realiza una petición a un endpoint protegido sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: Token inválido
- **WHEN** se realiza una petición a un endpoint protegido con un token inválido
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: Token vencido
- **WHEN** se realiza una petición a un endpoint protegido con un token vencido
- **THEN** el sistema retorna error con código HTTP 401

### Requirement: Autorización por rol
The system SHALL verificar que el rol del usuario tenga permiso para la operación solicitada.

#### Scenario: Rol insuficiente
- **WHEN** un usuario con rol insuficiente intenta realizar una operación no permitida por su rol
- **THEN** el sistema retorna error con código HTTP 403

### Requirement: Primer administrador mediante script seed
The system SHALL permitir crear el primer administrador mediante un script de inicialización (seed).

#### Scenario: Creación de primer administrador con seed
- **WHEN** se ejecuta el script de inicialización (seed) para crear el primer administrador
- **THEN** el sistema crea un usuario con rol ADMINISTRADOR
- **AND** el administrador puede autenticarse y realizar operaciones administrativas
