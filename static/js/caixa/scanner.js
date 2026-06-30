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

            console.log("Produto recebido:", produto);

            console.log("Disparando evento produtoLido...");

            EventBus.emit(
                "produtoLido",
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

            console.error(error);

            throw error;

        }

    }

};