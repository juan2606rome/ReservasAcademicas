# Registro de revisión de especificaciones

Autor: Juan Sandón

## Cómo se revisó

Con cada `/opsx-propose` el agente generó propuesta, diseño, especificación y tareas. Yo las leí, las comparé con `PLAN_INGENIERIA.md` y con el enunciado, pedí las correcciones con `/opsx-update` y guardé en Git dos commits por cambio: uno con la versión generada ("crear") y otro con la revisada ("revisar"). La diferencia entre los dos es la evidencia de la revisión.

Criterios usados: contradice el plan, ambiguo, falta algo, no se puede probar, seguridad, consistencia.

## Hallazgos por cambio

### add-usuarios-autenticacion
- Todo estaba en inglés, mientras el plan está en español.
- Los errores no tenían código HTTP (no se podían probar).
- Faltaban los casos de contraseña incorrecta y correo no registrado.
- Un usuario podría registrarse como administrador: se definió que el registro siempre crea SOLICITANTE.
- Faltaban validaciones de datos (correo, contraseña de 8 a 72 caracteres, nombre).
- El token JWT no tenía contenido ni vencimiento definidos (ahora: id, rol, 60 minutos).
- Ninguna tarea creaba la estructura base del proyecto.

### add-roles-permisos
- Se probaban permisos de endpoints que todavía no existían: cada etapa verifica los suyos.
- No había administración de usuarios (pedida en el enunciado) ni forma de desactivar un usuario.
- Un usuario desactivado conservaba su token: ahora se consulta al usuario en cada petición.
- El primer administrador se crea con un script y variables de entorno (sin contraseñas en el código).

### add-gestion-espacios
- Contradicción: un requisito decía que listar era solo del administrador y los escenarios decían "cualquier usuario autenticado".
- Faltaban errores 422 (tipo y nombre inválidos) y 404 (espacio inexistente).
- Nombre único sin distinguir mayúsculas ni espacios al inicio o al final.
- Se agregó reactivar y se definió qué pasa al desactivar un espacio con reservas futuras.

### add-solicitud-reservas
- Las fechas no definían zona horaria: "mismo día" se evalúa en hora de Bogotá.
- El usuario de la solicitud sale del token, nunca del cuerpo de la petición.
- El solapamiento se compara solo dentro del mismo espacio, y una solicitud PENDIENTE contra otra PENDIENTE se solapa (decisión D6 del plan).
- La disponibilidad no tenía parámetros ni respuesta definidos.
- Faltaba la consulta de reservas (propias y de todos), que los roles daban por hecha.

### add-aprobacion-reservas
- "Aprobar con conflicto" era ambiguo: ahora responde 409 y la reserva sigue PENDIENTE.
- La revalidación debe excluir la propia reserva, si no siempre chocaría consigo misma.
- Por la decisión D6, ese conflicto solo ocurre por una inconsistencia de datos: es una validación defensiva.
- Se definieron los estados resultantes, cuándo el motivo es obligatorio y que no se aprueba una reserva cuyo inicio ya pasó.

### add-cancelacion-historial
- Faltaban 404 al cancelar una reserva inexistente y los códigos de éxito.
- Se definió el contenido del historial (estado anterior NULL al crear, comentarios por defecto).
- El cambio de estado y su registro en el historial van en la misma transacción.
- Los filtros de fecha, estado y espacio no estaban definidos.

## Revisión global (Fase 2)

Se pidió al agente una revisión de solo lectura de los seis cambios contra el plan y el enunciado. Resultado:

- No hay contradicciones entre cambios (solo observaciones de severidad baja que resultaron coherentes).
- Los ocho requisitos mínimos del enunciado tienen especificación.
- Todos los escenarios tienen una tarea de prueba.

Observaciones:

- Algunos escenarios necesitan preparar la situación a mano en las pruebas: token vencido, usuario borrado con token válido, conflicto al aprobar (se inserta una reserva solapada directo en la base de datos) y fallo al escribir el historial (se simula un error en la inserción).
- "ISO 8601 con zona horaria" se entiende como `Z` o un desplazamiento `±hh:mm`; una fecha sin zona horaria se rechaza con 422.
- La zona horaria de Bogotá es fija (UTC-5, sin horario de verano), tal como dice el plan.
- El cambio de la regla de duración (E7 del plan) todavía no existe porque corresponde a la Fase 4, después de implementar los seis cambios.

## Diferencias respecto al plan

| Plan | Resultado | Motivo |
|---|---|---|
| Capacidades: usuarios, autorizacion, espacios, reservas, disponibilidad, aprobacion | usuarios-autenticacion, roles-permisos, gestion-espacios, solicitud-reservas (incluye disponibilidad), aprobacion-reservas, cancelacion-historial | OpenSpec propuso los nombres por cambio; la disponibilidad se agrupó con las solicitudes porque comparten el solapamiento |
| Cancelación e historial dentro de `reservas` | Módulos `cancelacion` e `historial` | Responsabilidades distintas |
| Sin consulta de reservas ni administración de usuarios entre las funcionalidades | Agregadas | Detectadas como faltantes al revisar |
| Zona horaria: supuesto S4 | El día se evalúa en hora de Bogotá | Evita errores en reservas nocturnas |
| Módulo `politicas` independiente (sección 2.3) | Archivo `reservas/politicas.py` dentro del módulo de reservas | Las reglas de reserva solo se usan allí; sigue siendo el lugar único donde se agregará la regla de duración |

## Mejoras pendientes (conocidas)

- `openspec validate` avisa que algunos requisitos son largos (más de 500 caracteres). Se dejaron así por tiempo; lo ideal es dividirlos en requisitos más cortos.
- *(Agregar aquí cualquier otro detalle que decidas no corregir.)*
