# Tasks

## 1. Base de datos
- [ ] 1.1 Crear tabla HistorialReserva en schema.sql con campos: id, reserva_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario. Verificar estructura.
- [ ] 1.2 Agregar foreign keys. Verificar restricciones.
- [ ] 1.3 Agregar índices para consultas. Verificar índices.

## 2. Capa de repositorio (historial)
- [ ] 2.1 Crear historial/repository.py para registrar entradas de historial. Verificar consultas parametrizadas.
- [ ] 2.2 Implementar registro de historial con todos los campos. Verificar funcionalidad.
- [ ] 2.3 Implementar consulta de historial con filtros. Verificar filtros por espacio, estado, fecha.
- [ ] 2.4 Implementar filtrado por permisos (usuario propio vs todos). Verificar lógica.

## 3. Capa de repositorio (cancelacion)
- [ ] 3.1 Crear cancelacion/repository.py para operaciones de cancelación. Verificar estructura.
- [ ] 3.2 Implementar actualización de estado a CANCELADA. Verificar actualización.

## 4. Capa de servicio
- [ ] 4.1 Crear cancelacion/service.py con lógica de cancelación. Verificar estructura.
- [ ] 4.2 Validar permisos: solicitante solo sus reservas, administrador cualquiera. Verificar retorno 403.
- [ ] 4.3 Validar estado cancelable (PENDIENTE o APROBADA). Verificar retorno 409 para RECHAZADA/CANCELADA.
- [ ] 4.4 Implementar cancelación en transacción. Verificar atomicidad.
- [ ] 4.5 Registrar en historial al cancelar. Verificar registro completo.
- [ ] 4.6 Crear servicio para historial con verificación de permisos. Verificar filtros.

## 5. Integración con otros módulos
- [ ] 5.1 Agregar registro de historial al crear solicitud. Verificar registro.
- [ ] 5.2 Agregar registro de historial al aprobar. Verificar registro.
- [ ] 5.3 Agregar registro de historial al rechazar. Verificar registro.
- [ ] 5.4 Verificar que cancelar libera el horario (CANCELADA no ocupa). Verificar lógica.

## 6. Capa de API
- [ ] 6.1 Crear cancelacion/router.py con endpoint para cancelar. Verificar ruta.
- [ ] 6.2 Crear historial/router.py con endpoint para consultar historial. Verificar ruta.
- [ ] 6.3 Proteger endpoints con autenticación. Verificar autorización.
- [ ] 6.4 Implementar POST /reservas/{id}/cancelar con validaciones. Verificar códigos HTTP.
- [ ] 6.5 Implementar GET /historial con filtros y permisos. Verificar funcionalidad.
- [ ] 6.6 Registrar routers en aplicación principal. Verificar endpoints accesibles.

## 7. Pruebas
- [ ] 7.1 Escribir prueba: "Solicitante cancela su reserva PENDIENTE" - verificar CANCELADA y horario liberado. Verificar test pasa.
- [ ] 7.2 Escribir prueba: "Solicitante cancela su reserva APROBADA" - verificar CANCELADA y horario liberado. Verificar test pasa.
- [ ] 7.3 Escribir prueba: "Administrador cancela cualquier reserva" - verificar permitido. Verificar test pasa.
- [ ] 7.4 Escribir prueba: "No se cancela reserva RECHAZADA" - verificar retorno 409. Verificar test pasa.
- [ ] 7.5 Escribir prueba: "No se cancela reserva ya CANCELADA" - verificar retorno 409. Verificar test pasa.
- [ ] 7.6 Escribir prueba: "Solicitante intenta cancelar reserva ajena" - verificar retorno 403. Verificar test pasa.
- [ ] 7.7 Escribir prueba: "Cancelar libera el horario" - verificar disponibilidad. Verificar test pasa.
- [ ] 7.8 Escribir prueba: "Registro al crear solicitud" - verificar historial. Verificar test pasa.
- [ ] 7.9 Escribir prueba: "Registro al aprobar" - verificar historial. Verificar test pasa.
- [ ] 7.10 Escribir prueba: "Registro al rechazar" - verificar historial. Verificar test pasa.
- [ ] 7.11 Escribir prueba: "Registro al cancelar" - verificar historial. Verificar test pasa.
- [ ] 7.12 Escribir prueba: "Solicitante consulta su historial" - verificar solo lo suyo. Verificar test pasa.
- [ ] 7.13 Escribir prueba: "Administrador consulta todo el historial" - verificar sin restricción. Verificar test pasa.
- [ ] 7.14 Escribir prueba: "Filtrar por espacio" - verificar filtro. Verificar test pasa.
- [ ] 7.15 Escribir prueba: "Filtrar por estado" - verificar filtro. Verificar test pasa.
- [ ] 7.16 Escribir prueba: "Filtrar por fecha" - verificar filtro. Verificar test pasa.
- [ ] 7.17 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
