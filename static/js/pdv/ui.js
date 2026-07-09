// ==============================================
// LOJA FASHION PDV
// Interface do Usuário
// ==============================================

const UI = {

    tabela: null,

    total: null,

    quantidade: null,

    iniciar(){

        this.tabela = document.getElementById(
            "tabela_produtos"
        );

        this.total = document.getElementById(
            "valor_total"
        );

        this.quantidade = document.getElementById(
            "quantidade_itens"
        );

        EventBus.on(

            Eventos.CARRINHO_ATUALIZADO,

            this.renderizar.bind(this)

        );

        Logger.sucesso(

            "UI iniciada."

        );

        Developer.registrarModulo(

            "UI"

        );

    },

    renderizar(carrinho){

        this.renderizarProdutos(carrinho);

        this.renderizarTotal(carrinho);

        this.renderizarQuantidade(carrinho);

    },

    renderizarProdutos(carrinho){

        this.tabela.innerHTML = "";

        carrinho.produtos.forEach(produto=>{

            const linha = document.createElement("tr");

            linha.innerHTML = `

                <td>${produto.codigo}</td>

                <td>${produto.nome}</td>

                <td>${produto.quantidade}</td>

                <td>R$ ${produto.preco.toFixed(2)}</td>

                <td>R$ ${(produto.preco * produto.quantidade).toFixed(2)}</td>

            `;

            this.tabela.appendChild(linha);

        });

    },

    renderizarTotal(carrinho){

        this.total.innerHTML =

            `R$ ${carrinho.total.toFixed(2)}`;

    },

    renderizarQuantidade(carrinho){

        if(this.quantidade){

            this.quantidade.innerHTML =

                carrinho.quantidadeItens;

        }

    }

};