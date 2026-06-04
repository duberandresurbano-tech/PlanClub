from flask import Blueprint, jsonify, request, render_template
from app.models import db, Usuario

bp = Blueprint('main', __name__)

# 1. RUTA RAÍZ: Ahora sí va a renderizar tu index.html original de la raíz
@bp.route('/')
def index():
    # Flask buscará index.html usando el puente que configuramos en el __init__.py
    return render_template('index.html')

# 2. RUTAS PARA TUS OTRAS VISTAS (Dentro de vista/html/)
@bp.route('/inicio')
def inicio():
    return render_template('vista/html/inicio.html')

@bp.route('/catalogo')
def catalogo():
    return render_template('vista/html/catalogo.html')

@bp.route('/login')
def login():
    return render_template('vista/html/login.html')

@bp.route('/chat')
def chat():
    return render_template('vista/html/chat.html')

@bp.route('/perfil')
def perfil():
    return render_template('vista/html/perfil.html')

@bp.route('/reserva')
def reserva():
    return render_template('vista/html/reserva.html')


# 3. RUTA DE PRUEBA: Mantenemos intacta tu ruta para meter el usuario a la DB
@bp.route('/crear-usuario-prueba', methods=['GET'])
def crear_usuario():
    try:
        # Creamos un registro con la estructura de tu modelo
        nuevo_usuario = Usuario(
            id_usuario="101010",
            nombre="Juan",
            apellido="Perez",
            correo="juan@planclub.com",
            contrasena="clave123",
            estado="activo",
            verificacion="completada"
        )
        
        # Le decimos a la base de datos que guarde el registro
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({"mensaje": "¡Primer usuario guardado con éxito en SQLite!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500