// ==============================================
// LOJA FASHION PDV
// Logger
// ==============================================

const Logger = {

    horario(){

        return new Date().toLocaleTimeString();

    },

    info(mensagem){

        if(!CONFIG.sistema.developerMode){

            return;

        }

        console.log(

            `[${this.horario()}] 📘 INFO:`,

            mensagem

        );

    },

    sucesso(mensagem){

        if(!PDV.sistema.developerMode){

            return;

        }

        console.log(

            `[${this.horario()}] ✅ SUCESSO:`,

            mensagem

        );

    },

    alerta(mensagem){

        if(!PDV.sistema.developerMode){

            return;

        }

        console.warn(

            `[${this.horario()}] ⚠️ ALERTA:`,

            mensagem

        );

    },

    erro(mensagem){

        console.error(

            `[${this.horario()}] ❌ ERRO:`,

            mensagem

        );

    }

};