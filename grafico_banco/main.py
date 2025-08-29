from view.graficos import GraficoBarras, GraficoPizza, GraficoLinha

if __name__ == "__main__":
    # Passo 1 - Escolher análise
    print("Escolha a análise que deseja realizar:")
    print("1 - Distribuição por Idade (60+ vs Menos de 60)")
    print("2 - Distribuição por Sexo")
    escolha_analise = input("Digite o número da análise desejada: ")

    if escolha_analise == "1":
        sql = """
        SELECT 
            CASE WHEN IDADE >= 60 THEN '60+' ELSE 'Menos de 60' END AS faixa,
            COUNT(*) 
        FROM SEGURADOS_DEPENDENTES
        GROUP BY faixa
        """
        titulo = "Distribuição por Idade"
        eixo_x = "Faixa Etária"
        eixo_y = "Quantidade"

    elif escolha_analise == "2":
        sql = """
        SELECT 
            CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
            COUNT(*) 
        FROM SEGURADOS_DEPENDENTES
        GROUP BY genero
        """
        titulo = "Distribuição por Sexo"
        eixo_x = "Sexo"
        eixo_y = "Quantidade"

    else:
        print("Opção inválida!")
        exit()

    # Passo 2 - Escolher tipo de gráfico
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

    # Exibir gráfico
    grafico.plotar()
