from view.graficos import GraficoBarras, GraficoPizza, GraficoLinha

# --- Dicionário com análises disponíveis ---
analises = {
    "1": {
        "sql": """
            SELECT 
                CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
                COUNT(*) 
            FROM SEGURADOS_DEPENDENTES
            GROUP BY genero
        """,
        "titulo": "Distribuição por Sexo",
        "eixo_x": "Sexo",
        "eixo_y": "Quantidade"
    },
    "2": {
        "sql": """
            SELECT 
                CASE WHEN IDADE >= 60 THEN '60+' ELSE 'Menos de 60' END AS faixa,
                COUNT(*) 
            FROM SEGURADOS_DEPENDENTES
            GROUP BY faixa
        """,
        "titulo": "Faixa Etária dos Dependentes",
        "eixo_x": "Faixa Etária",
        "eixo_y": "Quantidade"
    },
    "3": {
        "sql": """
            SELECT 
                CASE WHEN IDSITUACAO = 1 THEN 'Ativos' ELSE 'Inativos' END AS situacao,
                COUNT(*) 
            FROM SEGURADOS_DEPENDENTES
            GROUP BY situacao
        """,
        "titulo": "Situação dos Dependentes",
        "eixo_x": "Situação",
        "eixo_y": "Quantidade"
    },
    "4": {
        "sql": """
            SELECT 
                CASE 
                    WHEN CARTEIRA_UNIMED IS NOT NULL THEN 'Nova' 
                    ELSE 'Antiga' 
                END AS tipo_carteira,
                COUNT(*)
            FROM SEGURADOS_DEPENDENTES
            GROUP BY tipo_carteira
        """,
        "titulo": "Carteira Unimed (Nova vs Antiga)",
        "eixo_x": "Tipo de Carteira",
        "eixo_y": "Quantidade"
    }
}

# --- Menu inicial ---
print("Escolha a análise que deseja realizar:")
for k, v in analises.items():
    print(f"{k} - {v['titulo']}")

escolha_analise = input("Digite o número da análise desejada: ")

if escolha_analise not in analises:
    print("Opção inválida!")
    exit()

# Pega os dados da análise escolhida
sql = analises[escolha_analise]["sql"]
titulo = analises[escolha_analise]["titulo"]
eixo_x = analises[escolha_analise]["eixo_x"]
eixo_y = analises[escolha_analise]["eixo_y"]

# --- Escolher tipo de gráfico ---
print("\nEscolha o tipo de gráfico:")
print("1 - Barras")
print("2 - Pizza")
print("3 - Linha")
escolha_grafico = input("Digite o número do gráfico desejado: ")

if escolha_grafico == "1":
    grafico = GraficoBarras(sql, titulo, eixo_x, eixo_y)
elif escolha_grafico == "2":
    grafico = GraficoPizza(sql, titulo)
elif escolha_grafico == "3":
    grafico = GraficoLinha(sql, titulo, eixo_x, eixo_y)
else:
    print("Opção inválida!")
    exit()

# --- Exibir gráfico ---
grafico.plotar()
