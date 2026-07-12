// ==============================================
// LOJA FASHION PDV
// Inicialização da Aplicação
// ==============================================

const App = {

    iniciar(){

        // Diagnóstico do sistema
        Health.verificar();

        // Inicializa o modo desenvolvedor
        Developer.iniciar();

        Logger.info("================================");
        Logger.info(CONFIG.sistema.nome);
        Logger.info(`Versão ${CONFIG.sistema.versao}`);
        Logger.info("Inicializando...");
        Logger.info("================================");

        this.verificarModulos();

        this.iniciarModulos();

        EventBus.emit(

            Eventos.SISTEMA_INICIADO

        );

        Developer.registrarEvento(

            "Sistema",

            "PDV iniciado"

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

        if(typeof Developer === "undefined"){

            throw new Error("Developer não encontrado.");

        }

        if(typeof Venda === "undefined"){

            throw new Error("Venda não encontrada.");

        }

        if(typeof Pagamento === "undefined"){

        throw new Error(
            "Pagamento não encontrado."
        );

}

    },

    iniciarModulos(){

        EventBus.iniciar();

        Developer.registrarModulo(

            "EventBus"

        );

        API.iniciar();

        Developer.registrarModulo(

            "API"

        );

        Scanner.iniciar();

        Developer.registrarModulo(

            "Scanner"

        );

        Carrinho.iniciar();

        Developer.registrarModulo(

            "Carrinho"

        );

        UI.iniciar();

        Developer.registrarModulo(

            "UI"

        );

        Pagamento.iniciar();

        Developer.registrarModulo(

            "Pagamento"

        );

        Venda.iniciar();

        Developer.registrarModulo(

            "Venda"

        );

        

    }

};

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        App.iniciar();

    }

);