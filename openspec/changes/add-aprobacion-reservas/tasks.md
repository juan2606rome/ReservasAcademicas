# Tasks

## 1. Base de datos
- [ ] 1.1 Agregar columnas decidido_por, decidido_en y motivo_decision a schema.sql en esta etapa (no "agregar si faltan"). Verificar estructura.
- [ ] 1.2 Asegurar tipos correctos para trazabilidad. Verificar campos.

## 2. Capa de repositorio (aprobacion)
- [ ] 2.1 Crear aprobacion/repository.py con operaciones para aprobar/rechazar. Verificar consultas parametrizadas.
- [ ] 2.2 Implementar búsqueda de reserva por id. Verificar funcionalidad.
- [ ] 2.3 Implementar actualización de estado con trazabilidad. Verificar actualización.
- [ ] 2.4 Reutilizar lógica de verificación de solapamientos (excluyendo la propia reserva). Verificar integración.

## 3. Capa de servicio (aprobacion)
- [ ] 3.1 Crear aprobacion/service.py con lógica de aprobación y rechazo. Verificar estructura.
- [ ] 3.2 Aplicar orden de validaciones: 401, 403, 404, 422, 409. Verificar orden.
- [ ] 3.3 Validar existencia de reserva. Verificar retorno 404.
- [ ] 3.4 Validar que sea rol ADMINISTRADOR. Verificar retorno 403.
- [ ] 3.5 Validar estado PENDIENTE. Verificar retorno 409 para otros estados.
- [ ] 3.6 Validar motivo al rechazar: obligatorio, no vacío ni solo espacios, máximo 500 caracteres. Verificar retorno 422. Motivo opcional al aprobar (puede ser nulo).
- [ ] 3.7 Validar que no se apruebe si el inicio ya pasó. Verificar retorno 409.
- [ ] 3.8 Registrar decidido_por, decidido_en, motivo_decision. Verificar trazabilidad.
- [ ] 3.9 Revalidar disponibilidad al aprobar, excluyendo la propia reserva. Por decisión D6, solo conflicto por inconsistencia de datos. Verificar detección de conflictos (prueba con reserva solapada insertada directamente en BD).
- [ ] 3.10 Realizar operaciones en transacción con BEGIN IMMEDIATE. Verificar atomicidad.

## 4. Capa de API (aprobacion)
- [ ] 4.1 Crear aprobacion/router.py con endpoints para aprobar y rechazar. Verificar rutas.
- [ ] 4.2 Proteger endpoints con rol ADMINISTRADOR. Verificar autorización.
- [ ] 4.3 Implementar POST /reservas/{id}/aprobar (motivo opcional en cuerpo). Verificar códigos HTTP (200 al aprobar, deja en APROBADA).
- [ ] 4.4 Implementar POST /reservas/{id}/rechazar (motivo obligatorio en cuerpo). Verificar códigos HTTP (200 al rechazar, deja en RECHAZADA).
- [ ] 4.5 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 5. Pruebas
- [ ] 5.1 Escribir prueba: "Administrador aprueba reserva" - verificar responde 200 y reserva queda en APROBADA.
- [ ] 5.2 Escribir prueba: "Administrador rechaza reserva" - verificar responde 200 y reserva queda en RECHAZADA.
- [ ] 5.3 Escribir prueba: "Solicitante intenta aprobar" - verificar retorno 403.
- [ ] 5.4 Escribir prueba: "Solicitante intenta rechazar" - verificar retorno 403.
- [ ] 5.5 Escribir prueba: "Aprobar reserva ya aprobada" - verificar retorno 409.
- [ ] 5.6 Escribir prueba: "Rechazar reserva ya rechazada" - verificar retorno 409.
- [ ] 5.7 Escribir prueba: "Aprobar reserva cancelada" - verificar retorno 409.
- [ ] 5.8 Escribir prueba: "Rechazo sin motivo" - verificar retorno 422.
- [ ] 5.9 Escribir prueba: "Rechazo con motivo vacío o solo espacios" - verificar retorno 422.
- [ ] 5.10 Escribir prueba: "Rechazo con motivo excesivo" - verificar retorno 422 (máximo 500 caracteres).
- [ ] 5.11 Escribir prueba: "Rechazo con motivo válido" - verificar responde 200 y reserva queda en RECHAZADA.
- [ ] 5.12 Escribir prueba: "Aprobar sin motivo" - verificar responde 200 y reserva queda en APROBADA.
- [ ] 5.13 Escribir prueba: "Registro de aprobación" - verificar decidido_por, decidido_en, motivo_decision puede ser nulo.
- [ ] 5.14 Escribir prueba: "Registro de rechazo" - verificar decidido_por, decidido_en, motivo proporcionado.
- [ ] 5.15 Escribir prueba: "Aprobar sin conflictos" - verificar responde 200 y reserva queda en APROBADA.
- [ ] 5.16 Escribir prueba: "Aprobar con conflicto" - insertar reserva solapada directamente en BD; verificar retorna 409 y reserva permanece en PENDIENTE sin cambios.
- [ ] 5.17 Escribir prueba: "Aprobar reserva inexistente" - verificar retorno 404.
- [ ] 5.18 Escribir prueba: "Rechazar reserva inexistente" - verificar retorno 404.
- [ ] 5.19 Escribir prueba: "Aprobar reserva con inicio ya pasado" - verificar retorna 409 y reserva permanece en PENDIENTE sin cambios.
- [ ] 5.20 Escribir prueba: "Orden de validaciones cuando hay varios errores" - verificar retorno según orden 401, 403, 404, 422, 409.
- [ ] 5.21 Escribir prueba: "Aprobar mediante endpoint" - POST /reservas/{id}/aprobar sin motivo o con motivo nulo, verificar responde 200 y reserva queda en APROBADA.
- [ ] 5.22 Escribir prueba: "Rechazar mediante endpoint" - POST /reservas/{id}/rechazar con motivo en el cuerpo, verificar responde 200 y reserva queda en RECHAZADA.
- [ ] 5.23 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
