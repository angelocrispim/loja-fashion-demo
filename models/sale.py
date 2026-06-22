from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from database import Base


class Sale(Base):

    __tablename__ = "sales"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    funcionario_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    pagamento = Column(String)

    desconto = Column(
        Float,
        default=0
    )

    total = Column(
        Float,
        nullable=False
    )

    data_venda = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    funcionario = relationship(
        "Employee"
    )

    itens = relationship(
        "SaleItem",
        back_populates="venda",
        cascade="all, delete"
    )
    
    parcelas = Column(
        Integer,
        default=1
    )

    valor_parcela = Column(
        Float,
        default=0
    )


class SaleItem(Base):

    __tablename__ = "sale_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    venda_id = Column(
        Integer,
        ForeignKey("sales.id")
    )

    produto_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantidade = Column(Integer)

    preco_unitario = Column(Float)

    subtotal = Column(Float)

    venda = relationship(
        "Sale",
        back_populates="itens"
    )

    produto = relationship(
        "Product"
    )