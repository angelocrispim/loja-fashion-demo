from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Cookie

from database import SessionLocal
from models.user import User

# 🔐 Segurança
from utils.security import hash_senha, verificar_senha

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================
# 🔹 CONEXÃO COM BANCO
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 📄 PÁGINA INICIAL
# =========================
#@router.get("/")
#def home(request: Request):

#    return templates.TemplateResponse(
#        "paginas/index.html",
#        {"request": request}
#    )

# @router.get("/")
# def home(
#     request: Request,
#     usuario_id: str = Cookie(None),
#     db: Session = Depends(get_db)
# ):

#     print(usuario_id)

#     usuario = None

#     if usuario_id:

#         usuario = db.query(User).filter(
#             User.id == int(usuario_id)
#         ).first()

#     return templates.TemplateResponse(
#         "paginas/index.html",
#         {
#             "request": request,
#             "usuario": usuario
#         }
#     )
    

# =========================
# 📄 PÁGINA DE CADASTRO
# =========================
@router.get("/cadastro")
def pagina_cadastro(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="usuarios/cadastro.html",
        context={}
    )


# =========================
# 💾 CADASTRAR USUÁRIO
# =========================
@router.post("/cadastro")
def cadastrar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    cpf: str = Form(...),
    telefone: str = Form(...),
    db: Session = Depends(get_db)
):

    # Verifica email
    usuario_email = db.query(User).filter(
        User.email == email
    ).first()

    if usuario_email:

        return templates.TemplateResponse(
            request=request,
            name="usuarios/cadastro.html",
            context={
                "erro": "Este email já está cadastrado. Utilize outro email."
            }
        )

    # Verifica CPF
    usuario_cpf = db.query(User).filter(
        User.cpf == cpf
    ).first()

    if usuario_cpf:

        return templates.TemplateResponse(
            request=request,
            name="usuarios/cadastro.html",
            context={
                "erro": "Este CPF já está cadastrado. Utilize outro CPF."
            }
        )

    senha_hash = hash_senha(senha)

    novo_usuario = User(
        nome=nome,
        email=email,
        cpf=cpf,
        telefone=telefone,
        senha=senha_hash,
        cargo="cliente"
    )

    db.add(novo_usuario)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="usuarios/cadastro.html",
        context={
            "sucesso": "Usuário cadastrado com sucesso!"
        }
    )


# =========================
# 📄 PÁGINA LOGIN
# =========================
@router.get("/login")
def pagina_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="usuarios/login.html",
        context={}
    )


# =========================
# 🔑 LOGIN
# =========================
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    next_url: str = Form("/"),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(User.email == email).first()

    # usuário não encontrado
    if not usuario:
        return templates.TemplateResponse(
            request=request,
            name="usuarios/login.html",
            context={
                "erro": "Usuário não encontrado"
            }
        )

    # senha inválida
    if not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            request=request,
            name="usuarios/login.html",
            context={
                "erro": "Senha inválida"
            }
        )

    # login OK
    response = RedirectResponse(
        url=next_url,
        status_code=302
    )
    
    response.set_cookie(
    key="usuario_id",
    value=str(usuario.id),
    httponly=True,
    max_age=60 * 60 * 24 * 7
)

    return response

# =========================
# 🔑 LOGIN
# =========================
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    next_url: str = Form("/"),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(User.email == email).first()

    # usuário não encontrado
    if not usuario:
        return templates.TemplateResponse(
            request=request,
            name="usuarios/login.html",
            context={
                "erro": "Usuário não encontrado"
            }
        )

    # DEBUG
    print("SENHA DIGITADA:", senha)
    print("HASH DO BANCO:", usuario.senha)

    resultado = verificar_senha(senha, usuario.senha)

    print("RESULTADO:", resultado)

    # senha inválida
    if not resultado:
        return templates.TemplateResponse(
            request=request,
            name="usuarios/login.html",
            context={
                "erro": "Senha inválida"
            }
        )

    if usuario.is_admin:
        response = RedirectResponse(
            url="/admin",
            status_code=302
        )
    else:
        response = RedirectResponse(
            url=next_url,
            status_code=302
        )

    response.set_cookie(
        key="usuario_id",
        value=str(usuario.id),
        httponly=True,
        max_age=60 * 60 * 24 * 7
    )

    return response

###############
# LOGOUT
##############
@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/",
        status_code=302
    )

    response.delete_cookie("usuario_id")

    return response

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    next_url: str = Form("/"),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.email == email
    ).first()

    if not usuario:
        return templates.TemplateResponse(
            request=request,
            name="usuarios/login.html",
            context={
                "erro": "Usuário não encontrado"
            }
        )

    if not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            request=request,
            name="usuarios/login.html",
            context={
                "erro": "Senha inválida"
            }
        )

    response = RedirectResponse(
        url=next_url,
        status_code=302
    )

    response.set_cookie(
        key="usuario_id",
        value=str(usuario.id),
        httponly=True
    )

    return response

# =========================
# 👤 PERFIL DO USUÁRIO
# =========================
@router.get("/perfil")
def perfil(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    # se não estiver logado
    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    # segurança extra
    if not usuario:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="usuarios/perfil.html",
        context={
            "usuario": usuario
        }
    )


# =========================
# 👤 PERFIL DO ADMIN TEMPORARIO
# =========================

# @router.get("/criar-superadmin")
# def criar_superadmin(
#     db: Session = Depends(get_db)
# ):

#     admin = db.query(User).filter(
#         User.email == "admin@lojafashion.com"
#     ).first()

#     if admin:
#         return {
#             "msg": "Super Admin já existe"
#         }

#     novo_admin = User(
#         nome="Super Administrador",
#         email="admin@lojafashion.com",
#         senha=hash_senha("123456"),
#         telefone="00000000000",
#         cpf="00000000000",
#         is_admin=True,
#         is_superadmin=True
#     )

#     db.add(novo_admin)
#     db.commit()

#     return {
#         "msg": "Super Admin criado com sucesso"
#     }
