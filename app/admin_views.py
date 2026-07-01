from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash

from app.services.admin_service import (
    es_admin,
    query_usuarios_visibles,
    puede_eliminar_usuario,
    asignar_rol,
)


class VistaProtegidaAdmin(ModelView):
    # Desactiva joinedload automático que rompe SQLite con PKs personalizadas
    column_auto_select_related = False

    def is_accessible(self):
        return es_admin(current_user)

    def inaccessible_callback(self, name, **kwargs):
        flash("Acceso denegado. Se requieren permisos de administrador.", "danger")
        return redirect(url_for('main.login_page'))

    def get_query(self):
        return super().get_query()

    def get_count_query(self):
        return super().get_count_query()


class UsuarioAdminView(VistaProtegidaAdmin):

    column_list = [
        'id_usuario', 'nombre', 'apellido',
        'correo', 'celular', 'estado', 'id_rol'
    ]

    form_columns = [
        'nombre', 'apellido', 'correo', 'celular',
        'fecha_nacimiento', 'contrasena', 'estado', 'rol'
    ]

    def get_query(self):
        query = super().get_query()
        return query_usuarios_visibles(query, current_user)

    def get_count_query(self):
        query = super().get_count_query()
        return query_usuarios_visibles(query, current_user)

    def can_delete_model(self, model):
        return puede_eliminar_usuario(model)

    def on_model_change(self, form, model, is_created):
        asignar_rol(model, form, is_created)
