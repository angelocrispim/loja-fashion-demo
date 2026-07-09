// ==============================================
// LOJA FASHION PDV
// Scanner de Código de Barras
// Versão: 2.0
// ==============================================

const Scanner = {

    input: null,

    iniciar(){

        this.input = document.getElementById(
            "codigo_produto"
        );

        if(!this.input){

            Logger.erro(
                "Campo codigo_produto não encontrado."
            );

            return;

        }

        this.input.addEventListener(

            "keydown",

            this.lerCodigo.bind(this)

        );

        Logger.sucesso(
            "Scanner iniciado."
        );

        Developer.registrarModulo(
            "Scanner"
        );

    },

    async lerCodigo(event){

        if(event.key !== "Enter"){

            return;

        }

        if(CONFIG.scanner.bloquearLeitura){

            return;

        }

        const codigo = this.input.value.trim();

        if(codigo === ""){

            return;

        }

        CONFIG.scanner.bloquearLeitura = true;

        Logger.info(

            `Código lido: ${codigo}`

        );

        Developer.registrarEvento(

            "Scanner",

            `Código: ${codigo}`

        );

        try{

            const resposta = await API.buscarProduto(
                codigo
            );

            if(!resposta.sucesso){

                Logger.alerta(
                    resposta.mensagem
                );

                alert(
                    resposta.mensagem
                );

                return;

            }

            Logger.sucesso(

                `Produto encontrado: ${resposta.dados.nome}`

            );

            Developer.registrarEvento(

                "Scanner",

                `Produto encontrado: ${resposta.dados.nome}`

            );

            EventBus.emit(

                Eventos.PRODUTO_LIDO,

                resposta.dados

            );

            if(CONFIG.scanner.beep){

                this.tocarBeep();

            }

        }

        catch(erro){

            Logger.erro(

                erro.message

            );

            Developer.registrarEvento(

                "Scanner",

                `Erro: ${erro.message}`

            );

        }

        finally{

            CONFIG.scanner.bloquearLeitura = false;

            this.input.value = "";

            this.input.focus();

        }

    },

    tocarBeep(){

        const audio = new Audio(

            "/static/audio/beep.mp3"

        );

        audio.play();

    }

};