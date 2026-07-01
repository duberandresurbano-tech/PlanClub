import os
from flask import Flask
from datetime import date
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.menu import MenuLink

from app.models import db, Usuario, Mesa, Rol, Permisos, Producto

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)


def create_app():
    app = Flask(__name__, template_folder='templates')

    entorno = os.environ.get('FLASK_ENV', 'development')
    from app.config import config_map
    app.config.from_object(config_map.get(entorno, config_map['default']))

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login_page'

    # ── Panel Admin ───────────────────────────────────────────────────────────
    from app.admin_views import VistaProtegidaAdmin, UsuarioAdminView

    admin = Admin(app, name='👑 Panel Administrativo PlanClub', url='/admin')

    admin.add_view(UsuarioAdminView(Usuario,  db.session, name='Usuarios',  endpoint='usuarios_admin'))
    admin.add_view(VistaProtegidaAdmin(Rol,      db.session, name='Roles'))
    admin.add_view(VistaProtegidaAdmin(Permisos, db.session, name='Permisos'))
    admin.add_view(VistaProtegidaAdmin(Producto, db.session, name='Catálogo'))
    admin.add_view(VistaProtegidaAdmin(Mesa,     db.session, name='Mesas'))
    admin.add_link(MenuLink(name='🏠 Volver a PlanClub', url='/inicio'))

    # ── Blueprints ────────────────────────────────────────────────────────────
    from app.routes import main as main_bp
    app.register_blueprint(main_bp)

    # ── Seed ─────────────────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_roles()
        _seed_superadmin()
        _seed_mesas()

    return app


def _seed_roles():
    from app.models import Rol
    if Rol.query.count() == 0:
        db.session.add_all([
            Rol(id_rol='R1', nombre='Cliente'),
            Rol(id_rol='R2', nombre='Vendedor'),
            Rol(id_rol='R3', nombre='Administrador'),
        ])
        db.session.commit()
        print("✅ Roles creados")


def _seed_superadmin():
    from app.models import Usuario
    if not Usuario.query.filter_by(correo='admin@planclub.com').first():
        db.session.add(Usuario(
            id_usuario='SA001',
            nombre='Super',
            apellido='Admin',
            correo='admin@planclub.com',
            celular='0000000000',
            fecha_nacimiento=date(2000, 1, 1),
            contrasena='admin123',
            estado='Activa',
            id_rol='R3'
        ))
        db.session.commit()
        print("👑 Superadmin creado: admin@planclub.com / admin123")


def _seed_mesas():
    from app.models import Mesa
    if Mesa.query.count() == 0:
        mesas = [
            {"id_mesa": "1",  "numero": 1,  "capacidad": 8, "zona": "VIP",           "estado": "Disponible"},
            {"id_mesa": "2",  "numero": 2,  "capacidad": 8, "zona": "VIP",           "estado": "Disponible"},
            {"id_mesa": "3",  "numero": 3,  "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
            {"id_mesa": "4",  "numero": 4,  "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
            {"id_mesa": "5",  "numero": 5,  "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
            {"id_mesa": "6",  "numero": 6,  "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
            {"id_mesa": "7",  "numero": 7,  "capacidad": 4, "zona": "Fondo",         "estado": "Disponible"},
            {"id_mesa": "8",  "numero": 8,  "capacidad": 4, "zona": "Fondo",         "estado": "Disponible"},
            {"id_mesa": "9",  "numero": 9,  "capacidad": 4, "zona": "Fondo",         "estado": "Disponible"},
            {"id_mesa": "10", "numero": 10, "capacidad": 4, "zona": "Fondo",         "estado": "Disponible"},
        ]
        for m in mesas:
            db.session.add(Mesa(**m))
        db.session.commit()
        print(f"✅ {len(mesas)} mesas creadas")
