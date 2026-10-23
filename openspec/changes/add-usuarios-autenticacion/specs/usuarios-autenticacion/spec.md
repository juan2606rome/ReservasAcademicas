# Spec Delta

## Purpose

This capability provides user registration and authentication for the academic spaces reservation system. It ensures secure account creation with unique emails, password hashing, JWT-based authentication, and proper access control for inactive accounts.

## ADDED Requirements

### Requirement: User registration with name, unique email and password
The system SHALL allow users to register by providing name, email, and password. The email SHALL be unique across all users.

#### Scenario: Successful user registration
- **WHEN** a user provides valid name, unique email, and password for registration
- **THEN** the system creates the user account with hashed password
- **AND** the system returns success confirmation

#### Scenario: Registration with duplicate email
- **WHEN** a user attempts to register with an email that already exists
- **THEN** the system returns an error indicating the email is already in use

### Requirement: User login returns JWT token
The system SHALL authenticate users with valid credentials and return a JWT token upon successful login.

#### Scenario: Successful login
- **WHEN** a user provides valid credentials for an active account
- **THEN** the system validates the password against the stored hash
- **AND** the system returns a JWT token

### Requirement: Passwords stored with hash
The system SHALL store user passwords using secure password hashing. Passwords SHALL never be stored in plain text.

#### Scenario: Password hashing on registration
- **WHEN** a user registers with a password
- **THEN** the system hashes the password before storing it in the database
- **AND** the plain text password is not stored

### Requirement: Inactive user cannot log in
The system SHALL prevent inactive users from authenticating.

#### Scenario: Inactive user login attempt
- **WHEN** a user with inactive status attempts to log in with valid credentials
- **THEN** the system rejects the login attempt
- **AND** the system returns an error indicating the account is inactive

### Requirement: Duplicate email returns error
The system SHALL reject registration attempts when the email is already registered.

#### Scenario: Duplicate email error on registration
- **WHEN** a registration request contains an email that already exists in the system
- **THEN** the system returns an error response
- **AND** no duplicate user account is created
