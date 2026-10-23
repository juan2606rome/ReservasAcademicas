# Tasks

## 1. Base de datos
- [ ] 1.1 Crear/actualizar tabla espacios en schema.sql con campos: id, nombre, tipo, capacidad, activo. Verificar estructura.
- [ ] 1.2 Agregar restricción UNIQUE en nombre (considerando normalización en aplicación). Verificar restricción.
- [ ] 1.3 Agregar validación/check si es posible (tipo en {LABORATORIO,AUDITORIO,SALA_COMPUTO}, capacidad > 0). Verificar restricciones.
- [ ] 1.4 Inicializar tabla espacios. Verificar creación correcta.

## 2. Capa de repositorio (espacios)
- [ ] 2.1 Crear espacios/repository.py con operaciones CRUD usando consultas parametrizadas. Verificar uso de parámetros.
- [ ] 2.2 Implementar creación de espacio con validación de nombre único sin distinguir mayúsculas ni espacios al inicio o al final. Verificar manejo de duplicados.
- [ ] 2.3 Implementar listado de espacios activos por defecto (filtro activo=true). Verificar filtrado correcto.
- [ ] 2.4 Implementar listado con opción de incluir inactivos para administrador. Verificar funcionalidad.
- [ ] 2.5 Implementar consulta de espacio por id. Verificar funcionalidad.
- [ ] 2.6 Implementar edición de espacio. Verificar actualización.
- [ ] 2.7 Implementar desactivación (UPDATE activo=false) mediante PATCH /espacios/{id}/desactivar. Verificar que no se elimina.
- [ ] 2.8 Implementar activación (UPDATE activo=true) mediante PATCH /espacios/{id}/activar. Verificar funcionalidad.
- [ ] 2.9 Manejar violación de UNIQUE y propagar errores. Verificar comportamiento.

## 3. Capa de servicio (espacios)
- [ ] 3.1 Crear espacios/service.py con lógica de negocio. Verificar estructura.
- [ ] 3.2 Validar tipo de espacio (solo LABORATORIO, AUDITORIO, SALA_COMPUTO). Verificar retorno 422 para tipo inválido.
- [ ] 3.3 Validar nombre vacío o solo espacios. Verificar retorno 422.
- [ ] 3.4 Validar nombre único sin distinguir mayúsculas ni espacios al inicio o al final. Verificar retorno 409 en duplicados.
- [ ] 3.5 Validar capacidad entera mayor que 0. Verificar validación con 422.
- [ ] 3.6 Implementar desactivación. Verificar que solo se marca como inactivo y permite desactivar con reservas futuras PENDIENTE o APROBADA sin modificarlas.
- [ ] 3.7 Implementar activación. Verificar que solo se marca como activo.
- [ ] 3.8 Asegurar que listados por defecto solo retornan espacios activos. Verificar filtrado.
- [ ] 3.9 Implementar lógica de consulta por id: administrador recibe 200 para inactivo, solicitante recibe 404 para inactivo. Verificar comportamiento.
- [ ] 3.10 Retornar 404 al consultar, editar, activar o desactivar un espacio inexistente. Verificar comportamiento.

