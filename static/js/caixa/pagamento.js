// ========================================
// LOJA FASHION
// PAGAMENTOS
// ========================================

const Pagamento = {

    iniciar(){

        this.forma = document.getElementById(
            "forma_pagamento"
        );

    },

    obterForma(){

        return this.forma.value;

    },

    finalizar(){

        const forma = this.obterForma();

        switch(forma){

            case "Pix":

                EventBus.emit(
                    Eventos.PAGAMENTO_PIX
                );

                break;

            case "Dinheiro":

                EventBus.emit(
                    Eventos.PAGAMENTO_DINHEIRO
                );

                break;

            case "Cartão Crédito":

                EventBus.emit(
                    Eventos.PAGAMENTO_CREDITO
                );

                break;

            case "Cartão Débito":

                EventBus.emit(
                    Eventos.PAGAMENTO_DEBITO
                );

                break;

        }

    }

};