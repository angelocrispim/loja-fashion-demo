from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)

    nome = Column(String, nullable=False)

    matricula = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True
    )

    telefone = Column(String)

    cpf = Column(
        String,
        unique=True
    )

    cargo = Column(String)

    salario = Column(Float)

    data_admissao = Column(Date)

    status = Column(
        String,
        default="Ativo"
    )

    # NOVO CAMPO

    senha = Column(
        String,
        nullable=False,
        default="123456"
    )