# Design

## Context

See proposal.md - Why. This is stage E1 of the engineering plan. We need to establish user authentication as the foundation for all subsequent features (roles/permissions, spaces, reservations). The tech stack is FastAPI with SQLite, JWT for auth, and bcrypt for password hashing (as per section 3.2 of the plan).

## Goals / Non-Goals

**Goals:**
- Implement user registration with name, unique email, password
- Implement login that returns JWT token
- Store passwords securely using hashing
- Prevent inactive users from logging in
- Return appropriate errors for duplicate emails

**Non-Goals:**
- Role-based authorization details (that's stage E2 - add-roles-permisos)
- Password reset/recovery
- Email verification
- OAuth/social login
- User profile management beyond registration

## Decisions

### Decision: Use FastAPI with modular structure
- **Choice**: Follow the modular architecture defined in plan (section 3.4) - create `usuarios/` module with router, service, repository, models, schemas
- **Rationale**: Consistent with project structure, allows separation of concerns, testable
- **Alternatives considered**: Putting everything in main.py - rejected for maintainability

### Decision: Password hashing with bcrypt
- **Choice**: Use bcrypt for password hashing
- **Rationale**: Industry standard, secure, specified in tech stack (section 3.2)
- **Alternatives considered**: Argon2, PBKDF2 - bcrypt is simpler and meets requirements

### Decision: JWT for authentication tokens
- **Choice**: Use JWT tokens for stateless authentication
- **Rationale**: API is RESTful and consumable from any client (section 3.5 D4)
- **Alternatives considered**: Session cookies - rejected as less suitable for API consumption

### Decision: SQLite with direct SQL (sqlite3)
- **Choice**: Use sqlite3 module with parameterized queries
- **Rationale**: No server needed, matches plan (section 3.2), SQL visible for security
- **Alternatives considered**: ORM like SQLAlchemy - rejected to keep it simple and visible

### Decision: User model structure
- **Choice**: Store id, nombre (name), correo (email), hash_contraseña, rol, activo (active status)
- **Rationale**: Matches entities defined in plan (section 3.3)
- **Alternatives considered**: Different field naming - using Spanish names as per project style

### Decision: Email uniqueness enforcement
- **Choice**: Enforce uniqueness at database level (UNIQUE constraint) and also validate in application
- **Rationale**: Defense in depth, prevents race conditions
- **Alternatives considered**: Application-only validation - rejected as not sufficient

## Risks / Trade-offs

- **[Security] Plain text passwords** → Mitigation: Always hash with bcrypt before storing, never log passwords
- **[Security] JWT secret management** → Mitigation: Use environment variable for JWT secret, not hardcoded
- **[Data integrity] Duplicate emails** → Mitigation: UNIQUE constraint on email column plus application validation
- **[Auth bypass] Inactive users** → Mitigation: Check active status on every login attempt
- **[SQL Injection]** → Mitigation: Use parameterized queries everywhere
- **[Token security]** → Mitigation: Use appropriate expiration time, secure secret
