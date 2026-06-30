// ========================================
// LOJA FASHION
// PIX
// ========================================

const Pix = {

    modal: null,

    imagem: null,

    valor: null,

    tempo: null,

    status: null,

    iniciar(){

        this.modal = document.getElementById("modalPix");

        this.imagem = document.getElementById("imagemPix");

        this.valor = document.getElementById("valorPix");

        this.tempo = document.getElementById("tempoPix");

        this.status = document.getElementById("textoStatus");

    },

    abrir(){

        this.modal.style.display = "flex";

        this.status.innerHTML =

            "Aguardando pagamento...";

    },

    fechar(){

        this.modal.style.display = "none";

    },

        async gerarQRCode(){

        try{

            const resposta = await fetch(

                "/caixa/gerar-pix",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":"application/json"

                    },

                    body: JSON.stringify({

                        total: PDV.carrinho.total

                    })

                }

            );

            if(!resposta.ok){

                throw new Error("Erro ao gerar PIX.");

            }

            const dados = await resposta.json();

            this.imagem.src = dados.imagem;

            this.valor.innerHTML =

                `R$ ${dados.valor.toFixed(2)}`;

            this.status.innerHTML =

                "Aguardando pagamento...";

            this.abrir();

            this.iniciarContador();

        }

        catch(erro){

            console.error(erro);

            alert("Erro ao gerar o QR Code.");

        }

    },

    iniciarContador(){

        let tempo = 300;

        const intervalo = setInterval(()=>{

            const minutos =

                Math.floor(tempo / 60);

            const segundos =

                tempo % 60;

            this.tempo.innerHTML =

                `${String(minutos).padStart(2,"0")}:${String(segundos).padStart(2,"0")}`;

            tempo--;

            if(tempo < 0){

                clearInterval(intervalo);

                this.status.innerHTML =

                    "PIX expirado";

            }

        },1000);

    }

    
};

EventBus.on(

    Eventos.PAGAMENTO_PIX,

    ()=>{

        Pix.abrir();

    }

);

EventBus.on(

    Eventos.PAGAMENTO_PIX,

    async ()=>{

        await Pix.gerarQRCode();

    }

);

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        Pix.iniciar();

    }

);
