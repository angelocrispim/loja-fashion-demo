from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    codigo = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )

    nome = Column(String, nullable=False)

    descricao = Column(Text)

    preco = Column(Float, nullable=False)

    imagem = Column(String)

    categoria = Column(String)

    estoque = Column(Integer, default=0)
    
    em_promocao = Column(
    Boolean,
    default=False
    )

    percentual_desconto = Column(
        Integer,
        default=0
    )

    # RELAÇÃO COM IMAGENS

    imagens = relationship(
        "ProductImage",
        back_populates="produto",
        cascade="all, delete"
    )


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)

    produto_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    imagem = Column(String, nullable=False)

    produto = relationship(
        "Product",
        back_populates="imagens"
    )