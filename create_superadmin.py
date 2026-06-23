from database import SessionLocal
from models.user import User
from utils.security import hash_senha

db = SessionLocal()

# Verifica se já existe
admin = db.query(User).filter(
    User.email == "admin@lojafashion.com"
).first()

if admin:
    print("Super Admin já existe!")
else:

    novo_admin = User(
        nome="Super Administrador",
        email="admin@lojafashion.com",
        senha=hash_senha("123456"),
        telefone="00000000000",
        cpf="00000000000",
        is_admin=True,
        is_superadmin=True
    )

    db.add(novo_admin)
    db.commit()

    print("Super Admin criado com sucesso!")