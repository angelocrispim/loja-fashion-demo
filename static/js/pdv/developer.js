// ==============================================
// LOJA FASHION PDV
// Developer Tools
// ==============================================

const Developer = {

    modulos: [],

    eventos: [],

    ativo(){

        return CONFIG.sistema.developerMode;

    },

    iniciar(){

        if(!this.ativo()) return;

        Logger.info("Developer Mode ativado.");

    },

    registrarModulo(nome){

        if(!this.ativo()) return;

        this.modulos.push({

            nome,

            horario: new Date().toLocaleTimeString("pt-BR")

        });

        Logger.sucesso(`${nome} carregado.`);

    },

    registrarEvento(modulo, descricao){

        if(!this.ativo()) return;

        this.eventos.push({

            modulo,

            descricao,

            horario: new Date().toLocaleTimeString("pt-BR")

        });

        Logger.info(`${modulo}: ${descricao}`);

    },

    listarModulos(){

        if(!this.ativo()) return;

        console.table(this.modulos);

    },

    listarEventos(){

        if(!this.ativo()) return;

        console.table(this.eventos);

    }

};