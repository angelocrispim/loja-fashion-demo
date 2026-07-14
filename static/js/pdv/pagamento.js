// ==============================================
// LOJA FASHION PDV
// Pagamentos
// Versão 2.0
// ==============================================

const Pagamento = {

    forma: "Dinheiro",

    valorRecebido: 0,

    troco: 0,

    parcelas: 1,

    iniciar(){

        this.selectForma = document.getElementById(
            "forma_pagamento"
        );

        this.inputValor = document.getElementById(
            "valor_recebido"
        );

        this.lblTroco = document.getElementById(
            "troco"
        );

        this.inputParcelas = document.getElementById(
            "parcelas"
        );

        if(this.selectForma){

            this.selectForma.addEventListener(

                "change",

                ()=>{

                    this.alterarForma();

                }

            );

        }

        if(this.inputValor){

            this.inputValor.addEventListener(

                "input",

                ()=>{

                    this.calcularTroco();

                }

            );

        }

        Logger.sucesso(

            "Pagamento iniciado."

        );

    },

    alterarForma(){

        this.forma = this.selectForma.value;

        if(this.forma === "Dinheiro"){

            this.inputValor.disabled = false;

        }

        else{

            this.inputValor.value = "";

            this.inputValor.disabled = true;

            this.lblTroco.innerHTML = "R$ 0,00";

        }

    },

    calcularTroco(){

        const recebido = parseFloat(

            this.inputValor.value || 0

        );

        const total = PDV.carrinho.total;

        this.valorRecebido = recebido;

        this.troco = recebido - total;

        if(this.troco < 0){

            this.troco = 0;

        }

        this.lblTroco.innerHTML =

            `R$ ${this.troco.toFixed(2)}`;

    },

    obterDados(){

        return{

            forma: this.forma,

            valorRecebido: this.valorRecebido,

            troco: this.troco,

            parcelas: this.parcelas

        };

    },

    processarPagamento(){

        if(PDV.pagamento.forma === "PIX"){

            this.gerarPix();

            return;

        }

        Venda.finalizar();

    },

};