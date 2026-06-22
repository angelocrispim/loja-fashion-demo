from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    cpf = Column(String, unique=True)
    telefone = Column(String)
    
class ProdutoImagem(Base):
    __tablename__ = "produto_imagens"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    imagem = Column(String, nullable=False)
    produto = relationship("Produto", back_populates="imagens")