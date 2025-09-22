from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from model.database import executar_select

class GraficoBase(ABC):
    def __init__(self, query: str, titulo: str, eixo_x: str = "", eixo_y: str = ""):
        dados = executar_select(query)
        self.labels = [linha[0] for linha in dados]  # Ex: Sexo ou Faixa Etária
        self.valores = [linha[1] for linha in dados] # Ex: Quantidade
        self.titulo = titulo
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.total = sum(self.valores)

    @abstractmethod
    def plotar(self):
        pass


class GraficoBarras(GraficoBase):
    def plotar(self):
        plt.bar(self.labels, self.valores, color="skyblue")
        plt.title(self.titulo + f"\nTotal: {self.total}")
        plt.xlabel(self.eixo_x)
        plt.ylabel(self.eixo_y)
        plt.show()


class GraficoPizza(GraficoBase):
    def plotar(self):
        plt.pie(self.valores, labels=self.labels, autopct="%1.1f%%", startangle=90)
        plt.title(self.titulo + f"\nTotal: {self.total}")
        plt.show()


class GraficoLinha(GraficoBase):
    def plotar(self):
        plt.plot(self.labels, self.valores, marker="o", color="green")
        plt.title(self.titulo + f"\nTotal: {self.total}")
        plt.xlabel(self.eixo_x)
        plt.ylabel(self.eixo_y)
        plt.show()
