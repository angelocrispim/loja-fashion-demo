// ========================================
// LOJA FASHION
// MÓDULO CARRINHO
// ========================================

//const Carrinho = {

//    produtos: [],

//    desconto: 0,

//    vendaPixId: null,

//    subtotal: 0,

//    total: 0

//};

// ========================================
// ADICIONAR PRODUTO
// ========================================

console.log("VERSÃO NOVA DO CARRINHO");

console.log(PDV);

function adicionarProduto(produto){

    // Procura se o produto já existe no carrinho
    const existente = PDV.carrinho.produtos.find(

        p => p.id === produto.id

    );

    // Se já existe aumenta a quantidade
    if(existente){

        existente.quantidade++;

    }

    // Se não existe adiciona
    else{

        PDV.carrinho.produtos.push({

            id: produto.id,

            codigo: produto.codigo,

            nome: produto.nome,

            preco: produto.preco,

            quantidade: 1

        });

    }

    registrarEvento(

        `Produto adicionado: ${produto.nome}`

    );

    renderizarCarrinho();

}

// ========================================
// CALCULAR TOTAL
// ========================================

function calcularTotal(){

    return PDV.carrinho.produtos.reduce(

        (total, produto)=>{

            return total +

                produto.preco *

                produto.quantidade;

        },

        0

    );

}

// ========================================
// ATUALIZAR RESUMO
// ========================================

function atualizarResumo(){

    PDV.carrinho.subtotal = calcularTotal();

    PDV.carrinho.total =

        PDV.carrinho.subtotal -

        PDV.carrinho.desconto;

    document.getElementById(

        "valor_total"

    ).innerText =

        `R$ ${PDV.carrinho.subtotal.toFixed(2)}`;

    document.getElementById(

        "valor_final"

    ).innerText =

        `R$ ${PDV.carrinho.total.toFixed(2)}`;

}

// ========================================
// RENDERIZAR CARRINHO
// ========================================

function renderizarCarrinho(){

    const tabela = document.getElementById("tabela_produtos");

    tabela.innerHTML = "";

    PDV.carrinho.produtos.forEach(produto => {

        const linha = document.createElement("tr");

        linha.innerHTML = `

            <td>${produto.codigo}</td>

            <td>${produto.nome}</td>

            <td>

                <button
                    class="btn-qtd"
                    onclick="diminuirQuantidade(${produto.id})">

                    -

                </button>

                <span class="qtd-produto">

                    ${produto.quantidade}

                </span>

                <button
                    class="btn-qtd"
                    onclick="aumentarQuantidade(${produto.id})">

                    +

                </button>

            </td>

            <td>R$ ${produto.preco.toFixed(2)}</td>

            <td>R$ ${(produto.preco * produto.quantidade).toFixed(2)}</td>

            <td>

                <button
                    class="btn-remover"
                    onclick="removerProduto(${produto.id})">

                    <i class="fas fa-trash"></i>

                    Remover

                </button>

            </td>

        `;

        tabela.appendChild(linha);

    });

    atualizarResumo();

}

// ========================================
// REMOVER PRODUTO
// ========================================

function removerProduto(id){

    PDV.carrinho.produtos =
        PDV.carrinho.produtos.filter(

            produto => produto.id !== id

        );

        registrarEvento(

            `Produto removido`

        );

    renderizarCarrinho();

}

// ========================================
// AUMENTAR QUANTIDADE
// ========================================

function aumentarQuantidade(id){

    const produto = PDV.carrinho.produtos.find(

        p => p.id === id

    );

    if(!produto) return;

    produto.quantidade++;

    registrarEvento(

        "Quantidade aumentada"

    );

    renderizarCarrinho();

}

// ========================================
// DIMINUIR QUANTIDADE
// ========================================

function diminuirQuantidade(id){

    const produto = PDV.carrinho.produtos.find(

        p => p.id === id

    );

    if(!produto) return;

    if(produto.quantidade > 1){

        produto.quantidade--;

    }else{

        removerProduto(id);

        return;

    }

    registrarEvento(

        "Quantidade diminuída"

    );

    renderizarCarrinho();

}

// ========================================
// SOM DO LEITOR
// ========================================

function tocarBeep(){

    const audio = new Audio(
        "/static/audio/beep.mp3"
    );

    audio.play();

}

EventBus.on(

    Eventos.PRODUTO_LIDO,

    (produto)=>{

        adicionarProduto(produto);

    }

);