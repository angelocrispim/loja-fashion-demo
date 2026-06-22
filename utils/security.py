from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str):
    # 🔐 corta para evitar erro do bcrypt
    senha = senha[:72]
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash: str):
    senha = senha[:72]
    return pwd_context.verify(senha, hash)