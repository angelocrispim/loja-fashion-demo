// ==============================================
// LOJA FASHION PDV
// EventBus
// Versão: 2.0
// ==============================================

const EventBus = {

    eventos: {},

    iniciar(){

        Logger.info(

            "EventBus iniciado."

        );

    },

    on(nomeEvento, callback){

        if(!this.eventos[nomeEvento]){

            this.eventos[nomeEvento] = [];

        }

        this.eventos[nomeEvento].push(

            callback

        );

    },

    emit(nomeEvento, dados = null){

        if(!this.eventos[nomeEvento]){

            return;

        }

        Logger.info(

            `Evento: ${nomeEvento}`

        );

        this.eventos[nomeEvento].forEach(

            callback => callback(dados)

        );

    },

    off(nomeEvento, callback){

        if(!this.eventos[nomeEvento]){

            return;

        }

        this.eventos[nomeEvento] =

            this.eventos[nomeEvento].filter(

                evento => evento !== callback

            );

    }

};