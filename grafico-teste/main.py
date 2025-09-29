import flet as ft
from app.helpers import resource_path
from app.ui.tabs import render_tab
from app.ui.theme import tema_claro, tema_escuro
from app.settings import MAP_GERAL, MAP_TITULAR, MAP_DEP



def main(page: ft.Page):
    tema_atual = {"modo": "claro"}

    page.title = "Análise de Perfil dos Beneficiários"
    page.window_width = 1200
    page.window_height = 760
    page.theme = tema_claro()
    page.bgcolor = page.theme.color_scheme.background
    page.padding = ft.padding.all(16)
    page.font_family = "Inter"
    page.window_icon = resource_path("icon.ico")

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
        page.bgcolor = page.theme.color_scheme.background
        page.controls.clear()
        build_ui()
        page.update()

    botao_tema.on_click = alternar_tema

    def build_ui():
        header = ft.Row([
            ft.Text("📉 Análise de Perfil dos Beneficiários", size=24, weight="bold", color=page.theme.color_scheme.on_background),
            botao_tema
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)

        subtitle = ft.Text(
            "Este painel apresenta a distribuição dos beneficiários com base nos dados extraídos do sistema.",
            size=14, color=page.theme.color_scheme.on_background
        )

        tabs = ft.Tabs(selected_index=0, expand=1, tabs=[
            ft.Tab(tab_content=ft.Text("▤ Geral", color=page.theme.color_scheme.on_background),
                   content=render_tab(page, "Análises Gerais", MAP_GERAL, "#015afe", "Beneficiários Cadastrados")),
            ft.Tab(tab_content=ft.Text("👤 Titulares", color=page.theme.color_scheme.on_background),
                   content=render_tab(page, "Titulares", MAP_TITULAR, "#015afe", "Titulares Cadastrados")),
            ft.Tab(tab_content=ft.Text("👥 Dependentes", color=page.theme.color_scheme.on_background),
                   content=render_tab(page, "Dependentes", MAP_DEP, "#015afe", "Dependentes Cadastrados"))
        ])

        page.add(header, subtitle, ft.Divider(height=6), tabs)

    build_ui()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
