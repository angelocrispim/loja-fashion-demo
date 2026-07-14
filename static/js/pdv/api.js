// ==============================================
// LOJA FASHION PDV
// API
// Comunicação com o FastAPI
// Versão: 2.0
// ==============================================

const API = {

    iniciar(){

        Logger.sucesso(

            "API iniciada."

        );

    },

    // ==========================================
    // Monta a URL da API
    // ==========================================

    url(endpoint){

        return `${CONFIG.api.baseURL}${endpoint}`;

    },

    // ==========================================
    // Requisição Genérica
    // ==========================================

    async request(endpoint, options = {}){

        try{

            Logger.info(

                `Requisição: ${endpoint}`

            );

            const resposta = await fetch(

                this.url(endpoint),

                options

            );

            const dados = await resposta.json();

            if(!resposta.ok){

                throw new Error(

                    dados.erro ||

                    dados.detail ||

                    "Erro na API."

                );

            }

            return dados;

        }

        catch(erro){

            Logger.erro(

                erro.message

            );

            throw erro;

        }

    },

    // ==========================================
    // Buscar Produto
    // ==========================================

    async buscarProduto(codigo){

        try{

            const produto = await this.request(

                `/produto/codigo/${codigo}`

            );

            return{

                sucesso:true,

                dados:produto

            };

        }

        catch(erro){

            return{

                sucesso:false,

                mensagem:erro.message

            };

        }

    },

    // ==========================================
    // Finalizar Venda
    // ==========================================

    async finalizarVenda(dados){

        try{

            const resposta = await this.request(

                "/caixa/finalizar-venda",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":"application/json"

                    },

                    body:JSON.stringify(

                        dados

                    )

                }

            );

            return resposta;

        }

        catch(erro){

            return{

                success:false,

                mensagem:erro.message

            };

        }

    },

    // ==========================================
    // Gerar PIX
    // ==========================================

    async gerarPix(valor){

        try{

            return await this.request(

                "/caixa/gerar-pix",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":"application/json"

                    },

                    body:JSON.stringify({

                        total: valor

                    })

                }

            );

        }

        catch(erro){

            return{

                success:false,

                mensagem:erro.message

            };

        }

    },

};