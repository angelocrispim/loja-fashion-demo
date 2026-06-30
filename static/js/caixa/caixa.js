// ========================================
// LOJA FASHION
// PDV
// ========================================

const PDV = {

    carrinho: {

        produtos: [],

        desconto: 0,

        subtotal: 0,

        total: 0

    },

    pagamento: {

        forma: "Dinheiro",

        parcelas: 1,

        valorRecebido: 0,

        troco: 0

    },

    pix: {

        vendaId: null,

        qrCode: null,

        status: "aguardando",

        tempo: 300

    },

    operador: {

        id: null,

        nome: ""

    },

    historico: []

};

// ========================================
// HISTÓRICO DO PDV
// ========================================

function registrarEvento(acao){

    const agora = new Date();

    PDV.historico.push({

        horario: agora.toLocaleTimeString(),

        acao: acao

    });

}

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        Scanner.iniciar();

    }

);