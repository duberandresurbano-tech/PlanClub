from flask import Blueprint, jsonify, request, render_template
from app.models import db, Usuario, Rol, Mesa, Reserva
from datetime import datetime

# 🛠️ CORREGIDO: Cambiamos 'bp' por 'main' para que coincida con tus url_for del HTML
main = Blueprint('main', __name__)

# RUTA RAÍZ
@main.route('/')
def index():
    return render_template('html/index.html')

# 2. RUTAS DE NAVEGACIÓN (URLs limpias con @main.route)
@main.route('/inicio')
def inicio():
    return render_template('html/inicio.html')

@main.route('/catalogo')
def catalogo():
    return render_template('html/catalogo.html')

@main.route('/login')
def login_page():
    return render_template('html/login.html')

@main.route('/chat')
def chat():
    return render_template('html/chat.html')

@main.route('/perfil')
def perfil():
    return render_template('html/perfil.html')

@main.route('/reserva')
def reserva():
    return render_template('html/reserva.html')




# RUTA DE REGISTRO REAL - Guarda en base de datos SQLite
@main.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()
        
        # Verificar si el rol "Cliente" existe, si no, crearlo
        rol_cliente = Rol.query.filter_by(id_rol="ROL001").first()
        if not rol_cliente:
            rol_cliente = Rol(id_rol="ROL001", nombre="Cliente")
            db.session.add(rol_cliente)
            db.session.commit()
        
        # Generar ID único basado en el nombre de usuario
        import random
        id_usuario = f"U{random.randint(1000, 9999)}"
        
        # Convertir fecha de string a objeto date
        fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
        
        nuevo_usuario = Usuario(
            id_usuario=id_usuario,
            nombre=data['nombre'],
            apellido=data['apellido'],
            correo=data['correo'],
            celular=data['celular'],
            fecha_nacimiento=fecha_nacimiento,
            contrasena=data['contrasena'],
            estado="Activa",
            id_rol="ROL001"  # Por defecto rol de cliente
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            "mensaje": "¡Registro exitoso! Bienvenido a PlanClub.",
            "id_usuario": id_usuario
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# RUTA DE LOGIN REAL - Verifica contra base de datos
@main.route('/api/login', methods=['POST'])
def login_api():
    try:
        data = request.get_json()
        
        usuario = Usuario.query.filter_by(correo=data['correo']).first()
        
        if usuario and usuario.contrasena == data['contrasena']:
            return jsonify({
                "mensaje": "Login exitoso",
                "usuario": usuario.nombre,
                "id_usuario": usuario.id_usuario,
                "celular": usuario.celular,
                "apellido": usuario.apellido
            }), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# RUTAS PARA MESAS
# ==========================================

# Ruta para inicializar las mesas específicas en la base de datos
@main.route('/api/inicializar-mesas', methods=['POST'])
def inicializar_mesas():
    try:
        # Verificar si ya existen mesas
        mesas_existentes = Mesa.query.count()
        if mesas_existentes > 0:
            return jsonify({
                "mensaje": f"Ya existen {mesas_existentes} mesas en la base de datos. Elimínalas primero si quieres reiniciar.",
                "mesas_actuales": mesas_existentes
            }), 200
        
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
        
        return jsonify({
            "mensaje": "Mesas inicializadas exitosamente",
            "cantidad": len(mesas_datos),
            "detalle": [
                {"id": m["id_mesa"], "nombre": f"M-{m['numero']}", "capacidad": m["capacidad"], "zona": m["zona"]}
                for m in mesas_datos
            ]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Ruta para obtener todas las mesas disponibles
@main.route('/api/mesas', methods=['GET'])
def obtener_mesas():
    try:
        mesas = Mesa.query.filter_by(estado='Disponible').all()
        
        mesas_json = []
        for mesa in mesas:
            mesas_json.append({
                "id_mesa": mesa.id_mesa,
                "nombre": f"M-{mesa.numero}",
                "numero": mesa.numero,
                "capacidad": mesa.capacidad,
                "zona": mesa.zona,
                "estado": mesa.estado
            })
        
        return jsonify({
            "mesas": mesas_json,
            "cantidad": len(mesas_json)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para obtener todas las mesas (incluyendo no disponibles)
@main.route('/api/mesas/todas', methods=['GET'])
def obtener_todas_mesas():
    try:
        mesas = Mesa.query.all()
        
        mesas_json = []
        for mesa in mesas:
            mesas_json.append({
                "id_mesa": mesa.id_mesa,
                "nombre": f"M-{mesa.numero}",
                "numero": mesa.numero,
                "capacidad": mesa.capacidad,
                "zona": mesa.zona,
                "estado": mesa.estado
            })
        
        return jsonify({
            "mesas": mesas_json,
            "cantidad": len(mesas_json)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para eliminar todas las mesas (para reinicializar)
@main.route('/api/mesas/eliminar', methods=['DELETE'])
def eliminar_mesas():
    try:
        Mesa.query.delete()
        db.session.commit()
        
        return jsonify({
            "mensaje": "Todas las mesas han sido eliminadas"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ==========================================
# RUTAS PARA RESERVAS
# ==========================================

# Ruta de diagnóstico para verificar el estado del sistema
@main.route('/api/diagnostico', methods=['GET'])
def diagnostico():
    try:
        # Verificar mesas
        mesas_count = Mesa.query.count()
        mesas = Mesa.query.all()
        
        # Verificar usuarios
        usuarios_count = Usuario.query.count()
        usuarios = Usuario.query.all()
        
        # Verificar reservas
        reservas_count = Reserva.query.count()
        reservas = Reserva.query.all()
        
        return jsonify({
            "estado": "Sistema funcionando",
            "mesas": {
                "total": mesas_count,
                "detalle": [{"id": m.id_mesa, "numero": m.numero, "estado": m.estado} for m in mesas]
            },
            "usuarios": {
                "total": usuarios_count,
                "detalle": [{"id": u.id_usuario, "nombre": u.nombre, "correo": u.correo} for u in usuarios]
            },
            "reservas": {
                "total": reservas_count,
                "detalle": [{"id": r.id_reserva, "id_usuario": r.id_usuario, "id_mesa": r.id_mesa, "estado": r.estado} for r in reservas]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta de prueba para crear reserva automáticamente
@main.route('/api/test-reserva', methods=['POST'])
def test_reserva():
    try:
        # Buscar o crear usuario de prueba
        usuario_test = Usuario.query.filter_by(correo="test@test.com").first()
        if not usuario_test:
            # Crear usuario de prueba
            import random
            id_usuario = f"U{random.randint(10000, 99999)}"
            
            # Verificar si el rol "Cliente" existe
            rol_cliente = Rol.query.filter_by(id_rol="ROL001").first()
            if not rol_cliente:
                rol_cliente = Rol(id_rol="ROL001", nombre="Cliente")
                db.session.add(rol_cliente)
                db.session.commit()
            
            usuario_test = Usuario(
                id_usuario=id_usuario,
                nombre="Usuario",
                apellido="Test",
                correo="test@test.com",
                celular="1234567890",
                fecha_nacimiento=datetime.now().date(),
                contrasena="test123",
                estado="Activa",
                id_rol="ROL001"
            )
            db.session.add(usuario_test)
            db.session.commit()
            print(f"✅ Usuario de prueba creado: {id_usuario}")
        
        # Buscar mesa disponible
        mesa_disponible = Mesa.query.filter_by(estado='Disponible').first()
        if not mesa_disponible:
            return jsonify({"error": "No hay mesas disponibles"}), 400
        
        # Fecha futura para la reserva
        from datetime import timedelta
        fecha_reserva = datetime.now() + timedelta(days=1)
        fecha_str = fecha_reserva.strftime('%Y-%m-%d %H:%M')
        
        # Crear datos de reserva
        data = {
            'id_usuario': usuario_test.id_usuario,
            'id_mesa': mesa_disponible.id_mesa,
            'fecha': fecha_str,
            'cantidad_personas': 2
        }
        
        print(f"📥 Datos de prueba: {data}")
        
        # Llamar a la función de crear reserva
        return crear_reserva_con_datos(data)
        
    except Exception as e:
        print(f"❌ Error en test: {str(e)}")
        return jsonify({"error": str(e)}), 500


def crear_reserva_con_datos(data):
    """Función auxiliar para crear reserva con datos específicos"""
    try:
        id_usuario = data.get('id_usuario')
        id_mesa = data.get('id_mesa')
        fecha = data.get('fecha')
        cantidad_personas = data.get('cantidad_personas')
        
        # Verificar que el usuario existe
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Verificar que la mesa existe y está disponible
        mesa = Mesa.query.filter_by(id_mesa=id_mesa).first()
        if not mesa:
            return jsonify({"error": "Mesa no encontrada"}), 404
        
        if mesa.estado != 'Disponible':
            return jsonify({"error": "La mesa no está disponible"}), 400
        
        # Convertir fecha
        fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
        
        # Generar ID de reserva
        import random
        id_reserva = f"R{random.randint(1000, 9999)}"
        
        # Crear reserva
        nueva_reserva = Reserva(
            id_reserva=id_reserva,
            id_usuario=id_usuario,
            id_mesa=id_mesa,
            fecha=fecha_reserva,
            estado='Pendiente',
            cantidad_personas=cantidad_personas
        )
        
        # Actualizar estado de la mesa
        mesa.estado = 'Reservada'
        
        db.session.add(nueva_reserva)
        db.session.commit()
        
        print(f"✅ Reserva creada: {id_reserva}")
        
        return jsonify({
            "mensaje": "Reserva de prueba creada exitosamente",
            "id_reserva": id_reserva,
            "id_usuario": id_usuario,
            "nombre_usuario": usuario.nombre,
            "mesa": f"M-{mesa.numero}",
            "fecha": fecha
        }), 201
        
    except Exception as e:
        print(f"❌ Error al crear reserva: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Ruta para crear una nueva reserva (solo usuarios registrados)
@main.route('/api/reservas', methods=['POST'])
def crear_reserva():
    try:
        data = request.get_json()
        print(f"📥 Datos recibidos: {data}")  # Debug
        
        # Validar campos requeridos
        id_usuario = data.get('id_usuario')
        id_mesa = data.get('id_mesa')
        fecha = data.get('fecha')
        cantidad_personas = data.get('cantidad_personas')
        
        if not id_usuario:
            return jsonify({"error": "ID de usuario es requerido"}), 400
        if not id_mesa:
            return jsonify({"error": "ID de mesa es requerido"}), 400
        if not fecha:
            return jsonify({"error": "Fecha de reserva es requerida"}), 400
        if not cantidad_personas:
            return jsonify({"error": "Cantidad de personas es requerida"}), 400
        
        # Verificar que el usuario existe (debe estar registrado en la base de datos)
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        if not usuario:
            print(f"❌ Usuario no encontrado: {id_usuario}")  # Debug
            return jsonify({"error": "Usuario no encontrado. Debe estar registrado para hacer reservas."}), 404
        
        print(f"✅ Usuario encontrado: {usuario.nombre}")  # Debug
        
        # Verificar que la mesa existe y está disponible
        mesa = Mesa.query.filter_by(id_mesa=id_mesa).first()
        if not mesa:
            print(f"❌ Mesa no encontrada: {id_mesa}")  # Debug
            return jsonify({"error": "Mesa no encontrada"}), 404
        
        print(f"✅ Mesa encontrada: M-{mesa.numero}, Estado: {mesa.estado}")  # Debug
        
        if mesa.estado != 'Disponible':
            return jsonify({"error": "La mesa no está disponible"}), 400
        
        # Validar que la cantidad de personas no exceda la capacidad de la mesa
        if cantidad_personas > mesa.capacidad:
            return jsonify({
                "error": f"La mesa tiene capacidad para {mesa.capacidad} personas, pero solicitaste {cantidad_personas}"
            }), 400
        
        # Convertir fecha de string a datetime
        try:
            fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD HH:MM"}), 400
        
        # Validar que la fecha sea futura
        if fecha_reserva < datetime.now():
            return jsonify({"error": "La fecha de reserva debe ser futura"}), 400
        
        # Generar ID único para la reserva
        import random
        id_reserva = f"R{random.randint(1000, 9999)}"
        
        print(f"🔄 Creando reserva ID: {id_reserva}")  # Debug
        
        # Crear la reserva
        nueva_reserva = Reserva(
            id_reserva=id_reserva,
            id_usuario=id_usuario,
            id_mesa=id_mesa,
            fecha=fecha_reserva,
            estado='Pendiente',
            cantidad_personas=cantidad_personas
        )
        
        # Actualizar estado de la mesa
        mesa.estado = 'Reservada'
        
        db.session.add(nueva_reserva)
        db.session.commit()
        
        print(f"✅ Reserva creada exitosamente")  # Debug
        
        return jsonify({
            "mensaje": "Reserva creada exitosamente",
            "id_reserva": id_reserva,
            "id_usuario": id_usuario,
            "nombre_usuario": usuario.nombre,
            "mesa": f"M-{mesa.numero}",
            "fecha": fecha
        }), 201
        
    except Exception as e:
        print(f"❌ Error al crear reserva: {str(e)}")  # Debug
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Ruta para obtener reservas de un usuario
@main.route('/api/reservas/usuario/<id_usuario>', methods=['GET'])
def obtener_reservas_usuario(id_usuario):
    try:
        reservas = Reserva.query.filter_by(id_usuario=id_usuario).all()
        
        reservas_json = []
        for reserva in reservas:
            mesa = Mesa.query.get(reserva.id_mesa)
            reservas_json.append({
                "id_reserva": reserva.id_reserva,
                "id_mesa": reserva.id_mesa,
                "nombre_mesa": f"M-{mesa.numero}" if mesa else "N/A",
                "zona": mesa.zona if mesa else "N/A",
                "fecha": reserva.fecha.strftime('%Y-%m-%d %H:%M'),
                "estado": reserva.estado,
                "cantidad_personas": reserva.cantidad_personas
            })
        
        return jsonify({
            "reservas": reservas_json,
            "cantidad": len(reservas_json)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para cancelar una reserva
@main.route('/api/reservas/cancelar/<id_reserva>', methods=['PUT'])
def cancelar_reserva(id_reserva):
    try:
        reserva = Reserva.query.filter_by(id_reserva=id_reserva).first()
        if not reserva:
            return jsonify({"error": "Reserva no encontrada"}), 404
        
        # Actualizar estado de la reserva
        reserva.estado = 'Cancelada'
        
        # Liberar la mesa
        mesa = Mesa.query.get(reserva.id_mesa)
        if mesa:
            mesa.estado = 'Disponible'
        
        db.session.commit()
        
        return jsonify({
            "mensaje": "Reserva cancelada exitosamente",
            "id_reserva": id_reserva
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
