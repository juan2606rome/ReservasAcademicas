# Design

## Context

Ver proposal.md - Why. Esta es la etapa E1 del plan de ingeniería. Es necesario establecer la autenticación de usuarios como base para todas las funcionalidades posteriores (roles/permisos, espacios, reservas). El stack tecnológico es FastAPI con SQLite, JWT para autenticación y bcrypt para hash de contraseñas (sección 3.2 del plan).

## Goals / Non-Goals

**Objetivos:**
- Implementar registro de usuarios con nombre, correo único, contraseña
- Implementar inicio de sesión que retorne token JWT
- Almacenar contraseñas de forma segura con hash
- Prevenir inicio de sesión de usuarios inactivos
- Retornar códigos HTTP correctos para cada tipo de error
- Aplicar todas las validaciones y reglas especificadas

**No objetivos:**
- Detalles de autorización por roles (etapa E2 - add-roles-permisos)
- Recuperación o restablecimiento de contraseña
- Verificación de correo electrónico
- Autenticación OAuth/social
- Gestión de perfil más allá del registro

## Decisions

### Decisión: Usar FastAPI con estructura modular
- **Elección**: Seguir la arquitectura modular definida en el plan (sección 3.4) - crear módulo `usuarios/` con router, service, repository, models, schemas
- **Justificación**: Consistente con la estructura del proyecto, permite separación de responsabilidades y facilita las pruebas
- **Alternativas consideradas**: Todo en main.py - rechazado por mantenibilidad

### Decisión: Hash de contraseñas con bcrypt
- **Elección**: Usar bcrypt para el hash de contraseñas
- **Justificación**: Estándar de la industria, seguro, especificado en el stack tecnológico
- **Alternativas consideradas**: Argon2, PBKDF2 - bcrypt es suficiente y cumple con los requisitos

### Decisión: JWT para tokens de autenticación
- **Elección**: Usar tokens JWT para autenticación sin estado
- **Justificación**: API REST consumible desde cualquier cliente (sección 3.5 D4). El token debe contener id, rol y expiración de 60 minutos. JWT_SECRET debe provenir de variable de entorno
- **Alternativas consideradas**: Cookies de sesión - rechazadas por menor idoneidad para consumo de API

### Decisión: SQLite con SQL directo (sqlite3)
- **Elección**: Usar módulo sqlite3 con consultas parametrizadas
- **Justificación**: Sin necesidad de servidor, coincide con el plan (sección 3.2), SQL visible para revisión de seguridad
- **Alternativas consideradas**: ORM como SQLAlchemy - rechazado para mantener simplicidad y visibilidad

### Decisión: Estructura del modelo de usuario
- **Elección**: Almacenar id, nombre, correo, hash_contraseña, rol, activo
- **Justificación**: Coincide con las entidades definidas en el plan (sección 3.3)
- **Alternativas consideradas**: Diferentes nombres de campos - se usan nombres en español según estilo del proyecto

### Decisión: Unicidad de correo
- **Elección**: Aplicar restricción UNIQUE a nivel de base de datos y validación a nivel de aplicación. El correo se guarda en minúsculas y la comparación no distingue mayúsculas/minúsculas
- **Justificación**: Defensa en profundidad. Si la base de datos lanza violación de UNIQUE, el servicio debe responder con código HTTP 409
- **Alternativas consideradas**: Solo validación en aplicación - rechazada por insuficiente

### Decisión: Reglas de registro
- **Elección**: Todo usuario nuevo se crea con rol SOLICITANTE y activo=true. Si la petición trae un rol, se ignora. La respuesta nunca incluye contraseña ni hash
- **Justificación**: Requisito explícito de la especificación
- **Alternativas consideradas**: Permitir asignación de rol en registro - rechazado

### Decisión: Validaciones
- **Elección**: Correo con formato válido, contraseña de 8 a 72 caracteres, nombre no vacío. Errores de validación retornan 422
- **Justificación**: Requisito explícito de la especificación
- **Alternativas consideradas**: Otras reglas de validación - solo estas se especifican

### Decisión: Respuestas de login
- **Elección**: Contraseña incorrecta y correo no registrado deben retornar el mismo mensaje con código 401. Cuenta inactiva retorna 403. Datos inválidos retornan 422
- **Justificación**: Prevención de enumeración de usuarios
- **Alternativas consideradas**: Mensajes diferenciados - rechazado por seguridad

## Risks / Trade-offs

- **[Seguridad] Contraseñas en texto plano** → Mitigación: Siempre hashear con bcrypt antes de almacenar, nunca registrar contraseñas
- **[Seguridad] Gestión del secreto JWT** → Mitigación: Usar variable de entorno JWT_SECRET, nunca hardcodeado
- **[Integridad de datos] Correos duplicados** → Mitigación: Restricción UNIQUE en columna correo + validación en aplicación. Si la BD lanza violación de UNIQUE, el servicio responde 409
- **[Autenticación] Usuarios inactivos** → Mitigación: Verificar estado activo en cada intento de login, retornar 403
- **[Inyección SQL]** → Mitigación: Usar consultas parametrizadas en todas las operaciones
- **[Seguridad de tokens]** → Mitigación: Expiración de 60 minutos, secreto desde variable de entorno
- **[Enumeración de usuarios]** → Mitigación: Mismo mensaje para correo no registrado y contraseña incorrecta (401)

## Open Questions

- **Primer administrador**: El primer administrador se creará en la etapa E2. Aún no está definido el mecanismo exacto para su creación.
