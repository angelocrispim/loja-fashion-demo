from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_superadmin = Column(Boolean, default=False)

    telefone = Column(String)
    cpf = Column(String, unique=True)

    data_nascimento = Column(String)

    cep = Column(String)
    rua = Column(String)
    numero = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)
    
    pedidos = relationship(
        "Order",
        back_populates="usuario"
    )