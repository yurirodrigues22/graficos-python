# import time
# from pathlib import Path
# import pandas as pd
# import matplotlib.pyplot as plt
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# # ===================== CLASSE BASE (sem input) =====================
# class Grafico:
#     def __init__(self, arquivo, col_cat, col_val, sheet=0):
#         self._arquivo = Path(arquivo)
#         self._col_cat = col_cat
#         self._col_val = col_val
#         self._sheet = sheet

#     def carregar_dados(self):
#         df = pd.read_excel(self._arquivo, sheet_name=self._sheet, engine="openpyxl")
#         df.columns = [str(c).strip() for c in df.columns]
#         df = df[[self._col_cat, self._col_val]].copy()
#         df[self._col_val] = pd.to_numeric(df[self._col_val], errors="coerce")
#         df = df.dropna(subset=[self._col_val])
#         return df

#     def desenhar(self, ax):
#         raise NotImplementedError

# class GraficoBarras(Grafico):
#     def desenhar(self, ax):
#         df = self.carregar_dados()
#         ax.clear()
#         ax.bar(df[self._col_cat], df[self._col_val])
#         ax.set_title("Gráfico de Barras")
#         ax.set_xlabel(self._col_cat)
#         ax.set_ylabel(self._col_val)

# class GraficoPizza(Grafico):
#     def desenhar(self, ax):
#         df = self.carregar_dados()
#         ax.clear()
#         ax.pie(df[self._col_val], labels=df[self._col_cat], autopct="%1.1f%%", startangle=90)
#         ax.axis("equal")
#         ax.set_title("Gráfico de Pizza")

# class GraficoLinha(Grafico):
#     def desenhar(self, ax):
#         df = self.carregar_dados()
#         ax.clear()
#         ax.plot(df[self._col_cat], df[self._col_val], marker="o")
#         ax.set_title("Gráfico de Linha")
#         ax.set_xlabel(self._col_cat)
#         ax.set_ylabel(self._col_val)

# # =============== WATCHDOG (sem input) ===============
# class Handler(FileSystemEventHandler):
#     def __init__(self, grafico, ax):
#         self.grafico = grafico
#         self.ax = ax
#         self._ultimo = 0.0

#     def on_modified(self, event):
#         if Path(event.src_path).resolve() == self.grafico._arquivo.resolve():
#             agora = time.time()
#             if agora - self._ultimo > 0.5:
#                 self._ultimo = agora
#                 print("Planilha modificada → Atualizando gráfico...")
#                 self.grafico.desenhar(self.ax)
#                 plt.draw()

# if __name__ == "__main__":
#     ARQUIVO = "dados.xlsx"
#     COL_CAT = "Produto"
#     COL_VAL = "Vendas"
#     # Escolha aqui o tipo sem input:
#     grafico = GraficoBarras(ARQUIVO, COL_CAT, COL_VAL)
#     # grafico = GraficoPizza(ARQUIVO, COL_CAT, COL_VAL)
#     # grafico = GraficoLinha(ARQUIVO, COL_CAT, COL_VAL)

#     if not Path(ARQUIVO).exists():
#         raise FileNotFoundError(f"Arquivo não encontrado: {Path(ARQUIVO).resolve()}")

#     print("MODO EXCEL (sem input). Lendo:", Path(ARQUIVO).resolve())

#     plt.ion()
#     fig, ax = plt.subplots()
#     grafico.desenhar(ax)

#     observer = Observer()
#     handler = Handler(grafico, ax)
#     observer.schedule(handler, Path(ARQUIVO).parent, recursive=False)
#     observer.start()

#     plt.show(block=False)
#     print("Edite e SALVE o arquivo para atualizar o gráfico.")

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
