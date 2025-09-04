import threading
import webview
from app import app  # importa a aplicação Flask

def start_flask():
    # roda o Flask em segundo plano
    app.run(port=5000, debug=False)

if __name__ == "__main__":
    # inicia o Flask em uma thread separada
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    # abre a janela desktop apontando para a aplicação Flask
    webview.create_window(
        title="Gráfico Banco",
        url="http://127.0.0.1:5000",
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start()
