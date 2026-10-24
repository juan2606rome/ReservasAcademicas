# Spec Delta

## Purpose

Esta capacidad proporciona el control de acceso basado en roles para el sistema de reservas de espacios académicos. Define los roles ADMINISTRADOR y SOLICITANTE, establece una matriz de permisos, implementa la validación de tokens JWT y garantiza el manejo correcto de errores de autorización.

## ADDED Requirements

### Requirement: Restricción de valores del rol
El sistema SHALL aceptar únicamente los valores ADMINISTRADOR o SOLICITANTE en la columna rol. Si se intenta guardar cualquier otro valor en la columna rol, el sistema SHALL rechazar la operación.

#### Scenario: Intento de guardar rol inválido
- **WHEN** se intenta guardar un usuario con un valor distinto a ADMINISTRADOR o SOLICITANTE en la columna rol
- **THEN** el sistema rechaza la operación

### Requirement: Matriz de permisos
El sistema SHALL aplicar la siguiente matriz de permisos:

| Endpoint | Roles permitidos |
| GET /usuarios/yo | ADMINISTRADOR, SOLICITANTE |
| GET /usuarios | ADMINISTRADOR |
| GET /usuarios/{id} | ADMINISTRADOR |
| PATCH /usuarios/{id}/desactivar | ADMINISTRADOR |
| PATCH /usuarios/{id}/activar | ADMINISTRADOR |

Cada etapa posterior verifica los permisos de sus propios endpoints.

#### Scenario: SOLICITANTE recibe 200 en GET /usuarios/yo
- **WHEN** un usuario con rol SOLICITANTE realiza una petición GET /usuarios/yo con token válido
- **THEN** el sistema retorna código HTTP 200 con id, nombre, correo y rol, sin el hash de contraseña

#### Scenario: SOLICITANTE recibe 403 en GET /usuarios
- **WHEN** un usuario con rol SOLICITANTE realiza una petición GET /usuarios con token válido
- **THEN** el sistema retorna error con código HTTP 403

### Requirement: Autenticación obligatoria
El sistema SHALL requerir que el token se envíe en el encabezado Authorization: Bearer <token>. Si el encabezado falta o tiene formato incorrecto, el sistema SHALL retornar error con código HTTP 401. El sistema SHALL requerir un token JWT válido para acceder a endpoints protegidos.

#### Scenario: Sin token
- **WHEN** se realiza una petición a un endpoint protegido sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: Encabezado Authorization con formato incorrecto
- **WHEN** se realiza una petición a un endpoint protegido con el encabezado Authorization en formato incorrecto
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: Token inválido
- **WHEN** se realiza una petición a un endpoint protegido con un token inválido
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: Token vencido
- **WHEN** se realiza una petición a un endpoint protegido con un token vencido
- **THEN** el sistema retorna error con código HTTP 401

### Requirement: Verificación de usuario en base de datos
En cada petición protegida, el sistema SHALL consultar al usuario en la base de datos. Si el usuario no existe, el sistema SHALL retornar error con código HTTP 401. Si el usuario existe pero está inactivo, el sistema SHALL retornar error con código HTTP 403, aunque el token no haya vencido.

#### Scenario: Usuario no existe en base de datos
- **WHEN** se realiza una petición a un endpoint protegido con un token válido pero el usuario asociado no existe en la base de datos
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: Usuario inactivo
- **WHEN** se realiza una petición a un endpoint protegido con un token válido para un usuario que existe pero está inactivo
- **THEN** el sistema retorna error con código HTTP 403

### Requirement: Autorización por rol
El sistema SHALL verificar que el rol del usuario tenga permiso para la operación solicitada.

#### Scenario: Rol insuficiente
- **WHEN** un usuario con rol insuficiente intenta realizar una operación no permitida por su rol
- **THEN** el sistema retorna error con código HTTP 403

### Requirement: Administración de usuarios
El sistema SHALL exponer los siguientes endpoints, accesibles solo para usuarios con rol ADMINISTRADOR: GET /usuarios (lista), GET /usuarios/{id}, PATCH /usuarios/{id}/desactivar y PATCH /usuarios/{id}/activar. Un administrador no puede desactivarse a sí mismo, por lo que dicha operación SHALL retornar error con código HTTP 409. Si el usuario especificado no existe, el sistema SHALL retornar error con código HTTP 404.

Además, el sistema SHALL exponer GET /usuarios/yo, accesible para cualquier usuario autenticado, que SHALL devolver id, nombre, correo y rol del usuario autenticado, nunca el hash de contraseña.

#### Scenario: GET /usuarios/yo con usuario autenticado
- **WHEN** un usuario autenticado realiza una petición GET /usuarios/yo
- **THEN** el sistema retorna código HTTP 200 con id, nombre, correo y rol, sin el hash de contraseña

