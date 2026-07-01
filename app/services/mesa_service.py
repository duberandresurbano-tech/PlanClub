from app.models import db, Mesa


def obtener_mesas_disponibles():
    """
    Retorna todas las mesas disponibles
    """
    mesas = Mesa.query.filter_by(estado="Disponible").all()

    return [
        {
            "id_mesa": m.id_mesa,
            "numero": m.numero,
            "capacidad": m.capacidad,
            "zona": m.zona,
            "estado": m.estado
        }
        for m in mesas
    ]


def obtener_todas_mesas():
    """
    Retorna todas las mesas sin filtrar
    """
    mesas = Mesa.query.all()

    return [
        {
            "id_mesa": m.id_mesa,
            "numero": m.numero,
            "capacidad": m.capacidad,
            "zona": m.zona,
            "estado": m.estado
        }
        for m in mesas
    ]


def inicializar_mesas(mesas_data):
    """
    Crea mesas en base de datos
    """
    try:
        for m in mesas_data:
            nueva_mesa = Mesa(**m)
            db.session.add(nueva_mesa)

        db.session.commit()
        return {"mensaje": "Mesas inicializadas", "cantidad": len(mesas_data)}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def eliminar_todas_mesas():
    """
    Borra todas las mesas
    """
    try:
        Mesa.query.delete()
        db.session.commit()
        return {"mensaje": "Mesas eliminadas"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def liberar_mesa(id_mesa):
    """
    Marca una mesa como disponible
    """
    mesa = Mesa.query.filter_by(id_mesa=id_mesa).first()

    if not mesa:
        return {"error": "Mesa no encontrada"}, 404

    mesa.estado = "Disponible"
    db.session.commit()

    return {"mensaje": "Mesa liberada"}, 200


def ocupar_mesa(id_mesa):
    """
    Marca una mesa como reservada
    """
    mesa = Mesa.query.filter_by(id_mesa=id_mesa).first()

    if not mesa:
        return {"error": "Mesa no encontrada"}, 404

    mesa.estado = "Reservada"
    db.session.commit()

    return {"mensaje": "Mesa ocupada"}, 200