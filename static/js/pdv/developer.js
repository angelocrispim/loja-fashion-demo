// ==============================================
// LOJA FASHION PDV
// Developer Tools
// ==============================================

const Developer = {

    modulos: [],

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

            horario: new Date()

        });

        console.log(

            `✅ ${nome} carregado.`

        );

    },

    listarModulos(){

        console.table(

            this.modulos

        );

    }

};