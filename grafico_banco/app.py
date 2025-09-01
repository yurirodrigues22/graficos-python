from flask import Flask, render_template, request, jsonify

# Tentativa de importar a função de acesso ao banco
# Caso o módulo não exista ou dê erro, a aplicação funciona em modo "offline"
try:
    from model.database import executar_select
except Exception:
    executar_select = None

# Instância da aplicação Flask
app = Flask(__name__)

def consultar(analise: str):
    """
    Função central de consultas.
    Recebe o tipo de análise (sexo, idade, situacao, carteira)
    e retorna (labels, valores) para alimentar os gráficos.
    """

    # -----------------------------
    # Definição das queries SQL
    # -----------------------------
    sql_sexo = """
        SELECT 
            CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
            COUNT(*)
        FROM VW_SEGDEP
        GROUP BY genero
    """

    sql_idade = """
        SELECT 
            CASE 
                WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
                WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
                WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
                WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
                WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
                ELSE '60+'
            END AS faixa,
            COUNT(*)
        FROM VW_SEGDEP
        GROUP BY 
            CASE 
                WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
                WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
                WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
                WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
                WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
                ELSE '60+'
            END
        ORDER BY 1
    """

    sql_titular = """
        SELECT 
            CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END AS tipo,
            COUNT(*)
        FROM VW_SEGDEP
        GROUP BY CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END

    """
    
    sql_situacao = """
        SELECT 
            CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END AS status,
            COUNT(*)
        FROM VW_SEGDEP
        GROUP BY CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END
    """
    
    sql_dependentes_parentesco = """
       SELECT 
            CASE 
                WHEN IDGRAU_PARENTESCO = 1 THEN 'Cônjuge'
                WHEN IDGRAU_PARENTESCO = 2 THEN 'Filho(a)'
                WHEN IDGRAU_PARENTESCO = 3 THEN 'Pai/Mãe'
                ELSE 'Desconhecido'
            END AS parentesco,
            COUNT(*) AS quantidade
        FROM VW_SEGDEP
        WHERE SEQDEP <> 0
        GROUP BY 
            CASE 
                WHEN IDGRAU_PARENTESCO = 1 THEN 'Cônjuge'
                WHEN IDGRAU_PARENTESCO = 2 THEN 'Filho(a)'
                WHEN IDGRAU_PARENTESCO = 3 THEN 'Pai/Mãe'
                ELSE 'Desconhecido'
            END



    """

    sql_carteira = """
        SELECT 
            CASE 
                WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
                WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
                ELSE 'Nenhuma'
            END AS tipo,
            COUNT(*)
        FROM VW_SEGDEP
        GROUP BY CASE 
                WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
                WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
                ELSE 'Nenhuma'
            END
    """
    
    sql_alerta = """
        SELECT 
            CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' THEN 'Com alerta' ELSE 'Sem alerta' END AS alerta,
            COUNT(*)
        FROM VW_SEGDEP
        GROUP BY CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' THEN 'Com alerta' ELSE 'Sem alerta' END

    """
    

    # -----------------------------
    # Caso não exista conexão com banco
    # Retorna dados de exemplo (modo offline)
    # -----------------------------
    if executar_select is None:
        if analise == 'sexo':
            return (['Masculino', 'Feminino'], [0])
        elif analise == 'idade':
            return (['0-9', '10-17', '18-25', '26-39', '40-59', '60+'], [0])
        elif analise == 'titular':
            return (['Titular', 'Dependente'], [0])
        elif analise == 'situacao':
            return (['Ativos', 'Inativos'], [0])
        elif analise == 'dependentes_parentesco':
            return (['Cônjuge', 'Filho(a)', 'Outro'], [0])
        elif analise == 'carteira':
            return (['Nova', 'Antiga', 'Nenhuma'], [0])
        elif analise == 'alerta':
            return (['Com alerta', 'Sem alerta'], [0])
      

    # -----------------------------
    # Seleção da query conforme a análise
    # -----------------------------
    query = {
        "sexo": sql_sexo,
        "idade": sql_idade,
        "titular": sql_titular,
        "situacao": sql_situacao,
        "dependentes_parentesco": sql_dependentes_parentesco,
        "carteira": sql_carteira,
        "alerta": sql_alerta,
    }.get(analise)

    # -----------------------------
    # Execução da query no banco
    # -----------------------------
    try:
        rows = executar_select(query)   # Executa SQL
        labels = [r[0] for r in rows]   # Extrai categorias (coluna 1)
        valores = [int(r[1]) for r in rows]  # Extrai valores numéricos (coluna 2)
        return labels, valores
    except Exception:
        # Se der erro no banco, devolve fallback com valores zerados
        if analise == 'sexo':
            return (['Masculino', 'Feminino'], [0, 0])
        elif analise == 'idade':
            return (['0-9', '10-17', '18-25', '26-39', '40-59', '60+'], [0])
        elif analise == 'titular':
            return (['Titular', 'Dependente'], [0])
        elif analise == 'situacao':
            return (['Ativos', 'Inativos'], [0, 0])
        elif analise == 'dependentes_parentesco':
            return (['Cônjuge', 'Filho(a)', 'Outro'], [0, 0, 0])
        elif analise == 'carteira':
            return (['Nova', 'Antiga', 'Nenhuma'], [0, 0, 0])
        elif analise == 'alerta':
            return (['Com alerta', 'Sem alerta'], [0])
        

# -----------------------------
# Rotas da aplicação
# -----------------------------

@app.route("/")
def index():
    """
    Rota principal.
    Renderiza a página inicial (index.html) onde os gráficos são exibidos.
    """
    return render_template("index.html")


@app.get("/api/dados")
def api_dados():
    """
    API de dados em JSON.
    Recebe query param 'analise' (sexo | idade | situacao | carteira)
    e retorna {labels: [...], valores: [...]}
    """
    analise = request.args.get("analise", "sexo")  # default = sexo
    labels, valores = consultar(analise)
    return jsonify({"labels": labels, "valores": valores})


# -----------------------------
# Inicialização da aplicação
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)  # Debug=True só para desenvolvimento
