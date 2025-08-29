from flask import Flask, render_template, request, jsonify

# Tenta usar seu executor real; se não existir, usa fallback
try:
    from model.database import executar_select
except Exception:
    executar_select = None

app = Flask(__name__)

def consultar(analise: str):
    """
    Retorna (labels, valores) para a análise escolhida.
    Usa banco se 'executar_select' existir e funcionar; senão, dados de exemplo.
    """
    # SQLs
    sql_sexo = """
        SELECT 
            CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
            COUNT(*)
        FROM SEGURADOS_DEPENDENTES
        GROUP BY genero
    """
    sql_idade = """
        SELECT 
            CASE WHEN IDADE >= 60 THEN '60+' ELSE 'Menos de 60' END AS faixa,
            COUNT(*)
        FROM SEGURADOS_DEPENDENTES
        GROUP BY faixa
    """

    # Sem DB: retorna exemplo
    if executar_select is None:
        return (['Masculino', 'Feminino'], [120, 100]) if analise == 'sexo' \
               else (['60+', 'Menos de 60'], [80, 140])

    # Com DB
    query = sql_sexo if analise == 'sexo' else sql_idade
    try:
        rows = executar_select(query)
        labels = [r[0] for r in rows]
        valores = [int(r[1]) for r in rows]
        return labels, valores
    except Exception:
        # Se o banco falhar por qualquer motivo, usa exemplo
        return (['Masculino', 'Feminino'], [60, 40]) if analise == 'sexo' \
               else (['60+', 'Menos de 60'], [30, 70])

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/dados")
def api_dados():
    analise = request.args.get("analise", "sexo")  # 'sexo' | 'idade'
    labels, valores = consultar(analise)
    return jsonify({"labels": labels, "valores": valores})

if __name__ == "__main__":
    app.run(debug=True)

