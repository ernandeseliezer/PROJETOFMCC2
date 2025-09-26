document.addEventListener('DOMContentLoaded', () => {
    const grupoAInput = document.getElementById('grupoA');
    const grupoBInput = document.getElementById('grupoB');
    const modInputA = document.getElementById('mod');
    const modInputB = document.getElementById('mod2');
    const operacaoSomaRadio = document.getElementById('soma');
    const operacaoMultiplicacaoRadio = document.getElementById('multiplicacao');
    const botaoVerificar = document.getElementById('botao-verificar');
    const resultadoContainer = document.getElementById('resultado-container');
    const resultadoTexto = document.getElementById('resultado-texto');

    const ENDPOINT_VERIFICACAO = ''; //coloquem a url do back

    function exibirResultado(mensagem) {
        resultadoTexto.textContent = mensagem;
        resultadoTexto.style.color = '#f0f8ff';
        resultadoTexto.style.backgroundColor = 'transparent';

        resultadoContainer.style.display = 'block';
        resultadoContainer.classList.add('visivel');
    }
    
    async function verificarSubgrupo() {
        const grupoA = grupoAInput.value.split(',').map(item => item.trim());
        const grupoB = grupoBInput.value.split(',').map(item => item.trim());
        const modA = modInputA.value ? parseInt(modInputA.value) : null;
        const modB = modInputB.value ? parseInt(modInputB.value) : null;
        const operacao = operacaoSomaRadio.checked ? 'soma' : (operacaoMultiplicacaoRadio.checked ? 'multiplicacao' : null);

        if (grupoA.length === 0 || grupoB.length === 0 || !operacao) {
            exibirResultado('Preencha os campos obrigatórios');
            return;
        }

        try {
            const response = await fetch(ENDPOINT_VERIFICACAO, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    grupoA,
                    grupoB,
                    modA,
                    modB,
                    operacao
                })
            });

            if (!response.ok) {
                throw new Error(`Erro do servidor: ${response.status} ${response.statusText}`);
            }

            const resultado = await response.json();

            if (resultado.isSubgrupo) {
                exibirResultado(`O Grupo B é um subgrupo do Grupo A. Explicação: ${resultado.motivo}`);
            } else {
                exibirResultado(`O Grupo B NÃO é um subgrupo do Grupo A. Motivo: ${resultado.motivo}`);
            }

        } catch (error) {
            exibirResultado("Verifique se o back-end está rodando e se a URL está correta.");
        }
    }

    botaoVerificar.addEventListener('click', verificarSubgrupo);
});