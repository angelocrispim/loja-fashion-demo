from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Form, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from models.user import User
from models.product import Product
from models.contact_message import ContactMessage
from models.order_item import OrderItem

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def home(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    ###################################################
    # PRODUTOS DESTAQUE
    ###################################################

    produtos_destaque = db.query(Product)\
        .order_by(Product.id.desc())\
        .limit(8)\
        .all()

    ###################################################
    # PROMOÇÕES
    ###################################################

    promocoes = db.query(Product)\
        .filter(Product.em_promocao == True)\
        .limit(3)\
        .all()

    # Se não houver promoções,
    # usa os últimos produtos cadastrados
    if not promocoes:

        promocoes = db.query(Product)\
            .order_by(Product.id.desc())\
            .limit(3)\
            .all()

    ###################################################
    # MAIS VENDIDOS
    ###################################################

    mais_vendidos = (
        db.query(
            Product,
            func.sum(OrderItem.quantidade).label("vendidos")
        )
        .join(
            OrderItem,
            Product.id == OrderItem.produto_id
        )
        .group_by(Product.id)
        .order_by(
            func.sum(OrderItem.quantidade).desc()
        )
        .limit(4)
        .all()
    )

    # Se ainda não houver vendas,
    # mostra os últimos produtos cadastrados
    if not mais_vendidos:

        mais_vendidos = [

            (produto, 0)

            for produto in db.query(Product)
            .order_by(Product.id.desc())
            .limit(4)
            .all()

        ]

    ###################################################

    return templates.TemplateResponse(
        request=request,
        name="paginas/index.html",
        context={

            "usuario": usuario,

            "produtos_destaque": produtos_destaque,

            "promocoes": promocoes,

            "mais_vendidos": mais_vendidos

        }
    )


###################################################
# CONTATO
###################################################

@router.get("/contato")
def pagina_contato(
    request: Request,
    sucesso: int = Query(0),
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    return templates.TemplateResponse(
        request=request,
        name="paginas/contato.html",
        context={
            "usuario": usuario,
            "sucesso": sucesso
        }
    )


###################################################
# ENVIAR CONTATO
###################################################

@router.post("/contato")
def enviar_mensagem(

    nome: str = Form(...),

    email: str = Form(...),

    telefone: str = Form(""),

    assunto: str = Form(""),

    mensagem: str = Form(...),

    db: Session = Depends(get_db)

):

    nova_mensagem = ContactMessage(

        nome=nome,

        email=email,

        telefone=telefone,

        assunto=assunto,

        mensagem=mensagem

    )

    db.add(nova_mensagem)

    db.commit()

    return RedirectResponse(
        url="/contato?sucesso=1",
        status_code=302
    )