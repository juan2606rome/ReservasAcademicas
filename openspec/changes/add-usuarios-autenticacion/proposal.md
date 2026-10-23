# Proposal

## Why

The system currently has no user management or authentication mechanism. According to the engineering plan (section 1.2, N4), we need authentication, roles and permissions to control who can do what in the reservation system. As the first building block (stage E1), we need to establish user registration and authentication so that subsequent features (spaces, reservations, approvals) can be properly protected and audited. 

## What Changes

- Add user registration capability allowing users to register with name, unique email, and password
- Add authentication capability allowing users to log in and receive a JWT token
- Implement secure password storage using password hashing
- Enforce business rules: inactive users cannot log in; duplicate emails are rejected with an error

## Capabilities

### New Capabilities
- `usuarios-autenticacion`: User registration and authentication including password hashing, JWT token issuance, and validation rules for uniqueness and account status

### Modified Capabilities
- (none)

## Impact

- **APIs**: New endpoints for user registration and login
- **Database**: New `usuarios` table (or equivalent) to store user accounts with hashed passwords, role, and active status
- **Security**: Password hashing implementation, JWT token generation and validation
- **Dependencies**: JWT library and password hashing library (as per tech stack decisions in plan)
- **Modules**: `usuarios` module as defined in the plan (section 2.3)
