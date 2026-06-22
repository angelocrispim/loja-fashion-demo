from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi import Depends
from fastapi import Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy import func

from datetime import date

from database import SessionLocal

from models.cash_flow import CashFlow
from models.user import User
from models.sale import Sale, SaleItem
from models.financial_transaction import FinancialTransaction
from models.cash_closing import CashClosing
from models.product import Product
from models.order import Order
from models.employee import Employee

from utils.context import contexto_admin


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# DB
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# FINANCEIRO
# =========================
@router.get("/admin/financeiro")
def admin_financeiro(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    movimentacoes = db.query(CashFlow).order_by(
        CashFlow.id.desc()
    ).all()

    entradas = db.query(
        func.sum(CashFlow.valor)
    ).filter(
        CashFlow.tipo == "entrada"
    ).scalar() or 0

    saidas = db.query(
        func.sum(CashFlow.valor)
    ).filter(
        CashFlow.tipo == "saida"
    ).scalar() or 0

    saldo = entradas - saidas

    return templates.TemplateResponse(
        request=request,
        name="admin/financeiro.html",
        context={
            "usuario": usuario,
            "movimentacoes": movimentacoes,
            "entradas": entradas,
            "saidas": saidas,
            "saldo": saldo
        }
    )
    
@router.get("/admin/dashboard-financeiro")
def dashboard_financeiro(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    hoje = date.today()

    # =========================
    # VENDAS HOJE
    # =========================

    vendas_hoje = db.query(
        func.sum(Sale.total)
    ).filter(
        func.date(Sale.data_venda) == hoje
    ).scalar()

    if not vendas_hoje:
        vendas_hoje = 0

    # =========================
    # VENDAS MÊS
    # =========================

    vendas_mes = db.query(
        func.sum(Sale.total)
    ).filter(
        func.extract("month", Sale.data_venda)
        == hoje.month
    ).scalar()

    if not vendas_mes:
        vendas_mes = 0

    # =========================
    # QUANTIDADE VENDAS
    # =========================

    quantidade_vendas = db.query(
        Sale
    ).count()

    # =========================
    # TICKET MÉDIO
    # =========================

    ticket_medio = 0

    if quantidade_vendas > 0:

        ticket_medio = (
            vendas_mes / quantidade_vendas
        )
        
# ====================================
# GRÁFICO VENDAS POR DIA
# ====================================

    vendas_grafico = db.query(
        func.date(Sale.data_venda),
        func.sum(Sale.total)
    ).group_by(
            func.date(Sale.data_venda)
    ).order_by(
            func.date(Sale.data_venda)
    ).all()

    labels = []
    valores = []

    for data, valor in vendas_grafico:

        labels.append(
            data.strftime("%d/%m")
        )

        valores.append(
            float(valor)
        )
    

    return templates.TemplateResponse(
        request=request,
        name="finance/dashboard_financeiro.html",
        context={
            "request": request,
            "usuario": usuario,
            "vendas_hoje": vendas_hoje,
            "vendas_mes": vendas_mes,
            "quantidade_vendas": quantidade_vendas,
            "ticket_medio": ticket_medio,
            "labels": labels,
            "valores": valores 
        }
    )
    
@router.get("/admin/fluxo-caixa")
def fluxo_caixa(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    movimentacoes = db.query(
        FinancialTransaction
    ).order_by(
        FinancialTransaction.id.desc()
    ).all()

    entradas = db.query(
        func.sum(FinancialTransaction.valor)
    ).filter(
        FinancialTransaction.tipo == "Entrada"
    ).scalar() or 0

    saidas = db.query(
        func.sum(FinancialTransaction.valor)
    ).filter(
        FinancialTransaction.tipo == "Saida"
    ).scalar() or 0

    saldo = entradas - saidas

    return templates.TemplateResponse(
        request=request,
        name="finance/fluxo_caixa.html",
        context={
            "request": request,
            "usuario": usuario,
            "movimentacoes": movimentacoes,
            "entradas": entradas,
            "saidas": saidas,
            "saldo": saldo
        }
    )
    
@router.get("/admin/despesas")
def pagina_despesas(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="finance/despesas.html",
        context={
            "usuario": usuario
        }
    )
    
@router.post("/admin/despesas")
def cadastrar_despesa(

    descricao: str = Form(...),

    valor: float = Form(...),

    db: Session = Depends(get_db)

):

    despesa = CashFlow(

        tipo="saida",

        descricao=descricao,

        valor=valor

    )

    db.add(despesa)

    db.commit()

    return RedirectResponse(
        url="/admin/fluxo-caixa",
        status_code=302
    )
    
@router.get("/admin/gerenciar-despesas")
def gerenciar_despesas(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    despesas = db.query(CashFlow).filter(
        CashFlow.tipo == "saida"
    ).order_by(
        CashFlow.id.desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="finance/gerenciar_despesas.html",
        context={
            "usuario": usuario,
            "despesas": despesas
        }
    )
    
@router.get("/admin/despesa/{despesa_id}/excluir")
def excluir_despesa(
    despesa_id: int,
    db: Session = Depends(get_db)
):

    despesa = db.query(CashFlow).filter(
        CashFlow.id == despesa_id
    ).first()

    if despesa:

        db.delete(despesa)

        db.commit()

    return RedirectResponse(
        url="/admin/gerenciar-despesas",
        status_code=302
    )
    
########################################
# FECHAMENTO DE CAIXA
########################################

@router.get("/admin/fechamentos-caixa")
def fechamentos_caixa(

    request: Request,

    db: Session = Depends(get_db),

    usuario_id: str = Cookie(None)

):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    fechamentos = db.query(
        CashClosing
    ).order_by(
        CashClosing.id.desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="finance/fechamentos_caixa.html",
        context={
            "usuario": usuario,
            "fechamentos": fechamentos
        }
    )
    
###########################################
# RELATORIO DE VENDA
###########################################

@router.get("/admin/relatorio-vendas")
def relatorio_vendas(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    hoje = date.today()

    vendas_hoje = db.query(
        func.sum(Sale.total)
    ).filter(
        func.date(Sale.data_venda) == hoje
    ).scalar() or 0

    vendas_mes = db.query(
        func.sum(Sale.total)
    ).filter(
        func.extract("month", Sale.data_venda)
        == hoje.month
    ).scalar() or 0

    quantidade_vendas = db.query(
        Sale
    ).count()

    ticket_medio = 0

    if quantidade_vendas > 0:

        ticket_medio = (
            vendas_mes / quantidade_vendas
        )
        
        # ====================================
        # GRÁFICO DE VENDAS
        # ====================================

        vendas_grafico = db.query(
            func.date(Sale.data_venda),
            func.sum(Sale.total)
        ).group_by(
            func.date(Sale.data_venda)
        ).order_by(
            func.date(Sale.data_venda)
        ).all()

        labels = []
        valores = []

        for data, valor in vendas_grafico:

            labels.append(
                data.strftime("%d/%m")
            )

            valores.append(
                float(valor)
            )

    # ====================================
    # GRÁFICO DE VENDAS
    # ====================================

    vendas_grafico = db.query(
        func.date(Sale.data_venda),
        func.sum(Sale.total)
    ).group_by(
        func.date(Sale.data_venda)
    ).order_by(
        func.date(Sale.data_venda)
    ).all()

    labels = []
    valores = []

    for data, valor in vendas_grafico:

        labels.append(
            data.strftime("%d/%m")
        )

        valores.append(
            float(valor)
        )

    return templates.TemplateResponse(
        request=request,
        name="finance/relatorio_vendas.html",
        context={
            "usuario": usuario,
            "vendas_hoje": vendas_hoje,
            "vendas_mes": vendas_mes,
            "quantidade_vendas": quantidade_vendas,
            "ticket_medio": ticket_medio,

            # gráfico
            "labels": labels,
            "valores": valores
        }
    )
    
@router.get("/admin/produtos-mais-vendidos")
def produtos_mais_vendidos(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    produtos = db.query(
        Product.nome,
        func.sum(SaleItem.quantidade).label("total_vendido")
    ).join(
        SaleItem,
        Product.id == SaleItem.produto_id
    ).group_by(
        Product.nome
    ).order_by(
        func.sum(SaleItem.quantidade).desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="finance/produtos_mais_vendidos.html",
        context={
            "usuario": usuario,
            "produtos": produtos
        }
    )
    
# ====================================
# # ORGANIZAÇÃO DE RELATORIOS
# ====================================

@router.get("/admin/estoque-baixo")
def estoque_baixo(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    produtos = db.query(Product).filter(
        Product.estoque <= 10
    ).order_by(
        Product.estoque.asc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="finance/estoque_baixo.html",
        context={
            "usuario": usuario,
            "produtos": produtos
        }
    )
    
# ====================================
# # MELHORES CLIENTES
# ====================================

@router.get("/admin/melhores-clientes")
def melhores_clientes(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    clientes = db.query(
        User.nome,
        func.count(Order.id).label("total_pedidos"),
        func.sum(Order.total).label("total_comprado")
    ).join(
        Order,
        User.id == Order.usuario_id
    ).group_by(
        User.nome
    ).order_by(
        func.sum(Order.total).desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="finance/melhores_clientes.html",
        context={
            "usuario": usuario,
            "clientes": clientes
        }
    )
    
@router.get("/admin/ranking-vendedores")
def ranking_vendedores(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    vendedores = db.query(
        Employee.nome,
        func.count(Sale.id).label("total_vendas"),
        func.sum(Sale.total).label("faturamento")
    ).join(
        Sale,
        Employee.id == Sale.funcionario_id
    ).group_by(
        Employee.nome
    ).order_by(
        func.sum(Sale.total).desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="finance/ranking_vendedores.html",
        context={
            "usuario": usuario,
            "vendedores": vendedores
        }
    )
    
@router.get("/admin/relatorio-lucro")
def relatorio_lucro(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    total_vendas = db.query(
        func.sum(Sale.total)
    ).scalar() or 0

    total_despesas = db.query(
        func.sum(CashFlow.valor)
    ).filter(
        CashFlow.tipo == "saida"
    ).scalar() or 0

    lucro = total_vendas - total_despesas

    margem = 0

    if total_vendas > 0:

        margem = (
            lucro / total_vendas
        ) * 100

    return templates.TemplateResponse(
        request=request,
        name="finance/relatorio_lucro.html",
        context={
            "usuario": usuario,
            "total_vendas": total_vendas,
            "total_despesas": total_despesas,
            "lucro": lucro,
            "margem": margem
        }
    )
    
# ====================================
# # PDF
# ====================================
@router.get("/admin/relatorio-lucro/pdf")
def gerar_pdf_lucro(
    db: Session = Depends(get_db)
):

    total_vendas = db.query(
        func.sum(Sale.total)
    ).scalar() or 0

    total_despesas = db.query(
        func.sum(CashFlow.valor)
    ).filter(
        CashFlow.tipo == "saida"
    ).scalar() or 0

    lucro = total_vendas - total_despesas

    margem = 0

    if total_vendas > 0:

        margem = (
            lucro / total_vendas
        ) * 100

    arquivo = "relatorio_lucro.pdf"

    pdf = SimpleDocTemplate(
        arquivo
    )

    estilos = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            "Relatório de Lucro",
            estilos["Title"]
        )
    )

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(
        Paragraph(
            f"Receita Total: R$ {total_vendas:.2f}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Despesas Totais: R$ {total_despesas:.2f}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Lucro Líquido: R$ {lucro:.2f}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Margem de Lucro: {margem:.2f}%",
            estilos["Normal"]
        )
    )

    pdf.build(
        elementos
    )

    return FileResponse(
        arquivo,
        media_type="application/pdf",
        filename="relatorio_lucro.pdf"
    )