import os
from flask import Flask
from app.models import db, Mesa
from app.config import config_map


def create_app():
    app = Flask(__name__)

    # Selecciona el entorno según la variable de entorno FLASK_ENV
    # Si no está definida, usa 'development' por defecto
    entorno = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config_map.get(entorno, config_map['default']))

    # Inicializar la extensión de base de datos con la app
    db.init_app(app)

    # 🛠️ CORREGIDO: Importamos 'main' (que es el nombre que le dimos en routes.py)
    from app.routes import main as main_bp
    app.register_blueprint(main_bp)

    # Crear todas las tablas si no existen (útil en desarrollo)
    with app.app_context():
        db.create_all()
        
        # Inicializar mesas automáticamente si no existen
        inicializar_mesas_si_no_existen()

    return app


def inicializar_mesas_si_no_existen():
    """Inicializa las mesas automáticamente si no existen en la base de datos"""
    try:
        # Verificar si ya existen mesas
        mesas_existentes = Mesa.query.count()
        if mesas_existentes == 0:
            print("🔄 Inicializando mesas automáticamente...")
            
            # Datos de las mesas específicas según el requerimiento
            mesas_datos = [
                # Mesas VIP (capacidad 8)
                {"id_mesa": "1", "numero": 1, "capacidad": 8, "zona": "VIP", "estado": "Disponible"},
                {"id_mesa": "2", "numero": 2, "capacidad": 8, "zona": "VIP", "estado": "Disponible"},
                
                # Mesas Zona de baile (capacidad 6)
                {"id_mesa": "3", "numero": 3, "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
                {"id_mesa": "4", "numero": 4, "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
                {"id_mesa": "5", "numero": 5, "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
                {"id_mesa": "6", "numero": 6, "capacidad": 6, "zona": "Zona de baile", "estado": "Disponible"},
                
                # Mesas Fondo (capacidad 4)
                {"id_mesa": "7", "numero": 7, "capacidad": 4, "zona": "Fondo", "estado": "Disponible"},
                {"id_mesa": "8", "numero": 8, "capacidad": 4, "zona": "Fondo", "estado": "Disponible"},
                {"id_mesa": "9", "numero": 9, "capacidad": 4, "zona": "Fondo", "estado": "Disponible"},
                {"id_mesa": "10", "numero": 10, "capacidad": 4, "zona": "Fondo", "estado": "Disponible"},
            ]
            
            # Crear las mesas
            for mesa_data in mesas_datos:
                nueva_mesa = Mesa(**mesa_data)
                db.session.add(nueva_mesa)
            
            db.session.commit()
            print(f"✅ {len(mesas_datos)} mesas inicializadas exitosamente")
        else:
            print(f"ℹ️ Ya existen {mesas_existentes} mesas en la base de datos")
            
    except Exception as e:
        print(f"❌ Error al inicializar mesas: {str(e)}")
        db.session.rollback()
