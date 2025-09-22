import matplotlib.pyplot as plt

# Categorias e valores
categorias = input("Digite as categorias separadas por vírgula: ").split(",")
valores = list(map(float, input("Digite os valores correspondentes separados por vírgula: ").split(",")))


plt.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90)

plt.title("Distribuição dos Gastos Mensais")

plt.show()