from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class StoreConfig(Base):

    __tablename__ = "store_config"

    id = Column(
        Integer,
        primary_key=True
    )
    
    logo = Column(
        String,
        nullable=True
    )

    nome_loja = Column(String)

    telefone = Column(String)

    whatsapp = Column(String)

    email = Column(String)

    instagram = Column(String)

    endereco = Column(String)

    cidade = Column(String)

    logo = Column(String)