# Tasks

## 1. Estructura del proyecto
- [ ] 1.1 Crear estructura de carpetas src/app/ y tests/ (unit, integration). Verificar que las carpetas existen.
- [ ] 1.2 Crear archivo requirements.txt con dependencias necesarias (FastAPI, uvicorn, bcrypt, PyJWT, pytest, httpx). Verificar instalación de dependencias.
- [ ] 1.3 Crear main.py en src/app/. Verificar que la aplicación FastAPI se inicializa correctamente.
- [ ] 1.4 Crear módulo nucleo/ con conexión sqlite3, configuración, schema.sql y utilidades. Verificar conexión a base de datos.
- [ ] 1.5 Crear archivo .gitignore adecuado. Verificar que archivos sensibles no se rastrean.

## 2. Base de datos
- [ ] 2.1 Crear schema.sql con tabla usuarios (id, nombre, correo, hash_contraseña, rol, activo). Verificar que schema.sql existe y tiene la estructura correcta.
- [ ] 2.2 Agregar restricción UNIQUE en correo y tipos de datos apropiados. Verificar restricción en schema.
- [ ] 2.3 Implementar inicialización de base de datos desde schema.sql. Verificar que las tablas se crean correctamente.

## 3. Capa de repositorio (usuarios)
- [ ] 3.1 Crear usuarios/repository.py con función para crear usuario usando consultas parametrizadas. Verificar uso de parámetros.
- [ ] 3.2 Crear función para buscar usuario por correo (normalizado a minúsculas). Verificar búsqueda correcta.
- [ ] 3.3 Crear función para verificar existencia de correo sin distinguir mayúsculas/minúsculas. Verificar comportamiento correcto.
- [ ] 3.4 Manejar violación de UNIQUE constraint y propagarla al servicio. Verificar manejo de errores.

## 4. Hash de contraseñas
- [ ] 4.1 Configurar bcrypt para hash de contraseñas. Verificar configuración correcta.
- [ ] 4.2 Implementar función de hash de contraseña. Verificar que el hash es diferente al texto plano.
- [ ] 4.3 Implementar función de verificación de contraseña. Verificar validación correcta.

## 5. Capa de servicio (usuarios)
- [ ] 5.1 Crear usuarios/service.py con lógica de registro. Verificar que rol siempre es SOLICITANTE, activo=true, correo en minúsculas, contraseña hasheada, rol enviado es ignorado.
- [ ] 5.2 Implementar validaciones en servicio: correo formato válido, contraseña 8-72 caracteres, nombre no vacío. Verificar retorno 422 para datos inválidos.
- [ ] 5.3 Implementar lógica de login con verificación de contraseña, verificación de cuenta activa. Verificar mismo mensaje para correo no registrado y contraseña incorrecta (401), cuenta inactiva retorna 403.
- [ ] 5.4 Implementar generación de JWT con id, rol y expiración 60 minutos, usando JWT_SECRET desde variable de entorno. Verificar estructura del token.
- [ ] 5.5 Manejar violación de UNIQUE desde repositorio y retornar 409. Verificar respuesta correcta.
- [ ] 5.6 Asegurar que la respuesta de registro nunca incluya contraseña ni hash. Verificar estructura de respuesta.

## 6. Capa de API (usuarios)
- [ ] 6.1 Crear usuarios/schemas.py con esquemas de petición y respuesta. Verificar validaciones y que respuesta no incluye campos sensibles.
- [ ] 6.2 Crear usuarios/router.py con POST /usuarios/registro. Verificar códigos HTTP: 201 éxito, 409 duplicado, 422 datos inválidos.
- [ ] 6.3 Crear POST /usuarios/login. Verificar códigos HTTP: 200 éxito, 401 credenciales incorrectas/correo no registrado, 403 cuenta inactiva, 422 datos inválidos.
- [ ] 6.4 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 7. Pruebas
- [ ] 7.1 Escribir prueba unitaria: "Hash de contraseña en el registro" - verificar hash diferente al texto plano. Verificar test pasa.
- [ ] 7.2 Escribir prueba de integración: "Registro exitoso" - verificar rol SOLICITANTE, activo=true, sin contraseña/hash en respuesta. Verificar test pasa.
- [ ] 7.3 Escribir prueba de integración: "Registro con correo duplicado" - verificar respuesta 409. Verificar test pasa.
- [ ] 7.4 Escribir prueba de integración: "Registro ignora rol enviado" - verificar rol sigue siendo SOLICITANTE. Verificar test pasa.
- [ ] 7.5 Escribir prueba de integración: "Registro con datos inválidos" - verificar respuesta 422 para correo inválido, contraseña corta/larga, nombre vacío. Verificar test pasa.
- [ ] 7.6 Escribir prueba de integración: "Inicio de sesión exitoso" - verificar token JWT con id, rol, expiración 60 min. Verificar test pasa.
- [ ] 7.7 Escribir prueba de integración: "Inicio de sesión con contraseña incorrecta" - verificar respuesta 401 con mismo mensaje que correo no registrado. Verificar test pasa.
- [ ] 7.8 Escribir prueba de integración: "Inicio de sesión con correo no registrado" - verificar respuesta 401 con mismo mensaje que contraseña incorrecta. Verificar test pasa.
- [ ] 7.9 Escribir prueba de integración: "Inicio de sesión con cuenta inactiva" - verificar respuesta 403. Verificar test pasa.
- [ ] 7.10 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
