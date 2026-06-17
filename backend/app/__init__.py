import os
from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Flask buscará automáticamente en la carpeta 'templates' y 'static' 
    # que estén al mismo nivel de este archivo __init__.py
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'planclub.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'tu_llave_secreta'

    db.init_app(app)

    # 🛠️ CORREGIDO: Importamos 'main' (que es el nombre que le dimos en routes.py)
    from app.routes import main as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app