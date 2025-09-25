# main.py (trecho completo atualizado)
import flet as ft
from flet import Page, icons
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sys, os

from queries import QUERIES, FALLBACK

try:
    from model.database import executar_select
except Exception as e:
    print("⚠️ Não foi possível importar executar_select:", e)
    executar_select = None


# -----------------------------
# Helpers
# -----------------------------
def _to_int_safe(v):
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return 0


def is_color_dark(hexcolor: str) -> bool:
    """Retorna True se hexcolor for escuro (simple luminance check)."""
    if not hexcolor:
        return True
    c = hexcolor.lstrip('#')
    if len(c) != 6:
        return True
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance < 128


def consultar(analise: str):
    if analise not in QUERIES:
        return FALLBACK.get(analise, ([], []))
    if executar_select is None:
        return FALLBACK.get(analise, ([], []))
    try:
        rows = executar_select(QUERIES[analise])
        if not rows:
            return FALLBACK.get(analise, ([], []))
        labels = [r[0] for r in rows]
        valores = [_to_int_safe(r[1]) for r in rows]
        return labels, valores
    except Exception:
        return FALLBACK.get(analise, ([], []))


def gerar_grafico(df: pd.DataFrame, chart_type: str, cor: str, bg_color: str, text_color: str):
    """
    Gera imagem PNG (base64) do gráfico usando as cores de fundo/texto recebidas.
    """
    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))
    # aplicar fundo do gráfico
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    if chart_type == "Gráfico de Barras":
        sns.barplot(data=df, x="Categoria", y="Quantidade", ax=ax, color=cor)
        # cores dos eixos / ticks / labels
        ax.tick_params(colors=text_color)
        ax.yaxis.label.set_color(text_color)
        ax.xaxis.label.set_color(text_color)
        for spine in ax.spines.values():
            spine.set_color(text_color)
        for lbl in ax.get_xticklabels():
            lbl.set_color(text_color)
    else:
        colors = [
            "#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#FACC15", "#EAB308"
        ]
        wedges, texts, autotexts = ax.pie(
            df["Quantidade"],
            labels=df["Categoria"],
            autopct="%1.1f%%",
            startangle=90,
            colors=colors[:len(df)],
            textprops={'color': text_color}
        )
        ax.axis("equal")

    plt.tight_layout()
    buf = BytesIO()
    # garantir que o PNG mantenha o facecolor do fig
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# -----------------------------
# Render de uma aba (dinâmico)
# -----------------------------
def render_tab(page: Page, titulo: str, opcoes_map: dict, cor: str, metric_label: str):
    # cores do tema atual
    bg = page.theme.color_scheme.background
    fg = page.theme.color_scheme.on_background
    card_bg = bg  # cards com mesmo fundo que a página (você pode mudar se quiser)
    border_color = "#e6e6e6" if not is_color_dark(bg) else "#333333"
    shadow = ft.BoxShadow(color="#00000011", blur_radius=8, offset=ft.Offset(0, 2)) if not is_color_dark(bg) else None

    # Label + Dropdown de análise
    analise_label = ft.Text(
        "Escolha a análise", size=14, weight="bold",
        color=page.theme.color_scheme.on_background
    )
    dropdown_analise = ft.Dropdown(
        options=[ft.dropdown.Option(k) for k in opcoes_map.keys()],
        value=list(opcoes_map.keys())[0],
        width=320, 
        color=page.theme.color_scheme.on_background,
        bgcolor=page.theme.color_scheme.background,
        border_color=page.theme.color_scheme.on_background

    )

    # Label + Dropdown de visualização
    chart_label = ft.Text(
        "Tipo de Visualização", size=14, weight="bold",
        color=page.theme.color_scheme.on_background
    )
    dropdown_chart = ft.Dropdown(
        options=[
            ft.dropdown.Option("Gráfico de Barras"),
            ft.dropdown.Option("Gráfico de Pizza")
        ],
        value="Gráfico de Barras",
        width=320,
        color=page.theme.color_scheme.on_background,
        bgcolor=page.theme.color_scheme.background,
        border_color=page.theme.color_scheme.on_background
    )


    kpi_card = ft.Container(
        content=ft.Column([
            ft.Icon(icons.PEOPLE, size=28, color="#EAA900"),
            ft.Text("0", size=28, weight="bold", color=fg),
            ft.Text(metric_label, size=12, color=fg)
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.all(16),
        width=140,
        border_radius=12,
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        shadow=shadow
    )

    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Categoria", color=fg)), ft.DataColumn(ft.Text("Quantidade", color=fg))],
        rows=[],
        width=320
    )
    tabela_box = ft.Container(
        tabela, padding=8, height=370, width=320,
        bgcolor=card_bg, border_radius=12, border=ft.border.all(1, border_color),
        shadow=shadow
    )

    grafico_img = ft.Image(expand=True, fit=ft.ImageFit.CONTAIN)
    grafico_box = ft.Container(
        grafico_img, expand=True, padding=16,
        bgcolor=card_bg, border_radius=12, border=ft.border.all(1, border_color)
    )

    def atualizar(e=None):
        analise_key = opcoes_map[dropdown_analise.value]
        labels, valores = consultar(analise_key)
        df = pd.DataFrame({"Categoria": labels, "Quantidade": valores})

        total = int(df["Quantidade"].sum()) if not df.empty else 0
        kpi_card.content.controls[1].value = f"{total}"

        tabela.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(cat), color=fg)), ft.DataCell(ft.Text(str(qtd), color=fg))])
            for cat, qtd in zip(labels, valores)
        ]

        img64 = gerar_grafico(df, dropdown_chart.value, cor, bg_color=bg, text_color=fg)
        grafico_img.src_base64 = img64 if img64 else None

        page.update()

    dropdown_analise.on_change = atualizar
    dropdown_chart.on_change = atualizar

    left_panel = ft.ListView(
        controls=[
            ft.Container(ft.Text(titulo, size=20, weight="bold", color=fg), padding=ft.padding.only(bottom=6)),
            ft.Container(analise_label, padding=ft.padding.only(bottom=2)),
            ft.Container(dropdown_analise, padding=ft.padding.only(bottom=6)),
            ft.Container(chart_label, padding=ft.padding.only(bottom=2)),
            ft.Container(dropdown_chart, padding=ft.padding.only(bottom=6)),
            kpi_card,
            tabela_box
        ],
        width=360,
        padding=ft.padding.all(12),
        spacing=12
    )


    right_panel = ft.Container(
        content=ft.Column([grafico_box], expand=True),
        padding=ft.padding.all(12),
        expand=True
    )

    layout = ft.Row([left_panel, right_panel], expand=True, spacing=36, alignment=ft.alignment.center)

    atualizar()
    return layout


