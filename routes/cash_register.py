from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.employee import Employee
from models.product import Product
from models.cash_register import CashRegister



templates = Jinja2Templates(directory="templates")

router = APIRouter()


# =========================================
# TELA DO CAIXA
# =========================================

@router.get("/admin/caixa")
def tela_caixa(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    funcionarios = db.query(Employee).all()

    return templates.TemplateResponse(
    request=request,
    name="admin/caixa.html",
    context={
        "usuario": usuario,
        "funcionarios": funcionarios
    }
)
    
# =========================================
# BUSCAR PRODUTO PELO CÓDIGO
# =========================================

@router.get("/admin/caixa/produto/{codigo}")
def buscar_produto(
    codigo: str,
    db: Session = Depends(get_db)
):

    produto = db.query(Product).filter(
        Product.codigo == codigo
    ).first()

    if not produto:
        return JSONResponse(
            status_code=404,
            content={"erro": "Produto não encontrado"}
        )

    return {
        "id": produto.id,
        "nome": produto.nome,
        "preco": float(produto.preco),
        "estoque": produto.estoque
    }