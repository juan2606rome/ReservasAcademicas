# Tasks

## 1. Base de datos
- [ ] 1.1 Crear tabla reservas en schema.sql con campos: id, espacio_id, usuario_id, inicio, fin, motivo, estado, creada_en. Verificar estructura.
- [ ] 1.2 Agregar foreign keys a espacios y usuarios. Verificar restricciones.
- [ ] 1.3 Agregar restricción CHECK para fin > inicio. Verificar restricción.
- [ ] 1.4 Agregar índices para consultas de solapamiento por espacio. Verificar índices.

## 2. Capa de repositorio (reservas)
- [ ] 2.1 Crear reservas/repository.py con consultas parametrizadas. Verificar uso de parámetros.
- [ ] 2.2 Implementar búsqueda de reservas ocupadas por espacio y rango de tiempo (PENDIENTE o APROBADA), comparando solo en el MISMO espacio. Verificar consulta correcta.
- [ ] 2.3 Implementar creación de reserva dentro de transacción con BEGIN IMMEDIATE. Verificar uso de transacción.
- [ ] 2.4 Implementar consulta de disponibilidad por fecha (evaluada en hora de Bogotá America/Bogota, UTC-5), retornando franjas ocupadas ordenadas por inicio con inicio, fin y estado, sin datos de usuarios. Verificar funcionalidad.

## 3. Lógica de validación y políticas
- [ ] 3.1 Crear reservas/politicas.py con validaciones de fechas. Verificar fin > inicio, mismo día en hora de Bogotá (America/Bogota, UTC-5), inicio no en pasado en hora de Bogotá. Verificar que inicio y fin lleguen con zona horaria (si no, 422). Verificar conversión a UTC para guardado.
- [ ] 3.2 Implementar detección de solapamientos con intervalos [inicio, fin). Verificar fórmula correcta (a1 < b2 AND b1 < a2), solo mismo espacio, PENDIENTE contra PENDIENTE se solapa.
- [ ] 3.3 Crear función para verificar disponibilidad. Verificar lógica.
- [ ] 3.4 Validar motivo obligatorio, no vacío y máximo 500 caracteres. Verificar campos faltantes retornan 422.
- [ ] 3.5 Asegurar que usuario_id provenga del token (ignorar usuario en cuerpo). Verificar lógica.

## 4. Capa de servicio (reservas)
- [ ] 4.1 Crear reservas/service.py con lógica de creación de solicitud. Verificar estado PENDIENTE.
- [ ] 4.2 Validar existencia de espacio. Verificar retorno 404 si no existe.
- [ ] 4.3 Validar espacio activo. Verificar retorno 409 si inactivo.
- [ ] 4.4 Aplicar validaciones de fecha/hora, zona horaria, motivo y campos faltantes. Verificar retorno 422.
- [ ] 4.5 Aplicar orden de validaciones: 401, 422, 404, 409.
- [ ] 4.6 Implementar comprobación y creación en transacción con BEGIN IMMEDIATE. Verificar atomicidad.
- [ ] 4.7 Verificar solapamientos con reservas PENDIENTE o APROBADA solo en el MISMO espacio. Verificar retorno 409 en solapamiento.
- [ ] 4.8 Permitir reservas contiguas. Verificar que no hay solapamiento.
- [ ] 4.9 Implementar consulta de disponibilidad GET /reservas/disponibilidad con validaciones (espacio inexistente 404, fecha inválida/faltante 422), retornando lista vacía 200 si no hay reservas.
- [ ] 4.10 Implementar consulta de reservas GET /reservas (filtrado por rol: solicitante solo las suyas, administrador todas; filtros opcionales estado y espacio_id; más recientes primero).
- [ ] 4.11 Implementar consulta de reserva por id GET /reservas/{id} (dueño o administrador; ajena siendo solicitante 403; inexistente 404).

## 5. Capa de API (reservas)
- [ ] 5.1 Crear reservas/schemas.py con esquemas de petición y respuesta. Verificar validaciones (inicio/fin con zona horaria, motivo, etc.). Asegurar que las respuestas serialicen inicio/fin en formato ISO 8601 con zona horaria UTC.
- [ ] 5.2 Crear reservas/router.py con endpoints para crear solicitud, consultar disponibilidad, listar reservas y obtener reserva por id. Verificar rutas.
- [ ] 5.3 Proteger endpoints con autenticación (cualquier usuario autenticado puede crear solicitud y consultar disponibilidad). Verificar autorización.
- [ ] 5.4 Implementar POST /reservas/solicitudes retornando 201 con id, espacio_id, usuario_id, inicio, fin, motivo y estado=PENDIENTE en caso exitoso; inicio/fin en formato ISO 8601 con zona horaria UTC. Con códigos HTTP correctos según validaciones.
- [ ] 5.5 Implementar GET /reservas/disponibilidad con parámetros espacio_id y fecha. Verificar funcionalidad. Retornar franjas con inicio/fin en formato ISO 8601 con zona horaria UTC.
- [ ] 5.6 Implementar GET /reservas con filtros opcionales estado y espacio_id. Verificar filtrado por rol. Validar filtros inválidos (estado no válido o espacio_id no numérico) retornando 422. Retornar inicio/fin en formato ISO 8601 con zona horaria UTC.
- [ ] 5.7 Implementar GET /reservas/{id}. Verificar permisos (403 si ajena, 404 si inexistente). Retornar inicio/fin en formato ISO 8601 con zona horaria UTC.
- [ ] 5.8 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 6. Pruebas
- [ ] 6.1 Prueba: "Creación exitosa de solicitud" - usuario desde token, ignorar usuario en cuerpo, retorna 201 con id, espacio_id, usuario_id, inicio, fin, motivo y estado=PENDIENTE. Usar fechas futuras. Verificar test pasa.
- [ ] 6.2 Prueba: "Fin menor o igual a inicio" - verificar retorno 422. Usar fechas futuras. Verificar test pasa.
- [ ] 6.3 Prueba: "Reserva en días diferentes" - evaluar en hora de Bogotá, verificar retorno 422. Usar fechas futuras. Verificar test pasa.
- [ ] 6.4 Prueba: "Inicio en el pasado" - evaluar en hora de Bogotá, verificar retorno 422. Verificar test pasa.
- [ ] 6.5 Prueba: "Fechas sin zona horaria" - verificar retorno 422. Usar fechas futuras. Verificar test pasa.
- [ ] 6.6 Prueba: "Reserva válida de 19:00 a 21:00 hora de Bogotá" - verificar creación exitosa en estado PENDIENTE. Usar fechas futuras. Verificar test pasa.
- [ ] 6.7 Prueba: "Motivo vacío" - verificar retorno 422. Usar fechas futuras. Verificar test pasa.
- [ ] 6.8 Prueba: "Motivo excede 500 caracteres" - verificar retorno 422. Usar fechas futuras. Verificar test pasa.
- [ ] 6.9 Prueba: "Motivo faltante" - verificar retorno 422. Usar fechas futuras. Verificar test pasa.
- [ ] 6.10 Prueba: "Campos faltantes" - verificar retorno 422. Verificar test pasa.
- [ ] 6.11 Prueba: "Espacio inexistente" - verificar retorno 404. Usar fechas futuras. Verificar test pasa.
- [ ] 6.12 Prueba: "Espacio inactivo" - verificar retorno 409. Usar fechas futuras. Verificar test pasa.
- [ ] 6.13 Prueba: "Solapamiento detectado" - verificar retorno 409, solo mismo espacio. Usar fechas futuras. Verificar test pasa.
- [ ] 6.14 Prueba: "Reservas contiguas permitidas" - verificar creación exitosa. Usar fechas futuras. Verificar test pasa.
- [ ] 6.15 Prueba: "Reserva RECHAZADA o CANCELADA no ocupa espacio" - verificar permitido. Usar fechas futuras. Verificar test pasa.
- [ ] 6.16 Prueba: "Mismo horario en otro espacio es permitido" - verificar creación exitosa en ambos espacios. Usar fechas futuras. Verificar test pasa.
- [ ] 6.17 Prueba: "Una solicitud PENDIENTE contra otra PENDIENTE se solapa" - verificar retorno 409. Usar fechas futuras. Verificar test pasa.
- [ ] 6.18 Prueba: "Dos solicitudes simultáneas" - verificar solo una exitosa, otra con 409. Usar fechas futuras. Verificar test pasa.
- [ ] 6.19 Prueba: "Consultar disponibilidad con franjas ocupadas" - GET /reservas/disponibilidad, ordenadas por inicio, cada una con inicio, fin y estado, sin datos de usuarios; inicio/fin en formato ISO 8601 con zona horaria UTC. Usar fechas futuras. Verificar test pasa.
- [ ] 6.20 Prueba: "Sin reservas devuelve lista vacía" - GET /reservas/disponibilidad retorna lista vacía con 200. Usar fechas futuras. Verificar test pasa.
- [ ] 6.21 Prueba: "Espacio inexistente en consulta de disponibilidad" - verificar retorno 404. Verificar test pasa.
- [ ] 6.22 Prueba: "Fecha inválida o faltante en consulta de disponibilidad" - verificar retorno 422. Verificar test pasa.
- [ ] 6.23 Prueba: "Solicitante ve solo sus reservas" - GET /reservas, más recientes primero; inicio/fin en ISO 8601 UTC. Usar fechas futuras. Verificar test pasa.
- [ ] 6.24 Prueba: "Administrador ve todas las reservas" - GET /reservas; inicio/fin en ISO 8601 UTC. Usar fechas futuras. Verificar test pasa.
- [ ] 6.25 Prueba: "Filtrar reservas por estado" - GET /reservas?estado=PENDIENTE. Usar fechas futuras. Verificar test pasa.
- [ ] 6.26 Prueba: "Filtrar reservas por espacio_id" - GET /reservas?espacio_id=.... Usar fechas futuras. Verificar test pasa.
- [ ] 6.27 Prueba: "Consultar reserva propia por id" - GET /reservas/{id}; inicio/fin en ISO 8601 UTC. Usar fechas futuras. Verificar test pasa.
- [ ] 6.28 Prueba: "Administrador consulta cualquier reserva por id" - GET /reservas/{id}; inicio/fin en ISO 8601 UTC. Usar fechas futuras. Verificar test pasa.
- [ ] 6.29 Prueba: "Solicitante consulta reserva ajena" - GET /reservas/{id} retorna 403. Usar fechas futuras. Verificar test pasa.
- [ ] 6.30 Prueba: "Consultar reserva inexistente" - GET /reservas/{id} retorna 404. Verificar test pasa.
- [ ] 6.31 Prueba: "Orden de validaciones cuando hay varios errores" - 401, 422, 404, 409. Usar fechas futuras. Verificar test pasa.
- [ ] 6.32 Prueba: "Filtros inválidos de GET /reservas" - estado distinto de PENDIENTE, APROBADA, RECHAZADA o CANCELADA o espacio_id no numérico -> 422. Verificar test pasa.
- [ ] 6.33 Prueba: "Petición sin token y con datos inválidos" - retornar 401 (no 422). Verificar test pasa.
- [ ] 6.34 Prueba: "Petición con fechas inválidas y espacio_id inexistente" - retornar 422 (no 404). Verificar test pasa.
- [ ] 6.35 Prueba: "Petición válida sobre espacio inexistente" - retornar 404. Verificar test pasa.
- [ ] 6.36 Prueba: "Petición válida sobre espacio inactivo que además se solaparía" - retornar 409. Verificar test pasa.
- [ ] 6.37 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
