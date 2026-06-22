from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from database import Base


class CashFlow(Base):

    __tablename__ = "cash_flow"

    id = Column(
        Integer,
        primary_key=True
    )

    # tipo:
    # entrada / saida
    tipo = Column(
        String,
        nullable=False
    )

    # descrição
    descricao = Column(
        String,
        nullable=False
    )

    # valor
    valor = Column(
        Float,
        nullable=False
    )

    # forma pagamento
    forma_pagamento = Column(
        String,
        nullable=True
    )

    # categoria
    categoria = Column(
        String,
        nullable=True
    )

    # data criação
    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )