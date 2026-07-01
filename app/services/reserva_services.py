from datetime import datetime
from app.models import db, Reserva, Mesa, Usuario
import random
from flask import jsonify


# =========================
# CREAR RESERVA
# =========================

def crear_reserva(data):
    try:
        id_usuario = data.get('id_usuario')
        id_mesa = data.get('id_mesa')
        fecha = data.get('fecha')
        cantidad_personas = data.get('cantidad_personas')

        if not all([id_usuario, id_mesa, fecha, cantidad_personas]):
            return jsonify({"error": "Datos incompletos"}), 400

        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        mesa = Mesa.query.filter_by(id_mesa=id_mesa).first()
        if not mesa:
            return jsonify({"error": "Mesa no encontrada"}), 404

        try:
            fecha_reserva = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400

        if fecha_reserva < datetime.now():
            return jsonify({"error": "Fecha inválida"}), 400

        if cantidad_personas > mesa.capacidad:
            return jsonify({"error": "Excede la capacidad de la mesa"}), 400

        # Verificar si esa mesa ya está reservada para esa misma fecha
        reserva_existente = Reserva.query.filter(
            Reserva.id_mesa == id_mesa,
            Reserva.fecha == fecha_reserva,
            Reserva.estado != "Cancelada"
        ).first()

        if reserva_existente:
            return jsonify({
                "error": "La mesa ya está reservada para esa fecha."
            }), 400

        # Generar un ID único
        while True:
            id_reserva = f"R{random.randint(1000, 9999)}"
            if not Reserva.query.filter_by(id_reserva=id_reserva).first():
                break

        reserva = Reserva(
            id_reserva=id_reserva,
            id_usuario=id_usuario,
            id_mesa=id_mesa,
            fecha=fecha_reserva,
            estado="Pendiente",
            cantidad_personas=cantidad_personas
        )

        db.session.add(reserva)
        db.session.commit()

        return jsonify({
            "mensaje": "Reserva creada exitosamente",
            "id_reserva": id_reserva
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# =========================
# CANCELAR RESERVA
# =========================

def cancelar_reserva(id_reserva):
    try:
        reserva = Reserva.query.filter_by(id_reserva=id_reserva).first()

        if not reserva:
            return jsonify({"error": "Reserva no encontrada"}), 404

        reserva.estado = "Cancelada"

        db.session.commit()

        return jsonify({"mensaje": "Reserva cancelada"}), 200


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =========================
# RESERVAS POR USUARIO
# =========================

def get_reservas_usuario(id_usuario):
    try:

        reservas = Reserva.query.filter_by(
            id_usuario=id_usuario
        ).order_by(
            Reserva.fecha.desc()
        ).all()

        resultado = []

        for reserva in reservas:

            mesa = Mesa.query.filter_by(
                id_mesa=reserva.id_mesa
            ).first()

            resultado.append({
                "id_reserva": reserva.id_reserva,
                "fecha": reserva.fecha.strftime("%d/%m/%Y %H:%M"),
                "estado": reserva.estado,
                "cantidad_personas": reserva.cantidad_personas,
                "nombre_mesa": f"Mesa {mesa.numero}" if mesa else "Mesa no encontrada",
                "zona": mesa.zona if mesa else "Sin zona"
            })

        return jsonify({
            "reservas": resultado
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# BORRAR TODAS LAS RESERVAS
# =========================

def delete_reservas_usuario(id_usuario):
    try:
        print("===== DELETE RESERVAS =====")
        print("Usuario:", id_usuario)

        reservas = Reserva.query.filter_by(id_usuario=id_usuario).all()
        
        print("Cantidad de reservas encontradas:", len(reservas))

        if not reservas:
            return jsonify({"error": "No hay reservas"}), 404

        Reserva.query.filter_by(id_usuario=id_usuario).delete()

        db.session.commit()

        return jsonify({
            "mensaje": f"Eliminadas {len(reservas)} reservas"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500