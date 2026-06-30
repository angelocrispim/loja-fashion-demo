// ========================================
// LOJA FASHION
// EVENT BUS
// ========================================

const EventBus = {

    eventos:{},

    on(nomeEvento, callback){

        if(!this.eventos[nomeEvento]){

            this.eventos[nomeEvento]=[];

        }

        this.eventos[nomeEvento].push(callback);

    },

    emit(nomeEvento,dados){

        if(!this.eventos[nomeEvento]){

            return;

        }

        this.eventos[nomeEvento].forEach(

            callback=>callback(dados)

        );

    },

    off(nomeEvento,callback){

        if(!this.eventos[nomeEvento]){

            return;

        }

        this.eventos[nomeEvento] =
            this.eventos[nomeEvento].filter(

                evento => evento !== callback

            );

    }

};