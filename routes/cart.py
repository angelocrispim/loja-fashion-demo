from fastapi import APIRouter, Depends, Cookie, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse


from database import SessionLocal
from models.cart_item import CartItem
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
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


# ADICIONAR AO CARRINHO
@router.get("/adicionar-carrinho/{produto_id}")
def adicionar_carrinho(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    # se não estiver logado
    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    # buscar produto
    produto = db.query(Product).filter(
        Product.id == produto_id
    ).first()

    # produto não existe
    if not produto:
        return RedirectResponse(
            url="/produtos",
            status_code=302
        )

    # verificar estoque
    if produto.estoque <= 0:
        return RedirectResponse(
            url=f"/produto/{produto_id}",
            status_code=302
        )

    # verifica se produto já existe no carrinho
    item = db.query(CartItem).filter(
        CartItem.usuario_id == int(usuario_id),
        CartItem.produto_id == produto_id
    ).first()

    # se já existir -> soma quantidade
    if item:

        # impedir ultrapassar estoque
        if item.quantidade < produto.estoque:
            item.quantidade += 1

    else:

        novo_item = CartItem(
            usuario_id=int(usuario_id),
            produto_id=produto_id,
            quantidade=1
        )

        db.add(novo_item)

    db.commit()

    return RedirectResponse(
        url="/carrinho",
        status_code=302
    )
    
# PÁGINA CARRINHO
@router.get("/carrinho")
def pagina_carrinho(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    # usuário não logado
    if not usuario_id:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    itens = db.query(CartItem).filter(
        CartItem.usuario_id == int(usuario_id)
    ).all()

    total = 0

    for item in itens:

        produto = db.query(Product).filter(
            Product.id == item.produto_id
        ).first()

        item.produto = produto

        total += produto.preco * item.quantidade
        
    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    return templates.TemplateResponse(
    request=request,
    name="carrinho/carrinho.html",
    context={
        "itens": itens,
        "total": total,
        "usuario": usuario
    }
)
    
# REMOVER ITEM
@router.get("/remover-carrinho/{item_id}")
def remover_carrinho(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(CartItem).filter(
        CartItem.id == item_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    return RedirectResponse(
        url="/carrinho",
        status_code=302
    )
    
# AUMENTAR QUANTIDADE
@router.get("/aumentar/{item_id}")
def aumentar_quantidade(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(CartItem).filter(
        CartItem.id == item_id
    ).first()

    if item:

        produto = db.query(Product).filter(
            Product.id == item.produto_id
        ).first()

        # NÃO PASSAR DO ESTOQUE
        if item.quantidade < produto.estoque:
            item.quantidade += 1

        db.commit()

    return RedirectResponse(
        url="/carrinho",
        status_code=302
    )
    
# DIMINUIR QUANTIDADE
@router.get("/diminuir/{item_id}")
def diminuir_quantidade(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(CartItem).filter(
        CartItem.id == item_id
    ).first()

    if item:

        if item.quantidade > 1:
            item.quantidade -= 1

        else:
            db.delete(item)

        db.commit()

    return RedirectResponse(
        url="/carrinho",
        status_code=302
    )

# CHECKOUT 
@router.get("/checkout") 
def checkout( 
    request: Request, 
    db: Session = Depends(get_db), 
    usuario_id: str = Cookie(None) 
): 
    # usuário não logado 
    if not usuario_id: 
        return RedirectResponse( 
            url="/login", 
            status_code=302 
        ) 
    # buscar itens carrinho 
    itens = db.query(CartItem).filter( 
        CartItem.usuario_id == int(usuario_id) 
    ).all() 
    
    print("ITENS CARRINHO:", itens)
    
    total = 0 
    for item in itens: 
        produto = db.query(Product).filter( 
            Product.id == item.produto_id 
        ).first() 
        item.produto = produto 
        total += produto.preco * item.quantidade 
    usuario = db.query(User).filter( 
        User.id == int(usuario_id) ).first() 
    return templates.TemplateResponse( 
        request=request, 
        name="carrinho/checkout.html", 
        context={ 
            "itens": itens, 
            "total": total, 
            "usuario": usuario 
        }
    )

# FINALIZAR COMPRA
@router.post("/finalizar-compra")
def finalizar_compra(

    nome: str = Form(...),
    cep: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),

    frete: str = Form(...),

    pagamento: str = Form(...),

    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)

):

    print("USUARIO:", usuario_id)

    if not usuario_id:

        return RedirectResponse(
            url="/login?next=/finalizar-compra",
            status_code=302
        )

    itens_carrinho = db.query(
        CartItem
    ).filter(
        CartItem.usuario_id == int(usuario_id)
    ).all()

    if not itens_carrinho:

        return RedirectResponse(
            url="/carrinho",
            status_code=302
        )

    total_pedido = 0

    for item in itens_carrinho:

        produto = db.query(
            Product
        ).filter(
            Product.id == item.produto_id
        ).first()

        total_pedido += (
            produto.preco *
            item.quantidade
        )

    status_pagamento = "Pago"

    if pagamento.upper() == "PIX":

        status_pagamento = "Aguardando PIX"


    novo_pedido = Order(

        usuario_id=int(usuario_id),

        total=total_pedido,

        forma_pagamento=pagamento,

        parcelas=1,

        status=status_pagamento

    )

    db.add(novo_pedido)

    db.commit()

    db.refresh(novo_pedido)

    for item in itens_carrinho:

        produto = db.query(
            Product
        ).filter(
            Product.id == item.produto_id
        ).first()

        if produto.estoque < item.quantidade:

            return RedirectResponse(
                url="/carrinho",
                status_code=302
            )

        pedido_item = OrderItem(

            pedido_id=novo_pedido.id,

            produto_id=item.produto_id,

            quantidade=item.quantidade,

            preco=produto.preco

        )

        db.add(pedido_item)

        produto.estoque -= item.quantidade

    for item in itens_carrinho:

        db.delete(item)

    db.commit()

    print("FRETE:", frete)

    print("PAGAMENTO:", pagamento)

    print("FINALIZADO")

    return RedirectResponse(
        url="/meus-pedidos",
        status_code=302
    )
    
# MEUS PEDIDOS
@router.get("/meus-pedidos")
def meus_pedidos(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    # usuário não logado
    if not usuario_id:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    pedidos = db.query(Order).filter(
        Order.usuario_id == int(usuario_id)
    ).all()

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="pedidos/meus_pedidos.html",
        context={
            "pedidos": pedidos,
            "usuario": usuario
        }
    )
    

# REMOVER PEDIDO
@router.get("/remover-pedido/{pedido_id}")
def remover_pedido(
    pedido_id: int,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not usuario_id:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    pedido = db.query(Order).filter(
        Order.id == pedido_id,
        Order.usuario_id == int(usuario_id)
    ).first()

    if pedido:

        # remover itens do pedido
        for item in pedido.itens:
            db.delete(item)

        # remover pedido
        db.delete(pedido)

        db.commit()

    return RedirectResponse(
        url="/meus-pedidos",
        status_code=302
    )

# COMPRAR AGORA
@router.get("/comprar-agora/{produto_id}")
def comprar_agora(
    produto_id: int,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    # usuário não logado
    if not usuario_id:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    produto = db.query(Product).filter(
        Product.id == produto_id
    ).first()

    if not produto:

        return RedirectResponse(
            url="/produtos",
            status_code=302
        )

    # verificar se já existe no carrinho
    item = db.query(CartItem).filter(
        CartItem.usuario_id == int(usuario_id),
        CartItem.produto_id == produto_id
    ).first()

    if item:

        item.quantidade += 1

    else:

        novo_item = CartItem(
            usuario_id=int(usuario_id),
            produto_id=produto_id,
            quantidade=1
        )

        db.add(novo_item)

    db.commit()

    # vai direto checkout
    return RedirectResponse(
        url="/checkout",
        status_code=302
    )
    
# CONSULTAR CARRINHO PARA FASHION IA
@router.get("/fashion-ia/carrinho")
def fashion_ia_carrinho(
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not usuario_id:

        return {
            "tem_carrinho": False
        }

    itens = db.query(CartItem).filter(
        CartItem.usuario_id == int(usuario_id)
    ).all()

    if not itens:

        return {
            "tem_carrinho": False
        }

    quantidade = 0
    total = 0

    for item in itens:

        produto = db.query(Product).filter(
            Product.id == item.produto_id
        ).first()

        quantidade += item.quantidade

        total += (
            produto.preco *
            item.quantidade
        )

    return {

        "tem_carrinho": True,

        "quantidade": quantidade,

        "total": round(total, 2)

    }
    
    
#fashion-ia pedidos
@router.get("/fashion-ia/pedidos")
def fashion_ia_pedidos(
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not usuario_id:

        return {
            "tem_pedidos": False
        }

    pedidos = db.query(Order).filter(
        Order.usuario_id == int(usuario_id)
    ).order_by(Order.id.desc()).limit(3).all()

    if not pedidos:

        return {
            "tem_pedidos": False
        }

    lista_pedidos = []

    for pedido in pedidos:

        lista_pedidos.append({

            "id": pedido.id,

            "status": pedido.status,

            "total": float(pedido.total)

        })

    return {

        "tem_pedidos": True,

        "pedidos": lista_pedidos

    }

#fashion-ia notificações    
@router.get("/fashion-ia/notificacoes")
def fashion_ia_notificacoes(
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not usuario_id:

        return {
            "tem_notificacao": False
        }

    pedido = db.query(Order).filter(
        Order.usuario_id == int(usuario_id)
    ).order_by(
        Order.criado_em.desc()
    ).first()

    if not pedido:

        return {
            "tem_notificacao": False
        }

    return {

        "tem_notificacao": True,

        "pedido_id": pedido.id,

        "status": pedido.status

    }

#Admin Pedidos        
@router.get("/admin/pedidos")
def admin_pedidos(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    pedidos = db.query(Order)\
        .order_by(Order.criado_em.desc())\
        .all()

    return templates.TemplateResponse(
        request=request,
        name="admin/pedidos.html",
        context={
            "pedidos": pedidos,
            "usuario": usuario
        }
    )

@router.post("/admin/pedidos/{pedido_id}/status")
def atualizar_status_pedido(

    pedido_id: int,

    status: str = Form(...),

    db: Session = Depends(get_db)

):

    pedido = db.query(Order).filter(
        Order.id == pedido_id
    ).first()

    if pedido:

        pedido.status = status

        db.commit()

    return RedirectResponse(
        url="/admin/pedidos",
        status_code=302
    )

