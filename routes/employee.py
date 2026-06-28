from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Form
from fastapi import Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from utils.security import hash_senha

from sqlalchemy.orm import Session

from database import SessionLocal
from models.employee import Employee
from models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# CONEXÃO DB
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# LISTAR FUNCIONÁRIOS
# =========================
@router.get("/admin/funcionarios")
def admin_funcionarios(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    funcionarios = db.query(Employee).all()

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="admin/funcionarios.html",
        context={
            "funcionarios": funcionarios,
            "usuario": usuario
        }
    )


# =========================
# CADASTRAR FUNCIONÁRIO
# =========================
@router.post("/admin/cadastrar-funcionario")
def cadastrar_funcionario(
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf: str = Form(...),
    senha: str = Form(...),
    cargo: str = Form(...),
    salario: str = Form(...),
    db: Session = Depends(get_db)
):

    salario_convertido = (
        salario
        .replace(".", "")
        .replace(",", ".")
    )

    # Criptografa a senha
    senha_hash = hash_senha(senha)

    # Verifica e-mail
    usuario_email = db.query(User).filter(
        User.email == email
    ).first()

    if usuario_email:
        return RedirectResponse(
            "/admin/funcionarios",
            status_code=302
        )

    # Verifica CPF
    usuario_cpf = db.query(User).filter(
        User.cpf == cpf
    ).first()

    if usuario_cpf:
        return RedirectResponse(
            "/admin/funcionarios",
            status_code=302
        )

    # Define quem é administrador
    is_admin = cargo in ["Administrador", "Gerente"]

    novo_usuario = User(
        nome=nome,
        email=email,
        senha=senha_hash,
        telefone=telefone,
        cpf=cpf,
        cargo=cargo,
        is_admin=is_admin,
        is_superadmin=False
    )
    try:
        db.add(novo_usuario)

        funcionario = Employee(
            nome=nome,
            matricula=matricula,
            email=email,
            telefone=telefone,
            cpf=cpf,
            senha=senha_hash,
            cargo=cargo,
            salario=float(salario_convertido)
        )

        db.add(funcionario)

        db.commit()
        
        db.refresh(novo_usuario)

    except Exception as e:

        db.rollback()
        
        print("ERRO AO CADASTRAR FUNCIONÁRIO:", e)

        raise

    return RedirectResponse(
        url="/admin/funcionarios",
        status_code=303
    )
# =========================================
# PÁGINA EDITAR FUNCIONÁRIO
# =========================================

@router.get("/admin/editar-funcionario/{funcionario_id}")
def pagina_editar_funcionario(
    funcionario_id: int,
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    funcionario = db.query(Employee).filter(
        Employee.id == funcionario_id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="admin/editar_funcionario.html",
        context={
            "request": request,
            "usuario": usuario,
            "funcionario": funcionario
        }
    )


# =========================================
# SALVAR EDIÇÃO FUNCIONÁRIO
# =========================================

@router.post("/admin/editar-funcionario/{funcionario_id}")
def salvar_edicao_funcionario(
    funcionario_id: int,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf: str = Form(...),
    cargo: str = Form(...),
    salario: str = Form(...),
    db: Session = Depends(get_db)
):

    funcionario = db.query(Employee).filter(
        Employee.id == funcionario_id
    ).first()

    salario = salario.replace(".", "").replace(",", ".")

    funcionario.nome = nome
    funcionario.matricula = matricula
    funcionario.email = email
    funcionario.telefone = telefone
    funcionario.cpf = cpf
    funcionario.cargo = cargo
    funcionario.salario = float(salario)

    db.commit()

    return RedirectResponse(
        url="/admin/funcionarios",
        status_code=302
    )


# =========================================
# DESATIVAR FUNCIONÁRIO
# =========================================

@router.get("/admin/desativar-funcionario/{funcionario_id}")
def desativar_funcionario(
    funcionario_id: int,
    db: Session = Depends(get_db)
):

    funcionario = db.query(Employee).filter(
        Employee.id == funcionario_id
    ).first()

    funcionario.status = "Inativo"

    db.commit()

    return RedirectResponse(
        url="/admin/funcionarios",
        status_code=302
    )
    
# ====================================
# ATIVAR FUNCIONÁRIO
# ====================================

@router.get("/admin/ativar-funcionario/{funcionario_id}")
def ativar_funcionario(
    funcionario_id: int,
    db: Session = Depends(get_db)
):

    funcionario = db.query(Employee).filter(
        Employee.id == funcionario_id
    ).first()

    funcionario.status = "Ativo"

    db.commit()

    return RedirectResponse(
        url="/admin/funcionarios",
        status_code=302
    )