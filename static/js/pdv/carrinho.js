// ==============================================
// LOJA FASHION PDV
// Carrinho de Compras
// Versão: 2.0
// ==============================================

const Carrinho = {

    iniciar(){

        Logger.info(

            "Carrinho iniciado."

        );

        Developer.registrarModulo(

            "Carrinho"

        );


        EventBus.on(

            Eventos.PRODUTO_LIDO,

            this.adicionarProduto.bind(this)

        );

    },

    adicionarProduto(produto){

        Developer.registrarEvento(

            "Carrinho",

            `Adicionar ${produto.nome}`

        );

        //Logger.info(

            //`Adicionando: ${produto.nome}`

        //);

        const existente = PDV.carrinho.produtos.find(

            item => item.id === produto.id

        );

        if(existente){

            existente.quantidade++;

        }

        else{

            PDV.carrinho.produtos.push({

                id: produto.id,

                codigo: produto.codigo,

                nome: produto.nome,

                preco: produto.preco,

                quantidade: 1

            });

        }

        this.recalcularCarrinho();

    },

    recalcularCarrinho(){

        Developer.registrarEvento(

            "Carrinho",

            "Carrinho recalculado"

        );

        let subtotal = 0;

        let quantidade = 0;

        PDV.carrinho.produtos.forEach(produto=>{

            subtotal +=

                produto.preco *

                produto.quantidade;

            quantidade +=

                produto.quantidade;

        });

        PDV.carrinho.subtotal = subtotal;

        PDV.carrinho.quantidadeItens = quantidade;

        PDV.carrinho.total =

            subtotal -

            PDV.carrinho.desconto;

        EventBus.emit(

            Eventos.CARRINHO_ATUALIZADO,

            PDV.carrinho

        );

    },

    limpar(){

        Developer.registrarEvento(

            "Carrinho",

            "Venda cancelada"

        );

        PDV.limparVenda();

        EventBus.emit(

            Eventos.CARRINHO_ATUALIZADO,

            PDV.carrinho

        );

    }

};