import matplotlib.pyplot as plt

# grafico de linha
x = list(map(int, input("Digite os valores de X separados por vírgula: ").split(",")))
y = list(map(int, input("Digite os valores de Y separados por vírgula: ").split(",")))


plt.plot(x, y, color="red", marker="o", linestyle="-")
plt.title("Meu Primeiro Gráfico")
plt.xlabel("Eixo X")
plt.ylabel("Eixo Y")
plt.show()