from models.user import User
from models.store_config import StoreConfig


def contexto_admin(
    db,
    usuario_id
):

    print("Contexto Admin Executado")
    
    usuario = None

    if usuario_id:

        usuario = db.query(
            User
        ).filter(
            User.id == int(usuario_id)
        ).first()

    config = db.query(
        StoreConfig
    ).first()

    return {

        "usuario": usuario,

        "config": config

    }