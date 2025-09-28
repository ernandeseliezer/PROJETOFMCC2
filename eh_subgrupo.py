from flask import Flask, request, jsonify  # Importa o Flask para criar a API, request para receber dados e jsonify para retornar respostas em JSON
from flask_cors import CORS  # Permite que qualquer front-end acesse a API, evitando bloqueios de segurança do navegador

app = Flask(__name__)  # Inicializa a aplicação Flask
CORS(app)  # Ativa o CORS para liberar acesso externo

# Função que aplica a operação entre dois elementos, considerando módulo opcional
def aplicar_operacao(a, b, operacao, mod=None):
    # Escolhe a operação matemática conforme o símbolo passado
    if operacao == "+":
        resultado = a + b
    elif operacao == "*":
        resultado = a * b
    else:
        return None  # Se operação não reconhecida, retorna None
    
    # Se houver módulo, aplica resto da divisão (operação modular)
    if mod is not None:
        resultado %= mod
    return resultado

# Função que verifica se o conjunto é fechado sob a operação
def fechado(grupo, operacao, mod):
    # Para cada par de elementos, aplica a operação
    for a in grupo:
        for b in grupo:
            # Se algum resultado não estiver no conjunto, não é fechado
            if aplicar_operacao(a, b, operacao, mod) not in grupo:
                return False
    return True  # Todos os resultados ficaram no conjunto, então é fechado

# Função que encontra o elemento identidade do grupo
def identidade(grupo, operacao, mod):
    # Procura um elemento que não altere nenhum outro ao ser combinado
    for e in grupo:
        if all(aplicar_operacao(a, e, operacao, mod) == a and 
               aplicar_operacao(e, a, operacao, mod) == a for a in grupo):
            return e  # Encontrou a identidade
    return None  # Não existe identidade

# Função que verifica se todos os elementos possuem inverso
def inverso(grupo, operacao, elemento_identidade, mod):
    # Para cada elemento, verifica se existe algum inverso que volte à identidade
    for a in grupo:
        if not any(aplicar_operacao(a, b, operacao, mod) == elemento_identidade and 
                   aplicar_operacao(b, a, operacao, mod) == elemento_identidade for b in grupo):
            return False  # Algum elemento não tem inverso
    return True  # Todos os elementos possuem inverso

# Função principal para testar se um conjunto forma um grupo
def teste_grupo(grupo, operacao, mod, nome):
    resultado = {
        "nome": nome,
        "elementos": grupo,
        "operacao": operacao,
        "modulo": mod,
        "testes": {},
        "eh_grupo": False,
        "identidade": None,
        "mensagens": []
    }
    
    # Associatividade (assumimos verdadeira para + e *)
    resultado["testes"]["associatividade"] = True
    resultado["mensagens"].append("Associatividade: Verdadeiro ✅")
    
    # Teste de fechamento
    eh_fechado = fechado(grupo, operacao, mod)
    resultado["testes"]["fechamento"] = eh_fechado
    if eh_fechado:
        resultado["mensagens"].append("Fechamento: Verdadeiro ✅")
    else:
        resultado["mensagens"].append("Fechamento: Falso ❌")
    
    # Teste de identidade
    e = identidade(grupo, operacao, mod)
    resultado["identidade"] = e
    resultado["testes"]["identidade"] = e is not None
    if e is not None:
        resultado["mensagens"].append(f"Elemento identidade: {e} ✅")
    else:
        resultado["mensagens"].append("Elemento identidade: Não existe ❌")
    
    # Teste de inversos
    if e is not None:
        tem_inversos = inverso(grupo, operacao, e, mod)
        resultado["testes"]["inversos"] = tem_inversos
        if tem_inversos:
            resultado["mensagens"].append("Inverso: Todos os elementos possuem inverso ✅")
        else:
            resultado["mensagens"].append("Inverso: Nem todos os elementos possuem inverso ❌")
    else:
        resultado["testes"]["inversos"] = False
        resultado["mensagens"].append("Inverso: Não verificado, pois não existe identidade ❌")
    
    # Resultado final
    if eh_fechado and e is not None and resultado["testes"]["inversos"]:
        resultado["eh_grupo"] = True
        resultado["mensagens"].append("Resultado final: O conjunto forma um grupo! 🎉")
    else:
        resultado["eh_grupo"] = False
        resultado["mensagens"].append("Resultado final: O conjunto NÃO forma um grupo ❌")
    
    return resultado

