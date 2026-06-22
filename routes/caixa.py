from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Form
from fastapi import Cookie
from fastapi import Body

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal

from datetime import date

from models.employee import Employee
from models.sale import Sale, SaleItem
from models.product import Product
from models.financial_transaction import FinancialTransaction
from models.cash_closing import CashClosing
from models.cash_flow import CashFlow
from models.user import User


templates = Jinja2Templates(
    directory="templates"
)

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
        
        
@router.get("/caixa/login")
def pagina_login_caixa(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="caixa/login_caixa.html",
        context={}
    )
    
@router.post("/caixa/login")
def login_caixa(
    matricula: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):

    funcionario = db.query(Employee).filter(
        Employee.matricula == matricula
    ).first()

    print("MATRICULA DIGITADA:", matricula)

    if funcionario:
        print("FUNCIONARIO:", funcionario.nome)
        print("SENHA BANCO:", funcionario.senha)
        print("STATUS:", funcionario.status)
    else:
        print("FUNCIONARIO NÃO ENCONTRADO")

    if not funcionario:

        return RedirectResponse(
            url="/caixa/login",
            status_code=302
        )

    response = RedirectResponse(
        url="/caixa",
        status_code=302
    )

    response.set_cookie(
        key="operador_caixa",
        value=str(funcionario.id)
    )

    return response

# =====================================
# TELA PRINCIPAL DO CAIXA
# =====================================

@router.get("/caixa")
def tela_caixa(
    request: Request,
    operador_caixa: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not operador_caixa:

        return RedirectResponse(
            url="/caixa/login",
            status_code=302
        )

    funcionario = db.query(Employee).filter(
        Employee.id == int(operador_caixa)
    ).first()

    if not funcionario:

        return RedirectResponse(
            url="/caixa/login",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="caixa/caixa.html",
        context={
            "usuario": funcionario
        }
    )
   
@router.post("/caixa/finalizar-venda")
def finalizar_venda(
    dados: dict = Body(...),
    db: Session = Depends(get_db)
):

    funcionario_id = dados["funcionario_id"]

    pagamento = dados["pagamento"]

    desconto = dados["desconto"]

    total = dados["total"]

    produtos = dados["produtos"]

    parcelas = dados.get(
        "parcelas",
        1
    )

    valor_parcela = dados.get(
        "valor_parcela",
        total
    )

    venda = Sale(
        funcionario_id=funcionario_id,
        pagamento=pagamento,
        desconto=desconto,
        total=total,
        parcelas=parcelas,
        valor_parcela=valor_parcela
    )

    db.add(venda)

    db.commit()

    db.refresh(venda)
    
            # REGISTRAR NO FLUXO DE CAIXA

    movimentacao = FinancialTransaction(
        tipo="Entrada",
        categoria="Venda",
        descricao=f"Venda Nº {venda.id}",
        valor=total
    )

    db.add(movimentacao)

    db.commit()
    
    for item in produtos:

        produto = db.query(Product).filter(
            Product.id == item["id"]
        ).first()

        venda_item = SaleItem(
            venda_id=venda.id,
            produto_id=produto.id,
            quantidade=item["quantidade"],
            preco_unitario=produto.preco,
            subtotal=produto.preco * item["quantidade"]
        )

        db.add(venda_item)

        # BAIXA NO ESTOQUE
        produto.estoque -= item["quantidade"]
        
        # ====================================
        # REGISTRAR ENTRADA NO FLUXO DE CAIXA
        # ====================================

    movimentacao = CashFlow(

        tipo="entrada",

        descricao=f"Venda PDV #{venda.id} - {pagamento}",

        valor=total,

    )

    db.add(movimentacao)
        
        

    db.commit()

    return {
        "success": True,
        "venda_id": venda.id
    }
    
##########################
# FECHAMENTO DE CAIXA
##########################

@router.post("/caixa/fechar")
def fechar_caixa(

    operador_caixa: str = Cookie(None),

    db: Session = Depends(get_db)

):

    hoje = date.today()

    vendas = db.query(
        func.sum(Sale.total)
    ).filter(
        func.date(Sale.data_venda) == hoje
    ).scalar() or 0

    despesas = db.query(
        func.sum(CashFlow.valor)
    ).filter(
        CashFlow.tipo == "saida"
    ).scalar() or 0

    saldo = vendas - despesas

    fechamento = CashClosing(

        funcionario_id=int(operador_caixa),

        total_vendas=vendas,

        total_despesas=despesas,

        saldo_final=saldo

    )

    db.add(fechamento)

    db.commit()

    return {
        "success": True,
        "vendas": vendas,
        "despesas": despesas,
        "saldo": saldo
    }
    
#################################
# CAIXA VENDAS
#################################
@router.get("/caixa/vendas")
def historico_vendas(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    vendas = db.query(
        Sale
    ).order_by(
        Sale.id.desc()
    ).all()

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="caixa/caixa_vendas.html",
        context={
            "vendas": vendas,
            "usuario": usuario
        }
    )
        
#################################
# PAGAMENTOS
#################################
    
@router.get("/caixa/pagamento/{venda_id}")
def tela_pagamento(
    request: Request,
    venda_id: int,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    venda = db.query(Sale).filter(
        Sale.id == venda_id
    ).first()

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="caixa/pagamento.html",
        context={
            "venda": venda,
            "usuario": usuario
        }
    )
    
#################################
# DETALHE VENDAS
#################################
    
@router.get("/caixa/venda/{venda_id}")
def detalhes_venda(
    request: Request,
    venda_id: int,
    db: Session = Depends(get_db)
):

    venda = db.query(Sale).filter(
        Sale.id == venda_id
    ).first()

    if not venda:

        return RedirectResponse(
            url="/caixa",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="caixa/detalhes_venda.html",
        context={
            "venda": venda,
            "usuario": venda.funcionario,
            "funcionario": venda.funcionario
        }
    )