# Tasks

## 1. Base de datos
- [x] 1.1 Agregar columnas decidido_por, decidido_en y motivo_decision a schema.sql en esta etapa (no "agregar si faltan"). Verificar estructura.
- [x] 1.2 Asegurar tipos correctos para trazabilidad. Verificar campos.

## 2. Capa de repositorio (aprobacion)
- [x] 2.1 Crear aprobacion/repository.py con operaciones para aprobar/rechazar. Verificar consultas parametrizadas.
- [x] 2.2 Implementar búsqueda de reserva por id. Verificar funcionalidad.
- [x] 2.3 Implementar actualización de estado con trazabilidad. Verificar actualización.
- [x] 2.4 Reutilizar lógica de verificación de solapamientos (excluyendo la propia reserva). Verificar integración.

## 3. Capa de servicio (aprobacion)
- [x] 3.1 Crear aprobacion/service.py con lógica de aprobación y rechazo. Verificar estructura.
- [x] 3.2 Aplicar orden de validaciones: 401, 403, 404, 422, 409. Verificar orden.
- [x] 3.3 Validar existencia de reserva. Verificar retorno 404.
- [x] 3.4 Validar que sea rol ADMINISTRADOR. Verificar retorno 403.
- [x] 3.5 Validar estado PENDIENTE. Verificar retorno 409 para otros estados.
- [x] 3.6 Validar motivo al rechazar: obligatorio, no vacío ni solo espacios, máximo 500 caracteres. Verificar retorno 422. Motivo opcional al aprobar (puede ser nulo).
- [x] 3.7 Validar que no se apruebe si el inicio ya pasó. Verificar retorno 409.
- [x] 3.8 Registrar decidido_por, decidido_en, motivo_decision. Verificar trazabilidad.
- [x] 3.9 Revalidar disponibilidad al aprobar, excluyendo la propia reserva. Por decisión D6, solo conflicto por inconsistencia de datos. Verificar detección de conflictos (prueba con reserva solapada insertada directamente en BD).
- [x] 3.10 Realizar operaciones en transacción con BEGIN IMMEDIATE. Verificar atomicidad.

## 4. Capa de API (aprobacion)
- [x] 4.1 Crear aprobacion/router.py con endpoints para aprobar y rechazar. Verificar rutas.
- [x] 4.2 Proteger endpoints con rol ADMINISTRADOR. Verificar autorización.
- [x] 4.3 Implementar POST /reservas/{id}/aprobar (motivo opcional en cuerpo). Verificar códigos HTTP (200 al aprobar, deja en APROBADA).
- [x] 4.4 Implementar POST /reservas/{id}/rechazar (motivo obligatorio en cuerpo). Verificar códigos HTTP (200 al rechazar, deja en RECHAZADA).
- [x] 4.5 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 5. Pruebas
- [x] 5.1 Escribir prueba: "Administrador aprueba reserva" - verificar responde 200 y reserva queda en APROBADA.
- [x] 5.2 Escribir prueba: "Administrador rechaza reserva" - verificar responde 200 y reserva queda en RECHAZADA.
- [x] 5.3 Escribir prueba: "Solicitante intenta aprobar" - verificar retorno 403.
- [x] 5.4 Escribir prueba: "Solicitante intenta rechazar" - verificar retorno 403.
- [x] 5.5 Escribir prueba: "Aprobar reserva ya aprobada" - verificar retorno 409.
- [x] 5.6 Escribir prueba: "Rechazar reserva ya rechazada" - verificar retorno 409.
- [x] 5.7 Escribir prueba: "Aprobar reserva cancelada" - verificar retorno 409.
- [x] 5.8 Escribir prueba: "Rechazo sin motivo" - verificar retorno 422.
- [x] 5.9 Escribir prueba: "Rechazo con motivo vacío o solo espacios" - verificar retorno 422.
- [x] 5.10 Escribir prueba: "Rechazo con motivo excesivo" - verificar retorno 422 (máximo 500 caracteres).
- [x] 5.11 Escribir prueba: "Rechazo con motivo válido" - verificar responde 200 y reserva queda en RECHAZADA.
- [x] 5.12 Escribir prueba: "Aprobar sin motivo" - verificar responde 200 y reserva queda en APROBADA.
- [x] 5.13 Escribir prueba: "Registro de aprobación" - verificar decidido_por, decidido_en, motivo_decision puede ser nulo.
- [x] 5.14 Escribir prueba: "Registro de rechazo" - verificar decidido_por, decidido_en, motivo proporcionado.
- [x] 5.15 Escribir prueba: "Aprobar sin conflictos" - verificar responde 200 y reserva queda en APROBADA.
- [x] 5.16 Escribir prueba: "Aprobar con conflicto" - insertar reserva solapada directamente en BD; verificar retorna 409 y reserva permanece en PENDIENTE sin cambios.
- [x] 5.17 Escribir prueba: "Aprobar reserva inexistente" - verificar retorno 404.
- [x] 5.18 Escribir prueba: "Rechazar reserva inexistente" - verificar retorno 404.
- [x] 5.19 Escribir prueba: "Aprobar reserva con inicio ya pasado" - verificar retorna 409 y reserva permanece en PENDIENTE sin cambios.
- [x] 5.20 Escribir prueba: "Solicitante intenta aprobar una reserva inexistente" - verificar retorno 403 (no 404).
- [x] 5.21 Escribir prueba: "Administrador rechaza una reserva inexistente sin motivo" - verificar retorno 404 (no 422).
- [x] 5.22 Escribir prueba: "Administrador rechaza una reserva ya APROBADA sin motivo" - verificar retorno 422 (no 409).
- [x] 5.23 Escribir prueba: "Aprobar mediante endpoint" - POST /reservas/{id}/aprobar sin motivo o con motivo nulo, verificar responde 200 y reserva queda en APROBADA.
- [x] 5.24 Escribir prueba: "Rechazar mediante endpoint" - POST /reservas/{id}/rechazar con motivo en el cuerpo, verificar responde 200 y reserva queda en RECHAZADA.
- [x] 5.25 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
