// ==============================================
// LOJA FASHION PDV
// EventBus
// Versão: 2.0
// ==============================================

const EventBus = {

    eventos: {},

    on(nomeEvento, callback){

        if(!this.eventos[nomeEvento]){

            this.eventos[nomeEvento] = [];

        }

        if(!this.eventos[nomeEvento].includes(callback)){

            this.eventos[nomeEvento].push(callback);

        }

    },

    emit(nomeEvento, dados = null){

        if(!this.eventos[nomeEvento]) return;

        Logger.info(`Evento: ${nomeEvento}`);

        this.eventos[nomeEvento].forEach(callback => {

            try{

                callback(dados);

            }catch(error){

                Logger.error(error);

            }

        });

    },

    off(nomeEvento, callback){

        if(!this.eventos[nomeEvento]) return;

        this.eventos[nomeEvento] = this.eventos[nomeEvento].filter(
            evento => evento !== callback
        );

    },

    limpar(){

        this.eventos = {};

        Logger.info("Eventos removidos.");

    }

};