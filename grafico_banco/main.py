from view.graficos import GraficoBarras, GraficoPizza, GraficoLinha

if __name__ == "__main__":
    # SQL que retorna faixas etárias
    sql = """
    SELECT 
        CASE WHEN IDADE >= 60 THEN '60+' ELSE 'Menos de 60' END AS faixa,
        COUNT(*) 
    FROM SEGURADOS_DEPENDENTES
    GROUP BY faixa
    """

    print("Escolha o tipo de gráfico:")
    print("1 - Barras")
    print("2 - Pizza")
    print("3 - Linha")

    escolha = input("Digite o número do gráfico desejado: ")

    if escolha == "1":
        grafico = GraficoBarras(sql)
    elif escolha == "2":
        grafico = GraficoPizza(sql)
    elif escolha == "3":
        grafico = GraficoLinha(sql)
    else:
        print("Opção inválida!")
        exit()

    grafico.plotar()
