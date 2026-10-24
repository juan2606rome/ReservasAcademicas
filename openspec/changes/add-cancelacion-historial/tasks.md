# Tasks

## 1. Base de datos
- [ ] 1.1 Crear tabla HistorialReserva en schema.sql con campos: id, reserva_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario. Verificar estructura.
- [ ] 1.2 Agregar foreign keys. Verificar restricciones.
- [ ] 1.3 Agregar índices para consultas. Verificar índices.

## 2. Módulos y estructura
- [ ] 2.1 Crear módulos cancelacion/ e historial/ con las capas repository, service, router según corresponda. Verificar estructura.

## 3. Capa de repositorio (historial)
- [ ] 3.1 Crear historial/repository.py para registrar entradas de historial. Verificar consultas parametrizadas.
- [ ] 3.2 Implementar registro de historial con todos los campos (estado_anterior puede ser NULL). Verificar funcionalidad.
- [ ] 3.3 Implementar consulta de historial con filtros reserva_id, espacio_id, estado (estado_nuevo), desde y hasta (fechas AAAA-MM-DD en hora de Bogotá, inclusivas, sobre cambiado_en). Verificar filtros.
- [ ] 3.4 Implementar filtrado por permisos (usuario propio vs todos) y garantizar que el solicitante nunca vea historial ajeno. Verificar lógica.

## 4. Capa de repositorio (cancelacion)
- [ ] 4.1 Crear cancelacion/repository.py para operaciones de cancelación. Verificar estructura.
- [ ] 4.2 Implementar actualización de estado a CANCELADA. Verificar actualización.

## 5. Capa de servicio
- [ ] 5.1 Crear cancelacion/service.py con lógica de cancelación. Verificar estructura.
- [ ] 5.2 Aplicar orden de validaciones en cancelación: 401, 404, 403, 409. Sin token → 401 (sin evaluar existencia/propiedad/estado). Reserva inexistente → 404 (no 403). Reserva ajena RECHAZADA → 403 (no 409). Verificar precedencia.
- [ ] 5.3 Validar permisos: solicitante solo sus reservas, administrador cualquiera. Verificar retorno 403.
- [ ] 5.4 Validar estado cancelable (PENDIENTE o APROBADA). Verificar retorno 409 para RECHAZADA/CANCELADA. Verificar retorno 404 para reserva inexistente.
- [ ] 5.5 Implementar cancelación y registro en HistorialReserva en la misma transacción. Si falla el registro, el estado no cambia. Verificar atomicidad.
- [ ] 5.6 Permitir comentario o motivo opcional en cancelación (máximo 500 caracteres). Usar "Cancelada" o el motivo si se dio. Verificar funcionalidad.
- [ ] 5.7 Crear servicio para historial con verificación de permisos. Un solicitante con filtros no puede ver historial ajeno (lista vacía con 200). Verificar filtros.
- [ ] 5.8 Validar valores inválidos en filtros de historial retornando 422. Ordenar resultados del más reciente al más antiguo.

## 6. Integración con otros módulos
- [ ] 6.1 Agregar registro de historial al crear solicitud. Estado_anterior NULL, estado_nuevo PENDIENTE, comentario "Solicitud creada". Verificar registro y que las funcionalidades de la etapa de creación siguen funcionando (prueba de regresión).
- [ ] 6.2 Agregar registro de historial al aprobar. Estado_anterior PENDIENTE, estado_nuevo APROBADA, comentario "Aprobada" o el motivo si se dio. Verificar registro y que las funcionalidades de la etapa de aprobación siguen funcionando (prueba de regresión).
- [ ] 6.3 Agregar registro de historial al rechazar. Estado_anterior PENDIENTE, estado_nuevo RECHAZADA, comentario con el motivo del rechazo. Verificar registro y que las funcionalidades de la etapa de rechazo siguen funcionando (prueba de regresión).
- [ ] 6.4 Verificar que cancelar libera el horario (CANCELADA no ocupa). Verificar lógica.

## 7. Capa de API
- [ ] 7.1 Crear cancelacion/router.py con endpoint para cancelar. Verificar ruta.
- [ ] 7.2 Crear historial/router.py con endpoint para consultar historial. Verificar ruta.
- [ ] 7.3 Proteger endpoints con autenticación. Verificar autorización (401 sin token).
- [ ] 7.4 Implementar POST /reservas/{id}/cancelar con validaciones en orden 401, 404, 403, 409. Retornar 200 en éxito. Comentario/motivo opcional (máximo 500 caracteres). Verificar códigos HTTP.
- [ ] 7.5 Implementar GET /historial con filtros opcionales reserva_id, espacio_id, estado (estado_nuevo), desde y hasta (AAAA-MM-DD hora de Bogotá, inclusivas, sobre cambiado_en), permisos correctos, 422 para valores inválidos, orden del más reciente al más antiguo. El campo cambiado_en SHALL devolverse en formato ISO 8601 con zona horaria UTC. Verificar funcionalidad.
- [ ] 7.6 Registrar routers en aplicación principal. Verificar endpoints accesibles.

