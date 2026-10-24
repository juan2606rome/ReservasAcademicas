import os
import tempfile
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone


os.environ["JWT_SECRET"] = "test-secret-key"


def setup_db():
    import src.app.nucleo.conexion as conexion
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    conexion.DB_PATH = db_path
    conexion.init_db()
    return db_fd, db_path


def crear_usuario_admin_y_solicitante():
    from src.app.usuarios import repository as usuarios_repo
    from src.app.nucleo import seguridad
    solicitante = usuarios_repo.crear_usuario("Solicitante", "solicitante@test.com",
                                             seguridad.hash_contraseña("Password123"), "SOLICITANTE", True)
    admin = usuarios_repo.crear_usuario("Admin", "admin@test.com",
                                       seguridad.hash_contraseña("Password123"), "ADMINISTRADOR", True)
    return solicitante, admin


def obtener_token(correo, password="Password123"):
    from src.app.main import app
    client = TestClient(app)
    resp = client.post("/usuarios/login", json={"correo": correo, "contraseña": password})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def crear_espacio():
    from src.app.espacios import repository as espacios_repo
    espacio = espacios_repo.crear_espacio("Lab 1", "LABORATORIO", 30)
    from src.app.nucleo import conexion
    conn = conexion.get_connection()
    conn.execute("UPDATE espacios SET activo = 1 WHERE id = ?", (espacio["id"],))
    conn.commit()
    conn.close()
    return espacio


def crear_reserva_pendiente(espacio_id, usuario_id, inicio_horas_desde_ahora=2):
    from src.app.reservas import repository as reservas_repo
    from src.app.reservas import politicas
    inicio = datetime.now(timezone.utc) + timedelta(hours=inicio_horas_desde_ahora)
    fin = inicio + timedelta(hours=1)
    inicio_str = politicas.formatear_utc_iso8601(inicio)
    fin_str = politicas.formatear_utc_iso8601(fin)
    reserva = reservas_repo.crear_reserva(espacio_id, usuario_id, inicio_str, fin_str, "Clase", estado='PENDIENTE')
    return reserva


def test_solicitante_intenta_aprobar():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("solicitante@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/aprobar', headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403
    finally:
        os.close(db_fd)


def test_solicitante_intenta_rechazar():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("solicitante@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/rechazar', json={"motivo": "x"}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403
    finally:
        os.close(db_fd)


def test_aprobar_reserva_ya_aprobada():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        client.post(f'/reservas/{reserva["id"]}/aprobar', headers={"Authorization": f"Bearer {token}"})
        resp = client.post(f'/reservas/{reserva["id"]}/aprobar', headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 409
    finally:
        os.close(db_fd)


def test_rechazar_reserva_ya_rechazada():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        client.post(f'/reservas/{reserva["id"]}/rechazar', json={"motivo": "x"}, headers={"Authorization": f"Bearer {token}"})
        resp = client.post(f'/reservas/{reserva["id"]}/rechazar', json={"motivo": "x"}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 409
    finally:
        os.close(db_fd)


def test_aprobar_reserva_cancelada():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.nucleo import conexion
        conn = conexion.get_connection()
        conn.execute("UPDATE reservas SET estado='CANCELADA' WHERE id=?", (reserva['id'],))
        conn.commit()
        conn.close()
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/aprobar', headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 409
    finally:
        os.close(db_fd)


def test_rechazo_sin_motivo():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/rechazar', json={}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 422
    finally:
        os.close(db_fd)


def test_rechazo_con_motivo_vacio_o_espacios():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/rechazar', json={"motivo": "   "}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 422
    finally:
        os.close(db_fd)


def test_rechazo_con_motivo_excesivo():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        motivo_largo = "a" * 501
        resp = client.post(f'/reservas/{reserva["id"]}/rechazar', json={"motivo": motivo_largo}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 422
    finally:
        os.close(db_fd)


def test_rechazo_con_motivo_valido():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/rechazar', json={"motivo": "Motivo válido"}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        from src.app.reservas import repository as reservas_repo
        r = reservas_repo.obtener_reserva_por_id(reserva['id'])
        assert r['estado'] == 'RECHAZADA'
    finally:
        os.close(db_fd)


def test_aprobar_sin_motivo():
    db_fd, db_path = setup_db()
    try:
        solicitante, admin = crear_usuario_admin_y_solicitante()
        espacio = crear_espacio()
        reserva = crear_reserva_pendiente(espacio["id"], solicitante["id"])
        from src.app.main import app
        client = TestClient(app)
        token = obtener_token("admin@test.com")
        resp = client.post(f'/reservas/{reserva["id"]}/aprobar', headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        from src.app.reservas import repository as reservas_repo
        r = reservas_repo.obtener_reserva_por_id(reserva['id'])
        assert r['estado'] == 'APROBADA'
    finally:
        os.close(db_fd)
