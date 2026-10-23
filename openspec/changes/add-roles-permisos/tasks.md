# Tasks

## 1. Estructura de autorización
- [ ] 1.1 Crear módulo autorizacion/ con estructura (router, service, repository, models, schemas, dependencies). Verificar estructura creada.
- [ ] 1.2 Crear módulo para utilidades de autenticación y autorización. Verificar archivos creados.

## 2. Autenticación con JWT
- [ ] 2.1 Implementar dependencia para extraer y validar token JWT. Verificar que rechaza sin token con 401.
- [ ] 2.2 Implementar validación de token inválido. Verificar retorno 401.
- [ ] 2.3 Implementar validación de token vencido. Verificar retorno 401.
- [ ] 2.4 Extraer información del usuario (id, rol) del token. Verificar datos disponibles.

## 3. Autorización por rol
- [ ] 3.1 Crear dependencia para verificar rol ADMINISTRADOR. Verificar que rechaza rol insuficiente con 403.
- [ ] 3.2 Crear dependencia para verificar rol SOLICITANTE. Verificar comportamiento correcto.
- [ ] 3.3 Crear dependencia genérica para verificar roles permitidos. Verificar reutilización.
- [ ] 3.4 Implementar verificación de propiedad de recursos (para acciones sobre recursos propios). Verificar rechazo con 403 cuando no es propietario.

## 4. Script seed para primer administrador
- [ ] 4.1 Crear script de inicialización (seed) para crear primer administrador. Verificar estructura del script.
- [ ] 4.2 Implementar lógica para crear usuario con rol ADMINISTRADOR si no existe. Verificar creación correcta.
- [ ] 4.3 Agregar verificación para evitar duplicados. Verificar idempotencia.
- [ ] 4.4 Documentar uso del script. Verificar documentación presente.

## 5. Integración con endpoints existentes
- [ ] 5.1 Aplicar protección a endpoints que lo requieran según matriz de permisos. Verificar aplicación correcta.
- [ ] 5.2 Asegurar que la matriz se cumple: ADMINISTRADOR gestiona espacios, ve todas las reservas, aprueba/rechaza/cancela cualquiera. Verificar.
- [ ] 5.3 Asegurar que la matriz se cumple: SOLICITANTE consulta espacios/disponibilidad, crea reservas, ve/cancela las suyas. Verificar.
- [ ] 5.4 Verificar que SOLICITANTE no puede cancelar reserva ajena (403). Verificar.

## 6. Pruebas
- [ ] 6.1 Escribir prueba: "Sin token" - verificar retorno 401. Verificar test pasa.
- [ ] 6.2 Escribir prueba: "Token inválido" - verificar retorno 401. Verificar test pasa.
- [ ] 6.3 Escribir prueba: "Token vencido" - verificar retorno 401. Verificar test pasa.
- [ ] 6.4 Escribir prueba: "Roles disponibles" - verificar solo ADMINISTRADOR y SOLICITANTE. Verificar test pasa.
- [ ] 6.5 Escribir prueba: "Administrador gestiona espacios" - verificar permitido. Verificar test pasa.
- [ ] 6.6 Escribir prueba: "Administrador ve todas las reservas" - verificar permitido. Verificar test pasa.
- [ ] 6.7 Escribir prueba: "Administrador aprueba, rechaza y cancela cualquiera" - verificar permitido. Verificar test pasa.
- [ ] 6.8 Escribir prueba: "Solicitante consulta espacios y disponibilidad" - verificar permitido. Verificar test pasa.
- [ ] 6.9 Escribir prueba: "Solicitante crea reservas" - verificar permitido. Verificar test pasa.
- [ ] 6.10 Escribir prueba: "Solicitante ve y cancela las suyas" - verificar permitido. Verificar test pasa.
- [ ] 6.11 Escribir prueba: "Solicitante intenta cancelar reserva ajena" - verificar retorno 403. Verificar test pasa.
- [ ] 6.12 Escribir prueba: "Rol insuficiente" - verificar retorno 403. Verificar test pasa.
- [ ] 6.13 Escribir prueba: "Creación de primer administrador con seed" - verificar creación correcta. Verificar test pasa.
- [ ] 6.14 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
