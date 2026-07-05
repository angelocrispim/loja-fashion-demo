// ==============================================
// LOJA FASHION PDV
// API
// ==============================================

const API = {

    iniciar(){

        Logger.info(

            "API iniciada."

        );

    },

    async buscarProduto(codigo){

        try{

            Logger.info(

                `Buscando produto ${codigo}`

            );

            const resposta = await fetch(

                `/produto/codigo/${codigo}`

            );

            if(!resposta.ok){

                throw new Error(

                    "Produto não encontrado."

                );

            }

            const produto = await resposta.json();

            Logger.sucesso(

                `Produto encontrado: ${produto.nome}`

            );

            return {

                sucesso: true,

                dados: produto,

                mensagem: null

            };

        }

        catch(erro){

            Logger.erro(

                erro.message

            );

            return {

                sucesso: false,

                dados: null,

                mensagem: erro.message

            };

        }

    }

};