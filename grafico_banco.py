import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
import fdb  # cliente Firebird

# Classe base abstrata
class GraficoBase(ABC):
    def __init__(self, conexao, query: str):
        # Lê os dados do banco em um DataFrame do Pandas
        df = pd.read_sql_query(query, conexao)
        colunas = df.columns.tolist()
        object.__setattr__(self, "produtos", df.iloc[:, 0].tolist())
        object.__setattr__(self, "coluna_produto", colunas[0])
        object.__setattr__(self, "valores", df.iloc[:, 1].tolist())
        object.__setattr__(self, "coluna_valor", colunas[1])

    @abstractmethod
    def plotar(self):
        pass


class GraficoBarras(GraficoBase):
    def plotar(self):
        plt.bar(self.produtos, self.valores, color="skyblue")
        plt.title("Gráfico de Barras")
        plt.xlabel(self.coluna_produto)
        plt.ylabel(self.coluna_valor)
        plt.show()


class GraficoPizza(GraficoBase):
    def plotar(self):
        plt.pie(self.valores, labels=self.produtos, autopct="%1.1f%%", startangle=90)
        plt.title("Gráfico de Pizza")
        plt.show()


class GraficoLinha(GraficoBase):
    def plotar(self):
        plt.plot(self.produtos, self.valores, marker="o", color="green")
        plt.title("Gráfico de Linha")
        plt.xlabel(self.coluna_produto)
        plt.ylabel(self.coluna_valor)
        plt.show()


if __name__ == "__main__":
    # Faz a conexão com o Firebird
    con = fdb.connect(
        host="192.9.200.98",
        database="dbsaude",
        user="SYSDBA",
        password="7v28iwr9",
        charset="UTF8"
    )

    # Exemplo: pega duas colunas (nome + valor) da tabela
    sql = "SELECT NOME, ID_DEPENDENTE FROM SEGURADOS_DEPENDENTES ROWS 20"

    print("Escolha o tipo de gráfico:")
    print("1 - Barras")
    print("2 - Pizza")
    print("3 - Linha")

    escolha = input("Digite o número do gráfico desejado: ")

    if escolha == "1":
        grafico = GraficoBarras(con, sql)
    elif escolha == "2":
        grafico = GraficoPizza(con, sql)
    elif escolha == "3":
        grafico = GraficoLinha(con, sql)
    else:
        print("Opção inválida!")
        exit()

    grafico.plotar()
    con.close()
