from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    senha = Column(String, nullable=False)

    super_admin = Column(Boolean, default=False)