# -----------------------------
# Temas
# -----------------------------
def tema_claro():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#015afe", background="#ffffff", on_background="#000000"
        ),
        tabs_theme=ft.TabsTheme(
            indicator_color="#015afe",
            unselected_label_color="#555555",
            label_color="#015afe"
        )
    )


def tema_escuro():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#93C5FD", background="#141414", on_background="#ffffff"
        ),
        tabs_theme=ft.TabsTheme(
            indicator_color="#93C5FD",
            unselected_label_color="#bbbbbb",
            label_color="#93C5FD"
        )
    )


# -----------------------------
# App principal (reconstrói UI ao trocar tema)
# -----------------------------
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def main(page: Page):
    tema_atual = {"modo": "claro"}

    page.title = "Análise de Perfil dos Beneficiários"
    page.window_width = 1200
    page.window_height = 760
    page.theme = tema_claro()
    page.bgcolor = page.theme.color_scheme.background
    page.padding = ft.padding.all(16)
    page.font_family = "Inter"
    page.window_icon = resource_path("icone.ico")

    # botão de tema (criado uma vez, será reutilizado)
    botao_tema = ft.IconButton(icon=ft.icons.DARK_MODE, tooltip="Alternar tema")

    def alternar_tema(e):
        if tema_atual["modo"] == "claro":
            tema_atual["modo"] = "escuro"
            page.theme = tema_escuro()
            botao_tema.icon = ft.icons.LIGHT_MODE
        else:
            tema_atual["modo"] = "claro"
            page.theme = tema_claro()
            botao_tema.icon = ft.icons.DARK_MODE

        # atualizar bgcolor do page e reconstruir a UI para reaplicar cores nos controles
        page.bgcolor = page.theme.color_scheme.background
        page.controls.clear()
        build_ui()
        page.update()

    botao_tema.on_click = alternar_tema

    # função que monta a interface (recriada quando tema muda)
    def build_ui():
        header = ft.Row(
            [
                ft.Text("📉 Análise de Perfil dos Beneficiários", size=24, weight="bold", color=page.theme.color_scheme.on_background),
                botao_tema
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10
        )

        subtitle = ft.Text(
            "Este painel apresenta a distribuição dos beneficiários com base nos dados extraídos do sistema.",
            size=14, color=page.theme.color_scheme.on_background
        )

        tabs = ft.Tabs(
            selected_index=0,
            expand=1,
            tabs=[
                ft.Tab(
                    tab_content=ft.Text("▤ Geral", color=page.theme.color_scheme.on_background),
                    content=render_tab(page, "Análises Gerais", MAP_GERAL, "#015afe", "Beneficiários Cadastrados")
                ),
                ft.Tab(
                    tab_content=ft.Text("👤 Titulares", color=page.theme.color_scheme.on_background),
                    content=render_tab(page, "Titulares", MAP_TITULAR, "#015afe", "Titulares Cadastrados")
                ),
                ft.Tab(
                    tab_content=ft.Text("👥 Dependentes", color=page.theme.color_scheme.on_background),
                    content=render_tab(page, "Dependentes", MAP_DEP, "#015afe", "Dependentes Cadastrados")
                )
            ]
        )

        page.add(header, subtitle, ft.Divider(height=6), tabs)

    # Dados de mapas que você já tinha
    global MAP_GERAL, MAP_TITULAR, MAP_DEP
    MAP_GERAL = {
        "Distribuição por Sexo (Segurados)": "sexo_segurados",
        "Perfil Etário da População (Segurados)": "idade_segurados",
        "Alerta (Segurados)": "alerta_segurados",
        "Situação (Segurados)": "situacao_segurados",
        "Carteira (Segurados)": "carteira_segurados",
        "Titular vs Dependente": "titular",
    }
    
    MAP_TITULAR = {
        "Sexo (Titulares)": "sexo_titulares",
        "Idade (Titulares)": "idade_titulares",
        "Alerta (Titulares)": "alerta_titulares",
        "Situação (Titulares)": "situacao_titulares",
        "Carteira (Titulares)": "carteira_titulares",
        "Tempo de vínculo (Titulares)": "tempo_vinculo_titulares",
        "Dependentes (Titulares)": "dependentes_por_titular",
    }
    
    MAP_DEP = {
        "Sexo (Dependentes)": "sexo_dependentes",
        "Idade (Dependentes)": "idade_dependentes",
        "Alerta (Dependentes)": "alerta_dependentes",
        "Situação (Dependentes)": "situacao_dependentes",
        "Carteira (Dependentes)": "carteira_dependentes",
        "Parentesco (Dependentes)": "parentesco_dependentes",
    }

    build_ui()


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
