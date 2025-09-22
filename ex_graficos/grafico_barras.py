import matplotlib.pyplot as plt

produtos = input("Digite o nome de 3 produtos separados por vírgula: ").split(",")
vendas = list(map(int, input("Digite as vendas correspondentes separadas por vírgula: ").split(",")))

# Gráfico de barras
plt.bar(produtos, vendas, color="skyblue")

plt.title("Vendas por Produto")
plt.xlabel("Produtos")
plt.ylabel("Quantidade Vendida")

plt.show()
