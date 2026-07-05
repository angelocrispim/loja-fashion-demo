// ==============================================
// LOJA FASHION PDV
// Estado Global da Aplicação
// Versão: 2.0
// ==============================================

const PDV = {

    // ==========================
    // Operador do Caixa
    // ==========================
    operador: {

        id: null,

        nome: "",

        caixa: null

    },

    // ==========================
    // Venda Atual
    // ==========================
    venda: {

        numero: null,

        data: null,

        status: "ABERTA"

    },

    // ==========================
    // Cliente
    // ==========================
    cliente: {

        id: null,

        nome: "",

        cpf: ""

    },

    // ==========================
    // Carrinho
    // ==========================
    carrinho: {

        produtos: [],

        quantidadeItens: 0,

        subtotal: 0,

        desconto: 0,

        total: 0

    },

    // ==========================
    // Pagamento
    // ==========================
    pagamento: {

        forma: null,

        parcelas: 1,

        valorRecebido: 0,

        troco: 0

    },

    // ==========================
    // PIX
    // ==========================
    pix: {

        id: null,

        status: null,

        qrCode: null,

        copiaCola: null,

        expiracao: null

    },

    // ==========================
    // Sistema
    // ==========================
    sistema: {

        developerMode: true,

        online: true,

        carregando: false

    }

};

// ==============================================
// LOJA FASHION PDV
// Estado Global da Aplicação
// Versão: 2.0
// ==============================================

const PDV = {

    // ==========================
    // Operador do Caixa
    // ==========================
    operador: {

        id: null,

        nome: "",

        caixa: {

            id: null,

            numero: null

        }

    },

    // ==========================
    // Venda Atual
    // ==========================
    venda: {

        numero: null,

        data: null,

        status: "ABERTA"

    },

    // ==========================
    // Cliente
    // ==========================
    cliente: {

        id: null,

        nome: "",

        cpf: ""

    },

    // ==========================
    // Carrinho
    // ==========================
    carrinho: {

        produtos: [],

        quantidadeItens: 0,

        subtotal: 0,

        desconto: 0,

        total: 0

    },

    // ==========================
    // Pagamento
    // ==========================
    pagamento: {

        forma: null,

        parcelas: 1,

        valorRecebido: 0,

        troco: 0

    },

    // ==========================
    // PIX
    // ==========================
    pix: {

        id: null,

        status: null,

        qrCode: null,

        copiaCola: null,

        expiracao: null

    },

    // ==========================
    // Sistema
    // ==========================
    sistema: {

        developerMode: true,

        online: true,

        carregando: false,

        versao: "2.0.0"

    }

};

function limparVenda(){

    PDV.cliente = {

        id: null,

        nome: "",

        cpf: ""

    };

    PDV.carrinho = {

        produtos: [],

        quantidadeItens: 0,

        subtotal: 0,

        desconto: 0,

        total: 0

    };

    PDV.pagamento = {

        forma: null,

        parcelas: 1,

        valorRecebido: 0,

        troco: 0

    };

    PDV.pix = {

        id: null,

        status: null,

        qrCode: null,

        copiaCola: null,

        expiracao: null

    };

}