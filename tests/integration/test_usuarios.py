import os
import tempfile
from fastapi.testclient import TestClient


# Setup env
os.environ["JWT_SECRET"] = "test-secret-key"


def test_registro_exitoso():
    # Usar BD temporal
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    response = client.post("/usuarios/registro", json={
        "nombre": "Juan Perez",
        "correo": "juan@example.com",
        "contraseña": "Password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["rol"] == "SOLICITANTE"
    assert data["activo"] is True
    assert "contraseña" not in data
    assert "hash_contraseña" not in data
    
    os.close(db_fd)


def test_registro_correo_duplicado():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    payload = {"nombre": "Juan", "correo": "test@example.com", "contraseña": "Password123"}
    r1 = client.post("/usuarios/registro", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/usuarios/registro", json=payload)
    assert r2.status_code == 409
    
    os.close(db_fd)


def test_registro_ignora_rol():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    response = client.post("/usuarios/registro", json={
        "nombre": "Maria",
        "correo": "maria@example.com",
        "contraseña": "Password123",
        "rol": "ADMINISTRADOR"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["rol"] == "SOLICITANTE"
    
    os.close(db_fd)


def test_registro_datos_invalidos():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    # correo invalido
    r = client.post("/usuarios/registro", json={"nombre": "Juan", "correo": "invalido", "contraseña": "Password123"})
    assert r.status_code == 422
    # contraseña corta
    r = client.post("/usuarios/registro", json={"nombre": "Juan", "correo": "a@b.com", "contraseña": "1234567"})
    assert r.status_code == 422
    # contraseña larga
    r = client.post("/usuarios/registro", json={"nombre": "Juan", "correo": "b@c.com", "contraseña": "a"*73})
    assert r.status_code == 422
    # nombre vacio
    r = client.post("/usuarios/registro", json={"nombre": "", "correo": "c@d.com", "contraseña": "Password123"})
    assert r.status_code == 422
    
    os.close(db_fd)


def test_login_exitoso():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    client.post("/usuarios/registro", json={"nombre": "Juan", "correo": "juan@example.com", "contraseña": "Password123"})
    response = client.post("/usuarios/login", json={"correo": "juan@example.com", "contraseña": "Password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verificar token
    import jwt
    payload = jwt.decode(data["access_token"], os.environ["JWT_SECRET"], algorithms=["HS256"])
    assert "id" in payload
    assert "rol" in payload
    assert payload["rol"] == "SOLICITANTE"
    
    os.close(db_fd)


def test_login_contraseña_incorrecta():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    client.post("/usuarios/registro", json={"nombre": "Juan", "correo": "juan@example.com", "contraseña": "Password123"})
    response = client.post("/usuarios/login", json={"correo": "juan@example.com", "contraseña": "WrongPass123"})
    assert response.status_code == 401
    
    os.close(db_fd)


def test_login_correo_no_registrado():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    response = client.post("/usuarios/login", json={"correo": "noexiste@example.com", "contraseña": "Password123"})
    assert response.status_code == 401
    
    os.close(db_fd)


def test_login_cuenta_inactiva():
    import src.app.nucleo.conexion as conexion
    from src.app.nucleo.conexion import get_connection
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    client.post("/usuarios/registro", json={"nombre": "Juan", "correo": "juan@example.com", "contraseña": "Password123"})
    # Desactivar usuario
    conn = get_connection()
    conn.execute("UPDATE usuarios SET activo = 0 WHERE correo = 'juan@example.com'")
    conn.commit()
    conn.close()
    
    response = client.post("/usuarios/login", json={"correo": "juan@example.com", "contraseña": "Password123"})
    assert response.status_code == 403
    
    os.close(db_fd)


def test_login_datos_invalidos():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    
    from src.app.main import app
    client = TestClient(app)
    
    r = client.post("/usuarios/login", json={"correo": "invalido", "contraseña": "Password123"})
    assert r.status_code == 422
    r = client.post("/usuarios/login", json={"correo": "a@b.com"})  # falta contraseña
    assert r.status_code == 422
    
    os.close(db_fd)
