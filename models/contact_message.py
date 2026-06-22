from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

from datetime import datetime

from database import Base


class ContactMessage(Base):

    __tablename__ = "contact_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    telefone = Column(
        String
    )

    assunto = Column(
        String
    )

    mensagem = Column(
        Text,
        nullable=False
    )

    data_envio = Column(
        DateTime,
        default=datetime.utcnow
    )