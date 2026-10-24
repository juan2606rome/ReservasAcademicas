# Sistema de Gestión de Reservas de Espacios Académicos

API REST para gestionar la reserva de laboratorios, auditorios y salas de cómputo de una institución universitaria. Centraliza las solicitudes (que antes se hacían por correo y hojas de cálculo), evita conflictos de horario y guarda el historial de cada reserva.

Autor: Juan Sandón

Proyecto desarrollado con **Spec-Driven Development (SDD)** usando **OpenSpec** y un agente de IA de programación. Primero se escribió un plan de ingeniería, luego las especificaciones, y después el código y las pruebas.

> Las partes marcadas con **(AJUSTAR)** deben verificarse contra el código final antes de entregar.

## Funcionalidades

- Registro e inicio de sesión de usuarios con token JWT.
- Roles: `ADMINISTRADOR` y `SOLICITANTE`, con permisos por rol.
- Administración de usuarios (activar y desactivar) por el administrador.
- Gestión de espacios: crear, listar, consultar, editar, desactivar y reactivar.
- Solicitudes de reserva con validación de fechas y de disponibilidad.
- Prevención de reservas solapadas, incluso con solicitudes simultáneas.
- Aprobación y rechazo de solicitudes por el administrador.
- Cancelación de reservas e historial de cambios de estado.
- Consulta de disponibilidad por espacio y fecha.

## Reglas de negocio principales

- Una reserva puede estar en estado `PENDIENTE`, `APROBADA`, `RECHAZADA` o `CANCELADA`.
- Las reservas `PENDIENTE` y `APROBADA` **ocupan** el espacio; las `RECHAZADA` y `CANCELADA` lo liberan.
- Los intervalos son `[inicio, fin)`: una reserva que termina a las 10:00 no choca con otra que empieza a las 10:00.
- Una reserva debe empezar y terminar el mismo día (hora de Bogotá), con fechas en formato ISO 8601 con zona horaria.
- Todo registro de usuario crea un `SOLICITANTE`. El primer administrador se crea con un script.
- Rechazar una solicitud exige un motivo.
- Duración máxima de una reserva: 4 horas consecutivas por usuario *(mantener esta línea solo si el cambio de las 4 horas ya está implementado)*.

```
PENDIENTE → APROBADA → CANCELADA
PENDIENTE → RECHAZADA
PENDIENTE → CANCELADA
```

## Tecnologías

- Python 3.12 o superior **(AJUSTAR a la versión usada)**
- FastAPI
- SQLite (módulo `sqlite3` de Python, SQL escrito a mano)
- JWT y bcrypt para autenticación y contraseñas
- pytest para las pruebas

## Instalación (Windows)

1. Clona el repositorio y entra a la carpeta:

```
git clone https://github.com/juan2606rome/ReservasAcademicas.git
cd ReservasAcademicas
```

2. Crea y activa un entorno virtual:

```
python -m venv .venv
.venv\Scripts\activate
```

3. Instala las dependencias:

```
pip install -r requirements.txt
```

## Configuración

Las claves nunca están en el código; se definen como variables de entorno.

| Variable | Para qué sirve | ¿Obligatoria? |
|---|---|---|
| `JWT_SECRET` | Clave con la que se firman los tokens | Sí |
| `ADMIN_NOMBRE` | Nombre del primer administrador | Solo para el script seed |
| `ADMIN_CORREO` | Correo del primer administrador | Solo para el script seed |
| `ADMIN_PASSWORD` | Contraseña del primer administrador (8 a 72 caracteres) | Solo para el script seed |

En la terminal de Windows (cmd), por ejemplo:

```
set JWT_SECRET=cambia-esta-clave-por-una-larga
set ADMIN_NOMBRE=Administrador
set ADMIN_CORREO=admin@ejemplo.com
set ADMIN_PASSWORD=ClaveSegura123
```

## Crear el primer administrador

```
python -m scripts.seed
```
**(AJUSTAR: usar la ruta real del script seed.)** Si el correo ya existe, el script no crea otro usuario.

## Ejecutar la aplicación

```
uvicorn src.app.main:app --reload
```
**(AJUSTAR: usar el módulo real de arranque.)**

La documentación interactiva (Swagger) queda en `http://127.0.0.1:8000/docs`. Desde ahí puedes iniciar sesión y usar el botón **Authorize** con el token.

## Ejecutar las pruebas

```
pytest
```

## Endpoints principales

| Módulo | Endpoint | Quién puede |
|---|---|---|
| Usuarios | `POST /usuarios/registro` | Público |
| Usuarios | `POST /usuarios/login` | Público |
| Usuarios | `GET /usuarios/yo` | Cualquier usuario autenticado |
| Usuarios | `GET /usuarios`, `GET /usuarios/{id}` | Administrador |
| Usuarios | `PATCH /usuarios/{id}/desactivar`, `PATCH /usuarios/{id}/activar` | Administrador |
| Espacios | `GET /espacios`, `GET /espacios/{id}` | Cualquier usuario autenticado |
| Espacios | `POST /espacios`, `PUT /espacios/{id}` | Administrador |
| Espacios | `PATCH /espacios/{id}/desactivar`, `PATCH /espacios/{id}/activar` | Administrador |
| Reservas | `POST /reservas/solicitudes` | Cualquier usuario autenticado |
| Reservas | `GET /reservas/disponibilidad?espacio_id=...&fecha=AAAA-MM-DD` | Cualquier usuario autenticado |
| Reservas | `GET /reservas`, `GET /reservas/{id}` | Solicitante (las suyas) y administrador (todas) |
| Reservas | `POST /reservas/{id}/aprobar`, `POST /reservas/{id}/rechazar` | Administrador |
| Reservas | `POST /reservas/{id}/cancelar` | Dueño de la reserva o administrador |
| Historial | `GET /historial` | Solicitante (el suyo) y administrador (todo) |

**(AJUSTAR: comprobar cada ruta con `/docs`.)**

## Códigos de respuesta

| Código | Significado |
|---|---|
| 200 / 201 | Operación exitosa / recurso creado |
| 401 | Sin token, token inválido o vencido |
| 403 | Sin permiso para esa acción |
| 404 | El recurso no existe |
| 409 | Los datos son válidos pero chocan con el estado actual (por ejemplo, solapamiento) |
| 422 | Datos mal formados o incompletos |

## Estructura del proyecto

```
.
├── PLAN_INGENIERIA.md        # plan de ingeniería (anterior a las especificaciones)
├── INFORME_FINAL.md          # resultados, dificultades y conclusiones
├── REGISTRO_REVISION.md      # revisión de las especificaciones
├── README.md
├── openspec/                 # especificaciones, cambios y su archivo
├── src/app/                  # código (módulos: usuarios, autorizacion, espacios, reservas, ...)
├── tests/                    # pruebas automatizadas
└── requirements.txt
```
**(AJUSTAR a la estructura real.)**

## Proceso de desarrollo (SDD)

1. `PLAN_INGENIERIA.md`: análisis, arquitectura, riesgos y estrategia.
2. Especificaciones en `openspec/`: un cambio por funcionalidad, cada una con requisitos y escenarios verificables.
3. Revisión de las especificaciones antes de programar (`REGISTRO_REVISION.md`).
4. Implementación con un agente de IA, revisada por el autor, con pruebas por escenario.
5. Gestión de cambios: la regla de duración máxima se incorporó como un cambio nuevo de OpenSpec.
6. Verificación y cierre (`INFORME_FINAL.md`).

El historial de Git (`git log --oneline`) muestra esta secuencia.
