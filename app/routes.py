from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import re

from app.models import Mesa, Reserva

from app.services.auth_service import authenticate_user

from app.services.reserva_services import (
    crear_reserva,
    cancelar_reserva,
    get_reservas_usuario,
    delete_reservas_usuario
)


from app.services.user_service import registrar_usuario

main = Blueprint('main', __name__)

# =========================
# PÁGINAS
# =========================

@main.route('/')
def index():
    return render_template('html/index.html')

@main.route('/login')
def login_page():
    return render_template('html/inicio.html')

@main.route('/inicio')
@login_required
def inicio():
    return render_template('html/inicio.html')

@main.route('/catalogo')
def catalogo():
    return render_template('html/catalogo.html')

@main.route('/chat')
def chat():
    return render_template('html/chat.html')

@main.route('/perfil')
def perfil():
    return render_template('html/perfil.html')

@main.route('/reserva')
def reserva():
    return render_template('html/reserva.html')


# =========================
# AUTH
# =========================

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/api/login', methods=['POST'])
def login_api():
    try:
        data = request.get_json()

        user, msg = authenticate_user(
            data.get('correo'),
            data.get('contrasena')
        )

        if not user:
            return jsonify({"error": msg}), 401

        login_user(user)

        return jsonify({
            "mensaje": msg,
            "usuario": user.nombre,
            "id_usuario": user.id_usuario,
            "celular": user.celular,
            "apellido": user.apellido
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# REGISTRO (MOVIDO A SERVICE)
# =========================

@main.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()

        result, status = registrar_usuario(data)

        return jsonify(result), status

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# RESERVAS (SOLO LLAMADAS A SERVICE)
# =========================

@main.route('/api/reservas', methods=['POST'])
def api_crear_reserva():
    data = request.get_json()
    return crear_reserva(data)


@main.route('/api/reservas/usuario/<id_usuario>', methods=['GET'])
def api_get_reservas_usuario(id_usuario):
    return get_reservas_usuario(id_usuario)


@main.route('/api/reservas/cancelar/<id_reserva>', methods=['PUT'])
def api_cancelar_reserva(id_reserva):
    return cancelar_reserva(id_reserva)


@main.route('/api/reservas/usuario/<id_usuario>/borrar-todas', methods=['DELETE'])
def api_delete_reservas_usuario(id_usuario):
    return delete_reservas_usuario(id_usuario)

@main.route('/api/mesas/todas', methods=['GET'])
def api_get_mesas():

    fecha = request.args.get("fecha")

    if not fecha:
        return jsonify({
            "error": "Debe enviar la fecha."
        }), 400

    try:
        fecha_reserva = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({
            "error": "Formato de fecha inválido."
        }), 400

    mesas = Mesa.query.order_by(Mesa.numero).all()

    reservas = Reserva.query.filter(
        Reserva.fecha == fecha_reserva,
        Reserva.estado != "Cancelada"
    ).all()

    mesas_ocupadas = {
        r.id_mesa for r in reservas
    }

    resultado = []

    for mesa in mesas:

        estado = "Reservada" if mesa.id_mesa in mesas_ocupadas else "Disponible"

        resultado.append({
            "id_mesa": mesa.id_mesa,
            "numero": mesa.numero,
            "capacidad": mesa.capacidad,
            "zona": mesa.zona,
            "estado": estado
        })

    return jsonify({
        "mesas": resultado
    }), 200