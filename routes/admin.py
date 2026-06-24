from fastapi import (
    APIRouter,
    Request,
    Depends,
    Cookie,
    Form,
    UploadFile,
    File
)

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

import shutil
import os
import uuid

from database import SessionLocal

from models.user import User
from models.product import Product, ProductImage
from models.order import Order
from models.cart_item import CartItem
from models.order_item import OrderItem
from models.sale import Sale
from models.employee import Employee
from models.store_config import StoreConfig

from utils.context import contexto_admin


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ====================================
# DATABASE
# ====================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ====================================
# VERIFICAR ADMIN
# ====================================

def verificar_admin(usuario_id, db):

    if not usuario_id:
        return None

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    if not usuario:
        return None

    if not usuario.is_admin and not usuario.is_superadmin:
        return None

    return usuario


# ====================================
# PAINEL ADMIN
# ====================================

@router.get("/admin")
def painel_admin(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = verificar_admin(usuario_id, db)

    if not usuario:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    total_usuarios = db.query(User).count()

    total_produtos = db.query(Product).count()

    total_pedidos = db.query(Order).count()

    pedidos = db.query(Order).order_by(
        Order.id.desc()
    ).limit(5).all()

    total_vendas = sum(
        pedido.total for pedido in pedidos
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={
            "usuario": usuario,
            "total_usuarios": total_usuarios,
            "total_produtos": total_produtos,
            "total_pedidos": total_pedidos,
            "total_vendas": total_vendas,
            "pedidos": pedidos
        }
    )

# ====================================
# CLIENTES
# ====================================
@router.get("/admin/clientes")
def listar_clientes(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    contexto = contexto_admin(
        db,
        usuario_id
    )

    clientes = db.query(
        User
    ).filter(
        User.is_admin == False
    ).all()

    contexto["clientes"] = clientes

    return templates.TemplateResponse(
        request=request,
        name="admin/clientes.html",
        context=contexto
    )

# ====================================
# LISTAR PRODUTOS
# ====================================

@router.get("/admin/produtos")
def admin_produtos(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = verificar_admin(usuario_id, db)

    if not usuario:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    produtos = db.query(Product).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/produtos.html",
        context={
            "usuario": usuario,
            "produtos": produtos
        }
    )


# ====================================
# PÁGINA CADASTRAR PRODUTO
# ====================================

@router.get("/admin/cadastrar-produto")
def pagina_cadastrar_produto(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = verificar_admin(usuario_id, db)

    if not usuario:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="admin/cadastrar_produto.html",
        context={
            "usuario": usuario
        }
    )


# ====================================
# SALVAR PRODUTO
# ====================================

@router.post("/admin/cadastrar-produto")
def salvar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    categoria: str = Form(...),
    estoque: int = Form(...),
    imagens: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):

    # cria pasta uploads
    os.makedirs(
        "static/uploads",
        exist_ok=True
    )

    caminhos_imagens = []

    # ====================================
    # SALVAR IMAGENS
    # ====================================

    for imagem in imagens:

        extensao = imagem.filename.split(".")[-1]

        nome_arquivo = (
            f"{uuid.uuid4()}.{extensao}"
        )

        caminho = (
            f"static/uploads/{nome_arquivo}"
        )

        with open(caminho, "wb") as buffer:
            shutil.copyfileobj(
                imagem.file,
                buffer
            )

        caminhos_imagens.append(
            "/" + caminho
        )

    # ====================================
    # IMAGEM PRINCIPAL
    # ====================================

    imagem_principal = caminhos_imagens[0]

    # ====================================
    # CRIAR PRODUTO
    # ====================================

    novo_produto = Product(
        nome=nome,
        descricao=descricao,
        preco=preco,
        imagem=imagem_principal,
        categoria=categoria,
        estoque=estoque
    )

    db.add(novo_produto)

    db.commit()

    db.refresh(novo_produto)

    # ====================================
    # GALERIA DE IMAGENS
    # ====================================

    for caminho_imagem in caminhos_imagens:

        nova_imagem = ProductImage(
            produto_id=novo_produto.id,
            imagem=caminho_imagem
        )

        db.add(nova_imagem)

    db.commit()

    return RedirectResponse(
        url="/admin/produtos",
        status_code=302
    )


# ====================================
# EDITAR PRODUTO
# ====================================

@router.get("/admin/editar-produto/{produto_id}")
def pagina_editar_produto(
    produto_id: int,
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = verificar_admin(usuario_id, db)

    if not usuario:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    produto = db.query(Product).filter(
        Product.id == produto_id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="admin/editar_produto.html",
        context={
            "usuario": usuario,
            "produto": produto
        }
    )


# ====================================
# SALVAR EDIÇÃO
# ====================================

@router.post("/admin/editar-produto/{produto_id}")
def salvar_edicao_produto(
    produto_id: int,
    codigo: str = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    categoria: str = Form(...),
    estoque: int = Form(...),
    db: Session = Depends(get_db)
):

    produto = db.query(Product).filter(
        Product.id == produto_id
    ).first()

    if produto:

        produto.codigo = codigo
        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.categoria = categoria
        produto.estoque = estoque

        db.commit()

    return RedirectResponse(
        url="/admin/produtos",
        status_code=302
    )


# ====================================
# EXCLUIR PRODUTO
# ====================================

@router.get("/admin/excluir-produto/{produto_id}")
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):

    produto = db.query(Product).filter(
        Product.id == produto_id
    ).first()

    if produto:
    
        imagens = db.query(ProductImage).filter(
            ProductImage.produto_id == produto.id
        ).all()

        for img in imagens:

            caminho = img.imagem.replace("/", "")

            if os.path.exists(caminho):
                os.remove(caminho)

            db.delete(img)

        # remover carrinhos
        db.query(CartItem).filter(
            CartItem.produto_id == produto.id
        ).delete()

        # remover pedidos
        db.query(OrderItem).filter(
            OrderItem.produto_id == produto.id
        ).delete()

        caminho_principal = produto.imagem.replace("/", "")

        if os.path.exists(caminho_principal):
            os.remove(caminho_principal)

        db.delete(produto)

    db.commit()

    return RedirectResponse(
        url="/admin/produtos",
        status_code=302
    )


# ====================================
# PEDIDOS ADMIN
# ====================================

@router.get("/admin/pedidos")
def admin_pedidos(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = verificar_admin(usuario_id, db)

    if not usuario:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    pedidos = db.query(Order).order_by(
        Order.id.desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/pedidos.html",
        context={
            "usuario": usuario,
            "pedidos": pedidos
        }
    )


# ====================================
# ALTERAR STATUS PEDIDO
# ====================================

@router.get("/admin/pedido/status/{pedido_id}/{status}")
def alterar_status_pedido(
    pedido_id: int,
    status: str,
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
    
# =========================================
# DETALHE PEDIDO
# =========================================
@router.get("/admin/pedido/{pedido_id}")
def detalhe_pedido(
    pedido_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    contexto = contexto_admin(
        db,
        usuario_id
    )

    pedido = db.query(Order).filter(
        Order.id == pedido_id
    ).first()

    contexto["pedido"] = pedido

    return templates.TemplateResponse(
        request=request,
        name="admin/detalhe_pedido.html",
        context=contexto
    )
    
@router.get("/admin/vendas")
def listar_vendas(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    vendas = db.query(Sale)\
        .order_by(Sale.data_venda.desc())\
        .all()

    return templates.TemplateResponse(
        request=request,
        name="admin/vendas.html",
        context={
            "request": request,
            "usuario": usuario,
            "vendas": vendas
        }
    )
    
@router.get("/admin/venda/{venda_id}")
def visualizar_venda(
    venda_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    venda = db.query(Sale).filter(
        Sale.id == venda_id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="admin/detalhe_venda.html",
        context={
            "request": request,
            "usuario": usuario,
            "venda": venda
        }
    )
    
@router.post("/admin/pedido/{pedido_id}/status")
def atualizar_status_pedido(
    pedido_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db)
):

    pedido = db.query(
        Order
    ).filter(
        Order.id == pedido_id
    ).first()

    if pedido:

        pedido.status = status

        db.commit()

    return RedirectResponse(
        f"/admin/pedido/{pedido_id}",
        status_code=302
    )

# =========================================
# CONFIGURAÇÕES
# =========================================    
@router.get("/admin/configuracoes")
def configuracoes_loja(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    contexto = contexto_admin(
        db,
        usuario_id
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/configuracoes.html",
        context=contexto
    )
    
@router.post("/admin/configuracoes")
def salvar_configuracoes(

    nome_loja: str = Form(...),
    telefone: str = Form(...),
    whatsapp: str = Form(...),
    email: str = Form(...),
    instagram: str = Form(...),
    endereco: str = Form(...),
    cidade: str = Form(...),

    logo: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    config = db.query(
        StoreConfig
    ).first()

    if not config:

        config = StoreConfig()

        db.add(config)

    # Upload da logo
    if logo and logo.filename:

        os.makedirs(
            "static/uploads",
            exist_ok=True
        )

        caminho = (
            f"static/uploads/{logo.filename}"
        )

        with open(
            caminho,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                logo.file,
                buffer
            )

        config.logo = "/" + caminho

    # Dados da loja
    config.nome_loja = nome_loja
    config.telefone = telefone
    config.whatsapp = whatsapp
    config.email = email
    config.instagram = instagram
    config.endereco = endereco
    config.cidade = cidade

    db.commit()

    return RedirectResponse(
        "/admin/configuracoes",
        status_code=302
    )
    
# ====================================
# USUÁRIOS
# ====================================

@router.get("/admin/usuarios")
def listar_usuarios(
    request: Request,
    usuario_id: str = Cookie(None),
    db: Session = Depends(get_db)
):

    usuario = verificar_admin(
        usuario_id,
        db
    )

    if not usuario:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    usuarios = db.query(User).order_by(
        User.id.desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/usuarios.html",
        context={
            "usuario": usuario,
            "usuarios": usuarios
        }
    )
    
# ====================================
# criação de tabelas
# ====================================
    
from sqlalchemy import text

@router.get("/criar-campo-cargo")
def criar_campo_cargo(db: Session = Depends(get_db)):

    db.execute(
        text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS cargo VARCHAR DEFAULT 'cliente';
        """)
    )

    db.commit()

    return {"msg": "Campo cargo criado com sucesso"}