## 8. Pruebas
- [ ] 8.1 Escribir prueba: "Sin token al cancelar" - verificar retorno 401 sin evaluar existencia/propiedad/estado. Verificar test pasa.
- [ ] 8.2 Escribir prueba: "Solicitante intenta cancelar una reserva inexistente" - verificar retorno 404 (no 403). Verificar test pasa.
- [ ] 8.3 Escribir prueba: "Solicitante intenta cancelar una reserva ajena RECHAZADA" - verificar retorno 403 (no 409). Verificar test pasa.
- [ ] 8.4 Escribir prueba: "Solicitante cancela su reserva PENDIENTE con éxito" - verificar 200, CANCELADA y horario liberado. Verificar test pasa.
- [ ] 8.5 Escribir prueba: "Solicitante cancela su reserva APROBADA con éxito" - verificar 200, CANCELADA y horario liberado. Verificar test pasa.
- [ ] 8.6 Escribir prueba: "Administrador cancela cualquier reserva" - verificar permitido, 200. Verificar test pasa.
- [ ] 8.7 Escribir prueba: "No se cancela reserva RECHAZADA" - verificar retorno 409. Verificar test pasa.
- [ ] 8.8 Escribir prueba: "No se cancela reserva ya CANCELADA" - verificar retorno 409. Verificar test pasa.
- [ ] 8.9 Escribir prueba: "Solicitante intenta cancelar reserva ajena" - verificar retorno 403. Verificar test pasa.
- [ ] 8.10 Escribir prueba: "Cancelar libera el horario" - verificar disponibilidad. Verificar test pasa.
- [ ] 8.11 Escribir prueba: "Registro al crear solicitud" - verificar estado_anterior NULL, estado_nuevo PENDIENTE, comentario "Solicitud creada". Verificar test pasa.
- [ ] 8.12 Escribir prueba: "Registro al aprobar" - verificar historial con comentario "Aprobada" o motivo. Verificar test pasa.
- [ ] 8.13 Escribir prueba: "Registro al rechazar" - verificar historial con motivo del rechazo. Verificar test pasa.
- [ ] 8.14 Escribir prueba: "Registro al cancelar" - verificar historial con "Cancelada" o motivo. Verificar test pasa.
- [ ] 8.15 Escribir prueba: "Cambio de estado y registro en la misma transacción" - verificar que si falla el registro, el estado no cambia. Verificar test pasa.
- [ ] 8.16 Escribir prueba: "Sin token al consultar historial" - verificar retorno 401. Verificar test pasa.
- [ ] 8.17 Escribir prueba: "Solicitante consulta su historial" - verificar solo lo suyo, orden del más reciente al más antiguo. Verificar test pasa.
- [ ] 8.18 Escribir prueba: "Solicitante con filtros no ve historial ajeno" - verificar lista vacía con 200. Verificar test pasa.
- [ ] 8.19 Escribir prueba: "Administrador consulta todo el historial" - verificar sin restricción. Verificar test pasa.
- [ ] 8.20 Escribir prueba: "Filtrar por reserva_id" - verificar filtro. Verificar test pasa.
- [ ] 8.21 Escribir prueba: "Filtrar por espacio_id" - verificar filtro. Verificar test pasa.
- [ ] 8.22 Escribir prueba: "Filtrar por estado" - verificar filtro comparado con estado_nuevo. Verificar test pasa.
- [ ] 8.23 Escribir prueba: "Filtrar por rango de fechas en hora de Bogotá" - verificar inclusivas sobre cambiado_en. Verificar test pasa.
- [ ] 8.24 Escribir prueba: "Fechas en formato ISO 8601 UTC" - verificar que cambiado_en se devuelve en ISO 8601 con zona horaria UTC. Verificar test pasa.
- [ ] 8.25 Escribir prueba: "Valores inválidos en filtros" - verificar retorno 422. Verificar test pasa.
- [ ] 8.26 Escribir prueba: "Regresión: creación de solicitud sigue funcionando" - verificar que la funcionalidad de la etapa anterior no se rompe. Verificar test pasa.
- [ ] 8.27 Escribir prueba: "Regresión: aprobación/rechazo siguen funcionando" - verificar que las funcionalidades de las etapas anteriores no se rompen. Verificar test pasa.
- [ ] 8.28 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