## 4. Capa de API (espacios)
- [ ] 4.1 Crear espacios/schemas.py con esquemas de petición y respuesta. Verificar validaciones.
- [ ] 4.2 Crear espacios/router.py con endpoints CRUD. Verificar rutas.
- [ ] 4.3 Proteger endpoints con rol ADMINISTRADOR para crear, editar, activar y desactivar (403 para SOLICITANTE). Verificar autorización.
- [ ] 4.4 Permitir listar y consultar a cualquier usuario autenticado. Verificar autorización.
- [ ] 4.5 Implementar POST /espacios (solo admin). Verificar 201 al crear, 409 para duplicado, 422 para validación (tipo inválido, nombre vacío, capacidad inválida), 403 si no es admin.
- [ ] 4.6 Implementar GET /espacios (autenticado). Verificar por defecto solo activos con 200; administrador puede usar ?incluir_inactivos=true.
- [ ] 4.7 Implementar GET /espacios/{id} (autenticado). Verificar 200 para activo, 200 para inactivo si es administrador, 404 para inactivo si es solicitante, 404 si no existe.
- [ ] 4.8 Implementar PUT /espacios/{id} (solo admin). Verificar 200 al editar, 409 para duplicado, 422 para validación, 403 si no es admin, 404 si no existe.
- [ ] 4.9 Implementar PATCH /espacios/{id}/desactivar (solo admin). Verificar 200 al desactivar, 403 si no es admin, 404 si no existe.
- [ ] 4.10 Implementar PATCH /espacios/{id}/activar (solo admin). Verificar 200 al activar, 403 si no es admin, 404 si no existe.
- [ ] 4.11 Nunca implementar DELETE. Verificar ausencia de endpoint DELETE.
- [ ] 4.12 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 5. Pruebas
- [ ] 5.1 Escribir prueba: "Tipos válidos" - verificar acepta LABORATORIO, AUDITORIO, SALA_COMPUTO. Verificar test pasa.
- [ ] 5.2 Escribir prueba: "Tipo inválido" - verificar retorno 422 para tipo inválido. Verificar test pasa.
- [ ] 5.3 Escribir prueba: "Administrador crea espacio" - verificar permitido con 201. Verificar test pasa.
- [ ] 5.4 Escribir prueba: "Solicitante intenta crear espacio" - verificar retorno 403. Verificar test pasa.
- [ ] 5.5 Escribir prueba: "Solicitante intenta editar espacio" - verificar retorno 403. Verificar test pasa.
- [ ] 5.6 Escribir prueba: "Solicitante intenta desactivar espacio" - verificar retorno 403. Verificar test pasa.
- [ ] 5.7 Escribir prueba: "Solicitante intenta activar espacio" - verificar retorno 403. Verificar test pasa.
- [ ] 5.8 Escribir prueba: "Usuario autenticado lista espacios" - verificar permitido. Verificar test pasa.
- [ ] 5.9 Escribir prueba: "Usuario autenticado consulta espacio" - verificar permitido. Verificar test pasa.
- [ ] 5.10 Escribir prueba: "Creación con nombre duplicado" - verificar retorno 409 ignorando mayúsculas y espacios al inicio o al final. Verificar test pasa.
- [ ] 5.11 Escribir prueba: "Edición con nombre duplicado" - verificar retorno 409 ignorando mayúsculas y espacios al inicio o al final. Verificar test pasa.
- [ ] 5.12 Escribir prueba: "Nombre vacío" - verificar retorno 422 para nombre vacío o solo espacios. Verificar test pasa.
- [ ] 5.13 Escribir prueba: "Capacidad inválida" - verificar retorno 422 para 0, negativa o no entera. Verificar test pasa.
- [ ] 5.14 Escribir prueba: "Capacidad válida" - verificar acepta entero mayor que 0. Verificar test pasa.
- [ ] 5.15 Escribir prueba: "Desactivar espacio" - verificar marcado como inactivo, no eliminado, retorna 200. Verificar test pasa.
- [ ] 5.16 Escribir prueba: "Activar espacio" - verificar marcado como activo, retorna 200. Verificar test pasa.
- [ ] 5.17 Escribir prueba: "Desactivar espacio con reservas futuras PENDIENTE o APROBADA" - verificar permite desactivar, no modifica esas reservas, solo impide reservas nuevas. Verificar test pasa.
- [ ] 5.18 Escribir prueba: "Listar espacios por defecto" - verificar retorna únicamente espacios activos con 200. Verificar test pasa.
- [ ] 5.19 Escribir prueba: "Listar espacios incluyendo inactivos" - verificar administrador puede usar ?incluir_inactivos=true y recibe todos con 200. Verificar test pasa.
- [ ] 5.20 Escribir prueba: "Consultar espacio activo" - verificar retorna 200. Verificar test pasa.
- [ ] 5.21 Escribir prueba: "Consultar espacio inactivo como administrador" - verificar retorna 200. Verificar test pasa.
- [ ] 5.22 Escribir prueba: "Consultar espacio inactivo como solicitante" - verificar retorna 404. Verificar test pasa.
- [ ] 5.23 Escribir prueba: "Consultar espacio inexistente" - verificar retorna 404. Verificar test pasa.
- [ ] 5.24 Escribir prueba: "Editar espacio inexistente" - verificar retorna 404. Verificar test pasa.
- [ ] 5.25 Escribir prueba: "Desactivar espacio inexistente" - verificar retorna 404. Verificar test pasa.
- [ ] 5.26 Escribir prueba: "Activar espacio inexistente" - verificar retorna 404. Verificar test pasa.
- [ ] 5.27 Escribir prueba: "Crear espacio" - verificar retorna 201. Verificar test pasa.
- [ ] 5.28 Escribir prueba: "Listar espacios" - verificar retorna 200. Verificar test pasa.
- [ ] 5.29 Escribir prueba: "Consultar espacio" - verificar retorna 200. Verificar test pasa.
- [ ] 5.30 Escribir prueba: "Editar espacio" - verificar retorna 200. Verificar test pasa.
- [ ] 5.31 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
