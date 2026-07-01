from flask_login import current_user
from app.models import Usuario


def get_db_user():
    """
    Obtiene el usuario real desde la BD usando el session id
    """
    if not current_user.is_authenticated:
        return None

    return Usuario.query.filter_by(
        id_usuario=current_user.get_id()
    ).first()


def is_request_allowed():
    """
    Regla global de acceso:
    - autenticado
    - existe en BD
    - activo
    """
    user = get_db_user()

    if not user:
        return False, "No autenticado"

    if user.estado != "Activa":
        return False, "Usuario inactivo"

    return True, "OK"


def enforce_active_user():
    """
    Versión estricta para rutas críticas
    """
    user = get_db_user()

    if not user:
        return False, "No autenticado"

    if user.estado != "Activa":
        return False, "Cuenta desactivada"

    return True, user