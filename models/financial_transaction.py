from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from database import Base


class FinancialTransaction(Base):

    __tablename__ = "financial_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tipo = Column(
        String,
        nullable=False
    )
    # Entrada ou Saída

    categoria = Column(
        String,
        nullable=False
    )

    descricao = Column(
        String
    )

    valor = Column(
        Float,
        nullable=False
    )

    data = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )