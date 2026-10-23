# Tasks

## 1. Database Setup
- [ ] 1.1 Create users table schema with fields: id, nombre, correo (unique), hash_contraseña, rol, activo. Verify schema matches entities in plan section 3.3.
- [ ] 1.2 Add UNIQUE constraint on correo and ensure proper data types. Verify constraint is in place.
- [ ] 1.3 Update schema.sql to include users table. Verify schema.sql is updated correctly.

## 2. User Repository Layer
- [ ] 2.1 Create usuarios/repository.py with functions to create user and find user by email. Verify parameterized queries are used.
- [ ] 2.2 Implement function to check if email exists. Verify returns boolean correctly.
- [ ] 2.3 Add proper error handling for database operations. Verify no SQL injection vulnerabilities.

## 3. Password Hashing
- [ ] 3.1 Set up bcrypt for password hashing. Verify bcrypt is imported and configured.
- [ ] 3.2 Implement password hashing function. Verify hashed passwords are different from plain text.
- [ ] 3.3 Implement password verification function. Verify correct passwords validate successfully.

## 4. User Service Layer
- [ ] 4.1 Create usuarios/service.py with user registration logic. Verify duplicate email returns error.
- [ ] 4.2 Implement login logic with password verification and active user check. Verify inactive users cannot login.
- [ ] 4.3 Implement JWT token generation. Verify token is returned on successful login.
- [ ] 4.4 Ensure passwords are hashed before storage. Verify no plain text passwords stored.

## 5. API Endpoints
- [ ] 5.1 Create usuarios/router.py with POST /usuarios/registro endpoint. Verify endpoint accepts name, email, password.
- [ ] 5.2 Create POST /usuarios/login endpoint. Verify returns JWT token on success.
- [ ] 5.3 Add proper request/response schemas in usuarios/schemas.py. Verify validation works correctly.
- [ ] 5.4 Add appropriate HTTP status codes for errors (duplicate email, inactive user). Verify error responses are correct.

## 6. Testing
- [ ] 6.1 Write unit tests for password hashing and verification. Verify all hashing tests pass.
- [ ] 6.2 Write integration tests for user registration. Verify successful registration and duplicate email cases.
- [ ] 6.3 Write integration tests for login. Verify successful login returns token, inactive user rejected.
- [ ] 6.4 Write tests to verify passwords are stored hashed. Verify no plain text in database.
- [ ] 6.5 Run all tests and verify they pass. Verify test coverage for all scenarios in spec.
