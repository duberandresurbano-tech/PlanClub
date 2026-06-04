import os
from flask import Flask
from app.models import db

def create_app():
    # -------------------------------------------------------------------------
    # Bloque de Rutas para conectar tu estructura real de carpetas
    # Subimos un nivel fuera de 'backend' para encontrar 'vista' e 'index.html'
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Crea la instancia principal apuntando a tus carpetas reales sin moverlas
    app = Flask(
        __name__, 
        instance_relative_config=True,
        template_folder=root_path,          # Aquí encuentra tu index.html raíz
        static_folder=os.path.join(root_path, 'vista') # Aquí encuentra tus estilos, js e img
    )
    # -------------------------------------------------------------------------
    
    # Configuración de la base de datos SQLite local
    # Se guardará automáticamente dentro de la carpeta 'instance'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'planclub.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'tu_llave_secreta_para_los_tokens_del_bar'

    # Inicializa la base de datos con la configuración de la app
    db.init_app(app)

    # Registra las rutas del backend (las manejaremos en routes.py)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Bloque mágico: Crea el archivo .db con todas tus tablas si no existe
    with app.app_context():
        db.create_all()

    return app