#### Scenario: GET /usuarios/yo sin token
- **WHEN** se realiza una petición GET /usuarios/yo sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: GET /usuarios/yo con token inválido
- **WHEN** se realiza una petición GET /usuarios/yo con token inválido
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: GET /usuarios/yo con usuario inactivo
- **WHEN** un usuario inactivo realiza una petición GET /usuarios/yo con token válido
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: Un usuario desactivado por un administrador recibe 403 al intentar iniciar sesión
- **WHEN** un usuario desactivado por un administrador intenta iniciar sesión
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: GET /usuarios como ADMINISTRADOR
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición GET /usuarios
- **THEN** el sistema retorna código HTTP 200 con la lista de usuarios

#### Scenario: GET /usuarios sin token
- **WHEN** se realiza una petición GET /usuarios sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: GET /usuarios con rol insuficiente
- **WHEN** un usuario con rol SOLICITANTE realiza una petición GET /usuarios
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: GET /usuarios/{id} como ADMINISTRADOR
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición GET /usuarios/{id} con un id existente
- **THEN** el sistema retorna código HTTP 200 con los datos del usuario, sin el hash de la contraseña

#### Scenario: Ninguna respuesta de administración o GET /usuarios/{id} incluye el hash de la contraseña
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición GET /usuarios, GET /usuarios/{id}, PATCH /usuarios/{id}/desactivar o PATCH /usuarios/{id}/activar
- **THEN** ninguna respuesta incluye el hash de la contraseña

#### Scenario: GET /usuarios/{id} sin token
- **WHEN** se realiza una petición GET /usuarios/{id} sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: GET /usuarios/{id} con rol insuficiente
- **WHEN** un usuario con rol SOLICITANTE realiza una petición GET /usuarios/{id}
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: GET /usuarios/{id} usuario inexistente
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición GET /usuarios/{id} con un id inexistente
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: PATCH /usuarios/{id}/desactivar como ADMINISTRADOR
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición PATCH /usuarios/{id}/desactivar sobre otro usuario existente
- **THEN** el sistema retorna código HTTP 200

#### Scenario: PATCH /usuarios/{id}/desactivar sin token
- **WHEN** se realiza una petición PATCH /usuarios/{id}/desactivar sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: PATCH /usuarios/{id}/desactivar con rol insuficiente
- **WHEN** un usuario con rol SOLICITANTE realiza una petición PATCH /usuarios/{id}/desactivar
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: PATCH /usuarios/{id}/desactivar usuario inexistente
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición PATCH /usuarios/{id}/desactivar con un id inexistente
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: PATCH /usuarios/{id}/desactivar a sí mismo
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición PATCH /usuarios/{id}/desactivar sobre su propio id
- **THEN** el sistema retorna error con código HTTP 409

#### Scenario: PATCH /usuarios/{id}/activar como ADMINISTRADOR
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición PATCH /usuarios/{id}/activar sobre otro usuario inactivo
- **THEN** el sistema retorna código HTTP 200

#### Scenario: PATCH /usuarios/{id}/activar sin token
- **WHEN** se realiza una petición PATCH /usuarios/{id}/activar sin token
- **THEN** el sistema retorna error con código HTTP 401

#### Scenario: PATCH /usuarios/{id}/activar con rol insuficiente
- **WHEN** un usuario con rol SOLICITANTE realiza una petición PATCH /usuarios/{id}/activar
- **THEN** el sistema retorna error con código HTTP 403

#### Scenario: PATCH /usuarios/{id}/activar usuario inexistente
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición PATCH /usuarios/{id}/activar con un id inexistente
- **THEN** el sistema retorna error con código HTTP 404

#### Scenario: Activar un usuario que ya está activo
- **WHEN** un usuario con rol ADMINISTRADOR realiza una petición PATCH /usuarios/{id}/activar sobre otro usuario que ya está activo
- **THEN** el sistema retorna código HTTP 200 sin cambios

### Requirement: Primer administrador mediante script seed
El sistema SHALL permitir crear el primer administrador mediante un script de inicialización (seed). El nombre, el correo y la contraseña del primer administrador SHALL salir de las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO y ADMIN_PASSWORD, y nunca SHALL estar escritos en el código. Si el correo ya existe en la base de datos, el script SHALL NOT crear otro usuario ni SHALL NOT modificar el usuario existente. Si faltan alguna de las variables de entorno requeridas, el script SHALL terminar con un mensaje de error.

#### Scenario: Cuando se ejecuta el script con las tres variables de entorno definidas y el correo no existe
- **WHEN** se ejecutan las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO y ADMIN_PASSWORD correctamente y el correo no existe
- **THEN** el sistema crea un usuario con rol ADMINISTRADOR

#### Scenario: Ejecución repetida del seed
- **WHEN** se ejecuta el script de inicialización (seed) nuevamente y el correo ya existe en la base de datos
- **THEN** el script no crea otro usuario ni modifica el usuario existente

#### Scenario: Variables de entorno faltantes
- **WHEN** se ejecuta el script de inicialización (seed) y faltan alguna de las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO o ADMIN_PASSWORD
- **THEN** el script termina con un mensaje de error
