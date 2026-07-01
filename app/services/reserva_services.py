from datetime import datetime
from app.models import db, Reserva, Mesa, Usuario
import random


# =========================================
# CREAR RESERVA
# =========================================

def crear_reserva(data):
    try:
        id_usuario = data.get('id_usuario')
        id_mesa = data.get('id_mesa')
        fecha = data.get('fecha')
        cantidad_personas = data.get('cantidad_personas')

        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        if not usuario:
            return None, "Usuario no encontrado"

        mesa = Mesa.query.filter_by(id_mesa=id_mesa).first()
        if not mesa:
            return None, "Mesa no encontrada"

        if mesa.estado != "Disponible":
            return None, "Mesa no disponible"

        if cantidad_personas > mesa.capacidad:
            return None, "Excede capacidad de la mesa"

        fecha_reserva = datetime.strptime(fecha, "%Y-%m-%d %H:%M")

        if fecha_reserva < datetime.now():
            return None, "Fecha inválida"

        id_reserva = f"R{random.randint(1000, 9999)}"

        reserva = Reserva(
            id_reserva=id_reserva,
            id_usuario=id_usuario,
            id_mesa=id_mesa,
            fecha=fecha_reserva,
            estado="Pendiente",
            cantidad_personas=cantidad_personas
        )

        mesa.estado = "Reservada"

        db.session.add(reserva)
        db.session.commit()

        return reserva, "Reserva creada exitosamente"

    except Exception as e:
        db.session.rollback()
        return None, str(e)


# =========================================
# CANCELAR RESERVA
# =========================================

def cancelar_reserva(id_reserva):
    try:
        reserva = Reserva.query.filter_by(id_reserva=id_reserva).first()

        if not reserva:
            return False, "Reserva no encontrada"

        reserva.estado = "Cancelada"

        mesa = Mesa.query.get(reserva.id_mesa)
        if mesa:
            mesa.estado = "Disponible"

        db.session.commit()

        return True, "Reserva cancelada"

    except Exception as e:
        db.session.rollback()
        return False, str(e)


# =========================================
# RESERVAS POR USUARIO
# =========================================

def get_reservas_usuario(id_usuario):
    reservas = Reserva.query.filter_by(id_usuario=id_usuario).all()

    return reservas


# =========================================
# BORRAR TODAS LAS RESERVAS USUARIO
# =========================================

def delete_reservas_usuario(id_usuario):
    try:
        reservas = Reserva.query.filter_by(id_usuario=id_usuario).all()

        if not reservas:
            return False, "No hay reservas"

        for r in reservas:
            mesa = Mesa.query.get(r.id_mesa)
            if mesa:
                mesa.estado = "Disponible"

        Reserva.query.filter_by(id_usuario=id_usuario).delete()

        db.session.commit()

        return True, f"Eliminadas {len(reservas)} reservas"

    except Exception as e:
        db.session.rollback()
        return False, str(e)