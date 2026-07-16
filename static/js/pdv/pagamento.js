// ==============================================
// LOJA FASHION PDV
// Pagamentos
// Versão 2.0
// ==============================================

const Pagamento = {

    forma: "Dinheiro",

    valorRecebido: 0,

    troco: 0,

    parcelas: 1,

    iniciar(){

        this.selectForma = document.getElementById(
            "forma_pagamento"
        );

        this.inputValor = document.getElementById(
            "valor_recebido"
        );

        this.lblTroco = document.getElementById(
            "troco"
        );

        this.inputParcelas = document.getElementById(
            "parcelas"
        );

        if(this.selectForma){

            this.selectForma.addEventListener(

                "change",

                ()=>{

                    this.alterarForma();

                }

            );

        }

        if(this.inputValor){

            this.inputValor.addEventListener(

                "input",

                ()=>{

                    this.calcularTroco();

                }

            );

        }

        Logger.sucesso(

            "Pagamento iniciado."

        );

    },

    alterarForma(){

        this.forma = this.selectForma.value;

        PDV.pagamento.forma = this.forma;

        if(this.forma === "Dinheiro"){

            this.inputValor.disabled = false;

        }

        else{

            this.inputValor.value = "";

            this.inputValor.disabled = true;

            this.lblTroco.innerHTML = "R$ 0,00";

        }

    },

    calcularTroco(){

        const recebido = parseFloat(

            this.inputValor.value || 0

        );

        const total = PDV.carrinho.total;

        this.valorRecebido = recebido;

        this.troco = recebido - total;

        if(this.troco < 0){

            this.troco = 0;

        }

        this.lblTroco.innerHTML =

            `R$ ${this.troco.toFixed(2)}`;

    },

    obterDados(){

        return{

            forma: this.forma,

            valorRecebido: this.valorRecebido,

            troco: this.troco,

            parcelas: this.parcelas

        };

    },

    processarPagamento(){

        console.log("Forma selecionada:", this.forma);

        switch(this.forma){

            case "PIX":

                console.log("Entrou no PIX");

                this.gerarPix();

                break;

            case "Cartão Débito":

                console.log("Entrou no Débito");

                this.abrirDebito();

                break;

            case "Cartão Crédito":

                console.log("Entrou no Crédito");

                this.abrirCredito();

                break;

            default:

                console.log("Entrou no Dinheiro");

                Venda.finalizar();

        }

    },

    async gerarPix(){

    const modal = document.getElementById(

        "modal_pix"

    );

    modal.style.display = "flex";

        const resposta = await API.gerarPix(

            PDV.carrinho.total

        );

        console.log(resposta);

        if(!resposta.success){

            alert("Erro ao gerar PIX");

            return;

        }

        document.getElementById(

            "pix_qrcode"

        ).innerHTML = `

            <img

                src="${resposta.imagem}"

                width="220"

                style="width:220px;height:220px;"

            >

        `;

        const btn = document.getElementById("confirmar_pix");

        btn.disabled = false;

        btn.innerHTML = "Confirmar Pagamento";

        btn.onclick = ()=>{

            btn.innerHTML = "✔ Pagamento Confirmado";

            btn.style.background="#16a34a";

            btn.style.color="#fff";

            setTimeout(()=>{

                this.fecharModalPix();

                Venda.finalizar();

            },800);

        };
    },

    abrirDebito(){

        const modal = document.getElementById("modal_pix");

        modal.style.display = "flex";

        document.getElementById("pix_qrcode").innerHTML = `

            <img
                src="/static/imagens/cartao_debito.png"
                width="180"
            >

        `;

        document.querySelector("#modal_pix h2").innerHTML =
            "Pagamento Débito";

        document.querySelector("#modal_pix p").innerHTML =
            "Aguardando aprovação da maquininha...";

        const btn = document.getElementById("confirmar_pix");

        btn.innerHTML = "Confirmar Pagamento";

        btn.onclick = ()=>{

            btn.innerHTML = "✔ Pagamento Aprovado";

            btn.style.background="#16a34a";

            setTimeout(()=>{

                this.fecharModalPix();

                Venda.finalizar();

            },800);

        };

    },

    abrirCredito(){

        const modal = document.getElementById("modal_pix");

        modal.style.display = "flex";

        document.querySelector("#modal_pix h2").innerHTML =
            "Pagamento Crédito";

        document.getElementById("pix_qrcode").innerHTML = `

            <img

                src="/static/imagens/cartao_debito.png"

                width="180"

            >

        `;

        document.getElementById("pix_status").innerHTML =

            "Selecione o parcelamento";

        document.getElementById(

            "valor_modal"

        ).innerHTML =

            `R$ ${PDV.carrinho.total.toFixed(2)}`;

        document.getElementById("credito_parcelas").style.display =

            "block";

        const parcelas = document.getElementById(

            "parcelas_credito"

        );

        const valor = document.getElementById(

            "valor_parcela"

        );

        valor.innerHTML =

            `1x de R$ ${PDV.carrinho.total.toFixed(2)}`;

        parcelas.onchange = ()=>{

            const qtd = parseInt(parcelas.value);

            const parcela = PDV.carrinho.total / qtd;

            valor.innerHTML =

                `${qtd}x de R$ ${parcela.toFixed(2)}`;

        };

        const btn = document.getElementById(

            "confirmar_pix"

        );

        btn.innerHTML = "Confirmar Pagamento";

        btn.disabled = false;

        btn.onclick = ()=>{

            console.log("CLICOU EM CONFIRMAR");

            btn.innerHTML = "✔ Pagamento Aprovado";

            btn.style.background = "#16a34a";

            setTimeout(()=>{

                document.getElementById(

                    "credito_parcelas"

                ).style.display = "none";

                this.fecharModalPix();

                Venda.finalizar();

            },1000);

        };

    },

    abrirComprovante(venda){

        const modal = document.getElementById(

            "modal_comprovante"

        );

        modal.style.display = "flex";

        document.getElementById(

            "conteudo_comprovante"

        ).innerHTML = `

            <h2>

                LOJA FASHION

            </h2>

            <h3>

                CUPOM DE VENDA

            </h3>

            <hr>

            <p>

                <strong>Venda:</strong>

                Nº ${venda.venda_id}

            </p>

            <p>

                <strong>Operador:</strong>

                ${PDV.operador.nome}

            </p>

            <p>

                <strong>Forma:</strong>

                ${Pagamento.forma}

            </p>

            <hr>

            <h3>

                TOTAL

            </h3>

            <h2>

                R$ ${PDV.carrinho.total.toFixed(2)}

            </h2>

            <hr>

            <p>

                Obrigado pela preferência!

            </p>

        `;

        document.getElementById(

            "btn_imprimir"

        ).onclick = ()=>{

            window.print();

        };

    },

    fecharComprovante(){

        document.getElementById(

            "modal_comprovante"

        ).style.display = "none";

        Venda.limpar();

    },

    fecharModalPix(){

        document.getElementById(

            "modal_pix"

        ).style.display = "none";

        document.getElementById(

            "credito_parcelas"

        ).style.display = "none";

    },

};