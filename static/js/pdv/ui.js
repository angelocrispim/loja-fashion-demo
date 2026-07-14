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

        this.renderizar(

            PDV.carrinho

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

    },

    reset(){

        document.getElementById("desconto").value = 0;

        document.getElementById("forma_pagamento").value = "Dinheiro";

        document.getElementById("valor_recebido").value = "";

        document.getElementById("troco").innerHTML = "R$ 0,00";

        PDV.pagamento.forma = "Dinheiro";

        PDV.pagamento.valorRecebido = 0;

        PDV.pagamento.troco = 0;

        PDV.carrinho.desconto = 0;

        this.renderizar(PDV.carrinho);

        const input = document.getElementById("codigo_produto");

        if(input){

            input.value = "";

            input.focus();

        }

    }

};