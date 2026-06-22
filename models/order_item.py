from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    pedido_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    produto_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantidade = Column(Integer)

    preco = Column(Float, default=0)

    # RELACIONAMENTOS
    pedido = relationship(
        "Order",
        back_populates="itens"
    )

    produto = relationship(
        "Product"
    )