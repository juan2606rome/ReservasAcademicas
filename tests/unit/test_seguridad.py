from src.app.nucleo import seguridad


def test_hash_diferente_al_texto_plano():
    contraseña = "Password123"
    hash_pwd = seguridad.hash_contraseña(contraseña)
    assert hash_pwd != contraseña
    assert seguridad.verificar_contraseña(contraseña, hash_pwd) is True
    assert seguridad.verificar_contraseña("OtraClave123", hash_pwd) is False
