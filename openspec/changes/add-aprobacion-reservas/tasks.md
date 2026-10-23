# Tasks

## 1. Base de datos
- [ ] 1.1 Verificar campos en tabla reservas: decidido_por, decidido_en, motivo_decision. Agregar si faltan. Verificar estructura.
- [ ] 1.2 Asegurar tipos correctos para trazabilidad. Verificar campos.

## 2. Capa de repositorio (aprobacion)
- [ ] 2.1 Crear aprobacion/repository.py con operaciones para aprobar/rechazar. Verificar consultas parametrizadas.
- [ ] 2.2 Implementar búsqueda de reserva por id. Verificar funcionalidad.
- [ ] 2.3 Implementar actualización de estado con trazabilidad. Verificar actualización.
- [ ] 2.4 Reutilizar lógica de verificación de solapamientos. Verificar integración.

## 3. Capa de servicio (aprobacion)
- [ ] 3.1 Crear aprobacion/service.py con lógica de aprobación y rechazo. Verificar estructura.
- [ ] 3.2 Validar existencia de reserva. Verificar retorno 404.
- [ ] 3.3 Validar que sea rol ADMINISTRADOR. Verificar retorno 403.
- [ ] 3.4 Validar estado PENDIENTE. Verificar retorno 409 para otros estados.
- [ ] 3.5 Validar motivo obligatorio al rechazar. Verificar retorno 422.
- [ ] 3.6 Registrar decidido_por, decidido_en, motivo_decision. Verificar trazabilidad.
- [ ] 3.7 Revalidar disponibilidad al aprobar. Verificar detección de conflictos.
- [ ] 3.8 Realizar operaciones en transacción. Verificar atomicidad.

## 4. Capa de API (aprobacion)
- [ ] 4.1 Crear aprobacion/router.py con endpoints para aprobar y rechazar. Verificar rutas.
- [ ] 4.2 Proteger endpoints con rol ADMINISTRADOR. Verificar autorización.
- [ ] 4.3 Implementar POST /reservas/{id}/aprobar. Verificar códigos HTTP.
- [ ] 4.4 Implementar POST /reservas/{id}/rechazar con motivo. Verificar códigos HTTP.
- [ ] 4.5 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 5. Pruebas
- [ ] 5.1 Escribir prueba: "Administrador aprueba reserva" - verificar permitido. Verificar test pasa.
- [ ] 5.2 Escribir prueba: "Solicitante intenta aprobar" - verificar retorno 403. Verificar test pasa.
- [ ] 5.3 Escribir prueba: "Solicitante intenta rechazar" - verificar retorno 403. Verificar test pasa.
- [ ] 5.4 Escribir prueba: "Aprobar reserva ya aprobada" - verificar retorno 409. Verificar test pasa.
- [ ] 5.5 Escribir prueba: "Rechazar reserva ya rechazada" - verificar retorno 409. Verificar test pasa.
- [ ] 5.6 Escribir prueba: "Aprobar reserva cancelada" - verificar retorno 409. Verificar test pasa.
- [ ] 5.7 Escribir prueba: "Rechazo sin motivo" - verificar retorno 422. Verificar test pasa.
- [ ] 5.8 Escribir prueba: "Rechazo con motivo" - verificar aceptado. Verificar test pasa.
- [ ] 5.9 Escribir prueba: "Registro de aprobación" - verificar decidido_por, decidido_en, motivo_decision. Verificar test pasa.
- [ ] 5.10 Escribir prueba: "Registro de rechazo" - verificar trazabilidad. Verificar test pasa.
- [ ] 5.11 Escribir prueba: "Aprobar sin conflictos" - verificar aprobación exitosa. Verificar test pasa.
- [ ] 5.12 Escribir prueba: "Aprobar con conflicto" - verificar rechazo o manejo correcto. Verificar test pasa.
- [ ] 5.13 Escribir prueba: "Aprobar reserva inexistente" - verificar retorno 404. Verificar test pasa.
- [ ] 5.14 Escribir prueba: "Rechazar reserva inexistente" - verificar retorno 404. Verificar test pasa.
- [ ] 5.15 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
