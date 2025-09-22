# -----------------------------
# Imports
# -----------------------------
import flet as ft                # Biblioteca Flet para criar interfaces gráficas com Python
from flet import Page, Icons     # Importando tipos específicos do Flet
import pandas as pd              # Pandas para manipulação de dados (tabelas)
import seaborn as sns            # Seaborn para gráficos
import matplotlib.pyplot as plt  # Matplotlib para geração de gráficos
from io import BytesIO           # Para criar buffer de imagem em memória
import base64     # Para converter a imagem em string (base64) e exibir no Flet
import sys, os


from queries import QUERIES, FALLBACK  # Dicionários com consultas SQL pré-definidas e fallback

# Tenta importar a função de consulta ao banco de dados
try:
    from model.database import executar_select
except Exception as e:
    print("⚠️ Não foi possível importar executar_select:", e)
    executar_select = None


# -----------------------------
# Mapas de análises
# -----------------------------
# Esses dicionários mapeiam o "nome amigável" que aparece na tela
# para a "chave interna" que busca a query SQL correspondente
MAP_GERAL = {
    "Distribuição por Sexo (Segurados)": "sexo_segurados",
    "Perfil Etário da População (Segurados)": "idade_segurados",
    "Alerta (Segurados)": "alerta_segurados",
    "Situação (Segurados)": "situacao_segurados",
    "Carteira (Segurados)": "carteira_segurados",
    "Titular vs Dependente": "titular"
}

MAP_TITULAR = {
    "Sexo (Titulares)": "sexo_titulares",
    "Carteira (Titulares)": "carteira_titulares",
}

MAP_DEP = {
    "Parentesco (Dependentes)": "parentesco_dependentes",
    "Situação (Dependentes)": "situacao_dependentes",
    "Alerta (Dependentes)": "alerta_dependentes"
}


# -----------------------------
# Helpers
# -----------------------------
def _to_int_safe(v):
    """Converte valores em número inteiro de forma segura"""
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return 0


def consultar(analise: str):
    """
    Consulta os dados no banco ou retorna valores de fallback
    :param analise: chave da análise (ex: 'sexo_segurados')
    :return: (labels, valores)
    """
    if analise not in QUERIES:
        return FALLBACK.get(analise, ([], []))
    if executar_select is None:
        return FALLBACK.get(analise, ([], []))
    try:
        rows = executar_select(QUERIES[analise])   # executa query
        if not rows:
            return FALLBACK.get(analise, ([], []))
        labels = [r[0] for r in rows]              # primeira coluna: categorias
        valores = [_to_int_safe(r[1]) for r in rows]  # segunda coluna: quantidades
        return labels, valores
    except Exception:
        return FALLBACK.get(analise, ([], []))


def gerar_grafico(df: pd.DataFrame, chart_type: str, cor: str):
    """
    Gera gráfico (Barras ou Pizza) a partir de DataFrame e retorna em Base64.
    """
    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))

    # Se for gráfico de barras
    if chart_type == "Gráfico de Barras":
        sns.barplot(data=df, x="Categoria", y="Quantidade", ax=ax, color=cor)
        plt.xticks(rotation=30, ha="right")  # Rotaciona os rótulos do eixo X
    else:
        # Gráfico de pizza
        colors = [
            "#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#FACC15", "#EAB308"
        ]
        ax.pie(
            df["Quantidade"],
            labels=df["Categoria"],
            autopct="%1.1f%%",     # mostra percentual
            startangle=90,
            colors=colors[:len(df)]
        )
        ax.axis("equal")  # deixa circular

    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")  # salva em memória
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")  # retorna imagem em base64