# Função para testar se H é subgrupo de G
def teste_subgrupo(grupo_G, operacao_G, mod_G, grupo_H, operacao_H, mod_H, e_G, e_H):
    resultado = {
        "eh_subgrupo": False,
        "testes": {},
        "mensagens": []
    }
    
    resultado["mensagens"].append("Testando se H é subgrupo de G:")
    
    # 1. Contenção: todos elementos de H estão em G?
    contido = all(x in grupo_G for x in grupo_H)
    resultado["testes"]["contencao"] = contido
    resultado["mensagens"].append(f"Todos os elementos de H estão em G: {'✅' if contido else '❌'}")
    
    # 2. Fechamento de H
    fechado_H = fechado(grupo_H, operacao_H, mod_H)
    resultado["testes"]["fechamento_H"] = fechado_H
    resultado["mensagens"].append(f"H é fechado sob sua operação: {'✅' if fechado_H else '❌'}")
    
    # 3. Operação e módulo iguais aos de G?
    mesma_operacao = operacao_G == operacao_H
    mesmo_modulo = mod_G == mod_H
    resultado["testes"]["mesma_operacao"] = mesma_operacao
    resultado["testes"]["mesmo_modulo"] = mesmo_modulo
    
    if not mesma_operacao:
        resultado["mensagens"].append("As operações de G e H são diferentes: ❌")
    
    if not mesmo_modulo:
        resultado["mensagens"].append("Os módulos de G e H são diferentes: ❌")
    
    # 4. Identidade e inversos
    if e_H is None or e_H != e_G:
        resultado["testes"]["mesma_identidade"] = False
        resultado["mensagens"].append("H não contém a mesma identidade de G: ❌")
        resultado["testes"]["inversos_H"] = False
    else:
        resultado["testes"]["mesma_identidade"] = True
        resultado["mensagens"].append("H contém a mesma identidade de G: ✅")
        
        inverso_H = inverso(grupo_H, operacao_H, e_H, mod_H)
        resultado["testes"]["inversos_H"] = inverso_H
        resultado["mensagens"].append(f"Todos os elementos de H possuem inverso em H: {'✅' if inverso_H else '❌'}")
    
    # Veredito final
    if (contido and fechado_H and resultado["testes"]["mesma_identidade"] and 
        resultado["testes"]["inversos_H"] and mesma_operacao and mesmo_modulo):
        resultado["eh_subgrupo"] = True
        resultado["mensagens"].append("Resultado final: H é subgrupo de G! 🎉")
    else:
        resultado["eh_subgrupo"] = False
        resultado["mensagens"].append("Resultado final: H NÃO é subgrupo de G ❌")
    
    return resultado

# Rota principal da API para verificar grupos e subgrupos
@app.route('/verificar_grupos', methods=['POST'])
def verificar_grupos():
    try:
        data = request.json  # Recebe os dados enviados pelo front-end
        
        # Extrair dados do grupo G
        elementos_G = data['grupoG']['elementos']
        operacao_G = data['grupoG']['operacao']
        mod_G = data['grupoG']['modulo']
        if mod_G == '' or mod_G is None:
            mod_G = None
        else:
            mod_G = int(mod_G)
        
        # Extrair dados do grupo H
        elementos_H = data['grupoH']['elementos']
        operacao_H = data['grupoH']['operacao']
        mod_H = data['grupoH']['modulo']
        if mod_H == '' or mod_H is None:
            mod_H = None
        else:
            mod_H = int(mod_H)
        
        # Testar se G e H são grupos
        resultado_G = teste_grupo(elementos_G, operacao_G, mod_G, "G")
        resultado_H = teste_grupo(elementos_H, operacao_H, mod_H, "H")
        
        # Testar se H é subgrupo de G
        resultado_subgrupo = teste_subgrupo(
            elementos_G, operacao_G, mod_G,
            elementos_H, operacao_H, mod_H,
            resultado_G["identidade"], resultado_H["identidade"]
        )
        
        # Retornar resultado completo
        return jsonify({
            "sucesso": True,
            "grupoG": resultado_G,
            "grupoH": resultado_H,
            "subgrupo": resultado_subgrupo
        })
        
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": f"Erro ao processar os dados: {str(e)}"
        }), 400

# Health check simples para garantir que a API está funcionando
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "API funcionando corretamente"})

# Ponto de entrada da aplicação
if __name__ == '__main__':
    print("🚀 Iniciando API do Verificador de Grupos...")
    print("📡 Servidor rodando em: http://localhost:5000")
    print("🔍 Endpoint principal: POST /verificar_grupos")
    print("❤️  Health check: GET /health")
    app.run(debug=True, port=5000, host='0.0.0.0')
