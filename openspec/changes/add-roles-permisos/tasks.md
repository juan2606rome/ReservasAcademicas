# Tasks

## 1. Estructura de autorización
- [ ] 1.1 Crear módulo autorizacion/ con estructura (router, service, repository, models, schemas, dependencies). Verificar estructura creada.
- [ ] 1.2 Crear módulo para utilidades de autenticación y autorización. Verificar archivos creados.

## 2. Autenticación con JWT y verificación de usuario
- [ ] 2.1 Implementar dependencia para extraer y validar token JWT desde el encabezado Authorization: Bearer <token>. Verificar que rechaza sin token o con formato incorrecto con 401.
- [ ] 2.2 Implementar validación de token inválido. Verificar retorno 401.
- [ ] 2.3 Implementar validación de token vencido. Verificar retorno 401.
- [ ] 2.4 Extraer información del usuario (id, rol) del token.
- [ ] 2.5 En cada petición protegida, consultar al usuario en la base de datos. Verificar que si no existe retorna 401; si está inactivo retorna 403.

## 3. Autorización por rol y restricción de valores
- [ ] 3.1 Crear dependencia para verificar rol ADMINISTRADOR. Verificar que rechaza rol insuficiente con 403.
- [ ] 3.2 Crear dependencia genérica para verificar roles permitidos. Verificar reutilización.
- [ ] 3.3 Garantizar que la columna rol solo acepta ADMINISTRADOR o SOLICITANTE. Verificar que intentar guardar otro valor falla.

## 4. Endpoints de administración de usuarios
- [ ] 4.1 Implementar GET /usuarios/yo (cualquier usuario autenticado). Verificar que devuelve id, nombre, correo y rol, nunca el hash. Verificar escenarios con 200, 401, 403.
- [ ] 4.2 Implementar GET /usuarios (solo ADMINISTRADOR). Verificar escenarios con 200, 401, 403.
- [ ] 4.3 Implementar GET /usuarios/{id} (solo ADMINISTRADOR). Verificar escenarios con 200, 401, 403, 404.
- [ ] 4.4 Implementar PATCH /usuarios/{id}/desactivar (solo ADMINISTRADOR). Verificar que un administrador no puede desactivarse a sí mismo (409). Verificar escenarios con 200, 401, 403, 404, 409.
- [ ] 4.5 Implementar PATCH /usuarios/{id}/activar (solo ADMINISTRADOR). Verificar escenarios con 200, 401, 403, 404.

## 5. Script seed para primer administrador
- [ ] 5.1 Crear script de inicialización (seed) para crear primer administrador. Verificar estructura del script.
- [ ] 5.2 Implementar lógica para obtener nombre, correo y contraseña desde las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO y ADMIN_PASSWORD. Verificar que no están escritos en el código.
- [ ] 5.3 Implementar lógica para crear usuario con rol ADMINISTRADOR solo si el correo no existe. Si el correo ya existe, no crear ni modificar. Verificar idempotencia.
- [ ] 5.4 Implementar manejo de errores si faltan alguna de las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO o ADMIN_PASSWORD; el script debe terminar con un mensaje de error. Verificar comportamiento.
- [ ] 5.5 Documentar uso del script. Verificar documentación presente.

## 6. Pruebas
- [ ] 6.1 Escribir prueba: "Sin token" (endpoint protegido) - verificar retorno 401. Verificar test pasa.
- [ ] 6.2 Escribir prueba: "Encabezado Authorization con formato incorrecto" - verificar retorno 401. Verificar test pasa.
- [ ] 6.3 Escribir prueba: "Token inválido" - verificar retorno 401. Verificar test pasa.
- [ ] 6.4 Escribir prueba: "Token vencido" - verificar retorno 401. Verificar test pasa.
- [ ] 6.5 Escribir prueba: "Usuario no existe en base de datos" - verificar retorno 401. Verificar test pasa.
- [ ] 6.6 Escribir prueba: "Usuario inactivo" - verificar retorno 403. Verificar test pasa.
- [ ] 6.7 Escribir prueba: "Rol insuficiente" - verificar retorno 403. Verificar test pasa.
- [ ] 6.8 Escribir prueba: "Intento de guardar rol inválido" - verificar que falla. Verificar test pasa.
- [ ] 6.9 Escribir prueba: "GET /usuarios/yo con usuario autenticado" - verificar 200 con id, nombre, correo, rol sin hash. Verificar test pasa.
- [ ] 6.10 Escribir prueba: "GET /usuarios/yo sin token" - verificar 401. Verificar test pasa.
- [ ] 6.11 Escribir prueba: "GET /usuarios/yo con token inválido" - verificar 401. Verificar test pasa.
- [ ] 6.12 Escribir prueba: "GET /usuarios/yo con usuario inactivo" - verificar 403. Verificar test pasa.
- [ ] 6.13 Escribir prueba: "GET /usuarios como ADMINISTRADOR" - verificar 200. Verificar test pasa.
- [ ] 6.14 Escribir prueba: "GET /usuarios sin token" - verificar 401. Verificar test pasa.
- [ ] 6.15 Escribir prueba: "GET /usuarios con rol insuficiente" - verificar 403. Verificar test pasa.
- [ ] 6.16 Escribir prueba: "GET /usuarios/{id} como ADMINISTRADOR" - verificar 200. Verificar test pasa.
- [ ] 6.17 Escribir prueba: "GET /usuarios/{id} sin token" - verificar 401. Verificar test pasa.
- [ ] 6.18 Escribir prueba: "GET /usuarios/{id} con rol insuficiente" - verificar 403. Verificar test pasa.
- [ ] 6.19 Escribir prueba: "GET /usuarios/{id} usuario inexistente" - verificar 404. Verificar test pasa.
- [ ] 6.20 Escribir prueba: "PATCH /usuarios/{id}/desactivar como ADMINISTRADOR" - verificar 200. Verificar test pasa.
- [ ] 6.21 Escribir prueba: "PATCH /usuarios/{id}/desactivar sin token" - verificar 401. Verificar test pasa.
- [ ] 6.22 Escribir prueba: "PATCH /usuarios/{id}/desactivar con rol insuficiente" - verificar 403. Verificar test pasa.
- [ ] 6.23 Escribir prueba: "PATCH /usuarios/{id}/desactivar usuario inexistente" - verificar 404. Verificar test pasa.
- [ ] 6.24 Escribir prueba: "PATCH /usuarios/{id}/desactivar a sí mismo" - verificar 409. Verificar test pasa.
- [ ] 6.25 Escribir prueba: "PATCH /usuarios/{id}/activar como ADMINISTRADOR" - verificar 200. Verificar test pasa.
- [ ] 6.26 Escribir prueba: "PATCH /usuarios/{id}/activar sin token" - verificar 401. Verificar test pasa.
- [ ] 6.27 Escribir prueba: "PATCH /usuarios/{id}/activar con rol insuficiente" - verificar 403. Verificar test pasa.
- [ ] 6.28 Escribir prueba: "PATCH /usuarios/{id}/activar usuario inexistente" - verificar 404. Verificar test pasa.
- [ ] 6.29 Escribir prueba: "Creación de primer administrador con seed" - verificar creación correcta. Verificar test pasa.
- [ ] 6.30 Escribir prueba: "Ejecución repetida del seed" - verificar que no crea ni modifica si el correo ya existe. Verificar test pasa.
- [ ] 6.31 Escribir prueba: "Variables de entorno faltantes" - verificar que el script termina con un mensaje de error. Verificar test pasa.
- [ ] 6.32 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
