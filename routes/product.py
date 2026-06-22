from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi import Cookie
from fastapi import UploadFile, File
from fastapi import Body
import shutil
from sqlalchemy import or_

from database import SessionLocal
from models.product import Product, ProductImage
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
# PÁGINA PRODUTOS
# =========================
@router.get("/produtos")
def listar_produtos(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    produtos = db.query(Product).all()

    usuario = None

    if usuario_id:
        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produtos.html",
        context={
            "produtos": produtos,
            "usuario": usuario,
            "titulo": "Todos os Produtos"
        }
    )


# =========================
# PÁGINA CADASTRAR PRODUTO
# =========================

@router.get("/admin/cadastrar-produtos")
def pagina_cadastrar_produto(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="admin/cadastrar_produto.html",
        context={}
    )


# =========================
# CADASTRAR PRODUTO
# =========================
@router.post("/admin/produtos")
def cadastrar_produto(
    request: Request,
    codigo: str = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),

    imagem: UploadFile = File(...),      # Foto principal
    galeria: list[UploadFile] = File([]), # Galeria

    categoria: str = Form(...),
    estoque: int = Form(...),

    db: Session = Depends(get_db)
):

    # =========================
    # FOTO PRINCIPAL
    # =========================

    caminho_imagem = f"static/uploads/{imagem.filename}"

    with open(caminho_imagem, "wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)

    novo_produto = Product(
        codigo=codigo,
        nome=nome,
        descricao=descricao,
        preco=preco,
        imagem=f"/static/uploads/{imagem.filename}",
        categoria=categoria,
        estoque=estoque
    )

    db.add(novo_produto)

    db.commit()

    db.refresh(novo_produto)

    # =========================
    # GALERIA DE FOTOS
    # =========================

    for foto in galeria:

        if foto.filename:

            caminho_galeria = f"static/uploads/{foto.filename}"

            with open(caminho_galeria, "wb") as buffer:
                shutil.copyfileobj(foto.file, buffer)

            nova_imagem = ProductImage(
                produto_id=novo_produto.id,
                imagem=f"/static/uploads/{foto.filename}"
            )

            db.add(nova_imagem)

    db.commit()

    return RedirectResponse(
        url="/produtos",
        status_code=302
    )


# =========================
# DETALHE PRODUTO
# =========================
@router.get("/produto/{produto_id}")
def pagina_produto(
    produto_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:
        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    produto = db.query(Product).filter(
        Product.id == produto_id
    ).first()

    imagens = db.query(ProductImage).filter(
        ProductImage.produto_id == produto.id
    ).all()
    
    produtos_relacionados = db.query(Product).filter(
        Product.categoria == produto.categoria,
        Product.id != produto.id
    ).limit(4).all()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produto.html",
        context={
            "request": request,
            "produto": produto,
            "usuario": usuario,
            "imagens": imagens,
            "produtos_relacionados": produtos_relacionados
        }
    )
    
# =========================
# BUSCAR PRODUTO POR CÓDIGO
# =========================

@router.get("/produto/codigo/{codigo}")
def buscar_produto_codigo(
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
        "codigo": produto.codigo,
        "nome": produto.nome,
        "preco": float(produto.preco)
    }
    
# =========================
# MASCULINO
# =========================

@router.get("/mens")
def produtos_masculinos(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    produtos = db.query(Product).filter(
        Product.categoria == "Masculino"
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produtos.html",
        context={
            "produtos": produtos,
            "usuario": usuario,
            "titulo": "Moda Masculina"
        }
    )
    
# =========================
# FEMININO
# =========================

@router.get("/mulher")
def produtos_femininos(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    produtos = db.query(Product).filter(
        Product.categoria == "Feminino"
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produtos.html",
        context={
            "produtos": produtos,
            "usuario": usuario,
            "titulo": "Moda Feminina"
        }
    )
    
# =========================
# CALÇADOS
# =========================

@router.get("/calcados")
def produtos_calcados(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    produtos = db.query(Product).filter(
        Product.categoria == "Calçados"
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produtos.html",
        context={
            "produtos": produtos,
            "usuario": usuario,
            "titulo": "Calçados"
        }
    )
    
# =========================
# INFANTIL
# =========================

@router.get("/infantil")
def produtos_infantil(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    produtos = db.query(Product).filter(
        Product.categoria == "Infantil"
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produtos.html",
        context={
            "produtos": produtos,
            "usuario": usuario,
            "titulo": "Moda Infantil"
        }
    )
    
# =========================
# ACESSÓRIOS
# =========================

@router.get("/acessorios")
def produtos_acessorios(
    request: Request,
    db: Session = Depends(get_db),
    usuario_id: str = Cookie(None)
):

    usuario = None

    if usuario_id:

        usuario = db.query(User).filter(
            User.id == int(usuario_id)
        ).first()

    produtos = db.query(Product).filter(
        Product.categoria == "Acessórios"
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="produtos/produtos.html",
        context={
            "produtos": produtos,
            "usuario": usuario,
            "titulo": "Acessórios"
        }
    )
    
###############################################
# AGENTE IA
###############################################

@router.post("/fashion-ia")
def fashion_ia(
    dados: dict = Body(...),
    db: Session = Depends(get_db)
):

    mensagem = dados.get("mensagem", "").lower()

    produtos = db.query(Product).filter(

        or_(
            Product.nome.ilike(f"%{mensagem}%"),
            Product.categoria.ilike(f"%{mensagem}%")
        )

    ).limit(3).all()

    if produtos:

        resposta = ""

        for produto in produtos:

            resposta += f"""
            <div style="margin-bottom:15px;">

                🛍️ <strong>{produto.nome}</strong><br>

                💰 R$ {produto.preco:.2f}<br>

                <a href="/adicionar-carrinho/{produto.id}"
                   style="
                        display:inline-block;
                        margin-top:8px;
                        padding:8px 12px;
                        background:#224F34;
                        color:white;
                        border-radius:8px;
                        text-decoration:none;
                   ">

                   🛒 Adicionar ao Carrinho

                </a>

            </div>
            """

    else:
        
        resposta = """
        🤖 Desculpe, ainda não consegui encontrar esse produto
        ou responder essa dúvida.<br><br>

        Deseja falar com nossa equipe?<br><br>

        <a href="https://wa.me/5581999999999"
        target="_blank"
        style="
                display:inline-block;
                padding:8px 12px;
                background:#25D366;
                color:white;
                border-radius:8px;
                text-decoration:none;
                margin-right:8px;
        ">

        📱 WhatsApp

        </a>

        <a href="/contato"
        style="
                display:inline-block;
                padding:8px 12px;
                background:#224F34;
                color:white;
                border-radius:8px;
                text-decoration:none;
        ">

        📧 Contato

        </a>
        """

    return {
        "resposta": resposta
    }