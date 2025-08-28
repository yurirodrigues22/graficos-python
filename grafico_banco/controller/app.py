from model.database import executar_select
from view.graficos import GraficoBarras, GraficoPizza, GraficoLinha

def rodar():
    # Exemplo: buscar dados do banco
    sql = "SELECT NOME, IDADE FROM SEGURADOS_DEPENDENTES ROWS 10"
    dados = executar_select(sql)

    # Separar em listas (nome e idade)
    produtos = [linha[0] for linha in dados]   # nomes
    valores = [linha[1] for linha in dados]    # idades

    print("Escolha o tipo de gráfico:")
    print("1 - Barras")
    print("2 - Pizza")
    print("3 - Linha")

    escolha = input("Digite o número do gráfico desejado: ")

    if escolha == "1":
        grafico = GraficoBarras(produtos, valores, "Nome", "Idade")
    elif escolha == "2":
        grafico = GraficoPizza(produtos, valores, "Nome", "Idade")
    elif escolha == "3":
        grafico = GraficoLinha(produtos, valores, "Nome", "Idade")
    else:
        print("Opção inválida!")
        return

    grafico.plotar()
