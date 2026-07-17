// ==============================================
// LOJA FASHION ERP
// Health Check
// ==============================================

const Health = {

    verificar() {

        Logger.info("=====================================");
        Logger.info("Executando diagnóstico do sistema...");
        Logger.info("=====================================");

        this.verificarSistema();
        this.verificarAPI();
        this.verificarScanner();
        this.verificarCarrinho();
        this.verificarUI();

        Logger.info("=====================================");
        Logger.info("Diagnóstico finalizado.");
        Logger.info("=====================================");

    },

    verificarSistema() {

        if (PDV) {

            Logger.sucesso("Sistema OK");

        } else {

            Logger.erro("Sistema não inicializado");

        }

    },

    verificarAPI() {

        if (PDV.sistema.online) {

            Logger.sucesso("API Online");

        } else {

            Logger.erro("API Offline");

        }

    },

    verificarScanner() {

        if (!CONFIG.scanner.bloquearLeitura) {

            Logger.sucesso("Scanner OK");

        } else {

            Logger.alerta("Scanner bloqueado");

        }

    },

    verificarCarrinho() {

        if (Array.isArray(PDV.carrinho.produtos)) {

            Logger.sucesso(
                `Carrinho OK (${PDV.carrinho.produtos.length} produtos)`
            );

        } else {

            Logger.erro("Carrinho inválido");

        }

    },

    verificarUI() {

        const tela = document.getElementById("lista_produtos");

        if (tela) {

            Logger.sucesso("Interface OK");

        } else {

            Logger.erro("Interface não encontrada");

        }

    }

};