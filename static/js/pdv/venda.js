// ==============================================
// LOJA FASHION PDV
// Venda
// Versão: 2.0
// ==============================================

const Venda = {

    btnFinalizar: null,

    btnCancelar: null,

    iniciar(){

        Logger.sucesso(
            "Módulo Venda iniciado."
        );

        this.btnFinalizar = document.getElementById(
            "btn_finalizar"
        );

        this.btnCancelar = document.getElementById(
            "btn_cancelar"
        );

        if(this.btnCancelar){

            this.btnCancelar.addEventListener(

                "click",

                ()=>this.cancelar()

            );

        }

    },

    montarVenda(){

        const pagamento = Pagamento.obterDados();

        return{

            funcionario_id: PDV.operador.id,

            pagamento: pagamento.forma,

            desconto: PDV.carrinho.desconto,

            total: PDV.carrinho.total,

            parcelas: pagamento.parcelas,

            valor_parcela:

                pagamento.parcelas > 0

                ? PDV.carrinho.total /

                pagamento.parcelas

                : PDV.carrinho.total,

            valor_recebido:

                pagamento.valorRecebido,

            troco:

                pagamento.troco,

            produtos:

                PDV.carrinho.produtos.map(

                    produto=>({

                        id:produto.id,

                        quantidade:produto.quantidade

                    })

                )

        };

    },

    async finalizar(){

        if(PDV.carrinho.produtos.length === 0){

            alert(

                "Nenhum produto no carrinho."

            );

            return;

        }

        const dados = this.montarVenda();

        Logger.info(

            "Enviando venda..."

        );

        Developer.registrarEvento(

            "Venda",

            "Enviando venda ao servidor"

        );

        try{

            const resposta = await API.finalizarVenda(

                dados

            );

            if(!resposta.success){

                alert(

                    "Erro ao finalizar venda."

                );

                return;

            }

            Logger.sucesso(

                `Venda Nº ${resposta.venda_id} criada.`

            );

            Developer.registrarEvento(

                "Venda",

                `Venda ${resposta.venda_id} criada`

            );

            EventBus.emit(

                Eventos.VENDA_FINALIZADA,

                resposta

            );

            Pagamento.abrirComprovante(resposta);

        }

        catch(erro){

            Logger.erro(

                erro.message

            );

            alert(

                "Erro ao comunicar com o servidor."

            );

        }

    },

    cancelar(){

        if(

            confirm(

                "Deseja cancelar esta venda?"

            )

        ){

            this.limpar();

        }

    },

    limpar(){

        Carrinho.limpar();

        UI.reset();

    }

};