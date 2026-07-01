from flask_login import login_user, logout_user, current_user
from app.models import Usuario, Rol
from datetime import datetime
import random


# =========================================
# USUARIO ACTUAL
# =========================================

def get_current_user():
    """
    Devuelve el usuario actual desde la base de datos
    (si está autenticado)
    """
    if not current_user.is_authenticated:
        return None

    return Usuario.query.filter_by(
        id_usuario=current_user.get_id()
    ).first()


# =========================================
# VALIDACIÓN DE ESTADO
# =========================================

def is_user_active(user=None):
    """
    Verifica si el usuario está activo
    """
    if user is None:
        user = get_current_user()

    return bool(user and user.estado == "Activa")


def ensure_user_active():
    """
    Validación fuerte para rutas críticas
    """
    user = get_current_user()

    if not user:
        return False, "Usuario no autenticado"

    if user.estado != "Activa":
        return False, "Usuario inactivo"

    return True, "OK"


# =========================================
# LOGIN
# =========================================

def authenticate_user(correo, password):
    """
    Login centralizado (ANTES estaba en routes)
    """
    user = Usuario.query.filter_by(correo=correo).first()

    if not user:
        return None, "Usuario no encontrado"

    if user.contrasena != password:
        return None, "Contraseña incorrecta"

    if user.estado != "Activa":
        return None, "Usuario inactivo"

    login_user(user)

    return user, "Login exitoso"


# =========================================
# LOGOUT
# =========================================

def logout_current_user():
    """
    Logout centralizado
    """
    logout_user()


# =========================================
# REGISTRO
# =========================================

def register_user(data):
    """
    Registro centralizado (ANTES estaba en routes)
    """

    rol = Rol.query.filter_by(id_rol="ROL001").first()

    if not rol:
        rol = Rol(id_rol="ROL001", nombre="Cliente")
        db.session.add(rol)
        db.session.commit()

    new_user = Usuario(
        id_usuario=f"U{random.randint(1000, 9999)}",
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo=data['correo'],
        celular=data['celular'],
        fecha_nacimiento=datetime.strptime(
            data['fecha_nacimiento'], '%Y-%m-%d'
        ).date(),
        contrasena=data['contrasena'],
        estado="Activa",
        id_rol="ROL001"
    )

    return new_user