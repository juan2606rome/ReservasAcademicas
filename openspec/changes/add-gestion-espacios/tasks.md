# Tasks

## 1. Base de datos
- [ ] 1.1 Crear/actualizar tabla espacios en schema.sql con campos: id, nombre, tipo, capacidad, activo. Verificar estructura.
- [ ] 1.2 Agregar restricción UNIQUE en nombre. Verificar restricción.
- [ ] 1.3 Agregar validación/check si es posible (tipo en {LABORATORIO,AUDITORIO,SALA_COMPUTO}, capacidad > 0). Verificar restricciones.
- [ ] 1.4 Inicializar tabla espacios. Verificar creación correcta.

## 2. Capa de repositorio (espacios)
- [ ] 2.1 Crear espacios/repository.py con operaciones CRUD usando consultas parametrizadas. Verificar uso de parámetros.
- [ ] 2.2 Implementar creación de espacio con validación de nombre único. Verificar manejo de duplicados.
- [ ] 2.3 Implementar listado de espacios activos (filtro activo=true). Verificar filtrado correcto.
- [ ] 2.4 Implementar consulta de espacio por id. Verificar funcionalidad.
- [ ] 2.5 Implementar edición de espacio. Verificar actualización.
- [ ] 2.6 Implementar desactivación (UPDATE activo=false) en lugar de DELETE. Verificar que no se elimina.
- [ ] 2.7 Manejar violación de UNIQUE y propagar errores. Verificar comportamiento.

## 3. Capa de servicio (espacios)
- [ ] 3.1 Crear espacios/service.py con lógica de negocio. Verificar estructura.
- [ ] 3.2 Validar tipo de espacio (solo LABORATORIO, AUDITORIO, SALA_COMPUTO). Verificar validación.
- [ ] 3.3 Validar capacidad entera mayor que 0. Verificar validación con 422.
- [ ] 3.4 Validar nombre único. Verificar retorno 409 en duplicados.
- [ ] 3.5 Implementar desactivación. Verificar que solo se marca como inactivo.
- [ ] 3.6 Asegurar que listados solo retornan espacios activos. Verificar filtrado.

## 4. Capa de API (espacios)
- [ ] 4.1 Crear espacios/schemas.py con esquemas de petición y respuesta. Verificar validaciones.
- [ ] 4.2 Crear espacios/router.py con endpoints CRUD. Verificar rutas.
- [ ] 4.3 Proteger endpoints con rol ADMINISTRADOR (solo admin crea/edita/desactiva). Verificar autorización.
- [ ] 4.4 Implementar POST para crear espacio (solo admin). Verificar 409 para duplicado, 422 para validación, 403 si no es admin.
- [ ] 4.5 Implementar GET para listar espacios (autenticado). Verificar solo muestra activos.
- [ ] 4.6 Implementar GET para consultar espacio por id. Verificar funcionalidad.
- [ ] 4.7 Implementar PUT/PATCH para editar espacio (solo admin). Verificar validaciones.
- [ ] 4.8 Implementar DELETE o PATCH para desactivar espacio (solo admin). Verificar desactivación, no eliminación.
- [ ] 4.9 Registrar router en aplicación principal. Verificar endpoints accesibles.

## 5. Pruebas
- [ ] 5.1 Escribir prueba: "Tipos válidos" - verificar solo LABORATORIO, AUDITORIO, SALA_COMPUTO. Verificar test pasa.
- [ ] 5.2 Escribir prueba: "Administrador crea espacio" - verificar permitido. Verificar test pasa.
- [ ] 5.3 Escribir prueba: "Solicitante intenta crear espacio" - verificar retorno 403. Verificar test pasa.
- [ ] 5.4 Escribir prueba: "Creación con nombre duplicado" - verificar retorno 409. Verificar test pasa.
- [ ] 5.5 Escribir prueba: "Edición con nombre duplicado" - verificar retorno 409. Verificar test pasa.
- [ ] 5.6 Escribir prueba: "Capacidad inválida" - verificar retorno 422 para 0, negativa, no entera. Verificar test pasa.
- [ ] 5.7 Escribir prueba: "Capacidad válida" - verificar acepta entero mayor que 0. Verificar test pasa.
- [ ] 5.8 Escribir prueba: "Desactivar espacio" - verificar marcado como inactivo, no eliminado. Verificar test pasa.
- [ ] 5.9 Escribir prueba: "Espacio desactivado no aparece en listado normal" - verificar filtrado. Verificar test pasa.
- [ ] 5.10 Escribir prueba: "Espacio desactivado no acepta reservas" - verificar comportamiento. Verificar test pasa.
- [ ] 5.11 Escribir prueba: "Listar espacios" - verificar solo activos. Verificar test pasa.
- [ ] 5.12 Escribir prueba: "Consultar espacio" - verificar funcionalidad. Verificar test pasa.
- [ ] 5.13 Escribir prueba: "Editar espacio" - verificar actualización con datos válidos. Verificar test pasa.
- [ ] 5.14 Ejecutar toda la suite de pruebas y verificar que todas pasan. Verificar cobertura de todos los escenarios de la especificación.
