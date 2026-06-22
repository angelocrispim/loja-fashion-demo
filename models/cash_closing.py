from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class CashClosing(Base):

    __tablename__ = "cash_closings"

    id = Column(
        Integer,
        primary_key=True
    )

    funcionario_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    total_vendas = Column(
        Float,
        default=0
    )

    total_despesas = Column(
        Float,
        default=0
    )

    saldo_final = Column(
        Float,
        default=0
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # RELACIONAMENTO
    funcionario = relationship(
        "Employee"
    )