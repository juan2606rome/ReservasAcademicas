# Script seed para crear primer administrador

Para crear el primer usuario administrador, ejecutar:

`ash
export ADMIN_NOMBRE=\"Nombre Admin\"
export ADMIN_CORREO=\"admin@example.com\"
export ADMIN_PASSWORD=\"Password123\"
python scripts/seed_admin.py
`

O en Windows:
`ash
set ADMIN_NOMBRE=Nombre Admin
set ADMIN_CORREO=admin@example.com
set ADMIN_PASSWORD=Password123
python scripts/seed_admin.py
`

El script leerá las credenciales desde las variables de entorno, nunca desde el código.
Si el correo ya existe, no creará otro usuario ni modificará el existente.
Si faltan alguna de las variables, terminará con mensaje de error.
