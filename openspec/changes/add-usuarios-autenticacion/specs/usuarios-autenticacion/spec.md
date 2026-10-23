# Spec Delta

## Purpose

Esta capacidad proporciona el registro y la autenticación de usuarios para el sistema de gestión de reservas de espacios académicos. Garantiza la creación segura de cuentas con correos únicos, almacenamiento de contraseñas con hash, autenticación basada en JWT y control de acceso para cuentas inactivas.

## ADDED Requirements

### Requirement: Registro de usuarios con nombre, correo único y contraseña
The system SHALL permitir el registro de usuarios proporcionando nombre, correo y contraseña. El correo SHALL ser único a nivel global, guardado en minúsculas y la unicidad no SHALL distinguir mayúsculas y minúsculas. Todo usuario nuevo SHALL crearse con rol SOLICITANTE y activo=true. Si la petición trae un rol, este SHALL ser ignorado. La respuesta SHALL nunca incluir la contraseña ni el hash de la contraseña.

#### Scenario: Registro exitoso
- **WHEN** un usuario proporciona nombre no vacío, correo con formato válido y contraseña entre 8 y 72 caracteres
- **THEN** el sistema crea la cuenta con rol SOLICITANTE, activo=true, correo en minúsculas y contraseña almacenada con hash
- **AND** el sistema retorna confirmación exitosa sin incluir contraseña ni hash

#### Scenario: Registro con correo duplicado
- **WHEN** un usuario intenta registrarse con un correo que ya existe (sin distinguir mayúsculas/minúsculas)
- **THEN** el sistema retorna error con código HTTP 409
- **AND** no se crea una cuenta duplicada

#### Scenario: Registro con datos inválidos
- **WHEN** un usuario proporciona correo con formato inválido, o contraseña menor a 8 caracteres o mayor a 72 caracteres, o nombre vacío
- **THEN** el sistema retorna error con código HTTP 422

#### Scenario: Registro ignora rol enviado
- **WHEN** un usuario envía un rol en la petición de registro
- **THEN** el sistema ignora ese rol y crea la cuenta con rol SOLICITANTE

### Requirement: Inicio de sesión con credenciales válidas
The system SHALL autenticar a usuarios con credenciales válidas y, si la cuenta está activa, SHALL retornar un token JWT. El token JWT SHALL contener id del usuario, rol y fecha de expiración (60 minutos). JWT_SECRET SHALL obtenerse de una variable de entorno, no del código.

#### Scenario: Inicio de sesión exitoso
- **WHEN** un usuario proporciona credenciales válidas para una cuenta activa
- **THEN** el sistema valida la contraseña contra el hash almacenado
- **AND** el sistema retorna un token JWT con id, rol y expiración de 60 minutos

#### Scenario: Inicio de sesión con contraseña incorrecta
- **WHEN** un usuario proporciona un correo registrado pero contraseña incorrecta
- **THEN** el sistema retorna error con código HTTP 401 con el mismo mensaje que cuando el correo no está registrado

#### Scenario: Inicio de sesión con correo no registrado
- **WHEN** un usuario intenta iniciar sesión con un correo no registrado
- **THEN** el sistema retorna error con código HTTP 401 con el mismo mensaje que cuando la contraseña es incorrecta

#### Scenario: Inicio de sesión con cuenta inactiva
- **WHEN** un usuario con cuenta inactiva proporciona credenciales válidas
- **THEN** el sistema rechaza el inicio de sesión
- **AND** el sistema retorna error con código HTTP 403

### Requirement: Almacenamiento seguro de contraseñas
The system SHALL almacenar las contraseñas de usuarios usando hash seguro. Las contraseñas SHALL nunca almacenarse en texto plano.

#### Scenario: Hash de contraseña en el registro
- **WHEN** un usuario se registra con una contraseña
- **THEN** el sistema genera el hash de la contraseña antes de almacenarla en la base de datos
- **AND** la contraseña en texto plano no se almacena
