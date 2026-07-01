from app.models import db, Usuario, Rol
import random

SUPERADMIN_EMAIL = 'admin@planclub.com'


def es_admin(usuario) -> bool:
    """El usuario está autenticado y tiene rol R3."""
    return usuario.is_authenticated and getattr(usuario, 'id_rol', None) == 'R3'


def es_superadmin(usuario) -> bool:
    """El usuario es el superadmin oculto."""
    return usuario.is_authenticated and getattr(usuario, 'correo', '') == SUPERADMIN_EMAIL


def query_usuarios_visibles(query, usuario_actual):
    """
    Filtra el queryset de usuarios:
    - Superadmin ve a todos.
    - Otros admins NO ven al superadmin.
    """
    if not es_superadmin(usuario_actual):
        query = query.filter(Usuario.correo != SUPERADMIN_EMAIL)
    return query


def puede_editar_usuario(model, usuario_actual) -> bool:
    if model.correo == SUPERADMIN_EMAIL and not es_superadmin(usuario_actual):
        return False
    return True


def puede_eliminar_usuario(model) -> bool:
    """Nadie puede eliminar al superadmin."""
    return model.correo != SUPERADMIN_EMAIL


def asignar_rol(model, form, is_created: bool):
    """Mapea el objeto Rol seleccionado al campo id_rol del modelo."""

    # Si es un usuario nuevo, generar ID automáticamente
    if is_created and not model.id_usuario:
        model.id_usuario = f"U{random.randint(1000, 9999)}"

    if not model.estado:
        model.estado = 'Activa'

    if hasattr(form, 'rol') and form.rol.data:
        model.id_rol = form.rol.data.id_rol
    elif is_created:
        model.id_rol = 'R1'
