from datetime import datetime
import random

from app.models import db, Usuario, Rol


# =========================
# REGISTRO DE USUARIO
# =========================

def registrar_usuario(data):
    """
    Crea un usuario nuevo de forma segura.
    Devuelve (response_dict, status_code)
    """

    try:
        # -------------------------
        # Validación básica
        # -------------------------
        required_fields = ["nombre", "apellido", "correo", "celular", "fecha_nacimiento", "contrasena"]

        for field in required_fields:
            if not data.get(field):
                return {"error": f"Falta el campo {field}"}, 400

        # -------------------------
        # Verificar si ya existe
        # -------------------------
        existing_user = Usuario.query.filter_by(correo=data["correo"]).first()
        if existing_user:
            return {"error": "El correo ya está registrado"}, 409

        # -------------------------
        # Asegurar rol Cliente
        # -------------------------
        rol_cliente = Rol.query.filter_by(id_rol="ROL001").first()

        if not rol_cliente:
            rol_cliente = Rol(id_rol="ROL001", nombre="Cliente")
            db.session.add(rol_cliente)
            db.session.commit()

        # -------------------------
        # Generar ID usuario
        # -------------------------
        id_usuario = f"U{random.randint(1000, 9999)}"

        # Evitar colisión de ID
        while Usuario.query.filter_by(id_usuario=id_usuario).first():
            id_usuario = f"U{random.randint(1000, 9999)}"

        # -------------------------
        # Convertir fecha
        # -------------------------
        try:
            fecha_nacimiento = datetime.strptime(
                data["fecha_nacimiento"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return {"error": "Formato de fecha inválido (YYYY-MM-DD)"}, 400

        # -------------------------
        # Crear usuario
        # -------------------------
        nuevo_usuario = Usuario(
            id_usuario=id_usuario,
            nombre=data["nombre"],
            apellido=data["apellido"],
            correo=data["correo"],
            celular=data["celular"],
            fecha_nacimiento=fecha_nacimiento,
            contrasena=data["contrasena"],
            estado="Activa",
            id_rol="ROL001"
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return {
            "mensaje": "Usuario registrado correctamente",
            "id_usuario": id_usuario
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# =========================
# OBTENER USUARIO POR ID
# (útil para reservas/login futuro)
# =========================

def get_user_by_id(id_usuario):
    return Usuario.query.filter_by(id_usuario=id_usuario).first()


# =========================
# OBTENER USUARIO POR CORREO
# =========================

def get_user_by_email(correo):
    return Usuario.query.filter_by(correo=correo).first()


# =========================
# VALIDAR USUARIO ACTIVO
# =========================

def is_user_active(user):
    if not user:
        return False
    return user.estado == "Activa"


# =========================
# CAMBIAR ESTADO USUARIO
# (IMPORTANTE PARA TU PROBLEMA DE BLOQUEO)
# =========================

def set_user_status(id_usuario, estado):
    """
    Activa o desactiva usuario.
    """
    try:
        user = get_user_by_id(id_usuario)

        if not user:
            return {"error": "Usuario no encontrado"}, 404

        user.estado = estado
        db.session.commit()

        return {
            "mensaje": f"Usuario actualizado a {estado}",
            "id_usuario": id_usuario
        }, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500