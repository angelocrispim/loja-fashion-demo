// ==============================================
// LOJA FASHION PDV
// Developer Tools
// ==============================================

const Developer = {

    modulos: [],

    eventos: [],

    iniciar(){

        if(!CONFIG.sistema.developerMode){

            return;

        }

        Logger.info(

            "Developer Mode ativado."

        );

    },

    registrarModulo(nome){

        if(!CONFIG.sistema.developerMode){

            return;

        }

        this.modulos.push({

            nome,

            horario:new Date()

        });

        console.log(

            `✅ ${nome} carregado.`

        );

    },

    registrarEvento(modulo, descricao){

        if(!CONFIG.sistema.developerMode){

            return;

        }

        this.eventos.push({

            modulo,

            descricao,

            horario:new Date()

        });

        console.log(

            `📌 ${modulo}: ${descricao}`

        );

    },

    listarModulos(){

        console.table(

            this.modulos

        );

    },

    listarEventos(){

        console.table(

            this.eventos

        );

    }

};