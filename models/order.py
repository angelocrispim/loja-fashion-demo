from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

from database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    usuario_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    total = Column(
        Float,
        default=0
    )

    # NOVO: forma de pagamento
    forma_pagamento = Column(
        String,
        nullable=True
    )

    # NOVO: quantidade de parcelas
    parcelas = Column(
        Integer,
        default=1
    )

    # Status do pedido
    status = Column(
        String,
        default="Pendente"
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # RELACIONAMENTO USUÁRIO
    usuario = relationship(
        "User",
        back_populates="pedidos"
    )

    # RELACIONAMENTO ITENS
    itens = relationship(
        "OrderItem",
        back_populates="pedido"
    )