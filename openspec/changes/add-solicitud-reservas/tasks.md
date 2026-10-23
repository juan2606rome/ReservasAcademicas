# Tasks

## 1. Base de datos
- [ ] 1.1 Crear tabla reservas en schema.sql con campos: id, espacio_id, usuario_id, inicio, fin, motivo, estado, creada_en. Verificar estructura.
- [ ] 1.2 Agregar foreign keys a espacios y usuarios. Verificar restricciones.
- [ ] 1.3 Agregar restricción CHECK para fin > inicio. Verificar restricción.
- [ ] 1.4 Agregar índices para consultas de solapamiento. Verificar índices.

## 2. Capa de repositorio (reservas)
- [ ] 2.1 Crear reservas/repository.py con consultas parametrizadas. Verificar uso de parámetros.
- [ ] 2.2 Implementar búsqueda de reservas ocupadas por espacio y rango de tiempo (PENDIENTE o APROBADA). Verificar consulta correcta.
- [ ] 2.3 Implementar creación de reserva dentro de transacción. Verificar uso de transacción.
- [ ] 2.4 Implementar consulta de disponibilidad por fecha. Verificar funcionalidad.

## 3. Lógica de validación y políticas
- [ ] 3.1 Crear reservas/politicas.py con validaciones de fechas. Verificar fin > inicio, mismo día, inicio no en pasado.
- [ ] 3.2 Implementar detección de solapamientos con intervalos [inicio, fin). Verificar fórmula correcta.
- [ ] 3.3 Crear función para verificar disponibilidad. Verificar lógica.

## 4. Capa de servicio (reservas)
- [ ] 4.1 Crear reservas/service.py con lógica de creación de solicitud. Verificar estado PENDIENTE.
- [ ] 4.2 Validar existencia de espacio. Verificar retorno 404 si no existe.
- [ ] 4.3 Validar espacio activo. Verificar retorno 409 si inactivo.
- [ ] 4.4 Aplicar validaciones de fecha/hora. Verificar retorno 422.
- [ ] 4.5 Implementar comprobación y creación en transacción con BEGIN IMMEDIATE. Verificar atomicidad.
- [ ] 4.6 Verificar solapamientos con reservas PENDIENTE o APROBADA. Verificar retorno 409 en solapamiento.
- [ ] 4.7 Permitir reservas contiguas. Verificar que no hay solapamiento.
- [ ] 4.8 Implementar consulta de disponibilidad. Verificar retorno de franjas ocupadas.

## 5. Capa de API (reservas)
- [ ] 5.1 Crear reservas/schemas.py con esquemas de petición y respuesta. Verificar validaciones.
- [ ] 5.2 Crear reservas/router.py con endpoint para crear solicitud. Verificar ruta.
- [ ] 5.3 Crear endpoint para consultar disponibilidad. Verificar ruta.
- [ ] 5.4 Proteger endpoints con autenticación (cualquier usuario autenticado puede crear solicitud). Verificar autorización.
- [ ] 5.5 Implementar POST /reservas/solicitudes con códigos HTTP correctos. Verificar 201 éxito, 404 no existe, 409 inactivo/solapamiento, 422 validación.
- [ ] 5.6 Implementar GET /reservas/disponibilidad con parámetros espacio_id y fecha. Verificar funcionalidad.
- [ ] 5.7 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 6. Pruebas
- [ ] 6.1 Escribir prueba: "Creación exitosa de solicitud" - verificar estado PENDIENTE. Verificar test pasa.
- [ ] 6.2 Escribir prueba: "Fin menor o igual a inicio" - verificar retorno 422. Verificar test pasa.
- [ ] 6.3 Escribir prueba: "Reserva en días diferentes" - verificar retorno 422. Verificar test pasa.
- [ ] 6.4 Escribir prueba: "Inicio en el pasado" - verificar retorno 422. Verificar test pasa.
- [ ] 6.5 Escribir prueba: "Espacio inexistente" - verificar retorno 404. Verificar test pasa.
- [ ] 6.6 Escribir prueba: "Espacio inactivo" - verificar retorno 409. Verificar test pasa.
- [ ] 6.7 Escribir prueba: "Solapamiento detectado" - verificar retorno 409. Verificar test pasa.
- [ ] 6.8 Escribir prueba: "Reservas contiguas permitidas" - verificar creación exitosa. Verificar test pasa.
- [ ] 6.9 Escribir prueba: "Reserva RECHAZADA o CANCELADA no ocupa espacio" - verificar permitido. Verificar test pasa.
- [ ] 6.10 Escribir prueba: "Dos solicitudes simultáneas" - verificar solo una exitosa, otra con 409. Verificar test pasa.
- [ ] 6.11 Escribir prueba: "Consultar disponibilidad con franjas ocupadas" - verificar retorno correcto. Verificar test pasa.
- [ ] 6.12 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
