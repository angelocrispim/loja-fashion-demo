from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from database import Base


class CashRegister(Base):

    __tablename__ = "cash_register"

    id = Column(
        Integer,
        primary_key=True
    )

    # funcionário operador
    funcionario_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    # valor inicial caixa
    fundo_caixa = Column(
        Float,
        default=0
    )

    # valor fechamento
    saldo_final = Column(
        Float,
        default=0
    )

    # status
    # aberto / fechado
    status = Column(
        String,
        default="aberto"
    )

    # data abertura
    aberto_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # data fechamento
    fechado_em = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # relacionamento funcionário
    funcionario = relationship(
        "Employee"
    )