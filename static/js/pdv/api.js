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

         Developer.registrarModulo(

            "API"

        );

    },

    // ==========================================
    // Monta a URL completa da API
    // ==========================================

    url(endpoint){

        return `${CONFIG.api.baseURL}${endpoint}`;

    },

    // ==========================================
    // Método genérico para requisições
    // ==========================================

    async request(endpoint, options = {}){

        try{

            Logger.info(

                `Requisição: ${endpoint}`

            );

            Developer.registrarEvento(

                "API",

                endpoint

            );

            const resposta = await fetch(

                this.url(endpoint),

                options

            );

            if(!resposta.ok){

                throw new Error(

                    `Erro HTTP ${resposta.status}`

                );

            }

            return await resposta.json();

        }

        catch(erro){

            Logger.erro(

                erro.message

            );

            Developer.registrarEvento(

                "API",

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

            return {

                sucesso: true,

                dados: produto,

                mensagem: null

            };

        }

        catch(erro){

            return{

                sucesso:false,

                dados:null,

                mensagem:erro.message

            };

        }

    }

};