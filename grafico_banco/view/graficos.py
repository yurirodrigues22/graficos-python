from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from model.database import executar_select

class GraficoBase(ABC):
    def __init__(self, query: str):
        dados = executar_select(query)
        self.produtos = [linha[0] for linha in dados]  # Faixa ("60+" ou "Menos de 60")
        self.valores = [linha[1] for linha in dados]  # Quantidade

    @abstractmethod
    def plotar(self):
        pass

class GraficoBarras(GraficoBase):
    def plotar(self):
        plt.bar(self.produtos, self.valores, color="skyblue")
        plt.title("Distribuição de Idades")
        plt.xlabel("Faixa etária")
        plt.ylabel("Quantidade")
        plt.show()

class GraficoPizza(GraficoBase):
    def plotar(self):
        plt.pie(self.valores, labels=self.produtos, autopct="%1.1f%%", startangle=90)
        plt.title("Distribuição de Idades")
        plt.show()

class GraficoLinha(GraficoBase):
    def plotar(self):
        plt.plot(self.produtos, self.valores, marker="o", color="green")
        plt.title("Distribuição de Idades")
        plt.xlabel("Faixa etária")
        plt.ylabel("Quantidade")
        plt.show()
