// ==============================================
// LOJA FASHION PDV
// Venda
// Versão: 2.0
// ==============================================

const Venda = {

    iniciar(){

        Logger.sucesso(
            "Módulo Venda iniciado."
        );

    },

    async finalizar(){

        // Não permite vender carrinho vazio
        if(PDV.carrinho.produtos.length === 0){

            alert(
                "Nenhum produto no carrinho."
            );

            return;

        }

        const dados = {

            funcionario_id: PDV.operador.id,

            pagamento: PDV.pagamento.forma,

            desconto: PDV.carrinho.desconto,

            total: PDV.carrinho.total,

            produtos: PDV.carrinho.produtos,

            parcelas: PDV.pagamento.parcelas,

            valor_parcela:
                PDV.pagamento.parcelas > 0
                ? PDV.carrinho.total /
                  PDV.pagamento.parcelas
                : PDV.carrinho.total

        };

        Logger.info(
            "Enviando venda..."
        );

        const resposta = await API.request(

            "/caixa/finalizar-venda",

            {

                method: "POST",

                headers: {

                    "Content-Type":"application/json"

                },

                body: JSON.stringify(dados)

            }

        );

        if(!resposta.success){

            alert(

                "Erro ao finalizar venda."

            );

            return;

        }

        Logger.sucesso(

            `Venda ${resposta.venda_id} realizada.`

        );

        alert(

            `Venda Nº ${resposta.venda_id} realizada com sucesso.`

        );

        this.limpar();

    },

    cancelar(){

        if(

            confirm(

                "Cancelar venda atual?"

            )

        ){

            this.limpar();

        }

    },

    limpar(){

        Carrinho.limpar();

        document.getElementById(

            "codigo_produto"

        ).focus();

    }

};