// ========================================
// LOJA FASHION
// SCANNER
// ========================================

const Scanner = {

    input: null,

    iniciar(){

        this.input = document.getElementById(
            "codigo_produto"
        );

        if(!this.input){

            console.error(
                "Campo código_produto não encontrado."
            );

            return;

        }

        this.input.addEventListener(

            "keydown",

            this.lerCodigo.bind(this)

        );

    },

    async lerCodigo(event){

        if(event.key !== "Enter"){

            return;

        }

        const codigo = this.input.value.trim();

        if(codigo === ""){

            return;

        }

        try{

            const resposta = await fetch(

                `/produto/codigo/${codigo}`

            );

            if(!resposta.ok){

                alert("Produto não encontrado.");

                this.input.value = "";

                return;

            }

            const produto = await resposta.json();

            console.table(produto);

            console.log("Disparando evento produtoLido...");

            console.log("Emitindo evento...");

            EventBus.emit(
                Eventos.PRODUTO_LIDO,
                produto
            );

            tocarBeep();

            registrarEvento(

                `Scanner leu ${produto.nome}`

            );

            this.input.value = "";

            this.input.focus();

        }

       catch(error){

            console.error("========== ERRO SCANNER ==========");
            console.error(error);
            console.error(error.stack);

            alert("Veja o Console (F12)");
        }

    }

};