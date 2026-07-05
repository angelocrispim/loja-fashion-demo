// ==============================================
// LOJA FASHION PDV
// Inicialização
// ==============================================

const App = {

    iniciar(){

        Health.verificar();

        Logger.info("================================");
        Logger.info("LOJA FASHION PDV");
        Logger.info(`Versão ${CONFIG.sistema.versao}`);
        Logger.info("Inicializando...");
        Logger.info("================================");

        this.verificarModulos();

        this.iniciarModulos();

        EventBus.emit(

            Eventos.SISTEMA_INICIADO

        );

        Logger.sucesso(

            "Sistema iniciado com sucesso."

        );

    },

    verificarModulos(){

        if(typeof PDV === "undefined"){

            throw new Error("PDV não encontrado.");

        }

        if(typeof EventBus === "undefined"){

            throw new Error("EventBus não encontrado.");

        }

        if(typeof API === "undefined"){

            throw new Error("API não encontrada.");

        }

        if(typeof Scanner === "undefined"){

            throw new Error("Scanner não encontrado.");

        }

        if(typeof Carrinho === "undefined"){

            throw new Error("Carrinho não encontrado.");

        }

        if(typeof UI === "undefined"){

            throw new Error("UI não encontrada.");

        }

    },

    iniciarModulos(){

        EventBus.iniciar();

        API.iniciar();

        Scanner.iniciar();

        Carrinho.iniciar();

        UI.iniciar();

    }

};

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        App.iniciar();

    }

);