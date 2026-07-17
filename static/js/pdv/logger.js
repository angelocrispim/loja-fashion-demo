// ==============================================
// LOJA FASHION PDV
// Logger
// ==============================================

const Logger = {

    horario(){

        return new Date().toLocaleTimeString("pt-BR");

    },

    registrar(consoleMetodo, icone, tipo, mensagem){

        consoleMetodo(

            `[${this.horario()}] ${icone} ${tipo}:`,

            mensagem

        );

    },

    info(mensagem){

        if(!CONFIG.sistema.developerMode) return;

        this.registrar(console.info, "📘", "INFO", mensagem);

    },

    sucesso(mensagem){

        if(!CONFIG.sistema.developerMode) return;

        this.registrar(console.log, "✅", "SUCESSO", mensagem);

    },

    alerta(mensagem){

        if(!CONFIG.sistema.developerMode) return;

        this.registrar(console.warn, "⚠️", "ALERTA", mensagem);

    },

    erro(mensagem){

        this.registrar(console.error, "❌", "ERRO", mensagem);

    }

};