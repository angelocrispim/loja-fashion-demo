from database import SessionLocal
from models import User

db = SessionLocal()

email = "angelo@email.com"

usuario_existente = db.query(User).filter(User.email == email).first()

if usuario_existente:
    print("⚠️ Email já cadastrado!")
else:
    novo_usuario = User(
        nome="Angelo",
        email=email,
        senha="1234"
    )
    db.add(novo_usuario)
    db.commit()
    print("✅ Usuário criado!")

db.close()