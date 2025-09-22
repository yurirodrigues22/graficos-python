import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

# class mãe, cria classe abstrata que serve como modelo
# Classe base imutável
class GraficoBase(ABC):
    def __init__(self, arquivo_excel: str):
        # lê os dados da planilha
        df = pd.read_excel(arquivo_excel)
        colunas = df.columns.tolist()
        object.__setattr__(self, "produtos", df.iloc[:, 0].tolist())
        object.__setattr__(self, "coluna_produto", colunas[0])
        object.__setattr__(self, "valores", df.iloc[:, 1].tolist())
        object.__setattr__(self, "coluna_valor", colunas[1])

    @abstractmethod
    def plotar(self):
        """Método abstrato: cada gráfico implementa o seu próprio desenho"""
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
    arquivo = "dados.xlsx"

    print("Escolha o tipo de gráfico:")
    print("1 - Barras")
    print("2 - Pizza")
    print("3 - Linha")

    escolha = input("Digite o número do gráfico desejado: ")

    if escolha == "1":
        grafico = GraficoBarras(arquivo)
    elif escolha == "2":
        grafico = GraficoPizza(arquivo)
    elif escolha == "3":
        grafico = GraficoLinha(arquivo)
    else:
        print("Opção inválida!")
        exit()

    # Chama o método da classe escolhida
    grafico.plotar()