# -----------------------------
# Render de uma aba
# -----------------------------
def render_tab(page: Page, titulo: str, opcoes_map: dict, cor: str, metric_label: str):
    """
    Renderiza uma aba com dropdowns, KPI, tabela e gráfico.
    """

    # Dropdown para escolher a análise
    dropdown_analise = ft.Dropdown(
        label="Escolha a análise",
        options=[ft.dropdown.Option(k) for k in opcoes_map.keys()],
        value=list(opcoes_map.keys())[0],
        width=320
    )

    # Dropdown para escolher o tipo de gráfico
    dropdown_chart = ft.Dropdown(
        label="Tipo de visualização",
        options=[ft.dropdown.Option("Gráfico de Barras"), ft.dropdown.Option("Gráfico de Pizza")],
        value="Gráfico de Barras",
        width=320
    )

    # Cartão KPI (mostra número total)
    kpi_card = ft.Container(
        content=ft.Column([
            ft.Icon(Icons.PEOPLE, size=28, color="#EAA900"),
            ft.Text("0", size=28, weight="bold"),  # número dinâmico
            ft.Text(metric_label, size=12, color="#555555")
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.all(16),
        width=140,
        border_radius=12,
        bgcolor="white",
        shadow=ft.BoxShadow(color="#00000011", blur_radius=8, offset=ft.Offset(0, 2))
    )

    # Tabela com os dados
    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Categoria")), ft.DataColumn(ft.Text("Quantidade"))],
        rows=[],
        width=320
    )
    tabela_box = ft.Container(
        tabela, padding=8, height=370, width=320,
        bgcolor="white", border_radius=12, border=ft.border.all(1, "#e6e6e6"),
        shadow=ft.BoxShadow(color="#00000011", blur_radius=8, offset=ft.Offset(0, 2))
    )

    # Gráfico (imagem gerada dinamicamente)
    grafico_img = ft.Image(expand=True, fit=ft.ImageFit.CONTAIN)
    grafico_box = ft.Container(
        grafico_img, expand=True, padding=16,
        bgcolor="white", border_radius=12
    )

    # Função para atualizar tabela, KPI e gráfico
    def atualizar(e=None):
        analise_key = opcoes_map[dropdown_analise.value]   # pega chave SQL
        labels, valores = consultar(analise_key)           # consulta dados
        df = pd.DataFrame({"Categoria": labels, "Quantidade": valores})

        # Atualiza KPI
        total = int(df["Quantidade"].sum()) if not df.empty else 0
        kpi_card.content.controls[1].value = f"{total}"

        # Atualiza tabela
        tabela.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(cat))), ft.DataCell(ft.Text(str(qtd)))])
            for cat, qtd in zip(labels, valores)
        ]

        # Atualiza gráfico
        img64 = gerar_grafico(df, dropdown_chart.value, cor)
        grafico_img.src_base64 = img64 if img64 else None

        page.update()

    # Eventos de troca de opções
    dropdown_analise.on_change = atualizar
    dropdown_chart.on_change = atualizar

    # Painel da esquerda (filtros, KPI, tabela)
    left_panel = ft.ListView(
        controls=[
            ft.Container(ft.Text(titulo, size=20, weight="bold"), padding=ft.padding.only(bottom=6)),
            ft.Container(dropdown_analise, padding=ft.padding.only(bottom=6)),
            ft.Container(dropdown_chart, padding=ft.padding.only(bottom=6)),
            kpi_card,
            tabela_box
        ],
        width=360,
        padding=ft.padding.all(12),
        spacing=12
    )

    # Painel da direita (gráfico)
    right_panel = ft.Container(
        content=ft.Column([grafico_box], expand=True),
        padding=ft.padding.all(12),
        expand=True
    )

    # Layout com duas colunas
    layout = ft.Row([left_panel, right_panel], expand=True, spacing=36, alignment=ft.alignment.center)

    atualizar()  # inicializa a aba com dados carregados
    return layout


# -----------------------------
# App principal
# -----------------------------
def resource_path(relative_path):
    """ Retorna o caminho absoluto do recurso, compatível com PyInstaller """
    if hasattr(sys, "_MEIPASS"):  # se estiver rodando no exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main(page: Page):
    page.title = "Análise de Perfil dos Beneficiários"
    page.window_width = 1200
    page.window_height = 760
    page.bgcolor = "#ffffff"
    page.padding = ft.padding.all(16)
    page.font_family = "Inter"
    page.window_icon = resource_path("icone.ico")

    # Cabeçalho
    header = ft.Row(
        [
            ft.Text("📉Análise de Perfil dos Beneficiários", size=24, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    # Subtítulo
    subtitle = ft.Text(
        "Este painel apresenta a distribuição dos beneficiários com base nos dados extraídos do sistema.",
        size=14,
        color="#222222"
    )

    # Tema (cores das abas)
    page.theme = ft.Theme(
        tabs_theme=ft.TabsTheme(
            indicator_color="#EAA900",
            unselected_label_color="#555555",
            label_color="#EAA900",
        )
    )

    # Abas principais (Geral, Titulares, Dependentes)
    tabs = ft.Tabs(
        selected_index=0,
        expand=1,
        tabs=[
            ft.Tab(
                tab_content=ft.Text("▤ Geral", color="black"),
                content=render_tab(page, "Análises Gerais", MAP_GERAL, "#015afe", "Beneficiários Cadastrados")
            ), 
            ft.Tab(
                tab_content=ft.Text("👤 Titulares", color="black"),
                content=render_tab(page, "Titulares", MAP_TITULAR, "#015afe", "Titulares Cadastrados")
            ),  
            ft.Tab(
                tab_content=ft.Text("👥 Dependentes", color="black"),
                content=render_tab(page, "Dependentes", MAP_DEP, "#015afe", "Dependentes Cadastrados")
            )
        ]
    )

    # Monta a página
    page.add(header, subtitle, ft.Divider(height=6), tabs)


# -----------------------------
# Execução do app
# -----------------------------
if __name__ == "__main__":
    # view=FLET_APP abre como app desktop
    # poderia ser view=WEB_BROWSER para rodar no navegador
    ft.app(target=main, view=ft.AppView.FLET_APP)
